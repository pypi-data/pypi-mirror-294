import logging
import traceback
from pydoc import locate
from typing import TYPE_CHECKING, Optional

from confluent_kafka import Consumer as ConfluentConsumer
from confluent_kafka import cimpl

from django_kafka.conf import settings
from django_kafka.exceptions import DjangoKafkaError

if TYPE_CHECKING:
    from django_kafka.topic import Topic

logger = logging.getLogger(__name__)


class Topics:
    _topics: tuple["Topic", ...]
    _match: dict[str, "Topic"]

    def __init__(self, *topics: "Topic"):
        self._topics = topics
        self._match: dict[str, "Topic"] = {}

    def get_topic(self, name: str) -> "Topic":
        if name not in self._match:
            topic = next((t for t in self if t.matches(name)), None)
            if not topic:
                raise DjangoKafkaError(f"No topic registered for `{name}`")
            self._match[name] = topic

        return self._match[name]

    @property
    def names(self) -> list[str]:
        return [topic.name for topic in self]

    def __iter__(self):
        yield from self._topics


class Consumer:
    """
    Available settings of the producers (P) and consumers (C)
        https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md
    Consumer configs
        https://kafka.apache.org/documentation/#consumerconfigs
    Kafka Client Configuration
        https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#kafka-client-configuration
    confluent_kafka.Consumer API
        https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#pythonclient-consumer
    """

    topics: Topics
    config: dict

    polling_freq = settings.POLLING_FREQUENCY
    default_logger = logger
    default_error_handler = settings.ERROR_HANDLER

    def __init__(self, **kwargs):
        kwargs.setdefault("logger", self.default_logger)
        kwargs.setdefault("error_cb", locate(self.default_error_handler)())

        self.config = self.build_config()
        self._consumer = ConfluentConsumer(self.config, **kwargs)

    def __getattr__(self, name):
        """proxy consumer methods."""
        if name not in {"config"}:
            # For cases when `Consumer.config` is not set and
            #  `getattr(self, "config", {})` is called on `__init__`,
            #  the initialization will fail because `_consumer` is not yet set.
            return getattr(self._consumer, name)
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute 'name'")

    @classmethod
    def build_config(cls):
        return {
            "client.id": settings.CLIENT_ID,
            **settings.GLOBAL_CONFIG,
            **settings.CONSUMER_CONFIG,
            **getattr(cls, "config", {}),
        }

    @property
    def group_id(self) -> str:
        return self.config["group.id"]

    def commit_offset(self, msg: cimpl.Message):
        if not self.config.get("enable.auto.offset.store"):
            # Store the offset associated with msg to a local cache.
            # Stored offsets are committed to Kafka by a background
            #  thread every 'auto.commit.interval.ms'.
            # Explicitly storing offsets after processing gives at-least once semantics.
            self.store_offsets(msg)

    def handle_exception(self, msg: cimpl.Message, exc: Exception):
        from django_kafka.dead_letter.topic import DeadLetterTopic
        from django_kafka.retry.topic import RetryTopic

        topic = self.get_topic(msg)

        retried = False
        if topic.retry:
            retried = RetryTopic(group_id=self.group_id, main_topic=topic).retry_for(
                msg=msg,
                exc=exc,
            )

        if not retried:
            DeadLetterTopic(group_id=self.group_id, main_topic=topic).produce_for(
                msg=msg,
                header_message=str(exc),
                header_detail=traceback.format_exc(),
            )
            self.log_error(exc)

    def get_topic(self, msg: cimpl.Message) -> "Topic":
        return self.topics.get_topic(name=msg.topic())

    def log_error(self, error):
        logger.error(error, exc_info=True)

    def process_message(self, msg: cimpl.Message):
        if msg_error := msg.error():
            self.log_error(msg_error)
            return

        try:
            self.get_topic(msg).consume(msg)
        # ruff: noqa: BLE001 (we do not want consumer to stop if message processing is failing in any circumstances)
        except Exception as exc:
            self.handle_exception(msg, exc)

        self.commit_offset(msg)

    def poll(self) -> Optional[cimpl.Message]:
        # poll for self.polling_freq seconds
        return self._consumer.poll(timeout=self.polling_freq)

    def start(self):
        # define topics
        self.subscribe(topics=self.topics.names)
        while True:
            if msg := self.poll():
                self.process_message(msg)

    def stop(self):
        self.close()

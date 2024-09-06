import logging
import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Type

from confluent_kafka import cimpl
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import (
    Deserializer,
    MessageField,
    SerializationContext,
    Serializer,
    StringDeserializer,
    StringSerializer,
)

from django_kafka import kafka
from django_kafka.exceptions import DjangoKafkaError

if TYPE_CHECKING:
    from django_kafka.retry import RetrySettings

logger = logging.getLogger(__name__)


class Topic(ABC):
    key_serializer: Type[Serializer] = StringSerializer
    value_serializer: Type[Serializer] = StringSerializer

    key_deserializer: Type[Deserializer] = StringDeserializer
    value_deserializer: Type[Deserializer] = StringDeserializer

    retry_settings: Optional["RetrySettings"] = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Define Kafka topic name

        Regexp pattern subscriptions are supported by prefixing the name with "^". If
        used, then a name must always be supplied to .produce() method.
        """

    @property
    def retry(self) -> bool:
        """returns whether failure of message consumption should retry"""
        return self.retry_settings is not None

    def is_regex(self):
        """returns if the topic subscription is regex based"""
        return self.name.startswith("^")

    def validate_produce_name(self, name: Optional[str]) -> str:
        """validates and returns the topic producing name"""
        if name:
            if self.matches(name):
                return name
            raise DjangoKafkaError(
                f"topic producing name `{name}` is not valid for this topic",
            )
        if self.is_regex():
            raise DjangoKafkaError(
                "topic producing name must be supplied for regex-based topics",
            )
        return self.name

    def matches(self, topic_name: str):
        if self.is_regex():
            return bool(re.search(self.name, topic_name))
        return self.name == topic_name

    def consume(self, msg: cimpl.Message):
        """Implement message processing"""
        raise NotImplementedError

    def produce(self, value: any, **kwargs):
        name = self.validate_produce_name(kwargs.pop("name", None))
        key_serializer_kwargs = kwargs.pop("key_serializer_kwargs", {}) or {}
        value_serializer_kwargs = kwargs.pop("value_serializer_kwargs", {}) or {}
        headers = kwargs.get("headers")

        if "key" in kwargs:
            kwargs["key"] = self.serialize(
                name,
                kwargs["key"],
                MessageField.KEY,
                headers,
                **key_serializer_kwargs,
            )

        kafka.producer.produce(
            name,
            self.serialize(
                name,
                value,
                MessageField.VALUE,
                headers,
                **value_serializer_kwargs,
            ),
            **kwargs,
        )
        kafka.producer.poll(0)  # stops producer on_delivery callbacks buffer overflow

    def serialize(
        self,
        name,
        value,
        field: MessageField,
        headers: Optional[list] = None,
        **kwargs,
    ):
        if field == MessageField.VALUE:
            serializer = self.get_value_serializer(**kwargs)
            return serializer(
                value,
                self.context(name, MessageField.VALUE, headers),
            )

        if field == MessageField.KEY:
            serializer = self.get_key_serializer(**kwargs)
            return serializer(
                value,
                self.context(name, MessageField.KEY, headers),
            )

        raise DjangoKafkaError(f"Unsupported serialization field {field}.")

    def deserialize(
        self,
        name,
        value,
        field: MessageField,
        headers: Optional[list] = None,
        **kwargs,
    ):
        if field == MessageField.VALUE:
            deserializer = self.get_value_deserializer(**kwargs)
            return deserializer(
                value,
                self.context(name, MessageField.VALUE, headers),
            )

        if field == MessageField.KEY:
            deserializer = self.get_key_deserializer(**kwargs)
            return deserializer(
                value,
                self.context(name, MessageField.KEY, headers),
            )

        raise DjangoKafkaError(f"Unsupported deserialization field {field}.")

    def get_key_serializer(self, **kwargs):
        return self.key_serializer(**kwargs)

    def get_value_serializer(self, **kwargs):
        return self.value_serializer(**kwargs)

    def get_key_deserializer(self, **kwargs):
        return self.key_deserializer(**kwargs)

    def get_value_deserializer(self, **kwargs):
        return self.value_deserializer(**kwargs)

    def context(
        self,
        name: str,
        field: MessageField,
        headers: Optional[list] = None,
    ) -> SerializationContext:
        return SerializationContext(name, field, headers=headers)


class AvroTopic(Topic, ABC):
    """
    Consume.
        Defining schemas is not necessary as it gets retrieved automatically from the Schema Registry.

    Produce.
        Defining `value_schema` is required (`key_schema` is required when using keys).
        It gets submitted to the Schema Registry

    Multiple schemas and one Topic:
        `AvroTopic.produce` takes `serializer_kwargs` kw argument.
        `AvroSerializer` then gets initialized with the provided kwargs.
        When producing you can tell which schema to use for your message:
        ```python
        schema = {
            "type": "record",
            "name": "ValueTest",
            "fields": [
                {"name": "value", "type": "string"},
            ]
        }
        topic.produce({"value": 1}, value_serializer_kwargs={"schema_str": json.dumps(schema)})
        ```

    [Cofluent AvroSerializer Config](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#avroserializer)
    [Avro schema definition](https://avro.apache.org/docs/1.11.1/specification/)
    """  # noqa: E501

    key_schema: str
    value_schema: str
    schema_config: dict

    def get_key_serializer(self, **kwargs):
        kwargs.setdefault("schema_str", getattr(self, "key_schema", None))
        kwargs.setdefault("conf", getattr(self, "schema_config", None))

        return AvroSerializer(kafka.schema_client, **kwargs)

    def get_value_serializer(self, **kwargs):
        kwargs.setdefault("schema_str", getattr(self, "value_schema", None))
        kwargs.setdefault("conf", getattr(self, "schema_config", None))

        return AvroSerializer(kafka.schema_client, **kwargs)

    def get_key_deserializer(self, **kwargs):
        return AvroDeserializer(kafka.schema_client, **kwargs)

    def get_value_deserializer(self, **kwargs):
        return AvroDeserializer(kafka.schema_client, **kwargs)

import traceback
from contextlib import suppress
from unittest.mock import MagicMock, Mock, call, patch

from django.test import TestCase, override_settings

from django_kafka.conf import SETTINGS_KEY, settings
from django_kafka.consumer import Consumer, Topics


class StopWhileTrueError(Exception):
    pass


class ConsumerTestCase(TestCase):
    @patch(
        "django_kafka.consumer.Consumer.process_message",
        side_effect=StopWhileTrueError(),
    )
    @patch(
        "django_kafka.consumer.ConfluentConsumer",
        **{
            # first iteration - no message,
            # second iteration - 1 message represented as boolean value for testing
            "return_value.poll.side_effect": [None, True],
        },
    )
    def test_start(self, mock_consumer_client, mock_process_message):
        class SomeConsumer(Consumer):
            topics = MagicMock()
            config = {}

        consumer = SomeConsumer()

        # hack to break infinite loop
        # `consumer.start` is using `while True:` loop which never ends
        # in order to test it we need to break it which is achievable with side_effect
        with suppress(StopWhileTrueError):
            consumer.start()

        # subscribed to the topics defined by consumer class
        mock_consumer_client.return_value.subscribe.assert_called_once_with(
            topics=consumer.topics.names,
        )
        # poll for message with the frequency defined by consumer class
        self.assertEqual(
            mock_consumer_client.return_value.poll.call_args_list,
            # 2 calls expected as we setup 2 iterations in the test
            [call(timeout=consumer.polling_freq)] * 2,
        )
        # process_message called once as there was no message on the first iteration
        mock_process_message.assert_called_once_with(True)

    @patch("django_kafka.consumer.Consumer.commit_offset")
    @patch("django_kafka.consumer.ConfluentConsumer")
    def test_process_message_success(self, mock_consumer_client, mock_commit_offset):
        class SomeConsumer(Consumer):
            topics = MagicMock()
            config = {}

        msg = Mock(error=Mock(return_value=False))

        consumer = SomeConsumer()

        consumer.process_message(msg)

        # check if msg has error before processing
        msg.error.assert_called_once_with()
        # Topic.consume called
        consumer.get_topic(msg.topic()).consume.assert_called_once_with(msg)
        # commit_offset triggered
        mock_commit_offset.assert_called_once_with(msg)

    @patch("django_kafka.consumer.Consumer.log_error")
    @patch("django_kafka.consumer.Consumer.commit_offset")
    @patch("django_kafka.consumer.ConfluentConsumer")
    def test_process_message_msg_error_logged(
        self,
        mock_consumer_client,
        mock_commit_offset,
        log_error,
    ):
        class SomeConsumer(Consumer):
            topics = MagicMock()
            config = {}

        msg = Mock(error=Mock(return_value=True))

        consumer = SomeConsumer()

        consumer.process_message(msg)

        # check if msg has error before processing
        msg.error.assert_called_once_with()
        # error handler was triggered
        log_error.assert_called_once_with(msg.error.return_value)
        # Topic.consume is not called
        consumer.topics[msg.topic()].consume.assert_not_called()
        # Consumer.commit_offset is not called
        mock_commit_offset.assert_not_called()

    @patch("django_kafka.consumer.Consumer.handle_exception")
    @patch("django_kafka.consumer.Consumer.commit_offset")
    @patch("django_kafka.consumer.ConfluentConsumer")
    def test_process_message_exception(
        self,
        mock_consumer_client,
        mock_commit_offset,
        handle_exception,
    ):
        topic_consume_side_effect = TypeError("test")
        topic = Mock(
            **{
                "name": "topic",
                "consume.side_effect": topic_consume_side_effect,
            },
        )
        msg = Mock(**{"topic.return_value": topic.name, "error.return_value": False})

        class SomeConsumer(Consumer):
            topics = Topics(topic)
            config = {}

        consumer = SomeConsumer()

        consumer.process_message(msg)

        # check if msg has error before processing
        msg.error.assert_called_once_with()
        # Topic.consume was triggered
        topic.consume.assert_called_once_with(msg)
        # error handler was triggered on exception
        handle_exception.assert_called_once_with(msg, topic_consume_side_effect)
        # Consumer.commit_offset is not called
        mock_commit_offset.assert_called_once()

    @patch("django_kafka.dead_letter.topic.DeadLetterTopic")
    @patch("django_kafka.retry.topic.RetryTopic")
    @patch("django_kafka.consumer.ConfluentConsumer")
    def test_handle_exception__retry_behaviour(
        self,
        mock_consumer_client,
        mock_retry_topic_cls,
        mock_dead_letter_topic_cls,
    ):
        topic = Mock(name="topic", retry=True)
        msg = Mock(**{"topic.return_value": topic.name})
        mock_retry_topic_cls.return_value.retry_for.return_value = True

        class SomeConsumer(Consumer):
            topics = Topics(topic)
            config = {"group.id": "group_id"}
            log_error = Mock()

        consumer = SomeConsumer()
        exc = ValueError()

        consumer.handle_exception(msg, exc)

        mock_retry_topic_cls.assert_called_once_with(
            group_id=consumer.group_id,
            main_topic=topic,
        )
        mock_retry_topic_cls.return_value.retry_for.assert_called_once_with(
            msg=msg,
            exc=exc,
        )
        mock_dead_letter_topic_cls.assert_not_called()
        consumer.log_error.assert_not_called()

    @patch("django_kafka.dead_letter.topic.DeadLetterTopic")
    @patch("django_kafka.retry.topic.RetryTopic")
    @patch("django_kafka.consumer.ConfluentConsumer")
    def test_handle_exception__dead_letter_behaviour(
        self,
        mock_consumer_client,
        mock_retry_topic_cls,
        mock_dead_letter_topic_cls,
    ):
        topic = Mock(name="topic", retry=False)
        msg = Mock(**{"topic.return_value": topic.name})

        class SomeConsumer(Consumer):
            topics = Topics(topic)
            config = {"group.id": "group_id"}
            log_error = Mock()

        consumer = SomeConsumer()
        exc = ValueError("error")

        consumer.handle_exception(msg, exc)

        mock_retry_topic_cls.return_value.assert_not_called()
        mock_dead_letter_topic_cls.assert_called_once_with(
            group_id=consumer.group_id,
            main_topic=topic,
        )
        mock_dead_letter_topic_cls.return_value.produce_for.assert_called_once_with(
            msg=msg,
            header_message=str(exc),
            header_detail=traceback.format_exc(),
        )
        consumer.log_error.assert_called_once_with(exc)

    @patch("django_kafka.consumer.ConfluentConsumer")
    def test_auto_offset_false(self, mock_consumer_client):
        class SomeConsumer(Consumer):
            config = {"enable.auto.offset.store": False}

        consumer = SomeConsumer()

        msg = Mock()
        consumer.commit_offset(msg)

        mock_consumer_client.return_value.store_offsets.assert_called_once_with(msg)

    @patch("django_kafka.consumer.ConfluentConsumer")
    def test_auto_offset_true(self, mock_consumer_client):
        class SomeConsumer(Consumer):
            config = {"enable.auto.offset.store": True}

        consumer = SomeConsumer()

        consumer.commit_offset(Mock())

        mock_consumer_client.return_value.store_offsets.assert_not_called()

    def test_settings_are_correctly_assigned(self):
        self.assertEqual(Consumer.polling_freq, settings.POLLING_FREQUENCY)
        self.assertEqual(Consumer.default_error_handler, settings.ERROR_HANDLER)

    @override_settings(
        **{
            SETTINGS_KEY: {
                "CLIENT_ID": "client.id-initial-definition",
                "GLOBAL_CONFIG": {
                    "client.id": "client-id-overridden-by-global-config",
                    "bootstrap.servers": "defined-in-global-config",
                },
                "CONSUMER_CONFIG": {
                    "bootstrap.servers": "bootstrap.servers-overridden-by-consumer",
                    "group.id": "group.id-defined-by-consumer-config",
                },
            },
        },
    )
    @patch("django_kafka.consumer.ConfluentConsumer")
    def test_init_config_merge_override(self, mock_consumer_client):
        """
        1. CLIENT_ID is added to the consumers config
        2. GLOBAL_CONFIG overrides CLIENT_ID (client.id) if it contains one
        3. CONSUMER_CONFIG merges with GLOBAL_CONFIG and overrides keys if any
        4. Consumer.config is merged with CONSUMER_CONFIG and overrides keys if any
        4. Lastly `config` provided to Consumer.__init__ merges and overrides everything
        """

        class SomeConsumer(Consumer):
            config = {
                "group.id": "group.id.overridden-by-consumer-class",
                "enable.auto.offset.store": True,
            }

        # Consumer.config is properly merged
        consumer = SomeConsumer()

        self.assertDictEqual(
            consumer.build_config(),
            {
                "client.id": "client-id-overridden-by-global-config",
                "bootstrap.servers": "bootstrap.servers-overridden-by-consumer",
                "group.id": "group.id.overridden-by-consumer-class",
                "enable.auto.offset.store": True,
            },
        )
        self.assertDictEqual(
            consumer.build_config(),
            consumer.config,
        )

    def test_group_id_property(self):
        class SomeConsumer(Consumer):
            config = {"group.id": "group.id"}

        consumer = SomeConsumer()

        self.assertEqual(consumer.group_id, "group.id")

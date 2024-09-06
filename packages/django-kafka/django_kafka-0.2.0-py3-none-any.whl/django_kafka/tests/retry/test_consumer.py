import datetime
import traceback
from unittest import mock

from confluent_kafka import TopicPartition
from django.test import TestCase
from django.utils import timezone

from django_kafka import Retry
from django_kafka.consumer import Consumer, Topics
from django_kafka.retry.consumer import RetryConsumer, RetryTopics
from django_kafka.retry.headers import RetryHeader
from django_kafka.topic import Topic


class RetryConsumerTestCase(TestCase):
    def _get_topic(self):
        class NormalTopic(Topic):
            name = "normal_topic"

        return NormalTopic()

    def _get_retryable_topic(self):
        class RetryableTopic(Topic):
            name = "retry_topic"

        retry = Retry()
        retry(max_retries=5, delay=60)(RetryableTopic)

        return RetryableTopic()

    def _get_retryable_consumer_cls(self):
        class TestConsumer(Consumer):
            topics = Topics(self._get_topic(), self._get_retryable_topic())
            config = {"group.id": "group_id"}

        return TestConsumer

    def _get_retry_consumer(self):
        return RetryConsumer.build(self._get_retryable_consumer_cls())()

    def test_build(self):
        consumer_cls = self._get_retryable_consumer_cls()
        retry_consumer_cls = RetryConsumer.build(consumer_cls)

        self.assertTrue(issubclass(retry_consumer_cls, RetryConsumer))

        self.assertEqual(
            retry_consumer_cls.config["group.id"],
            f"{consumer_cls.build_config()['group.id']}.retry",
        )
        self.assertIsInstance(retry_consumer_cls.topics, RetryTopics)
        self.assertCountEqual(
            [t for t in consumer_cls.topics if t.retry],
            [t.main_topic for t in retry_consumer_cls.topics],
        )

    def test_build__no_retry_topics(self):
        class TestConsumer(Consumer):
            topics = Topics()
            config = {}

        self.assertIsNone(RetryConsumer.build(TestConsumer))

    @mock.patch("django_kafka.retry.consumer.DeadLetterTopic")
    @mock.patch("django_kafka.consumer.ConfluentConsumer")
    def test_handle_exception__retry_behaviour(
        self,
        mock_consumer_client,
        mock_dead_letter_topic_cls,
    ):
        retry_consumer = self._get_retry_consumer()
        retry_consumer.log_error = mock.Mock()
        retry_topic = next(iter(retry_consumer.topics))
        retry_topic.retry_for = mock.Mock(return_value=True)
        exc = ValueError()
        msg_mock = mock.Mock(
            **{
                "topic.return_value": retry_topic.get_produce_name(
                    retry_topic.main_topic.name,
                    attempt=1,
                ),
            },
        )

        retry_consumer.handle_exception(msg_mock, exc)

        retry_topic.retry_for.assert_called_once_with(msg=msg_mock, exc=exc)
        mock_dead_letter_topic_cls.assert_not_called()
        retry_consumer.log_error.assert_not_called()

    @mock.patch("django_kafka.retry.consumer.DeadLetterTopic")
    @mock.patch("django_kafka.consumer.ConfluentConsumer")
    def test_handle_exception__dead_letter_behaviour(
        self,
        mock_consumer_client,
        mock_dead_letter_topic_cls,
    ):
        retry_consumer = self._get_retry_consumer()
        retry_consumer.log_error = mock.Mock()
        retry_topic = next(iter(retry_consumer.topics))
        retry_topic.retry_for = mock.Mock(return_value=False)
        exc = ValueError()
        msg_mock = mock.Mock(
            **{
                "topic.return_value": retry_topic.get_produce_name(
                    retry_topic.main_topic.name,
                    attempt=1,
                ),
            },
        )
        retry_consumer.handle_exception(msg_mock, exc)

        retry_topic.retry_for.assert_called_once_with(msg=msg_mock, exc=exc)
        mock_dead_letter_topic_cls.assert_called_once_with(
            group_id=retry_topic.group_id,
            main_topic=retry_topic.main_topic,
        )
        mock_dead_letter_topic_cls.return_value.produce_for.assert_called_once_with(
            msg=msg_mock,
            header_message=str(exc),
            header_detail=traceback.format_exc(),
        )
        retry_consumer.log_error.assert_called_once_with(exc)

    @mock.patch("django_kafka.consumer.ConfluentConsumer")
    def test_pause_partition(self, mock_confluent_consumer):
        retry_consumer = self._get_retry_consumer()
        mock_msg = mock.Mock(
            **{
                "topic.return_value": "msg_topic",
                "partition.return_value": 0,
                "offset.return_value": 0,
            },
        )
        partition = TopicPartition(
            mock_msg.topic(),
            mock_msg.partition(),
            mock_msg.offset(),
        )
        retry_time = timezone.now()

        retry_consumer.pause_partition(mock_msg, retry_time)

        mock_confluent_consumer.return_value.seek.assert_called_once_with(partition)
        mock_confluent_consumer.return_value.pause.assert_called_once_with([partition])

    @mock.patch("django_kafka.consumer.ConfluentConsumer")
    def test_resume_partition__before_retry_time(self, mock_confluent_consumer):
        retry_consumer = self._get_retry_consumer()
        mock_msg = mock.Mock(
            **{
                "topic.return_value": "msg_topic",
                "partition.return_value": 0,
                "offset.return_value": 0,
            },
        )
        retry_time = timezone.now() + datetime.timedelta(minutes=1)

        retry_consumer.pause_partition(mock_msg, retry_time)
        retry_consumer.resume_ready_partitions()

        mock_confluent_consumer.return_value.resume.assert_not_called()

    @mock.patch("django_kafka.consumer.ConfluentConsumer")
    def test_resume_ready_partitions__after_retry_time(self, mock_confluent_consumer):
        retry_consumer = self._get_retry_consumer()
        mock_msg = mock.Mock(
            **{
                "topic.return_value": "msg_topic",
                "partition.return_value": 0,
                "offset.return_value": 0,
            },
        )
        partition = TopicPartition(
            mock_msg.topic(),
            mock_msg.partition(),
            mock_msg.offset(),
        )
        retry_time = timezone.now() - datetime.timedelta(minutes=1)

        retry_consumer.pause_partition(mock_msg, retry_time)
        retry_consumer.resume_ready_partitions()

        mock_confluent_consumer.return_value.resume.assert_called_once_with([partition])

    @mock.patch("django_kafka.consumer.ConfluentConsumer")
    def test_poll(self, mock_confluent_consumer):
        """tests poll resumes partitions"""
        retry_consumer = self._get_retry_consumer()
        retry_consumer.resume_ready_partitions = mock.Mock()
        mock_msg = mock.Mock()
        mock_confluent_consumer.return_value.poll.return_value = mock_msg

        msg = retry_consumer.poll()

        self.assertEqual(msg, mock_msg)
        retry_consumer.resume_ready_partitions.assert_called_once()  # always called

    @mock.patch("django_kafka.consumer.Consumer.process_message")
    @mock.patch("django_kafka.consumer.ConfluentConsumer")
    def test_process_message__before_retry_time(
        self,
        mock_confluent_consumer,
        mock_consumer_process_message,
    ):
        retry_consumer = self._get_retry_consumer()
        retry_consumer.pause_partition = mock.Mock()
        retry_time = timezone.now() + datetime.timedelta(minutes=1)
        mock_msg = mock.Mock(
            **{
                "error.return_value": None,
                "headers.return_value": [
                    (RetryHeader.TIMESTAMP, str(retry_time.timestamp())),
                ],
            },
        )

        retry_consumer.process_message(mock_msg)
        retry_consumer.pause_partition.assert_called_once_with(mock_msg, retry_time)
        mock_consumer_process_message.process_message.assert_not_called()

    @mock.patch("django_kafka.consumer.Consumer.process_message")
    @mock.patch("django_kafka.consumer.ConfluentConsumer")
    def test_process_message__after_retry_time(
        self,
        mock_confluent_consumer,
        mock_consumer_process_message,
    ):
        retry_consumer = self._get_retry_consumer()
        retry_consumer.pause_partition = mock.Mock()
        retry_time = timezone.now() - datetime.timedelta(minutes=1)
        mock_msg = mock.Mock(
            **{
                "error.return_value": None,
                "headers.return_value": [
                    (RetryHeader.TIMESTAMP, str(retry_time.timestamp())),
                ],
            },
        )

        retry_consumer.process_message(mock_msg)

        retry_consumer.pause_partition.assert_not_called()
        mock_consumer_process_message.assert_called_once_with(mock_msg)

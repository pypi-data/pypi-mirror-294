from typing import TYPE_CHECKING, Optional, Type

from django.utils import timezone

if TYPE_CHECKING:
    from django_kafka.topic import Topic


class RetrySettings:
    def __init__(
        self,
        max_retries: int,
        delay: int,
        backoff: bool = False,
        include: Optional[list[Type[Exception]]] = None,
        exclude: Optional[list[Type[Exception]]] = None,
    ):
        """
        :param max_retries: maximum number of retry attempts
        :param delay: delay (seconds)
        :param backoff: exponential backoff
        :param include: exception types to retry for
        :param exclude: exception types to exclude from retry
        """
        if max_retries <= 0:
            raise ValueError("max_retries must be greater than zero")
        if delay <= 0:
            raise ValueError("delay must be greater than zero")
        if include is not None and exclude is not None:
            raise ValueError("cannot specify both include and exclude")

        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff
        self.include = include
        self.exclude = exclude

    def attempts_exceeded(self, attempt):
        return attempt >= self.max_retries

    def should_retry(self, exc: Exception) -> bool:
        if self.include is not None:
            return any(isinstance(exc, e) for e in self.include)
        if self.exclude is not None:
            return not any(isinstance(exc, e) for e in self.exclude)

        return True

    def get_retry_timestamp(self, attempt: int) -> str:
        delay = self.delay * 2 ** (attempt - 1) if self.backoff else self.delay
        return str(timezone.now().timestamp() + delay)


class Retry:
    def __call__(self, *args, **kwargs):
        def add_retry_settings(topic_cls: Type["Topic"]):
            topic_cls.retry_settings = RetrySettings(*args, **kwargs)
            return topic_cls

        return add_retry_settings

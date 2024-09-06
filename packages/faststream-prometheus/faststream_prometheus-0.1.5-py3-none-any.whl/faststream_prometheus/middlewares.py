from __future__ import annotations

import logging
from logging import Logger
from types import TracebackType
from typing import Any, Optional, Type

from faststream import BaseMiddleware
from faststream.broker.message import StreamMessage
from prometheus_client import CollectorRegistry

from faststream_prometheus.collectors import SafeFaststreamCollector

try:
    from faststream.kafka.message import KafkaMessage

except ImportError:
    KafkaMessage = None

try:
    from faststream.nats.message import NatsMessage

except ImportError:
    NatsMessage = None

try:
    from faststream.rabbit.message import RabbitMessage

except ImportError:
    RabbitMessage = None

try:
    from faststream.redis.message import RedisMessage

except ImportError:
    RedisMessage = None


logger = logging.getLogger('faststream_prometheus')


class FaststreamPrometheusMiddleware(BaseMiddleware):
    msg: Optional[Any] = None

    def __init__(self, registry: Optional[CollectorRegistry] = None, prefix: str = 'faststream'):
        self.faststream_collector_group = SafeFaststreamCollector.get_collector(registry, prefix)

    async def on_receive(self) -> None:
        self.faststream_collector_group.on_receive()
        return await super().on_receive()

    async def after_processed(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> Optional[bool]:
        """Asynchronously called after processing."""
        if exc_val is not None:
            self.faststream_collector_group.was_exception(exc_val)

        return False

    async def on_consume(self, msg: StreamMessage[Any]) -> StreamMessage[Any]:
        self.faststream_collector_group.receive_message(msg)

        if KafkaMessage is not None and isinstance(msg, KafkaMessage):
            self.faststream_collector_group.receive_kafka_message(msg)

        elif RedisMessage is not None and isinstance(msg, RedisMessage):
            self.faststream_collector_group.receive_redis_message(msg)

        elif RabbitMessage is not None and isinstance(msg, RabbitMessage):
            self.faststream_collector_group.receive_rabbit_message(msg)

        elif NatsMessage is not None and isinstance(msg, NatsMessage):
            self.faststream_collector_group.receive_nats_message(msg)

        elif isinstance(msg, Logger):
            pass

        else:
            logger.warning(f'Unexpected message type: {type(logger)}')

        return await super().on_consume(msg)

    async def on_publish(self, msg: Any, *args: Any, **kwargs: Any) -> Any:
        self.faststream_collector_group.on_publish()

        return await super().on_publish(msg, *args, **kwargs)

    async def after_publish(self, err: Optional[Exception]) -> None:
        self.faststream_collector_group.after_publish(err)

        return await super().after_publish(err)

    def __call__(self, msg: Optional[Any]) -> FaststreamPrometheusMiddleware:
        self.msg = msg
        return self

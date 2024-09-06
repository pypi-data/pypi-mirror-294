from __future__ import annotations

import typing
from typing import Any, Dict, Iterable, Optional, Self

from prometheus_client import REGISTRY, CollectorRegistry, Counter, Gauge, Histogram
from prometheus_client.metrics_core import Metric
from prometheus_client.registry import Collector

if typing.TYPE_CHECKING:
    from faststream.broker.message import StreamMessage
    from faststream.kafka.message import KafkaMessage
    from faststream.nats.message import NatsMessage
    from faststream.rabbit.message import RabbitMessage
    from faststream.redis.message import RedisMessage

# _m_kafka_received_message_value_size_buckets = tuple(
#     [1, 5, 10] + [25 * i for i in range(1, 9)] + [50 * i for i in range(5, 11)] + [100 * i for i in range(5, 11)]
# )
_m_kafka_received_message_value_size_buckets = tuple([100 * i for i in range(0, 11)])


class FaststreamCollector(Collector):
    registry: CollectorRegistry
    namespace: str

    def __init__(self, registry: Optional[CollectorRegistry], namespace: str) -> None:
        if not isinstance(registry, CollectorRegistry):
            registry = REGISTRY

        self.registry = registry
        self.namespace = namespace

        self._m_exceptions = Counter(
            'exceptions',
            'Count of exceptions',
            labelnames=['type'],
            namespace=self.namespace,
            registry=self.registry,
        )

        self._m_received_message = Counter(
            'messages_received',
            'Count of received messages',
            labelnames=['type'],
            namespace=self.namespace,
            registry=self.registry,
        )

        self._m_kafka_received_message = Counter(
            'kafka_messages_received',
            'Count of received Kafka messages',
            labelnames=['topic', 'partition'],
            namespace=self.namespace,
            registry=self.registry,
        )

        self._m_kafka_offset = Gauge(
            'kafka_offset',
            'Count of received Kafka messages',
            labelnames=['topic', 'partition'],
            namespace=self.namespace,
            registry=self.registry,
        )

        self._m_kafka_received_message_key_size = Histogram(
            'kafka_messages_received_key_size',
            'Histogram Size of key of received Kafka messages',
            labelnames=['topic', 'partition'],
            namespace=self.namespace,
            registry=self.registry,
            buckets=_m_kafka_received_message_value_size_buckets,
        )

        self._m_kafka_received_message_value_size = Histogram(
            'kafka_messages_received_value_size',
            'Histogram Size of value of received Kafka messages',
            labelnames=['topic', 'partition'],
            namespace=self.namespace,
            registry=self.registry,
            buckets=_m_kafka_received_message_value_size_buckets,
        )

        self._m_redis_received_message = Counter(
            'redis_messages_received',
            'Count of received Redis messages',
            labelnames=[],
            namespace=self.namespace,
            registry=self.registry,
        )
        self._m_rabbit_received_message = Counter(
            'rabbit_messages_received',
            'Count of received Rabbit messages',
            labelnames=[],
            namespace=self.namespace,
            registry=self.registry,
        )
        self._m_nats_received_message = Counter(
            'nats_messages_received',
            'Count of received Nats messages',
            labelnames=[],
            namespace=self.namespace,
            registry=self.registry,
        )

    def on_receive(self):
        pass

    def on_publish(self):
        pass

    def after_publish(self, ex: Optional[Exception] = None):
        if ex is None:
            return

    def was_exception(self, ex: BaseException):
        self._m_exceptions.labels(
            type=ex.__class__.__name__,
        ).inc()

    def receive_message(self, message: StreamMessage[Any]):
        self._m_received_message.labels(
            type=message.__class__.__name__,
        ).inc()

    def receive_kafka_message(self, message: KafkaMessage):
        if isinstance(message.raw_message, tuple):
            records = message.raw_message

        else:
            records = (message.raw_message,)

        for record in records:
            self._m_kafka_received_message.labels(
                topic=record.topic,
                partition=str(record.partition),
            ).inc()

            self._m_kafka_received_message_key_size.labels(
                topic=record.topic,
                partition=str(record.partition),
            ).observe(record.serialized_key_size)

            self._m_kafka_received_message_value_size.labels(
                topic=record.topic,
                partition=str(record.partition),
            ).observe(record.serialized_value_size)

            self._m_kafka_offset.labels(
                topic=record.topic,
                partition=str(record.partition),
            ).set(record.offset)

    def receive_redis_message(self, message: RedisMessage):
        self._m_redis_received_message.labels().inc()

    def receive_rabbit_message(self, message: RabbitMessage):
        self._m_rabbit_received_message.labels().inc()

    def receive_nats_message(self, message: NatsMessage):
        self._m_nats_received_message.labels().inc()

    def collect(self) -> Iterable[Metric]:
        yield from self._m_exceptions.collect()
        yield from self._m_received_message.collect()
        yield from self._m_kafka_received_message.collect()
        yield from self._m_kafka_offset.collect()
        yield from self._m_kafka_received_message_key_size.collect()
        yield from self._m_kafka_received_message_value_size.collect()
        yield from self._m_redis_received_message.collect()
        yield from self._m_rabbit_received_message.collect()
        yield from self._m_nats_received_message.collect()


class SafeFaststreamCollector(FaststreamCollector):
    registry: CollectorRegistry
    namespace: str

    COLLECTORS_STORAGE: Dict[int, Self] = {}

    @classmethod
    def get_collector(cls, registry: Optional[CollectorRegistry], namespace: str) -> Self:
        collector_id = hash((id(registry), hash(namespace)))

        if collector_id not in cls.COLLECTORS_STORAGE:
            cls.COLLECTORS_STORAGE[collector_id] = cls(registry, namespace)

        return cls.COLLECTORS_STORAGE[collector_id]

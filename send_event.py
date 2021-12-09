# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from kafka import KafkaProducer


def send_kafka_event(
        topic: str,
        producer: KafkaProducer,
        message: dict,
        CID: bytes,
) -> None:
    producer.send(
        topic,
        key=None,
        value=message,
        headers=[("CID", CID)]
    )
    producer.flush()

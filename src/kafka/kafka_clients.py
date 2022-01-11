# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import json

from kafka import KafkaProducer

from src.config import settings


def kafka_producer():
    return KafkaProducer(
        api_version=(2, 6),
        bootstrap_servers=settings.KAFKA_BROKER4KAFKA,
        value_serializer=lambda
            v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda
            v: json.dumps(v).encode('utf-8')
    )

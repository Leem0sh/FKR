# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import json

from kafka import KafkaProducer, KafkaConsumer


def kafka_producer():
    return KafkaProducer(
        api_version=(2, 6),
        bootstrap_servers="localhost" + ":" + str(
            9092
        ),
        value_serializer=lambda
            v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda
            v: json.dumps(v).encode('utf-8')
    )


def kafka_consumer():
    return KafkaConsumer(
        api_version=(2, 6),
        group_id=None,
        client_id="client1",
        bootstrap_servers="localhost" + ":" + str(
            9092
        ),
        value_deserializer=lambda
            v: json.loads(v.decode('utf-8')),
        key_deserializer=lambda
            v: json.loads(v.decode('utf-8')),
        max_poll_records=10
    )

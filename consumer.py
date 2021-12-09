# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import Final

from pydantic import parse_obj_as

from finisher import TOPIC_FROM_DS_TO_FINISHER, TOPIC_FROM_GATEWAY_TO_DS
from kafka_clients import kafka_consumer, kafka_producer
from send_event import send_kafka_event
from models import DimensionRequestBodyModel

logger: Final = logging.getLogger(__name__)


def get_cid_from_headers(
        headers
):
    dic = dict(headers)
    return dic["CID"]


def main():
    consumer = kafka_consumer()
    consumer.subscribe(topics=[TOPIC_FROM_GATEWAY_TO_DS])
    producer = kafka_producer()

    for message in consumer:
        print(
            "%d:%d: k=%s v=%s h=%s" % (message.partition,
                                       message.offset,
                                       message.key,
                                       message.value,
                                       message.headers)
        )
        CID = get_cid_from_headers(message.headers)
        print(CID)
        parsed_message = parse_obj_as(DimensionRequestBodyModel, message.value)
        print(parsed_message)
        # time.sleep(0.1)
        # r = coroner_call(parsed_message)
        r = {
            "dimensions": [
                {
                    "y": [
                        "100"
                    ],
                    "unit": [
                        "cm"
                    ]
                }
            ]
        }
        print(r)
        send_kafka_event(
            TOPIC_FROM_DS_TO_FINISHER,
            producer,
            r,
            CID=CID
        )


if __name__ == '__main__':
    main()

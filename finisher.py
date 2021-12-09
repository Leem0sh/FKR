# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
import json

import nats
from kafka import KafkaConsumer


TOPIC_FROM_GATEWAY_TO_DS = "ai.gateway.dimensions.measure.v0-1"
TOPIC_FROM_DS_TO_CORONER = "ai.dimensions.coroner.v0-1"
TOPIC_FROM_CORONER_TO_DS = "ai.coroner.dimensions.parse.v0-1"
TOPIC_FROM_DS_TO_FINISHER = "ai.dimensions.finisher.V0-1"


def get_cid_from_headers(
    headers
):
    dic = dict(headers)
    return dic["CID"]


async def main():
    nc = await nats.connect()
    print(nc)

    def kafka_consumer():
        return KafkaConsumer(
            api_version=(2, 6),
            group_id="finisher_consumer",
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

    async def message_handler(
        msg
    ):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(
            "Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data
            )
        )

    c = kafka_consumer()
    c.subscribe(topics=[TOPIC_FROM_DS_TO_FINISHER])

    for message in c:
        CID = get_cid_from_headers(message.headers).decode("utf-8")
        print(message)
        print(CID)
        print(message.headers)
        msg = message.value
        print(msg)
        await nc.publish(
            CID,
            json.dumps(message.value).encode()
        )
        await nc.flush()


if __name__ == '__main__':
    asyncio.run(main())

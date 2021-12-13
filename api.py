# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import json
from uuid import uuid4

from fastapi import FastAPI, Depends
from kafka import KafkaProducer
from pydantic import parse_obj_as
from redis import Redis
from starlette.responses import JSONResponse

from finisher import TOPIC_FROM_GATEWAY_TO_DS
from kafka_clients import kafka_producer
from models import DimensionRequestBodyModel

app = FastAPI()
rc = Redis(retry_on_timeout=True, socket_timeout=1)


async def send_kafka_event(
        topic: str,
        producer: KafkaProducer,
        message: dict,
        CID,
) -> None:
    producer.send(
        topic,
        key=None,
        value=message,
        headers=[("CID", bytes(CID, "utf-8"))]
    )
    producer.flush()


def redis_connect():
    return rc.pubsub(ignore_subscribe_messages=True)


@app.post(
    "/test/",
    description="Test description",
    summary="Test summary",
    tags=["Test"],
    include_in_schema=True,
)
async def _(
        *,
        producer: KafkaProducer = Depends(kafka_producer),
        redis_subscriber=Depends(redis_connect),
        description: DimensionRequestBodyModel,
) -> JSONResponse:
    response = None
    CID = uuid4().hex
    parsed_description = parse_obj_as(DimensionRequestBodyModel, description)

    print(CID, parsed_description)
    redis_subscriber.subscribe(CID)
    await send_kafka_event(
        TOPIC_FROM_GATEWAY_TO_DS,
        producer,
        parsed_description.dict(),
        CID
    )
    while True:
        message = redis_subscriber.get_message()
        print(message)
        if message:
            break
    redis_subscriber.close()
    return JSONResponse(
        status_code=200, content=json.loads(
            message["data"].decode("utf-8")
        )
    )

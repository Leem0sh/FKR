# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import json
from uuid import uuid4

import nats
from fastapi import FastAPI, Depends
from kafka import KafkaProducer
from nats.aio.client import Client
from pydantic import parse_obj_as
from starlette.responses import JSONResponse

from finisher import TOPIC_FROM_GATEWAY_TO_DS
from kafka_clients import kafka_producer
from models import DimensionRequestBodyModel

app = FastAPI()

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



async def nats_connect():
    async def disconnected_cb():
        print('Got disconnected!')

    async def reconnected_cb():
        print(f'Got reconnected to {nc.connected_url.netloc}')

    async def error_cb(
        e
    ):
        print(f'There was an error: {e}')

    async def closed_cb():
        print('Connection is closed')

    # Connect to NATS with logging callbacks.
    nc = await nats.connect(
        error_cb=error_cb,
        reconnected_cb=reconnected_cb,
        disconnected_cb=disconnected_cb,
        closed_cb=closed_cb,
    )
    return nc



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
    nats_consumer: Client = Depends(nats_connect),
    description: DimensionRequestBodyModel,
) -> JSONResponse:

    response = None
    CID = uuid4().hex
    parsed_description = parse_obj_as(DimensionRequestBodyModel, description)

    print(CID, parsed_description)
    await send_kafka_event(TOPIC_FROM_GATEWAY_TO_DS, producer, parsed_description.dict(), CID)
    sub = await nats_consumer.subscribe(CID)
    try:
        async for msg in sub.messages:
            print(f"Received a message on '{msg.subject} {msg.reply}': {msg.data.decode()}")
            response = json.loads(msg.data.decode())
            await sub.unsubscribe(CID)



    except Exception as e:
        print(e)
    return JSONResponse(status_code=200, content=response)

# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import json
import logging
from typing import Final, List
from uuid import uuid4

from fastapi import FastAPI, Depends
from kafka import KafkaProducer
from redis.client import PubSub
from starlette.responses import JSONResponse

from src.config import settings
from src.kafka.kafka_clients import kafka_producer
from src.log import configure_basic_logging
from src.models import MathModel, ResultModel
from src.redis.redis_connect import redis_connect

configure_basic_logging()

logger: Final = logging.getLogger(__name__)

app = FastAPI()

err_postfix: Final = ".NOT_OK"
ok_postfix: Final = ".OK"


def group_subscribe(
        redis_subscriber: PubSub,
        channels: List[str]
):
    redis_subscriber.subscribe(*channels)
    return redis_subscriber


def gen_headers(
        CID: str,
        ok_channel: str,
        err_channel: str,
) -> List[tuple[str, bytes]]:
    return [(settings.CID, bytes(CID, "utf-8")),
            (settings.REPLY_TO_OK_TOPIC, bytes(ok_channel, "utf-8")),
            (settings.REPLY_TO_NOT_OK_TOPIC, bytes(err_channel, "utf-8"))]


def channel_preparation(
        cid: str
) -> tuple[str, str]:
    ok_channel = f"{cid}{ok_postfix}"
    err_channel = f"{cid}{err_postfix}"
    return ok_channel, err_channel


async def send_kafka_event(
        topic: str,
        producer: KafkaProducer,
        message: dict,
        headers,
) -> None:
    producer.send(
        topic,
        key=None,
        value=message,
        headers=headers
    )
    producer.flush()


@app.post(
    "/test/",
    response_model=ResultModel,
    description="Test description",
    summary="Test summary",
    tags=["Test"],
    include_in_schema=True,
)
async def _(
        *,
        producer: KafkaProducer = Depends(kafka_producer),
        redis_pubsub=Depends(redis_connect),
        values: MathModel,
) -> JSONResponse:
    response = None

    CID = uuid4().hex
    ok_channel, err_channel = channel_preparation(CID)
    kafka_headers = gen_headers(
        CID,
        ok_channel,
        err_channel,
    )
    redis_subscriber = group_subscribe(redis_pubsub, [ok_channel, err_channel])

    logger.info("sending kafka event")
    logger.info(
        f"{settings.API_TO_SERVICE}, {producer}, {values.dict()}, {kafka_headers}"
    )
    await send_kafka_event(
        settings.API_TO_SERVICE,
        producer,
        values.dict(),
        kafka_headers
    )
    logger.info("kafka event sent")
    while True:
        message = redis_subscriber.get_message()
        if message:
            break
    print(message)
    redis_subscriber.close()
    return JSONResponse(
        status_code=200, content=json.loads(
            message["data"].decode("utf-8")
        )
    )

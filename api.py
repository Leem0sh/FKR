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

L: Final = logging.getLogger(__name__)

app = FastAPI()

OK_POSTFIX: Final = ".OK"
ERR_POSTFIX: Final = ".NOT_OK"


def _group_subscribe(
        redis_subscriber: PubSub,
        channels: List[str]
) -> PubSub:
    """
    Subsrcibes to the list of channels (<CID>.OK, <CID>.NOT_OK)

    :param redis_subscriber: Redis PubSub
    :param channels: list of channels for subscription
    :return: PubSub with subscribed channels
    """
    redis_subscriber.subscribe(*channels)
    return redis_subscriber


def _gen_headers(
        cid_name: str,
        ok_channel_name: str,
        err_channel_name: str,
        cid: str,
        ok_channel: str,
        err_channel: str,
) -> List[tuple[str, bytes]]:
    """

    :param CID: Correlation ID
    :param ok_channel: Channel for 200 responses
    :param err_channel: Channel for != 200 responses
    :return: List of headers tuple[str,bytes]
    """
    return [(cid_name, bytes(cid, "utf-8")),
            (ok_channel_name, bytes(ok_channel, "utf-8")),
            (err_channel_name, bytes(err_channel, "utf-8"))]


def _channel_preparation(
        cid: str
) -> tuple[str, str]:
    """
    Adds postfixes to the CID

    :param cid: Correlation ID
    :return: Correlation ID with postfixes - for subscription
    """
    ok_channel = f"{cid}{OK_POSTFIX}"
    err_channel = f"{cid}{ERR_POSTFIX}"
    return ok_channel, err_channel


async def send_kafka_event(
        topic: str,
        producer: KafkaProducer,
        message: dict,
        headers: List[tuple[str, bytes]],
) -> None:
    """

    :param topic: Targeted kafka topic
    :param producer: Kafka producer
    :param message: payload message
    :param headers: kafka headers with channels and CID List[tuple[str, bytes]]
    :return: None
    """
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
    """
    API Endpoint which sends Kafka events into Kafka topic, subscribes to
    redis channel and waits for response (key-value)

    :param producer: Kafka producer dependency
    :param redis_pubsub: Redis PubSub client
    :param values: MathModel - input data
    :return: Response to the client
    """

    cid: Final = uuid4().hex
    ok_channel, err_channel = _channel_preparation(cid)
    kafka_headers = _gen_headers(
        settings.CID,
        settings.REPLY_TO_OK_CHANNEL,
        settings.REPLY_TO_NOT_OK_CHANNEL,
        cid,
        ok_channel,
        err_channel,
    )
    redis_subscriber = _group_subscribe(redis_pubsub, [ok_channel, err_channel])

    L.info(
        f"{settings.API_TO_SERVICE}, {producer}, {values.dict()}, {kafka_headers}"
    )
    await send_kafka_event(
        settings.API_TO_SERVICE,
        producer,
        values.dict(),
        kafka_headers
    )
    while True:
        message = redis_subscriber.get_message()
        if message:
            break
    L.info(message)
    redis_subscriber.close()
    return JSONResponse(
        status_code=200, content=json.loads(
            message["data"].decode("utf-8")
        )
    )

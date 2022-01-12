# -*- encoding: utf-8 -*-
# ! python3
"""
Inits the faust_ app and process the data
"""

from __future__ import annotations

import json
import logging
from typing import Final

import faust
from faust import Stream

from src.config import settings
from src.log import configure_basic_logging
from src.models import MathModel
from src.redis_.redis_connect import REDIS_CONNECT
from src.service import operation_add

configure_basic_logging()

L: Final = logging.getLogger(__name__)

app = faust.App("basic-math-app", broker=settings.BROKER)
math_topic = app.topic(settings.API_TO_SERVICE, value_type=bytes)


@app.agent(math_topic)
async def math_streaming(
        stream: Stream
) -> None:
    """
    Catches event from stream, process operations and publishes to redis_ topic

    :param stream: Kafka event stream
    :return: None
    """
    async for payload in stream.events():
        L.info(payload)
        result = await operation_add(MathModel.parse_obj(payload.value))

        REDIS_CONNECT.publish(
            payload.headers[settings.REPLY_TO_OK_TOPIC],
            json.dumps(result.dict())
        )
        L.info(
            f"{result.dict()} sent to"
            f" {payload.headers[settings.REPLY_TO_OK_TOPIC]}"
        )

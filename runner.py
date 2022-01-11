# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import json
import logging
from typing import Final

import faust

from src.config import settings
from src.log import configure_basic_logging
from src.models import MathModel
from src.redis.redis_connect import REDIS_CONNECT
from src.service import operation_add

configure_basic_logging()

logger: Final = logging.getLogger(__name__)

app = faust.App("basic-math-app", broker=settings.BROKER)
math_topic = app.topic(settings.API_TO_SERVICE, value_type=bytes)


@app.agent(math_topic)
async def math_streaming(
        stream
):
    async for payload in stream.events():
        logger.info(payload)
        result = await operation_add(MathModel.parse_obj(payload.value))

        REDIS_CONNECT.publish(
            payload.headers[settings.REPLY_TO_OK_TOPIC],
            json.dumps(result.dict())
        )
        logger.info(
            f"{result.dict()} sent to"
            f" {payload.headers[settings.REPLY_TO_OK_TOPIC]}"
        )

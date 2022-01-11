# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from functools import cache
from typing import Final

import redis

from src.config import settings

REDIS_CONNECT: Final = redis.Redis(
    host=settings.REDIS_HOST_URL,
    port=int(settings.REDIS_HOST_PORT),
    db=int(settings.REDIS_HOST_DB),
    retry_on_timeout=True,
    socket_timeout=1
)


@cache
def redis_connect():
    return REDIS_CONNECT.pubsub(ignore_subscribe_messages=True)

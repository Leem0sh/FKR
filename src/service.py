# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from src.models import MathModel, ResultModel


async def operation_add(
        data: MathModel
) -> ResultModel:
    """
    val1 + val2

    :param data: MathModel - Data from request
    :return: ResultModel
    """
    result = data.val1 + data.val2
    return ResultModel(result=result)

from __future__ import annotations

from pydantic import BaseModel


class ResultModel(BaseModel):
    result: int


class MathModel(BaseModel):
    val1: int
    val2: int

    class Config:
        schema_extra = {
            "example": {
                "val1": 1,
                "val2": 4
            }
        }

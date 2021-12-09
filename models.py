from __future__ import annotations

from enum import Enum
from typing import List, Union

from pydantic import BaseModel, NonNegativeFloat, constr


class DimensionRequestBodyModel(BaseModel):
    """
    Model for Dimension request
    """
    description: constr(strip_whitespace=True)

    class Config:
        schema_extra = {
            "example": {
                "description": "just a random description ",
            }
        }


class DimensionResponseModel(BaseModel):
    """
    Model for Dimension request
    """

    dimensions: List[dict]


class DimensionsEnums(str, Enum):
    nabytek = "nabytek"
    textil = "textil"

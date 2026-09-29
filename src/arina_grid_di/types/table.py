# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .point import Point

__all__ = ["Table"]


class Table(BaseModel):
    """A table block's HTML."""

    block_id: Optional[int] = FieldInfo(alias="blockId", default=None)

    polygon: List[Point]

    html: str

# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .point import Point

__all__ = ["Block"]


class Block(BaseModel):
    """One layout region, in reading order."""

    id: Optional[int] = None
    """Block identifier."""

    type: str
    """Open string; see API_PARSE.md for values"""

    label: str
    """Raw block label from the parser."""

    content: str

    polygon: List[Point]

    reading_order: int = FieldInfo(alias="readingOrder")

    layout_score: Optional[float] = FieldInfo(alias="layoutScore", default=None)

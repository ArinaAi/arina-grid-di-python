# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import List, Optional

from .._models import BaseModel

from .point import Point

__all__ = ["TextLine"]


class TextLine(BaseModel):
    """One text line."""

    polygon: List[Point]

    text: str

    score: Optional[float] = None

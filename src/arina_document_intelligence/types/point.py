# File generated from our OpenAPI spec by Scalar. See README.md for details.

from .._models import BaseModel

__all__ = ["Point"]


class Point(BaseModel):
    """One vertex, in the coordinate space of its page."""

    x: float

    y: float

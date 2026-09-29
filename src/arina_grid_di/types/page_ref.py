# File generated from our OpenAPI spec by Scalar. See README.md for details.

from .._models import BaseModel

__all__ = ["PageRef"]


class PageRef(BaseModel):
    """The page a citation refers to, and the frame its coordinates use."""

    number: int
    """1-based page number"""

    width: float
    """Page width in the polygon's units"""

    height: float
    """Page height in the polygon's units"""

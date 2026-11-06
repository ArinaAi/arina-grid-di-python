# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["BatchCounts"]


class BatchCounts(BaseModel):
    """How many items are in each state. ``total`` is the sum of the others."""

    total: Optional[int] = None

    pending: Optional[int] = None

    processing: Optional[int] = None

    processed: Optional[int] = None

    failed: Optional[int] = None

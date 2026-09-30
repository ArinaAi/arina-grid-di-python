# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import List, Optional

from .._models import BaseModel

from .extractor import Extractor

__all__ = ["ExtractorList"]


class ExtractorList(BaseModel):
    """``GET /extractors`` response."""

    object: Optional[str] = None

    data: List[Extractor]

# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .citation import Citation

__all__ = ["FieldMetadata"]


class FieldMetadata(BaseModel):
    """Per-field confidence and provenance, keyed by field path in the output."""

    ocr_confidence: Optional[float] = FieldInfo(alias="ocrConfidence", default=None)
    """Text recognition confidence for the underlying span"""

    citations: Optional[List[Citation]] = None
    """Empty when the value could not be located on the page. Indicates absence of a position, not low confidence in the value."""

# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .page_ref import PageRef
from .point import Point

__all__ = ["Citation"]


class Citation(BaseModel):
    """Where in the document a value came from."""

    page: PageRef
    """The page a citation refers to, and the frame its coordinates use."""

    polygon: List[Point]
    """Region outline, clockwise from top-left. Four points for an axis-aligned region, or a quad when the page is skewed."""

    reference_text: Optional[str] = FieldInfo(alias="referenceText", default=None)
    """The source text backing the value, when recoverable"""

    layout_score: Optional[float] = FieldInfo(alias="layoutScore", default=None)
    """Block-detection confidence, 0–1. Diagnostic; not a field-level accuracy measure."""

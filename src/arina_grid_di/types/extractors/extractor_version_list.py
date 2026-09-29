# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import List, Optional

from ..._models import BaseModel

from .extractor_version import ExtractorVersion

__all__ = ["ExtractorVersionList"]


class ExtractorVersionList(BaseModel):
    """``GET /extractors/{id}/versions`` response."""

    object: Optional[str] = None

    data: List[ExtractorVersion]

# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

from ..extract_config import ExtractConfig

__all__ = ["ExtractorVersion"]


class ExtractorVersion(BaseModel):
    """An immutable snapshot of an extractor's config."""

    object: Optional[str] = None

    extractor_id: str = FieldInfo(alias="extractorId")

    version: int

    config: ExtractConfig
    """
    Extraction parameters for one run.
    
    Requires ``jsonSchema``, ``extractionRules``, or both, unless ``extractorId``
    names a saved extractor, whose configuration is resolved into these fields when
    the run is created. Neither is rejected rather than inferring a schema the
    caller cannot inspect.
    """

    created_at: str = FieldInfo(alias="createdAt")
    """RFC 3339 UTC"""

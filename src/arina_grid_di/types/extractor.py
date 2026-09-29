# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .extract_config import ExtractConfig

__all__ = ["Extractor"]


class Extractor(BaseModel):
    """A saved extractor at its current version."""

    object: Optional[str] = None

    id: str
    """Extractor identifier, prefixed 'ext_'"""

    api_version: Optional[str] = FieldInfo(alias="apiVersion", default=None)

    organization_id: str = FieldInfo(alias="organizationId")

    name: str

    description: Optional[str] = None

    version: int

    status: Optional[str] = None
    """Open string"""

    config: ExtractConfig
    """
    Extraction parameters for one run.
    
    Requires ``jsonSchema``, ``extractionRules``, or both, unless ``extractorId``
    names a saved extractor, whose configuration is resolved into these fields when
    the run is created. Neither is rejected rather than inferring a schema the
    caller cannot inspect.
    """

    metadata: Optional[Dict[str, object]] = None

    created_at: str = FieldInfo(alias="createdAt")
    """RFC 3339 UTC"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """RFC 3339 UTC"""

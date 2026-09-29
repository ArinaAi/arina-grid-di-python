# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .extract_config import ExtractConfig
from .extract_output import ExtractOutput

__all__ = ["ExtractRun"]


class ExtractRun(BaseModel):
    """An extraction run. See :class:`RunEnvelope` for the envelope and status rules."""

    object: Optional[str] = None

    id: str
    """Run identifier, prefixed 'exr_'"""

    api_version: Optional[str] = FieldInfo(alias="apiVersion", default=None)
    """Wire contract version that produced this run (date-based)"""

    status: str
    """See RunStatus; treat as an open string"""

    upload_id: str = FieldInfo(alias="uploadId")

    document_name: Optional[str] = FieldInfo(alias="documentName", default=None)

    organization_id: Optional[str] = FieldInfo(alias="organizationId", default=None)

    collection: Optional[str] = None

    config: ExtractConfig
    """
    Extraction parameters for one run.
    
    Requires ``jsonSchema``, ``extractionRules``, or both, unless ``extractorId``
    names a saved extractor, whose configuration is resolved into these fields when
    the run is created. Neither is rejected rather than inferring a schema the
    caller cannot inspect.
    """

    output: Optional[ExtractOutput] = None
    """The extracted data, and per-field provenance for it."""

    failure_reason: Optional[str] = FieldInfo(alias="failureReason", default=None)
    """See FailureReason; treat as an open string"""

    failure_message: Optional[str] = FieldInfo(alias="failureMessage", default=None)
    """Human-readable detail; never the only signal"""

    metadata: Optional[Dict[str, object]] = None

    created_at: str = FieldInfo(alias="createdAt")
    """RFC 3339 UTC"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """RFC 3339 UTC"""

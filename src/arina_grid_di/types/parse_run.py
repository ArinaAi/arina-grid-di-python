# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .parse_config import ParseConfig
from .parse_output import ParseOutput

__all__ = ["ParseRun"]


class ParseRun(BaseModel):
    """A parse run. See :class:`RunEnvelope` for the envelope and status rules."""

    object: Optional[str] = None

    id: str
    """Run identifier, prefixed 'prs_'"""

    api_version: Optional[str] = FieldInfo(alias="apiVersion", default=None)
    """Wire contract version that produced this run (date-based)"""

    status: str
    """See RunStatus; treat as an open string"""

    upload_id: str = FieldInfo(alias="uploadId")

    document_name: Optional[str] = FieldInfo(alias="documentName", default=None)

    organization_id: Optional[str] = FieldInfo(alias="organizationId", default=None)

    collection: Optional[str] = None

    config: Optional[ParseConfig] = None
    """Options for a parse run. Every option has a default, so ``config`` may be omitted."""

    output: Optional[ParseOutput] = None
    """The parsed page."""

    failure_reason: Optional[str] = FieldInfo(alias="failureReason", default=None)
    """See FailureReason; treat as an open string"""

    failure_message: Optional[str] = FieldInfo(alias="failureMessage", default=None)
    """Human-readable detail; never the only signal"""

    metadata: Optional[Dict[str, object]] = None

    created_at: str = FieldInfo(alias="createdAt")
    """RFC 3339 UTC"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """RFC 3339 UTC"""

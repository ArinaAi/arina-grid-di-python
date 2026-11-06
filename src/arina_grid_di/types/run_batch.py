# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .batch_counts import BatchCounts
from .batch_item import BatchItem

__all__ = ["RunBatch"]


class RunBatch(BaseModel):
    """
    A batch of runs. ``object`` names the kind: ``parse_batch`` or ``extract_batch``.

    ``status`` and ``counts`` are what they were when the record was written or last
    refreshed; a route serves a batch through ``refresh`` so a caller sees them live.
    The member runs' outputs stay on the runs.
    """

    object: str
    """'parse_batch' or 'extract_batch'"""

    id: str
    """Batch identifier, prefixed 'pbt_'"""

    api_version: Optional[str] = FieldInfo(alias="apiVersion", default=None)
    """Wire contract version that produced this batch (date-based)"""

    status: Optional[str] = None
    """See BatchStatus; treat as an open string"""

    counts: Optional[BatchCounts] = None
    """How many items are in each state. ``total`` is the sum of the others."""

    items: Optional[List[BatchItem]] = None

    organization_id: Optional[str] = FieldInfo(alias="organizationId", default=None)

    config: Optional[object] = None
    """The configuration every member run was made with"""

    metadata: Optional[Dict[str, object]] = None

    created_at: str = FieldInfo(alias="createdAt")
    """RFC 3339 UTC"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """RFC 3339 UTC; the latest change among the member runs"""

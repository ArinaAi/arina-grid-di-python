# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["BatchItem"]


class BatchItem(BaseModel):
    """
    One document of the batch and the run it became.

    ``run_id`` is None when the infrastructure refused the document at accept
    time (storage, record or publish). Such an item is FAILED from the start, and
    the caller resubmits that document on its own.
    """

    document_name: str = FieldInfo(alias="documentName")

    run_id: Optional[str] = FieldInfo(alias="runId", default=None)

    status: Optional[str] = None
    """See RunStatus; treat as an open string"""

    failure_reason: Optional[str] = FieldInfo(alias="failureReason", default=None)
    """See FailureReason; treat as an open string"""

    failure_message: Optional[str] = FieldInfo(alias="failureMessage", default=None)

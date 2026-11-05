# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

from typing_extensions import Annotated, Required, TypedDict
from .._types import FileTypes, SequenceNotStr

from .._utils import PropertyInfo

__all__ = ["ExtractionCreateExtractBatchParams"]


class ExtractionCreateExtractBatchParams(TypedDict, total=False):
    files: Required[SequenceNotStr[FileTypes]]
    """Documents to process, one part per file under this name. PDF, PNG or JPEG; page 1 of each. Up to 100 files, 15 MB each, 90 MB per request."""

    config: Required[str]
    """Extraction configuration: the `ExtractRunRequest` object, JSON-encoded into this single form field (e.g. `json.dumps(...)` / `JSON.stringify(...)`). See the `ExtractRunRequest` schema for the fields. Applied to every document."""

    x_api_version: Annotated[str, PropertyInfo(alias="X-Api-Version")]

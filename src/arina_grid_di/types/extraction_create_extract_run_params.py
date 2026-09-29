# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

from typing_extensions import Annotated, Required, TypedDict
from .._types import FileTypes

from .._utils import PropertyInfo

__all__ = ["ExtractionCreateExtractRunParams"]


class ExtractionCreateExtractRunParams(TypedDict, total=False):
    file: Required[FileTypes]
    """Document to process. PDF, PNG or JPEG. Page 1 only. Max 15 MB."""

    config: Required[str]
    """Extraction configuration: the `ExtractRunRequest` object, JSON-encoded into this single form field (e.g. `json.dumps(...)` / `JSON.stringify(...)`). See the `ExtractRunRequest` schema for the fields."""

    x_api_version: Annotated[str, PropertyInfo(alias="X-Api-Version")]

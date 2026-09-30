# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ExtractConfigParam"]


class ExtractConfigParam(TypedDict, total=False):
    extractor_id: Annotated[Optional[str], PropertyInfo(alias="extractorId")]
    """Saved extractor to take the configuration from"""

    extractor_version: Annotated[Optional[int], PropertyInfo(alias="extractorVersion")]
    """Extractor version to use; on a run, the version actually used. Absent on the request means the current version."""

    json_schema: Annotated[Optional[Dict[str, object]], PropertyInfo(alias="jsonSchema")]
    """JSON Schema describing the fields to extract. Supported subset: an object at the root; types string, number, integer, boolean, object, array; primitives must admit null (e.g. ["number", "null"]); array items are objects; enums include null; nesting at most 3 levels; property names [A-Za-z0-9_-]; at most 200 fields."""

    extraction_rules: Annotated[Optional[str], PropertyInfo(alias="extractionRules")]
    """Natural-language guidance, e.g. 'amounts are in USD; treat a dash as zero'. Applied in addition to the schema."""

    citations_enabled: Annotated[bool, PropertyInfo(alias="citationsEnabled")]
    """Locate each value on the page and return its geometry"""

    citation_mode: Annotated[str, PropertyInfo(alias="citationMode")]
    """Granularity of citation geometry. Only 'block' is served today; 'cell', 'line' and 'word' are declared but rejected until the upstream geometry they need is enabled."""

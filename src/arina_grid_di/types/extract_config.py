# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ExtractConfig"]


class ExtractConfig(BaseModel):
    """
    Extraction parameters for one run.

    Requires ``jsonSchema``, ``extractionRules``, or both, unless ``extractorId``
    names a saved extractor, whose configuration is resolved into these fields when
    the run is created. Neither is rejected rather than inferring a schema the
    caller cannot inspect.
    """

    extractor_id: Optional[str] = FieldInfo(alias="extractorId", default=None)
    """Saved extractor to take the configuration from"""

    extractor_version: Optional[int] = FieldInfo(alias="extractorVersion", default=None)
    """Extractor version to use; on a run, the version actually used. Absent on the request means the current version."""

    json_schema: Optional[Dict[str, object]] = FieldInfo(alias="jsonSchema", default=None)
    """JSON Schema describing the fields to extract. Supported subset: an object at the root; types string, number, integer, boolean, object, array; primitives must admit null (e.g. ["number", "null"]); array items are objects; enums include null; nesting at most 3 levels; property names [A-Za-z0-9_-]; at most 200 fields."""

    extraction_rules: Optional[str] = FieldInfo(alias="extractionRules", default=None)
    """Natural-language guidance, e.g. 'amounts are in USD; treat a dash as zero'. Applied in addition to the schema."""

    citations_enabled: Optional[bool] = FieldInfo(alias="citationsEnabled", default=None)
    """Locate each value on the page and return its geometry"""

    citation_mode: Optional[str] = FieldInfo(alias="citationMode", default=None)
    """Granularity of citation geometry. Only 'block' is served today; 'cell', 'line' and 'word' are declared but rejected until the upstream geometry they need is enabled."""

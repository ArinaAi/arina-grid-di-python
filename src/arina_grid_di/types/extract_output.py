# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .field_metadata import FieldMetadata
from .page_image import PageImage

__all__ = ["ExtractOutput"]


class ExtractOutput(BaseModel):
    """The extracted data, and per-field provenance for it."""

    value: Dict[str, object]
    """Extracted data, conforming to the requested jsonSchema"""

    metadata: Optional[Dict[str, FieldMetadata]] = None
    """Keyed by field path into `value` — see FIELD_PATH_GRAMMAR. A path may be absent when nothing was located for it."""

    page_image: Optional[PageImage] = FieldInfo(alias="pageImage", default=None)
    """The raster the citation polygons refer to. None if it could not be stored, in which case the extracted values remain valid but no overlay can be drawn."""

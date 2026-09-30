# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .page_ref import PageRef
from .block import Block
from .table import Table
from .text_line import TextLine
from .page_image import PageImage

__all__ = ["ParseOutput"]


class ParseOutput(BaseModel):
    """The parsed page."""

    page: PageRef
    """The page a citation refers to, and the frame its coordinates use."""

    markdown: str

    blocks: Optional[List[Block]] = None

    tables: Optional[List[Table]] = None

    text_lines: Optional[List[TextLine]] = FieldInfo(alias="textLines", default=None)
    """Present only when config.includeTextLines was set"""

    page_image: Optional[PageImage] = FieldInfo(alias="pageImage", default=None)
    """The rendered page's coordinate frame. Fetch the image itself from `GET /{run}/page`; overlay polygons are in this width/height."""

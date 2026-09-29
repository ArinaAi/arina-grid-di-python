# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ParseConfig"]


class ParseConfig(BaseModel):
    """Options for a parse run. Every option has a default, so ``config`` may be omitted."""

    include_text_lines: Optional[bool] = FieldInfo(alias="includeTextLines", default=None)
    """Also return every text line with its polygon and score"""

# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ExtractorDeleteParams"]


class ExtractorDeleteParams(TypedDict, total=False):
    permanent: bool

    x_api_version: Annotated[str, PropertyInfo(alias="X-Api-Version")]

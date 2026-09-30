# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

from typing_extensions import Annotated, Literal, Required, TypedDict

from .._utils import PropertyInfo

__all__ = ["ExtractorListParams"]


class ExtractorListParams(TypedDict, total=False):
    organization_id: Required[Annotated[str, PropertyInfo(alias="organizationId")]]
    """Tenant that owns the resource."""

    status: Literal["ACTIVE", "ARCHIVED", "all"]

    x_api_version: Annotated[str, PropertyInfo(alias="X-Api-Version")]

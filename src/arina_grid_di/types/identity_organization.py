# File generated from our OpenAPI spec by Scalar. See README.md for details.

from .._models import BaseModel

__all__ = ["IdentityOrganization"]


class IdentityOrganization(BaseModel):
    """The tenant a key belongs to."""

    id: str
    """Stable identifier of the organisation."""

    slug: str
    """Organisation name as used in storage and logs."""

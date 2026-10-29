# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

from .identity_organization import IdentityOrganization
from .identity_user import IdentityUser

__all__ = ["Identity"]


class Identity(BaseModel):
    """
    Who the presented credential is.

    For an API key: the organisation, the key id and its scopes. For a signed-in
    user: the organisation, the user and the scopes their role grants. Derived
    entirely from the credential: the caller declares nothing.
    """

    organization: IdentityOrganization
    """The tenant a key belongs to."""

    subject: str
    """`key:<keyId>` or `user:<id>`; what audit attributes to."""

    scopes: List[str]
    """What the credential may do, one entry per route group."""

    key_id: Optional[str] = FieldInfo(alias="keyId", default=None)
    """Public identifier of the key; absent for a user session."""

    user: Optional[IdentityUser] = None
    """The signed-in person; absent for an API key."""

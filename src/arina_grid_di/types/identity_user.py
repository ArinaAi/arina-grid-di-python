# File generated from our OpenAPI spec by Scalar. See README.md for details.

from .._models import BaseModel

__all__ = ["IdentityUser"]


class IdentityUser(BaseModel):
    """The signed-in person, when the credential is a session rather than a key."""

    id: str

    email: str

    role: str
    """`owner`, `admin` or `member`."""

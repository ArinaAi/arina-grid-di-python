# File generated from our OpenAPI spec by Scalar. See README.md for details.

from .._models import BaseModel

__all__ = ["PageImage"]


class PageImage(BaseModel):
    """The rendered page's coordinate frame. Fetch the image itself from `GET /{run}/page`; overlay polygons are in this width/height."""

    width: float

    height: float

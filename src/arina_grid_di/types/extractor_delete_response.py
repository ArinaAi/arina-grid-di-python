# File generated from our OpenAPI spec by Scalar. See README.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .._models import BaseModel

from .extractor import Extractor

__all__ = ["ExtractorDeleteResponse"]


class ExtractorDeleteResponse(BaseModel):
    object: str

    id: str

    deleted: bool


ExtractorDeleteResponse: TypeAlias = Union[Extractor, ExtractorDeleteResponse]

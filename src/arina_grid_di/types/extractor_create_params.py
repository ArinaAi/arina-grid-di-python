# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Annotated, Required, TypedDict

from .._utils import PropertyInfo

from .extract_config_param import ExtractConfigParam

__all__ = ["ExtractorCreateParams"]


class ExtractorCreateParams(TypedDict, total=False):
    organization_id: Required[Annotated[str, PropertyInfo(alias="organizationId")]]

    name: Required[str]

    description: Optional[str]

    config: Required[ExtractConfigParam]
    """
    Extraction parameters for one run.
    
    Requires ``jsonSchema``, ``extractionRules``, or both, unless ``extractorId``
    names a saved extractor, whose configuration is resolved into these fields when
    the run is created. Neither is rejected rather than inferring a schema the
    caller cannot inspect.
    """

    metadata: Optional[Dict[str, object]]

    x_api_version: Annotated[str, PropertyInfo(alias="X-Api-Version")]

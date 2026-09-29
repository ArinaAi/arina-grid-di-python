from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `arina_document_intelligence.resources` module.

    This is used so that we can lazily import `arina_document_intelligence.resources` only when
    needed *and* so that users can just import `arina_document_intelligence` and reference `arina_document_intelligence.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("arina_document_intelligence.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()

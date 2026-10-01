# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

import os
import threading
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, is_mapping_t, get_async_library
from ._compat import cached_property
from ._exceptions import APIStatusError, ArinaDocumentIntelligenceAPIError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._version import __version__

if TYPE_CHECKING:
    from .resources import extraction, parse, extractors
    from .resources.extraction import ExtractionResource, AsyncExtractionResource
    from .resources.parse import ParseResource, AsyncParseResource
    from .resources.extractors import ExtractorsResource, AsyncExtractorsResource

# Serializes lazy resource imports so concurrent cold access from multiple
# threads cannot deadlock on CPython import locks (see CPython 3.14).
_RESOURCE_IMPORT_LOCK = threading.RLock()

__all__ = [
    "ArinaDocumentIntelligenceAPI",
    "AsyncArinaDocumentIntelligenceAPI",
    "Client",
    "AsyncClient",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
]


class ArinaDocumentIntelligenceAPI(SyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous ArinaDocumentIntelligenceAPI client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ARINA_GRID_API_KEY`
        """
        if api_key is None:
            api_key = os.environ.get("ARINA_GRID_API_KEY")
        if api_key is None:
            raise ArinaDocumentIntelligenceAPIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the ARINA_GRID_API_KEY environment variable"
            )
        self.api_key = api_key
        if base_url is None:
            base_url = os.environ.get("ARINA_GRID_BASE_URL")
        if base_url is None:
            raise ArinaDocumentIntelligenceAPIError(
                "The base_url client option must be set either by passing base_url to the client or by setting the ARINA_GRID_BASE_URL environment variable"
            )
        custom_headers_env = os.environ.get("ARINA_GRID_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}
        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )
        self._idempotency_header = None
        self._default_stream_cls = Stream

    @cached_property
    def extraction(self) -> "ExtractionResource":
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extraction import ExtractionResource
        return ExtractionResource(self)

    @cached_property
    def parse(self) -> "ParseResource":
        with _RESOURCE_IMPORT_LOCK:
            from .resources.parse import ParseResource
        return ParseResource(self)

    @cached_property
    def extractors(self) -> "ExtractorsResource":
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extractors import ExtractorsResource
        return ExtractorsResource(self)

    @cached_property
    def with_raw_response(self) -> ArinaDocumentIntelligenceAPIWithRawResponse:
        return ArinaDocumentIntelligenceAPIWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ArinaDocumentIntelligenceAPIWithStreamedResponse:
        return ArinaDocumentIntelligenceAPIWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {
            **self._api_key_header_auth,
        }

    @override
    def _auth_query(self, security: dict[str, bool]) -> dict[str, str]:
        _ = security
        return {}

    @override
    def _auth_cookies(self, security: dict[str, bool]) -> dict[str, str]:
        _ = security
        return {}

    @property
    def _api_key_header_auth(self) -> dict[str, str]:
        value = self.api_key
        if value is None:
            return {}
        return {"X-API-Key": value}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Scalar-Async": "false",
            **self._custom_headers,
        }

    @override
    def _validate_headers(
        self,
        headers: Headers,
        custom_headers: Headers,
        params: Mapping[str, object],
        cookies: Mapping[str, str],
    ) -> None:
        if headers.get("X-API-Key"):
            return
        if isinstance(custom_headers.get("X-API-Key"), Omit):
            return
        raise TypeError(
            '"Could not resolve authentication method. Expected the api_key to be set. Or for the `X-API-Key` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """Create a new client reusing this client's options with optional overrides."""
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")
        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")
        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers
        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query
        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            _strict_response_validation=self._strict_response_validation,
            **_extra_kwargs,
        )

    with_options = copy

    @override
    def _make_status_error(self, err_msg: str, *, body: object, response: httpx.Response) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)
        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)
        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)
        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)
        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)
        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)
        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)
        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncArinaDocumentIntelligenceAPI(AsyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncArinaDocumentIntelligenceAPI client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ARINA_GRID_API_KEY`
        """
        if api_key is None:
            api_key = os.environ.get("ARINA_GRID_API_KEY")
        if api_key is None:
            raise ArinaDocumentIntelligenceAPIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the ARINA_GRID_API_KEY environment variable"
            )
        self.api_key = api_key
        if base_url is None:
            base_url = os.environ.get("ARINA_GRID_BASE_URL")
        if base_url is None:
            raise ArinaDocumentIntelligenceAPIError(
                "The base_url client option must be set either by passing base_url to the client or by setting the ARINA_GRID_BASE_URL environment variable"
            )
        custom_headers_env = os.environ.get("ARINA_GRID_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}
        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )
        self._idempotency_header = None
        self._default_stream_cls = AsyncStream

    @cached_property
    def extraction(self) -> "AsyncExtractionResource":
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extraction import AsyncExtractionResource
        return AsyncExtractionResource(self)

    @cached_property
    def parse(self) -> "AsyncParseResource":
        with _RESOURCE_IMPORT_LOCK:
            from .resources.parse import AsyncParseResource
        return AsyncParseResource(self)

    @cached_property
    def extractors(self) -> "AsyncExtractorsResource":
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extractors import AsyncExtractorsResource
        return AsyncExtractorsResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncArinaDocumentIntelligenceAPIWithRawResponse:
        return AsyncArinaDocumentIntelligenceAPIWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncArinaDocumentIntelligenceAPIWithStreamedResponse:
        return AsyncArinaDocumentIntelligenceAPIWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {
            **self._api_key_header_auth,
        }

    @override
    def _auth_query(self, security: dict[str, bool]) -> dict[str, str]:
        _ = security
        return {}

    @override
    def _auth_cookies(self, security: dict[str, bool]) -> dict[str, str]:
        _ = security
        return {}

    @property
    def _api_key_header_auth(self) -> dict[str, str]:
        value = self.api_key
        if value is None:
            return {}
        return {"X-API-Key": value}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Scalar-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    def _validate_headers(
        self,
        headers: Headers,
        custom_headers: Headers,
        params: Mapping[str, object],
        cookies: Mapping[str, str],
    ) -> None:
        if headers.get("X-API-Key"):
            return
        if isinstance(custom_headers.get("X-API-Key"), Omit):
            return
        raise TypeError(
            '"Could not resolve authentication method. Expected the api_key to be set. Or for the `X-API-Key` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """Create a new client reusing this client's options with optional overrides."""
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")
        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")
        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers
        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query
        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            _strict_response_validation=self._strict_response_validation,
            **_extra_kwargs,
        )

    with_options = copy

    @override
    def _make_status_error(self, err_msg: str, *, body: object, response: httpx.Response) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)
        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)
        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)
        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)
        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)
        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)
        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)
        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class ArinaDocumentIntelligenceAPIWithRawResponse:
    _client: ArinaDocumentIntelligenceAPI

    def __init__(self, client: ArinaDocumentIntelligenceAPI) -> None:
        self._client = client

    @cached_property
    def extraction(self) -> extraction.ExtractionResourceWithRawResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extraction import ExtractionResourceWithRawResponse
        return ExtractionResourceWithRawResponse(self._client.extraction)

    @cached_property
    def parse(self) -> parse.ParseResourceWithRawResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.parse import ParseResourceWithRawResponse
        return ParseResourceWithRawResponse(self._client.parse)

    @cached_property
    def extractors(self) -> extractors.ExtractorsResourceWithRawResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extractors import ExtractorsResourceWithRawResponse
        return ExtractorsResourceWithRawResponse(self._client.extractors)


class AsyncArinaDocumentIntelligenceAPIWithRawResponse:
    _client: AsyncArinaDocumentIntelligenceAPI

    def __init__(self, client: AsyncArinaDocumentIntelligenceAPI) -> None:
        self._client = client

    @cached_property
    def extraction(self) -> extraction.AsyncExtractionResourceWithRawResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extraction import AsyncExtractionResourceWithRawResponse
        return AsyncExtractionResourceWithRawResponse(self._client.extraction)

    @cached_property
    def parse(self) -> parse.AsyncParseResourceWithRawResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.parse import AsyncParseResourceWithRawResponse
        return AsyncParseResourceWithRawResponse(self._client.parse)

    @cached_property
    def extractors(self) -> extractors.AsyncExtractorsResourceWithRawResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extractors import AsyncExtractorsResourceWithRawResponse
        return AsyncExtractorsResourceWithRawResponse(self._client.extractors)


class ArinaDocumentIntelligenceAPIWithStreamedResponse:
    _client: ArinaDocumentIntelligenceAPI

    def __init__(self, client: ArinaDocumentIntelligenceAPI) -> None:
        self._client = client

    @cached_property
    def extraction(self) -> extraction.ExtractionResourceWithStreamingResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extraction import ExtractionResourceWithStreamingResponse
        return ExtractionResourceWithStreamingResponse(self._client.extraction)

    @cached_property
    def parse(self) -> parse.ParseResourceWithStreamingResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.parse import ParseResourceWithStreamingResponse
        return ParseResourceWithStreamingResponse(self._client.parse)

    @cached_property
    def extractors(self) -> extractors.ExtractorsResourceWithStreamingResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extractors import ExtractorsResourceWithStreamingResponse
        return ExtractorsResourceWithStreamingResponse(self._client.extractors)


class AsyncArinaDocumentIntelligenceAPIWithStreamedResponse:
    _client: AsyncArinaDocumentIntelligenceAPI

    def __init__(self, client: AsyncArinaDocumentIntelligenceAPI) -> None:
        self._client = client

    @cached_property
    def extraction(self) -> extraction.AsyncExtractionResourceWithStreamingResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extraction import AsyncExtractionResourceWithStreamingResponse
        return AsyncExtractionResourceWithStreamingResponse(self._client.extraction)

    @cached_property
    def parse(self) -> parse.AsyncParseResourceWithStreamingResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.parse import AsyncParseResourceWithStreamingResponse
        return AsyncParseResourceWithStreamingResponse(self._client.parse)

    @cached_property
    def extractors(self) -> extractors.AsyncExtractorsResourceWithStreamingResponse:
        with _RESOURCE_IMPORT_LOCK:
            from .resources.extractors import AsyncExtractorsResourceWithStreamingResponse
        return AsyncExtractorsResourceWithStreamingResponse(self._client.extractors)


# Alias names for the documented `Client` / `AsyncClient` symbols.
Client = ArinaDocumentIntelligenceAPI
AsyncClient = AsyncArinaDocumentIntelligenceAPI

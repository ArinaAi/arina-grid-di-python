# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform, strip_not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.extractors.extractor_version_list import ExtractorVersionList
from ...types.extractors import version_list_params, version_retrieve_params
from ...types.extractors.extractor_version import ExtractorVersion

__all__ = ["VersionsResource", "AsyncVersionsResource"]


class VersionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VersionsResourceWithRawResponse:
        return VersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VersionsResourceWithStreamingResponse:
        return VersionsResourceWithStreamingResponse(self)

    def list(
        self,
        extractor_id: str,
        *,
        organization_id: str,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExtractorVersionList:
        """
        Every immutable config snapshot, newest first.

        Args:
            extractor_id: Path parameter.
            organization_id: Tenant that owns the resource.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractorVersionList: The versions, newest first.

        Example:
            ```python
            version = client.extractors.versions.list(
                extractor_id="extractorId",
                organization_id="organization_id",
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._get(
            path_template("/extractors/{extractor_id}/versions", **{"extractor_id": extractor_id}),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"organization_id": organization_id}, version_list_params.VersionListParams),
            ),
            cast_to=ExtractorVersionList,
        )

    def retrieve(
        self,
        version: int,
        *,
        extractor_id: str,
        organization_id: str,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExtractorVersion:
        """
        One config snapshot by number.

        Args:
            version: Path parameter.
            extractor_id: Path parameter.
            organization_id: Tenant that owns the resource.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractorVersion: The version.

        Example:
            ```python
            version = client.extractors.versions.retrieve(
                extractor_id="extractorId",
                version=1,
                organization_id="organization_id",
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        if version is None or (isinstance(version, str) and not version):
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._get(
            path_template(
                "/extractors/{extractor_id}/versions/{version}", **{"extractor_id": extractor_id, "version": version}
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"organization_id": organization_id}, version_retrieve_params.VersionRetrieveParams
                ),
            ),
            cast_to=ExtractorVersion,
        )


class AsyncVersionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVersionsResourceWithStreamingResponse:
        return AsyncVersionsResourceWithStreamingResponse(self)

    async def list(
        self,
        extractor_id: str,
        *,
        organization_id: str,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExtractorVersionList:
        """
        Every immutable config snapshot, newest first.

        Args:
            extractor_id: Path parameter.
            organization_id: Tenant that owns the resource.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractorVersionList: The versions, newest first.

        Example:
            ```python
            version = await client.extractors.versions.list(
                extractor_id="extractorId",
                organization_id="organization_id",
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._get(
            path_template("/extractors/{extractor_id}/versions", **{"extractor_id": extractor_id}),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"organization_id": organization_id}, version_list_params.VersionListParams
                ),
            ),
            cast_to=ExtractorVersionList,
        )

    async def retrieve(
        self,
        version: int,
        *,
        extractor_id: str,
        organization_id: str,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExtractorVersion:
        """
        One config snapshot by number.

        Args:
            version: Path parameter.
            extractor_id: Path parameter.
            organization_id: Tenant that owns the resource.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractorVersion: The version.

        Example:
            ```python
            version = await client.extractors.versions.retrieve(
                extractor_id="extractorId",
                version=1,
                organization_id="organization_id",
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        if version is None or (isinstance(version, str) and not version):
            raise ValueError(f"Expected a non-empty value for `version` but received {version!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._get(
            path_template(
                "/extractors/{extractor_id}/versions/{version}", **{"extractor_id": extractor_id, "version": version}
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"organization_id": organization_id}, version_retrieve_params.VersionRetrieveParams
                ),
            ),
            cast_to=ExtractorVersion,
        )


class VersionsResourceWithRawResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.list = to_raw_response_wrapper(
            versions.list,
        )
        self.retrieve = to_raw_response_wrapper(
            versions.retrieve,
        )


class AsyncVersionsResourceWithRawResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.list = async_to_raw_response_wrapper(
            versions.list,
        )
        self.retrieve = async_to_raw_response_wrapper(
            versions.retrieve,
        )


class VersionsResourceWithStreamingResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.list = to_streamed_response_wrapper(
            versions.list,
        )
        self.retrieve = to_streamed_response_wrapper(
            versions.retrieve,
        )


class AsyncVersionsResourceWithStreamingResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.list = async_to_streamed_response_wrapper(
            versions.list,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            versions.retrieve,
        )

# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

import httpx

from typing import Dict, Optional
from typing_extensions import Literal

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
from .versions import (
    VersionsResource,
    AsyncVersionsResource,
    VersionsResourceWithRawResponse,
    AsyncVersionsResourceWithRawResponse,
    VersionsResourceWithStreamingResponse,
    AsyncVersionsResourceWithStreamingResponse,
)
from ...types.extractor import Extractor
from ...types.extract_config_param import ExtractConfigParam
from ...types import (
    extractor_create_params,
    extractor_list_params,
    extractor_retrieve_params,
    extractor_update_params,
    extractor_delete_params,
)
from ...types.extractor_list import ExtractorList
from ...types.extractor_delete_response import ExtractorDeleteResponse

__all__ = ["ExtractorsResource", "AsyncExtractorsResource"]


class ExtractorsResource(SyncAPIResource):
    @cached_property
    def versions(self) -> VersionsResource:
        return VersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ExtractorsResourceWithRawResponse:
        return ExtractorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExtractorsResourceWithStreamingResponse:
        return ExtractorsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        organization_id: str,
        name: str,
        description: Optional[str] | Omit = omit,
        config: ExtractConfigParam,
        metadata: Optional[Dict[str, object]] | Omit = omit,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Extractor:
        """
        Save a named, versioned extraction configuration. The schema is validated here, so a mistake is a 422 at save time.

        Args:
            organization_id: Body parameter.
            name: Body parameter.
            description: Body parameter.
            config: Extraction parameters for one run.
            metadata: Body parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            Extractor: Created at version 1.

        Example:
            ```python
            extractor = client.extractors.create(
                organization_id="org_123",
                name="Invoice — EU vendors",
                description=None,
                config={
                    "jsonSchema": {"type": "object", "properties": {"invoiceTotal": {"type": ["number", "null"]}}},
                    "citationsEnabled": True,
                },
                metadata=None,
            )
            ```
        """
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._post(
            "/extractors",
            body=maybe_transform(
                {
                    "organization_id": organization_id,
                    "name": name,
                    "description": description,
                    "config": config,
                    "metadata": metadata,
                },
                extractor_create_params.ExtractorCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Extractor,
        )

    def list(
        self,
        *,
        organization_id: str,
        status: Literal["ACTIVE", "ARCHIVED", "all"] | Omit = omit,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExtractorList:
        """
        A tenant's extractors, `ACTIVE` by default. `status=ARCHIVED|all` to widen.

        Args:
            organization_id: Tenant that owns the resource.
            status: Query parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractorList: The list.

        Example:
            ```python
            extractor = client.extractors.list(
                organization_id="organization_id",
            )
            ```
        """
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._get(
            "/extractors",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"organization_id": organization_id, "status": status}, extractor_list_params.ExtractorListParams
                ),
            ),
            cast_to=ExtractorList,
        )

    def retrieve(
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
    ) -> Extractor:
        """
        The current version of one extractor.

        Args:
            extractor_id: Path parameter.
            organization_id: Tenant that owns the resource.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            Extractor: The extractor.

        Example:
            ```python
            extractor = client.extractors.retrieve(
                extractor_id="extractorId",
                organization_id="organization_id",
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._get(
            path_template("/extractors/{extractor_id}", **{"extractor_id": extractor_id}),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"organization_id": organization_id}, extractor_retrieve_params.ExtractorRetrieveParams
                ),
            ),
            cast_to=Extractor,
        )

    def update(
        self,
        extractor_id: str,
        *,
        organization_id: str,
        name: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        config: Optional[ExtractConfigParam] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
        version: Optional[int] | Omit = omit,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Extractor:
        """
        Rename, describe or reconfigure. Only a `config` change bumps the version. Send `version` to get a 409 on a stale edit.

        Args:
            extractor_id: Path parameter.
            organization_id: Body parameter.
            name: Body parameter.
            description: Body parameter.
            config: Extraction parameters for one run.
            metadata: Body parameter.
            version: Expected current version; 409 if it has moved on
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            Extractor: The updated extractor. A config change bumps `version`; a rename does not.

        Example:
            ```python
            extractor = client.extractors.update(
                extractor_id="extractorId",
                organization_id="x",
                name=None,
                description=None,
                config=None,
                metadata=None,
                version=None,
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._patch(
            path_template("/extractors/{extractor_id}", **{"extractor_id": extractor_id}),
            body=maybe_transform(
                {
                    "organization_id": organization_id,
                    "name": name,
                    "description": description,
                    "config": config,
                    "metadata": metadata,
                    "version": version,
                },
                extractor_update_params.ExtractorUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Extractor,
        )

    def delete(
        self,
        extractor_id: str,
        *,
        organization_id: str,
        permanent: bool | Omit = omit,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExtractorDeleteResponse:
        """
        Archive by default (record and versions kept, new runs refused). `permanent=true` removes the record and every version; runs already made keep their frozen config.

        Args:
            extractor_id: Path parameter.
            organization_id: Tenant that owns the resource.
            permanent: Query parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractorDeleteResponse: Archived extractor (default), or `{object, id, deleted: true}` when `permanent=true`.

        Example:
            ```python
            extractor = client.extractors.delete(
                extractor_id="extractorId",
                organization_id="organization_id",
                permanent=False,
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._delete(
            path_template("/extractors/{extractor_id}", **{"extractor_id": extractor_id}),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"organization_id": organization_id, "permanent": permanent},
                    extractor_delete_params.ExtractorDeleteParams,
                ),
            ),
            cast_to=ExtractorDeleteResponse,
        )


class AsyncExtractorsResource(AsyncAPIResource):
    @cached_property
    def versions(self) -> AsyncVersionsResource:
        return AsyncVersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncExtractorsResourceWithRawResponse:
        return AsyncExtractorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExtractorsResourceWithStreamingResponse:
        return AsyncExtractorsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        organization_id: str,
        name: str,
        description: Optional[str] | Omit = omit,
        config: ExtractConfigParam,
        metadata: Optional[Dict[str, object]] | Omit = omit,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Extractor:
        """
        Save a named, versioned extraction configuration. The schema is validated here, so a mistake is a 422 at save time.

        Args:
            organization_id: Body parameter.
            name: Body parameter.
            description: Body parameter.
            config: Extraction parameters for one run.
            metadata: Body parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            Extractor: Created at version 1.

        Example:
            ```python
            extractor = await client.extractors.create(
                organization_id="org_123",
                name="Invoice — EU vendors",
                description=None,
                config={
                    "jsonSchema": {"type": "object", "properties": {"invoiceTotal": {"type": ["number", "null"]}}},
                    "citationsEnabled": True,
                },
                metadata=None,
            )
            ```
        """
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._post(
            "/extractors",
            body=await async_maybe_transform(
                {
                    "organization_id": organization_id,
                    "name": name,
                    "description": description,
                    "config": config,
                    "metadata": metadata,
                },
                extractor_create_params.ExtractorCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Extractor,
        )

    async def list(
        self,
        *,
        organization_id: str,
        status: Literal["ACTIVE", "ARCHIVED", "all"] | Omit = omit,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExtractorList:
        """
        A tenant's extractors, `ACTIVE` by default. `status=ARCHIVED|all` to widen.

        Args:
            organization_id: Tenant that owns the resource.
            status: Query parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractorList: The list.

        Example:
            ```python
            extractor = await client.extractors.list(
                organization_id="organization_id",
            )
            ```
        """
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._get(
            "/extractors",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"organization_id": organization_id, "status": status}, extractor_list_params.ExtractorListParams
                ),
            ),
            cast_to=ExtractorList,
        )

    async def retrieve(
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
    ) -> Extractor:
        """
        The current version of one extractor.

        Args:
            extractor_id: Path parameter.
            organization_id: Tenant that owns the resource.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            Extractor: The extractor.

        Example:
            ```python
            extractor = await client.extractors.retrieve(
                extractor_id="extractorId",
                organization_id="organization_id",
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._get(
            path_template("/extractors/{extractor_id}", **{"extractor_id": extractor_id}),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"organization_id": organization_id}, extractor_retrieve_params.ExtractorRetrieveParams
                ),
            ),
            cast_to=Extractor,
        )

    async def update(
        self,
        extractor_id: str,
        *,
        organization_id: str,
        name: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        config: Optional[ExtractConfigParam] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
        version: Optional[int] | Omit = omit,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Extractor:
        """
        Rename, describe or reconfigure. Only a `config` change bumps the version. Send `version` to get a 409 on a stale edit.

        Args:
            extractor_id: Path parameter.
            organization_id: Body parameter.
            name: Body parameter.
            description: Body parameter.
            config: Extraction parameters for one run.
            metadata: Body parameter.
            version: Expected current version; 409 if it has moved on
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            Extractor: The updated extractor. A config change bumps `version`; a rename does not.

        Example:
            ```python
            extractor = await client.extractors.update(
                extractor_id="extractorId",
                organization_id="x",
                name=None,
                description=None,
                config=None,
                metadata=None,
                version=None,
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._patch(
            path_template("/extractors/{extractor_id}", **{"extractor_id": extractor_id}),
            body=await async_maybe_transform(
                {
                    "organization_id": organization_id,
                    "name": name,
                    "description": description,
                    "config": config,
                    "metadata": metadata,
                    "version": version,
                },
                extractor_update_params.ExtractorUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Extractor,
        )

    async def delete(
        self,
        extractor_id: str,
        *,
        organization_id: str,
        permanent: bool | Omit = omit,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExtractorDeleteResponse:
        """
        Archive by default (record and versions kept, new runs refused). `permanent=true` removes the record and every version; runs already made keep their frozen config.

        Args:
            extractor_id: Path parameter.
            organization_id: Tenant that owns the resource.
            permanent: Query parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractorDeleteResponse: Archived extractor (default), or `{object, id, deleted: true}` when `permanent=true`.

        Example:
            ```python
            extractor = await client.extractors.delete(
                extractor_id="extractorId",
                organization_id="organization_id",
                permanent=False,
            )
            ```
        """
        if extractor_id is None or (isinstance(extractor_id, str) and not extractor_id):
            raise ValueError(f"Expected a non-empty value for `extractor_id` but received {extractor_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._delete(
            path_template("/extractors/{extractor_id}", **{"extractor_id": extractor_id}),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"organization_id": organization_id, "permanent": permanent},
                    extractor_delete_params.ExtractorDeleteParams,
                ),
            ),
            cast_to=ExtractorDeleteResponse,
        )


class ExtractorsResourceWithRawResponse:
    def __init__(self, extractors: ExtractorsResource) -> None:
        self._extractors = extractors

        self.create = to_raw_response_wrapper(
            extractors.create,
        )
        self.list = to_raw_response_wrapper(
            extractors.list,
        )
        self.retrieve = to_raw_response_wrapper(
            extractors.retrieve,
        )
        self.update = to_raw_response_wrapper(
            extractors.update,
        )
        self.delete = to_raw_response_wrapper(
            extractors.delete,
        )

    @cached_property
    def versions(self) -> VersionsResourceWithRawResponse:
        return VersionsResourceWithRawResponse(self._extractors.versions)


class AsyncExtractorsResourceWithRawResponse:
    def __init__(self, extractors: AsyncExtractorsResource) -> None:
        self._extractors = extractors

        self.create = async_to_raw_response_wrapper(
            extractors.create,
        )
        self.list = async_to_raw_response_wrapper(
            extractors.list,
        )
        self.retrieve = async_to_raw_response_wrapper(
            extractors.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            extractors.update,
        )
        self.delete = async_to_raw_response_wrapper(
            extractors.delete,
        )

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self._extractors.versions)


class ExtractorsResourceWithStreamingResponse:
    def __init__(self, extractors: ExtractorsResource) -> None:
        self._extractors = extractors

        self.create = to_streamed_response_wrapper(
            extractors.create,
        )
        self.list = to_streamed_response_wrapper(
            extractors.list,
        )
        self.retrieve = to_streamed_response_wrapper(
            extractors.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            extractors.update,
        )
        self.delete = to_streamed_response_wrapper(
            extractors.delete,
        )

    @cached_property
    def versions(self) -> VersionsResourceWithStreamingResponse:
        return VersionsResourceWithStreamingResponse(self._extractors.versions)


class AsyncExtractorsResourceWithStreamingResponse:
    def __init__(self, extractors: AsyncExtractorsResource) -> None:
        self._extractors = extractors

        self.create = async_to_streamed_response_wrapper(
            extractors.create,
        )
        self.list = async_to_streamed_response_wrapper(
            extractors.list,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            extractors.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            extractors.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            extractors.delete,
        )

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithStreamingResponse:
        return AsyncVersionsResourceWithStreamingResponse(self._extractors.versions)

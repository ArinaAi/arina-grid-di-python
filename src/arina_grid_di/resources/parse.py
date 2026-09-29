# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

import httpx

from typing import Mapping, cast
from .._types import FileTypes

from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._files import deepcopy_with_paths
from .._utils import extract_files, path_template, maybe_transform, async_maybe_transform, strip_not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.parse_run import ParseRun
from ..types import parse_create_run_params

__all__ = ["ParseResource", "AsyncParseResource"]


class ParseResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ParseResourceWithRawResponse:
        return ParseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ParseResourceWithStreamingResponse:
        return ParseResourceWithStreamingResponse(self)

    def create_run(
        self,
        *,
        file: FileTypes,
        config: str,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseRun:
        """
        Read page 1 into layout blocks, tables (HTML) and markdown — no schema. `202`: poll `GET /parse_runs/{id}`.

        Args:
            file: Document to process. PDF, PNG or JPEG. Page 1 only. Max 15 MB.
            config: Parse configuration: the `ParseRunRequest` object, JSON-encoded into this single form field (e.g. `json.dumps(...)` / `JSON.stringify(...)`). See the `ParseRunRequest` schema for the fields.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ParseRun: Run accepted.

        Example:
            ```python
            parse = client.parse.create_run(
                file=b"file",
                config='{"organizationId": "org_123", "config": {"includeTextLines": false}}',
            )
            ```
        """
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        body = deepcopy_with_paths(
            {
                "file": file,
                "config": config,
            },
            [["file"]],
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/parse_runs",
            body=maybe_transform(body, parse_create_run_params.ParseCreateRunParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseRun,
        )

    def retrieve_run(
        self,
        run_id: str,
        *,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseRun:
        """
        Report a run's status, and its parsed output once finished.

        Args:
            run_id: Path parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ParseRun: The run.

        Example:
            ```python
            parse = client.parse.retrieve_run(
                run_id="runId",
            )
            ```
        """
        if run_id is None or (isinstance(run_id, str) and not run_id):
            raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._get(
            path_template("/parse_runs/{run_id}", **{"run_id": run_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseRun,
        )

    def list_run_page(
        self,
        run_id: str,
        *,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """
        Serve the page image the output polygons were measured against.

        Args:
            run_id: Path parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            BinaryAPIResponse: The rendered page image (JPEG). Overlay polygons are in its frame.

        Example:
            ```python
            parse = client.parse.list_run_page(
                run_id="runId",
            )
            ```
        """
        if run_id is None or (isinstance(run_id, str) and not run_id):
            raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        extra_headers = {"Accept": "image/jpeg", **(extra_headers or {})}
        return self._get(
            path_template("/parse_runs/{run_id}/page", **{"run_id": run_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncParseResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncParseResourceWithRawResponse:
        return AsyncParseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncParseResourceWithStreamingResponse:
        return AsyncParseResourceWithStreamingResponse(self)

    async def create_run(
        self,
        *,
        file: FileTypes,
        config: str,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseRun:
        """
        Read page 1 into layout blocks, tables (HTML) and markdown — no schema. `202`: poll `GET /parse_runs/{id}`.

        Args:
            file: Document to process. PDF, PNG or JPEG. Page 1 only. Max 15 MB.
            config: Parse configuration: the `ParseRunRequest` object, JSON-encoded into this single form field (e.g. `json.dumps(...)` / `JSON.stringify(...)`). See the `ParseRunRequest` schema for the fields.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ParseRun: Run accepted.

        Example:
            ```python
            parse = await client.parse.create_run(
                file=b"file",
                config='{"organizationId": "org_123", "config": {"includeTextLines": false}}',
            )
            ```
        """
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        body = deepcopy_with_paths(
            {
                "file": file,
                "config": config,
            },
            [["file"]],
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/parse_runs",
            body=await async_maybe_transform(body, parse_create_run_params.ParseCreateRunParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseRun,
        )

    async def retrieve_run(
        self,
        run_id: str,
        *,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParseRun:
        """
        Report a run's status, and its parsed output once finished.

        Args:
            run_id: Path parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ParseRun: The run.

        Example:
            ```python
            parse = await client.parse.retrieve_run(
                run_id="runId",
            )
            ```
        """
        if run_id is None or (isinstance(run_id, str) and not run_id):
            raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._get(
            path_template("/parse_runs/{run_id}", **{"run_id": run_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParseRun,
        )

    async def list_run_page(
        self,
        run_id: str,
        *,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """
        Serve the page image the output polygons were measured against.

        Args:
            run_id: Path parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            AsyncBinaryAPIResponse: The rendered page image (JPEG). Overlay polygons are in its frame.

        Example:
            ```python
            parse = await client.parse.list_run_page(
                run_id="runId",
            )
            ```
        """
        if run_id is None or (isinstance(run_id, str) and not run_id):
            raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        extra_headers = {"Accept": "image/jpeg", **(extra_headers or {})}
        return await self._get(
            path_template("/parse_runs/{run_id}/page", **{"run_id": run_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ParseResourceWithRawResponse:
    def __init__(self, parse: ParseResource) -> None:
        self._parse = parse

        self.create_run = to_raw_response_wrapper(
            parse.create_run,
        )
        self.retrieve_run = to_raw_response_wrapper(
            parse.retrieve_run,
        )
        self.list_run_page = to_custom_raw_response_wrapper(
            parse.list_run_page,
            BinaryAPIResponse,
        )


class AsyncParseResourceWithRawResponse:
    def __init__(self, parse: AsyncParseResource) -> None:
        self._parse = parse

        self.create_run = async_to_raw_response_wrapper(
            parse.create_run,
        )
        self.retrieve_run = async_to_raw_response_wrapper(
            parse.retrieve_run,
        )
        self.list_run_page = async_to_custom_raw_response_wrapper(
            parse.list_run_page,
            AsyncBinaryAPIResponse,
        )


class ParseResourceWithStreamingResponse:
    def __init__(self, parse: ParseResource) -> None:
        self._parse = parse

        self.create_run = to_streamed_response_wrapper(
            parse.create_run,
        )
        self.retrieve_run = to_streamed_response_wrapper(
            parse.retrieve_run,
        )
        self.list_run_page = to_custom_streamed_response_wrapper(
            parse.list_run_page,
            StreamedBinaryAPIResponse,
        )


class AsyncParseResourceWithStreamingResponse:
    def __init__(self, parse: AsyncParseResource) -> None:
        self._parse = parse

        self.create_run = async_to_streamed_response_wrapper(
            parse.create_run,
        )
        self.retrieve_run = async_to_streamed_response_wrapper(
            parse.retrieve_run,
        )
        self.list_run_page = async_to_custom_streamed_response_wrapper(
            parse.list_run_page,
            AsyncStreamedBinaryAPIResponse,
        )

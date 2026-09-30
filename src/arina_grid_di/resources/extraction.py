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
from ..types.extract_run import ExtractRun
from ..types import extraction_create_extract_run_params

__all__ = ["ExtractionResource", "AsyncExtractionResource"]


class ExtractionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ExtractionResourceWithRawResponse:
        return ExtractionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExtractionResourceWithStreamingResponse:
        return ExtractionResourceWithStreamingResponse(self)

    def create_extract_run(
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
    ) -> ExtractRun:
        """
        Accept a document and return a run to poll. `config.config` is either an inline `jsonSchema`/`extractionRules`, or an `extractorId` (optionally with `extractorVersion`) naming a saved extractor. `202`: accepted, not complete — poll `GET /extract_runs/{id}`.

        Args:
            file: Document to process. PDF, PNG or JPEG. Page 1 only. Max 15 MB.
            config: Extraction configuration: the `ExtractRunRequest` object, JSON-encoded into this single form field (e.g. `json.dumps(...)` / `JSON.stringify(...)`). See the `ExtractRunRequest` schema for the fields.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractRun: Run accepted.

        Example:
            ```python
            extraction = client.extraction.create_extract_run(
                file=b"file",
                config='{"organizationId": "org_123", "config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
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
            "/extract_runs",
            body=maybe_transform(body, extraction_create_extract_run_params.ExtractionCreateExtractRunParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExtractRun,
        )

    def retrieve_extract_run(
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
    ) -> ExtractRun:
        """
        Report a run's status, and its output with citations once finished.

        Args:
            run_id: Path parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractRun: The run.

        Example:
            ```python
            extraction = client.extraction.retrieve_extract_run(
                run_id="runId",
            )
            ```
        """
        if run_id is None or (isinstance(run_id, str) and not run_id):
            raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._get(
            path_template("/extract_runs/{run_id}", **{"run_id": run_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExtractRun,
        )

    def list_extract_run_page(
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
        Serve the page image a run's citation polygons were measured against.

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
            extraction = client.extraction.list_extract_run_page(
                run_id="runId",
            )
            ```
        """
        if run_id is None or (isinstance(run_id, str) and not run_id):
            raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        extra_headers = {"Accept": "image/jpeg", **(extra_headers or {})}
        return self._get(
            path_template("/extract_runs/{run_id}/page", **{"run_id": run_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncExtractionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncExtractionResourceWithRawResponse:
        return AsyncExtractionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExtractionResourceWithStreamingResponse:
        return AsyncExtractionResourceWithStreamingResponse(self)

    async def create_extract_run(
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
    ) -> ExtractRun:
        """
        Accept a document and return a run to poll. `config.config` is either an inline `jsonSchema`/`extractionRules`, or an `extractorId` (optionally with `extractorVersion`) naming a saved extractor. `202`: accepted, not complete — poll `GET /extract_runs/{id}`.

        Args:
            file: Document to process. PDF, PNG or JPEG. Page 1 only. Max 15 MB.
            config: Extraction configuration: the `ExtractRunRequest` object, JSON-encoded into this single form field (e.g. `json.dumps(...)` / `JSON.stringify(...)`). See the `ExtractRunRequest` schema for the fields.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractRun: Run accepted.

        Example:
            ```python
            extraction = await client.extraction.create_extract_run(
                file=b"file",
                config='{"organizationId": "org_123", "config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
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
            "/extract_runs",
            body=await async_maybe_transform(
                body, extraction_create_extract_run_params.ExtractionCreateExtractRunParams
            ),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExtractRun,
        )

    async def retrieve_extract_run(
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
    ) -> ExtractRun:
        """
        Report a run's status, and its output with citations once finished.

        Args:
            run_id: Path parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            ExtractRun: The run.

        Example:
            ```python
            extraction = await client.extraction.retrieve_extract_run(
                run_id="runId",
            )
            ```
        """
        if run_id is None or (isinstance(run_id, str) and not run_id):
            raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._get(
            path_template("/extract_runs/{run_id}", **{"run_id": run_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExtractRun,
        )

    async def list_extract_run_page(
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
        Serve the page image a run's citation polygons were measured against.

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
            extraction = await client.extraction.list_extract_run_page(
                run_id="runId",
            )
            ```
        """
        if run_id is None or (isinstance(run_id, str) and not run_id):
            raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        extra_headers = {"Accept": "image/jpeg", **(extra_headers or {})}
        return await self._get(
            path_template("/extract_runs/{run_id}/page", **{"run_id": run_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ExtractionResourceWithRawResponse:
    def __init__(self, extraction: ExtractionResource) -> None:
        self._extraction = extraction

        self.create_extract_run = to_raw_response_wrapper(
            extraction.create_extract_run,
        )
        self.retrieve_extract_run = to_raw_response_wrapper(
            extraction.retrieve_extract_run,
        )
        self.list_extract_run_page = to_custom_raw_response_wrapper(
            extraction.list_extract_run_page,
            BinaryAPIResponse,
        )


class AsyncExtractionResourceWithRawResponse:
    def __init__(self, extraction: AsyncExtractionResource) -> None:
        self._extraction = extraction

        self.create_extract_run = async_to_raw_response_wrapper(
            extraction.create_extract_run,
        )
        self.retrieve_extract_run = async_to_raw_response_wrapper(
            extraction.retrieve_extract_run,
        )
        self.list_extract_run_page = async_to_custom_raw_response_wrapper(
            extraction.list_extract_run_page,
            AsyncBinaryAPIResponse,
        )


class ExtractionResourceWithStreamingResponse:
    def __init__(self, extraction: ExtractionResource) -> None:
        self._extraction = extraction

        self.create_extract_run = to_streamed_response_wrapper(
            extraction.create_extract_run,
        )
        self.retrieve_extract_run = to_streamed_response_wrapper(
            extraction.retrieve_extract_run,
        )
        self.list_extract_run_page = to_custom_streamed_response_wrapper(
            extraction.list_extract_run_page,
            StreamedBinaryAPIResponse,
        )


class AsyncExtractionResourceWithStreamingResponse:
    def __init__(self, extraction: AsyncExtractionResource) -> None:
        self._extraction = extraction

        self.create_extract_run = async_to_streamed_response_wrapper(
            extraction.create_extract_run,
        )
        self.retrieve_extract_run = async_to_streamed_response_wrapper(
            extraction.retrieve_extract_run,
        )
        self.list_extract_run_page = async_to_custom_streamed_response_wrapper(
            extraction.list_extract_run_page,
            AsyncStreamedBinaryAPIResponse,
        )

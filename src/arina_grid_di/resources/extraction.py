# File generated from our OpenAPI spec by Scalar. See README.md for details.

from __future__ import annotations

import httpx

from typing import Mapping, cast
from .._types import FileTypes, SequenceNotStr

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
from ..types import extraction_create_extract_run_params, extraction_create_extract_batch_params
from ..types.run_batch import RunBatch

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
                config='{"config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
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

    def create_extract_batch(
        self,
        *,
        files: SequenceNotStr[FileTypes],
        config: str,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RunBatch:
        """
        Accept up to 100 documents under one `config` and return a batch to poll. Each document becomes an ordinary extraction run, listed in `items` with its run id; results are read from the runs. The request is checked whole: one file of the wrong type or size refuses all of it, naming the files. Available where queued execution is enabled.

        Args:
            files: Documents to process, one part per file under this name. PDF, PNG or JPEG; page 1 of each. Up to 100 files, 15 MB each, 90 MB per request.
            config: Extraction configuration: the `ExtractRunRequest` object, JSON-encoded into this single form field (e.g. `json.dumps(...)` / `JSON.stringify(...)`). See the `ExtractRunRequest` schema for the fields. Applied to every document.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            RunBatch: Batch accepted. Every document the service could take in is now a queued run, named in `items`; one it could not is an item with `runId: null` and `status: FAILED`.

        Example:
            ```python
            extraction = client.extraction.create_extract_batch(
                files=[b"file"],
                config='{"config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
            )
            ```
        """
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        body = deepcopy_with_paths(
            {
                "files": files,
                "config": config,
            },
            [["files", "<array>"]],
        )
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]], array_format="repeat")
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/extract_runs/batches",
            body=maybe_transform(body, extraction_create_extract_batch_params.ExtractionCreateExtractBatchParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RunBatch,
        )

    def retrieve_extract_batch(
        self,
        batch_id: str,
        *,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RunBatch:
        """
        Report a batch's progress: `status`, `counts`, and each document's run and state. Poll this instead of every run; when `status` is `COMPLETED`, read the results from `GET /extract_runs/{id}` for the items you want.

        Args:
            batch_id: Path parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            RunBatch: The batch as it stands now: each item's `status` is its run's, `counts` add them up, `updatedAt` is the latest change among the runs. Not cacheable.

        Example:
            ```python
            extraction = client.extraction.retrieve_extract_batch(
                batch_id="batchId",
            )
            ```
        """
        if batch_id is None or (isinstance(batch_id, str) and not batch_id):
            raise ValueError(f"Expected a non-empty value for `batch_id` but received {batch_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return self._get(
            path_template("/extract_runs/batches/{batch_id}", **{"batch_id": batch_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RunBatch,
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
                config='{"config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
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

    async def create_extract_batch(
        self,
        *,
        files: SequenceNotStr[FileTypes],
        config: str,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RunBatch:
        """
        Accept up to 100 documents under one `config` and return a batch to poll. Each document becomes an ordinary extraction run, listed in `items` with its run id; results are read from the runs. The request is checked whole: one file of the wrong type or size refuses all of it, naming the files. Available where queued execution is enabled.

        Args:
            files: Documents to process, one part per file under this name. PDF, PNG or JPEG; page 1 of each. Up to 100 files, 15 MB each, 90 MB per request.
            config: Extraction configuration: the `ExtractRunRequest` object, JSON-encoded into this single form field (e.g. `json.dumps(...)` / `JSON.stringify(...)`). See the `ExtractRunRequest` schema for the fields. Applied to every document.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            RunBatch: Batch accepted. Every document the service could take in is now a queued run, named in `items`; one it could not is an item with `runId: null` and `status: FAILED`.

        Example:
            ```python
            extraction = await client.extraction.create_extract_batch(
                files=[b"file"],
                config='{"config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
            )
            ```
        """
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        body = deepcopy_with_paths(
            {
                "files": files,
                "config": config,
            },
            [["files", "<array>"]],
        )
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]], array_format="repeat")
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/extract_runs/batches",
            body=await async_maybe_transform(
                body, extraction_create_extract_batch_params.ExtractionCreateExtractBatchParams
            ),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RunBatch,
        )

    async def retrieve_extract_batch(
        self,
        batch_id: str,
        *,
        x_api_version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RunBatch:
        """
        Report a batch's progress: `status`, `counts`, and each document's run and state. Poll this instead of every run; when `status` is `COMPLETED`, read the results from `GET /extract_runs/{id}` for the items you want.

        Args:
            batch_id: Path parameter.
            x_api_version: Contract version. Currently only `2026-09-05`. Omit to get the current version. An unsupported value is rejected with 400.
            extra_headers: Send extra headers with the request.
            extra_query: Send extra query parameters with the request.
            extra_body: Send extra JSON properties with the request.
            timeout: Override the client-level default timeout for this request, in seconds.

        Returns:
            RunBatch: The batch as it stands now: each item's `status` is its run's, `counts` add them up, `updatedAt` is the latest change among the runs. Not cacheable.

        Example:
            ```python
            extraction = await client.extraction.retrieve_extract_batch(
                batch_id="batchId",
            )
            ```
        """
        if batch_id is None or (isinstance(batch_id, str) and not batch_id):
            raise ValueError(f"Expected a non-empty value for `batch_id` but received {batch_id!r}")
        extra_headers = {**strip_not_given({"X-Api-Version": x_api_version}), **(extra_headers or {})}
        return await self._get(
            path_template("/extract_runs/batches/{batch_id}", **{"batch_id": batch_id}),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RunBatch,
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
        self.create_extract_batch = to_raw_response_wrapper(
            extraction.create_extract_batch,
        )
        self.retrieve_extract_batch = to_raw_response_wrapper(
            extraction.retrieve_extract_batch,
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
        self.create_extract_batch = async_to_raw_response_wrapper(
            extraction.create_extract_batch,
        )
        self.retrieve_extract_batch = async_to_raw_response_wrapper(
            extraction.retrieve_extract_batch,
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
        self.create_extract_batch = to_streamed_response_wrapper(
            extraction.create_extract_batch,
        )
        self.retrieve_extract_batch = to_streamed_response_wrapper(
            extraction.retrieve_extract_batch,
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
        self.create_extract_batch = async_to_streamed_response_wrapper(
            extraction.create_extract_batch,
        )
        self.retrieve_extract_batch = async_to_streamed_response_wrapper(
            extraction.retrieve_extract_batch,
        )

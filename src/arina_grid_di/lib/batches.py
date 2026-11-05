"""Many documents in one request: submit within the batch limits and wait for the batch to complete.

A batch is a handle on a set of runs. Its ``status`` is ``COMPLETED`` once every member run is
terminal; failures live in ``counts.failed`` and the ``FAILED`` items, never on the batch, so
there is nothing to raise on. Results are read from the member runs.
"""

from __future__ import annotations

import json
import os
from collections.abc import Awaitable, Callable, Iterable, Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, BinaryIO, Union

from .polling import _poll, _poll_async

if TYPE_CHECKING:
    from .._client import ArinaDocumentIntelligenceAPI, AsyncArinaDocumentIntelligenceAPI
    from ..types.run_batch import RunBatch

#: The one status after which a batch no longer changes.
BATCH_COMPLETED = "COMPLETED"

#: The API's limits per request, checked here before anything is sent.
MAX_BATCH_FILES = 100
MAX_FILE_BYTES = 15 * 1024 * 1024
MAX_BATCH_BYTES = 90 * 1024 * 1024

#: What the batch endpoints take, by file suffix, and the content type sent for each.
DOCUMENT_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}

# A hundred documents take minutes, not seconds: poll less often and wait longer than for a run.
DEFAULT_BATCH_TIMEOUT = 1800.0
DEFAULT_BATCH_INTERVAL = 2.0
DEFAULT_BATCH_MAX_INTERVAL = 10.0

#: A directory, one file, or any iterable of files.
Documents = Union[str, "os.PathLike[str]", Iterable[Union[str, "os.PathLike[str]"]]]
Config = Union[str, Mapping[str, Any]]


class BatchTimeoutError(TimeoutError):
    """The batch did not complete within ``timeout`` seconds. Its runs keep going server-side."""

    def __init__(self, batch: RunBatch, timeout: float) -> None:
        self.batch = batch
        self.timeout = timeout
        progress = ""
        if batch.counts is not None:
            done = (batch.counts.processed or 0) + (batch.counts.failed or 0)
            progress = f" ({done} of {batch.counts.total or 0} documents finished)"
        super().__init__(
            f"batch {batch.id!r} still {batch.status!r} after {timeout:g}s{progress}; it keeps running server-side"
        )


# Waiting


def _completed(on_poll: Callable[[RunBatch], None] | None) -> Callable[[RunBatch], RunBatch | None]:
    def check(batch: RunBatch) -> RunBatch | None:
        if on_poll is not None:
            on_poll(batch)
        return batch if batch.status == BATCH_COMPLETED else None

    return check


def wait_for_parse_batch(
    client: ArinaDocumentIntelligenceAPI,
    batch_id: str,
    *,
    timeout: float = DEFAULT_BATCH_TIMEOUT,
    interval: float = DEFAULT_BATCH_INTERVAL,
    max_interval: float = DEFAULT_BATCH_MAX_INTERVAL,
    on_poll: Callable[[RunBatch], None] | None = None,
) -> RunBatch:
    """Poll ``GET /parse_runs/batches/{batch_id}`` until ``COMPLETED`` and return the batch.

    Args:
        timeout: Overall seconds before :class:`BatchTimeoutError`.
        interval: First delay between polls; grows 1.5x per poll up to ``max_interval``.
        on_poll: Called with the batch after every poll, for progress (``batch.counts``).
    """
    return _poll(
        lambda: client.parse.retrieve_batch(batch_id),
        timeout=timeout,
        interval=interval,
        max_interval=max_interval,
        check=_completed(on_poll),
        timed_out=BatchTimeoutError,
    )


def wait_for_extract_batch(
    client: ArinaDocumentIntelligenceAPI,
    batch_id: str,
    *,
    timeout: float = DEFAULT_BATCH_TIMEOUT,
    interval: float = DEFAULT_BATCH_INTERVAL,
    max_interval: float = DEFAULT_BATCH_MAX_INTERVAL,
    on_poll: Callable[[RunBatch], None] | None = None,
) -> RunBatch:
    """Poll ``GET /extract_runs/batches/{batch_id}`` until ``COMPLETED`` and return the batch.

    Same arguments as :func:`wait_for_parse_batch`.
    """
    return _poll(
        lambda: client.extraction.retrieve_extract_batch(batch_id),
        timeout=timeout,
        interval=interval,
        max_interval=max_interval,
        check=_completed(on_poll),
        timed_out=BatchTimeoutError,
    )


async def wait_for_parse_batch_async(
    client: AsyncArinaDocumentIntelligenceAPI,
    batch_id: str,
    *,
    timeout: float = DEFAULT_BATCH_TIMEOUT,
    interval: float = DEFAULT_BATCH_INTERVAL,
    max_interval: float = DEFAULT_BATCH_MAX_INTERVAL,
    on_poll: Callable[[RunBatch], None] | None = None,
) -> RunBatch:
    """Async :func:`wait_for_parse_batch`."""
    return await _poll_async(
        lambda: client.parse.retrieve_batch(batch_id),
        timeout=timeout,
        interval=interval,
        max_interval=max_interval,
        check=_completed(on_poll),
        timed_out=BatchTimeoutError,
    )


async def wait_for_extract_batch_async(
    client: AsyncArinaDocumentIntelligenceAPI,
    batch_id: str,
    *,
    timeout: float = DEFAULT_BATCH_TIMEOUT,
    interval: float = DEFAULT_BATCH_INTERVAL,
    max_interval: float = DEFAULT_BATCH_MAX_INTERVAL,
    on_poll: Callable[[RunBatch], None] | None = None,
) -> RunBatch:
    """Async :func:`wait_for_extract_batch`."""
    return await _poll_async(
        lambda: client.extraction.retrieve_extract_batch(batch_id),
        timeout=timeout,
        interval=interval,
        max_interval=max_interval,
        check=_completed(on_poll),
        timed_out=BatchTimeoutError,
    )


# Submitting


def plan_batches(documents: Documents) -> list[list[Path]]:
    """Group documents into requests that fit the API's limits, in the order given.

    A directory means the documents in it (by suffix, sorted by name, not recursive); anything
    else is a file or an iterable of files. Every file is checked before anything is sent, so a
    file the API would refuse costs no upload: :class:`ValueError` names it.
    """
    paths = _resolve(documents)
    if not paths:
        raise ValueError("no documents to submit")
    groups: list[list[Path]] = []
    current: list[Path] = []
    current_bytes = 0
    for path in paths:
        size = _check(path)
        if current and (len(current) == MAX_BATCH_FILES or current_bytes + size > MAX_BATCH_BYTES):
            groups.append(current)
            current, current_bytes = [], 0
        current.append(path)
        current_bytes += size
    groups.append(current)
    return groups


def _resolve(documents: Documents) -> list[Path]:
    if isinstance(documents, (str, os.PathLike)):
        path = Path(documents)
        if path.is_dir():
            return sorted(p for p in path.iterdir() if p.is_file() and p.suffix.lower() in DOCUMENT_TYPES)
        return [path]
    return [Path(p) for p in documents]


def _check(path: Path) -> int:
    """The file's size, once it is known to be a document the API takes."""
    if path.suffix.lower() not in DOCUMENT_TYPES:
        raise ValueError(
            f"{path}: unsupported type {path.suffix or '(no suffix)'!r}; the API takes {', '.join(DOCUMENT_TYPES)}"
        )
    size = path.stat().st_size
    if size > MAX_FILE_BYTES:
        raise ValueError(
            f"{path}: {size / (1024 * 1024):.1f} MB exceeds the {MAX_FILE_BYTES // (1024 * 1024)} MB limit per file"
        )
    return size


def _config_json(config: Config) -> str:
    return config if isinstance(config, str) else json.dumps(config)


def _parts(group: list[Path], handles: list[BinaryIO]) -> list[tuple[str, BinaryIO, str]]:
    return [(path.name, handle, DOCUMENT_TYPES[path.suffix.lower()]) for path, handle in zip(group, handles)]


def _submit(create: Callable[..., RunBatch], group: list[Path], config: str) -> RunBatch:
    handles = [path.open("rb") for path in group]
    try:
        return create(files=_parts(group, handles), config=config)
    finally:
        for handle in handles:
            handle.close()


async def _submit_async(create: Callable[..., Awaitable[RunBatch]], group: list[Path], config: str) -> RunBatch:
    handles = [path.open("rb") for path in group]
    try:
        return await create(files=_parts(group, handles), config=config)
    finally:
        for handle in handles:
            handle.close()


def submit_parse_batches(client: ArinaDocumentIntelligenceAPI, documents: Documents, config: Config) -> list[RunBatch]:
    """``POST /parse_runs/batches`` once per group from :func:`plan_batches`; the batches, in order.

    Args:
        documents: A directory, a file, or an iterable of files (PDF, PNG, JPEG).
        config: The ``ParseRunRequest`` as a JSON string, or a mapping to encode.
    """
    config = _config_json(config)
    return [_submit(client.parse.create_batch, group, config) for group in plan_batches(documents)]


def submit_extract_batches(
    client: ArinaDocumentIntelligenceAPI, documents: Documents, config: Config
) -> list[RunBatch]:
    """``POST /extract_runs/batches`` once per group from :func:`plan_batches`; the batches, in order.

    Same arguments as :func:`submit_parse_batches`; ``config`` is the ``ExtractRunRequest``.
    """
    config = _config_json(config)
    return [_submit(client.extraction.create_extract_batch, group, config) for group in plan_batches(documents)]


async def submit_parse_batches_async(
    client: AsyncArinaDocumentIntelligenceAPI, documents: Documents, config: Config
) -> list[RunBatch]:
    """Async :func:`submit_parse_batches`."""
    config = _config_json(config)
    return [await _submit_async(client.parse.create_batch, group, config) for group in plan_batches(documents)]


async def submit_extract_batches_async(
    client: AsyncArinaDocumentIntelligenceAPI, documents: Documents, config: Config
) -> list[RunBatch]:
    """Async :func:`submit_extract_batches`."""
    config = _config_json(config)
    return [
        await _submit_async(client.extraction.create_extract_batch, group, config) for group in plan_batches(documents)
    ]

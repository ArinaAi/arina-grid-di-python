"""Poll extraction and parse runs to a terminal status with backoff and a deadline.

`status` is an open string in the contract: anything not in TERMINAL_STATUSES counts as running.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, TypeVar, Union

if TYPE_CHECKING:
    from .._client import ArinaDocumentIntelligenceAPI, AsyncArinaDocumentIntelligenceAPI
    from ..types.extract_run import ExtractRun
    from ..types.parse_run import ParseRun

    Run = Union[ExtractRun, ParseRun]

RunT = TypeVar("RunT")

#: Statuses after which a run no longer changes.
TERMINAL_STATUSES = frozenset({"PROCESSED", "FAILED", "CANCELLED"})

DEFAULT_TIMEOUT = 120.0
DEFAULT_INTERVAL = 1.0
DEFAULT_MAX_INTERVAL = 5.0
_BACKOFF = 1.5


class RunTimeoutError(TimeoutError):
    """The run did not reach a terminal status within ``timeout`` seconds."""

    def __init__(self, run: Run, timeout: float) -> None:
        self.run = run
        self.timeout = timeout
        super().__init__(f"run {run.id!r} still {run.status!r} after {timeout:g}s; it keeps running server-side")


class RunFailedError(RuntimeError):
    """The run finished as ``FAILED`` or ``CANCELLED``. The run is on ``.run``."""

    def __init__(self, run: Run) -> None:
        self.run = run
        reason = getattr(run, "failure_reason", None)
        message = getattr(run, "failure_message", None)
        detail = ": ".join(part for part in (reason, message) if part)
        super().__init__(f"run {run.id!r} ended {run.status}" + (f" ({detail})" if detail else ""))


def _validate(timeout: float, interval: float, max_interval: float) -> float:
    """Validate polling settings; return the effective max_interval (never below interval)."""
    if not timeout > 0:
        raise ValueError(f"timeout must be > 0 seconds, got {timeout!r}")
    if not interval > 0:
        raise ValueError(f"interval must be > 0 seconds, got {interval!r}")
    return max(max_interval, interval)


def _check_terminal(run: RunT, *, raise_on_failure: bool) -> RunT | None:
    """Return the run if terminal (raising on failure when asked), else ``None``."""
    status = getattr(run, "status", None)
    if status not in TERMINAL_STATUSES:
        return None
    if status != "PROCESSED" and raise_on_failure:
        raise RunFailedError(run)  # type: ignore[arg-type]
    return run


def _poll(
    fetch: Callable[[], RunT],
    *,
    timeout: float,
    interval: float,
    max_interval: float,
    raise_on_failure: bool,
) -> RunT:
    max_interval = _validate(timeout, interval, max_interval)
    deadline = time.monotonic() + timeout
    delay = interval
    while True:
        run = fetch()
        done = _check_terminal(run, raise_on_failure=raise_on_failure)
        if done is not None:
            return done
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RunTimeoutError(run, timeout)  # type: ignore[arg-type]
        time.sleep(min(delay, remaining))
        delay = min(delay * _BACKOFF, max_interval)


async def _poll_async(
    fetch: Callable[[], Awaitable[RunT]],
    *,
    timeout: float,
    interval: float,
    max_interval: float,
    raise_on_failure: bool,
) -> RunT:
    max_interval = _validate(timeout, interval, max_interval)
    deadline = time.monotonic() + timeout
    delay = interval
    while True:
        run = await fetch()
        done = _check_terminal(run, raise_on_failure=raise_on_failure)
        if done is not None:
            return done
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RunTimeoutError(run, timeout)  # type: ignore[arg-type]
        await asyncio.sleep(min(delay, remaining))
        delay = min(delay * _BACKOFF, max_interval)


def wait_for_extract_run(
    client: ArinaDocumentIntelligenceAPI,
    run_id: str,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    interval: float = DEFAULT_INTERVAL,
    max_interval: float = DEFAULT_MAX_INTERVAL,
    raise_on_failure: bool = True,
) -> ExtractRun:
    """Poll ``GET /extract_runs/{run_id}`` until terminal and return the run.

    Args:
        timeout: Overall seconds before :class:`RunTimeoutError`.
        interval: First delay between polls; grows 1.5x per poll up to ``max_interval``.
        raise_on_failure: Raise :class:`RunFailedError` on FAILED/CANCELLED instead of returning.
    """
    return _poll(
        lambda: client.extraction.retrieve_extract_run(run_id),
        timeout=timeout,
        interval=interval,
        max_interval=max_interval,
        raise_on_failure=raise_on_failure,
    )


def wait_for_parse_run(
    client: ArinaDocumentIntelligenceAPI,
    run_id: str,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    interval: float = DEFAULT_INTERVAL,
    max_interval: float = DEFAULT_MAX_INTERVAL,
    raise_on_failure: bool = True,
) -> ParseRun:
    """Poll ``GET /parse_runs/{run_id}`` until terminal and return the run.

    Same arguments as :func:`wait_for_extract_run`.
    """
    return _poll(
        lambda: client.parse.retrieve_run(run_id),
        timeout=timeout,
        interval=interval,
        max_interval=max_interval,
        raise_on_failure=raise_on_failure,
    )


async def wait_for_extract_run_async(
    client: AsyncArinaDocumentIntelligenceAPI,
    run_id: str,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    interval: float = DEFAULT_INTERVAL,
    max_interval: float = DEFAULT_MAX_INTERVAL,
    raise_on_failure: bool = True,
) -> ExtractRun:
    """Async :func:`wait_for_extract_run`."""
    return await _poll_async(
        lambda: client.extraction.retrieve_extract_run(run_id),
        timeout=timeout,
        interval=interval,
        max_interval=max_interval,
        raise_on_failure=raise_on_failure,
    )


async def wait_for_parse_run_async(
    client: AsyncArinaDocumentIntelligenceAPI,
    run_id: str,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    interval: float = DEFAULT_INTERVAL,
    max_interval: float = DEFAULT_MAX_INTERVAL,
    raise_on_failure: bool = True,
) -> ParseRun:
    """Async :func:`wait_for_parse_run`."""
    return await _poll_async(
        lambda: client.parse.retrieve_run(run_id),
        timeout=timeout,
        interval=interval,
        max_interval=max_interval,
        raise_on_failure=raise_on_failure,
    )

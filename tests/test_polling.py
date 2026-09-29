"""Polling helpers in arina_document_intelligence.lib."""

from __future__ import annotations

import re
from itertools import chain, repeat

import httpx
import pytest

from arina_document_intelligence.lib import (
    RunFailedError,
    RunTimeoutError,
    wait_for_extract_run,
    wait_for_extract_run_async,
    wait_for_parse_run,
)

from .conftest import run_payload

FAST = {"interval": 0.001, "max_interval": 0.002}


def scripted(kind: str, *statuses: str, **last_overrides: object):
    """Answer successive polls with the given statuses; the last one repeats forever."""
    sequence = chain(statuses, repeat(statuses[-1]))

    def responder(request: httpx.Request) -> httpx.Response:
        status = next(sequence)
        overrides = last_overrides if status == statuses[-1] else {}
        return httpx.Response(200, json=run_payload(kind, status=status, **overrides))

    return responder


def test_returns_when_processed_after_several_polls(make_client):
    client, rec = make_client(
        scripted(
            "extract_run",
            "PROCESSING",
            "PROCESSING",
            "PROCESSED",
            output={"value": {"total": 42.5}, "metadata": {}, "pageImage": None},
        )
    )

    run = wait_for_extract_run(client, "run_1", timeout=5, **FAST)

    assert run.status == "PROCESSED"
    assert run.output is not None and run.output.value == {"total": 42.5}
    assert len(rec.requests) == 3
    assert all(r.url.path == "/extract_runs/run_1" for r in rec.requests)


def test_parse_run_polls_the_parse_endpoint(make_client):
    client, rec = make_client(scripted("parse_run", "PROCESSED"))
    run = wait_for_parse_run(client, "run_1", timeout=5, **FAST)
    assert run.status == "PROCESSED"
    assert rec.last.url.path == "/parse_runs/run_1"


def test_failed_run_raises_with_reason_and_run_attached(make_client):
    client, _ = make_client(
        scripted("extract_run", "PROCESSING", "FAILED", failureReason="UNREADABLE", failureMessage="blank page")
    )
    with pytest.raises(RunFailedError) as excinfo:
        wait_for_extract_run(client, "run_1", timeout=5, **FAST)
    assert excinfo.value.run.status == "FAILED"
    assert "UNREADABLE: blank page" in str(excinfo.value)


def test_failed_run_is_returned_when_asked_not_to_raise(make_client):
    client, _ = make_client(scripted("extract_run", "CANCELLED"))
    run = wait_for_extract_run(client, "run_1", timeout=5, raise_on_failure=False, **FAST)
    assert run.status == "CANCELLED"


def test_unknown_status_is_treated_as_still_running(make_client):
    # `status` is an open string in the contract; a new value must not be mistaken for done.
    client, rec = make_client(scripted("extract_run", "QUEUED_SOMEWHERE_NEW", "PROCESSED"))
    run = wait_for_extract_run(client, "run_1", timeout=5, **FAST)
    assert run.status == "PROCESSED" and len(rec.requests) == 2


def test_timeout_raises_and_reports_last_status(make_client):
    client, rec = make_client(scripted("extract_run", "PROCESSING"))
    with pytest.raises(RunTimeoutError) as excinfo:
        wait_for_extract_run(client, "run_1", timeout=0.02, **FAST)
    assert excinfo.value.run.status == "PROCESSING"
    assert excinfo.value.timeout == 0.02
    assert len(rec.requests) >= 2, "polled more than once before giving up"


@pytest.mark.asyncio
async def test_async_helper_polls_until_processed(make_async_client):
    client, rec = make_async_client(scripted("extract_run", "PROCESSING", "PROCESSED"))
    run = await wait_for_extract_run_async(client, "run_1", timeout=5, **FAST)
    assert run.status == "PROCESSED" and len(rec.requests) == 2


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"timeout": 0}, "timeout must be > 0"),
        ({"timeout": -1}, "timeout must be > 0"),
        ({"interval": 0}, "interval must be > 0"),
    ],
)
def test_rejects_settings_that_would_spin_or_never_poll(make_client, kwargs, message):
    client, rec = make_client(scripted("extract_run", "PROCESSING"))
    with pytest.raises(ValueError, match=re.escape(message)):
        wait_for_extract_run(client, "run_1", **kwargs)
    assert rec.requests == [], "invalid settings are rejected before any request is made"


@pytest.mark.asyncio
async def test_async_helper_rejects_invalid_settings_too(make_async_client):
    client, rec = make_async_client(scripted("extract_run", "PROCESSING"))
    with pytest.raises(ValueError, match="interval must be > 0"):
        await wait_for_extract_run_async(client, "run_1", interval=0)
    assert rec.requests == []


def test_interval_above_max_interval_disables_backoff_instead_of_failing(make_client):
    # A caller asking for a slow fixed cadence must not be punished for leaving max_interval
    # at its default (5s): the effective cap is raised to the interval.
    client, rec = make_client(scripted("extract_run", "PROCESSING", "PROCESSED"))
    run = wait_for_extract_run(client, "run_1", timeout=5, interval=0.002, max_interval=0.001)
    assert run.status == "PROCESSED" and len(rec.requests) == 2

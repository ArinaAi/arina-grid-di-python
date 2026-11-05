"""Batch helpers in arina_grid_di.lib: waiting for a batch, planning and submitting documents."""

from __future__ import annotations

import json
from itertools import chain, repeat
from pathlib import Path

import httpx
import pytest

from arina_grid_di.lib import (
    BatchTimeoutError,
    plan_batches,
    submit_extract_batches,
    submit_parse_batches,
    submit_parse_batches_async,
    wait_for_extract_batch,
    wait_for_parse_batch,
    wait_for_parse_batch_async,
)
from arina_grid_di.lib import batches as batches_module

from .conftest import batch_payload

FAST = {"interval": 0.001, "max_interval": 0.002}
DONE = {"total": 2, "pending": 0, "processing": 0, "processed": 1, "failed": 1}


def scripted(kind: str, *statuses: str, **last_overrides: object):
    """Answer successive polls with the given statuses; the last one repeats forever."""
    sequence = chain(statuses, repeat(statuses[-1]))

    def responder(request: httpx.Request) -> httpx.Response:
        status = next(sequence)
        overrides = last_overrides if status == statuses[-1] else {}
        return httpx.Response(200, json=batch_payload(kind, status=status, **overrides))

    return responder


# Waiting


def test_returns_when_completed_after_several_polls(make_client):
    client, rec = make_client(scripted("parse_batch", "PENDING", "PROCESSING", "COMPLETED", counts=DONE))

    batch = wait_for_parse_batch(client, "pbt_1", timeout=5, **FAST)

    assert batch.status == "COMPLETED"
    assert batch.counts is not None and batch.counts.failed == 1
    assert len(rec.requests) == 3
    assert all(r.url.path == "/parse_runs/batches/pbt_1" for r in rec.requests)


def test_extract_batch_polls_the_extract_endpoint(make_client):
    client, rec = make_client(scripted("extract_batch", "COMPLETED"))
    batch = wait_for_extract_batch(client, "pbt_1", timeout=5, **FAST)
    assert batch.object == "extract_batch"
    assert rec.last.url.path == "/extract_runs/batches/pbt_1"


def test_a_batch_with_failed_documents_is_still_completed(make_client):
    # Failures live in the counts and the items; the batch itself never fails, so nothing is raised.
    client, _ = make_client(
        scripted(
            "parse_batch",
            "COMPLETED",
            counts={"total": 2, "pending": 0, "processing": 0, "processed": 0, "failed": 2},
        )
    )
    batch = wait_for_parse_batch(client, "pbt_1", timeout=5, **FAST)
    assert batch.status == "COMPLETED"
    assert batch.counts is not None and batch.counts.failed == 2


def test_timeout_raises_with_the_batch_and_its_progress(make_client):
    client, _ = make_client(scripted("parse_batch", "PROCESSING"))
    with pytest.raises(BatchTimeoutError) as excinfo:
        wait_for_parse_batch(client, "pbt_1", timeout=0.01, **FAST)
    error = excinfo.value
    assert error.batch.status == "PROCESSING"
    assert error.timeout == 0.01
    assert "1 of 2 documents finished" in str(error)
    assert isinstance(error, TimeoutError)


def test_unknown_status_is_treated_as_still_running(make_client):
    # `status` is an open string in the contract; a new value must not be mistaken for done.
    client, rec = make_client(scripted("parse_batch", "PAUSED_SOMEWHERE_NEW", "COMPLETED"))
    batch = wait_for_parse_batch(client, "pbt_1", timeout=5, **FAST)
    assert batch.status == "COMPLETED"
    assert len(rec.requests) == 2


def test_on_poll_sees_every_poll_including_the_last(make_client):
    client, _ = make_client(scripted("parse_batch", "PENDING", "PROCESSING", "COMPLETED", counts=DONE))
    seen: list[str] = []
    wait_for_parse_batch(client, "pbt_1", timeout=5, on_poll=lambda b: seen.append(b.status or ""), **FAST)
    assert seen == ["PENDING", "PROCESSING", "COMPLETED"]


def test_invalid_settings_are_refused_before_any_request(make_client):
    client, rec = make_client(scripted("parse_batch", "COMPLETED"))
    with pytest.raises(ValueError):
        wait_for_parse_batch(client, "pbt_1", timeout=0)
    assert rec.requests == []


@pytest.mark.asyncio
async def test_async_waiter(make_async_client):
    client, rec = make_async_client(scripted("parse_batch", "PROCESSING", "COMPLETED", counts=DONE))
    batch = await wait_for_parse_batch_async(client, "pbt_1", timeout=5, **FAST)
    assert batch.status == "COMPLETED"
    assert len(rec.requests) == 2


# Planning


def _write(folder: Path, name: str, size: int = 4) -> Path:
    path = folder / name
    path.write_bytes(b"x" * size)
    return path


def test_a_directory_means_its_documents_sorted_by_name(tmp_path):
    _write(tmp_path, "b.pdf")
    _write(tmp_path, "A.PNG")
    _write(tmp_path, "c.jpeg")
    _write(tmp_path, "notes.txt")  # not a document: skipped, not refused
    (tmp_path / "sub").mkdir()
    _write(tmp_path / "sub", "d.pdf")  # not recursive

    [group] = plan_batches(tmp_path)

    assert [p.name for p in group] == ["A.PNG", "b.pdf", "c.jpeg"]


def test_an_explicit_list_keeps_its_order(tmp_path):
    paths = [_write(tmp_path, "z.pdf"), _write(tmp_path, "a.pdf")]
    [group] = plan_batches([str(paths[0]), paths[1]])
    assert group == paths


def test_a_single_file_is_a_batch_of_one(tmp_path):
    path = _write(tmp_path, "one.pdf")
    assert plan_batches(path) == [[path]]


def test_groups_split_at_the_file_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(batches_module, "MAX_BATCH_FILES", 2)
    paths = [_write(tmp_path, f"{i}.pdf") for i in range(5)]
    groups = plan_batches(paths)
    assert [len(g) for g in groups] == [2, 2, 1]
    assert [p for g in groups for p in g] == paths


def test_groups_split_when_the_next_file_would_exceed_the_byte_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(batches_module, "MAX_BATCH_BYTES", 10)
    paths = [_write(tmp_path, f"{i}.pdf", size=4) for i in range(3)]
    assert plan_batches(paths) == [paths[:2], paths[2:]]


def test_a_file_over_the_per_file_limit_is_refused_by_name(tmp_path, monkeypatch):
    monkeypatch.setattr(batches_module, "MAX_FILE_BYTES", 3)
    big = _write(tmp_path, "big.pdf", size=4)
    with pytest.raises(ValueError, match="big.pdf"):
        plan_batches([_write(tmp_path, "ok.pdf", size=3), big])


def test_an_unsupported_type_in_an_explicit_list_is_refused_by_name(tmp_path):
    with pytest.raises(ValueError, match="notes.txt"):
        plan_batches([_write(tmp_path, "a.pdf"), _write(tmp_path, "notes.txt")])


def test_nothing_to_submit_is_refused(tmp_path):
    with pytest.raises(ValueError, match="no documents"):
        plan_batches(tmp_path)
    with pytest.raises(ValueError, match="no documents"):
        plan_batches([])


# Submitting


def accepted(kind: str = "parse_batch"):
    """Answer each POST with a fresh batch id, so the order of the returned batches can be checked."""
    counter = iter(range(1, 100))

    def responder(request: httpx.Request) -> httpx.Response:
        return httpx.Response(202, json=batch_payload(kind, id=f"pbt_{next(counter)}", status="PENDING"))

    return responder


def test_submits_one_request_per_group_with_repeated_file_parts(make_client, tmp_path, monkeypatch):
    monkeypatch.setattr(batches_module, "MAX_BATCH_FILES", 2)
    client, rec = make_client(accepted())
    _write(tmp_path, "a.pdf", size=3)
    _write(tmp_path, "b.jpg", size=5)
    _write(tmp_path, "c.png", size=7)

    batches = submit_parse_batches(client, tmp_path, '{"config": {"includeTextLines": true}}')

    assert [b.id for b in batches] == ["pbt_1", "pbt_2"]
    assert [r.url.path for r in rec.requests] == ["/parse_runs/batches"] * 2

    first = rec.parts_of(rec.requests[0])
    assert [name for name, _ in first] == ["config", "files", "files"]
    assert first[0][1]["data"] == b'{"config": {"includeTextLines": true}}'
    assert [(p["filename"], p["content_type"], len(p["data"])) for _, p in first[1:]] == [
        ("a.pdf", "application/pdf", 3),
        ("b.jpg", "image/jpeg", 5),
    ]
    second = rec.parts_of(rec.requests[1])
    assert [(name, p["filename"]) for name, p in second] == [("config", None), ("files", "c.png")]


def test_a_mapping_config_is_json_encoded(make_client, tmp_path):
    client, rec = make_client(accepted())
    _write(tmp_path, "a.pdf")
    submit_parse_batches(client, tmp_path, {"config": {"includeTextLines": False}, "metadata": {"job": 7}})
    config = dict(rec.parts_of(rec.last))["config"]["data"]
    assert json.loads(config) == {"config": {"includeTextLines": False}, "metadata": {"job": 7}}


def test_extract_batches_post_to_the_extract_endpoint(make_client, tmp_path):
    client, rec = make_client(accepted("extract_batch"))
    _write(tmp_path, "a.pdf")
    [batch] = submit_extract_batches(client, tmp_path, '{"config": {"jsonSchema": {"type": "object"}}}')
    assert batch.object == "extract_batch"
    assert rec.last.url.path == "/extract_runs/batches"


def test_nothing_is_sent_when_a_document_would_be_refused(make_client, tmp_path):
    client, rec = make_client(accepted())
    paths = [_write(tmp_path, "a.pdf"), _write(tmp_path, "b.csv")]
    with pytest.raises(ValueError, match="b.csv"):
        submit_parse_batches(client, paths, "{}")
    assert rec.requests == []


def test_file_handles_are_closed_after_the_request(make_client, tmp_path, monkeypatch):
    client, _ = make_client(accepted())
    paths = [_write(tmp_path, "a.pdf"), _write(tmp_path, "b.pdf")]
    opened = []
    real_open = Path.open

    def recording_open(self, *args, **kwargs):
        handle = real_open(self, *args, **kwargs)
        opened.append(handle)
        return handle

    monkeypatch.setattr(Path, "open", recording_open)
    submit_parse_batches(client, paths, "{}")
    assert len(opened) == 2
    assert all(handle.closed for handle in opened)


@pytest.mark.asyncio
async def test_async_submit(make_async_client, tmp_path, monkeypatch):
    monkeypatch.setattr(batches_module, "MAX_BATCH_FILES", 1)
    client, rec = make_async_client(accepted())
    paths = [_write(tmp_path, "a.pdf"), _write(tmp_path, "b.pdf")]
    batches = await submit_parse_batches_async(client, paths, "{}")
    assert [b.id for b in batches] == ["pbt_1", "pbt_2"]
    assert [dict(rec.parts_of(r))["files"]["filename"] for r in rec.requests] == ["a.pdf", "b.pdf"]

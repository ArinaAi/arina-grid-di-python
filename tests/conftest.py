"""Offline client fixtures: httpx.MockTransport records requests; a stdlib multipart parser inspects them."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from email.parser import BytesParser
from email.policy import HTTP

import httpx
import pytest

from arina_grid_di import ArinaDocumentIntelligenceAPI, AsyncArinaDocumentIntelligenceAPI

BASE_URL = "http://api.test"
API_KEY = "test-key"

Responder = Callable[[httpx.Request], httpx.Response]


def run_payload(kind: str = "extract_run", **overrides: object) -> dict:
    """A minimal valid run body, as the API returns it (camelCase, declared fields present)."""
    body: dict = {
        "object": kind,
        "id": "run_1",
        "apiVersion": "2026-09-05",
        "status": "PROCESSING",
        "uploadId": "up_1",
        "documentName": "invoice.pdf",
        "organizationId": "org_123",
        "collection": None,
        "config": {"citationsEnabled": True, "citationMode": "block"}
        if kind == "extract_run"
        else {"includeTextLines": False},
        "output": None,
        "failureReason": None,
        "failureMessage": None,
        "metadata": None,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:00:00Z",
    }
    body.update(overrides)
    return body


def batch_payload(kind: str = "parse_batch", **overrides: object) -> dict:
    """A minimal valid batch body, as the API returns it: two documents, one done, one waiting."""
    body: dict = {
        "object": kind,
        "id": "pbt_1",
        "apiVersion": "2026-09-05",
        "status": "PROCESSING",
        "counts": {"total": 2, "pending": 1, "processing": 0, "processed": 1, "failed": 0},
        "items": [
            {
                "documentName": "a.pdf",
                "runId": "run_1",
                "status": "PROCESSED",
                "failureReason": None,
                "failureMessage": None,
            },
            {
                "documentName": "b.pdf",
                "runId": "run_2",
                "status": "PENDING",
                "failureReason": None,
                "failureMessage": None,
            },
        ],
        "organizationId": "org_123",
        "config": {},
        "metadata": None,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:00:00Z",
    }
    body.update(overrides)
    return body


def multipart_parts(content_type: str, body: bytes) -> list[tuple[str, dict]]:
    """Parse a multipart/form-data body with the stdlib email parser, one entry per part, in order.

    Each entry is ``(field_name, {"data": bytes, "filename": str | None, "content_type": str | None})``;
    a name repeated on the wire (``files``) appears once per part.
    """
    message = BytesParser(policy=HTTP).parsebytes(
        b"Content-Type: " + content_type.encode() + b"\r\nMIME-Version: 1.0\r\n\r\n" + body
    )
    assert message.is_multipart(), "expected a multipart body"
    parts: list[tuple[str, dict]] = []
    for part in message.iter_parts():
        name = part.get_param("name", header="content-disposition")
        assert name is not None, "multipart part without a field name"
        parts.append(
            (
                name,
                {
                    "data": part.get_payload(decode=True),
                    "filename": part.get_filename(),
                    "content_type": part.get_content_type() if "content-type" in part else None,
                },
            )
        )
    return parts


def parse_multipart(content_type: str, body: bytes) -> dict[str, dict]:
    """``multipart_parts`` keyed by field name, for bodies where every name occurs once."""
    return dict(multipart_parts(content_type, body))


@dataclass
class Recorder:
    """Records requests and answers them with a scripted responder."""

    responder: Responder
    requests: list[httpx.Request] = field(default_factory=list)

    def __call__(self, request: httpx.Request) -> httpx.Response:
        request.read()
        self.requests.append(request)
        return self.responder(request)

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]

    def last_multipart(self) -> dict[str, dict]:
        return parse_multipart(self.last.headers["content-type"], self.last.content)

    @staticmethod
    def parts_of(request: httpx.Request) -> list[tuple[str, dict]]:
        return multipart_parts(request.headers["content-type"], request.content)

    def last_json(self) -> object:
        return json.loads(self.last.content)


@pytest.fixture
def make_client():
    """Build a sync client bound to a recorder: ``client, rec = make_client(responder)``."""

    def factory(responder: Responder) -> tuple[ArinaDocumentIntelligenceAPI, Recorder]:
        rec = Recorder(responder)
        client = ArinaDocumentIntelligenceAPI(
            api_key=API_KEY,
            base_url=BASE_URL,
            http_client=httpx.Client(transport=httpx.MockTransport(rec)),
            max_retries=0,
        )
        return client, rec

    return factory


@pytest.fixture
def make_async_client():
    """Async twin of ``make_client``."""

    def factory(responder: Responder) -> tuple[AsyncArinaDocumentIntelligenceAPI, Recorder]:
        rec = Recorder(responder)
        client = AsyncArinaDocumentIntelligenceAPI(
            api_key=API_KEY,
            base_url=BASE_URL,
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(rec)),
            max_retries=0,
        )
        return client, rec

    return factory

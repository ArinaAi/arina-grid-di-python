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


def parse_multipart(content_type: str, body: bytes) -> dict[str, dict]:
    """Parse a multipart/form-data body with the stdlib email parser.

    Returns ``{field_name: {"data": bytes, "filename": str | None, "content_type": str | None}}``.
    """
    message = BytesParser(policy=HTTP).parsebytes(
        b"Content-Type: " + content_type.encode() + b"\r\nMIME-Version: 1.0\r\n\r\n" + body
    )
    assert message.is_multipart(), "expected a multipart body"
    parts: dict[str, dict] = {}
    for part in message.iter_parts():
        name = part.get_param("name", header="content-disposition")
        assert name is not None, "multipart part without a field name"
        parts[name] = {
            "data": part.get_payload(decode=True),
            "filename": part.get_filename(),
            "content_type": part.get_content_type() if "content-type" in part else None,
        }
    return parts


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

    def last_json(self) -> object:
        return json.loads(self.last.content)


@pytest.fixture
def make_client():
    """Build a sync client bound to a recorder: ``client, rec = make_client(responder)``."""

    def factory(responder: Responder) -> tuple[ArinaDocumentIntelligenceAPI, Recorder]:
        rec = Recorder(responder)
        client = ArinaDocumentIntelligenceAPI(
            api_key_auth=API_KEY,
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
            api_key_auth=API_KEY,
            base_url=BASE_URL,
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(rec)),
            max_retries=0,
        )
        return client, rec

    return factory

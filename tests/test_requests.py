"""Wire contract: what the SDK sends must be what the API's routes parse.

Key cases: `config` is ONE multipart form field holding JSON (the server reads `config: str = Form(...)`),
and the API key is the tenant, so no request names an organisation.
"""

from __future__ import annotations

import json

import httpx
import pytest

from arina_grid_di import (
    ArinaDocumentIntelligenceAPI,
    ArinaDocumentIntelligenceAPIError,
    AsyncArinaDocumentIntelligenceAPI,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    UnprocessableEntityError,
)
from arina_grid_di.types.extract_run import ExtractRun
from arina_grid_di.types.extractor import Extractor
from arina_grid_di.types.identity import Identity
from arina_grid_di.types.parse_run import ParseRun

from .conftest import API_KEY, run_payload

EXTRACT_CONFIG = {
    "config": {
        "jsonSchema": {
            "type": "object",
            "properties": {"invoiceTotal": {"type": ["number", "null"]}},
        },
        "citationsEnabled": True,
    },
    "metadata": None,
}

PARSE_CONFIG = {"config": {"includeTextLines": True}}

EXTRACTOR = {
    "object": "extractor",
    "id": "ext_1",
    "organizationId": "org_123",  # reported by the server; never sent by the client
    "name": "Invoices",
    "description": None,
    "version": 1,
    "status": "ACTIVE",
    "config": {"citationsEnabled": True, "citationMode": "block"},
    "metadata": None,
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-01-01T00:00:00Z",
}

IDENTITY = {
    "organization": {"id": "org_123", "slug": "acme"},
    "subject": "key:k_abc",
    "scopes": ["extract", "parse", "extractors:read", "extractors:write"],
    "keyId": "k_abc",
    "user": None,
}


def accepted(kind: str):
    return lambda request: httpx.Response(202, json=run_payload(kind))


def ok(payload: object):
    return lambda request: httpx.Response(200, json=payload)


class TestMultipartRuns:
    def test_extract_run_sends_config_as_single_json_form_field(self, make_client):
        client, rec = make_client(accepted("extract_run"))

        run = client.extraction.create_extract_run(
            file=("invoice.pdf", b"%PDF-1.4 fake", "application/pdf"),
            config=json.dumps(EXTRACT_CONFIG),
        )

        assert rec.last.method == "POST"
        assert rec.last.url.path == "/extract_runs"
        assert rec.last.headers["content-type"].startswith("multipart/form-data")

        parts = rec.last_multipart()
        assert sorted(parts) == ["config", "file"], "exactly two parts, as the route declares"
        assert json.loads(parts["config"]["data"]) == EXTRACT_CONFIG, "config round-trips as JSON"
        assert parts["config"]["data"].count(b"{") >= 2, "nested object stayed nested, not flattened"
        assert parts["file"]["data"] == b"%PDF-1.4 fake"
        assert parts["file"]["filename"] == "invoice.pdf"
        assert parts["file"]["content_type"] == "application/pdf"

        assert isinstance(run, ExtractRun)
        assert run.id == "run_1" and run.status == "PROCESSING"

    def test_parse_run_sends_config_as_single_json_form_field(self, make_client):
        client, rec = make_client(accepted("parse_run"))

        run = client.parse.create_run(
            file=("page.png", b"\x89PNG\r\n\x1a\n", "image/png"),
            config=json.dumps(PARSE_CONFIG),
        )

        parts = rec.last_multipart()
        assert rec.last.url.path == "/parse_runs"
        assert sorted(parts) == ["config", "file"]
        assert json.loads(parts["config"]["data"]) == PARSE_CONFIG
        assert parts["file"]["data"] == b"\x89PNG\r\n\x1a\n"
        assert isinstance(run, ParseRun)

    def test_json_null_survives_the_config_field(self, make_client):
        client, rec = make_client(accepted("extract_run"))
        client.extraction.create_extract_run(file=b"x", config=json.dumps({"config": {}, "metadata": None}))
        assert json.loads(rec.last_multipart()["config"]["data"])["metadata"] is None

    def test_pending_is_a_valid_accepted_status(self, make_client):
        # A queued run is accepted as PENDING; the model must not reject the value.
        client, _ = make_client(lambda r: httpx.Response(202, json=run_payload("parse_run", status="PENDING")))
        run = client.parse.create_run(file=b"x", config="{}")
        assert run.status == "PENDING"

    @pytest.mark.asyncio
    async def test_async_client_sends_the_same_multipart_shape(self, make_async_client):
        client, rec = make_async_client(accepted("extract_run"))
        await client.extraction.create_extract_run(file=b"%PDF", config=json.dumps(EXTRACT_CONFIG))
        parts = rec.last_multipart()
        assert sorted(parts) == ["config", "file"]
        assert json.loads(parts["config"]["data"]) == EXTRACT_CONFIG


class TestHeaders:
    def test_api_key_header_on_every_request(self, make_client):
        client, rec = make_client(ok(run_payload()))
        client.extraction.retrieve_extract_run("run_1")
        assert rec.last.headers["x-api-key"] == API_KEY
        assert "authorization" not in rec.last.headers, "the key is the only credential"

    def test_version_header_only_when_given(self, make_client):
        client, rec = make_client(ok(run_payload()))
        client.extraction.retrieve_extract_run("run_1")
        assert "x-api-version" not in rec.last.headers
        client.extraction.retrieve_extract_run("run_1", x_api_version="2026-09-05")
        assert rec.last.headers["x-api-version"] == "2026-09-05"

    def test_page_image_is_requested_as_jpeg_and_returned_raw(self, make_client):
        client, rec = make_client(
            lambda r: httpx.Response(200, content=b"\xff\xd8\xff\xe0", headers={"content-type": "image/jpeg"})
        )
        image = client.extraction.list_extract_run_page("run_1")
        assert rec.last.url.path == "/extract_runs/run_1/page"
        assert rec.last.headers["accept"] == "image/jpeg"
        assert image.read() == b"\xff\xd8\xff\xe0"


class TestAccount:
    def test_who_am_i_is_a_bare_get_on_me(self, make_client):
        client, rec = make_client(ok(IDENTITY))

        me = client.account.who_am_i()

        assert rec.last.method == "GET" and rec.last.url.path == "/me"
        assert not rec.last.url.params, "the key alone says who is calling"
        assert rec.last.headers["x-api-key"] == API_KEY
        assert isinstance(me, Identity)
        assert me.organization.id == "org_123" and me.organization.slug == "acme"
        assert me.key_id == "k_abc" and me.subject == "key:k_abc" and me.user is None
        assert me.scopes == IDENTITY["scopes"]

    @pytest.mark.asyncio
    async def test_async_who_am_i(self, make_async_client):
        client, rec = make_async_client(ok(IDENTITY))
        me = await client.account.who_am_i()
        assert rec.last.url.path == "/me" and me.key_id == "k_abc"


class TestJsonEndpoints:
    def test_create_extractor_sends_camel_case_json_body(self, make_client):
        client, rec = make_client(lambda r: httpx.Response(201, json=EXTRACTOR))

        extractor = client.extractors.create(
            name="Invoices",
            config={"json_schema": {"type": "object"}, "citations_enabled": True},
        )

        assert rec.last.headers["content-type"] == "application/json"
        assert rec.last_json() == {
            "name": "Invoices",
            "config": {"jsonSchema": {"type": "object"}, "citationsEnabled": True},
        }
        assert isinstance(extractor, Extractor) and extractor.version == 1
        assert extractor.organization_id == "org_123", "the server still reports the key's organisation"

    def test_retrieve_extractor_sends_only_the_id(self, make_client):
        client, rec = make_client(ok(EXTRACTOR))
        client.extractors.retrieve("ext_1")
        assert rec.last.url.path == "/extractors/ext_1"
        assert not rec.last.url.params

    def test_delete_extractor_permanent_flag(self, make_client):
        client, rec = make_client(ok({"object": "extractor", "id": "ext_1", "deleted": True}))
        client.extractors.delete("ext_1", permanent=True)
        assert rec.last.method == "DELETE"
        assert dict(rec.last.url.params) == {"permanent": "true"}


class TestTheKeyIsTheTenant:
    """No request names an organisation: not in the body, not in the query, not in the path."""

    def test_no_operation_names_an_organization(self, make_client):
        client, rec = make_client(ok(EXTRACTOR))
        client.extractors.create(name="n", config={"json_schema": {"type": "object"}})
        client.extractors.update("ext_1", name="renamed", version=1)
        client.extractors.retrieve("ext_1")
        client.extractors.versions.retrieve(1, extractor_id="ext_1")

        client, rec2 = make_client(ok({"object": "list", "data": [EXTRACTOR]}))
        client.extractors.list(status="all")
        client.extractors.versions.list("ext_1")

        for request in rec.requests + rec2.requests:
            assert "organization" not in str(request.url).lower(), request.url
            assert b"organization" not in request.content, request.content


class TestErrors:
    def test_401_is_authentication_error_with_the_bare_body(self, make_client):
        client, _ = make_client(lambda r: httpx.Response(401, json={"detail": "Unauthorized"}))
        with pytest.raises(AuthenticationError) as excinfo:
            client.account.who_am_i()
        assert excinfo.value.status_code == 401
        assert excinfo.value.body == {"detail": "Unauthorized"}

    def test_403_missing_scope_names_the_scopes_in_the_body(self, make_client):
        detail = {
            "code": "missing_scope",
            "message": "your credential lacks a scope this action needs",
            "missing": ["extractors:write"],
        }
        client, _ = make_client(lambda r: httpx.Response(403, json={"detail": detail}))
        with pytest.raises(PermissionDeniedError) as excinfo:
            client.extractors.create(name="n", config={})
        assert excinfo.value.status_code == 403
        assert excinfo.value.body["detail"]["code"] == "missing_scope"
        assert excinfo.value.body["detail"]["missing"] == ["extractors:write"]

    def test_404_maps_to_not_found_with_body(self, make_client):
        client, _ = make_client(
            lambda r: httpx.Response(404, json={"detail": "Run 'x' not found. It may have expired."})
        )
        with pytest.raises(NotFoundError) as excinfo:
            client.extraction.retrieve_extract_run("x")
        assert excinfo.value.status_code == 404
        assert excinfo.value.body == {"detail": "Run 'x' not found. It may have expired."}

    def test_422_maps_to_unprocessable_entity(self, make_client):
        client, _ = make_client(
            lambda r: httpx.Response(422, json={"detail": [{"loc": ["config"], "msg": "Value error, bad schema"}]})
        )
        with pytest.raises(UnprocessableEntityError):
            client.extraction.create_extract_run(file=b"x", config="{}")


class TestClientConstruction:
    def test_credential_comes_from_arina_grid_api_key_only(self, monkeypatch):
        # The env var is namespaced; an unrelated API_KEY in the environment must never be picked up.
        monkeypatch.setenv("ARINA_GRID_BASE_URL", "https://di.example.test")
        monkeypatch.setenv("API_KEY", "must-not-be-read")
        monkeypatch.delenv("ARINA_GRID_API_KEY", raising=False)
        with pytest.raises(ArinaDocumentIntelligenceAPIError, match="ARINA_GRID_API_KEY"):
            ArinaDocumentIntelligenceAPI()
        monkeypatch.setenv("ARINA_GRID_API_KEY", "from-env")
        assert ArinaDocumentIntelligenceAPI().api_key == "from-env"

    def test_base_url_is_required(self, monkeypatch):
        # No default host: a forgotten base_url must fail before any request (and any key) leaves.
        monkeypatch.delenv("ARINA_GRID_BASE_URL", raising=False)
        with pytest.raises(ArinaDocumentIntelligenceAPIError, match="base_url"):
            ArinaDocumentIntelligenceAPI(api_key="k")
        with pytest.raises(ArinaDocumentIntelligenceAPIError, match="base_url"):
            AsyncArinaDocumentIntelligenceAPI(api_key="k")

    def test_base_url_from_environment(self, monkeypatch):
        monkeypatch.setenv("ARINA_GRID_BASE_URL", "https://di.example.test")
        client = ArinaDocumentIntelligenceAPI(api_key="k")
        assert str(client.base_url).rstrip("/") == "https://di.example.test"

    def test_custom_headers_from_environment(self, monkeypatch, make_client):
        monkeypatch.setenv("ARINA_GRID_CUSTOM_HEADERS", "X-Trace: abc\nX-Team: billing")
        client, rec = make_client(ok(IDENTITY))
        client.account.who_am_i()
        assert rec.last.headers["x-trace"] == "abc" and rec.last.headers["x-team"] == "billing"

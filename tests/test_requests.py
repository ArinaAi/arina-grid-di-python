"""Wire contract: what the SDK sends must be what the API's routes parse.

Key case: `config` is ONE multipart form field holding JSON (the server reads `config: str = Form(...)`).
"""

from __future__ import annotations

import json

import httpx
import pytest

from arina_grid_di import NotFoundError, UnprocessableEntityError
from arina_grid_di.types.extract_run import ExtractRun
from arina_grid_di.types.extractor import Extractor
from arina_grid_di.types.parse_run import ParseRun

from .conftest import API_KEY, run_payload

EXTRACT_CONFIG = {
    "organizationId": "org_123",
    "config": {
        "jsonSchema": {
            "type": "object",
            "properties": {"invoiceTotal": {"type": ["number", "null"]}},
        },
        "citationsEnabled": True,
    },
    "metadata": None,
}

PARSE_CONFIG = {"organizationId": "org_123", "config": {"includeTextLines": True}}


def accepted(kind: str):
    return lambda request: httpx.Response(202, json=run_payload(kind))


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
        client.extraction.create_extract_run(file=b"x", config=json.dumps({"organizationId": "o", "metadata": None}))
        assert json.loads(rec.last_multipart()["config"]["data"])["metadata"] is None

    @pytest.mark.asyncio
    async def test_async_client_sends_the_same_multipart_shape(self, make_async_client):
        client, rec = make_async_client(accepted("extract_run"))
        await client.extraction.create_extract_run(file=b"%PDF", config=json.dumps(EXTRACT_CONFIG))
        parts = rec.last_multipart()
        assert sorted(parts) == ["config", "file"]
        assert json.loads(parts["config"]["data"]) == EXTRACT_CONFIG


class TestHeaders:
    def test_api_key_header_on_every_request(self, make_client):
        client, rec = make_client(lambda r: httpx.Response(200, json=run_payload()))
        client.extraction.retrieve_extract_run("run_1")
        assert rec.last.headers["x-api-key"] == API_KEY

    def test_version_header_only_when_given(self, make_client):
        client, rec = make_client(lambda r: httpx.Response(200, json=run_payload()))
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


class TestJsonEndpoints:
    def test_create_extractor_sends_camel_case_json_body(self, make_client):
        client, rec = make_client(
            lambda r: httpx.Response(
                201,
                json={
                    "object": "extractor",
                    "id": "ext_1",
                    "organizationId": "org_123",
                    "name": "Invoices",
                    "description": None,
                    "version": 1,
                    "status": "ACTIVE",
                    "config": {"citationsEnabled": True, "citationMode": "block"},
                    "metadata": None,
                    "createdAt": "2026-01-01T00:00:00Z",
                    "updatedAt": "2026-01-01T00:00:00Z",
                },
            )
        )

        extractor = client.extractors.create(
            organization_id="org_123",
            name="Invoices",
            config={"json_schema": {"type": "object"}, "citations_enabled": True},
        )

        assert rec.last.headers["content-type"] == "application/json"
        assert rec.last_json() == {
            "organizationId": "org_123",
            "name": "Invoices",
            "config": {"jsonSchema": {"type": "object"}, "citationsEnabled": True},
        }
        assert isinstance(extractor, Extractor) and extractor.version == 1

    def test_retrieve_extractor_puts_organization_in_query(self, make_client):
        client, rec = make_client(
            lambda r: httpx.Response(
                200,
                json={
                    "id": "ext_1",
                    "organizationId": "org_123",
                    "name": "n",
                    "version": 1,
                    "config": {},
                    "createdAt": "t",
                    "updatedAt": "t",
                },
            )
        )
        client.extractors.retrieve(extractor_id="ext_1", organization_id="org_123")
        assert rec.last.url.path == "/extractors/ext_1"
        assert rec.last.url.params["organizationId"] == "org_123"

    def test_delete_extractor_permanent_flag(self, make_client):
        client, rec = make_client(lambda r: httpx.Response(200, json={"id": "ext_1", "deleted": True}))
        client.extractors.delete(extractor_id="ext_1", organization_id="org_123", permanent=True)
        assert rec.last.method == "DELETE"
        assert rec.last.url.params["permanent"] == "true"


class TestErrors:
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

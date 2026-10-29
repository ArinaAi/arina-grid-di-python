"""Shipped docs (sdist/wheel metadata, api.md, the skills) must name THIS distribution and describe key-only auth."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DIST_NAME = re.search(r'^name\s*=\s*"([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.M).group(1)
IMPORT_NAME = DIST_NAME.replace("-", "_")
DOCS = ["api.md", "SKILL.md", "README.md", ".claude/skills/arina-document-intelligence-api-python-sdk/SKILL.md"]


@pytest.mark.parametrize("name", DOCS)
def test_shipped_docs_name_this_package(name):
    text = (ROOT / name).read_text()
    assert f"pip install {DIST_NAME}" in text or f"import {IMPORT_NAME}" in text or f"from {IMPORT_NAME}" in text
    foreign = {m for m in re.findall(r"pip install ([A-Za-z0-9_.-]+)", text)} - {DIST_NAME}
    assert not foreign, f"{name} tells users to install {sorted(foreign)}"
    assert "arina_document_intelligence" not in text and "API_KEY_AUTH" not in text


@pytest.mark.parametrize("name", DOCS)
def test_shipped_docs_describe_the_key_as_the_only_credential(name):
    text = (ROOT / name).read_text()
    assert "ARINA_GRID_API_KEY" in text, f"{name} must point at the namespaced credential variable"
    assert not re.search(r"\bAPI_KEY\b", text.replace("ARINA_GRID_API_KEY", "")), (
        f"{name} names the generator's bare API_KEY"
    )
    assert "ARINA_LOG" not in text and "ARINA_BASE_URL" not in text
    assert "SessionAuth" not in text and "SESSION_AUTH" not in text and "Bearer" not in text


@pytest.mark.parametrize("name", DOCS)
def test_no_request_in_the_docs_names_an_organization(name):
    # Response models still report organizationId; requests never carry it. Catch the request-side spellings.
    text = (ROOT / name).read_text()
    assert "organization_id=" not in text, f"{name} passes organization_id to a method"
    assert '"organizationId":' not in text, f"{name} puts organizationId in a request body"
    assert "organizationId=" not in text, f"{name} puts organizationId in a query string"

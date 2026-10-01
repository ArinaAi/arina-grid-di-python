"""Shipped docs (sdist/wheel metadata and api.md) must name THIS distribution and import package."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DIST_NAME = re.search(r'^name\s*=\s*"([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.M).group(1)
IMPORT_NAME = DIST_NAME.replace("-", "_")


@pytest.mark.parametrize("name", ["api.md", "SKILL.md", "README.md"])
def test_shipped_docs_name_this_package(name):
    text = (ROOT / name).read_text()
    assert f"pip install {DIST_NAME}" in text or f"import {IMPORT_NAME}" in text or f"from {IMPORT_NAME}" in text
    foreign = {m for m in re.findall(r"pip install ([A-Za-z0-9_.-]+)", text)} - {DIST_NAME}
    assert not foreign, f"{name} tells users to install {sorted(foreign)}"
    assert "arina_document_intelligence" not in text and "API_KEY_AUTH" not in text

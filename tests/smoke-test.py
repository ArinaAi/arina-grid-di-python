# File generated from our OpenAPI spec by Scalar. See README.md for details.

# Smoke test: calls every generated operation once to confirm the SDK can reach each endpoint.
# Run it from this repo with `python tests/smoke-test.py`. The generator also runs this file
# against a mock server and reads the JSON report produced via SCALAR_SMOKE_REPORT.
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, TypedDict

from arina_document_intelligence import ArinaDocumentIntelligenceAPI

# The shared smoke-test runner injects base URL and credentials through the same
# environment variables the generated client reads in normal use.
client = ArinaDocumentIntelligenceAPI(max_retries=2, timeout=10)


class SmokeResult(TypedDict, total=False):
    operation: str
    method: str
    path: str
    label: str
    status: str
    durationMs: int
    error: str


class _SmokeCaseBase(TypedDict):
    operation: str
    method: str
    path: str
    run: Callable[[], Any]


# `label` says which of an operation's two calls this is — "required params" or "all params".
# It sits in a total=False extension because it is absent when the operation contributed a
# single case, while the fields above are always present.
class SmokeCase(_SmokeCaseBase, total=False):
    label: str


def _smoke_case_0() -> None:
    extraction = client.extraction.create_extract_run(
        file=b"file",
        config='{"organizationId": "org_123", "config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
    )


def _smoke_case_1() -> None:
    extraction = client.extraction.create_extract_run(
        file=b"file",
        config='{"organizationId": "org_123", "config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
        x_api_version="2026-09-05",
    )


def _smoke_case_2() -> None:
    extraction = client.extraction.retrieve_extract_run(
        run_id="runId",
    )


def _smoke_case_3() -> None:
    extraction = client.extraction.retrieve_extract_run(
        run_id="runId",
        x_api_version="2026-09-05",
    )


def _smoke_case_4() -> None:
    extraction = client.extraction.list_extract_run_page(
        run_id="runId",
    )


def _smoke_case_5() -> None:
    extraction = client.extraction.list_extract_run_page(
        run_id="runId",
        x_api_version="2026-09-05",
    )


def _smoke_case_6() -> None:
    parse = client.parse.create_run(
        file=b"file",
        config='{"organizationId": "org_123", "config": {"includeTextLines": false}}',
    )


def _smoke_case_7() -> None:
    parse = client.parse.create_run(
        file=b"file",
        config='{"organizationId": "org_123", "config": {"includeTextLines": false}}',
        x_api_version="2026-09-05",
    )


def _smoke_case_8() -> None:
    parse = client.parse.retrieve_run(
        run_id="runId",
    )


def _smoke_case_9() -> None:
    parse = client.parse.retrieve_run(
        run_id="runId",
        x_api_version="2026-09-05",
    )


def _smoke_case_10() -> None:
    parse = client.parse.list_run_page(
        run_id="runId",
    )


def _smoke_case_11() -> None:
    parse = client.parse.list_run_page(
        run_id="runId",
        x_api_version="2026-09-05",
    )


def _smoke_case_12() -> None:
    extractor = client.extractors.create(
        organization_id="org_123",
        name="Invoice — EU vendors",
        description=None,
        config={
            "jsonSchema": {"type": "object", "properties": {"invoiceTotal": {"type": ["number", "null"]}}},
            "citationsEnabled": True,
        },
        metadata=None,
    )


def _smoke_case_13() -> None:
    extractor = client.extractors.create(
        organization_id="org_123",
        name="Invoice — EU vendors",
        description=None,
        config={
            "jsonSchema": {"type": "object", "properties": {"invoiceTotal": {"type": ["number", "null"]}}},
            "citationsEnabled": True,
        },
        metadata=None,
        x_api_version="2026-09-05",
    )


def _smoke_case_14() -> None:
    extractor = client.extractors.list(
        organization_id="organization_id",
    )


def _smoke_case_15() -> None:
    extractor = client.extractors.list(
        organization_id="organization_id",
        status="ACTIVE",
        x_api_version="2026-09-05",
    )


def _smoke_case_16() -> None:
    extractor = client.extractors.retrieve(
        extractor_id="extractorId",
        organization_id="organization_id",
    )


def _smoke_case_17() -> None:
    extractor = client.extractors.retrieve(
        extractor_id="extractorId",
        organization_id="organization_id",
        x_api_version="2026-09-05",
    )


def _smoke_case_18() -> None:
    extractor = client.extractors.update(
        extractor_id="extractorId",
        organization_id="x",
        name=None,
        description=None,
        config=None,
        metadata=None,
        version=None,
    )


def _smoke_case_19() -> None:
    extractor = client.extractors.update(
        extractor_id="extractorId",
        organization_id="x",
        name=None,
        description=None,
        config=None,
        metadata=None,
        version=None,
        x_api_version="2026-09-05",
    )


def _smoke_case_20() -> None:
    extractor = client.extractors.delete(
        extractor_id="extractorId",
        organization_id="organization_id",
        permanent=False,
    )


def _smoke_case_21() -> None:
    extractor = client.extractors.delete(
        extractor_id="extractorId",
        organization_id="organization_id",
        permanent=False,
        x_api_version="2026-09-05",
    )


def _smoke_case_22() -> None:
    version = client.extractors.versions.list(
        extractor_id="extractorId",
        organization_id="organization_id",
    )


def _smoke_case_23() -> None:
    version = client.extractors.versions.list(
        extractor_id="extractorId",
        organization_id="organization_id",
        x_api_version="2026-09-05",
    )


def _smoke_case_24() -> None:
    version = client.extractors.versions.retrieve(
        extractor_id="extractorId",
        version=1,
        organization_id="organization_id",
    )


def _smoke_case_25() -> None:
    version = client.extractors.versions.retrieve(
        extractor_id="extractorId",
        version=1,
        organization_id="organization_id",
        x_api_version="2026-09-05",
    )


cases: list[SmokeCase] = [
    {
        "operation": "createExtractRun",
        "method": "POST",
        "path": "/extract_runs",
        "label": "required params",
        "run": _smoke_case_0,
    },
    {
        "operation": "createExtractRun",
        "method": "POST",
        "path": "/extract_runs",
        "label": "all params",
        "run": _smoke_case_1,
    },
    {
        "operation": "retrieveExtractRun",
        "method": "GET",
        "path": "/extract_runs/{run_id}",
        "label": "required params",
        "run": _smoke_case_2,
    },
    {
        "operation": "retrieveExtractRun",
        "method": "GET",
        "path": "/extract_runs/{run_id}",
        "label": "all params",
        "run": _smoke_case_3,
    },
    {
        "operation": "listExtractRunPage",
        "method": "GET",
        "path": "/extract_runs/{run_id}/page",
        "label": "required params",
        "run": _smoke_case_4,
    },
    {
        "operation": "listExtractRunPage",
        "method": "GET",
        "path": "/extract_runs/{run_id}/page",
        "label": "all params",
        "run": _smoke_case_5,
    },
    {
        "operation": "createRun",
        "method": "POST",
        "path": "/parse_runs",
        "label": "required params",
        "run": _smoke_case_6,
    },
    {
        "operation": "createRun",
        "method": "POST",
        "path": "/parse_runs",
        "label": "all params",
        "run": _smoke_case_7,
    },
    {
        "operation": "retrieveRun",
        "method": "GET",
        "path": "/parse_runs/{run_id}",
        "label": "required params",
        "run": _smoke_case_8,
    },
    {
        "operation": "retrieveRun",
        "method": "GET",
        "path": "/parse_runs/{run_id}",
        "label": "all params",
        "run": _smoke_case_9,
    },
    {
        "operation": "listRunPage",
        "method": "GET",
        "path": "/parse_runs/{run_id}/page",
        "label": "required params",
        "run": _smoke_case_10,
    },
    {
        "operation": "listRunPage",
        "method": "GET",
        "path": "/parse_runs/{run_id}/page",
        "label": "all params",
        "run": _smoke_case_11,
    },
    {
        "operation": "create",
        "method": "POST",
        "path": "/extractors",
        "label": "required params",
        "run": _smoke_case_12,
    },
    {
        "operation": "create",
        "method": "POST",
        "path": "/extractors",
        "label": "all params",
        "run": _smoke_case_13,
    },
    {
        "operation": "list",
        "method": "GET",
        "path": "/extractors",
        "label": "required params",
        "run": _smoke_case_14,
    },
    {
        "operation": "list",
        "method": "GET",
        "path": "/extractors",
        "label": "all params",
        "run": _smoke_case_15,
    },
    {
        "operation": "retrieve",
        "method": "GET",
        "path": "/extractors/{extractor_id}",
        "label": "required params",
        "run": _smoke_case_16,
    },
    {
        "operation": "retrieve",
        "method": "GET",
        "path": "/extractors/{extractor_id}",
        "label": "all params",
        "run": _smoke_case_17,
    },
    {
        "operation": "update",
        "method": "PATCH",
        "path": "/extractors/{extractor_id}",
        "label": "required params",
        "run": _smoke_case_18,
    },
    {
        "operation": "update",
        "method": "PATCH",
        "path": "/extractors/{extractor_id}",
        "label": "all params",
        "run": _smoke_case_19,
    },
    {
        "operation": "delete",
        "method": "DELETE",
        "path": "/extractors/{extractor_id}",
        "label": "required params",
        "run": _smoke_case_20,
    },
    {
        "operation": "delete",
        "method": "DELETE",
        "path": "/extractors/{extractor_id}",
        "label": "all params",
        "run": _smoke_case_21,
    },
    {
        "operation": "list",
        "method": "GET",
        "path": "/extractors/{extractor_id}/versions",
        "label": "required params",
        "run": _smoke_case_22,
    },
    {
        "operation": "list",
        "method": "GET",
        "path": "/extractors/{extractor_id}/versions",
        "label": "all params",
        "run": _smoke_case_23,
    },
    {
        "operation": "retrieve",
        "method": "GET",
        "path": "/extractors/{extractor_id}/versions/{version}",
        "label": "required params",
        "run": _smoke_case_24,
    },
    {
        "operation": "retrieve",
        "method": "GET",
        "path": "/extractors/{extractor_id}/versions/{version}",
        "label": "all params",
        "run": _smoke_case_25,
    },
]

DEFAULT_SMOKE_CONCURRENCY = 32


def _selected_cases() -> list[SmokeCase]:
    filter_value = os.environ.get("SCALAR_SMOKE_FILTER")
    needles = [needle.strip() for needle in filter_value.split(",") if needle.strip()] if filter_value else []
    if not needles:
        return cases
    return [case for case in cases if any(needle in case["operation"] or needle in case["path"] for needle in needles)]


def _smoke_concurrency(case_count: int) -> int:
    override = os.environ.get("SCALAR_SMOKE_CONCURRENCY")
    if override:
        try:
            parsed = int(override)
            if parsed > 0:
                return min(parsed, case_count)
        except ValueError:
            pass
    return min(DEFAULT_SMOKE_CONCURRENCY, case_count)


def _case_identity(case: SmokeCase) -> SmokeResult:
    # `label` is carried through only when the operation contributed both of its calls, so a
    # single-case operation reports exactly as it did before there were two.
    identity: SmokeResult = {
        "operation": case["operation"],
        "method": case["method"],
        "path": case["path"],
    }
    label = case.get("label")
    if label:
        identity["label"] = label
    return identity


def _run_case(case: SmokeCase) -> SmokeResult:
    started_at = time.monotonic()
    identity = _case_identity(case)
    try:
        case["run"]()
        return {
            **identity,
            "status": "passed",
            "durationMs": int((time.monotonic() - started_at) * 1000),
        }
    except Exception:
        return {
            **identity,
            "status": "failed",
            "durationMs": int((time.monotonic() - started_at) * 1000),
            "error": traceback.format_exc(),
        }


def main() -> None:
    selected = _selected_cases()
    if selected:
        # Keep enough parallelism to catch generated SDK concurrency bugs without overwhelming
        # CI runners or the in-process mock server for large SDKs.
        with ThreadPoolExecutor(max_workers=_smoke_concurrency(len(selected))) as executor:
            results = list(executor.map(_run_case, selected))
    else:
        results = []
    failed = [result for result in results if result["status"] == "failed"]

    report_path = os.environ.get("SCALAR_SMOKE_REPORT")
    if report_path:
        Path(report_path).write_text(
            json.dumps({"total": len(results), "failed": len(failed), "results": results}), encoding="utf-8"
        )
    else:
        for result in results:
            suffix = f" [{result['label']}]" if result.get("label") else ""
            if result["status"] == "passed":
                print(
                    f"PASS {result['operation']}{suffix} ({result['method']} {result['path']}) {result['durationMs']}ms"
                )
            else:
                print(
                    f"FAIL {result['operation']}{suffix} ({result['method']} {result['path']})\n{result.get('error', '')}",
                    file=sys.stderr,
                )
        if not results:
            print("No code samples ran (empty SDK or a SCALAR_SMOKE_FILTER that matched nothing).", file=sys.stderr)
        else:
            print(f"\n{len(results) - len(failed)}/{len(results)} samples passed")

    if failed or not results:
        sys.exit(1)


if __name__ == "__main__":
    main()

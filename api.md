# Arina Document Intelligence Python API

Complete reference of every operation, grouped by resource. See [the README](./README.md) for usage and configuration.

## Contents

- [`Extraction`](#extraction)
  - [Start an extraction run](#start-an-extraction-run)
  - [Get an extraction run](#get-an-extraction-run)
  - [Get the extraction page image](#get-the-extraction-page-image)
- [`Parse`](#parse)
  - [Start a parse run](#start-a-parse-run)
  - [Get a parse run](#get-a-parse-run)
  - [Get the parse page image](#get-the-parse-page-image)
- [`Extractors`](#extractors)
  - [Create an extractor](#create-an-extractor)
  - [List extractors](#list-extractors)
  - [Get an extractor](#get-an-extractor)
  - [Update an extractor](#update-an-extractor)
  - [Archive or delete an extractor](#archive-or-delete-an-extractor)
  - [`Extractors Versions`](#extractors-versions)
    - [List extractor versions](#list-extractor-versions)
    - [Get an extractor version](#get-an-extractor-version)

## Setup

```python
import os

from arina_document_intelligence import ArinaDocumentIntelligenceAPI

client = ArinaDocumentIntelligenceAPI(
    api_key_auth=os.environ.get("API_KEY_AUTH"),
)
```

## `Extraction`

Submit a document and the fields you want — as a JSON Schema inline, or by the id of a saved extractor — and get each value back with a **spatial citation**: the polygon on the page it was read from, the source text, and a recognition score.

Asynchronous: `POST` returns `202` and a run id; poll `GET /extract_runs/{id}` until `PROCESSED`; then `GET .../page` for the image to draw citations on. A field is *located* (citations present), *found but not located* (`citations: []` — printed more than once, or handwritten), or *not on the page* (`null`). Booleans are read from printed Yes/No or a ticked box and are cited only when the answer is printed on the field's own row.

### Start an extraction run

Accept a document and return a run to poll. `config.config` is either an inline `jsonSchema`/`extractionRules`, or an `extractorId` (optionally with `extractorVersion`) naming a saved extractor. `202`: accepted, not complete — poll `GET /extract_runs/{id}`.

| Direction | Type |
| --- | --- |
| Request | [`ExtractionCreateExtractRunParams`](./src/arina_document_intelligence/types/extraction_create_extract_run_params.py) |
| Response | [`ExtractRun`](./src/arina_document_intelligence/types/extract_run.py) |

```python
extraction = client.extraction.create_extract_run(
    file=b"file",
    config='{"organizationId": "org_123", "config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
)
```

### Get an extraction run

Report a run's status, and its output with citations once finished.

| Direction | Type |
| --- | --- |
| Response | [`ExtractRun`](./src/arina_document_intelligence/types/extract_run.py) |

```python
extraction = client.extraction.retrieve_extract_run(
    run_id="runId",
)
```

### Get the extraction page image

Serve the page image a run's citation polygons were measured against.

```python
extraction = client.extraction.list_extract_run_page(
    run_id="runId",
)
```

## `Parse`

Read page 1 into its structure with **no schema**: every layout block in reading order (type, text, polygon, detection score), each table as HTML (merged cells preserved), and the whole page as markdown. Optionally every text line with its polygon (`includeTextLines`).

Same run lifecycle as extraction. Running headers, footers and page numbers stay in the markdown as HTML comments (`<!-- PageHeader="…" -->`) so nothing is lost but rendered text reads cleanly. Block `type` is an open string (`title`, `sectionHeading`, `text`, `table`, `figure`, `figureCaption`, `formula`, `footnote`, `header`, `footer`, `pageNumber`); treat unknown values as `text`. Block polygons are axis-aligned; text-line polygons may be skewed — draw them as polygons.

### Start a parse run

Read page 1 into layout blocks, tables (HTML) and markdown — no schema. `202`: poll `GET /parse_runs/{id}`.

| Direction | Type |
| --- | --- |
| Request | [`ParseCreateRunParams`](./src/arina_document_intelligence/types/parse_create_run_params.py) |
| Response | [`ParseRun`](./src/arina_document_intelligence/types/parse_run.py) |

```python
parse = client.parse.create_run(
    file=b"file",
    config='{"organizationId": "org_123", "config": {"includeTextLines": false}}',
)
```

### Get a parse run

Report a run's status, and its parsed output once finished.

| Direction | Type |
| --- | --- |
| Response | [`ParseRun`](./src/arina_document_intelligence/types/parse_run.py) |

```python
parse = client.parse.retrieve_run(
    run_id="runId",
)
```

### Get the parse page image

Serve the page image the output polygons were measured against.

```python
parse = client.parse.list_run_page(
    run_id="runId",
)
```

## `Extractors`

A saved, **versioned** extraction configuration for a tenant: the schema, rules and citation settings a run would otherwise carry inline. Save it once, then start runs with `config.extractorId`.

Editing replaces `config` whole and bumps `version`; renaming does not. Pass the `version` you loaded to get `409` on a stale edit. A run records the extractor id and the exact version it used and keeps its own copy of the config, so later edits never change an existing run. `DELETE` archives by default — the record and every version stay, new runs are refused unless a version is pinned; `?permanent=true` removes the record and all versions (runs already made are unaffected). Extractors do not expire.

### Create an extractor

Save a named, versioned extraction configuration. The schema is validated here, so a mistake is a 422 at save time.

| Direction | Type |
| --- | --- |
| Request | [`ExtractorCreateParams`](./src/arina_document_intelligence/types/extractor_create_params.py) |
| Response | [`Extractor`](./src/arina_document_intelligence/types/extractor.py) |

```python
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
```

### List extractors

A tenant's extractors, `ACTIVE` by default. `status=ARCHIVED|all` to widen.

| Direction | Type |
| --- | --- |
| Request | [`ExtractorListParams`](./src/arina_document_intelligence/types/extractor_list_params.py) |
| Response | [`ExtractorList`](./src/arina_document_intelligence/types/extractor_list.py) |

```python
extractor = client.extractors.list(
    organization_id="organization_id",
)
```

### Get an extractor

The current version of one extractor.

| Direction | Type |
| --- | --- |
| Request | [`ExtractorRetrieveParams`](./src/arina_document_intelligence/types/extractor_retrieve_params.py) |
| Response | [`Extractor`](./src/arina_document_intelligence/types/extractor.py) |

```python
extractor = client.extractors.retrieve(
    extractor_id="extractorId",
    organization_id="organization_id",
)
```

### Update an extractor

Rename, describe or reconfigure. Only a `config` change bumps the version. Send `version` to get a 409 on a stale edit.

| Direction | Type |
| --- | --- |
| Request | [`ExtractorUpdateParams`](./src/arina_document_intelligence/types/extractor_update_params.py) |
| Response | [`Extractor`](./src/arina_document_intelligence/types/extractor.py) |

```python
extractor = client.extractors.update(
    extractor_id="extractorId",
    organization_id="x",
    name=None,
    description=None,
    config=None,
    metadata=None,
    version=None,
)
```

### Archive or delete an extractor

Archive by default (record and versions kept, new runs refused). `permanent=true` removes the record and every version; runs already made keep their frozen config.

| Direction | Type |
| --- | --- |
| Request | [`ExtractorDeleteParams`](./src/arina_document_intelligence/types/extractor_delete_params.py) |
| Response | [`ExtractorDeleteResponse`](./src/arina_document_intelligence/types/extractor_delete_response.py) |

```python
extractor = client.extractors.delete(
    extractor_id="extractorId",
    organization_id="organization_id",
    permanent=False,
)
```

### `Extractors Versions`

A saved, **versioned** extraction configuration for a tenant: the schema, rules and citation settings a run would otherwise carry inline. Save it once, then start runs with `config.extractorId`.

Editing replaces `config` whole and bumps `version`; renaming does not. Pass the `version` you loaded to get `409` on a stale edit. A run records the extractor id and the exact version it used and keeps its own copy of the config, so later edits never change an existing run. `DELETE` archives by default — the record and every version stay, new runs are refused unless a version is pinned; `?permanent=true` removes the record and all versions (runs already made are unaffected). Extractors do not expire.

#### List extractor versions

Every immutable config snapshot, newest first.

| Direction | Type |
| --- | --- |
| Request | [`VersionListParams`](./src/arina_document_intelligence/types/extractors/version_list_params.py) |
| Response | [`ExtractorVersionList`](./src/arina_document_intelligence/types/extractors/extractor_version_list.py) |

```python
version = client.extractors.versions.list(
    extractor_id="extractorId",
    organization_id="organization_id",
)
```

#### Get an extractor version

One config snapshot by number.

| Direction | Type |
| --- | --- |
| Request | [`VersionRetrieveParams`](./src/arina_document_intelligence/types/extractors/version_retrieve_params.py) |
| Response | [`ExtractorVersion`](./src/arina_document_intelligence/types/extractors/extractor_version.py) |

```python
version = client.extractors.versions.retrieve(
    extractor_id="extractorId",
    version=1,
    organization_id="organization_id",
)
```

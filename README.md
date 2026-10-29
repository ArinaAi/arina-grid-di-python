# Arina Document Intelligence API

This library provides convenient access to the Arina Document Intelligence API from Python.

The full API of this library can be found in [api.md](./api.md).

<br />

## Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [Usage](#usage)
- [Waiting for a run](#waiting-for-a-run)
- [API Reference](./api.md)
- [Async](#async)
- [Errors](#errors)
- [Client Options](#client-options)
- [Retries and Timeouts](#retries-and-timeouts)
- [Helpers](#helpers)
- [Logging](#logging)
- [Requirements](#requirements)

<br />

## Installation

```sh
pip install arina-grid-di
```

<br />

## Authentication

Every request carries one credential: an API key, sent as the `X-API-Key` header. **The key
is the tenant.** It names your organisation and what it may do, so no request names an
organisation: there is no `organizationId` to pass anywhere.

### Get your key

Sign in to the GRID portal, open **API keys** and create one. The secret is shown once; keep
it in a secret manager or the `ARINA_GRID_API_KEY` environment variable, never in source
control. Keys look like `grid_<12 hex>_<64 hex>`.

A key carries **scopes**, one per group of operations:

| Scope | Allows |
| --- | --- |
| `extract` | `client.extraction.*` |
| `parse` | `client.parse.*` |
| `extractors:read` | `client.extractors.list` / `retrieve` and `client.extractors.versions.*` |
| `extractors:write` | `client.extractors.create` / `update` / `delete` |

`client.account.who_am_i()` needs no scope.

### Check your key

```python
from arina_grid_di import ArinaDocumentIntelligenceAPI

client = ArinaDocumentIntelligenceAPI(api_key="<your key>", base_url="https://<your base url>")

me = client.account.who_am_i()
print(me.organization.slug, me.key_id, me.scopes)
```

A missing, revoked or expired key raises `AuthenticationError` (401). A key without a scope
the operation needs raises `PermissionDeniedError` (403) whose body names the missing scopes;
see [Errors](#errors).

The client reads `ARINA_GRID_API_KEY` and `ARINA_GRID_BASE_URL` when the options are not
passed. This version targets deployments that enforce API keys: Arina's hosted service, and
your organisation's own deployment once it has been switched over.

<br />

## Usage

You need the base URL of the service you are using (Arina-hosted, or your organisation's
own deployment) and an API key for it. Both are required: the client has no default host.

```python
import json

from arina_grid_di import ArinaDocumentIntelligenceAPI

client = ArinaDocumentIntelligenceAPI(
    api_key="<your key>",
    base_url="https://<your base url>",
)

# Runs are asynchronous: POST returns 202 with a run id, then you poll.
# `config` is the ExtractRunRequest object as a JSON string (one multipart form field).
run = client.extraction.create_extract_run(
    file=open("invoice.pdf", "rb"),
    config=json.dumps({
        "config": {
            "jsonSchema": {
                "type": "object",
                "properties": {
                    "invoiceNumber": {"type": ["string", "null"]},
                    "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"},
                },
            },
            "citationsEnabled": True,
        },
    }),
)
print(run.id, run.status)  # exr_..., PENDING or PROCESSING
```

The examples in the following sections assume a `client` configured as shown above.

See the [API reference](./api.md) for every available operation.

<br />

## Waiting for a run

`arina_grid_di.lib` adds helpers that poll a run until it reaches a
terminal status (`PROCESSED`, `FAILED`, `CANCELLED`), with backoff and a timeout:

```python
from arina_grid_di.lib import wait_for_extract_run

run = wait_for_extract_run(client, run.id, timeout=120)

total = run.output.value["invoiceTotal"]

# `citations` is a list when the value was located, [] when it was found but not
# located, and None when citations were disabled — so guard before iterating.
field = run.output.metadata["invoiceTotal"]
for citation in field.citations or []:
    print(citation.page.number, citation.polygon, citation.reference_text)

# The page image the polygons were measured against:
with open("page.jpg", "wb") as fh:
    fh.write(client.extraction.list_extract_run_page(run.id).read())
```

`wait_for_parse_run` does the same for parse runs, and both have `async` counterparts
(`await wait_for_extract_run_async(...)`). A `FAILED` or `CANCELLED` run raises
`RunFailedError` (the run is on `.run`); pass `raise_on_failure=False` to get it back
instead. Exceeding `timeout` raises `RunTimeoutError`. Unknown statuses are treated as
still running, because status is an open string.

<br />

## Async

Every client has an `Async` counterpart (`AsyncArinaDocumentIntelligenceAPI`) exposing the same resource tree with `await`.

```python
import asyncio

from arina_grid_di import AsyncArinaDocumentIntelligenceAPI


async def main() -> None:
    client = AsyncArinaDocumentIntelligenceAPI()  # ARINA_GRID_API_KEY and ARINA_GRID_BASE_URL from the environment
    extraction = await client.extraction.create_extract_run(
        file=b"file",
        config='{"config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
    )


asyncio.run(main())
```

<br />

## Errors

Non-success responses raise generated API errors, all subclasses of `APIStatusError`. Each
carries `status_code`, `message`, the parsed JSON `body` and the raw `response`.

```python
from arina_grid_di import APIStatusError, AuthenticationError, PermissionDeniedError

try:
    extractor = client.extractors.create(name="Invoices", config={"jsonSchema": {"type": "object"}})
except AuthenticationError:
    # 401: the key is missing, unknown, revoked or expired. The body is a bare {"detail": "Unauthorized"}.
    raise
except PermissionDeniedError as err:
    # 403: the key lacks a scope this operation needs.
    detail = err.body["detail"]  # {"code": "missing_scope", "message": "...", "missing": ["extractors:write"]}
    print(detail["code"], detail.get("missing"))
    raise
except APIStatusError as err:
    print(err.status_code, err.message)
    raise
```

`body["detail"]` is a string for most refusals, a list of `{loc, msg}` objects for a
request-validation failure (422), and an object `{code, message, ...}` where you are meant
to branch on `code`. A resource that belongs to another organisation is a plain `404`.

Documented error statuses: `400`, `401`, `403`, `404`, `409`, `422`, `503`. A `503` (key check
or run storage unavailable) carries `Retry-After` and is retried automatically; see below.

<br />

## Client Options

Configure the generated client by setting any of these options when you create it.

```python
from arina_grid_di import ArinaDocumentIntelligenceAPI

client = ArinaDocumentIntelligenceAPI(
    timeout=60.0,
    max_retries=2,
)
```

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `api_key` | `str \| None` | `os.environ.get("ARINA_GRID_API_KEY")` | Credential for the ApiKey scheme, sent as `X-API-Key`. |
| `base_url` | `str \| httpx.URL \| None` | `os.environ.get("ARINA_GRID_BASE_URL")` | Where the service is. Required: there is no default host. |
| `timeout` | `float \| Timeout \| None` | `60.0` | Maximum time in seconds to wait for a response before aborting a request. |
| `max_retries` | `int` | `2` | Number of retries for temporary failures. |
| `default_headers` | `Mapping[str, str] \| None` | - | Headers sent with every request. |
| `default_query` | `Mapping[str, object] \| None` | - | Query parameters sent with every request. |

`ARINA_GRID_CUSTOM_HEADERS` (newline-separated `Name: value` lines) adds headers to every
request, like `default_headers`; an explicit `default_headers` wins on a clash.

<br />

## Retries and Timeouts

Generated clients support request timeouts and retry temporary failures such as network errors, 408, 409, 429, and 5xx responses. Retry delays honor `Retry-After` headers when present. Tune the retry and timeout client options shown above, or override them per request.

<br />

## Helpers

- Use `client.with_raw_response.<resource>.<method>(...)` to access the raw `httpx.Response` and parse it yourself.
- Use `client.with_streaming_response.<resource>.<method>(...)` to stream a response body without buffering it.

<br />

## Logging

- Set the `ARINA_GRID_LOG` environment variable to `info` or `debug` to enable HTTP logging.
- Logs are emitted through the standard `logging` module under the `arina_grid_di` logger.

<br />

## Requirements

- Python 3.9 or newer

<br />

## Contributing

Client code under `src/arina_grid_di/` (except `lib/`) is generated from the
API's OpenAPI document; helpers, tests and release automation are maintained here. See
[CONTRIBUTING.md](./CONTRIBUTING.md). Security reports: [SECURITY.md](./SECURITY.md).

Client generated with Scalar.

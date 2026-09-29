# Arina Document Intelligence API

This library provides convenient access to the Arina Document Intelligence API from Python.

The full API of this library can be found in [api.md](./api.md).

<br />

## Contents

- [Installation](#installation)
- [Usage](#usage)
- [Waiting for a run](#waiting-for-a-run)
- [API Reference](./api.md)
- [Async](#async)
- [Authentication](#authentication)
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

## Usage

You need the base URL of the service you are using (Arina-hosted, or your organisation's
own deployment) and the API key that goes with it.

```python
import json

from arina_grid_di import ArinaDocumentIntelligenceAPI

client = ArinaDocumentIntelligenceAPI(
    api_key_auth="<your key>",
    base_url="https://<your base url>",
)

# Runs are asynchronous: POST returns 202 with a run id, then you poll.
# `config` is the ExtractRunRequest object as a JSON string (one multipart form field).
run = client.extraction.create_extract_run(
    file=open("invoice.pdf", "rb"),
    config=json.dumps({
        "organizationId": "org_123",
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
print(run.id, run.status)  # exr_..., PROCESSING
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
    client = AsyncArinaDocumentIntelligenceAPI()
    extraction = await client.extraction.create_extract_run(
        file=b"file",
        config='{"organizationId": "org_123", "config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
    )


asyncio.run(main())
```

<br />

## Authentication

Pass credentials to the generated client constructor. Environment variables are read automatically when supported by the target runtime.

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `api_key_auth` | `string \| provider` | - | Credential for the ApiKeyAuth scheme. Defaults to API_KEY_AUTH. |

Declared schemes:

- `ApiKeyAuth` API key in header `X-API-Key`

<br />

## Errors

Non-success responses throw generated API errors. Error objects expose status, headers, response body, and request metadata where the target runtime supports it.

```python
from arina_grid_di import APIStatusError

try:
    extraction = client.extraction.create_extract_run(
        file=b"file",
        config='{"organizationId": "org_123", "config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
    )
except APIStatusError as err:
    print(err.status_code, err.message)
    raise
```

Documented error statuses: `400`, `404`, `409`, `422`, `503`.

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
| `api_key_auth` | `str \| None` | `os.environ.get("API_KEY_AUTH")` | Credential for the ApiKeyAuth scheme. |
| `base_url` | `str \| httpx.URL \| None` | - | Override the default API base URL. |
| `timeout` | `float \| Timeout \| None` | `60.0` | Maximum time in seconds to wait for a response before aborting a request. |
| `max_retries` | `int` | `2` | Number of retries for temporary failures. |
| `default_headers` | `Mapping[str, str] \| None` | - | Headers sent with every request. |
| `default_query` | `Mapping[str, object] \| None` | - | Query parameters sent with every request. |

<br />

## Retries and Timeouts

Generated clients support request timeouts and retry temporary failures such as network errors, 408, 409, 429, and 5xx responses. Retry delays honor `Retry-After` headers when present. Tune the retry and timeout client options shown above, or override them per request.

<br />

## Helpers

- Use `client.with_raw_response.<resource>.<method>(...)` to access the raw `httpx.Response` and parse it yourself.
- Use `client.with_streaming_response.<resource>.<method>(...)` to stream a response body without buffering it.

<br />

## Logging

- Set the `ARINA_LOG` environment variable to `info` or `debug` to enable HTTP logging.
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

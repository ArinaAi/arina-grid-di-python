---
name: arina-document-intelligence-api-python-sdk
description: "Python SDK for Arina Document Intelligence API. Use when writing Python code that calls Arina Document Intelligence API with the arina-document-intelligence package: installing it, constructing and authenticating the client, and calling API operations."
---

# Arina Document Intelligence API Python SDK

Generated Python client for Arina Document Intelligence API, published as `arina-document-intelligence`. Use the generated client instead of hand-writing HTTP requests.

## Install

```sh
pip install arina-document-intelligence
```

## Client setup and authentication

```python
import os

from arina_document_intelligence import ArinaDocumentIntelligenceAPI

client = ArinaDocumentIntelligenceAPI(
    api_key_auth=os.environ.get("API_KEY_AUTH"),
)
```

Provide credentials using the options below. Environment variables are read automatically when the target runtime supports them:

- `api_key_auth` (env: `API_KEY_AUTH`) — Credential for the ApiKeyAuth scheme.

## Calling operations

```python
import os

from arina_document_intelligence import ArinaDocumentIntelligenceAPI

client = ArinaDocumentIntelligenceAPI(
    api_key_auth=os.environ.get("API_KEY_AUTH"),
)

extraction = client.extraction.create_extract_run(
    file=b"file",
    config='{"organizationId": "org_123", "config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
)

print(extraction)
```

Method names, parameter shapes, and response types are generated from the API description — do not guess them. Look up the exact call signature in [api.md](./api.md) before writing a call.

## Error handling

Non-success responses throw generated API errors. Error objects expose status, headers, response body, and request metadata where the target runtime supports it.

```python
from arina_document_intelligence import APIStatusError

try:
    extraction = client.extraction.create_extract_run(
        file=b"file",
        config='{"organizationId": "org_123", "config": {"jsonSchema": {"type": "object", "properties": {"invoiceNumber": {"type": ["string", "null"]}, "invoiceTotal": {"type": ["number", "null"], "description": "Total amount due"}}}, "citationsEnabled": true}}',
    )
except APIStatusError as err:
    print(err.status_code, err.message)
    raise
```

## Requirements

- Python 3.8 or newer

## Reference files

- [README.md](./README.md) — full feature tour: client options, retries and timeouts, logging.
- [api.md](./api.md) — complete catalogue of every operation with request and response types.

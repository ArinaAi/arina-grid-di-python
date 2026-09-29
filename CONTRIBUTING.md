# Contributing

Python SDK for the Arina Document Intelligence API. The client is generated from the API's
public OpenAPI document; helpers, tests and automation are maintained here. Releases are cut
by the `Release` workflow from Conventional Commits; repository and index setup is documented
internally.

## File ownership

| Owner | Paths | Rule |
| --- | --- | --- |
| **Generator (Scalar)** | `src/arina_grid_di/**` except `lib/`; `api.md`; `SKILL.md`; `.claude/`; `scalar-sdk.manifest.json`; `tests/smoke-test.py`; `.gitignore` | Never edit. Replaced by `scripts/import_sdk.py`. Fix upstream: the OpenAPI document (API repo, `openapi/generate.py`) or the generator config. |
| **This repo** | `src/arina_grid_di/lib/`; `tests/` (except `smoke-test.py`); `scripts/import_sdk.py`; `.github/` (workflows, `release-config.json`, `release-manifest.json`); `CHANGELOG.md`; `CONTRIBUTING.md`; `SECURITY.md` | Normal code review. New helpers go in new modules under `lib/`. |
| **Generated once, then this repo** | `pyproject.toml`; `README.md`; `LICENSE`; `SECURITY.md` | Import never overwrites them; it prints a diff when the generated version changed (usually a new runtime dependency) so the change can be ported by hand. |

Generated and hand-written code never share a file, so regeneration is a plain copy with no merge.

## Regenerating after an API change

1. API repo: change the model or route, run `python openapi/spec.py build`, commit `openapi/openapi.public.json`.
2. Generator: upload that document, download the Python zip.
3. Here, on a branch:

   ```sh
   python scripts/import_sdk.py ~/Downloads/<sdk>.zip
   git status          # generated paths changed; lib/ and tests/ untouched
   pytest              # wire-contract tests are the safety net
   ```

4. Commit with the prefix that matches the API change (below), open a PR, merge when CI is green.

The import restores the current version into `_version.py` (the zip always says `0.1.0`), rejects zips that
are not this SDK, and replaces the generator's placeholder default host (`https://example.com`, emitted when
no environment is configured) with a "base_url is required" error so a key can never be sent to a host we
do not own. Once a production environment is configured in the generator, that step is a no-op.

## Commit messages

Conventional Commits on `main` drive versioning and the changelog (release-please). With *Squash and merge*, the PR title is the commit.

| Prefix | Release | Version (0.x) |
| --- | --- | --- |
| `fix:` | yes | patch |
| `feat:` | yes | minor |
| `feat!:` / `BREAKING CHANGE:` | yes | minor while 0.x, major from 1.0 |
| `docs:` `chore:` `ci:` `test:` `refactor:` | no | — |

## Local development

```sh
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
ruff check && ruff format --check
pytest
python -m build && twine check --strict dist/*
```

Tests are offline: `tests/conftest.py` binds the client to an `httpx.MockTransport` and asserts on the
bytes sent — for example that `config` is one multipart form field holding JSON, which is what the API's
routes parse. `tests/smoke-test.py` is the generator's live reachability check; run it by hand.

## Known follow-ups

- Regenerate with the generator config set to `readEnv: ARINA_GRID_API_KEY` and `defaultEnvPrefix: ARINA_GRID`; the current client reads `API_KEY_AUTH` / `ARINA_BASE_URL` and defaults to a development host.
- Confirm the copyright holder in `LICENSE` is the legal entity name.

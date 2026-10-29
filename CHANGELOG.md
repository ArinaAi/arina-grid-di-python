# Changelog

## [0.2.0](https://github.com/ArinaAi/arina-grid-di-python/compare/v0.1.1...v0.2.0) (2026-10-29)


### ⚠ BREAKING CHANGES

* remove `organizationId` from run `config` JSON and the `organization_id=` keyword from `client.extractors.*` calls; the API key identifies the organisation. Requires a deployment that enforces API keys.

### Features

* the API key is the tenant — remove organizationId from requests, add whoAmI ([#10](https://github.com/ArinaAi/arina-grid-di-python/issues/10)) ([655ade4](https://github.com/ArinaAi/arina-grid-di-python/commit/655ade44c19ebbfd52f2901611107cdc6780170e))

## [0.1.1](https://github.com/ArinaAi/arina-grid-di-python/compare/v0.1.0...v0.1.1) (2026-10-01)


### Bug Fixes

* credential option is api_key; environment variables are ARINA_GRID_* ([#8](https://github.com/ArinaAi/arina-grid-di-python/issues/8)) ([e8a0145](https://github.com/ArinaAi/arina-grid-di-python/commit/e8a0145b9070c3321d1c7a2cdc4b91bb2c896808))

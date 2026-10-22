# Contributing to Adaptify Docs

## Docs cycles

- Cycles run only when Ash asks.
- One area per cycle, with at most 5-8 pages and 3-5 `docs` issues.
- One branch (`docs/<area>-<version>`) and one pull request per cycle.
- Push with git (clone, edit locally, push), not per-file API calls.
- Never merge. Ash reviews and merges.

## Content

- Markdown only.
- Every page has `audience:`, `goals:` and `video: ""` in its front matter.
- `audience` is `internal` or `external` (any capitalization). It does not default. A missing value fails the build.
- Mark any step that has not been checked in the product with `TODO verify`.
- Work and capture screenshots in **Test Tenant** only. Never use a production or Adaptify organization tenant.
- Plain, positive, task-based language. Use full component names on first mention (Product Vault), then the short form (Vault). Bold exact UI labels.

## Screenshots

- Crop to the relevant area and save as WebP, under about 200 KB each.
- Store under `docs/assets/<area>/`. No Git LFS.

## Build and publish

- Pull requests are checked by GitHub Actions: `scripts/check_redirects.py`, then `mkdocs build --strict` for `DOCS_AUDIENCE=internal` and `DOCS_AUDIENCE=external`.
- A merge to `main` publishes the internal site. Do not run `mkdocs gh-deploy`.

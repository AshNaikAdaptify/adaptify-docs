# Contributing to Adaptify Docs

## Docs cycles

- Cycles run only when Ash asks.
- One area per cycle, with at most 5-8 pages and 3-5 `docs` issues.
- One branch (`docs/<area>-<version>`) and one pull request per cycle.
- Push with git (clone, edit locally, push), not per-file API calls.
- Never merge. Ash reviews and merges.

## Content

- Markdown only.
- Every page has `goals:` and `video: ""` in its front matter.
- Mark any step that has not been checked in the product with `TODO verify`.
- Work and capture screenshots in **Test Tenant** only. Never use a production or Adaptify organization tenant.
- Plain, positive, task-based language. Use full component names on first mention (Product Vault), then the short form (Vault). Bold exact UI labels.

## Screenshots

- Crop to the relevant area and save as WebP, under about 200 KB each.
- Store under `docs/assets/<area>/`. No Git LFS.

## Build and publish

- No GitHub Actions in v1.
- Check with `mkdocs build --strict` before opening a PR.
- Publish by building `main` locally and pushing to the `gh-pages` branch (for example `mkdocs gh-deploy --force`, run from an up-to-date `main`).

# Adaptify Docs

End-user documentation for Adaptify, the platform that helps insurance carriers get their products built, filed, approved and operational. Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

Published site: https://ashnaikadaptify.github.io/adaptify-docs/

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
DOCS_AUDIENCE=internal .venv/bin/mkdocs serve    # http://127.0.0.1:8000
DOCS_AUDIENCE=internal .venv/bin/mkdocs build --strict
DOCS_AUDIENCE=external .venv/bin/mkdocs build --strict --site-dir site-external
```

`DOCS_AUDIENCE` is required. It is `internal` or `external`, and it does not default.

## Layout

- `docs/` Markdown pages, one folder per area (Get Started, Product Vault, Workbench, Sandbox, Filing Manager, Rating Catalog, Reference)
- `overrides/` theme overrides: the "What this page helps you do" goals box, video block and page feedback
- `docs/stylesheets/extra.css` Adaptify styling

## Page front matter

```yaml
---
title: Page title
audience: external   # or internal; required, any capitalization, no default
goals:
  - What the reader can do after reading
video: ""   # YouTube or Vimeo URL; empty shows a "coming soon" placeholder
---
```

Every page needs `audience`. A page without it fails the build. `internal` publishes the staff site (every page). `external` is the customer site: internal pages are left out of the HTML, the search index and the sitemap, and so are `docs/assets/internal/` and assets that only internal pages use.

## Publish

Pull requests build both sites in strict mode. A merge to `main` publishes the **internal** site to GitHub Pages. The repo is public, so that site is publicly readable. Internal docs move to AWS when budget allows.

Do not run `mkdocs gh-deploy`. It force-pushes `gh-pages` and deletes the `pr-preview/` directories that pull request previews use.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how docs cycles work.

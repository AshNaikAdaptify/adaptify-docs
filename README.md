# Adaptify Docs

End-user documentation for Adaptify, the platform that helps insurance carriers get their products built, filed, approved and operational. Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

Published site: https://ashnaikadaptify.github.io/adaptify-docs/

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve          # http://127.0.0.1:8000
.venv/bin/mkdocs build --strict # check before opening a PR
```

## Layout

- `docs/` Markdown pages, one folder per area (Get Started, Product Vault, Workbench, Sandbox, Filing Manager, Rating Catalog, Reference)
- `overrides/` theme overrides: the "What this page helps you do" goals box, video block and page feedback
- `docs/stylesheets/extra.css` Adaptify styling

## Page front matter

```yaml
---
title: Page title
goals:
  - What the reader can do after reading
video: ""   # YouTube, Vimeo, or local .mp4/.webm URL; empty or omitted renders no player
---
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how docs cycles work.

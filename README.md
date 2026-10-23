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
video: ""   # YouTube, Vimeo, or local .mp4/.webm URL; empty or omitted renders no player
---
```

Every page needs `audience`. A page without it fails the build. `internal` publishes the staff site (every page). `external` is the customer site: internal pages are left out of the HTML, the search index and the sitemap, and so are `docs/assets/internal/` and assets that only internal pages use.

Internal builds show an **Edit this page** pencil that opens the page on GitHub (`edit/main/docs/`). That link is internal-only by design. External builds, including release candidates, clear `repo_url`, `repo_name`, and `edit_uri`, so the pencil and the header link to the public repository are both absent.

External pages show thumbs for **This page was helpful** and **This page was not helpful**. A click sends `{path, release, vote}` to `/_feedback` on the same origin, with no personal data. `release` is the number in a live `/_rc/<n>/` path, or `""` when that prefix is absent. A failed request, including before that endpoint is deployed, leaves the buttons in place and shows no error. `extra.support_email` is empty by default; set it to add a **Report a problem** mailto whose subject is the page path. Internal pages keep the GitHub issue feedback.

## Publish

Pull requests build both sites in strict mode. A merge to `main` publishes the **internal** site to GitHub Pages. The repo is public, so that site is publicly readable. Internal docs move to AWS when budget allows.

Do not run `mkdocs gh-deploy`. It force-pushes `gh-pages` and deletes the `pr-preview/` directories that pull request previews use.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how docs cycles work.

## Redirects

Add a redirect in the same PR that removes or moves a page. Put it in `redirect_maps` in `mkdocs.yml`, from the old `docs/` path to the new page. Do not add it while the old file still exists. Assets are not redirected.

`scripts/check_redirects.py` fails if any redirect source still exists under `docs/`, or any target page does not.

The redirects plugin records pages during `on_files`, which runs before the audience hook drops internal pages. A target excluded from the external build does not fail that build. The plugin still writes the redirect HTML, and that HTML points at a page the external site does not publish. The internal build includes the redirect and the page. The same note is under `plugins:` in `mkdocs.yml`.

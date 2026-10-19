#!/usr/bin/env python3
"""Check a built site against the audience front matter.

The external site must not contain an internal page (HTML, search index,
sitemap, title or path) or an internal-only asset. The internal site must
contain every page. This reads the built files; it does not trust the hook
to have filtered them.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
from xml.etree import ElementTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from hooks.audience import (  # noqa: E402
    is_internal_tree,
    survey,
    theme_keep,
)

TITLE_RE = re.compile(r"<title>([^<]*)</title>", re.I)
ISSUE_LINK = "issues/new"
TEXT_EXTENSIONS = {".html", ".xml", ".json", ".js", ".css", ".txt", ".svg", ".map"}
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def page_key(src_uri: str) -> str:
    if src_uri == "index.md":
        return ""
    stem = src_uri[: -len(".md")]
    if stem.endswith("/index"):
        return stem[: -len("/index")]
    return stem


def output_candidates(src_uri: str) -> list[str]:
    if src_uri == "index.md":
        return ["index.html"]
    stem = src_uri[: -len(".md")]
    if stem.endswith("/index"):
        parent = stem[: -len("/index")]
        return [f"{parent}/index.html"]
    return [f"{stem}/index.html", f"{stem}.html"]


def norm_location(loc: str) -> str:
    loc = loc.split("#", 1)[0].split("?", 1)[0].strip()
    loc = loc.strip("/")
    if loc.endswith("/index.html"):
        loc = loc[: -len("/index.html")]
    elif loc.endswith(".html"):
        loc = loc[: -len(".html")]
    if loc.endswith("/index"):
        loc = loc[: -len("/index")]
    if loc in {"index", "index.html", "."}:
        return ""
    return loc


def loc_key(loc: str, site_url: str) -> str:
    loc = (loc or "").strip()
    base = site_url.rstrip("/") + "/"
    if loc.startswith(base):
        loc = loc[len(base) :]
    elif site_url and loc.rstrip("/") == site_url.rstrip("/"):
        loc = ""
    return norm_location(loc)


def load_yaml_config(path: str) -> dict:
    import yaml

    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data if isinstance(data, dict) else {}


def iter_text_files(site_dir: str):
    """Generated pages, the sitemap and the search index.

    Theme bundles under assets/javascripts are skipped. They contain unrelated
    strings such as a browserify path ``./support/isBuffer``.
    """
    for dirpath, _dirnames, filenames in os.walk(site_dir):
        for name in filenames:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, site_dir).replace(os.sep, "/")
            if rel.startswith("assets/javascripts/") or rel.startswith("assets/stylesheets/"):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext == ".gz" and name.endswith(".xml.gz"):
                try:
                    with gzip.open(path, "rt", encoding="utf-8") as handle:
                        yield path, handle.read()
                except OSError:
                    continue
                continue
            if ext not in TEXT_EXTENSIONS:
                continue
            try:
                with open(path, encoding="utf-8") as handle:
                    yield path, handle.read()
            except (OSError, UnicodeDecodeError):
                continue


def search_docs(site_dir: str) -> list[dict]:
    path = os.path.join(site_dir, "search", "search_index.json")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    docs = data.get("docs") if isinstance(data, dict) else None
    return docs if isinstance(docs, list) else []


def sitemap_locs(site_dir: str) -> list[str]:
    path = os.path.join(site_dir, "sitemap.xml")
    if not os.path.isfile(path):
        return []
    root = ElementTree.parse(path).getroot()
    locs = [el.text or "" for el in root.findall(".//sm:loc", SITEMAP_NS)]
    if not locs:
        locs = [el.text or "" for el in root.iter() if el.tag.endswith("loc")]
    return locs


def title_matches(tag: str, title: str) -> bool:
    tag = " ".join(tag.split())
    return tag == title or tag.startswith(title + " - ") or tag.startswith(title + " | ")


def grep_tokens(src_uri: str, external_keys: set[str]) -> list[str]:
    if src_uri == "index.md":
        # "index.html" is a suffix of every section index. Presence of the
        # homepage is checked as the file site/index.html, not as a substring.
        return []
    tokens = [src_uri]
    tokens.extend(output_candidates(src_uri))
    key = page_key(src_uri)
    if key:
        prefix = key + "/"
        shadowed = any(other == key or other.startswith(prefix) for other in external_keys)
        if not shadowed:
            tokens.append(prefix)
    return tokens


def check(docs_dir: str, site_dir: str, expect: str, config_path: str) -> list[str]:
    config = load_yaml_config(config_path)
    theme = config.get("theme") or {}
    keep = theme_keep(
        docs_dir,
        theme.get("logo"),
        theme.get("favicon"),
        config.get("extra_css") or [],
        config.get("extra_javascript") or [],
    )
    planned = survey(docs_dir, keep)
    site_url = str(config.get("site_url") or "")
    failures: list[str] = []
    external_keys = {page_key(uri) for uri in planned.external_pages}

    texts = list(iter_text_files(site_dir))
    blob_hits: dict[str, list[str]] = {}

    def hits(token: str) -> list[str]:
        if token not in blob_hits:
            found = []
            for path, text in texts:
                if token in text:
                    found.append(os.path.relpath(path, site_dir))
            blob_hits[token] = found
        return blob_hits[token]

    search = search_docs(site_dir)
    if not search and planned.pages:
        failures.append("search index missing or empty: search/search_index.json")
    search_keys = set()
    for doc in search:
        if not isinstance(doc, dict):
            continue
        search_keys.add(norm_location(str(doc.get("location") or "")))

    locs = sitemap_locs(site_dir)
    if not locs and planned.external_pages and expect == "external":
        failures.append("sitemap missing or empty: sitemap.xml")
    loc_keys = {loc_key(loc, site_url) for loc in locs}

    title_tags = []
    for _path, text in texts:
        if "<title>" not in text.lower():
            continue
        title_tags.extend(TITLE_RE.findall(text))

    for src in sorted(planned.internal_pages):
        key = page_key(src)
        present = [
            rel for rel in output_candidates(src) if os.path.isfile(os.path.join(site_dir, rel))
        ]
        if expect == "external":
            if present:
                failures.append(f"internal html present: {present[0]}")
            if key in search_keys:
                failures.append(f"internal page in search index: {src}")
            if key in loc_keys:
                failures.append(f"internal page in sitemap: {src}")
            # Headings on external pages reuse phrases like "Before you start".
            # Only the document <title> is the published page title.
            title = planned.titles.get(src) or ""
            if title and any(title_matches(tag, title) for tag in title_tags):
                failures.append(f"internal title in html: {title}")
            for token in grep_tokens(src, external_keys):
                found = hits(token)
                if found:
                    failures.append(f"internal path {token!r} in {found[0]}")
        else:
            if not present:
                failures.append(f"internal html missing: {output_candidates(src)[0]}")

    for src in sorted(planned.external_pages):
        present = [
            rel for rel in output_candidates(src) if os.path.isfile(os.path.join(site_dir, rel))
        ]
        if not present:
            failures.append(f"external html missing: {output_candidates(src)[0]}")
        if expect == "internal" and page_key(src) not in search_keys and search:
            # Home and section indexes should be indexed when the internal build
            # includes them. A missing key is a leak in the other direction.
            failures.append(f"external page missing from internal search index: {src}")

    if expect == "external":
        for rel in sorted(planned.dropped):
            if rel.endswith(".md"):
                continue
            if os.path.isfile(os.path.join(site_dir, rel)):
                failures.append(f"internal asset present: {rel}")
            found = hits(rel)
            if found:
                failures.append(f"internal asset path {rel!r} in {found[0]}")
        for rel in sorted(keep):
            if is_internal_tree(rel):
                if os.path.isfile(os.path.join(site_dir, rel)):
                    failures.append(f"theme file under assets/internal present: {rel}")
                continue
            if not os.path.isfile(os.path.join(site_dir, rel)):
                failures.append(f"theme asset missing from external build: {rel}")
        for rel in sorted(planned.by_external):
            if is_internal_tree(rel) or rel in planned.dropped:
                continue
            if not os.path.isfile(os.path.join(site_dir, rel)):
                failures.append(f"external page asset missing: {rel}")
        if hits(ISSUE_LINK):
            failures.append("public GitHub issue link present in external build")
    else:
        if not hits(ISSUE_LINK):
            failures.append("internal build is missing the GitHub issue feedback link")
        for rel in sorted(planned.by_internal | planned.by_external | keep):
            if rel.endswith(".md") or not os.path.isfile(os.path.join(docs_dir, rel)):
                continue
            if not os.path.isfile(os.path.join(site_dir, rel)):
                failures.append(f"asset missing from internal build: {rel}")

    return failures


def list_pages(docs_dir: str) -> int:
    planned = survey(docs_dir, set())
    print(f"{'audience':<10} {'title':<32} path")
    for src in sorted(planned.pages, key=lambda item: (planned.pages[item], item)):
        audience = planned.pages[src]
        title = planned.titles.get(src, "")
        print(f"{audience:<10} {title:<32} {src}")
    print(
        f"{len(planned.external_pages)} external, {len(planned.internal_pages)} internal, "
        f"{len(planned.pages)} total"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", default=os.path.join(ROOT, "docs"))
    parser.add_argument("--site", default="")
    parser.add_argument("--config", default=os.path.join(ROOT, "mkdocs.yml"))
    parser.add_argument("--expect", choices=("external", "internal"))
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    if args.list:
        return list_pages(args.docs)
    if not args.site or not args.expect:
        parser.error("--site and --expect are required unless --list is set")
    failures = check(args.docs, args.site, args.expect, args.config)
    if failures:
        print(f"audience check failed ({args.expect}, {len(failures)}):", file=sys.stderr)
        for item in failures:
            print(f"  {item}", file=sys.stderr)
        return 1
    print(f"audience check passed ({args.expect})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

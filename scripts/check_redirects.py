#!/usr/bin/env python3
"""Fail if a redirect source still exists, or its target page does not.

Paths are relative to docs/, matching mkdocs-redirects. An empty
redirect_maps is valid. Assets are not redirect targets.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MKDOCS = ROOT / "mkdocs.yml"
DOCS = ROOT / "docs"


def die(messages: list[str]) -> None:
    for message in messages:
        print(f"redirects: {message}", file=sys.stderr)
    sys.exit(1)


def plugin_options(config: dict) -> dict:
    plugins = config.get("plugins")
    if isinstance(plugins, dict):
        entries = list(plugins.items())
    elif isinstance(plugins, list):
        entries = []
        for entry in plugins:
            if isinstance(entry, str):
                entries.append((entry, {}))
            elif isinstance(entry, dict) and len(entry) == 1:
                name, opts = next(iter(entry.items()))
                entries.append((name, opts or {}))
            else:
                die([f"unrecognized plugins entry: {entry!r}"])
    else:
        die(["mkdocs.yml is missing the redirects plugin"])

    found = None
    for name, opts in entries:
        if name != "redirects":
            continue
        if found is not None:
            die(["redirects plugin is configured more than once"])
        if not isinstance(opts, dict):
            die(["redirects plugin options must be a mapping"])
        found = opts
    if found is None:
        die(["redirects plugin is not configured"])
    if "redirect_maps" not in found:
        die(["redirects plugin is missing redirect_maps"])
    maps = found["redirect_maps"] or {}
    if not isinstance(maps, dict):
        die([f"redirect_maps must be a mapping, got {type(maps).__name__}"])
    return maps


def docs_page(raw: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        errors.append(f"{label} is empty")
        return None
    text = raw.strip().split("#", 1)[0].split("?", 1)[0].strip()
    if not text or "://" in text or text.startswith(("/", "\\")):
        errors.append(f"{label} {raw!r} is not a page under docs/")
        return None
    rel = Path(text)
    if rel.is_absolute() or ".." in rel.parts:
        errors.append(f"{label} {raw!r} must stay inside docs/")
        return None
    path = DOCS / rel
    try:
        path.resolve().relative_to(DOCS.resolve())
    except ValueError:
        errors.append(f"{label} {raw!r} must stay inside docs/")
        return None
    return path


def main() -> None:
    if not MKDOCS.is_file():
        die([f"missing {MKDOCS}"])
    config = yaml.safe_load(MKDOCS.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        die(["mkdocs.yml is not a mapping"])
    maps = plugin_options(config)
    errors: list[str] = []
    for src, dest in maps.items():
        src_path = docs_page(src, f"source {src!r}", errors)
        dest_path = docs_page(dest, f"target for {src!r}", errors)
        if src_path is not None and src_path.exists():
            errors.append(f"source still exists: {src}")
        if dest_path is not None and not dest_path.is_file():
            errors.append(f"target does not exist: {src} -> {dest}")
    if errors:
        die(errors)
    print(f"redirects: {len(maps)} mapping(s) ok")


if __name__ == "__main__":
    main()

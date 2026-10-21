#!/usr/bin/env python3
"""Fail if styling escapes docs/stylesheets/extra.css.

Scans overrides/, docs/javascripts/, and docs Markdown for inline styles.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLES = ("style=", "<style", ".style.", "cssText")


def files() -> list[Path]:
    found: list[Path] = []
    for folder in (ROOT / "overrides", ROOT / "docs" / "javascripts"):
        if folder.is_dir():
            found.extend(p for p in folder.rglob("*") if p.is_file())
    docs = ROOT / "docs"
    if docs.is_dir():
        found.extend(docs.rglob("*.md"))
    return found


def main() -> None:
    hits: list[str] = []
    for path in files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            if any(needle in line for needle in NEEDLES):
                rel = path.relative_to(ROOT)
                hits.append(f"{rel}:{lineno}: {line.strip()}")
    if hits:
        print("inline style forbidden outside docs/stylesheets/extra.css:", file=sys.stderr)
        for hit in hits:
            print(hit, file=sys.stderr)
        sys.exit(1)
    print(f"inline styles: none in {len(files())} file(s)")


if __name__ == "__main__":
    main()

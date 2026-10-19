"""Two MkDocs builds, selected by DOCS_AUDIENCE=internal or external.

Every Markdown page must set ``audience`` to internal or external
(case-insensitive). A missing or unknown value fails the build. There is
no default, for the page or for DOCS_AUDIENCE.

The internal build publishes every page and asset, and still checks audience.
The external build leaves out internal pages (so they are absent from the
HTML, nav, search index and sitemap), everything under ``assets/internal/``,
and any other asset that only internal pages reference.
"""

from __future__ import annotations

import logging
import os
import posixpath
import re
from dataclasses import dataclass, field

from mkdocs.exceptions import Abort
from mkdocs.utils import meta as meta_util

log = logging.getLogger("mkdocs.plugins.audience")

VALID = frozenset({"internal", "external"})
INTERNAL_ASSET_PREFIX = "assets/internal/"
MEDIA_KEYS = ("video", "video_poster")

LINK_RE = re.compile(
    r"(?<!!)\[([^\]\n]*)\]\(([^)\s]+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\)"
)
IMAGE_RE = re.compile(
    r"!\[([^\]\n]*)\]\(([^)\s]+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\)"
)
HTML_URL_RE = re.compile(r"""(?:src|href)\s*=\s*['"]([^'"]+)['"]""", re.I)
CSS_URL_RE = re.compile(r"""url\(\s*['"]?([^'")\s]+)['"]?\s*\)""")

_STATE = {"mode": "", "dropped": frozenset()}


def _fail(message: str) -> None:
    raise Abort(message)


def audience_mode() -> str:
    raw = os.environ.get("DOCS_AUDIENCE")
    if raw is None or not str(raw).strip():
        _fail(
            "DOCS_AUDIENCE is not set. Set it to internal or external. "
            "There is no default."
        )
    mode = str(raw).strip().lower()
    if mode not in VALID:
        _fail(f"DOCS_AUDIENCE must be internal or external, got {raw!r}.")
    return mode


def display_path(docs_dir: str, path: str) -> str:
    root = os.path.dirname(os.path.abspath(docs_dir))
    rel = os.path.relpath(os.path.abspath(path), root)
    return rel.replace(os.sep, "/")


def is_internal_tree(src_uri: str) -> bool:
    return src_uri == "assets/internal" or src_uri.startswith(INTERNAL_ASSET_PREFIX)


def load_meta(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    _body, data = meta_util.get_data(text)
    return data if isinstance(data, dict) else {}


def page_audience(path: str, docs_dir: str) -> str:
    shown = display_path(docs_dir, path)
    try:
        data = load_meta(path)
    except OSError as exc:
        _fail(f"audience missing: {shown} ({exc})")
    if "audience" not in data or data.get("audience") is None:
        _fail(f"audience missing: {shown}")
    raw = data.get("audience")
    if isinstance(raw, str) and not raw.strip():
        _fail(f"audience missing: {shown}")
    value = str(raw).strip().lower()
    if value not in VALID:
        _fail(f"bad audience {raw!r}: {shown}")
    return value


def page_title(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    body, data = meta_util.get_data(text)
    if isinstance(data, dict):
        title = data.get("title")
        if isinstance(title, str) and title.strip():
            return title.strip()
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return posixpath.splitext(posixpath.basename(path))[0]


def resolve_ref(src_uri: str, raw: str) -> str | None:
    raw = raw.strip()
    if not raw or raw.startswith(("#", "mailto:")):
        return None
    if raw.startswith("<") and raw.endswith(">"):
        raw = raw[1:-1].strip()
    raw = raw.split("#", 1)[0].split("?", 1)[0].strip()
    if not raw or "://" in raw or raw.startswith("//") or raw.startswith("/"):
        return None
    rel = posixpath.normpath(posixpath.join(posixpath.dirname(src_uri), raw))
    if rel == ".." or rel.startswith("../"):
        return None
    return rel


def asset_refs(src_uri: str, abs_path: str) -> set[str]:
    with open(abs_path, encoding="utf-8") as handle:
        text = handle.read()
    found: set[str] = set()
    _body, data = meta_util.get_data(text)
    if isinstance(data, dict):
        for key in MEDIA_KEYS:
            val = data.get(key)
            if isinstance(val, str) and val.strip():
                rel = resolve_ref(src_uri, val.strip())
                if rel:
                    found.add(rel)
    for pattern in (IMAGE_RE, LINK_RE):
        for match in pattern.finditer(text):
            rel = resolve_ref(src_uri, match.group(2))
            if rel and not rel.endswith(".md"):
                found.add(rel)
    for match in HTML_URL_RE.finditer(text):
        rel = resolve_ref(src_uri, match.group(1))
        if rel and not rel.endswith(".md"):
            found.add(rel)
    return found


def theme_keep(docs_dir: str, logo, favicon, stylesheets, scripts) -> set[str]:
    keep: set[str] = set()
    for val in (logo, favicon):
        if isinstance(val, str) and val.strip():
            rel = posixpath.normpath(val.strip())
            if rel != ".." and not rel.startswith("../"):
                keep.add(rel)
    sheets = []
    for item in list(stylesheets or []) + list(scripts or []):
        rel = str(item).split("#", 1)[0].split("?", 1)[0].strip()
        if not rel:
            continue
        rel = posixpath.normpath(rel)
        if rel == ".." or rel.startswith("../"):
            continue
        keep.add(rel)
        sheets.append(rel)
    for rel in sheets:
        if not rel.endswith(".css"):
            continue
        path = os.path.join(docs_dir, rel)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        for match in CSS_URL_RE.finditer(text):
            ref = resolve_ref(rel, match.group(1))
            if ref:
                keep.add(ref)
    return keep


def theme_keep_from_config(config) -> set[str]:
    logo = favicon = None
    theme = config.theme
    if theme is not None:
        try:
            logo = theme["logo"]
        except (KeyError, TypeError):
            logo = None
        try:
            favicon = theme["favicon"]
        except (KeyError, TypeError):
            favicon = None
    return theme_keep(
        config.docs_dir,
        logo,
        favicon,
        list(config.extra_css or []),
        list(config.extra_javascript or []),
    )


@dataclass
class Survey:
    pages: dict[str, str] = field(default_factory=dict)
    titles: dict[str, str] = field(default_factory=dict)
    by_internal: set[str] = field(default_factory=set)
    by_external: set[str] = field(default_factory=set)
    dropped: set[str] = field(default_factory=set)

    @property
    def internal_pages(self) -> set[str]:
        return {uri for uri, audience in self.pages.items() if audience == "internal"}

    @property
    def external_pages(self) -> set[str]:
        return {uri for uri, audience in self.pages.items() if audience == "external"}


def _walk_docs(docs_dir: str) -> list[tuple[str, str]]:
    found = []
    for dirpath, dirnames, filenames in os.walk(docs_dir):
        dirnames.sort()
        for name in sorted(filenames):
            abs_path = os.path.join(dirpath, name)
            rel = os.path.relpath(abs_path, docs_dir).replace(os.sep, "/")
            found.append((rel, abs_path))
    return found


def survey(docs_dir: str, keep: set[str] | None = None) -> Survey:
    """Read every docs file. Abort if any page has a missing or bad audience."""
    keep = keep or set()
    result = Survey()
    refs: dict[str, set[str]] = {}
    for rel, abs_path in _walk_docs(docs_dir):
        if not rel.endswith(".md"):
            continue
        result.pages[rel] = page_audience(abs_path, docs_dir)
        result.titles[rel] = page_title(abs_path)
        refs[rel] = asset_refs(rel, abs_path)
    for rel, audience in result.pages.items():
        bucket = result.by_internal if audience == "internal" else result.by_external
        bucket.update(refs.get(rel, ()))
    present = {rel for rel, _abs in _walk_docs(docs_dir)}
    for rel in present:
        if rel.endswith(".md"):
            if result.pages.get(rel) == "internal" or is_internal_tree(rel):
                result.dropped.add(rel)
            continue
        internal_only = (
            rel in result.by_internal
            and rel not in result.by_external
            and rel not in keep
        )
        if is_internal_tree(rel) or internal_only:
            result.dropped.add(rel)
    return result


def _matches_dropped(resolved: str, dropped: frozenset[str] | set[str]) -> bool:
    if resolved in dropped:
        return True
    candidates = []
    if not resolved.endswith(".md"):
        trimmed = resolved.rstrip("/")
        candidates.append(trimmed + ".md")
        candidates.append(trimmed + "/index.md")
    for candidate in candidates:
        if candidate in dropped:
            return True
    return False


def _target_dropped(src_uri: str, raw: str) -> bool:
    resolved = resolve_ref(src_uri, raw)
    if resolved is None:
        return False
    return _matches_dropped(resolved, _STATE["dropped"])


def rewrite_markdown(markdown: str, src_uri: str) -> str:
    """Drop links and images that point at files the external build removed."""
    if _STATE["mode"] != "external":
        return markdown
    lines = markdown.splitlines(keepends=True)
    out: list[str] = []
    prose: list[str] = []
    fence: str | None = None

    def flush() -> None:
        if not prose:
            return
        text = "".join(prose)
        prose.clear()

        def image_repl(match: re.Match[str]) -> str:
            if _target_dropped(src_uri, match.group(2)):
                return match.group(1)
            return match.group(0)

        def link_repl(match: re.Match[str]) -> str:
            if _target_dropped(src_uri, match.group(2)):
                return match.group(1)
            return match.group(0)

        text = IMAGE_RE.sub(image_repl, text)
        text = LINK_RE.sub(link_repl, text)
        out.append(text)

    for line in lines:
        stripped = line.lstrip()
        if fence is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            flush()
            fence = stripped[:3]
            out.append(line)
            continue
        if fence is not None:
            out.append(line)
            if stripped.startswith(fence):
                fence = None
            continue
        prose.append(line)
    flush()
    return "".join(out)


def prune_nav(items, docs_dir: str):
    if not items:
        return items
    kept = []
    for item in items:
        if isinstance(item, str):
            key, value = None, item
        elif isinstance(item, dict) and len(item) == 1:
            key, value = next(iter(item.items()))
        else:
            _fail(f"unrecognized nav entry: {item!r}")
        if isinstance(value, list):
            children = prune_nav(value, docs_dir)
            if children:
                kept.append({key: children})
            continue
        target = str(value)
        if target.endswith(".md"):
            rel = posixpath.normpath(target)
            path = os.path.join(docs_dir, rel)
            if is_internal_tree(rel) or page_audience(path, docs_dir) == "internal":
                continue
        kept.append(item)
    return kept


def _remember(mode: str, dropped: set[str]) -> None:
    _STATE["mode"] = mode
    _STATE["dropped"] = frozenset(dropped)


def on_config(config):
    mode = audience_mode()
    keep = theme_keep_from_config(config)
    planned = survey(config.docs_dir, keep)
    _remember(mode, planned.dropped if mode == "external" else set())
    config.extra["docs_audience"] = mode
    # Public GitHub issues stay off the external build until a feedback API exists.
    config.extra["issue_feedback"] = mode == "internal"
    if mode == "external" and config.nav:
        config.nav = prune_nav(config.nav, config.docs_dir)
    return config


def on_files(files, config):
    mode = audience_mode()
    keep = theme_keep_from_config(config)
    planned = survey(config.docs_dir, keep)
    dropped = planned.dropped if mode == "external" else set()
    _remember(mode, dropped)
    docs_root = os.path.abspath(config.docs_dir) + os.sep
    if mode == "external":
        for file in list(files):
            abs_src = os.path.abspath(file.abs_src_path)
            if not abs_src.startswith(docs_root):
                continue
            if file.src_uri in dropped:
                files.remove(file)
    log.info(
        "Audience %s: %d external page(s), %d internal page(s), %d file(s) omitted",
        mode,
        len(planned.external_pages),
        len(planned.internal_pages),
        len(dropped),
    )
    return files


def on_page_markdown(markdown, page, config, files):
    if _STATE["mode"] != "external":
        return markdown
    meta = page.meta or {}
    for key in MEDIA_KEYS:
        val = meta.get(key)
        if isinstance(val, str) and val.strip() and _target_dropped(page.file.src_uri, val):
            meta[key] = ""
    return rewrite_markdown(markdown, page.file.src_uri)

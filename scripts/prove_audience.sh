#!/usr/bin/env bash
# Port of the audience proof (eval/audience): internal pages, their paths and
# assets/internal must be absent from the external build, and a missing
# audience must fail both builds.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
MKDOCS=${MKDOCS:-mkdocs}
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

fail() {
  echo "prove_audience: $*" >&2
  exit 1
}

hits() {
  # $1 needle, $2 directory. Prints a match count. grep's "no match" status
  # is not a script failure.
  local out
  out=$(grep -R -I -F -o "$1" "$2" 2>/dev/null || true)
  if [[ -z "$out" ]]; then
    echo 0
  else
    printf '%s\n' "$out" | wc -l | tr -d ' '
  fi
}

cp "$ROOT/mkdocs.yml" "$ROOT/requirements.txt" "$WORK/"
cp -a "$ROOT/hooks" "$ROOT/overrides" "$ROOT/docs" "$WORK/"
cd "$WORK"

mkdir -p docs/assets/internal docs/assets/only-internal
echo "ZZ-INTERNAL-ASSET" > docs/assets/internal/secret.txt
echo "ZZ-ONLY-INTERNAL-ASSET" > docs/assets/only-internal/note.txt
echo "ZZ-SHARED-ASSET" > docs/assets/shared-marker.txt
printf '\n\nZZ-INTERNAL-MARKER-glossary\n\n[only internal](../assets/only-internal/note.txt)\n\n[shared marker](../assets/shared-marker.txt)\n' >> docs/reference/glossary.md
printf '\n\n[shared marker](../assets/shared-marker.txt)\n\n```\n[kept in fence](zz-fence-target.md)\n```\n' >> docs/get-started/index.md

# The published tree may mark every page internal (until a release flips the
# public set). The proof still needs one external page, so this scratch copy
# marks Get Started external. The repo files are not changed.
python3 - <<'PY'
from pathlib import Path
path = Path("docs/get-started/index.md")
text = path.read_text(encoding="utf-8")
start = text.find("audience:")
if start < 0:
    raise SystemExit("prove_audience: get-started has no audience line")
line_end = text.find("\n", start)
# Replace the whole line. A trailing comment can mention "external" while the
# value is still internal.
text = text[:start] + "audience: external" + text[line_end:]
path.write_text(text, encoding="utf-8")
PY

DOCS_AUDIENCE=internal "$MKDOCS" build --strict -d "$WORK/site-internal"
DOCS_AUDIENCE=external "$MKDOCS" build --strict -d "$WORK/site-external"

internal_markers=$(find "$WORK/site-internal" -name '*.html' -print0 | xargs -0 grep -l 'ZZ-INTERNAL-MARKER-glossary' | wc -l | tr -d ' ')
marker_hits=$(hits "ZZ-INTERNAL-MARKER-glossary" "$WORK/site-external")
projects_hits=$(hits "workbench/projects" "$WORK/site-external")
glossary_hits=$(hits "reference/glossary" "$WORK/site-external")
if [[ -e "$WORK/site-external/assets/internal/secret.txt" ]]; then
  asset_state="YES-LEAK"
else
  asset_state="no"
fi

echo "internal build has marker pages: ${internal_markers} files"
echo "external build: marker text hits: ${marker_hits}; 'workbench/projects' URL hits: ${projects_hits}; glossary hits: ${glossary_hits}"
echo "external build: internal asset present? ${asset_state}"

[[ "$internal_markers" -ge 1 ]] || fail "internal build did not publish the marker page"
[[ "$marker_hits" == 0 ]] || fail "marker text leaked into the external build"
[[ "$projects_hits" == 0 ]] || fail "workbench/projects leaked into the external build"
[[ "$glossary_hits" == 0 ]] || fail "reference/glossary leaked into the external build"
[[ "$asset_state" == no ]] || fail "docs/assets/internal leaked into the external build"
[[ -f "$WORK/site-internal/assets/internal/secret.txt" ]] || fail "internal build dropped assets/internal"
[[ ! -e "$WORK/site-external/assets/only-internal/note.txt" ]] || fail "asset referenced only by an internal page leaked"
[[ $(hits "only-internal/note.txt" "$WORK/site-external") == 0 ]] || fail "internal-only asset path leaked"
[[ -f "$WORK/site-internal/assets/only-internal/note.txt" ]] || fail "internal build dropped an internal-only asset"
[[ -f "$WORK/site-external/assets/shared-marker.txt" ]] || fail "asset referenced by an external page was dropped"
[[ -f "$WORK/site-external/assets/adaptify-logo.png" ]] || fail "theme logo missing from the external build"
[[ -f "$WORK/site-external/get-started/index.html" ]] || fail "External page get-started was dropped (case)"
[[ ! -e "$WORK/site-external/index.html" ]] || fail "internal homepage was published in the external build"
[[ $(hits "issues/new" "$WORK/site-external") == 0 ]] || fail "public issue link leaked into the external build"
[[ $(hits "issues/new" "$WORK/site-internal") -ge 1 ]] || fail "internal build hid the issue feedback link"
[[ $(hits "zz-fence-target.md" "$WORK/site-external") -ge 1 ]] || fail "rewriter changed a fenced code sample"
[[ $(hits "workbench/" "$WORK/site-external") == 0 ]] || fail "internal workbench path still linked from the external build"

# Missing and unknown audience fail both builds. There is no default.
cp docs/support/index.md "$WORK/support.md.bak"
python3 - <<'PY'
from pathlib import Path
path = Path("docs/support/index.md")
text = path.read_text(encoding="utf-8")
text = text.replace("audience: internal\n", "", 1)
path.write_text(text, encoding="utf-8")
PY

build_fails() {
  local mode=$1
  local log=$2
  set +e
  DOCS_AUDIENCE="$mode" "$MKDOCS" build --strict -d "$WORK/bad-$mode" >"$log" 2>&1
  local status=$?
  set -e
  [[ "$status" -ne 0 ]] || fail "$mode build succeeded without audience"
  grep -q "audience missing:" "$log" || fail "$mode build did not report audience missing"
}

build_fails internal "$WORK/missing-internal.log"
build_fails external "$WORK/missing-external.log"
echo "audience missing: docs/support/index.md"
echo "internal build with a missing audience: FAILS"
echo "external build with a missing audience: FAILS"

cp "$WORK/support.md.bak" docs/support/index.md
python3 - <<'PY'
from pathlib import Path
path = Path("docs/support/index.md")
text = path.read_text(encoding="utf-8")
text = text.replace("audience: internal\n", "audience: staff\n", 1)
path.write_text(text, encoding="utf-8")
PY
for mode in internal external; do
  set +e
  DOCS_AUDIENCE="$mode" "$MKDOCS" build --strict -d "$WORK/bad-value-$mode" >"$WORK/bad-value-$mode.log" 2>&1
  status=$?
  set -e
  [[ "$status" -ne 0 ]] || fail "$mode build accepted audience: staff"
  grep -q "bad audience" "$WORK/bad-value-$mode.log" || fail "$mode build did not report bad audience"
done

set +e
env -u DOCS_AUDIENCE "$MKDOCS" build --strict -d "$WORK/bad-unset" >"$WORK/unset.log" 2>&1
status=$?
set -e
[[ "$status" -ne 0 ]] || fail "build succeeded without DOCS_AUDIENCE"
grep -q "DOCS_AUDIENCE is not set" "$WORK/unset.log" || fail "unset DOCS_AUDIENCE was not rejected"

# Case-insensitive mode, and the existing 'External' front matter.
cp "$WORK/support.md.bak" docs/support/index.md
DOCS_AUDIENCE=EXTERNAL "$MKDOCS" build --strict -d "$WORK/site-external-case"
[[ -f "$WORK/site-external-case/get-started/index.html" ]] || fail "DOCS_AUDIENCE=EXTERNAL did not build external pages"

echo "prove_audience: PASS"

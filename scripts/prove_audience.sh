#!/usr/bin/env bash
# Prove the audience hook against tests/fixtures/audience, not the real docs.
# The fixture has one internal page and one external page. Real pages can
# change audience (a release PR flips the glossary) without breaking this.
# Real-site strict builds stay in CI; this script only checks that the
# fixture markers did not land in those outputs when the directories exist.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
MKDOCS=${MKDOCS:-mkdocs}
FIXTURE="$ROOT/tests/fixtures/audience"
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

html_hits() {
  # $1 needle, $2 directory. Same as hits(), limited to HTML files.
  local out
  out=$(grep -R -I -F -o --include='*.html' "$1" "$2" 2>/dev/null || true)
  if [[ -z "$out" ]]; then
    echo 0
  else
    printf '%s\n' "$out" | wc -l | tr -d ' '
  fi
}

content_pages() {
  # HTML pages other than the theme 404. A build of only 404.html counts as 0.
  find "$1" -type f -name '*.html' ! -name '404.html' | wc -l | tr -d ' '
}

external_docs() {
  # Markdown pages under docs/ whose front matter audience is external.
  ROOT_DOCS="$ROOT/docs" python3 - <<'PY'
import os
root = os.environ["ROOT_DOCS"]
count = 0
for dirpath, _, files in os.walk(root):
    for name in files:
        if not name.endswith(".md"):
            continue
        path = os.path.join(dirpath, name)
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end < 0:
            continue
        for line in text[3:end].splitlines():
            stripped = line.strip()
            if not stripped.lower().startswith("audience:"):
                continue
            value = stripped.split(":", 1)[1].split("#", 1)[0].strip().strip("'\"").lower()
            if value == "external":
                count += 1
            break
print(count)
PY
}

[[ -f "$FIXTURE/mkdocs.yml" ]] || fail "missing fixture config"
[[ -f "$FIXTURE/docs/internal.md" ]] || fail "missing fixture internal page"
[[ -f "$FIXTURE/docs/external.md" ]] || fail "missing fixture external page"
[[ $(hits "ZZ-AUDIENCE-FIXTURE" "$ROOT/docs") == 0 ]] || fail "fixture marker is inside the real docs tree"

DOCS_AUDIENCE=internal "$MKDOCS" build --strict -f "$FIXTURE/mkdocs.yml" -d "$WORK/site-internal"
DOCS_AUDIENCE=external "$MKDOCS" build --strict -f "$FIXTURE/mkdocs.yml" -d "$WORK/site-external"

[[ -f "$WORK/site-internal/internal/index.html" ]] || fail "internal build dropped the internal fixture page"
[[ -f "$WORK/site-internal/external/index.html" ]] || fail "internal build dropped the external fixture page"
[[ -f "$WORK/site-external/external/index.html" ]] || fail "external build dropped the external fixture page"
[[ ! -e "$WORK/site-external/internal/index.html" ]] || fail "external build published the internal fixture page"
[[ $(hits "ZZ-AUDIENCE-FIXTURE-INTERNAL" "$WORK/site-internal") -ge 1 ]] || fail "internal build lost the internal marker"
[[ $(hits "ZZ-AUDIENCE-FIXTURE-EXTERNAL" "$WORK/site-internal") -ge 1 ]] || fail "internal build lost the external marker"
[[ $(hits "ZZ-AUDIENCE-FIXTURE-INTERNAL" "$WORK/site-external") == 0 ]] || fail "internal marker leaked into the external build"
[[ $(hits "ZZ-AUDIENCE-FIXTURE-EXTERNAL" "$WORK/site-external") -ge 1 ]] || fail "external build lost the external marker"
[[ -f "$WORK/site-internal/assets/internal/secret.txt" ]] || fail "internal build dropped assets/internal"
[[ ! -e "$WORK/site-external/assets/internal/secret.txt" ]] || fail "assets/internal leaked into the external build"
[[ -f "$WORK/site-internal/assets/only-internal/note.txt" ]] || fail "internal build dropped an internal-only asset"
[[ ! -e "$WORK/site-external/assets/only-internal/note.txt" ]] || fail "asset referenced only by an internal page leaked"
[[ $(hits "only-internal/note.txt" "$WORK/site-external") == 0 ]] || fail "internal-only asset path leaked"
[[ -f "$WORK/site-external/assets/shared-marker.txt" ]] || fail "asset referenced by an external page was dropped"
[[ $(hits "zz-fence-target.md" "$WORK/site-external") -ge 1 ]] || fail "rewriter changed a fenced code sample"
[[ $(hits "staff note" "$WORK/site-external") -ge 1 ]] || fail "external page lost the label of a link to an internal page"
[[ $(hits "internal/" "$WORK/site-external/external/index.html") == 0 ]] || fail "external page still links to the internal fixture page"
[[ $(hits "issues/new" "$WORK/site-external") == 0 ]] || fail "public issue link leaked into the external build"
[[ $(hits "issues/new" "$WORK/site-internal") -ge 1 ]] || fail "internal build hid the issue feedback link"
[[ $(hits "Contact Adaptify support" "$WORK/site-internal") == 0 ]] || fail "unset support_url rendered a contact link"
[[ $(hits "Contact Adaptify support" "$WORK/site-external") == 0 ]] || fail "unset support_url rendered a contact link"
[[ $(hits "/edit/main/docs/" "$WORK/site-internal") -ge 1 ]] || fail "internal build missing the edit link"
[[ $(hits "Edit this page on GitHub" "$WORK/site-internal") -ge 1 ]] || fail "internal build missing the edit tooltip"
[[ $(hits "/edit/" "$WORK/site-external") == 0 ]] || fail "external build contains an edit link"
[[ $(hits "github.com/AshNaikAdaptify/adaptify-docs" "$WORK/site-external") == 0 ]] || fail "external build links to the public repo"
[[ $(html_hits 'class="md-source"' "$WORK/site-external") == 0 ]] || fail "external build rendered the repository header link"
fixture_ext_pages=$(content_pages "$WORK/site-external")
echo "prove_audience: fixture external non-404 pages: ${fixture_ext_pages}"
[[ "$fixture_ext_pages" -ge 1 ]] || fail "fixture external build has no content pages"

for site in "$ROOT/site-internal" "$ROOT/site-external"; do
  if [[ -d "$site" ]]; then
    [[ $(hits "ZZ-AUDIENCE-FIXTURE" "$site") == 0 ]] || fail "fixture page leaked into the real site build at $site"
  fi
done

# The fixture always has an external page. A real site-external directory
# (CI builds one before this script) may be 404-only when every doc is
# internal. Print that count. Fail only when docs actually mark pages external
# and the build still published none of them, and keep the edit/repo checks
# on whatever HTML was published.
if [[ -d "$ROOT/site-external" ]]; then
  real_ext_pages=$(content_pages "$ROOT/site-external")
  real_ext_sources=$(external_docs)
  echo "prove_audience: site-external non-404 pages: ${real_ext_pages} (docs with audience external: ${real_ext_sources})"
  if [[ "$real_ext_sources" -ge 1 && "$real_ext_pages" -lt 1 ]]; then
    fail "external pages are in docs but site-external has no non-404 HTML"
  fi
  [[ $(html_hits "/edit/" "$ROOT/site-external") == 0 ]] || fail "site-external HTML contains an edit link"
  [[ $(html_hits 'class="md-source"' "$ROOT/site-external") == 0 ]] || fail "site-external HTML contains the repository header link"
  [[ $(html_hits "github.com/AshNaikAdaptify/adaptify-docs" "$ROOT/site-external") == 0 ]] || fail "site-external HTML links to the public repo"
fi

write_config() {
  # $1 dest yml, $2 docs_dir, $3 optional extra support_url line
  local dest=$1 docs_dir=$2 support_line=${3:-}
  cat > "$dest" <<EOF
site_name: Audience fixture
site_url: https://example.invalid/audience-fixture/
docs_dir: ${docs_dir}
theme:
  name: material
  custom_dir: ${ROOT}/overrides
hooks:
  - ${ROOT}/hooks/audience.py
extra:
  feedback_repo: example/fixture
${support_line}
nav:
  - Internal: internal.md
  - External: external.md
EOF
}

build_fails() {
  local mode=$1 config=$2 log=$3 needle=$4
  set +e
  DOCS_AUDIENCE="$mode" "$MKDOCS" build --strict -f "$config" -d "$WORK/bad-$mode" >"$log" 2>&1
  local status=$?
  set -e
  [[ "$status" -ne 0 ]] || fail "$mode build succeeded: $config"
  grep -q "$needle" "$log" || fail "$mode build did not report: $needle"
}

# Missing and unknown audience fail both builds. There is no default.
cp -a "$FIXTURE/docs" "$WORK/docs-missing"
python3 - <<PY
from pathlib import Path
path = Path("$WORK/docs-missing/internal.md")
text = path.read_text(encoding="utf-8")
start = text.find("audience:")
if start < 0:
    raise SystemExit("prove_audience: fixture internal page has no audience line")
line_end = text.find("\n", start)
text = text[:start] + text[line_end + 1:]
path.write_text(text, encoding="utf-8")
PY
write_config "$WORK/missing.yml" "$WORK/docs-missing"
build_fails internal "$WORK/missing.yml" "$WORK/missing-internal.log" "audience missing:"
build_fails external "$WORK/missing.yml" "$WORK/missing-external.log" "audience missing:"

cp -a "$FIXTURE/docs" "$WORK/docs-bad"
python3 - <<PY
from pathlib import Path
path = Path("$WORK/docs-bad/internal.md")
text = path.read_text(encoding="utf-8")
start = text.find("audience:")
if start < 0:
    raise SystemExit("prove_audience: fixture internal page has no audience line")
line_end = text.find("\n", start)
text = text[:start] + "audience: staff" + text[line_end:]
path.write_text(text, encoding="utf-8")
PY
write_config "$WORK/bad-value.yml" "$WORK/docs-bad"
build_fails internal "$WORK/bad-value.yml" "$WORK/bad-value-internal.log" "bad audience"
build_fails external "$WORK/bad-value.yml" "$WORK/bad-value-external.log" "bad audience"

set +e
env -u DOCS_AUDIENCE "$MKDOCS" build --strict -f "$FIXTURE/mkdocs.yml" -d "$WORK/bad-unset" >"$WORK/unset.log" 2>&1
status=$?
set -e
[[ "$status" -ne 0 ]] || fail "build succeeded without DOCS_AUDIENCE"
grep -q "DOCS_AUDIENCE is not set" "$WORK/unset.log" || fail "unset DOCS_AUDIENCE was not rejected"

DOCS_AUDIENCE=EXTERNAL "$MKDOCS" build --strict -f "$FIXTURE/mkdocs.yml" -d "$WORK/site-external-case"
[[ -f "$WORK/site-external-case/external/index.html" ]] || fail "DOCS_AUDIENCE=EXTERNAL did not build the external fixture page"
[[ ! -e "$WORK/site-external-case/internal/index.html" ]] || fail "DOCS_AUDIENCE=EXTERNAL published the internal fixture page"

# Blank support_url renders nothing. A real value renders the contact link.
write_config "$WORK/blank-support.yml" "$FIXTURE/docs" '  support_url: "   "'
DOCS_AUDIENCE=internal "$MKDOCS" build --strict -f "$WORK/blank-support.yml" -d "$WORK/site-blank-support"
[[ $(hits "Contact Adaptify support" "$WORK/site-blank-support") == 0 ]] || fail "blank support_url rendered a contact link"

write_config "$WORK/set-support.yml" "$FIXTURE/docs" "  support_url: https://example.invalid/help"
DOCS_AUDIENCE=internal "$MKDOCS" build --strict -f "$WORK/set-support.yml" -d "$WORK/site-set-support"
[[ $(hits "https://example.invalid/help" "$WORK/site-set-support") -ge 1 ]] || fail "set support_url did not render"
[[ $(hits "Contact Adaptify support" "$WORK/site-set-support") -ge 1 ]] || fail "set support_url did not render the contact link"

echo "prove_audience: PASS"

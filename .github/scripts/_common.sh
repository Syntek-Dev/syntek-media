#!/usr/bin/env bash
#
# _common.sh — the one home for what every syntek-media audit reads. Sourced, never run.
#
#              Sixteen audits ask overlapping questions of the same four inputs: copier.yml
#              (what is gated, what is seeded, which tokens are registered), DESIGN.md (what
#              each brand kind, platform and media kind must ship), a tree (the template source,
#              a standalone render, or a render applied over syntek-author), and the frozen list
#              of syntek-author's names. When each script carried its own parser they disagreed
#              — about whether `/README.md` and `README.md` name the same seed, about whether
#              `not ('youtube' in PLATFORMS)` and `'youtube' in PLATFORMS` are the same gate — and
#              an audit that disagrees with its neighbour about the input is two audits that
#              cannot both be right. One reader, one home (syntek-author's _common.sh, ported).
#
#              What lives here:
#                - logging, findings, the named SKIP and the self-test harness (SB house shape);
#                - copier.yml readers: list items, registered keys, question choices, gated
#                  paths, gate negation (list membership included: DESIGN.md D15);
#                - the DESIGN.md catalogue: skills (media's and the seven family skills),
#                  mode files, gated paths (AGENT_CLIENTS's included), seeds, examples, the
#                  copy-only shared paths (one retired) and the two client folders' update
#                  gates, the spine set, the identity tokens, the companion skills, pair-only
#                  folders and pair exemptions, the D13 allow, ask, deny and hook lists, the
#                  _message_after_copy lines, and the D83 community files and
#                  private-reporting URL;
#                - SM_FAMILY_SHARED, the family-shared set media vendors from one syntek-author
#                  tag (DESIGN.md D80, D81, D85; syntek-author D48): forty-three files and four
#                  blocks since 0.6.0, the update script and the user guide's fourteen among
#                  them, the one list every audit's family exemption reads, and sm_family_py,
#                  the reader (and writer) of the root family-shared.json that records it;
#                - a reader for a rendered tree's answers (multiselect lists included), a gate
#                  evaluator, and the over-author scope (<render>.owned, DESIGN.md Section 7);
#                - syntek-author's names: the frozen file (syntek-author-names.txt, D27), the
#                  generator that lists a live tree's names, and the drift between the two;
#                - the rendering helpers (snapshot a working tree, render media, render
#                  syntek-author, apply media over it), the family-shared migrations and
#                  update blocks (D85, D81) and the two fixture templates the integration
#                  self-tests run against;
#                - the Python pin (DESIGN.md D81, Section 7): sourcing this file refuses, with
#                  one message saying why, a python3 or a UV_PYTHON older than SM_PYTHON_MIN,
#                  and pins UV_PYTHON to python3 where it is unset (CI sets it), so every
#                  Copier the audits run, and the family scripts inside it, run on 3.14.
#
#              The catalogue is DESIGN.md transcribed. When DESIGN.md changes, this file
#              changes in the same commit; every audit that reads it then moves together.
#              syntek-author's names are never transcribed here: they are read from
#              syntek-author-names.txt, which only `coexist-test.sh --refresh-names` writes.
#
#              Nothing here writes to the repository, except sm_family_py's write mode, which
#              only shipped-seeds.sh --write-manifest runs: it rewrites the root
#              family-shared.json from the vendored files. Fixtures and snapshots go to mktemp.
#
# Requirements: bash 4.3+, git, grep, awk, sed; python3 SM_PYTHON_MIN (3.14) or later, which
#               sourcing this file checks. rsync and uvx only for the rendering helpers:
#               copier_init's `uvx copier` runs on the pinned UV_PYTHON, which is why
#               docs-pairing.sh check 20 does not read .github/scripts/.

# This file is a library: its catalogue variables are read by the scripts that source it.
# shellcheck disable=SC2034

[[ -n "${_SM_COMMON_LOADED:-}" ]] && return 0
_SM_COMMON_LOADED=1

SM_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SM_ROOT="${SM_ROOT:-$(cd "$SM_SCRIPTS_DIR/../.." && pwd)}"
SM_ANSWERS_FILE=".copier-answers.syntek-media.yml"
SM_AUTHOR_ANSWERS=".copier-answers.syntek-author.yml"
SM_AUTHOR_NAMES_FILE="${SM_AUTHOR_NAMES_FILE:-$SM_SCRIPTS_DIR/syntek-author-names.txt}"
: "${SCRIPT_NAME:=audit}"

# ── Logging and findings ─────────────────────────────────────────────────────

QUIET=${QUIET:-false}
log()  { $QUIET || printf '%s\n' "$*"; }
note() { printf '%s\n' "$*" >&2; }
die()  { printf '%s error: %s\n' "$SCRIPT_NAME" "$*" >&2; exit 2; }
bold() { $QUIET || printf '\033[1m%s\033[0m\n' "$*"; }

FINDINGS=()
finding() { FINDINGS+=("$1"); }

print_findings() {
  local f
  for f in "${FINDINGS[@]}"; do printf '  · %s\n' "$f"; done
}

# A skip is NAMED, never counted as a pass (DESIGN.md D27). Every skip prints one line in this
# exact shape on stderr, --quiet or not; run-all.sh lists each one as SKIP in its summary.
skip_named() { # $1 = what was skipped, $2 = why
  printf 'SKIP — %s — %s\n' "$1" "$2" >&2
}

# ── Self-test harness ────────────────────────────────────────────────────────
#
# SB rule 38: a guard nobody has seen fail is a guard nobody knows works. The baseline must be
# clean first ("a mutation proof on a broken baseline means nothing"), then each mutation must
# produce EXACTLY ONE finding carrying the expected text — a check that fires for the wrong
# reason fails the proof as loudly as one that never fires.

ST_FAILS=0
ST_PROBES=0

st_baseline() { # $1 = what the baseline is
  run_checks
  if [[ ${#FINDINGS[@]} -ne 0 ]]; then
    printf '\033[31m  ✗ %s already fails — a mutation proof on a broken baseline means nothing\033[0m\n' "$1" >&2
    printf '    %s\n' "${FINDINGS[@]}" >&2
    exit 2
  fi
  log "  ✓ $1 passes — the baseline is clean"
}

probe() { # $1 = label, $2 = a substring the single expected finding must contain
  ST_PROBES=$((ST_PROBES + 1))
  run_checks
  if [[ ${#FINDINGS[@]} -eq 1 ]] && [[ "${FINDINGS[0]}" == *"$2"* ]]; then
    log "  ✓ $1"
  else
    ST_FAILS=$((ST_FAILS + 1))
    printf '\033[31m  ✗ %s produced %d finding(s): %s\033[0m\n' \
      "$1" "${#FINDINGS[@]}" "$(printf '%s; ' "${FINDINGS[@]:-(none)}")"
  fi
}

probe_clean() { # $1 = label — a shape the checks must NOT flag
  ST_PROBES=$((ST_PROBES + 1))
  run_checks
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $1"
  else
    ST_FAILS=$((ST_FAILS + 1))
    printf '\033[31m  ✗ %s produced %d finding(s): %s\033[0m\n' \
      "$1" "${#FINDINGS[@]}" "$(printf '%s; ' "${FINDINGS[@]}")"
  fi
}

st_finish() { # $1 = what the detector separates
  log ""
  if [[ "$ST_FAILS" -eq 0 ]]; then
    bold "✓ Self-test passed — $ST_PROBES probes: every check fires on its own mutation."
    return 0
  fi
  log "  the detector no longer separates $1 —"
  log "  fix the check, never the expectation."
  return 1
}

sm_mktemp() { mktemp -d "${TMPDIR:-/tmp}/syntek-media-audit.XXXXXX" || die "could not create a temporary directory"; }

# Scratch repositories must stay still once a script is done with them. After a commit, Git may
# start `gc --auto` or `maintenance run --auto` in the background, detached (GitHub runners do),
# and it can still be writing into .git while the cleanup removes the folder: "rm: cannot remove
# '…/.git': Directory not empty" ended update-test on a runner. Turning both off for every Git
# command an audit starts, Copier's included (it inherits the environment), keeps the race away;
# appended to any GIT_CONFIG_* pairs already set, never replacing them.
sm_git_quiet() {
  local n="${GIT_CONFIG_COUNT:-0}"
  export "GIT_CONFIG_KEY_$n=gc.auto" "GIT_CONFIG_VALUE_$n=0"
  export "GIT_CONFIG_KEY_$((n + 1))=maintenance.auto" "GIT_CONFIG_VALUE_$((n + 1))=false"
  export GIT_CONFIG_COUNT=$((n + 2))
}
sm_git_quiet

# Remove a scratch tree; one retry after a second covers a straggler that outlived its parent.
sm_rmtree() { rm -rf "$1" 2>/dev/null || { sleep 1; rm -rf "$1"; }; }

# ── The one Python minimum (DESIGN.md D81, Section 7; syntek-author D3, D18) ─
#
# Python 3.14 is media's base since 0.6.0: the vendored family scripts (the update script, the
# outside-link script, the data-root resolver, the permissions script) and the hooks need it,
# and below it each does nothing but print a framed warning, or refuses (exit 2). This is the
# audits' one copy of the number; CI's setup-python steps and UV_PYTHON name the same release.
SM_PYTHON_MIN="3.14"
# The house form every shown copy or update command runs Copier in (D3, D81): the minimum
# quoted, since unquoted the shell reads > as a redirection.
SM_UVX_COPIER="uvx --python '>=$SM_PYTHON_MIN' copier"

# "X.Y" of an interpreter on stdout; status 1, and nothing, where it does not run.
sm_py_version() { # $1 = interpreter
  local v
  v="$("$1" -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null)" || return 1
  [[ "$v" =~ ^[0-9]+\.[0-9]+$ ]] || return 1
  printf '%s\n' "$v"
}
# True where version $1 (X.Y) is older than $2 (X.Y; SM_PYTHON_MIN by default).
sm_py_older() { # $1 = X.Y, $2 = X.Y
  local a="$1" b="${2:-$SM_PYTHON_MIN}"
  [[ "$a" =~ ^[0-9]+\.[0-9]+$ && "$b" =~ ^[0-9]+\.[0-9]+$ ]] || return 1
  (( 10#${a%%.*} < 10#${b%%.*} || (10#${a%%.*} == 10#${b%%.*} && 10#${a#*.} < 10#${b#*.}) ))
}

# The pin, on the model of syntek-author's sa_python_pin. Every audit runs python3 itself (the
# vendored self-tests, the permissions script's --check, sm_family_py), and uvx runs Copier, with
# the family scripts inside it, on UV_PYTHON. On a Python older than SM_PYTHON_MIN each of those
# does nothing or refuses, by design, so an audit there would pass vacuously or report only the
# interpreter: refuse once, here, loudly, before anything runs (exit 2). uv prefers a managed
# interpreter it already has over python3, so an unpinned uvx may run Copier on an older one: CI
# sets UV_PYTHON to a version; locally it is pinned to python3. A UV_PYTHON that is a version, a
# path or any request uv can find without a download is judged too; one uv would download is
# uv's to fetch. SM_PYTHON_PINNED keeps a child process from judging the same pair again.
sm_python_pin() {
  local py v req want
  py="$(command -v python3 2>/dev/null || true)"
  [[ "${SM_PYTHON_PINNED:-}" != "$py|${UV_PYTHON:-}" || -z "$py" ]] || return 0
  if [[ -n "$py" ]]; then
    v="$(sm_py_version "$py")" || die "python3 ($py) does not run, so nothing ran"
    if sm_py_older "$v"; then
      die "python3 is Python $v ($py), and the audits need Python $SM_PYTHON_MIN or later: the minimum of the vendored family scripts, which Copier runs on its own Python, and of every shown Copier command ($SM_UVX_COPIER …). Nothing ran. Upgrade to Python $SM_PYTHON_MIN (or put it first on PATH; CI's setup-python steps name it) and run again."
    fi
  fi
  if [[ -n "${UV_PYTHON:-}" ]]; then
    req="$UV_PYTHON"; want=""
    if [[ "$req" =~ ^([0-9]+\.[0-9]+)(\.[0-9]+)?$ ]]; then want="${BASH_REMATCH[1]}"
    elif [[ "$req" == */* && -x "$req" ]]; then want="$(sm_py_version "$req" || true)"
    elif command -v uv >/dev/null 2>&1; then
      want="$(UV_PYTHON_DOWNLOADS=never uv python find "$req" 2>/dev/null || true)"
      [[ -z "$want" ]] || want="$(sm_py_version "$want" || true)"
    fi
    if [[ -n "$want" ]] && sm_py_older "$want"; then
      die "UV_PYTHON is '$req' (Python $want), so uvx would run Copier, and the family scripts inside it, on a Python older than $SM_PYTHON_MIN, where they do nothing. Nothing ran. Unset UV_PYTHON, or set it to $SM_PYTHON_MIN or later, and run again."
    fi
  elif [[ -n "$py" ]]; then
    UV_PYTHON="$py"
    export UV_PYTHON
  fi
  SM_PYTHON_PINNED="$py|${UV_PYTHON:-}"
  export SM_PYTHON_PINNED
}
sm_python_pin

# ── copier.yml readers ───────────────────────────────────────────────────────

# Every list item under a top-level key, unquoted, one per line. Comments and blank lines are
# skipped; the block ends at the next top-level key. Handles "double", 'single' (with '' as an
# escaped quote) and bare items, and strips a trailing comment from a bare item.
yaml_list() { # $1 = key, $2 = file
  [[ -f "$2" ]] || return 0
  awk -v key="$1" '
    function unq(s,   c, out, i, ch) {
      sub(/^[ \t]+/, "", s)
      c = substr(s, 1, 1)
      if (c == "\"") {
        out = ""; i = 2
        while (i <= length(s)) {
          ch = substr(s, i, 1)
          if (ch == "\\") { out = out substr(s, i + 1, 1); i += 2; continue }
          if (ch == "\"") break
          out = out ch; i++
        }
        return out
      }
      if (c == "\047") {
        out = ""; i = 2
        while (i <= length(s)) {
          ch = substr(s, i, 1)
          if (ch == "\047") { if (substr(s, i + 1, 1) == "\047") { out = out "\047"; i += 2; continue }; break }
          out = out ch; i++
        }
        return out
      }
      sub(/[ \t]+#.*/, "", s); sub(/[ \t]+$/, "", s)
      return s
    }
    $0 ~ "^" key ":" { on = 1; next }
    on && /^[A-Za-z_][A-Za-z0-9_]*:/ { exit }
    on && /^[ \t]*#/ { next }
    on && /^[ \t]+- / { line = $0; sub(/^[ \t]+- /, "", line); print unq(line) }
  ' "$2"
}

registered_keys() { # $1 = copier.yml
  grep -oE '^[A-Z][A-Z0-9_]*:' "$1" 2>/dev/null | tr -d ':' | sort -u
}

# The VALUES a question offers, one per line — never the labels. A choice is written as a flow
# list ([a, b]), a block list (- a), or syntek-author's labelled mapping ("label": value).
question_choices() { # $1 = key, $2 = copier.yml
  [[ -f "$2" ]] || return 0
  awk -v key="$1" '
    function unq(s) {
      sub(/^[ \t]+/, "", s); sub(/[ \t]+#.*/, "", s); sub(/[ \t]+$/, "", s)
      if (s ~ /^".*"$/ || s ~ /^\047.*\047$/) s = substr(s, 2, length(s) - 2)
      return s
    }
    function indent(s) { match(s, /^[ ]*/); return RLENGTH }
    $0 ~ "^" key ":" { inq = 1; next }
    inq && /^[A-Za-z_][A-Za-z0-9_]*:/ { exit }
    !inq { next }
    inch && /^[ \t]*(#|$)/ { next }
    inch && indent($0) <= chind { exit }
    inch {
      l = $0; sub(/^[ \t]+/, "", l)
      if (l ~ /^- /) { sub(/^- /, "", l); print unq(l); next }
      c = substr(l, 1, 1)
      if (c == "\"" || c == "\047") {
        rest = substr(l, 2); j = index(rest, c)
        if (j) { rest = substr(rest, j + 1); sub(/^[ \t]*:[ \t]*/, "", rest); print unq(rest) }
        next
      }
      j = index(l, ": "); if (j) print unq(substr(l, j + 2))
      next
    }
    /^[ \t]+choices:/ {
      chind = indent($0)
      v = $0; sub(/^[ \t]+choices:[ \t]*/, "", v)
      if (v ~ /^\[/) {
        gsub(/[][]/, "", v); n = split(v, a, ",")
        for (i = 1; i <= n; i++) { x = unq(a[i]); if (x != "") print x }
        exit
      }
      inch = 1
    }
  ' "$2"
}

norm_expr() { # collapse whitespace, prefer single quotes
  local e="$1"
  e="${e//\"/\'}"
  e="$(printf '%s' "$e" | tr -s '[:space:]' ' ')"
  e="${e#"${e%%[![:space:]]*}"}"; e="${e%"${e##*[![:space:]]}"}"
  printf '%s' "$e"
}

# Split a templated list item "<: if COND :>/path<: endif :>" into COND<TAB>path (path without
# its leading slash). Prints nothing for an untemplated item.
split_gated_item() {
  local re='^<:-?[[:space:]]*if[[:space:]]+(.+[^[:space:]-])[[:space:]]*-?:>(.*)<:-?[[:space:]]*endif[[:space:]]*-?:>$'
  if [[ "$1" =~ $re ]]; then
    printf '%s\t%s\n' "$(norm_expr "${BASH_REMATCH[1]}")" "${BASH_REMATCH[2]#/}"
  fi
}

# COND<TAB>path for every templated _exclude entry.
exclude_gates() { # $1 = copier.yml
  local item
  while IFS= read -r item; do
    split_gated_item "$item"
  done < <(yaml_list _exclude "$1")
}

# The SHIPPING gate of an exclusion condition: `not (G)` → G; `A == 'x' or not B` →
# `A != 'x' and B`; `'x' in L` ↔ `'x' not in L` (list membership, DESIGN.md D15). Returns 1
# for a shape it cannot negate textually.
negate_gate() {
  local c out="" atom rest
  c="$(norm_expr "$1")"
  if [[ "$c" =~ ^not\ \(([^()]*)\)$ ]]; then printf '%s' "${BASH_REMATCH[1]}"; return 0; fi
  [[ "$c" == *'('* || "$c" == *' and '* ]] && return 1
  rest="$c"
  while :; do
    if [[ "$rest" == *' or '* ]]; then atom="${rest%% or *}"; rest="${rest#* or }"; else atom="$rest"; rest=""; fi
    if   [[ "$atom" =~ ^(\'[^\']+\')\ not\ in\ ([A-Za-z_][A-Za-z0-9_]*)$ ]]; then atom="${BASH_REMATCH[1]} in ${BASH_REMATCH[2]}"
    elif [[ "$atom" =~ ^(\'[^\']+\')\ in\ ([A-Za-z_][A-Za-z0-9_]*)$ ]];      then atom="${BASH_REMATCH[1]} not in ${BASH_REMATCH[2]}"
    elif [[ "$atom" =~ ^([A-Za-z_][A-Za-z0-9_]*)\ ==\ (.+)$ ]]; then atom="${BASH_REMATCH[1]} != ${BASH_REMATCH[2]}"
    elif [[ "$atom" =~ ^([A-Za-z_][A-Za-z0-9_]*)\ !=\ (.+)$ ]]; then atom="${BASH_REMATCH[1]} == ${BASH_REMATCH[2]}"
    elif [[ "$atom" =~ ^not\ ([A-Za-z_][A-Za-z0-9_]*)$ ]];     then atom="${BASH_REMATCH[1]}"
    elif [[ "$atom" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]];            then atom="not $atom"
    else return 1; fi
    out="${out:+$out and }$atom"
    [[ -z "$rest" ]] && break
  done
  printf '%s' "$out"
}

# ── The DESIGN.md catalogue ──────────────────────────────────────────────────
#
# Gates are written in a small vocabulary so a tree's answers can be tested against them:
#   always · optional · business · fiction · nonfiction · author · seed · p:<platform> ·
#   k:<media kind> · agents · agents-md · gemini-md · cl-<client> — joined with & for "and".
#   p: and k: are list membership in PLATFORMS and MEDIA_KINDS, which are always asked and
#   never empty, so they carry no BRAND_KIND test (DESIGN.md D15). `author` (BRAND_KIND !=
#   'business') is vocabulary only: no Section 3.5 path ships on it, so it is not a shipping
#   gate an index row may use. The last four are the client gates of the family-shared
#   question block (DESIGN.md D80; syntek-author D47), as syntek-author's audits spell them:
#   `agents` is AGENT_CLIENTS | length > 0 (the .agents folder), `agents-md` Codex or OpenCode
#   (AGENTS.md), `gemini-md` Gemini CLI or Antigravity (GEMINI.md), `cl-<client>` one client's
#   own files. AGENT_CLIENTS is always asked and may be empty: a project that ticks none is
#   Claude-only.

SM_KINDS="business author-fiction author-nonfiction"
# The three own-channel platforms joined in 0.2.0 (DESIGN.md D53); the per-kind defaults below
# did not change (D54).
SM_PLATFORMS="youtube tiktok instagram linkedin facebook podcast website blog newsletter"
SM_MEDIA_KINDS="short-video long-video podcast audiobook trailer voiceover"
# AGENT_CLIENTS's values, the family's gate strings (syntek-author D47), never renamed.
SM_CLIENTS="codex gemini-cli antigravity opencode"

declare -A SM_GATE_EXPR=(
  [business]="BRAND_KIND == 'business'"
  [fiction]="BRAND_KIND == 'author-fiction'"
  [nonfiction]="BRAND_KIND == 'author-nonfiction'"
  [author]="BRAND_KIND != 'business'"
)
for _sm_x in $SM_PLATFORMS;   do SM_GATE_EXPR["p:$_sm_x"]="'$_sm_x' in PLATFORMS"; done
for _sm_x in $SM_MEDIA_KINDS; do SM_GATE_EXPR["k:$_sm_x"]="'$_sm_x' in MEDIA_KINDS"; done
for _sm_x in $SM_CLIENTS;     do SM_GATE_EXPR["cl-$_sm_x"]="'$_sm_x' in AGENT_CLIENTS"; done
SM_GATE_EXPR[agents]="AGENT_CLIENTS | length > 0"
SM_GATE_EXPR[agents-md]="'codex' in AGENT_CLIENTS or 'opencode' in AGENT_CLIENTS"
SM_GATE_EXPR[gemini-md]="'gemini-cli' in AGENT_CLIENTS or 'antigravity' in AGENT_CLIENTS"
unset _sm_x

# The shipping gates of DESIGN.md Section 3.5, in the vocabulary: the three mode gates, every
# list-membership gate and the client gates. Index rows may use exactly these
# (check-template-tokens.sh check 9).
SM_SHIPPING_ATOMS="business fiction nonfiction$(for p in $SM_PLATFORMS; do printf ' p:%s' "$p"; done)$(for k in $SM_MEDIA_KINDS; do printf ' k:%s' "$k"; done) agents agents-md gemini-md$(for c in $SM_CLIENTS; do printf ' cl-%s' "$c"; done)"

# Per-kind defaults (DESIGN.md Section 2), as values; and the syntek-author variant each kind
# is applied over (DESIGN.md D4, D28).
declare -A SM_DEFAULT_PLATFORMS=(
  [business]="youtube linkedin instagram"
  [author-fiction]="youtube tiktok instagram facebook"
  [author-nonfiction]="youtube podcast instagram facebook"
)
declare -A SM_DEFAULT_MEDIA_KINDS=(
  [business]="short-video long-video voiceover"
  [author-fiction]="short-video trailer audiobook voiceover"
  [author-nonfiction]="long-video short-video podcast audiobook voiceover"
)
declare -A SM_DEFAULT_MODEL=([business]=opus [author-fiction]=sonnet [author-nonfiction]=sonnet)
declare -A SM_AUTHOR_DOC_TYPE=([business]=business [author-fiction]=fiction [author-nonfiction]=theology)

author_doc_for_kind() { printf '%s' "${SM_AUTHOR_DOC_TYPE[$1]:-}"; }

# Skills (DESIGN.md Section 5.1): name · gate · modes (BFN = BUSINESS+FICTION+NONFICTION, -).
SM_SKILLS=$(cat <<'EOF'
run-media-workflow  always       -
write-script        always       BFN
storyboard          always       BFN
repurpose           always       BFN
thumbnail-brief     always       BFN
prepare-post        always       BFN
voiceover           always       BFN
narrate-audiobook   k:audiobook  BFN
captions            always       -
cut-for-platform    always       -
EOF
)

SM_MODE_FILES="BUSINESS.md FICTION.md NONFICTION.md"

# The family skills (DESIGN.md D80, its own table in Section 5; syntek-author D51): the seven
# working-practice skills whose SKILL.md media vendors byte for byte (SM_FAMILY_SHARED below),
# copy-only, and beside five of them media's own routing-only mode files, MEDIA-BUSINESS.md,
# MEDIA-FICTION.md and MEDIA-NONFICTION.md, gated on BRAND_KIND like every media mode file and
# template-owned. The prefix keeps them apart from syntek-author's own mode files in the same
# folders (BUSINESS.md, FICTION.md, THEOLOGY.md) in a project that takes both. name · gate ·
# modes, as SM_SKILLS. Their SKILL.md keeps the family's H1 (no brand name), locale line (no
# time zone) and neutral Mode paragraph, so skill-conformance.sh checks 8, 9 and 14 never read
# it; and syntek-author ships the same folders by design, so no D27 name check reports them.
# This catalogue gives each family skill its gate and modes only: which skills are family
# skills, and so every exemption, is read from SM_FAMILY_SHARED below (SM_FAMILY_SKILLS). A name
# here that list lacks is judged as a media skill, and a family skill missing here is
# shipped-brands.sh check 3's.
SM_FAMILY_SKILLS_CAT=$(cat <<'EOF'
grill-me          always  -
grill-with-docs   always  BFN
grilling          always  BFN
handoff           always  BFN
to-questionnaire  always  BFN
wait-what         always  -
wayfinder         always  BFN
EOF
)
SM_FAMILY_MODE_FILES="MEDIA-BUSINESS.md MEDIA-FICTION.md MEDIA-NONFICTION.md"
is_family_skill() { [[ " $SM_FAMILY_SKILLS " == *" $1 "* ]]; }   # SM_FAMILY_SKILLS: below

# The skill contract (DESIGN.md Section 5), as skill-conformance.sh compares it. The mode
# paragraph is syntek-author's with the three names swapped, and is compared whitespace- and
# `> `-normalised; the guard sentence is syntek-author's, verbatim, in every skill that names a
# credit-spending ElevenLabs tool (SM_SETTINGS_ASK lists those tools, its mcp__ entries; its two
# Bash entries are the voice remix run asks of D82).
SM_MODE_PARA="**Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of \`BUSINESS.md\`, \`FICTION.md\`, \`NONFICTION.md\` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author."
SM_MODE_H2S="Paths and unit|Additions to the steps|Domain rules|Examples"
SM_GUARD_SENTENCE="If nothing was asked, stop: never generate unasked, including as a 'helpful' extra after another skill."
SM_SKILL_KEYS="name description context agent background model metadata"
SM_SKILL_H1_TOKEN="<%BRAND_NAME%>"
SM_GOVERNING_LINE="## Governing procedures (route here — do not restate at length)"

# The shared MEMORY.md's six headings (DESIGN.md Section 4.1, syntek-author's), and the texts an
# update must print or refuse with (D14, D16; the crash pointer, DESIGN.md Sections 3.5 and 10).
SM_MEMORY_H2S=("Facts" "Decisions" "Feedback" "Status" "Open questions" "Sensitivities")
SM_KIND_REFUSAL="BRAND_KIND cannot change on update"
SM_BEFORE_UPDATE_MARK="Before you answer: removing a platform or a media kind deletes"
SM_BEFORE_UPDATE_CRASH="If this update stops with OSError: [Errno 39] Directory not empty, never commit what it left"
# The pointer's last words. Copier prints its own "Updating to template version X" or "Keeping
# template version X" straight after _message_before_update (9.19.1 _main.py:1389-1390,
# _print_template_update_info), so a message that ends with the pointer is followed by one.
SM_BEFORE_UPDATE_CRASH_END="gives the recovery and the command to use."

mode_for_kind() { # business → BUSINESS.md; $2 = MEDIA- for a family skill's mode file
  case "$1" in business) echo "${2:-}BUSINESS.md" ;; author-fiction) echo "${2:-}FICTION.md" ;; author-nonfiction) echo "${2:-}NONFICTION.md" ;; esac
}
kind_for_mode() { # BUSINESS.md or MEDIA-BUSINESS.md → business
  case "${1#MEDIA-}" in BUSINESS.md) echo business ;; FICTION.md) echo author-fiction ;; NONFICTION.md) echo author-nonfiction ;; esac
}
modes_list() { # BFN → BUSINESS.md FICTION.md NONFICTION.md; $2 = MEDIA- for a family skill
  local out=""
  [[ "$1" == *B* ]] && out+="${2:-}BUSINESS.md "
  [[ "$1" == *F* ]] && out+="${2:-}FICTION.md "
  [[ "$1" == *N* ]] && out+="${2:-}NONFICTION.md "
  printf '%s' "${out% }"
}
mode_prefix() { # skill name → MEDIA- for a family skill, nothing for a media skill
  is_family_skill "$1" && printf 'MEDIA-'
  return 0
}

# Required and gated paths (DESIGN.md Sections 3–4; MANIFEST). Skills and mode files are
# SM_SKILLS's and SM_FAMILY_SKILLS_CAT's; folder pairs are docs-pairing.sh's; a workflow's
# STEPS.md and CHECKLIST.md are docs-pairing.sh check 12's. kind: d = directory, f = file.
# The client files ship only for the clients AGENT_CLIENTS ticks (DESIGN.md D80, Section 3.5;
# syntek-author's seven gate lines); every other family-shared file ships always, the guide
# guard and the user guide's thirteen family files under how-to/ among them since 0.6.0 (D84,
# Section 4.4: how-to/ ships in every render, its folders and their pairs ungated). Media's own
# files under how-to/'s three syntek-media/ folders take rows of their own.
SM_PATHS=$(cat <<'EOF'
always        f  .copier-answers.syntek-media.yml
always        f  README.md
always        f  CONTEXT.md
always        f  .gitignore
always        f  .mcp.json
always        f  .claude/CLAUDE.md
always        f  .claude/CONTEXT.md
always        f  .claude/MEMORY.md
always        f  .claude/settings.json
always        f  .claude/skills/CONTEXT.md
always        f  .claude/skills/CLAUDE.md
agents-md     f  AGENTS.md
gemini-md     f  GEMINI.md
agents        d  .agents
agents        d  .agents/skills
cl-antigravity f  .agents/mcp_config.json
cl-codex      f  .codex/config.toml
cl-codex      f  .codex/CONTEXT.md
cl-codex      f  .codex/CLAUDE.md
cl-gemini-cli f  .gemini/settings.json
cl-gemini-cli f  .gemini/CONTEXT.md
cl-gemini-cli f  .gemini/CLAUDE.md
cl-opencode   f  opencode.json
always        f  .claude/syntek-media-agents.md
always        f  .claude/syntek-media-dataroot.py
always        f  .claude/syntek-media-permissions.py
always        f  .claude/syntek-media-dataroot.json
always        d  .claude/hooks
always        f  .claude/hooks/CONTEXT.md
always        f  .claude/hooks/CLAUDE.md
always        f  .claude/hooks/context-threshold-handoff.sh
always        f  .claude/hooks/how-to-read-only.sh
always        f  .claude/hooks/pre-compact-handoff.sh
always        d  handoffs
always        f  handoffs/CONTEXT.md
always        f  handoffs/CLAUDE.md
always        d  how-to
always        f  how-to/CONTEXT.md
always        f  how-to/CLAUDE.md
always        d  how-to/docs
always        f  how-to/docs/CONTEXT.md
always        f  how-to/docs/CLAUDE.md
always        d  how-to/src
always        f  how-to/src/CONTEXT.md
always        f  how-to/src/CLAUDE.md
always        d  how-to/src/TEMPLATE-GUIDE
always        f  how-to/src/TEMPLATE-GUIDE/CONTEXT.md
always        f  how-to/src/TEMPLATE-GUIDE/CLAUDE.md
always        f  how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md
always        f  how-to/src/TEMPLATE-GUIDE/the-data-root.md
always        f  how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md
always        d  how-to/workflows
always        f  how-to/workflows/CONTEXT.md
always        f  how-to/workflows/CLAUDE.md
always        f  .claude/rules/syntek-media/01-layout-and-routing.md
always        f  .claude/rules/syntek-media/02-skills.md
always        f  .claude/rules/syntek-media/03-production-ethics.md
always        f  .claude/rules/syntek-media/04-toolkit-pipeline.md
always        f  .claude/rules/syntek-media/05-model-allocation.md
always        f  .claude/rules/syntek-media/06-global-rules.md
always        f  .claude/rules/syntek-media/07-session-boundaries.md
always        f  .claude/rules/syntek-media/08-naming-and-memory.md
always        d  brand/docs/reference
always        d  brand/docs/project
always        d  brand/src
always        d  brand/workflows/local
always        f  brand/docs/reference/the-brand-kit.md
always        f  brand/docs/reference/claude-design.md
always        f  brand/docs/reference/design-exports.md
always        f  brand/docs/reference/the-spoken-voice.md
always        f  brand/docs/reference/platform-profiles.md
always        f  brand/src/design-register.md
always        d  brand/src/design-system
always        f  brand/src/design-system/tokens.css
always        d  brand/src/design-system/previews
always        f  brand/src/design-system/previews/colors.html
always        f  brand/src/design-system/previews/type.html
always        f  brand/src/design-system/previews/spacing.html
always        f  brand/src/design-system/previews/brand.html
always        f  brand/src/design-system/previews/captions.html
always        f  brand/src/design-system/previews/thumbnail.html
always        f  brand/src/design-system/previews/card.html
always        d  brand/src/design-system/fonts
always        d  brand/src/exports
always        d  brand/src/exports/large
always        f  brand/src/exports/large/.gitattributes
always        d  brand/src/voice
always        f  brand/src/voice/voice.md
always        d  brand/src/platforms
p:youtube     f  brand/src/platforms/youtube.md
p:tiktok      f  brand/src/platforms/tiktok.md
p:instagram   f  brand/src/platforms/instagram.md
p:linkedin    f  brand/src/platforms/linkedin.md
p:facebook    f  brand/src/platforms/facebook.md
p:podcast     f  brand/src/platforms/podcast.md
p:website     f  brand/src/platforms/website.md
p:blog        f  brand/src/platforms/blog.md
p:newsletter  f  brand/src/platforms/newsletter.md
always        f  brand/src/platforms/overrides.toml
always        d  brand/workflows/01-set-up-the-brand-kit
always        d  brand/workflows/02-sync-with-claude-design
always        d  brand/workflows/03-record-a-design-export
always        d  brand/workflows/04-set-up-a-platform
always        d  brand/workflows/05-write-the-spoken-voice
always        d  brand/workflows/06-check-the-setup
always        d  scripts/docs/reference
always        d  scripts/docs/project
always        d  scripts/src
always        d  scripts/workflows/local
always        f  scripts/docs/reference/the-piece-ladder.md
always        f  scripts/docs/reference/writing-for-the-ear.md
always        f  scripts/docs/reference/storyboards-and-shot-lists.md
k:short-video f  scripts/docs/reference/short-video.md
k:long-video  f  scripts/docs/reference/long-video.md
k:podcast     f  scripts/docs/reference/podcast-episodes.md
k:trailer     f  scripts/docs/reference/trailers.md
k:voiceover   f  scripts/docs/reference/standalone-voiceovers.md
always        f  scripts/src/piece-register.md
always        d  scripts/src/pieces
always        d  scripts/workflows/01-brief-a-piece
always        d  scripts/workflows/02-write-a-script
always        d  scripts/workflows/03-storyboard-a-piece
always        d  production/docs/reference
always        d  production/docs/project
always        d  production/src
always        d  production/workflows/local
always        f  production/docs/reference/source-media.md
always        f  production/docs/reference/edit-decision-lists.md
always        f  production/docs/reference/sound-and-loudness.md
always        f  production/docs/reference/rights-and-consent.md
always        f  production/docs/reference/elevenlabs.md
always        f  production/docs/reference/voiceover.md
always        f  production/docs/reference/recorded-pieces.md
always        f  production/docs/reference/scenes-as-code.md
always        f  production/docs/reference/character-voices.md
k:audiobook   f  production/docs/reference/audiobook-narration.md
always        f  production/src/.gitignore
always        f  production/src/rights-register.md
always        f  production/src/credits-log.md
always        f  production/src/renders/README.md
always        d  production/src/footage
always        f  production/src/footage/manifest.toml
always        f  production/src/footage/raw/README.md
always        d  production/src/assets
always        d  production/src/edits
always        d  production/src/cards
always        d  production/src/voiceover
always        f  production/src/voiceover/generated/README.md
always        d  production/src/timing
always        d  production/src/scenes
k:audiobook   d  production/src/audiobook
k:audiobook   f  production/src/audiobook/generated/README.md
k:audiobook   f  production/src/audiobook/renders/README.md
always        d  production/workflows/01-log-source-media
always        d  production/workflows/02-make-a-voiceover
always        d  production/workflows/03-assemble-the-master
k:podcast     d  production/workflows/04-master-a-podcast-episode
k:audiobook   d  production/workflows/05-narrate-an-audiobook
k:audiobook   d  production/workflows/06-master-an-audiobook
always        d  production/workflows/07-clear-the-rights
always        d  production/workflows/08-bring-in-a-recording
always        d  production/workflows/09-time-the-voice
always        d  production/workflows/10-animate-a-scene
always        d  production/workflows/11-design-character-voices
always        d  publishing/docs/reference
always        d  publishing/docs/project
always        d  publishing/src
always        d  publishing/workflows/local
always        f  publishing/docs/reference/cut-downs.md
always        f  publishing/docs/reference/captions.md
always        f  publishing/docs/reference/thumbnails.md
always        f  publishing/docs/reference/scoring-options.md
always        f  publishing/docs/reference/ai-disclosure.md
always        f  publishing/docs/reference/posting-and-the-log.md
always        f  publishing/docs/reference/platform-specs.md
p:youtube     f  publishing/docs/reference/youtube.md
p:tiktok      f  publishing/docs/reference/tiktok.md
p:instagram   f  publishing/docs/reference/instagram.md
p:linkedin    f  publishing/docs/reference/linkedin.md
p:facebook    f  publishing/docs/reference/facebook.md
p:podcast     f  publishing/docs/reference/podcast.md
p:podcast     f  publishing/docs/reference/podcast-feed.md
p:website     f  publishing/docs/reference/website.md
p:blog        f  publishing/docs/reference/blog.md
p:newsletter  f  publishing/docs/reference/newsletter.md
always        f  publishing/src/.gitignore
always        f  publishing/src/schedule.md
always        f  publishing/src/publish-log.md
always        f  publishing/src/renders/README.md
always        d  publishing/src/cut-downs
always        d  publishing/src/captions
always        d  publishing/src/thumbnails
always        d  publishing/src/posts
p:podcast     d  publishing/src/podcast
always        d  publishing/workflows/01-plan-the-cut-downs
always        d  publishing/workflows/02-cut-for-a-platform
always        d  publishing/workflows/03-caption-a-piece
always        d  publishing/workflows/04-brief-a-thumbnail
always        d  publishing/workflows/05-prepare-a-post
always        d  publishing/workflows/06-record-a-publication
always        d  publishing/workflows/07-refresh-the-platform-specs
p:podcast     d  publishing/workflows/08-publish-the-podcast-feed
always        f  toolkit/.gitignore
always        f  toolkit/media.py
always        f  toolkit/media_common.py
always        f  toolkit/media_video.py
always        f  toolkit/media_audio.py
always        f  toolkit/media_captions.py
always        f  toolkit/media_repo.py
always        f  toolkit/media_image.py
always        f  toolkit/media_feed.py
always        f  toolkit/media_score.py
always        f  toolkit/media_voice.py
always        f  toolkit/card.py
always        f  toolkit/transcribe.py
always        f  toolkit/data/platforms.toml
always        f  toolkit/data/packaging-score.toml
always        f  toolkit/templates/thumbnail.html
always        f  toolkit/templates/card.html
seed          d  scripts/src/pieces/000-example-piece
seed          f  production/src/edits/000-example-piece.toml
seed          f  production/src/cards/000-example-piece.title.html
seed          f  publishing/src/cut-downs/000-example-piece.md
seed          f  publishing/src/captions/000-example-piece.en-GB.srt
seed          f  publishing/src/thumbnails/000-example-piece.md
seed          f  publishing/src/thumbnails/000-example-piece.html
seed          f  publishing/src/posts/000-example-piece.md
EOF
)

# The four media layers (DESIGN.md D8): the only places a numbered media workflow may sit.
SM_LAYERS="brand scripts production publishing"

# Paths that must never reach a generated project: the template repository's own state, the
# retired agent and command tiers (D6), the root files no template seeds (Section 9), and the
# four community files at the root (D83; the three in .github/ are covered by .github).
SM_NEVER="copier.yml DESIGN.md CHANGELOG.md VERSION examples template .copier-answers.yml .github .claude/agents .claude/commands CLAUDE.md .gitattributes LICENSE CONTRIBUTING.md SECURITY.md CODE_OF_CONDUCT.md"

# The community files (DESIGN.md D83): what GitHub shows a visitor and a contributor, at the
# repository root and in .github/ only, never shipped (_subdirectory: template). Each family
# repository writes its own. community-files.sh checks every one; SM_NEVER above lists the four
# at the root, so shipped-brands.sh check 8 proves no standalone render carries one.
SM_COMMUNITY_FILES="LICENSE CONTRIBUTING.md SECURITY.md CODE_OF_CONDUCT.md .github/CODEOWNERS .github/PULL_REQUEST_TEMPLATE.md .github/ISSUE_TEMPLATE/bug_report.yml .github/ISSUE_TEMPLATE/template_improvement.yml .github/ISSUE_TEMPLATE/config.yml"
# The one route for a security report (D83): this repository's GitHub private vulnerability
# reporting, switched on 20/10/2026. config.yml links it (community-files.sh check 4), and
# SECURITY.md names it (check 6).
SM_PRIVATE_REPORT_URL="https://github.com/Syntek-Dev/syntek-media/security/advisories/new"

# syntek-author's paths, which a standalone media render never ships (DESIGN.md Section 9,
# "Media never ships"). Its skill folders are added from syntek-author-names.txt, less the seven
# family skills (SM_FAMILY_SKILLS). Since D80 media ships the family's .claude/hooks/ (its pair
# and the two session hooks) and the handoffs/ pair, so neither is syntek-author's alone.
SM_AUTHOR_NEVER="Makefile .claude/rules/syntek-author learning assets build manuscript library planning research proposal typeset world standards tooling"

# The first segments of syntek-author's paths, and its two named files, that media never
# backticks (doc-references.sh check 6). handoffs/ ships in media since D80, so it is not one,
# and how-to/ is the family's shared folder since D84, so it is never a head: only
# syntek-author's guide folders under it are its own (SM_AUTHOR_PATH_GLOBS).
SM_AUTHOR_PATH_HEADS="standards manuscript library planning research proposal typeset world tooling learning assets"
SM_AUTHOR_PATH_PREFIXES=".claude/rules/syntek-author"
SM_AUTHOR_FILE_NAMES="Makefile 00-project.md"
# syntek-author's guide folders (DESIGN.md D84, Section 7; syntek-author D56): a folder named
# syntek-author at any depth under how-to/ (how-to/docs/syntek-author/,
# how-to/src/TEMPLATE-GUIDE/syntek-author/, how-to/workflows/syntek-author/) and everything
# under it. A bash pattern, never a path: match it unquoted on the right of [[ == ]], and never
# expand it unquoted in a word list, where the shell would glob it.
SM_AUTHOR_PATH_GLOBS='how-to/*/syntek-author'

# The copy-only shared paths (DESIGN.md D11, D73, D76, D80, D84, Section 3.6): each has an
# anchored _skip_if_exists line and an update-gated _exclude line, for ever. The first nineteen are
# D11's own; eighteen of them ship on copy: the .agents folder (whose own two lines cover the
# folder: without them an update recreates an empty .agents/ where the author removed it, and
# fails on a dangling link there) and its two entries among them. SM_SHARED_RETIRED keeps its
# two lines but no longer ships on copy: a third, unconditional _exclude line takes it out
# (D76), and the file stays under template/ (D11). The next seventeen arrived with D80, file by
# file, as syntek-author lists them (never a folder: the family skill folders also hold
# media's template-owned MEDIA-*.md mode files): Gemini CLI's pair and settings and OpenCode's
# file (syntek-author D47), then the family's working practice (syntek-author D51), the seven
# skills, the two session hooks with the .claude/hooks/ pair, and the handoffs/ pair. All are
# family-shared bytes (SM_FAMILY_SHARED); the client files among them also carry a client gate.
# The last fourteen arrived with D84 (0.6.0), file by file as syntek-author's copier.yml holds
# them (syntek-author D56): the guide guard, then the five container pairs of how-to/ and its
# three shared chapters. Never /how-to or a folder under it: every how-to folder also holds
# media's template-owned files under its three syntek-media/ folders. Fifty paths, forty-nine
# shipped; through SM_SHARED_SHIPPED they join SM_AFTER_COPY_LINES below.
SM_SHARED="README.md CONTEXT.md .gitignore .mcp.json .claude/CLAUDE.md .claude/CONTEXT.md .claude/MEMORY.md .claude/settings.json .claude/skills/CONTEXT.md .claude/skills/CLAUDE.md AGENTS.md GEMINI.md .agents .codex/config.toml .codex/CONTEXT.md .codex/CLAUDE.md .claude/mcp_config.json .agents/skills .agents/mcp_config.json .gemini/settings.json .gemini/CONTEXT.md .gemini/CLAUDE.md opencode.json .claude/skills/grill-me/SKILL.md .claude/skills/grill-with-docs/SKILL.md .claude/skills/grilling/SKILL.md .claude/skills/handoff/SKILL.md .claude/skills/to-questionnaire/SKILL.md .claude/skills/wait-what/SKILL.md .claude/skills/wayfinder/SKILL.md .claude/hooks/pre-compact-handoff.sh .claude/hooks/context-threshold-handoff.sh .claude/hooks/CONTEXT.md .claude/hooks/CLAUDE.md handoffs/CONTEXT.md handoffs/CLAUDE.md .claude/hooks/how-to-read-only.sh how-to/CONTEXT.md how-to/CLAUDE.md how-to/docs/CONTEXT.md how-to/docs/CLAUDE.md how-to/src/CONTEXT.md how-to/src/CLAUDE.md how-to/src/TEMPLATE-GUIDE/CONTEXT.md how-to/src/TEMPLATE-GUIDE/CLAUDE.md how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md how-to/src/TEMPLATE-GUIDE/the-data-root.md how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md how-to/workflows/CONTEXT.md how-to/workflows/CLAUDE.md"
SM_SHARED_RETIRED=".claude/mcp_config.json"
# The two client folders that take an update gate of their own and no _skip_if_exists line, as
# syntek-author's copier.yml writes them (D80): Copier creates an EMPTY folder on an update that
# crosses the release which introduced it, even where every path inside it is excluded.
# shipped-seeds.sh check 8 accepts exactly these beside the shared paths.
SM_SHARED_DIRS=".codex .gemini"
SM_SHARED_SHIPPED="$(for _sm_x in $SM_SHARED; do [[ " $SM_SHARED_RETIRED " == *" $_sm_x "* ]] || printf '%s ' "$_sm_x"; done)"
SM_SHARED_SHIPPED="${SM_SHARED_SHIPPED% }"
SM_SHARED_GATE="_copier_operation == 'update'"
# The D76 agent folder: a real .agents/ whose skills entry is this exact relative link, so one
# skill tree serves every client and Codex can mount .agents read-only (D76).
SM_AGENTS_SKILLS_LINK="../.claude/skills"
# The first migration (DESIGN.md D76): run by an update that crosses v0.4.2.
SM_D76_MIGRATION="migrations/v0.4.2-agents-folder.py"
SM_D76_VERSION="v0.4.2"
# D76's outside-link pair, D11's second, transient exception: the only migrations keyed to no
# release. hold (before the render) renames an .agents link that leaves the project to
# SM_OUTSIDE_HELD and prints the hand fix, SM_OUTSIDE_CHECK its first step and SM_OUTSIDE_FIX
# its last; restore (after, declared before the v0.4.2 entry) renames it back.
SM_OUTSIDE_MIGRATION="migrations/agents-outside-link.py"
SM_OUTSIDE_HELD=".agents.syntek-held"
SM_OUTSIDE_FIX="mv $SM_OUTSIDE_HELD .agents"
SM_OUTSIDE_CHECK="ls -ld .agents $SM_OUTSIDE_HELD"
# D85: the script is syntek-author's family-shared copy (syntek-author D48), vendored byte for
# byte from one syntek-author release tag and never edited here. Since D80 its sha256 and mode
# are read from this repository's own family-shared.json (SM_FAMILY_SHARED below), never
# transcribed here; shipped-seeds.sh check 21 holds the script to that entry.
# update-test.sh check 23 tags a clone of its snapshot with this release, whose copier.yml alone
# carries a failing after-stage entry above restore: a stop after the render.
SM_CRASH_VERSION="v0.4.3"

# ── The family-shared set (DESIGN.md D80, D81, D84, D85; syntek-author D48–D56) ──
#
# What media vendors byte for byte from ONE syntek-author release tag and never edits here: the
# client files, the .agents/ folder's two entries, the MCP declarations, the working-practice
# skills, hooks and handoffs pair, the guide guard and the user guide's thirteen family files
# under how-to/ (D84), the data-root resolver and the permissions script under media's names,
# the outside-link migration and the update script (both of repository scope), and four
# blocks: the 'questions', 'migrations' and 'update' blocks of copier.yml and the
# 'rules-web-tools' block of rules 06. Since 0.6.0 that is forty-three files and four blocks,
# every entry of the tag's own manifest (D81). This repository's root family-shared.json
# records each in the family's own format (format 1, owner syntek-media, release v + VERSION or
# unreleased, each file's source, bytes, sha256 and mode, each link's target, each block's
# markers, bytes and sha256, and rules-web-tools's destination), so that syntek-author's
# family-shared.sh --sibling can compare it and media's audits can read it: shipped-seeds.sh
# checks 21–27 hold the files and blocks to it, and coexist-test.sh check 22 holds it to the
# --author tree's own manifest. Nothing here transcribes a hash.
#
# SM_FAMILY_RELEASE is the syntek-author tag the set comes from: the tag CI pins as
# SYNTEK_AUTHOR_TAG, re-vendored whole at each adoption (D85: one tag for every family file).
# SM_FAMILY_DEFERRED names any entry of syntek-author's manifest media has not yet adopted, so
# coexist-test.sh check 22 can tell one from a family file media has never heard of. Since
# D81 (0.6.0) it is empty: media vendors every file and block the tag lists, so a family file
# a later tag adds fails check 22 until it is adopted.
SM_FAMILY_RELEASE="v0.7.0"
SM_FAMILY_MANIFEST="family-shared.json"
SM_FAMILY_OWNER="syntek-media"
# destination path · source in this repository · scope (blank: project, under template/). The
# destination is the family's, `<template>` its literal placeholder for each template's name;
# listed in byte order of the destination, as the manifest lists them.
SM_FAMILY_SHARED=$(cat <<'EOF'
.agents/mcp_config.json                     template/.agents/mcp_config.json
.agents/skills                              template/.agents/skills
.claude/hooks/CLAUDE.md                     template/.claude/hooks/CLAUDE.md
.claude/hooks/CONTEXT.md                    template/.claude/hooks/CONTEXT.md
.claude/hooks/context-threshold-handoff.sh  template/.claude/hooks/context-threshold-handoff.sh
.claude/hooks/how-to-read-only.sh           template/.claude/hooks/how-to-read-only.sh
.claude/hooks/pre-compact-handoff.sh        template/.claude/hooks/pre-compact-handoff.sh
.claude/skills/grill-me/SKILL.md            template/.claude/skills/grill-me/SKILL.md
.claude/skills/grill-with-docs/SKILL.md     template/.claude/skills/grill-with-docs/SKILL.md
.claude/skills/grilling/SKILL.md            template/.claude/skills/grilling/SKILL.md
.claude/skills/handoff/SKILL.md             template/.claude/skills/handoff/SKILL.md
.claude/skills/to-questionnaire/SKILL.md    template/.claude/skills/to-questionnaire/SKILL.md
.claude/skills/wait-what/SKILL.md           template/.claude/skills/wait-what/SKILL.md
.claude/skills/wayfinder/SKILL.md           template/.claude/skills/wayfinder/SKILL.md
.claude/syntek-<template>-dataroot.py       template/.claude/syntek-media-dataroot.py
.claude/syntek-<template>-permissions.py    template/.claude/syntek-media-permissions.py
.codex/CLAUDE.md                            template/.codex/CLAUDE.md
.codex/CONTEXT.md                           template/.codex/CONTEXT.md
.codex/config.toml                          template/.codex/config.toml
.gemini/CLAUDE.md                           template/.gemini/CLAUDE.md
.gemini/CONTEXT.md                          template/.gemini/CONTEXT.md
.gemini/settings.json                       template/.gemini/settings.json
.mcp.json                                   template/.mcp.json
AGENTS.md                                   template/AGENTS.md
GEMINI.md                                   template/GEMINI.md
handoffs/CLAUDE.md                          template/handoffs/CLAUDE.md
handoffs/CONTEXT.md                         template/handoffs/CONTEXT.md
how-to/CLAUDE.md                                    template/how-to/CLAUDE.md
how-to/CONTEXT.md                                   template/how-to/CONTEXT.md
how-to/docs/CLAUDE.md                               template/how-to/docs/CLAUDE.md
how-to/docs/CONTEXT.md                              template/how-to/docs/CONTEXT.md
how-to/src/CLAUDE.md                                template/how-to/src/CLAUDE.md
how-to/src/CONTEXT.md                               template/how-to/src/CONTEXT.md
how-to/src/TEMPLATE-GUIDE/CLAUDE.md                 template/how-to/src/TEMPLATE-GUIDE/CLAUDE.md
how-to/src/TEMPLATE-GUIDE/CONTEXT.md                template/how-to/src/TEMPLATE-GUIDE/CONTEXT.md
how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md  template/how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md
how-to/src/TEMPLATE-GUIDE/the-data-root.md          template/how-to/src/TEMPLATE-GUIDE/the-data-root.md
how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md  template/how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md
how-to/workflows/CLAUDE.md                          template/how-to/workflows/CLAUDE.md
how-to/workflows/CONTEXT.md                         template/how-to/workflows/CONTEXT.md
migrations/agents-outside-link.py           migrations/agents-outside-link.py            repository
migrations/family-update.py                 migrations/family-update.py                  repository
opencode.json                               template/opencode.json
EOF
)
SM_FAMILY_LINKS=".agents/skills"
# The family skills, read from that one list: each .claude/skills/<name>/SKILL.md it holds. Every
# exemption a family skill takes (D27's names, the forms skill-conformance.sh checks 8, 9 and 14
# leave unread, shipped-brands.sh checks 3 and 5) reads this, never a list of its own.
SM_FAMILY_SKILLS="$(awk '$1 ~ /^[.]claude[/]skills[/][^/]+[/]SKILL[.]md$/ { split($1, a, "/"); printf "%s%s", (n++ ? " " : ""), a[3] }' <<< "$SM_FAMILY_SHARED")"
# name|source|destination (blank: copier.yml's own block)|BEGIN marker|END marker, in manifest
# order. The marker lines are syntek-author's, byte for byte: their D48 is its decision. The
# 'update' block (D81) closes copier.yml's _migrations; shipped-seeds.sh check 20 holds its place.
SM_FAMILY_BLOCKS=$(cat <<'EOF'
questions|copier.yml||# BEGIN family-shared questions (D48)|# END family-shared questions (D48)
migrations|copier.yml||# BEGIN family-shared migrations (D48)|# END family-shared migrations (D48)
update|copier.yml||# BEGIN family-shared update (D48)|# END family-shared update (D48)
rules-web-tools|template/.claude/rules/syntek-media/06-global-rules.md|.claude/rules/syntek-<template>/06-global-rules.md|<!-- BEGIN family-shared rules: web and code tools -->|<!-- END family-shared rules: web and code tools -->
EOF
)
# syntek-author's entries media takes later: file paths, then `block:<name>`. Empty since D81
# (0.6.0), which vendors every entry of v0.7.0's manifest; kept, so a later adoption can defer.
SM_FAMILY_DEFERRED=""
# The family files that are template-owned in every family template (syntek-author D49, D50):
# updated by every update, so they take no _skip_if_exists or update-gated line. Every other
# project-scope family file is copy-only (SM_SHARED).
SM_FAMILY_TEMPLATE_OWNED=".claude/syntek-media-dataroot.py .claude/syntek-media-permissions.py"
# The three family files that carry the seven shared keys (AGENT_CLIENTS, the model answers):
# Copier renders them, so a render's bytes differ from the source's by design. Every other
# project-scope family file holds no delimiter and renders to its own bytes.
SM_FAMILY_RENDERED=".codex/config.toml .gemini/settings.json opencode.json"
# Media's own data-root map (D80): template-owned, not family-shared (each template writes its
# own), and empty in 0.5.0: media files nothing on the data root yet (shipped-seeds.sh check 28).
SM_DATAROOT_MAP=".claude/syntek-media-dataroot.json"

# The project-scope family paths under media's name, one per line: what a render holds.
SM_FAMILY_PATHS="$(awk 'NF && $3 != "repository" { p = $1; sub(/<template>/, "media", p); print p }' <<< "$SM_FAMILY_SHARED" | paste -sd' ' -)"
is_family_path() { [[ " $SM_FAMILY_PATHS " == *" $1 "* ]]; }
# A top-level entry, or a .claude/ entry, that a family path passes through or ends in: both
# templates write there by design, so no D27 name check reports it (shipped-brands.sh check 11,
# coexist-test.sh check 13).
is_family_entry() { # $1 = a top-level entry, or .claude/<entry>
  local p
  for p in $SM_FAMILY_PATHS; do
    [[ "$p" == "$1" || "$p" == "$1"/* ]] && return 0
  done
  return 1
}

# Seeds (DESIGN.md Section 3.1): twenty-six, then the sixteen author-filled index-pair files.
SM_REGISTER_SEEDS="brand/src/design-register.md scripts/src/piece-register.md production/src/rights-register.md production/src/credits-log.md publishing/src/schedule.md publishing/src/publish-log.md"
SM_TOML_SEEDS="brand/src/platforms/overrides.toml production/src/footage/manifest.toml"
SM_PLATFORM_SEEDS="$(for p in $SM_PLATFORMS; do printf 'brand/src/platforms/%s.md ' "$p"; done)"
SM_PLATFORM_SEEDS="${SM_PLATFORM_SEEDS% }"
SM_PREVIEW_SEEDS="$(for c in colors type spacing brand captions thumbnail card; do printf 'brand/src/design-system/previews/%s.html ' "$c"; done)"
SM_PREVIEW_SEEDS="${SM_PREVIEW_SEEDS% }"
SM_BRAND_SEEDS="brand/src/design-system/tokens.css brand/src/design-system/previews/thumbnail.html brand/src/design-system/previews/card.html brand/src/voice/voice.md $SM_PLATFORM_SEEDS"
SM_INDEX_SEEDS="$(for l in $SM_LAYERS; do for d in docs/project workflows/local; do printf '%s/%s/CONTEXT.md %s/%s/CLAUDE.md ' "$l" "$d" "$l" "$d"; done; done)"
SM_INDEX_SEEDS="${SM_INDEX_SEEDS% }"
SM_SEEDS="$SM_REGISTER_SEEDS $SM_TOML_SEEDS brand/src/design-system/tokens.css $SM_PREVIEW_SEEDS brand/src/voice/voice.md $SM_PLATFORM_SEEDS $SM_INDEX_SEEDS"

# Seed-once examples (DESIGN.md Section 3.2, D43): eight _exclude lines.
SM_EXAMPLES="scripts/src/pieces/000-example-piece production/src/edits/000-example-piece.toml production/src/cards/000-example-piece.title.html publishing/src/cut-downs/000-example-piece.md publishing/src/captions/000-example-piece.en-GB.srt publishing/src/thumbnails/000-example-piece.md publishing/src/thumbnails/000-example-piece.html publishing/src/posts/000-example-piece.md"
SM_EXAMPLE_GATE="_copier_operation == 'update' or not SEED_EXAMPLES"
SM_EXAMPLE_NAME="000-example-piece"

# The root spine (DESIGN.md Section 2, Token discipline). The copy-only shared paths, the seeds and
# the examples are spine through their own sets; index files are computed.
SM_ROOT_SPINE="$SM_ANSWERS_FILE"
SM_ROOT_SPINE_GLOBS=".claude/rules/syntek-media/*.md"

# Tokens that may appear anywhere (DESIGN.md Section 2): identity and locale.
SM_IDENTITY_TOKENS="BRAND_NAME BRAND_SLUG OWNER_NAME OWNER_FIRST_NAME DATE TIMEZONE"
SM_COPIER_VARS="_copier_operation _copier_answers _copier_conf"

# syntek-author's skills media names in prose and never ships (DESIGN.md D10, Section 5.2).
# grilling, grill-with-docs, handoff and wayfinder left the list with D80: they ship in media
# as family skills (SM_FAMILY_SKILLS), so a media file names them as skills of its own.
SM_COMPANIONS="spelling grammar comprehension flow fact-check improve-section adapt-section research social-media-documents run-workflow pronounce character-voice"

# The standalone settings seed (DESIGN.md D13). Arrays: the entries carry spaces. The deny list
# ends, since 0.6.0, with the guide's one anchored Edit rule (D84; syntek-author D56), after
# media's three and before the family's embed_graph_tool deny, as the seed orders them.
SM_SETTINGS_DENY=("AskUserQuestion" "Edit(**/generated/**)" "Edit(**/renders/**)" "Edit(/how-to/**)")
SM_SETTINGS_ALLOW=("Bash(python3 toolkit/*.py *)" "Bash(uv run toolkit/*.py *)" "Bash(ffmpeg *)" "Bash(ffprobe *)" "WebSearch" "WebFetch")
SM_SETTINGS_ASK=(
  "mcp__elevenlabs__text_to_speech"
  "mcp__elevenlabs__speech_to_text"
  "mcp__elevenlabs__compose_music"
  "mcp__elevenlabs__text_to_sound_effects"
  "mcp__elevenlabs__speech_to_speech"
  "mcp__elevenlabs__voice_clone"
  "mcp__elevenlabs__isolate_audio"
  "mcp__elevenlabs__text_to_voice"
  "mcp__elevenlabs__create_voice_from_preview"
  "Bash(python3 toolkit/media.py voice remix run *)"
  "Bash(uv run toolkit/media.py voice remix run *)"
)
SM_SETTINGS_BANNED_KEYS="effortLevel ultracode enabledPlugins"   # and every disable* key
# The seed's top-level values (DESIGN.md D13, D35; syntek-author D29): key=JSON value, each the
# same in syntek-author's seed. idleCompaction joined autoCompactEnabled in 0.6.0 (D81).
SM_SETTINGS_TOP=("autoCompactEnabled=false" "idleCompaction=false")
# The family's rules in the same seed (DESIGN.md D13 as D80 amends it; syntek-author D54), after
# media's own: the eight MCP asks in the family's order (Scrapling's six browser tools, then
# code-review-graph's two that write), and the deny on embed_graph_tool, which --tools already
# withholds. Kept apart from media's lists: skill-conformance.sh check 21 reads SM_SETTINGS_ASK's
# mcp__ entries as ElevenLabs calls, and these spend no credits.
SM_SETTINGS_FAMILY_ASK=(
  "mcp__scrapling__stealthy_fetch"
  "mcp__scrapling__bulk_stealthy_fetch"
  "mcp__scrapling__open_session"
  "mcp__scrapling__session_fetch"
  "mcp__scrapling__fetch"
  "mcp__scrapling__bulk_fetch"
  "mcp__code-review-graph__apply_refactor_tool"
  "mcp__code-review-graph__generate_wiki_tool"
)
SM_SETTINGS_FAMILY_DENY=("mcp__code-review-graph__embed_graph_tool")
# The seed's hooks key: syntek-author's seed's hooks object, byte for byte as JSON, at
# SM_FAMILY_RELEASE (D80; since 0.6.0 its v0.7.0, D81, D84): four handoff-hook entries in the
# silent `|| exit 0` form, the context-threshold handoff on UserPromptSubmit, the pre-compact
# handoff on PreCompact (auto and manual) and on SessionStart (compact, `compacted`); then two
# PreToolUse entries, the data-root guard and the guide guard (how-to-read-only.sh). Each finds
# its script from the repository root at run time and does nothing where the script is absent.
# Compared as parsed JSON by shipped-seeds.sh check 12, and with the --author tree's seed by
# coexist-test.sh check 22.
SM_SETTINGS_HOOKS=$(cat <<'EOF'
{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/context-threshold-handoff.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/context-threshold-handoff.sh\"'","timeout":10}]}],"PreCompact":[{"matcher":"auto","hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" auto'","timeout":10}]},{"matcher":"manual","hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" manual'","timeout":10}]}],"SessionStart":[{"matcher":"compact","hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" compacted'","timeout":10}]}],"PreToolUse":[{"matcher":"Edit|Write|MultiEdit|NotebookEdit|Grep|Glob","hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; for f in \"$ROOT\"/.claude/syntek-*-dataroot.py; do [ -f \"$f\" ] && exec python3 \"$f\" guard; done; exit 0'","timeout":10}]},{"matcher":"Edit|Write|MultiEdit|NotebookEdit","hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/how-to-read-only.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/how-to-read-only.sh\"'","timeout":10}]}]}
EOF
)

# What _message_after_copy must say, in DESIGN.md D13's order: (1) every shipped shared path
# (the eighteen of D11, the seventeen of D80 and, since 0.6.0, the fourteen of D84) and the
# skip rule, that Copier's 'conflict' then 'skip' pair is expected, and Section 8's hand edits
# 2 and 3 (the optional line in .claude/CLAUDE.md; nothing to add to .gitignore or .mcp.json);
# (2) what to add by hand to a settings.json the copy skipped (DESIGN.md Section 8), as the
# 0.6.0 paragraph below gives it, then the permissions script's --write, which carries the
# seed's ask and deny rules to the other clients' files (D80; syntek-author D49); (3) the user-scope
# `claude mcp add` line with ELEVENLABS_MCP_BASE_PATH; (4) the repository-local
# filter.lfs.required and `git lfs install`; (5) the setup check; (6) the update command with
# -a, run as `uvx --python '>=3.14' copier` since 0.6.0 (D3, D81), with Git's housekeeping off
# (DESIGN.md Section 10). Since 0.5.0 (D13, D80) item 2 also gives the family's eight asks and
# its deny, from the same lists shipped-seeds.sh check 12 holds the seed to, and the seed's
# "hooks" object with its PreToolUse data-root guard, for a settings.json that syntek-author
# did not seed; since 0.6.0 also "idleCompaction": false and the SessionStart entry. Item 1's
# 0.5.0 sentence on coding-agent answers went with D81: the family questions block now takes
# syntek-author's recorded clients itself. Since 0.6.0 (D81) item 2 gives the six allows by
# hand, which no lane offers, the refresh data's entries only where the baseline task says
# family-update did NOT run (or the copy took --skip-tasks), and the data-root guard, which no
# lane offers, for a settings file that lacks it.
# Each entry is a fragment the copy output must carry, matched with whitespace collapsed and
# Copier's own file-operation lines removed. generate-all.sh check 4 and coexist-test.sh
# check 19 read this list; shipped-seeds.sh check 12 reads the settings lists above.
SM_AFTER_COPY_LINES=()
for _sm_x in $SM_SHARED_SHIPPED; do SM_AFTER_COPY_LINES+=("$_sm_x"); done
SM_AFTER_COPY_LINES+=("skip")
SM_AFTER_COPY_LINES+=("${SM_SETTINGS_ALLOW[@]}")
SM_AFTER_COPY_LINES+=("did NOT run" "--skip-tasks")
SM_AFTER_COPY_LINES+=("${SM_SETTINGS_ASK[@]}")
for _sm_x in "${SM_SETTINGS_DENY[@]}"; do [[ "$_sm_x" == Edit\(* ]] && SM_AFTER_COPY_LINES+=("$_sm_x"); done
SM_AFTER_COPY_LINES+=('"idleCompaction": false')
SM_AFTER_COPY_LINES+=("${SM_SETTINGS_FAMILY_ASK[@]}" "${SM_SETTINGS_FAMILY_DENY[@]}" '"hooks" object' "SessionStart" "PreToolUse"
                      "guide guard" "data-root guard" "no lane offers")
SM_AFTER_COPY_LINES+=("python3 .claude/syntek-media-permissions.py --write")
SM_AFTER_COPY_LINES+=("claude mcp add" "ELEVENLABS_MCP_BASE_PATH=" "filter.lfs.required" "git lfs install"
                      "python3 toolkit/media.py check --setup" "$SM_UVX_COPIER update" "-a $SM_ANSWERS_FILE"
                      "GIT_CONFIG_KEY_1=maintenance.auto")
SM_AFTER_COPY_LINES+=("'conflict' then 'skip'" ".claude/rules/syntek-media/ in .claude/CLAUDE.md"
                      "Nothing needs adding to .gitignore or .mcp.json")
unset _sm_x

# ── D81's offers: the baseline task and media's refresh data (DESIGN.md D81, D84) ──
#
# syntek-author's copy-only baseline task, its two lines transcribed byte for byte from its
# SM_FAMILY_RELEASE copier.yml (D81): the last entry of media's _tasks (shipped-seeds.sh check
# 30), held to the --author tree's last _tasks entry by coexist-test.sh check 22.
SM_BASELINE_TASK=$(cat <<'EOF'
  - command: '"<% _copier_python %>" "<% _copier_conf.src_path %>/migrations/family-update.py" baseline --src "<% _copier_conf.src_path %>" --to <% _copier_conf.vcs_ref_hash %> --answers "<% _copier_conf.answers_file %>"'
    when: "<% _copier_operation == 'copy' %>"
EOF
)
SM_UPDATE_MIGRATION="migrations/family-update.py"
# D84's copy-time warning (_tasks entry 4): the file whose absence beside syntek-author's answers
# file means a syntek-author older than v0.6.0, and the fragment of the warning that
# coexist-test.sh check 23 looks for in the copy's output, copied from copier.yml's own text.
SM_AUTHOR_GUIDE_START="how-to/src/TEMPLATE-GUIDE/syntek-author/01-overview.md"
SM_AUTHOR_GUIDE_WARNING="so this syntek-author is older than v0.6.0, which a combined project must not keep"
# migrations/family-refresh.json, media's own refresh data in syntek-author D48's format (D81):
# what shipped-seeds.sh check 31 holds it to. A one-way door: an entry 0.6.0 lists reaches every
# project and cannot be withdrawn. The twenty-seven refresh paths and the restore folder are
# syntek-author's, verbatim (the thirteen working-practice files and D84's fourteen); the hooks
# are its refresh data's hooks object, verbatim (the four handoff-hook entries and the guide
# guard, never the data-root guard, which names no script under .claude/hooks/); the denies and
# asks are the seed's, the six allows apart (D13); the top-level values are the seed's two; the
# mcp lane is syntek-author's, verbatim: two servers, five files at their keys, never
# .claude/mcp_config.json (D76). "model" is never listed.
SM_REFRESH_DATA="migrations/family-refresh.json"
SM_REFRESH_TEMPLATE="syntek-media"
SM_REFRESH_PATHS=".claude/hooks/CLAUDE.md .claude/hooks/CONTEXT.md .claude/hooks/context-threshold-handoff.sh .claude/hooks/how-to-read-only.sh .claude/hooks/pre-compact-handoff.sh .claude/skills/grill-me/SKILL.md .claude/skills/grill-with-docs/SKILL.md .claude/skills/grilling/SKILL.md .claude/skills/handoff/SKILL.md .claude/skills/to-questionnaire/SKILL.md .claude/skills/wait-what/SKILL.md .claude/skills/wayfinder/SKILL.md handoffs/CLAUDE.md handoffs/CONTEXT.md how-to/CLAUDE.md how-to/CONTEXT.md how-to/docs/CLAUDE.md how-to/docs/CONTEXT.md how-to/src/CLAUDE.md how-to/src/CONTEXT.md how-to/src/TEMPLATE-GUIDE/CLAUDE.md how-to/src/TEMPLATE-GUIDE/CONTEXT.md how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md how-to/src/TEMPLATE-GUIDE/the-data-root.md how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md how-to/workflows/CLAUDE.md how-to/workflows/CONTEXT.md"
SM_REFRESH_RESTORE="how-to"
SM_REFRESH_TOP=("${SM_SETTINGS_TOP[@]}")
SM_REFRESH_DENY=("${SM_SETTINGS_DENY[@]}" "${SM_SETTINGS_FAMILY_DENY[@]}")
SM_REFRESH_ASK=("${SM_SETTINGS_ASK[@]}" "${SM_SETTINGS_FAMILY_ASK[@]}")
SM_REFRESH_HOOKS=$(cat <<'EOF'
{"PreCompact":[{"matcher":"auto","hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" auto'","timeout":10}]},{"matcher":"manual","hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" manual'","timeout":10}]}],"PreToolUse":[{"matcher":"Edit|Write|MultiEdit|NotebookEdit","hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/how-to-read-only.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/how-to-read-only.sh\"'","timeout":10}]}],"SessionStart":[{"matcher":"compact","hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/pre-compact-handoff.sh\" compacted'","timeout":10}]}],"UserPromptSubmit":[{"hooks":[{"type":"command","command":"bash -c 'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/context-threshold-handoff.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/context-threshold-handoff.sh\"'","timeout":10}]}]}
EOF
)
SM_REFRESH_MCP_SERVERS="code-review-graph scrapling"
# file<TAB>key path (dot-joined), as the refresh data's "mcp"."files" object holds them.
SM_REFRESH_MCP_FILES="$(printf '%s\t%s\n' .agents/mcp_config.json mcpServers .codex/config.toml mcp_servers \
  .gemini/settings.json mcpServers .mcp.json mcpServers opencode.json mcp.servers)"

# Author-owned, pair-only folders (DESIGN.md Section 3.3). Globs are bash patterns on
# tree-relative directory paths. publishing/src/podcast (gated 'podcast' in PLATFORMS, D59) is
# listed by hand, so shipped-seeds.sh check 11 polices it: a show register or a feed left there
# by a toolkit run inside template/ would otherwise ship into every project. So are
# production/src/timing and production/src/scenes (D64, 0.3.0), for the same reason: a piece's
# tracked timing or scene file written there by a toolkit run inside template/ would ship.
SM_PAIR_ONLY_GLOBS="*/docs/project */workflows/local brand/src/design-system/fonts brand/src/exports brand/src/exports/large brand/src/voice brand/src/platforms scripts/src/pieces production/src/footage production/src/assets production/src/edits production/src/cards production/src/voiceover production/src/timing production/src/scenes production/src/audiobook publishing/src/cut-downs publishing/src/captions publishing/src/thumbnails publishing/src/posts publishing/src/podcast"

# The folder pair's exceptions (DESIGN.md D42): syntek-author's, verbatim — build/, .git/,
# audio/, __pycache__/, node_modules/, .claude/rules/, the inside of each skill folder, each
# drafts/ and each .base/ — then media's: each generated/, renders/ and raw/ (README only), and
# the .agents folder, which holds only the skills link and Antigravity's MCP file (D76). Since
# D80 handoffs/ is no exception: media ships the family's handoffs/ pair, so the folder carries
# it like any other (and .claude/hooks/ and .gemini/ theirs).
exempt_dir() { # tree-relative dir; true when it needs no pair
  case "/$1/" in
    */.git/*|*/build/*|*/audio/*|*/__pycache__/*|*/node_modules/*) return 0 ;;
    /.claude/rules/*) return 0 ;;
    /.claude/skills/*/*) return 0 ;;
    */drafts/*) return 0 ;;
    */.base/*) return 0 ;;
    */generated/*|*/renders/*|*/raw/*) return 0 ;;
    /.agents/*) return 0 ;;   # D76: the agent folder holds a link and a client file, no pair
  esac
  return 1
}
SM_README_ONLY_DIRS="generated renders raw"

# ── Spine and gate sets, built from the catalogue and copier.yml together ────

declare -A SM_SPINE_EXACT=()
declare -A SM_SEED_SET=()
SM_EXAMPLE_LIST=()
SM_SHARED_LIST=()
SM_GATED_LIST=()
SM_ALLOWED_GATES=()
SM_SETS_FOR=""

# Build once per copier.yml. A missing copier.yml leaves the catalogue alone in charge, which is
# what a partial tree needs: the audits still know DESIGN.md's answer. An _exclude line gated
# exactly "_copier_operation == 'update'" is the copy-only shared class (D11); one gated
# "_copier_operation == 'update' or not SEED_EXAMPLES" is a seed-once example (D43). Neither is
# a shipping gate, so neither may gate an index row.
build_sets() { # $1 = copier.yml (may be absent)
  local copier="${1:-}" p cond path gate s m expr a
  [[ "$SM_SETS_FOR" == "x$copier" ]] && return 0
  SM_SETS_FOR="x$copier"
  SM_SPINE_EXACT=(); SM_SEED_SET=(); SM_EXAMPLE_LIST=(); SM_SHARED_LIST=(); SM_GATED_LIST=(); SM_ALLOWED_GATES=()

  for p in $SM_ROOT_SPINE; do SM_SPINE_EXACT["$p"]=1; done
  for p in $SM_SEEDS $SM_SHARED; do SM_SEED_SET["$p"]=1; done
  for p in $SM_EXAMPLES; do SM_EXAMPLE_LIST+=("$p"); done
  for a in $SM_SHIPPING_ATOMS; do SM_ALLOWED_GATES+=("$(norm_expr "${SM_GATE_EXPR[$a]}")"); done

  if [[ -n "$copier" && -f "$copier" ]]; then
    while IFS= read -r p; do
      [[ -z "$p" ]] && continue
      [[ "$p" == *'<:'* ]] && continue
      SM_SEED_SET["${p#/}"]=1
    done < <(yaml_list _skip_if_exists "$copier")
    while IFS=$'\t' read -r cond path; do
      [[ -z "$path" ]] && continue
      SM_GATED_LIST+=("$path")
      if [[ "$cond" == "$SM_SHARED_GATE" ]]; then SM_SHARED_LIST+=("$path"); continue; fi
      if [[ "$cond" == *_copier_operation* ]]; then SM_EXAMPLE_LIST+=("$path"); continue; fi
      [[ "$cond" == *SEED_EXAMPLES* ]] && continue
      if expr="$(negate_gate "$cond")"; then SM_ALLOWED_GATES+=("$(norm_expr "$expr")"); fi
    done < <(exclude_gates "$copier")
  fi

  while read -r gate _ path; do
    [[ -z "$gate" || "$gate" == '#'* || "$gate" == always ]] && continue
    SM_GATED_LIST+=("$path")
  done <<< "$SM_PATHS"

  while read -r s gate m; do
    [[ -z "$s" ]] && continue
    [[ "$gate" != always ]] && SM_GATED_LIST+=(".claude/skills/$s")
    for p in $(modes_list "$m"); do SM_GATED_LIST+=(".claude/skills/$s/$p"); done
  done <<< "$SM_SKILLS"
}

is_seed() { [[ -n "${SM_SEED_SET[$1]:-}" ]]; }

is_shared() { [[ " $SM_SHARED " == *" $1 "* ]]; }

is_example() { # under a seed-once example path
  local e
  for e in "${SM_EXAMPLE_LIST[@]}"; do
    [[ "$1" == "$e" || "$1" == "$e"/* ]] && return 0
  done
  return 1
}

# An index file: a CONTEXT.md or CLAUDE.md whose folder holds a gated descendant.
is_index_file() {
  local base="${1##*/}" dir g
  [[ "$base" == CONTEXT.md || "$base" == CLAUDE.md ]] || return 1
  if [[ "$1" == */* ]]; then dir="${1%/*}"; else dir=""; fi
  for g in "${SM_GATED_LIST[@]}"; do
    if [[ -z "$dir" ]]; then return 0; fi
    [[ "$g" == "$dir"/* ]] && return 0
  done
  return 1
}

is_root_spine() {
  local g
  [[ -n "${SM_SPINE_EXACT[$1]:-}" ]] && return 0
  for g in $SM_ROOT_SPINE_GLOBS; do
    # shellcheck disable=SC2053  # the right-hand side is a glob on purpose
    [[ "$1" == $g ]] && return 0
  done
  return 1
}

# spine_kind REL → prints root | seed | example | index, or returns 1 for a shared file.
spine_kind() {
  if is_root_spine "$1"; then echo root; return 0; fi
  if is_seed "$1"; then echo seed; return 0; fi
  if is_example "$1"; then echo example; return 0; fi
  if is_index_file "$1"; then echo index; return 0; fi
  return 1
}

is_allowed_gate() {
  local e g
  e="$(norm_expr "$1")"
  for g in "${SM_ALLOWED_GATES[@]}"; do [[ "$e" == "$g" ]] && return 0; done
  return 1
}

# ── A rendered tree's answers, and the gate evaluator ────────────────────────

A_KIND=""; A_PLATFORMS=""; A_KINDS=""; A_SEED=true; A_CLIENTS=""

answer_value() { # $1 = key, $2 = answers file → raw value, unquoted
  awk -v key="$1" '
    $0 ~ "^" key ":" {
      v = $0; sub("^" key ":[ \t]*", "", v); sub(/[ \t]+$/, "", v)
      if (v ~ /^".*"$/ || v ~ /^\047.*\047$/) v = substr(v, 2, length(v) - 2)
      print v; exit
    }' "$2" 2>/dev/null
}

# Every value of a list answer (a multiselect such as PLATFORMS), one per line. Copier writes a
# block list (`KEY:` then `- value` lines at column 0); a flow list (`KEY: [a, b]`) is read too.
answer_list() { # $1 = key, $2 = answers file
  awk -v key="$1" '
    $0 ~ "^" key ":" {
      v = $0; sub("^" key ":[ \t]*", "", v)
      if (v ~ /^\[/) { gsub(/[][ \t"\047]/, "", v); n = split(v, a, ","); for (i = 1; i <= n; i++) if (a[i] != "") print a[i]; exit }
      on = 1; next
    }
    on && /^[ \t]*- / { v = $0; sub(/^[ \t]*- [ \t]*/, "", v); gsub(/["\047]/, "", v); print v; next }
    on { exit }' "$2" 2>/dev/null
}

load_answers() { # $1 = answers file. Returns 1 if absent or carries no BRAND_KIND.
  local f="$1" v
  [[ -f "$f" ]] || return 1
  A_KIND="$(answer_value BRAND_KIND "$f")"
  [[ -n "$A_KIND" ]] || return 1
  A_PLATFORMS="$(answer_list PLATFORMS "$f" | tr '\n' ' ')"; A_PLATFORMS="${A_PLATFORMS% }"
  A_KINDS="$(answer_list MEDIA_KINDS "$f" | tr '\n' ' ')"; A_KINDS="${A_KINDS% }"
  v="$(answer_value SEED_EXAMPLES "$f")"
  case "$v" in false|False|no) A_SEED=false ;; *) A_SEED=true ;; esac
  # No AGENT_CLIENTS key (a project from before 0.5.0) or an empty list: Claude Code only.
  A_CLIENTS="$(answer_list AGENT_CLIENTS "$f" | tr '\n' ' ')"; A_CLIENTS="${A_CLIENTS% }"
  return 0
}

has_client() { [[ " $A_CLIENTS " == *" $1 "* ]]; }

gate_true() { # $1 = gate in the catalogue vocabulary
  local atom IFS='&'
  for atom in $1; do
    case "$atom" in
      always|optional) ;;
      business)   [[ "$A_KIND" == business ]] || return 1 ;;
      fiction)    [[ "$A_KIND" == author-fiction ]] || return 1 ;;
      nonfiction) [[ "$A_KIND" == author-nonfiction ]] || return 1 ;;
      author)     [[ "$A_KIND" != business ]] || return 1 ;;
      p:*)        [[ " $A_PLATFORMS " == *" ${atom#p:} "* ]] || return 1 ;;
      k:*)        [[ " $A_KINDS " == *" ${atom#k:} "* ]] || return 1 ;;
      seed)       [[ "$A_SEED" == true ]] || return 1 ;;
      # The client gates (DESIGN.md D80, Section 3.5; syntek-author D47).
      agents)     [[ -n "${A_CLIENTS// /}" ]] || return 1 ;;
      agents-md)  has_client codex || has_client opencode || return 1 ;;
      gemini-md)  has_client gemini-cli || has_client antigravity || return 1 ;;
      cl-*)       has_client "${atom#cl-}" || return 1 ;;
      *) return 1 ;;
    esac
  done
  return 0
}

# Render names are <kind>--<profile> (DESIGN.md D28): the kinds carry a hyphen, so split on two.
kind_of()    { printf '%s' "${1%%--*}"; }
profile_of() { printf '%s' "${1#*--}"; }

# ── The over-author scope (DESIGN.md Section 7) ──────────────────────────────
#
# On a <kind>--over-author tree every per-tree audit checks only media-owned paths: the files
# media's copy added to the committed syntek-author render, which generate-all.sh records
# beside the tree as <render>.owned, one tree-relative path per line. A standalone tree has no
# .owned file, and every path in it is media's.

SM_OWNED_MODE=false
declare -A SM_OWNED=()
declare -A SM_OWNED_DIRS=()
declare -A SM_FOREIGN_DIRS=()

owned_paths() { # $1 = tree → its media-owned paths, or return 1 for a standalone tree
  local t="${1%/}"
  [[ -f "$t.owned" ]] || return 1
  grep -v '^[[:space:]]*$' "$t.owned" || true
}

# Load a tree's scope. A directory is media-owned when it holds a media-owned file and no file
# of anyone else's — so brand/ is media's, .claude/skills/ (syntek-author's pair, both
# templates' skills) is not, and neither is the root.
load_owned() { # $1 = tree
  local t="${1%/}" f d
  SM_OWNED_MODE=false; SM_OWNED=(); SM_OWNED_DIRS=(); SM_FOREIGN_DIRS=()
  [[ -f "$t.owned" ]] || return 0
  SM_OWNED_MODE=true
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    SM_OWNED["$f"]=1
    d="$f"
    while [[ "$d" == */* ]]; do d="${d%/*}"; SM_OWNED_DIRS["$d"]=1; done
  done < "$t.owned"
  while IFS= read -r -d '' f; do
    f="${f#./}"
    [[ -n "${SM_OWNED[$f]:-}" ]] && continue
    SM_FOREIGN_DIRS["."]=1
    d="$f"
    while [[ "$d" == */* ]]; do d="${d%/*}"; SM_FOREIGN_DIRS["$d"]=1; done
  done < <(cd "$t" && find . -name .git -prune -o \( -type f -o -type l \) -print0)
  return 0
}

is_owned_file() { # tree-relative file; always true on a standalone tree
  $SM_OWNED_MODE || return 0
  [[ -n "${SM_OWNED[$1]:-}" ]]
}

is_owned_dir() { # tree-relative dir ("" or "." for the root); always true on a standalone tree
  local d="${1:-.}"
  $SM_OWNED_MODE || return 0
  [[ "$d" == . ]] && return 1
  [[ -n "${SM_OWNED_DIRS[$d]:-}" && -z "${SM_FOREIGN_DIRS[$d]:-}" ]]
}

# ── syntek-author's names (DESIGN.md D27, Section 7) ─────────────────────────
#
# The names media must never take are frozen in syntek-author-names.txt: a dated header, then
# one line per name — `top <entry>` for each entry of syntek-author's template/ plus `top build`,
# `claude <entry>` for each entry of its template/.claude/, `skill <name>` for each skill folder,
# `rules <file>` for each file of its rules folder (template/.claude/rules/syntek-author/) —
# sorted. author_names prints exactly those lines for a live tree; coexist-test.sh
# --refresh-names writes the file from it, and the drift is the difference.

SM_AUTHOR_DIR=""
SM_AUTHOR_SOURCE="none"

# Where syntek-author is: --author DIR (must exist), else $SYNTEK_AUTHOR_DIR, else
# $SM_ROOT/../syntek-author. Sets SM_AUTHOR_DIR (empty when there is none) and
# SM_AUTHOR_SOURCE (explicit | env | default | none). An audit that needs it SKIPs, named, when
# it is empty (D27): never a pass.
resolve_author_dir() { # $1 = the --author argument (may be empty)
  SM_AUTHOR_DIR=""; SM_AUTHOR_SOURCE="none"
  if [[ -n "${1:-}" ]]; then
    [[ -d "$1/template" && -f "$1/copier.yml" ]] || die "--author $1 is not a syntek-author repository (no copier.yml and template/)"
    SM_AUTHOR_DIR="$(cd "$1" && pwd)"; SM_AUTHOR_SOURCE="explicit"; return 0
  fi
  if [[ -n "${SYNTEK_AUTHOR_DIR:-}" && -d "$SYNTEK_AUTHOR_DIR/template" && -f "$SYNTEK_AUTHOR_DIR/copier.yml" ]]; then
    SM_AUTHOR_DIR="$(cd "$SYNTEK_AUTHOR_DIR" && pwd)"; SM_AUTHOR_SOURCE="env"; return 0
  fi
  if [[ -d "$SM_ROOT/../syntek-author/template" && -f "$SM_ROOT/../syntek-author/copier.yml" ]]; then
    SM_AUTHOR_DIR="$(cd "$SM_ROOT/../syntek-author" && pwd)"; SM_AUTHOR_SOURCE="default"; return 0
  fi
  return 0
}

author_names() { # $1 = syntek-author repository → the name lines, sorted
  local a="$1" tpl="$1/template" e
  [[ -d "$tpl" ]] || return 1
  ignored() { git -C "$a" check-ignore -q -- "$1" 2>/dev/null; }
  {
    printf 'top build\n'
    while IFS= read -r e; do ignored "template/$e" || printf 'top %s\n' "$e"; done \
      < <(find "$tpl" -mindepth 1 -maxdepth 1 -printf '%f\n')
    if [[ -d "$tpl/.claude" ]]; then
      while IFS= read -r e; do ignored "template/.claude/$e" || printf 'claude %s\n' "$e"; done \
        < <(find "$tpl/.claude" -mindepth 1 -maxdepth 1 -printf '%f\n')
    fi
    if [[ -d "$tpl/.claude/skills" ]]; then
      while IFS= read -r e; do ignored "template/.claude/skills/$e" || printf 'skill %s\n' "$e"; done \
        < <(find "$tpl/.claude/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n')
    fi
    if [[ -d "$tpl/.claude/rules/syntek-author" ]]; then
      while IFS= read -r e; do ignored "template/.claude/rules/syntek-author/$e" || printf 'rules %s\n' "$e"; done \
        < <(find "$tpl/.claude/rules/syntek-author" -mindepth 1 -maxdepth 1 -type f -printf '%f\n')
    fi
  } | LC_ALL=C sort -u
}

# The name lines of the frozen file (comments and blank lines dropped), sorted.
names_file_lines() { # $1 = names file (default: SM_AUTHOR_NAMES_FILE)
  local f="${1:-$SM_AUTHOR_NAMES_FILE}"
  [[ -f "$f" ]] || return 1
  grep -vE '^[[:space:]]*(#|$)' "$f" | sed 's/[[:space:]]*$//' | LC_ALL=C sort -u
}

declare -A SM_AUTHOR_TOP=()
declare -A SM_AUTHOR_CLAUDE=()
declare -A SM_AUTHOR_SKILL=()
declare -A SM_AUTHOR_RULES=()

# Read the frozen names, or stop: the file is read on every run and is never a SKIP, so a
# missing one means the run cannot be completed (exit 2; DESIGN.md D27).
require_author_names() {
  local kind name
  [[ -f "$SM_AUTHOR_NAMES_FILE" ]] || die "$SM_AUTHOR_NAMES_FILE is missing — syntek-author's frozen names are read on every run and never skipped; write it with: bash .github/scripts/coexist-test.sh --refresh-names --author <syntek-author>"
  SM_AUTHOR_TOP=(); SM_AUTHOR_CLAUDE=(); SM_AUTHOR_SKILL=(); SM_AUTHOR_RULES=()
  while read -r kind name; do
    case "$kind" in
      top)    SM_AUTHOR_TOP["$name"]=1 ;;
      claude) SM_AUTHOR_CLAUDE["$name"]=1 ;;
      skill)  SM_AUTHOR_SKILL["$name"]=1 ;;
      rules)  SM_AUTHOR_RULES["$name"]=1 ;;
    esac
  done < <(names_file_lines)
  [[ ${#SM_AUTHOR_SKILL[@]} -gt 0 ]] || die "$SM_AUTHOR_NAMES_FILE names no syntek-author skill — it is not the frozen list"
}

# The difference between the frozen file and a live tree: `+ line` for a name the tree has and
# the file lacks, `- line` for the reverse. Prints nothing when they agree.
names_drift() { # $1 = syntek-author repository
  LC_ALL=C comm -3 <(names_file_lines) <(author_names "$1") \
    | sed -e 's/^\t/+ /' -e 's/^\([^+]\)/- \1/'
}

# ── Files ────────────────────────────────────────────────────────────────────

# Every file under DIR, relative to it, NUL-separated: git-tracked plus untracked-unignored
# when DIR is inside a work tree (the file just written is the one that most needs checking),
# a plain walk otherwise. .git is never listed.
list_files0() { # $1 = dir
  local dir="$1" top rel
  if top="$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)" && [[ "$(cd "$dir" && pwd -P)" != "$(cd "$top" && pwd -P)"/.git* ]]; then
    { git -C "$dir" ls-files -z --full-name -- . ; git -C "$dir" ls-files -z --others --exclude-standard --full-name -- . ; } \
      | { rel="$(cd "$dir" && pwd -P)"; rel="${rel#"$(cd "$top" && pwd -P)"}"; rel="${rel#/}"
          while IFS= read -r -d '' f; do
            [[ -n "$rel" ]] && f="${f#"$rel"/}"
            [[ -e "$dir/$f" ]] && printf '%s\0' "$f"
          done; } | sort -zu
  else
    (cd "$dir" && find . -name .git -prune -o -type f -print0 | sed -z 's#^\./##' | sort -z)
  fi
}

# Every file of a tree, relative, one per line, sorted bytewise — whatever Git ignores
# included. The over-author scope is the difference of two of these.
tree_files() { # $1 = dir
  (cd "$1" && find . -name .git -prune -o \( -type f -o -type l \) -print | sed 's#^\./##' | LC_ALL=C sort)
}

# ── _message_after_copy ──────────────────────────────────────────────────────

# Every SM_AFTER_COPY_LINES fragment a Copier log does not carry, one per line. ANSI colour
# and Copier's own file-operation lines (create, skip, conflict …) are removed first, so a path
# Copier merely listed never stands in for the message; whitespace runs are collapsed.
message_missing_lines() { # $1 = Copier's output (stdout and stderr, captured without --quiet)
  local text frag
  text="$(sed -e 's/\x1b\[[0-9;]*m//g' "$1" 2>/dev/null \
    | { grep -vE '^[[:space:]]*(create|identical|conflict|skip|overwrite|force|delete|run|unsafe)[[:space:]]{2}' || true; } \
    | { grep -v '^Copying from template' || true; } | tr -s '[:space:]' ' ')"
  for frag in "${SM_AFTER_COPY_LINES[@]}"; do
    [[ "$text" == *"$frag"* ]] || printf '%s\n' "$frag"
  done
}

# ── Rendering ────────────────────────────────────────────────────────────────

SM_COPIER=()
copier_init() {
  if [[ -n "${COPIER_CMD:-}" ]]; then
    read -r -a SM_COPIER <<< "$COPIER_CMD"
  elif command -v uvx >/dev/null 2>&1; then
    SM_COPIER=(uvx copier)
  elif command -v copier >/dev/null 2>&1; then
    SM_COPIER=(copier)
  else
    die "neither uvx nor copier is on PATH — nothing can render (install uv, or set COPIER_CMD)"
  fi
}

sm_git() { # $1 = dir, then git arguments — with an identity, so CI needs no global config
  local d="$1"; shift
  git -C "$d" -c user.name='syntek-media audit' -c user.email='audit@example.com' \
    -c commit.gpgsign=false -c init.defaultBranch=main "$@"
}

# Copy a working tree (uncommitted work included, .gitignore honoured as a commit would) to
# DEST and commit it, so `--vcs-ref=HEAD` renders exactly what is on disk (SB rule 17).
sm_snapshot() { # $1 = source repo, $2 = dest
  command -v rsync >/dev/null 2>&1 || die "rsync is not installed"
  rm -rf "$2"; mkdir -p "$2"
  rsync -a --exclude '.git' "$1/" "$2/" || return 1
  sm_git "$2" init -q && sm_git "$2" add -A && sm_git "$2" commit -q -m 'audit snapshot' || return 1
}

# The answers every media render passes: the questions with no default, and BRAND_KIND. Lists
# go as values with no spaces (PLATFORMS=[linkedin]); never --quiet, which would swallow the
# _message_after_copy that generate-all.sh check 4 reads.
SM_RENDER_NAME="Probe Studio"
SM_RENDER_DESCRIPTION="A probe brand rendered by the audit suite to prove the template generates end to end."
SM_RENDER_OWNER="Ada Example"
SM_RENDER_DATE="01/01/2027"

# SM_VCS_REF (default HEAD) names the ref a render or update takes: update-test.sh's D76 flow
# tags a snapshot v0.4.1 and v0.4.2 so the migration's version gate is crossed for real.
sm_render() { # $1 = template, $2 = dest, $3 = BRAND_KIND, then extra copier arguments
  local src="$1" dest="$2" kind="$3"; shift 3
  [[ ${#SM_COPIER[@]} -gt 0 ]] || copier_init
  "${SM_COPIER[@]}" copy --trust --defaults --vcs-ref="${SM_VCS_REF:-HEAD}" \
    --data "BRAND_NAME=$SM_RENDER_NAME" \
    --data "BRAND_DESCRIPTION=$SM_RENDER_DESCRIPTION" \
    --data "OWNER_NAME=$SM_RENDER_OWNER" \
    --data "DATE=$SM_RENDER_DATE" \
    --data "BRAND_KIND=$kind" \
    "$@" "$src" "$dest" </dev/null
}

sm_update() { # $1 = project dir, then extra copier arguments
  local proj="$1"; shift
  [[ ${#SM_COPIER[@]} -gt 0 ]] || copier_init
  (cd "$proj" && "${SM_COPIER[@]}" update --trust --defaults --vcs-ref="${SM_VCS_REF:-HEAD}" \
     --answers-file "$SM_ANSWERS_FILE" "$@" </dev/null)
}

# syntek-author's own render, exactly as its audits render it: its four questions with no
# default, and DOC_TYPE (business, fiction or theology: author_doc_for_kind).
SM_AUTHOR_RENDER_NAME="Probe Project"
SM_AUTHOR_RENDER_DESCRIPTION="A probe project rendered by the audit suite to prove the template generates end to end."
SM_AUTHOR_RENDER_AUTHOR="Ada Example"
SM_AUTHOR_RENDER_DATE="01/01/2027"

sm_render_author() { # $1 = syntek-author template, $2 = dest, $3 = DOC_TYPE, then extra arguments
  local src="$1" dest="$2" doc="$3"; shift 3
  [[ ${#SM_COPIER[@]} -gt 0 ]] || copier_init
  "${SM_COPIER[@]}" copy --trust --defaults --vcs-ref=HEAD \
    --data "PROJECT_NAME=$SM_AUTHOR_RENDER_NAME" \
    --data "PROJECT_DESCRIPTION=$SM_AUTHOR_RENDER_DESCRIPTION" \
    --data "AUTHOR_NAME=$SM_AUTHOR_RENDER_AUTHOR" \
    --data "DATE=$SM_AUTHOR_RENDER_DATE" \
    --data "DOC_TYPE=$doc" \
    "$@" "$src" "$dest" </dev/null
}

sm_update_author() { # $1 = project dir, then extra copier arguments
  local proj="$1"; shift
  [[ ${#SM_COPIER[@]} -gt 0 ]] || copier_init
  (cd "$proj" && "${SM_COPIER[@]}" update --trust --defaults --vcs-ref=HEAD \
     --answers-file "$SM_AUTHOR_ANSWERS" "$@" </dev/null)
}

# The intended path (DESIGN.md D4, Section 8): syntek-author rendered and committed, then media
# copied in WITHOUT --overwrite. Writes DEST.owned — the files media's copy added, whatever Git
# ignores included — and sets OA_AUTHOR_STATUS and OA_MEDIA_STATUS. Returns non-zero when either
# copy failed. Output goes wherever the caller sends it (generate-all.sh keeps it in DEST.log).
# D76's pre-copy check (bridge, 'Enabling an existing project'; README.md; DESIGN.md Section
# 3.7). Copier writes a folder's entries THROUGH an existing .agents link (into .claude, or the
# author's own tree), so a copy over an .agents link, or over a file, passes --exclude /.agents.
# Over a real .agents folder only a REAL DIRECTORY at .agents/skills fails (Copier asserts before
# its skip check where a path resolving to a directory meets a link in the template), and takes
# --exclude /.agents/skills. A .agents/skills link of any target is skipped without error and
# left as it is, so it needs no argument. Prints the arguments, one per line (none when the copy
# needs none). A link that leaves the project fails every copy and update before _exclude is
# read (ForbiddenPathError, Copier 9.17.1 _main.py:810-811, read 14/10/2026), so no argument
# helps on its own. An update holds such a link aside and restores it through D76's
# unversioned migration pair (SM_OUTSIDE_MIGRATION, DESIGN.md D11's second exception); a copy
# runs no migration and takes the hand recipe of the bridge and README.md instead: mv .agents
# .agents.syntek-held, copy with --exclude /.agents (the argument this prints for the link, called
# before the mv), then mv .agents.syntek-held .agents.
sm_agents_copy_args() { # $1 = destination
  local d="$1/.agents"
  if [[ -L "$d" || ( -e "$d" && ! -d "$d" ) ]]; then printf -- '--exclude\n/.agents\n'; return 0; fi
  [[ -d "$d/skills" && ! -L "$d/skills" ]] && printf -- '--exclude\n/.agents/skills\n'
  return 0
}

OA_AUTHOR_STATUS=0
OA_MEDIA_STATUS=0
sm_render_over_author() { # $1 = syntek-author snapshot, $2 = media snapshot, $3 = dest, $4 = BRAND_KIND, then media arguments
  local asnap="$1" msnap="$2" dest="$3" kind="$4" before
  shift 4
  OA_AUTHOR_STATUS=0; OA_MEDIA_STATUS=0
  rm -f "$dest.owned"
  sm_render_author "$asnap" "$dest" "$(author_doc_for_kind "$kind")" || OA_AUTHOR_STATUS=$?
  [[ "$OA_AUTHOR_STATUS" -eq 0 ]] || return "$OA_AUTHOR_STATUS"
  [[ -d "$dest/.git" ]] || sm_git "$dest" init -q
  sm_git "$dest" add -A && sm_git "$dest" commit -q -m 'syntek-author' || true
  before="$(mktemp)"
  tree_files "$dest" > "$before"
  local -a agents_args=()
  mapfile -t agents_args < <(sm_agents_copy_args "$dest")
  sm_render "$msnap" "$dest" "$kind" "${agents_args[@]}" "$@" || OA_MEDIA_STATUS=$?
  tree_files "$dest" | LC_ALL=C comm -13 "$before" - > "$dest.owned"
  rm -f "$before"
  return "$OA_MEDIA_STATUS"
}

# The family-shared migrations block (syntek-author D48), markers included, byte for byte as
# syntek-author's SM_FAMILY_RELEASE copier.yml carries it, for the FIXTURES only: the real
# copier.yml's block is held to the 'migrations' entry of family-shared.json (shipped-seeds.sh
# check 22), never to this copy. The markers' D48 is syntek-author's number, never media's.
# Media's copier.yml takes the block first in _migrations (D85). sm_fixture_template below and
# shipped-seeds.sh's self-test fixture print it, so the fixture's updates run the vendored
# script as the real ones do: with the interpreter running Copier, _copier_python.
SM_FAMILY_MIGRATIONS_BEGIN="# BEGIN family-shared migrations (D48)"
SM_FAMILY_MIGRATIONS_END="# END family-shared migrations (D48)"
sm_family_migrations_block() {
  cat <<'EOF'
# BEGIN family-shared migrations (D48)
  # Unversioned on purpose, so they run on every update and never on a copy. Where .agents
  # is a link that resolves outside the project, which Copier refuses to render beneath even
  # where _exclude names it, hold renames the link to .agents.syntek-held before the render
  # and restore renames it back after; the link's target is never touched. Both always exit
  # 0. Keep this pair first: restore must run before every other after-stage migration.
  - command: '"<% _copier_python %>" "<% _copier_conf.src_path %>/migrations/agents-outside-link.py" hold'
    when: "<% _stage == 'before' %>"
  - command: '"<% _copier_python %>" "<% _copier_conf.src_path %>/migrations/agents-outside-link.py" restore'
    when: "<% _stage == 'after' %>"
# END family-shared migrations (D48)
EOF
}

# The family-shared update block (syntek-author D48, D51, D52; media's D81), markers included,
# byte for byte as syntek-author's SM_FAMILY_RELEASE copier.yml carries it, for the FIXTURES
# only: the real copier.yml's block is held to the 'update' entry of family-shared.json
# (shipped-seeds.sh check 26), never to this copy. It closes _migrations, so the fixtures'
# updates run the real migrations/family-update.py last, on the interpreter running Copier.
SM_FAMILY_UPDATE_BEGIN="# BEGIN family-shared update (D48)"
SM_FAMILY_UPDATE_END="# END family-shared update (D48)"
SM_FAMILY_UPDATE_SCRIPT="migrations/family-update.py"
sm_family_update_block() {
  cat <<'EOF'
# BEGIN family-shared update (D48)
  # Unversioned and last, so it runs after every other migration on every update. It reports
  # each file this update did not deliver, refreshes the shared files the owner had not
  # changed, and records the render in refs/<template>/ inside .git. Always exits 0.
  - command: '"<% _copier_python %>" "<% _copier_conf.src_path %>/migrations/family-update.py" update --src "<% _copier_conf.src_path %>" --to <% _copier_conf.vcs_ref_hash %> --answers "<% _copier_conf.answers_file %>"'
    when: "<% _stage == 'after' %>"
# END family-shared update (D48)
EOF
}

# The SHA-256 of standard input, as hex: sha256sum (Linux) or shasum (macOS).
sm_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum | cut -c1-64
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 | cut -c1-64
  else die "neither sha256sum nor shasum is installed"; fi
}

# ── family-shared.json: the reader and the writer (DESIGN.md D80) ─────────────
#
# One program reads the manifest for every audit that needs it, so no two scripts disagree
# about its format, which is the family's (syntek-author's family-shared.sh, entry, block_lines
# and block_entry): files sorted by destination path; a block's bytes are the lines strictly
# between its two marker lines, each ended with \n, hashed as UTF-8. A file's mode is "755"
# where Git's index holds it at 100755, or, for a file the index does not hold (or outside a
# work tree), where it is executable; no key at all otherwise. Modes:
#   check ROOT            shipped-seeds.sh checks 23–26 on the source: one "N<TAB>text" line per
#                         finding, then "E<TAB>outside<TAB>sha256<TAB>mode" and
#                         "E<TAB>migrations<TAB>sha256" wherever the manifest holds a usable
#                         entry for checks 21 and 22. Exit 3: a .git stands that Git will not read.
#   write ROOT            rewrite ROOT/family-shared.json from the files and blocks (exit 2: a
#                         source is not what SM_FAMILY_SHARED says, or a block's markers are wrong).
#   tree ROOT TREE [OWN]  shipped-seeds.sh checks 10 and 27 on a render: each token-free
#                         project-scope family file the tree holds (and OWN lists, over
#                         syntek-author) has the bytes and executable bit ROOT's manifest
#                         records (the .agents/skills link is shipped-brands.sh check 13's).
#   compare ROOT AUTHOR   coexist-test.sh check 22: ROOT's manifest against the AUTHOR tree's,
#                         entry by entry, nothing deferred since D81, and _common.sh's family
#                         asks, denies (the guide's Edit(/how-to/**) among them), top-level
#                         values and hooks against the AUTHOR tree's own settings seed; since
#                         0.6.0 also the family lists of ROOT's migrations/family-refresh.json
#                         against the AUTHOR tree's, and SM_BASELINE_TASK against the AUTHOR
#                         tree's last _tasks entry (D81).
sm_family_py() {
  SMF_FILES="$SM_FAMILY_SHARED" SMF_LINKS="$SM_FAMILY_LINKS" SMF_BLOCKS="$SM_FAMILY_BLOCKS" \
  SMF_MANIFEST="$SM_FAMILY_MANIFEST" SMF_OWNER="$SM_FAMILY_OWNER" SMF_RELEASE="$SM_FAMILY_RELEASE" \
  SMF_DEFERRED="$SM_FAMILY_DEFERRED" SMF_RENDERED="$SM_FAMILY_RENDERED" SMF_OUTSIDE="$SM_OUTSIDE_MIGRATION" \
  SMF_AGENTS_LINK="$SM_AGENTS_SKILLS_LINK" \
  SMF_ASK="$(printf '%s\n' "${SM_SETTINGS_FAMILY_ASK[@]}")" \
  SMF_DENY="$(printf '%s\n' "${SM_SETTINGS_FAMILY_DENY[@]}")" SMF_HOOKS="$SM_SETTINGS_HOOKS" \
  SMF_TOP="$(printf '%s\n' "${SM_SETTINGS_TOP[@]}")" \
  SMF_EDIT_DENY="$(printf '%s\n' "${SM_SETTINGS_DENY[@]}" | grep '^Edit(/how-to/' || true)" \
  SMF_REFRESH_DATA="$SM_REFRESH_DATA" SMF_BASELINE="$SM_BASELINE_TASK" \
  SMF_MEDIA_ASK="$(printf '%s\n' "${SM_SETTINGS_ASK[@]}")" \
  python3 -I - "$@" <<'PYFAMILY'
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

E = os.environ
mode, root = sys.argv[1], Path(sys.argv[2])
FILES = []
for line in E["SMF_FILES"].splitlines():
    f = line.split()
    if f:
        FILES.append((f[0], f[1], f[2] if len(f) > 2 else "project"))
LINKS = set(E["SMF_LINKS"].split())
BLOCKS = []
for line in E["SMF_BLOCKS"].splitlines():
    if line.strip():
        n, src, dest, b, e = line.split("|")
        BLOCKS.append((n, src, dest or None, b, e))
MANIFEST, OWNER, RELEASE = E["SMF_MANIFEST"], E["SMF_OWNER"], E["SMF_RELEASE"]
OWN_NAME = OWNER[len("syntek-"):]
DEFERRED = set(E["SMF_DEFERRED"].split())
RENDERED = set(E["SMF_RENDERED"].split())
OUTSIDE = E["SMF_OUTSIDE"]
WANT = [(p, s, "symlink" if p in LINKS else "file", sc) for p, s, sc in sorted(FILES)]
WANT_B = list(BLOCKS)
out = []

def finding(n, text):
    out.append(f"{n}\t{text}")

def git(*args):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return r.returncode, r.stdout

def index_modes():
    """{path: Git mode} for what the index holds under ROOT; None outside a work tree."""
    code, top = git("rev-parse", "--is-inside-work-tree")
    if code or top.strip() != "true":
        if (root / ".git").exists() or (root / ".git").is_symlink():
            print(f"{root / '.git'} stands, but Git will not read it (an ownership mismatch? see git config safe.directory)", file=sys.stderr)
            sys.exit(3)
        return None
    code, listing = git("ls-files", "-s", "-z")
    modes = {}
    for rec in listing.split("\0"):
        if rec and "\t" in rec:
            meta, path = rec.split("\t", 1)
            modes[path] = meta.split()[0]
    return modes

def file_mode(rel, modes):
    if modes is not None and rel in modes:
        return "755" if modes[rel] == "100755" else None
    return "755" if os.stat(root / rel).st_mode & 0o111 else None

def entry(path, source, scope, modes):
    """(the manifest entry the file on disk would have, whether it is the kind listed)."""
    p = root / source
    kind = "symlink" if path in LINKS else "file"
    e = {"path": path, "source": source, "kind": kind}
    if scope != "project":
        e["scope"] = scope
    if kind == "symlink":
        if not p.is_symlink():
            return e, False
        e["target"] = os.readlink(p)
        return e, True
    if p.is_symlink() or not p.is_file():
        return e, False
    b = p.read_bytes()
    e["bytes"], e["sha256"] = len(b), hashlib.sha256(b).hexdigest()
    m = file_mode(source, modes)
    if m:
        e["mode"] = m
    return e, True

def block_lines(path, begin, end):
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None, "cannot be read"
    b = [i for i, l in enumerate(lines) if l == begin]
    e = [i for i, l in enumerate(lines) if l == end]
    if len(b) != 1 or len(e) != 1 or b[0] > e[0]:
        return None, f"holds '{begin}' {len(b)} time(s) and '{end}' {len(e)} time(s); each must appear once, BEGIN first"
    return lines[b[0] + 1:e[0]], ""

def block_entry(name, source, dest, begin, end, lines):
    data = "".join(l + "\n" for l in lines).encode()
    e = {"name": name, "source": source}
    if dest is not None:
        e["destination"] = dest
    e.update({"begin": begin, "end": end, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return e

def release_wanted():
    """The release values the manifest may hold, and why: 'v' + VERSION on the commit that tag
    names and on an untagged commit whose VERSION no tag has yet (the release commit);
    'unreleased' once that tag is an ancestor of HEAD; either where Git cannot tell."""
    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        version = ""
    either = {"unreleased"} | ({f"v{version}"} if version else set())
    if not version:
        return either, ""
    code, top = git("rev-parse", "--show-toplevel")
    if code or Path(top.strip()).resolve() != root.resolve():
        return either, ""
    tag = "v" + version
    code, tagged = git("rev-parse", "-q", "--verify", f"refs/tags/{tag}^{{commit}}")
    if code:
        code, tags = git("tag", "-l", "v[0-9]*")
        if not code and tags.strip():
            return {tag}, f"VERSION is {version} and no tag {tag} exists yet, so this is its release commit"
        return either, ""
    code, head = git("rev-parse", "-q", "--verify", "HEAD^{commit}")
    if code:
        return either, ""
    if tagged.strip() == head.strip():
        return {tag}, f"HEAD is tagged {tag}"
    code, _ = git("merge-base", "--is-ancestor", tagged.strip(), head.strip())
    if code == 0:
        return {"unreleased"}, f"{tag} is already released, so later work is unreleased until the next release"
    return either, ""

def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), ""
    except FileNotFoundError:
        return None, "missing"
    except (OSError, ValueError) as err:
        return None, f"not JSON ({err})"

def usable(man):
    return isinstance(man, dict) and man.get("format") == 1 and man.get("owner") == OWNER

def listed(man):
    """The manifest's file and block entries that belong to the set, by path and by name."""
    files = man.get("files") if isinstance(man.get("files"), list) else []
    blocks = man.get("blocks") if isinstance(man.get("blocks"), list) else []
    fs = {e["path"]: e for e in files if isinstance(e, dict)
          and (e.get("path"), e.get("source"), e.get("kind"), e.get("scope", "project")) in WANT}
    bs = {x["name"]: x for x in blocks if isinstance(x, dict)
          and (x.get("name"), x.get("source"), x.get("destination"), x.get("begin"), x.get("end")) in WANT_B}
    return files, blocks, fs, bs

def short(h):
    return (str(h)[:12] + "…") if h else "none"

if mode == "write":
    modes = index_modes()
    wanted, _ = release_wanted()
    old, _ = load(root / MANIFEST)
    release = old["release"] if isinstance(old, dict) and old.get("release") in wanted else "unreleased"
    if len(wanted) == 1:
        release = next(iter(wanted))
    entries = []
    for path, source, scope in sorted(FILES):
        e, ok = entry(path, source, scope, modes)
        if not ok:
            print(f"{source} is not {'a link' if path in LINKS else 'a file'}; vendor it from syntek-author {RELEASE} first", file=sys.stderr)
            sys.exit(2)
        entries.append(e)
    blocks = []
    for n, src, dest, b, e in BLOCKS:
        lines, err = block_lines(root / src, b, e)
        if lines is None:
            print(f"{src} {err}", file=sys.stderr)
            sys.exit(2)
        blocks.append(block_entry(n, src, dest, b, e, lines))
    text = ('{\n  "format": 1,\n  "owner": "' + OWNER + '",\n  "release": ' + json.dumps(release) + ',\n  "files": [\n'
            + ",\n".join("    " + json.dumps(e, ensure_ascii=False) for e in entries)
            + '\n  ],\n  "blocks": [\n'
            + ",\n".join("    " + json.dumps(x, ensure_ascii=False) for x in blocks)
            + "\n  ]\n}\n")
    (root / MANIFEST).write_text(text, encoding="utf-8")
    sys.exit(0)

if mode == "check":
    modes = index_modes()
    man, err = load(root / MANIFEST)
    if man is None:
        finding(23, f"{MANIFEST} is {'missing from the repository root' if err == 'missing' else err}: the family-shared set has no record to be held to (write it with shipped-seeds.sh --write-manifest; DESIGN.md D80)")
    else:
        wanted, why = release_wanted()
        if not usable(man) or man.get("release") not in wanted:
            finding(23, f"{MANIFEST} must hold format 1, owner {OWNER} and release one of {sorted(wanted)}"
                        + (f" ({why}; shipped-seeds.sh --write-manifest sets it)" if why else "")
                        + " (DESIGN.md D80; the family's format, syntek-author D48)")
            man = None
    if man is not None:
        files, blocks, fs, bs = listed(man)
        have = [(e.get("path"), e.get("source"), e.get("kind"), e.get("scope", "project")) if isinstance(e, dict) else None for e in files]
        if have != WANT:
            missing = [w[0] for w in WANT if w not in have]
            extra = [str(h[0]) if h else repr(h) for h in have if h not in WANT]
            finding(24, f"{MANIFEST} files are not the vendored set of _common.sh's SM_FAMILY_SHARED (missing, or a wrong source, kind or scope: "
                        f"{', '.join(missing) or 'none'}; extra or wrong: {', '.join(extra) or 'none'}; order: "
                        f"{'wrong' if not missing and not extra else 'n/a'}) (DESIGN.md D80)")
        have_b = [(x.get("name"), x.get("source"), x.get("destination"), x.get("begin"), x.get("end")) if isinstance(x, dict) else None for x in blocks]
        if have_b != WANT_B:
            finding(24, f"{MANIFEST} blocks are not exactly the questions, migrations and update blocks of copier.yml, then the rules-web-tools "
                        f"block of {BLOCKS[-1][1]} with its destination {BLOCKS[-1][2]}, in that order, between the family's markers "
                        "(DESIGN.md D80, D81)")
        for path, e in fs.items():
            if path == OUTSIDE:
                if e.get("sha256"):
                    out.append(f"E\toutside\t{e.get('sha256')}\t{'100755' if e.get('mode') == '755' else '100644'}")
                continue
            cur, ok = entry(path, e["source"], e.get("scope", "project"), modes)
            if path in LINKS:
                # The link itself is shipped-seeds.sh check 18's (the D76 link); this check
                # holds only the record to it, so one fault is one finding.
                if ok and cur.get("target") == E["SMF_AGENTS_LINK"] and cur.get("target") != e.get("target"):
                    finding(25, f"{e['source']} is the link {cur.get('target')!r}, but {MANIFEST} records {e.get('target')!r} (DESIGN.md D76, D80)")
            elif not ok:
                finding(25, f"{e['source']} is not a file, as {MANIFEST} records it: vendor it from syntek-author {RELEASE} (DESIGN.md D80)")
            else:
                if (cur["bytes"], cur["sha256"]) != (e.get("bytes"), e.get("sha256")):
                    finding(25, f"{e['source']} has SHA-256 {short(cur['sha256'])} ({cur['bytes']} bytes), not {short(e.get('sha256'))} "
                                f"({e.get('bytes')} bytes) as {MANIFEST} records: a family-shared file is vendored byte for byte from "
                                f"syntek-author {RELEASE} and never edited here (DESIGN.md D80; syntek-author D48)")
                if cur.get("mode") != e.get("mode"):
                    finding(25, f"{e['source']} is at mode {cur.get('mode') or '644'}, not {e.get('mode') or '644'} as {MANIFEST} records "
                                "(Git's index where it holds the file, else the executable bit: git update-index --chmod=+x or -x; DESIGN.md D80)")
        for name, x in bs.items():
            src = x["source"]
            lines, err = block_lines(root / src, x["begin"], x["end"])
            if name == "migrations":
                if x.get("sha256"):
                    out.append(f"E\tmigrations\t{x.get('sha256')}")
                continue
            if lines is None:
                finding(26, f"{src} {err}: the family-shared {name} block is taken whole (DESIGN.md D80; syntek-author D48)")
                continue
            data = "".join(l + "\n" for l in lines).encode()
            sha = hashlib.sha256(data).hexdigest()
            if (len(data), sha) != (x.get("bytes"), x.get("sha256")):
                finding(26, f"the lines between {src}'s family-shared {name} markers have SHA-256 {short(sha)} ({len(data)} bytes), not "
                            f"{short(x.get('sha256'))} as {MANIFEST} records: the block is taken byte for byte and never edited here "
                            "(DESIGN.md D80; syntek-author D48)")
    print("\n".join(out))
    sys.exit(0)

if mode == "tree":
    tree = Path(sys.argv[3])
    own = None
    if len(sys.argv) > 4 and sys.argv[4]:
        own = set(Path(sys.argv[4]).read_text(encoding="utf-8").splitlines())
    man, _ = load(root / MANIFEST)
    if man is None or not usable(man):
        sys.exit(0)  # check 23's, on the source
    _, _, fs, _ = listed(man)
    for path, e in sorted(fs.items()):
        if e.get("scope", "project") != "project":
            continue
        dest = path.replace("<template>", OWN_NAME)
        if dest in RENDERED or (own is not None and dest not in own):
            continue
        p = tree / dest
        if not (p.exists() or p.is_symlink()):
            continue  # shipped-brands.sh check 6's
        if path in LINKS:
            continue  # a render's .agents/skills link is shipped-brands.sh check 13's
        n = 10 if dest == ".mcp.json" else 27
        why = ("it declares the family's two servers, code-review-graph and scrapling, pinned, and never ElevenLabs, which stays "
               "user-scoped (DESIGN.md D21, D80)") if n == 10 else "a token-free family file renders to its own bytes (DESIGN.md D80)"
        if p.is_symlink() or not p.is_file():
            finding(n, f"{dest} is not a file")
            continue
        b = p.read_bytes()
        sha = hashlib.sha256(b).hexdigest()
        if sha != e.get("sha256"):
            finding(n, f"{dest} has SHA-256 {short(sha)}, not {short(e.get('sha256'))} as {MANIFEST} records for it: {why}")
        elif e.get("mode") == "755" and not os.access(p, os.X_OK):
            finding(n, f"{dest} is not executable in the render, though {MANIFEST} records mode 755 (copier.yml's copy-only chmod task; DESIGN.md D80)")
    print("\n".join(out))
    sys.exit(0)

if mode == "compare":
    author = Path(sys.argv[3])
    def say(text):
        out.append(text)
    mine, err = load(root / MANIFEST)
    theirs, terr = load(author / MANIFEST)
    if mine is None or not usable(mine):
        say(f"media's {MANIFEST} cannot be read as the family's format (shipped-seeds.sh check 23 says why), so nothing can be compared")
    elif theirs is None:
        say(f"the --author tree's {MANIFEST} is {'missing' if terr == 'missing' else terr}: it predates the family-shared set media vendors from syntek-author {RELEASE}")
    else:
        if theirs.get("owner") != "syntek-author" or theirs.get("format") != 1:
            say(f"the --author tree's {MANIFEST} is not syntek-author's format-1 manifest (owner {theirs.get('owner')!r}, format {theirs.get('format')!r})")
        if theirs.get("release") != RELEASE:
            say(f"the --author tree's {MANIFEST} records release {theirs.get('release')!r}, not {RELEASE}, the tag media vendors from: run against "
                f"that tag (CI's SYNTEK_AUTHOR_TAG), or re-vendor every family file and block from the new tag and move SM_FAMILY_RELEASE "
                "with it (DESIGN.md D85: one tag for every family file)")
        tfiles = {e.get("path"): e for e in theirs.get("files", []) if isinstance(e, dict)}
        tblocks = {x.get("name"): x for x in theirs.get("blocks", []) if isinstance(x, dict)}
        _, _, fs, bs = listed(mine)
        for path, e in sorted(fs.items()):
            t = tfiles.get(path)
            if t is None:
                say(f"media vendors {path}, which the --author tree's {MANIFEST} does not list")
                continue
            keys = ("kind", "scope", "bytes", "sha256", "mode", "target")
            diff = [k for k in keys if e.get(k) != t.get(k)]
            if diff:
                def show(d):
                    return ", ".join(k + " " + (short(d.get(k)) if k == "sha256" else repr(d.get(k))) for k in diff)
                say(f"{path}: media's {MANIFEST} records {show(e)}, the --author tree's {show(t)}: "
                    "re-vendor it from that tag, never edit it here (DESIGN.md D80, D85)")
        for path in sorted(p for p in tfiles if p not in fs and p not in DEFERRED):
            say(f"the --author tree's {MANIFEST} lists {path}, which media does not vendor: adopt it, with its "
                "copier.yml lines and its place in SM_FAMILY_SHARED (DESIGN.md D80, D81, D85)")
        for name, x in bs.items():
            t = tblocks.get(name)
            if t is None:
                say(f"media takes the {name} block, which the --author tree's {MANIFEST} does not list")
                continue
            diff = [k for k in ("destination", "begin", "end", "bytes", "sha256") if x.get(k) != t.get(k)]
            if diff:
                say(f"the {name} block: media's {MANIFEST} and the --author tree's differ in {', '.join(diff)}: re-vendor it from that tag "
                    "(DESIGN.md D80, D85)")
        for name in sorted(n for n in tblocks if n not in bs and f"block:{n}" not in DEFERRED):
            say(f"the --author tree's {MANIFEST} lists the {name} block, which media does not take: adopt it, with its place in "
                "SM_FAMILY_BLOCKS (DESIGN.md D80, D81, D85)")
    seed = author / "template" / ".claude" / "settings.json"
    try:
        sd = json.loads(re.sub(r"<:.*?:>", "", seed.read_text(encoding="utf-8"), flags=re.S))
    except (OSError, ValueError) as error:
        say(f"the --author tree's template/.claude/settings.json cannot be read with its gates removed ({error.__class__.__name__}), so the "
            "family's asks, denies, top-level values and hooks cannot be compared")
    else:
        perms = sd.get("permissions") or {}
        ask = [a for a in perms.get("ask") or [] if a.startswith("mcp__")]
        alldeny = perms.get("deny") or []
        deny = [d for d in alldeny if d.startswith("mcp__")]
        if ask != [a for a in E["SMF_ASK"].splitlines() if a]:
            say("_common.sh's SM_SETTINGS_FAMILY_ASK is not the --author tree's seed's MCP asks, in order: transcribe them again (DESIGN.md D13, D80)")
        if deny != [d for d in E["SMF_DENY"].splitlines() if d]:
            say("_common.sh's SM_SETTINGS_FAMILY_DENY is not the --author tree's seed's MCP denies (DESIGN.md D13, D80)")
        for rule in [r for r in E["SMF_EDIT_DENY"].splitlines() if r]:
            if rule not in alldeny:
                say(f"_common.sh's SM_SETTINGS_DENY holds the guide's {rule}, which the --author tree's seed does not deny: media's seed "
                    "takes syntek-author's one anchored rule (DESIGN.md D13, D84; syntek-author D56)")
        for kv in [t for t in E["SMF_TOP"].splitlines() if t]:
            key, val = kv.split("=", 1)
            if sd.get(key, "absent") != json.loads(val):
                say(f"_common.sh's SM_SETTINGS_TOP sets {key} to {val}, but the --author tree's seed holds {json.dumps(sd.get(key, 'absent'))}: "
                    "transcribe the top-level values again (DESIGN.md D13, D35, D81)")
        if sd.get("hooks") != json.loads(E["SMF_HOOKS"]):
            say("_common.sh's SM_SETTINGS_HOOKS is not the --author tree's seed's hooks key, byte for byte as JSON: media's seed registers "
                "the family's hooks as syntek-author's does (DESIGN.md D13, D35, D80)")
    # D81: the family lists of the two templates' refresh data agree, entry by entry. Media's own
    # asks and denies (ElevenLabs, voice remix run, generated and renders) and syntek-author's own
    # denies are each template's; everything else either lists is the family's.
    rd = E["SMF_REFRESH_DATA"]
    mr, merr = load(root / rd)
    ar, aerr = load(author / rd)
    if not isinstance(mr, dict):
        say(f"media's {rd} is {merr or 'not an object'}, so its family lists cannot be compared (shipped-seeds.sh check 31 says why)")
    elif not isinstance(ar, dict):
        say(f"the --author tree's {rd} is {aerr or 'not an object'}: it predates D81's refresh data, which media's copies from {RELEASE}")
    else:
        def st(d):
            return d.get("settings") if isinstance(d.get("settings"), dict) else {}
        def perm(d, kind):
            p = st(d).get("permissions") if isinstance(st(d).get("permissions"), dict) else {}
            return p.get(kind) if isinstance(p.get(kind), list) else []
        for key, why in (("refresh", "the family-shared files the update refreshes"), ("restore", "the folder the update restores")):
            if mr.get(key) != ar.get(key):
                say(f"media's {rd} lists {key} {json.dumps(mr.get(key))[:160]}, the --author tree's {json.dumps(ar.get(key))[:160]}: "
                    f"{why} are syntek-author's, verbatim (DESIGN.md D81, D84)")
        if st(mr).get("hooks") != st(ar).get("hooks"):
            say(f"media's {rd} hooks are not the --author tree's, as parsed JSON: the hook entries both templates offer are the family's, "
                "verbatim (DESIGN.md D81)")
        for k in ("autoCompactEnabled", "idleCompaction"):
            if st(mr).get(k, "absent") != st(ar).get(k, "absent"):
                say(f"media's {rd} lists {k} {json.dumps(st(mr).get(k, 'absent'))}, the --author tree's {json.dumps(st(ar).get(k, 'absent'))} (DESIGN.md D81)")
        own_ask = [a for a in E["SMF_MEDIA_ASK"].splitlines() if a]
        if [a for a in perm(mr, "ask") if a not in own_ask] != perm(ar, "ask"):
            say(f"media's {rd} asks, its own eleven apart, are not the --author tree's, in order: syntek-author D54's eight are the family's "
                "(DESIGN.md D13, D81)")
        family_deny = ["AskUserQuestion"] + [r for r in E["SMF_EDIT_DENY"].splitlines() if r]
        for rule in family_deny:
            if (rule in perm(mr, "deny")) != (rule in perm(ar, "deny")):
                say(f"media's {rd} and the --author tree's disagree on the deny {rule}: one lists it, the other does not (DESIGN.md D81, D84)")
        if [d for d in perm(mr, "deny") if d.startswith("mcp__")] != [d for d in perm(ar, "deny") if d.startswith("mcp__")]:
            say(f"media's {rd} MCP denies are not the --author tree's: syntek-author D54's deny is the family's (DESIGN.md D81)")
        if mr.get("mcp") != ar.get("mcp"):
            say(f"media's {rd} mcp lane is not the --author tree's: the two servers and the five files are the family's, verbatim (DESIGN.md D81)")
    # D81: the baseline task media transcribes is the --author tree's last _tasks entry.
    try:
        cy = (author / "copier.yml").read_text(encoding="utf-8").splitlines()
    except OSError:
        cy = None
    if cy is None:
        say("the --author tree has no copier.yml, so its baseline task cannot be compared")
    else:
        entries, on = [], False
        for line in cy:
            if line.startswith("_tasks:"):
                on = True
                continue
            if on and re.match(r"[A-Za-z_]", line):
                break
            if not on or not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.startswith("  - "):
                entries.append([line])
            elif entries:
                entries[-1].append(line)
        last = "\n".join(entries[-1]) if entries else ""
        if last != E["SMF_BASELINE"]:
            say("_common.sh's SM_BASELINE_TASK is not the --author tree's last _tasks entry, line for line: transcribe syntek-author's "
                "baseline task again from the tag, and media's copier.yml with it (DESIGN.md D81)")
    print("\n".join(out))
    sys.exit(0)

print(f"sm_family_py: unknown mode {mode}", file=sys.stderr)
sys.exit(2)
PYFAMILY
}

# ── The fixture templates ────────────────────────────────────────────────────
#
# sm_fixture_template: a minimal syntek-media with the real repository's shape — the house
# delimiters, the named answers file, the copy-only shared paths (the retired one excluded
# on copy as well), the D76 .agents folder and its v0.4.2 migration after the family-shared
# migrations block (D85: the vendored outside-link pair), a register seed and a
# brand seed, a gated profile and platform guide per platform, the podcast platform's gate on
# the pair-only folder of the show registers (DESIGN.md D59), the audiobook gate on a folder
# and a skill, one seed-once example, a moded skill with its generated mode block, the D14
# guard (the previous answers through _external_data, BRAND_KIND's validator), the static
# _message_before_update, and a _message_after_copy carrying every SM_AFTER_COPY_LINES fragment.
# sm_author_fixture_template: syntek-author's own fixture, ported from its _common.sh — its
# answers file, its D17 seeds, its rules folder, its run-workflow skill and its Makefile.
# The integration self-tests run their whole flow against these, so the harness is proven
# independently of the real template's state — which, mid-build, may not render at all.

# What both fixture templates share for D81's lanes: one server in .mcp.json (the same bytes in
# both, so a copy over the other offers nothing there), the guide guard's hook entry, and the
# minimal refresh data that lists them with the guard and one deny.
SM_FIXTURE_MCP='{"mcpServers": {"scrapling": {"command": "uvx", "args": ["scrapling", "mcp"]}}}'
SM_FIXTURE_GUARD_HOOK='{"matcher": "Edit|Write|MultiEdit|NotebookEdit", "hooks": [{"type": "command", "command": "bash -c '"'"'ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f \"$ROOT/.claude/hooks/how-to-read-only.sh\" ] || exit 0; exec bash \"$ROOT/.claude/hooks/how-to-read-only.sh\"'"'"'", "timeout": 10}]}'
sm_fixture_refresh_json() { # $1 = template name → the fixture's migrations/family-refresh.json
  SMR_GUARD="$SM_FIXTURE_GUARD_HOOK" python3 -I - "$1" <<'PYREFRESH'
import json, os, sys
guard = json.loads(os.environ["SMR_GUARD"])
data = {"format": 1, "template": sys.argv[1],
        "refresh": [".claude/hooks/how-to-read-only.sh"] if sys.argv[1] == "syntek-media" else [],
        "restore": ["how-to"],
        "settings": {"hooks": {"PreToolUse": [guard]} if sys.argv[1] == "syntek-media" else {},
                     "permissions": {"deny": ["Edit(/how-to/**)"] if sys.argv[1] == "syntek-media" else []}},
        "mcp": {"servers": ["scrapling"], "files": {".mcp.json": ["mcpServers"]}}}
print(json.dumps(data, indent=2))
PYREFRESH
}

sm_fixture_template() { # $1 = dest (created, git-initialised and committed)
  local t="$1" p k s m q="'"
  rm -rf "$t"; mkdir -p "$t/template"
  {
    cat <<'EOF'
_min_copier_version: "9.12.0"
_subdirectory: template
_preserve_symlinks: true
_answers_file: .copier-answers.syntek-media.yml
_external_data:
  prev: .copier-answers.syntek-media.yml
_migrations:
EOF
    sm_family_migrations_block
    cat <<'EOF'
  - version: v0.4.2
    command: python3 "<% _copier_conf.src_path %>/migrations/v0.4.2-agents-folder.py"
    when: "<% _stage == 'after' %>"
EOF
    sm_family_update_block
    cat <<'EOF'
_message_before_update: |
  Before you answer: removing a platform or a media kind deletes EVERY file it generated.
    PLATFORMS without <platform>     brand/src/platforms/<platform>.md and
                                     publishing/docs/reference/<platform>.md — for each of
                                     youtube, tiktok, instagram, linkedin, facebook, podcast,
                                     website, blog, newsletter
    PLATFORMS without podcast        also publishing/src/podcast/ (its pair; registers stay)
    MEDIA_KINDS without audiobook    production/src/audiobook/ and the narrate-audiobook skill
    MEDIA_KINDS without podcast      nothing in this fixture
    MEDIA_KINDS without trailer      nothing in this fixture
    MEDIA_KINDS without short-video  nothing in this fixture
    MEDIA_KINDS without long-video   nothing in this fixture
    MEDIA_KINDS without voiceover    nothing in this fixture
  BRAND_KIND never changes.

  If this update stops with OSError: [Errno 39] Directory not empty, never commit what it
  left: README.md 'Updating a project', at the template's source, gives the recovery and the
  command to use.
_message_after_copy: |
EOF
    printf '  Shared files, written only where absent (a skip left yours exactly as it was):\n'
    for p in $SM_SHARED_SHIPPED; do printf '    %s\n' "$p"; done
    printf '    Existing agent directories, aliases and settings need manual setup.\n'
    printf '  Copier lists an existing one as %sconflict%s then %sskip%s; that pair is expected.\n' "$q" "$q" "$q" "$q"
    printf '  Optional: name .claude/rules/syntek-media/ in .claude/CLAUDE.md.\n'
    printf '  Nothing needs adding to .gitignore or .mcp.json.\n'
    printf '  Add these to an existing .claude/settings.json by hand, since no lane offers them:\n'
    for p in "${SM_SETTINGS_ALLOW[@]}"; do printf '    allow: %s\n' "$p"; done
    printf '  The rest only if family-update did NOT run, or the copy took --skip-tasks:\n'
    for p in "${SM_SETTINGS_ASK[@]}"; do printf '    ask: %s\n' "$p"; done
    for p in "${SM_SETTINGS_DENY[@]}"; do [[ "$p" == Edit\(* ]] && printf '    deny: %s\n' "$p"; done
    printf '  Where syntek-author v0.7.0 or later did not seed it, the family entries too:\n'
    printf '    top level: "idleCompaction": false\n'
    for p in "${SM_SETTINGS_FAMILY_ASK[@]}"; do printf '    ask: %s\n' "$p"; done
    for p in "${SM_SETTINGS_FAMILY_DENY[@]}"; do printf '    deny: %s\n' "$p"; done
    printf '    and the seed%ss "hooks" object, its SessionStart entry and the guide guard%ss PreToolUse entry.\n' "$q" "$q"
    printf '  Add the data-root guard by hand where it is missing: no lane offers it.\n'
    printf '  Then carry them to the other clients: python3 .claude/syntek-media-permissions.py --write\n'
    printf '  claude mcp add --scope user elevenlabs -- uvx elevenlabs-mcp\n'
    printf '    with --env ELEVENLABS_MCP_BASE_PATH="$HOME": the base path must contain the project.\n'
    printf '  This copy may have set filter.lfs.required in .git/config; git lfs install makes it harmless.\n'
    printf '  Then run: python3 toolkit/media.py check --setup\n'
    printf '  Update with: GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false uvx --python %s>=3.14%s copier update --trust -a .copier-answers.syntek-media.yml\n' "$q" "$q"
    cat <<'EOF'
_templates_suffix: ""
_envops:
  variable_start_string: "<%"
  variable_end_string: "%>"
  block_start_string: "<:"
  block_end_string: ":>"
  comment_start_string: "<~"
  comment_end_string: "~>"
  keep_trailing_newline: true
_exclude:
  - .git
EOF
    for p in $SM_SHARED; do printf '  - "<: if _copier_operation == %supdate%s :>/%s<: endif :>"\n' "$q" "$q" "$p"; done
    for p in $SM_SHARED_RETIRED; do printf '  - /%s\n' "$p"; done
    for p in $SM_PLATFORMS; do
      printf '  - "<: if not (%s%s%s in PLATFORMS) :>/brand/src/platforms/%s.md<: endif :>"\n' "$q" "$p" "$q" "$p"
      printf '  - "<: if not (%s%s%s in PLATFORMS) :>/publishing/docs/reference/%s.md<: endif :>"\n' "$q" "$p" "$q" "$p"
    done
    printf '  - "<: if not (%spodcast%s in PLATFORMS) :>/publishing/src/podcast<: endif :>"\n' "$q" "$q"
    printf '  - "<: if not (%saudiobook%s in MEDIA_KINDS) :>/production/src/audiobook<: endif :>"\n' "$q" "$q"
    printf '  - "<: if not (%saudiobook%s in MEDIA_KINDS) :>/.claude/skills/narrate-audiobook<: endif :>"\n' "$q" "$q"
    printf '  - "<: if _copier_operation == %supdate%s or not SEED_EXAMPLES :>/scripts/src/pieces/000-example-piece<: endif :>"\n' "$q" "$q"
    printf '  # BEGIN generated mode excludes\n'
    for m in $SM_MODE_FILES; do
      printf '  - "<: if BRAND_KIND != %s%s%s :>/.claude/skills/write-script/%s<: endif :>"\n' "$q" "$(kind_for_mode "$m")" "$q" "$m"
    done
    printf '  # END generated mode excludes\n'
    printf '_skip_if_exists:\n'
    for p in $SM_SHARED brand/src/design-system/tokens.css publishing/src/publish-log.md $SM_PLATFORM_SEEDS; do printf '  - /%s\n' "$p"; done
    # _tasks (D81, D84): media's first two, its copy-time warning's stand-in, then syntek-author's
    # baseline task exactly as SM_BASELINE_TASK transcribes it, last.
    printf '_tasks:\n'
    printf '  - command: "[ -d .git ] || git init --initial-branch=main"\n    when: "<%% _copier_operation == %scopy%s %%>"\n' "$q" "$q"
    printf '  - command: "chmod +x .claude/hooks/*.sh 2>/dev/null || true"\n    when: "<%% _copier_operation == %scopy%s %%>"\n' "$q" "$q"
    printf '  - command: >-\n      [ ! -f %s ] || [ -f %s ] || echo %ssyntek-media fixture: %s%s\n    when: "<%% _copier_operation == %scopy%s %%>"\n' \
      "$SM_AUTHOR_ANSWERS" "$SM_AUTHOR_GUIDE_START" "$q" "$SM_AUTHOR_GUIDE_WARNING" "$q" "$q" "$q"
    printf '%s\n' "$SM_BASELINE_TASK"
    cat <<'EOF'
BRAND_NAME:
  type: str
BRAND_DESCRIPTION:
  type: str
BRAND_KIND:
  type: str
  choices: [business, author-fiction, author-nonfiction]
  validator: "<: if (_external_data.prev.BRAND_KIND | default(BRAND_KIND, true)) != BRAND_KIND :>BRAND_KIND cannot change on update.<: endif :>"
OWNER_NAME:
  type: str
DATE:
  type: str
PLATFORMS:
  type: str
  multiselect: true
  choices:
    "youtube — long videos": youtube
    "tiktok — vertical video": tiktok
    "instagram — reels": instagram
    "linkedin — video posts": linkedin
    "facebook — reels": facebook
    "podcast — feeds": podcast
    "website — sites": website
    "blog — posts": blog
    "newsletter — issues": newsletter
  default: "<% {'business': ['youtube', 'linkedin', 'instagram'], 'author-fiction': ['youtube', 'tiktok', 'instagram', 'facebook'], 'author-nonfiction': ['youtube', 'podcast', 'instagram', 'facebook']}[BRAND_KIND] | tojson %>"
  validator: "<: if not PLATFORMS :>Choose at least one platform.<: endif :>"
MEDIA_KINDS:
  type: str
  multiselect: true
  choices:
    "short-video — shorts": short-video
    "long-video — explainers": long-video
    "podcast — episodes": podcast
    "audiobook — books": audiobook
    "trailer — trailers": trailer
    "voiceover — voiceovers": voiceover
  default: "<% {'business': ['short-video', 'long-video', 'voiceover'], 'author-fiction': ['short-video', 'trailer', 'audiobook', 'voiceover'], 'author-nonfiction': ['long-video', 'short-video', 'podcast', 'audiobook', 'voiceover']}[BRAND_KIND] | tojson %>"
  validator: "<: if not MEDIA_KINDS :>Choose at least one media kind.<: endif :>"
SEED_EXAMPLES:
  type: bool
  default: true
EOF
  } > "$t/copier.yml"

  cd "$t/template" || return 1
  mkdir -p .claude/rules/syntek-media .claude/skills/run-media-workflow .claude/skills/write-script \
    .claude/skills/narrate-audiobook brand/src/design-system brand/src/platforms publishing/docs/reference \
    publishing/src/podcast production/src/audiobook/generated scripts/src/pieces/000-example-piece toolkit
  printf '<%% _copier_answers|to_nice_yaml -%%>\n' > "$SM_ANSWERS_FILE"
  printf '# <%%BRAND_NAME%%>\n\nA fixture brand on <%% PLATFORMS | join(%s, %s) %%>.\n' "$q" "$q" > README.md
  printf '# CONTEXT.md — <%%BRAND_NAME%%>\n' > CONTEXT.md
  printf '__pycache__/\n' > .gitignore
  printf '%s\n' "$SM_FIXTURE_MCP" > .mcp.json
  mkdir -p .codex
  printf '# AGENTS.md — fixture instructions\n' > AGENTS.md
  printf '# GEMINI.md — fixture instructions\n' > GEMINI.md
  mkdir .agents; ln -s "$SM_AGENTS_SKILLS_LINK" .agents/skills
  printf '{"mcpServers": {}}\n' > .agents/mcp_config.json
  printf "project_doc_fallback_filenames = ['CLAUDE.md']\n" > .codex/config.toml
  printf '# CONTEXT.md — .codex/\n' > .codex/CONTEXT.md
  printf '# CLAUDE.md — .codex/\n' > .codex/CLAUDE.md
  printf '{"mcpServers": {}}\n' > .claude/mcp_config.json
  printf '# CLAUDE.md — <%%BRAND_NAME%%>\n\n## 3. Project-specific rules\n' > .claude/CLAUDE.md
  printf '# CONTEXT.md — .claude/\n' > .claude/CONTEXT.md
  printf '# MEMORY.md — <%%BRAND_SLUG%%>\n\n## Facts\n\n## Decisions\n\n## Feedback\n\n## Status\n\n## Open questions\n\n## Sensitivities\n' > .claude/MEMORY.md
  {
    printf '{\n  "model": "opus",\n  "autoCompactEnabled": false,\n  "permissions": {\n'
    printf '    "deny": [%s],\n' "$(for s in "${SM_SETTINGS_DENY[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '    "allow": [%s],\n' "$(for s in "${SM_SETTINGS_ALLOW[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '    "ask": [%s]\n' "$(for s in "${SM_SETTINGS_ASK[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '  },\n  "hooks": {"PreToolUse": [%s]}\n}\n' "$SM_FIXTURE_GUARD_HOOK"
  } > .claude/settings.json
  # The guide guard (D84), the one shared hook the fixture ships, executable as the family's is.
  mkdir -p .claude/hooks
  printf '#!/usr/bin/env bash\n# a fixture guide guard\nexit 0\n' > .claude/hooks/how-to-read-only.sh
  chmod 755 .claude/hooks/how-to-read-only.sh
  printf '# CONTEXT.md — .claude/skills/\n' > .claude/skills/CONTEXT.md
  printf '@./CONTEXT.md\n\n# CLAUDE.md — .claude/skills/\n' > .claude/skills/CLAUDE.md
  printf '# 01-layout-and-routing.md — layout and routing\n\nTemplate-owned; updated by copier update.\n\n## 1. The brand\n\n<%%BRAND_NAME%%>, a <%%BRAND_KIND%%> brand.\n' \
    > .claude/rules/syntek-media/01-layout-and-routing.md
  printf -- '---\nname: run-media-workflow\ndescription: Route a media request to its workflow.\n---\n\n# Skill: Run media workflow (<%%BRAND_NAME%%>)\n' \
    > .claude/skills/run-media-workflow/SKILL.md
  printf -- '---\nname: write-script\ndescription: Write a script for the ear.\n---\n\n# Skill: Write script (<%%BRAND_NAME%%>)\n\n> **Mode.** Before step 1, read the brand-kind mode file beside this one.\n' \
    > .claude/skills/write-script/SKILL.md
  for m in $SM_MODE_FILES; do printf '# %s — write-script, %s mode\n' "$m" "$(kind_for_mode "$m")" > ".claude/skills/write-script/$m"; done
  printf -- '---\nname: narrate-audiobook\ndescription: Narrate an audiobook.\n---\n\n# Skill: Narrate audiobook (<%%BRAND_NAME%%>)\n' \
    > .claude/skills/narrate-audiobook/SKILL.md
  printf ':root {\n  --color-bg: #ffffff; /* AUTHOR TO CONFIRM: the brand background */\n}\n' > brand/src/design-system/tokens.css
  for p in $SM_PLATFORMS; do
    printf '# %s profile — <%%BRAND_NAME%%>\n\n## Account\n\n<!-- AUTHOR TO CONFIRM: the handle -->\n' "$p" > "brand/src/platforms/$p.md"
    printf '# %s — the platform guide\n' "$p" > "publishing/docs/reference/$p.md"
  done
  printf '# Publish log\n\n> **This file is a seeded stub, and it is deliberately unfinished.**\n\n| Date | Platform | Deliverable | Piece | URL | Disclosure set | Captions | Notes |\n|---|---|---|---|---|---|---|---|\n' \
    > publishing/src/publish-log.md
  printf '# CONTEXT.md — publishing/src/podcast/\n' > publishing/src/podcast/CONTEXT.md
  printf '@./CONTEXT.md\n\n# CLAUDE.md — publishing/src/podcast/\n' > publishing/src/podcast/CLAUDE.md
  printf '# CONTEXT.md — production/src/audiobook/\n' > production/src/audiobook/CONTEXT.md
  printf '@./CONTEXT.md\n\n# CLAUDE.md — production/src/audiobook/\n' > production/src/audiobook/CLAUDE.md
  printf '# generated/\n\nGenerated audio; git-ignored.\n' > production/src/audiobook/generated/README.md
  printf -- '---\npiece: 000-example-piece\nstatus: storyboarded\n---\n\n# The example piece — brief\n' > scripts/src/pieces/000-example-piece/brief.md
  cat > toolkit/media.py <<'EOF'
#!/usr/bin/env python3
"""A fixture toolkit: one command and a self-test."""
import sys

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        print("media.py self-test: ok")
        sys.exit(0)
    print("usage: media.py --self-test", file=sys.stderr)
    sys.exit(2)
EOF
  cd - >/dev/null || return 1
  # The real D76 migration, so the fixture's update proves the script it ships (a fixture
  # without it cannot test the first migration at all).
  mkdir -p "$t/migrations"
  cp "$SM_ROOT/$SM_D76_MIGRATION" "$t/$SM_D76_MIGRATION" || return 1
  cp "$SM_ROOT/$SM_OUTSIDE_MIGRATION" "$t/$SM_OUTSIDE_MIGRATION" || return 1
  # The real update script (D81), which the fixture's update block runs last and its baseline
  # task on copy, on 3.14, with a minimal refresh data so that every lane has something to do:
  # the guide guard refreshed, its hook entry and one deny offered, one server over .mcp.json.
  cp "$SM_ROOT/$SM_FAMILY_UPDATE_SCRIPT" "$t/$SM_FAMILY_UPDATE_SCRIPT" || return 1
  sm_fixture_refresh_json syntek-media > "$t/$SM_REFRESH_DATA"
  sm_git "$t" init -q && sm_git "$t" add -A && sm_git "$t" commit -q -m 'fixture template'
}

sm_author_fixture_template() { # $1 = dest (created, git-initialised and committed)
  local t="$1" d
  rm -rf "$t"; mkdir -p "$t/template"
  {
  cat <<'EOF'
_min_copier_version: "9.12.0"
_subdirectory: template
_answers_file: .copier-answers.syntek-author.yml
_external_data:
  prev: .copier-answers.syntek-author.yml
_migrations:
EOF
  sm_family_update_block
  # Its first task and its last, as syntek-author's copier.yml has them: the repository, then the
  # baseline task, which records refs/syntek-author/ there.
  printf '_tasks:\n  - command: "[ -d .git ] || git init --initial-branch=main"\n    when: "<%% _copier_operation == %scopy%s %%>"\n%s\n' "'" "'" "$SM_BASELINE_TASK"
  cat <<'EOF'
_templates_suffix: ""
_envops:
  variable_start_string: "<%"
  variable_end_string: "%>"
  block_start_string: "<:"
  block_end_string: ":>"
  comment_start_string: "<~"
  comment_end_string: "~>"
  keep_trailing_newline: true
_exclude:
  - .git
  - "<: if not (DOC_TYPE != 'business') :>/manuscript<: endif :>"
  - "<: if not (DOC_TYPE == 'business') :>/library<: endif :>"
  - "<: if _copier_operation == 'update' or not SEED_EXAMPLES :>/manuscript/src/01-example-chapter<: endif :>"
_skip_if_exists:
  - /README.md
  - /CONTEXT.md
  - /.gitignore
  - /.mcp.json
  - /.claude/CLAUDE.md
  - /.claude/CONTEXT.md
  - /.claude/MEMORY.md
  - /.claude/settings.json
  - /.claude/skills/CONTEXT.md
  - /.claude/skills/CLAUDE.md
  - /.claude/hooks/CONTEXT.md
  - /.claude/hooks/CLAUDE.md
  - /.claude/rules/syntek-author/00-project.md
  - /standards/style/style-sheet.md
PROJECT_NAME:
  type: str
PROJECT_DESCRIPTION:
  type: str
AUTHOR_NAME:
  type: str
DATE:
  type: str
DOC_TYPE:
  type: str
  choices: [theology, fiction, business]
  validator: "<: if (_external_data.prev.DOC_TYPE | default(DOC_TYPE, true)) != DOC_TYPE :>DOC_TYPE cannot change on update.<: endif :>"
SEED_EXAMPLES:
  type: bool
  default: true
EOF
  } > "$t/copier.yml"
  cd "$t/template" || return 1
  mkdir -p .claude/skills/run-workflow .claude/skills/spelling .claude/hooks .claude/rules/syntek-author standards/style \
    manuscript/src/01-example-chapter library/src handoffs "$(dirname "$SM_AUTHOR_GUIDE_START")"
  printf '<%% _copier_answers|to_nice_yaml -%%>\n' > "$SM_AUTHOR_ANSWERS"
  printf '# <%%PROJECT_NAME%%>\n\nA fixture project.\n' > README.md
  printf '# CONTEXT.md — <%%PROJECT_NAME%%>\n' > CONTEXT.md
  printf 'build/\n' > .gitignore
  printf '%s\n' "$SM_FIXTURE_MCP" > .mcp.json
  printf '# CLAUDE.md — <%%PROJECT_NAME%%>\n\n## 3. Project-specific rules\n' > .claude/CLAUDE.md
  # syntek-author's guide starts here from v0.6.0 (D84): its presence keeps media's copy-time
  # warning silent over a full render.
  printf '# Overview\n\nWhere the guide starts.\n' > "$SM_AUTHOR_GUIDE_START"
  for d in .claude .claude/skills .claude/hooks manuscript/src library/src handoffs; do
    printf '# CONTEXT.md — %s/\n' "$d" > "$d/CONTEXT.md"
  done
  for d in .claude/skills .claude/hooks manuscript/src library/src handoffs; do
    printf '@./CONTEXT.md\n\n# CLAUDE.md — %s/\n' "$d" > "$d/CLAUDE.md"
  done
  printf '# MEMORY.md — <%%PROJECT_NAME%%>\n\n## Facts\n\n_No entries yet._\n' > .claude/MEMORY.md
  printf '{"model": "opus"}\n' > .claude/settings.json
  printf '# 00-project.md — project settings\n\n## Paths\n' > .claude/rules/syntek-author/00-project.md
  printf '# 01 — layout and routing\n\nTemplate-owned; updated by copier update.\n' > .claude/rules/syntek-author/01-layout-and-routing.md
  printf -- '---\nname: run-workflow\ndescription: Route a request to its workflow.\n---\n\n# Skill: run-workflow (<%%PROJECT_NAME%%>)\n' > .claude/skills/run-workflow/SKILL.md
  printf -- '---\nname: spelling\ndescription: Check spelling.\n---\n\n# Skill: Spelling (<%%PROJECT_NAME%%>)\n' > .claude/skills/spelling/SKILL.md
  printf '# Style sheet\n\n## Spelling\n' > standards/style/style-sheet.md
  printf '# The example chapter\n' > manuscript/src/01-example-chapter/01-example-chapter.md
  # lint and flags as syntek-author's Makefile offers them: SCOPE names the folder, and each
  # finding is a file:line line (here, two sentences on one line, and an -ize word), so
  # coexist-test.sh check 24 has something to read.
  {
    printf 'SCOPE ?= .\n\nhelp:\n\t@echo help\n\n'
    printf 'lint:\n\t@grep -rnE --include=*.md %s[.?!] [A-Z]%s $(SCOPE) | sed %ss/$$/: two sentences on one line/%s || true\n\n' "'" "'" "'" "'"
    printf 'flags:\n\t@grep -rnwE --include=*.md %s[a-z]+ize[sd]?%s $(SCOPE) | sed %ss/$$/: an -ize spelling/%s || true\n' "'" "'" "'" "'"
  } > Makefile
  cd - >/dev/null || return 1
  printf '0.7.0\n' > "$t/VERSION"
  # syntek-author's update block (its v0.7.0) runs the same family script, last, on 3.14, and
  # its baseline task on copy, with refresh data of its own (one server over .mcp.json).
  mkdir -p "$t/migrations"
  cp "$SM_ROOT/$SM_FAMILY_UPDATE_SCRIPT" "$t/$SM_FAMILY_UPDATE_SCRIPT" || return 1
  sm_fixture_refresh_json syntek-author > "$t/$SM_REFRESH_DATA"
  sm_git "$t" init -q && sm_git "$t" add -A && sm_git "$t" commit -q -m 'fixture syntek-author'
}

# ── The offers' one exception to 'no byte changed' (DESIGN.md D81) ───────────
#
# Every difference between two .claude/settings.json files that is not the addition of an entry
# the refresh data lists, one per line: a key removed or changed, a list entry removed or
# reordered, a hook entry or rule added that the data does not list, a top-level value added
# that it does not list with the same value. Without REFRESH_JSON, any addition is a difference.
# Nothing printed means AFTER is BEFORE plus offered entries only. update-test.sh check 24 and
# coexist-test.sh checks 8 and 12 read it.
sm_settings_offered_only() { # $1 = BEFORE, $2 = AFTER, $3 = REFRESH_JSON (optional)
  python3 -I - "$1" "$2" "${3:-}" <<'PYOFFER'
import json, sys
def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, ValueError):
        return "unreadable"
before, after = load(sys.argv[1]), load(sys.argv[2])
listed = load(sys.argv[3]) if sys.argv[3] else None
listed = (listed.get("settings") or {}) if isinstance(listed, dict) else {}
out = []
if before is None and after is None:
    sys.exit(0)
if not isinstance(before, dict) or not isinstance(after, dict):
    print("settings.json is " + ("absent" if before is None else "unreadable" if before == "unreadable" else "not an object")
          + " before and " + ("absent" if after is None else "unreadable" if after == "unreadable" else "an object") + " after")
    sys.exit(0)
def strip(have, was, offer, where):
    """have minus the additions offer lists, each at most once, which must then equal was."""
    kept, added = list(have), []
    for x in have:
        if x not in was:
            if x in offer and x not in added:
                added.append(x)
                kept.remove(x)
            elif x in offer:
                out.append(f"{where} gained {json.dumps(x)[:120]} twice; an offered entry is added once")
                kept.remove(x)
            else:
                out.append(f"{where} gained {json.dumps(x)[:120]}, which the refresh data does not list")
                kept.remove(x)
    if kept != was:
        out.append(f"{where} lost, reordered or changed an entry it held")
for k in before:
    if k not in after:
        out.append(f"{k} was removed")
for k in after:
    if k in ("hooks", "permissions"):
        continue
    if k not in before:
        if k not in listed or listed[k] != after[k]:
            out.append(f"{k} was added as {json.dumps(after[k])}, which the refresh data does not list")
    elif after[k] != before[k]:
        out.append(f"{k} changed from {json.dumps(before[k])} to {json.dumps(after[k])}")
for key in ("hooks", "permissions"):
    b, a, l = before.get(key), after.get(key), listed.get(key) or {}
    if a is None:
        continue
    if b is None:
        b = {}
    if not isinstance(a, dict) or not isinstance(b, dict):
        if a != b:
            out.append(f"{key} changed")
        continue
    for sub in a:
        if sub not in b and not isinstance(a[sub], list):
            out.append(f"{key}.{sub} was added")
        elif isinstance(a[sub], list):
            strip(a[sub], b.get(sub) or [], l.get(sub) or [], f"{key}.{sub}")
        elif a[sub] != b.get(sub):
            out.append(f"{key}.{sub} changed")
print("\n".join(out))
PYOFFER
}

# ── Integration helpers (update-test.sh, coexist-test.sh; added by AUDITS-finish) ──
#
# What the two integration tests share: which files a rendered project holds and which of them
# a template owns, what a step changed, a fingerprint of every byte, the conflicts an update
# left behind, and the text of a Copier message with Copier's own file lines taken out.

# Every file of a rendered project, "O path" when the template owns it (rendered and not matched
# by its own _skip_if_exists) and "A path" for every file it rendered; the answers file left
# out (syntek-author's coexist-test.sh, ported). A templated entry is not a path, so it is
# skipped; a glob entry matches as a glob.
owned_and_all() { # $1 = rendered dir, $2 = copier.yml, $3 = answers file
  local f s seed
  local -a skips=()
  while IFS= read -r s; do [[ -n "$s" && "$s" != *'<:'* ]] && skips+=("${s#/}"); done < <(yaml_list _skip_if_exists "$2")
  while IFS= read -r -d '' f; do
    f="${f#./}"
    [[ "$f" == "$3" ]] && continue
    printf 'A %s\n' "$f"
    seed=false
    for s in "${skips[@]}"; do
      # shellcheck disable=SC2053  # _skip_if_exists entries may be globs
      [[ "$f" == $s ]] && { seed=true; break; }
    done
    $seed || printf 'O %s\n' "$f"
  done < <(cd "$1" && find . -name .git -prune -o \( -type f -o -type l \) -print0)
}

# The paths a step changed in a committed project — modified, added, deleted and untracked
# (every file of an untracked folder) — one per line, sorted. Ignored files are not changes.
changed_paths() { # $1 = project
  git -C "$1" status --porcelain -uall 2>/dev/null \
    | sed -E 's/^.{3}//; s/^.* -> //; s/^"(.*)"$/\1/' | LC_ALL=C sort -u
}

# path<TAB>sha1 for every file of a tree (.git left out), sorted by path: what "no byte
# changed" is measured against.
# Link targets are fingerprinted without following the alias into a second tree (D73).
path_fingerprint() { # $1 = file or symbolic link
  if [[ -L "$1" ]]; then { printf 'symlink:'; readlink -n -- "$1"; } | sha1sum | cut -d' ' -f1
  elif [[ -f "$1" ]]; then sha1sum < "$1" | cut -d' ' -f1
  else printf 'absent'; fi
}

hash_tree() { # $1 = dir
  python3 - "$1" <<'PYHASH'
from pathlib import Path
import hashlib, os, sys
root = Path(sys.argv[1])
rows = []
for folder, dirs, files in os.walk(root, followlinks=False):
    dirs[:] = [d for d in dirs if d != '.git']
    names = files + [d for d in dirs if (Path(folder) / d).is_symlink()]
    for name in names:
        path = Path(folder) / name
        digest = hashlib.sha1()
        if path.is_symlink(): digest.update(b'symlink:' + os.fsencode(os.readlink(path)))
        else:
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(64 * 1024), b''): digest.update(block)
        rows.append((path.relative_to(root).as_posix(), digest.hexdigest()))
for name, digest in sorted(rows): print(name + '\t' + digest)
PYHASH
}

# Every *.rej file and every file holding a conflict marker, relative, one per line.
conflicts_in() { # $1 = project
  {
    (cd "$1" && find . -name .git -prune -o -name '*.rej' -print | sed 's#^\./##')
    (cd "$1" && grep -rlI --exclude-dir=.git -e '^<<<<<<< ' . 2>/dev/null | sed 's#^\./##')
  } | LC_ALL=C sort -u || true
}

sm_commit_all() { # $1 = dir, $2 = message — commit whatever is there; nothing to commit is fine
  sm_git "$1" add -A >/dev/null 2>&1 && sm_git "$1" commit -q -m "$2" >/dev/null 2>&1 || true
}

# A Copier log as the person reading it sees the message: colour removed, Copier's own
# file-operation lines (create, identical, skip, conflict …) removed, whitespace collapsed.
copier_message_text() { # $1 = Copier's captured output
  sed -e 's/\x1b\[[0-9;]*m//g' "$1" 2>/dev/null \
    | { grep -vE '^[[:space:]]*(create|identical|conflict|skip|overwrite|force|delete|run|unsafe)[[:space:]]{2}' || true; } \
    | { grep -v '^Copying from template' || true; } | tr -s '[:space:]' ' '
}

# The catalogue paths that ship on exactly one gate atom (p:<platform> or k:<media kind>): the
# SM_PATHS rows with that gate, then the skill folders SM_SKILLS gates on it. A d row names a
# whole folder.
catalogue_paths() { # $1 = gate atom → "kind path" lines (kind: d or f)
  awk -v g="$1" '$1 == g { print $2 " " $3 }' <<< "$SM_PATHS"
  awk -v g="$1" '$2 == g { print "d .claude/skills/" $1 }' <<< "$SM_SKILLS"
}

# A gated platform and media kind to take away in an update (update-test.sh check 13,
# coexist-test.sh check 18): of the project's values that some _exclude line of the template
# gates (a comment or a default naming one does not count), the one with the most catalogue
# paths, the first in answer order on a tie (DESIGN.md Section 7). So the removal that deletes
# the most is the one proved: podcast in the author-nonfiction defaults, the one platform whose
# removal deletes a folder that also holds author files (D59). Prints nothing when none
# qualifies, or when the answer has a single value (the validators need one).
removable_value() { # $1 = PLATFORMS | MEDIA_KINDS, $2 = answers file, $3 = copier.yml
  local v n gates atom c best="" best_n=-1
  n="$(answer_list "$1" "$2" | grep -c . || true)"
  [[ "$n" -ge 2 ]] || return 0
  gates="$(exclude_gates "$3" | cut -f1)"
  case "$1" in PLATFORMS) atom=p ;; *) atom=k ;; esac
  while IFS= read -r v; do
    [[ -z "$v" ]] && continue
    grep -qF "'$v' in $1" <<< "$gates" || continue
    c="$(catalogue_paths "$atom:$v" | grep -c . || true)"
    if [[ "$c" -gt "$best_n" ]]; then best="$v"; best_n="$c"; fi
  done < <(answer_list "$1" "$2")
  [[ -z "$best" ]] || printf '%s' "$best"
}

# The answer without one value, as Copier's --data takes a list: [a,b] with no spaces.
list_without() { # $1 = key, $2 = answers file, $3 = the value to drop
  answer_list "$1" "$2" | grep -vxF "$3" | paste -sd, - | sed 's/^/[/; s/$/]/'
}

# The LFS tripwire exactly as copier.yml's copy-time task runs it (DESIGN.md D19): the folded
# `command: >-` whose first line tests filter.lfs.process, joined into one shell line. Prints
# nothing when copier.yml carries no such task. toolkit-smoke.sh check 8 applies it.
lfs_tripwire_command() { # $1 = copier.yml (default: the repository's)
  awk '
    /^[[:space:]]*- command: >-[[:space:]]*$/ { buf = ""; on = 1; next }
    on && /^[[:space:]]*(when|- command):/ { if (buf ~ /filter\.lfs\.process/) { print buf; exit } on = 0; next }
    on { l = $0; sub(/^[[:space:]]+/, "", l); buf = (buf == "" ? l : buf " " l) }
  ' "${1:-$SM_ROOT/copier.yml}" 2>/dev/null
}

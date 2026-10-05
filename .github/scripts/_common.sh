#!/usr/bin/env bash
#
# _common.sh — the one home for what every syntek-media audit reads. Sourced, never run.
#
#              Twenty audits ask overlapping questions of the same four inputs: copier.yml
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
#                - the DESIGN.md catalogue: skills, mode files, gated paths, seeds, examples,
#                  the ten copy-only shared files, the spine set, the identity tokens, the
#                  companion skills, pair-only folders and pair exemptions, the D13 allow, ask
#                  and deny lists, and the _message_after_copy lines;
#                - a reader for a rendered tree's answers (multiselect lists included), a gate
#                  evaluator, and the over-author scope (<render>.owned, DESIGN.md Section 7);
#                - syntek-author's names: the frozen file (syntek-author-names.txt, D27), the
#                  generator that lists a live tree's names, and the drift between the two;
#                - the rendering helpers (snapshot a working tree, render media, render
#                  syntek-author, apply media over it) and the two fixture templates the
#                  integration self-tests run against.
#
#              The catalogue is DESIGN.md transcribed. When DESIGN.md changes, this file
#              changes in the same commit; every audit that reads it then moves together.
#              syntek-author's names are never transcribed here: they are read from
#              syntek-author-names.txt, which only `coexist-test.sh --refresh-names` writes.
#
#              Nothing here writes to the repository. Fixtures and snapshots go to mktemp.
#
# Requirements: bash 4.3+, git, grep, awk, sed. rsync and uvx only for the rendering helpers.

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
      sub(/[ \t]+#.*$/, "", s); sub(/[ \t]+$/, "", s)
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
      sub(/^[ \t]+/, "", s); sub(/[ \t]+#.*$/, "", s); sub(/[ \t]+$/, "", s)
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
#   k:<media kind> — joined with & for "and". p: and k: are list membership in PLATFORMS and
#   MEDIA_KINDS, which are always asked and never empty, so they carry no BRAND_KIND test
#   (DESIGN.md D15). `author` (BRAND_KIND != 'business') is vocabulary only: no Section 3.5
#   path ships on it, so it is not a shipping gate an index row may use.

SM_KINDS="business author-fiction author-nonfiction"
# The three own-channel platforms joined in 0.2.0 (DESIGN.md D53); the per-kind defaults below
# did not change (D54).
SM_PLATFORMS="youtube tiktok instagram linkedin facebook podcast website blog newsletter"
SM_MEDIA_KINDS="short-video long-video podcast audiobook trailer voiceover"

declare -A SM_GATE_EXPR=(
  [business]="BRAND_KIND == 'business'"
  [fiction]="BRAND_KIND == 'author-fiction'"
  [nonfiction]="BRAND_KIND == 'author-nonfiction'"
  [author]="BRAND_KIND != 'business'"
)
for _sm_x in $SM_PLATFORMS;   do SM_GATE_EXPR["p:$_sm_x"]="'$_sm_x' in PLATFORMS"; done
for _sm_x in $SM_MEDIA_KINDS; do SM_GATE_EXPR["k:$_sm_x"]="'$_sm_x' in MEDIA_KINDS"; done
unset _sm_x

# The shipping gates of DESIGN.md Section 3.5, in the vocabulary: the three mode gates and
# every list-membership gate. Index rows may use exactly these (check-template-tokens.sh check 9).
SM_SHIPPING_ATOMS="business fiction nonfiction$(for p in $SM_PLATFORMS; do printf ' p:%s' "$p"; done)$(for k in $SM_MEDIA_KINDS; do printf ' k:%s' "$k"; done)"

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

# The skill contract (DESIGN.md Section 5), as skill-conformance.sh compares it. The mode
# paragraph is syntek-author's with the three names swapped, and is compared whitespace- and
# `> `-normalised; the guard sentence is syntek-author's, verbatim, in every skill that names a
# credit-spending ElevenLabs tool (SM_SETTINGS_ASK lists those tools).
SM_MODE_PARA="**Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of \`BUSINESS.md\`, \`FICTION.md\`, \`NONFICTION.md\` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author."
SM_MODE_H2S="Paths and unit|Additions to the steps|Domain rules|Examples"
SM_GUARD_SENTENCE="If nothing was asked, stop: never generate unasked, including as a 'helpful' extra after another skill."
SM_SKILL_KEYS="name description context agent background model metadata"
SM_SKILL_H1_TOKEN="<%BRAND_NAME%>"
SM_GOVERNING_LINE="## Governing procedures (route here — do not restate at length)"

# The shared MEMORY.md's six headings (DESIGN.md Section 4.1, syntek-author's), and the texts an
# update must print or refuse with (D14, D16).
SM_MEMORY_H2S=("Facts" "Decisions" "Feedback" "Status" "Open questions" "Sensitivities")
SM_KIND_REFUSAL="BRAND_KIND cannot change on update"
SM_BEFORE_UPDATE_MARK="Before you answer: removing a platform or a media kind deletes"

mode_for_kind() { # business → BUSINESS.md
  case "$1" in business) echo BUSINESS.md ;; author-fiction) echo FICTION.md ;; author-nonfiction) echo NONFICTION.md ;; esac
}
kind_for_mode() { # BUSINESS.md → business
  case "$1" in BUSINESS.md) echo business ;; FICTION.md) echo author-fiction ;; NONFICTION.md) echo author-nonfiction ;; esac
}
modes_list() { # BFN → BUSINESS.md FICTION.md NONFICTION.md
  local out=""
  [[ "$1" == *B* ]] && out+="BUSINESS.md "
  [[ "$1" == *F* ]] && out+="FICTION.md "
  [[ "$1" == *N* ]] && out+="NONFICTION.md "
  printf '%s' "${out% }"
}

# Required and gated paths (DESIGN.md Sections 3–4; MANIFEST). Skills and mode files are
# SM_SKILLS's; folder pairs are docs-pairing.sh's; a workflow's STEPS.md and CHECKLIST.md are
# docs-pairing.sh check 12's. kind: d = directory, f = file.
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
always        d  publishing/docs/reference
always        d  publishing/docs/project
always        d  publishing/src
always        d  publishing/workflows/local
always        f  publishing/docs/reference/cut-downs.md
always        f  publishing/docs/reference/captions.md
always        f  publishing/docs/reference/thumbnails.md
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
always        f  toolkit/card.py
always        f  toolkit/data/platforms.toml
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
# retired agent and command tiers (D6), and the root files no template seeds (Section 9).
SM_NEVER="copier.yml DESIGN.md CHANGELOG.md VERSION examples template .copier-answers.yml .github .claude/agents .claude/commands CLAUDE.md .gitattributes"

# syntek-author's paths, which a standalone media render never ships (DESIGN.md Section 9,
# "Media never ships"). Its 51 skill folders are added from syntek-author-names.txt.
SM_AUTHOR_NEVER="Makefile .claude/hooks .claude/rules/syntek-author handoffs learning assets build manuscript library planning research proposal typeset world standards tooling"

# The first segments of syntek-author's paths, and its two named files, that media never
# backticks (doc-references.sh check 6).
SM_AUTHOR_PATH_HEADS="standards manuscript library planning research proposal typeset world tooling handoffs learning assets"
SM_AUTHOR_PATH_PREFIXES=".claude/rules/syntek-author"
SM_AUTHOR_FILE_NAMES="Makefile 00-project.md"

# The ten copy-only shared files (DESIGN.md D11, Section 3.6).
SM_SHARED="README.md CONTEXT.md .gitignore .mcp.json .claude/CLAUDE.md .claude/CONTEXT.md .claude/MEMORY.md .claude/settings.json .claude/skills/CONTEXT.md .claude/skills/CLAUDE.md"
SM_SHARED_GATE="_copier_operation == 'update'"

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

# The root spine (DESIGN.md Section 2, Token discipline). The ten shared files, the seeds and
# the examples are spine through their own sets; index files are computed.
SM_ROOT_SPINE="$SM_ANSWERS_FILE"
SM_ROOT_SPINE_GLOBS=".claude/rules/syntek-media/*.md"

# Tokens that may appear anywhere (DESIGN.md Section 2): identity and locale.
SM_IDENTITY_TOKENS="BRAND_NAME BRAND_SLUG OWNER_NAME OWNER_FIRST_NAME DATE TIMEZONE"
SM_COPIER_VARS="_copier_operation _copier_answers _copier_conf"

# syntek-author's skills media names in prose and never ships (DESIGN.md D10, Section 5.2).
SM_COMPANIONS="spelling grammar comprehension flow fact-check improve-section adapt-section research grilling grill-with-docs handoff wayfinder social-media-documents run-workflow pronounce"

# The standalone settings seed (DESIGN.md D13). Arrays: the entries carry spaces.
SM_SETTINGS_DENY=("AskUserQuestion" "Edit(**/generated/**)" "Edit(**/renders/**)")
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
)
SM_SETTINGS_BANNED_KEYS="hooks effortLevel ultracode enabledPlugins"   # and every disable* key

# What _message_after_copy must say, in DESIGN.md D13's order: (1) the ten shared files and the
# skip rule, that Copier's 'conflict' then 'skip' pair is expected, and Section 8's hand edits 2
# and 3 (the optional line in .claude/CLAUDE.md; nothing to add to .gitignore or .mcp.json);
# (2) the four Bash allows, the nine asks and the two Edit denies to add by hand (DESIGN.md
# Section 8); (3) the user-scope `claude mcp add` line with ELEVENLABS_MCP_BASE_PATH; (4) the
# repository-local filter.lfs.required and `git lfs install`; (5) the setup check; (6) the
# update command with -a.
# Each entry is a fragment the copy output must carry, matched with whitespace collapsed and
# Copier's own file-operation lines removed. generate-all.sh check 4 and coexist-test.sh
# check 19 read this list; shipped-seeds.sh check 12 reads the settings lists above.
SM_AFTER_COPY_LINES=()
for _sm_x in $SM_SHARED; do SM_AFTER_COPY_LINES+=("$_sm_x"); done
SM_AFTER_COPY_LINES+=("skip")
for _sm_x in "${SM_SETTINGS_ALLOW[@]}"; do [[ "$_sm_x" == Bash\(* ]] && SM_AFTER_COPY_LINES+=("$_sm_x"); done
SM_AFTER_COPY_LINES+=("${SM_SETTINGS_ASK[@]}")
for _sm_x in "${SM_SETTINGS_DENY[@]}"; do [[ "$_sm_x" == Edit\(* ]] && SM_AFTER_COPY_LINES+=("$_sm_x"); done
SM_AFTER_COPY_LINES+=("claude mcp add" "ELEVENLABS_MCP_BASE_PATH=" "filter.lfs.required" "git lfs install"
                      "python3 toolkit/media.py check --setup" "copier update" "-a $SM_ANSWERS_FILE")
SM_AFTER_COPY_LINES+=("'conflict' then 'skip'" ".claude/rules/syntek-media/ in .claude/CLAUDE.md"
                      "Nothing needs adding to .gitignore or .mcp.json")
unset _sm_x

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
# a handoffs/ folder media's rules create standalone (no pair, ever).
exempt_dir() { # tree-relative dir; true when it needs no pair
  case "/$1/" in
    */.git/*|*/build/*|*/audio/*|*/__pycache__/*|*/node_modules/*) return 0 ;;
    /.claude/rules/*) return 0 ;;
    /.claude/skills/*/*) return 0 ;;
    */drafts/*) return 0 ;;
    */.base/*) return 0 ;;
    */generated/*|*/renders/*|*/raw/*) return 0 ;;
    /handoffs/*) return 0 ;;
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

A_KIND=""; A_PLATFORMS=""; A_KINDS=""; A_SEED=true

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
  return 0
}

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
  done < <(cd "$t" && find . -name .git -prune -o -type f -print0)
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
  (cd "$1" && find . -name .git -prune -o -type f -print | sed 's#^\./##' | LC_ALL=C sort)
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

sm_render() { # $1 = template, $2 = dest, $3 = BRAND_KIND, then extra copier arguments
  local src="$1" dest="$2" kind="$3"; shift 3
  [[ ${#SM_COPIER[@]} -gt 0 ]] || copier_init
  "${SM_COPIER[@]}" copy --trust --defaults --vcs-ref=HEAD \
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
  (cd "$proj" && "${SM_COPIER[@]}" update --trust --defaults --vcs-ref=HEAD \
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
  sm_render "$msnap" "$dest" "$kind" "$@" || OA_MEDIA_STATUS=$?
  tree_files "$dest" | LC_ALL=C comm -13 "$before" - > "$dest.owned"
  rm -f "$before"
  return "$OA_MEDIA_STATUS"
}

# ── The fixture templates ────────────────────────────────────────────────────
#
# sm_fixture_template: a minimal syntek-media with the real repository's shape — the house
# delimiters, the named answers file, the ten copy-only shared files, a register seed and a
# brand seed, a gated profile and platform guide per platform, the podcast platform's gate on
# the pair-only folder of the show registers (DESIGN.md D59), the audiobook gate on a folder
# and a skill, one seed-once example, a moded skill with its generated mode block, the D14
# guard (the previous answers through _external_data, BRAND_KIND's validator), the static
# _message_before_update, and a _message_after_copy carrying every SM_AFTER_COPY_LINES fragment.
# sm_author_fixture_template: syntek-author's own fixture, ported from its _common.sh — its
# answers file, its D17 seeds, its rules folder, its run-workflow skill and its Makefile.
# The integration self-tests run their whole flow against these, so the harness is proven
# independently of the real template's state — which, mid-build, may not render at all.

sm_fixture_template() { # $1 = dest (created, git-initialised and committed)
  local t="$1" p k s m q="'"
  rm -rf "$t"; mkdir -p "$t/template"
  {
    cat <<'EOF'
_min_copier_version: "9.6.0"
_subdirectory: template
_answers_file: .copier-answers.syntek-media.yml
_external_data:
  prev: .copier-answers.syntek-media.yml
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
_message_after_copy: |
EOF
    printf '  Shared files, written only where absent (a skip left yours exactly as it was):\n'
    for p in $SM_SHARED; do printf '    %s\n' "$p"; done
    printf '  Copier lists an existing one as %sconflict%s then %sskip%s; that pair is expected.\n' "$q" "$q" "$q" "$q"
    printf '  Optional: name .claude/rules/syntek-media/ in .claude/CLAUDE.md.\n'
    printf '  Nothing needs adding to .gitignore or .mcp.json.\n'
    printf '  Add these to an existing .claude/settings.json by hand:\n'
    for p in "${SM_SETTINGS_ALLOW[@]}"; do [[ "$p" == Bash\(* ]] && printf '    allow: %s\n' "$p"; done
    for p in "${SM_SETTINGS_ASK[@]}"; do printf '    ask: %s\n' "$p"; done
    for p in "${SM_SETTINGS_DENY[@]}"; do [[ "$p" == Edit\(* ]] && printf '    deny: %s\n' "$p"; done
    printf '  claude mcp add --scope user elevenlabs -- uvx elevenlabs-mcp\n'
    printf '    with --env ELEVENLABS_MCP_BASE_PATH="$HOME": the base path must contain the project.\n'
    printf '  This copy may have set filter.lfs.required in .git/config; git lfs install makes it harmless.\n'
    printf '  Then run: python3 toolkit/media.py check --setup\n'
    printf '  Update with: uvx copier update --trust -a .copier-answers.syntek-media.yml\n'
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
  printf '{"mcpServers": {}}\n' > .mcp.json
  printf '# CLAUDE.md — <%%BRAND_NAME%%>\n\n## 3. Project-specific rules\n' > .claude/CLAUDE.md
  printf '# CONTEXT.md — .claude/\n' > .claude/CONTEXT.md
  printf '# MEMORY.md — <%%BRAND_SLUG%%>\n\n## Facts\n\n## Decisions\n\n## Feedback\n\n## Status\n\n## Open questions\n\n## Sensitivities\n' > .claude/MEMORY.md
  {
    printf '{\n  "model": "opus",\n  "autoCompactEnabled": false,\n  "permissions": {\n'
    printf '    "deny": [%s],\n' "$(for s in "${SM_SETTINGS_DENY[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '    "allow": [%s],\n' "$(for s in "${SM_SETTINGS_ALLOW[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '    "ask": [%s]\n' "$(for s in "${SM_SETTINGS_ASK[@]}"; do printf '"%s", ' "$s"; done | sed 's/, $//')"
    printf '  }\n}\n'
  } > .claude/settings.json
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
  sm_git "$t" init -q && sm_git "$t" add -A && sm_git "$t" commit -q -m 'fixture template'
}

sm_author_fixture_template() { # $1 = dest (created, git-initialised and committed)
  local t="$1" d
  rm -rf "$t"; mkdir -p "$t/template"
  cat > "$t/copier.yml" <<'EOF'
_min_copier_version: "9.6.0"
_subdirectory: template
_answers_file: .copier-answers.syntek-author.yml
_external_data:
  prev: .copier-answers.syntek-author.yml
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
  cd "$t/template" || return 1
  mkdir -p .claude/skills/run-workflow .claude/skills/spelling .claude/hooks .claude/rules/syntek-author standards/style \
    manuscript/src/01-example-chapter library/src handoffs
  printf '<%% _copier_answers|to_nice_yaml -%%>\n' > "$SM_AUTHOR_ANSWERS"
  printf '# <%%PROJECT_NAME%%>\n\nA fixture project.\n' > README.md
  printf '# CONTEXT.md — <%%PROJECT_NAME%%>\n' > CONTEXT.md
  printf 'build/\n' > .gitignore
  printf '{"mcpServers": {}}\n' > .mcp.json
  printf '# CLAUDE.md — <%%PROJECT_NAME%%>\n\n## 3. Project-specific rules\n' > .claude/CLAUDE.md
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
  printf 'help:\n\t@echo help\n' > Makefile
  cd - >/dev/null || return 1
  sm_git "$t" init -q && sm_git "$t" add -A && sm_git "$t" commit -q -m 'fixture syntek-author'
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
  done < <(cd "$1" && find . -name .git -prune -o -type f -print0)
}

# The paths a step changed in a committed project — modified, added, deleted and untracked
# (every file of an untracked folder) — one per line, sorted. Ignored files are not changes.
changed_paths() { # $1 = project
  git -C "$1" status --porcelain -uall 2>/dev/null \
    | sed -E 's/^.{3}//; s/^.* -> //; s/^"(.*)"$/\1/' | LC_ALL=C sort -u
}

# path<TAB>sha1 for every file of a tree (.git left out), sorted by path: what "no byte
# changed" is measured against.
hash_tree() { # $1 = dir
  (cd "$1" && find . -name .git -prune -o -type f -print0 | LC_ALL=C sort -z | xargs -0 -r sha1sum) \
    | sed -E 's#^([0-9a-f]+)  \./(.*)$#\2\t\1#' | LC_ALL=C sort
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

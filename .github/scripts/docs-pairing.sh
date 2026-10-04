#!/usr/bin/env bash
#
# docs-pairing.sh — Enforce the folder pair, and the shapes of the files that carry routing.
#
#                   Every directory a generated project contains carries CONTEXT.md (what is
#                   here and why) and CLAUDE.md (how to work here). That pair is how Claude
#                   finds its way: the read order walks it top-down, and a folder without it is
#                   a folder nobody was told how to work in. The exceptions are DESIGN.md D42's
#                   and only those (.claude/rules/syntek-media/01-layout-and-routing.md Section
#                   6): syntek-author's, verbatim — build/, .git/, audio/, __pycache__/,
#                   node_modules/, .claude/rules/ (a CONTEXT.md there would LOAD AS A RULE), the
#                   inside of each skill folder, each drafts/ and each .base/ (README only) —
#                   then media's: each generated/, renders/ and raw/ folder carries only a
#                   README.md (everything else in it is git-ignored), and a handoffs/ folder
#                   media's rules create standalone carries none (its pair is syntek-author's).
#                   The project root carries CONTEXT.md; its CLAUDE.md is .claude/CLAUDE.md.
#                   Every piece folder carries its own pair, as syntek-author's unit folders do.
#
#                   The same audit holds the shapes the routing depends on: a CLAUDE.md that
#                   does not import its CONTEXT.md loads half a folder; a workflow without its
#                   CHECKLIST.md cannot be ticked; a STEPS.md step without its Skill line routes
#                   nowhere; a guide without its Governing standard section restates a rule it
#                   should cite.
#
#                   Nineteen checks — syntek-author's seventeen, unchanged in meaning and number,
#                   then media's two:
#                     1. A directory has no CONTEXT.md.
#                     2. A directory has no CLAUDE.md (the root excepted).
#                     3. A CLAUDE.md does not open with @./CONTEXT.md.
#                     4. A CLAUDE.md has no `Read order:` line.
#                     5. A CLAUDE.md's H2s are not exactly: Purpose (one line) · How to work
#                        here · Guardrails · Output & naming.
#                     6. A CLAUDE.md carries a directory tree (it belongs in CONTEXT.md).
#                     7. A CONTEXT.md has no `## Directory Tree` with a text fence.
#                     8. A CONTEXT.md carries an operating-rule heading (Rules, Guardrails,
#                        Conventions, Requirements, Constraints, How to work here, Definition of
#                        done) — that belongs in CLAUDE.md.
#                     9. A CONTEXT.md tree row has no annotation.
#                    10. .claude/rules/ carries a CONTEXT.md or CLAUDE.md.
#                    11. A drafts/ folder lacks README.md, or carries a pair (media ships none;
#                        the check stands so one never arrives unnoticed).
#                    12. A workflow folder (layer/workflows/NN-name/) lacks STEPS.md or
#                        CHECKLIST.md.
#                    13. STEPS.md or CHECKLIST.md routing frontmatter is wrong: `workflow:` is
#                        not the folder name, `phase:` is not one of plan · research · produce ·
#                        review · publish · convert · author, `skills:` or `model:` is missing,
#                        or an `agent:` key is present (skills only — DESIGN.md D6).
#                    14. A CHECKLIST.md item does not end ` · _opus_` or ` · _sonnet_`.
#                    15. A STEPS.md step (## N.) does not open with `> **Skill:**`, or does not
#                        carry _Substantive._ or _Mechanical._ (a parenthetical before the full
#                        stop is allowed, and may wrap: _Substantive (the author's call)._).
#                    16. A guide (docs/reference/*.md) breaks the house format: frontmatter
#                        `type: guide`, `skills:`, `model:`; `**What it is.**`; the H2s How we
#                        apply it here, Who implements it, and Governing standard (last); 54–82
#                        lines (DESIGN.md D33).
#                    17. A STEPS.md, CHECKLIST.md or guide lacks the metadata header
#                        (**Last Updated** … **Version** … **Maintained By** …, then
#                        **Language**: British English (en_GB)). Media has no standards folder.
#                    18. A piece folder (scripts/src/pieces/NNN-kebab-title/) has no brief.md —
#                        the brief is where the piece's status and gates live (DESIGN.md D17).
#                    19. A generated/, renders/ or raw/ folder lacks README.md, or carries a pair
#                        (DESIGN.md D42).
#
#                   Numbers are stable identifiers. Append, never renumber.
#
#                   Block delimiters are stripped before a line is read, so a gated tree row in
#                   an index file is judged as the row it renders to; headings inside fenced
#                   code (an entry template quoted in a CLAUDE.md) are not read as headings.
#
#                   Over-author scope (DESIGN.md Section 7): on a tree with a <tree>.owned
#                   beside it, only media-owned folders and files are checked — syntek-author's
#                   own folders are its audit's business, and its exempt_dir does not know
#                   media's README-only folders.
#
#                   What it CANNOT check: whether a paragraph says anything. A script proves a
#                   heading and a tree exist; only a reader can tell whether they orient.
#
# SELF-TEST. --self-test builds a conformant tree at runtime — pairs, a skill, the rules folder,
#            a workflow, a guide, a piece folder, a generated/ folder — proves it clean, then
#            applies one mutation per check and asserts exactly one finding each.
#
# Requirements: bash 4+, grep, awk, sed, find. No network.
#
# Usage: docs-pairing.sh [--root DIR] [--quiet] [--self-test] [--help] [<tree>...]
#        With no tree, checks template/ in the repository.
#
# Exit codes:  0 = every pair present and every routed file in shape
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, a tree that does not exist)

set -euo pipefail
SCRIPT_NAME="docs-pairing.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
TARGETS=()

usage() {
  cat <<'EOF'
docs-pairing.sh — Enforce the folder pair, and the shapes of the files that carry routing

Usage: docs-pairing.sh [--root DIR] [--quiet] [--self-test] [--help] [<tree>...]

  <tree>       A rendered project, or any directory shaped like one
               (default: template/ in the repository)
  --root DIR   The template repository (default: this repository)
  --quiet      Print findings only
  --self-test  Prove the checks still fire against a tree built at runtime
  --help       Show this message

A <tree>.owned file marks an over-author tree: only media-owned folders are checked.
Exit codes: 0 = clean  1 = finding(s), or the self-test no longer separates
            2 = script error
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)      [[ $# -gt 1 ]] || die "--root needs a value"; SM_ROOT="$(cd "$2" && pwd)" || die "no such directory: $2"; shift 2 ;;
    --quiet|-q)  QUIET=true; shift ;;
    --self-test) SELF_TEST=true; shift ;;
    --help|-h)   usage; exit 0 ;;
    -*)          die "unknown argument: $1" ;;
    *)           TARGETS+=("$1"); shift ;;
  esac
done

TREE=""
DIRS_CHECKED=0
FILES_CHECKED=0
PHASES="plan research produce review publish convert author"
CLAUDE_H2='Purpose (one line)|How to work here|Guardrails|Output & naming'
BANNED='^#{2,3} +(Rules|Guardrails|Conventions|Requirements|Constraints|How to work here|Definition of done)( |$)'

# Read a file with every block delimiter removed, so a gated row reads as the row it renders to.
unblocked() { sed -E 's/<:([^:]|:[^>])*:>//g' "$1"; }
# …and with fenced code removed, so a heading quoted in a sample is not read as one.
unfenced() { unblocked "$1" | awk '/^[[:space:]]*```/ { f = !f; next } !f'; }

frontmatter() { # the lines between the opening --- and the closing --- (empty if none)
  awk 'NR == 1 && $0 != "---" { exit } NR == 1 { next } /^---[[:space:]]*$/ { exit } { print }' "$1"
}
fm_value() { # $1 = key, stdin = frontmatter
  awk -v k="$1" '$0 ~ "^" k ":" { v = $0; sub("^" k ":[ \t]*", "", v); print v; exit }'
}

is_guide() { # tree-relative path
  [[ "$1" == */docs/reference/*.md || "$1" == docs/reference/*.md ]] || return 1
  local b="${1##*/}"
  [[ "$b" == CONTEXT.md || "$b" == CLAUDE.md ]] && return 1
  [[ "$b" =~ ^[A-Z0-9-]+\.md$ ]] && return 1     # SCREAMING-CASE sub-docs behind an index
  [[ "$1" == */docs/reference/*/* ]] && return 1
  return 0
}

has_header() { # file carries both metadata lines
  grep -qE '^\*\*Last Updated\*\*: .+ \*\*Version\*\*: .+ \*\*Maintained By\*\*: .+' "$1" \
    && grep -qE '^\*\*Language\*\*: British English \(en_GB\)' "$1"
}

check_claude() { # $1 = rel
  local f="$TREE/$1" first h2
  [[ "$1" == .claude/CLAUDE.md ]] && return 0
  FILES_CHECKED=$((FILES_CHECKED + 1))
  first="$(unblocked "$f" | grep -m1 '[^[:space:]]' || true)"
  [[ "$first" == '@./CONTEXT.md' ]] || finding "check 3 — $1 does not open with @./CONTEXT.md"
  grep -q '^Read order:' "$f" || finding "check 4 — $1 has no 'Read order:' line"
  h2="$(unfenced "$f" | grep '^## ' | sed 's/^## //; s/[[:space:]]*$//' | paste -sd'|' -)"
  [[ "$h2" == "$CLAUDE_H2" ]] || finding "check 5 — $1 has H2s '${h2:-none}'; expected '$CLAUDE_H2'"
  grep -q '^```text' "$f" && finding "check 6 — $1 carries a directory tree; it belongs in CONTEXT.md"
  return 0
}

check_context() { # $1 = rel
  local f="$TREE/$1" h r
  FILES_CHECKED=$((FILES_CHECKED + 1))
  if ! grep -q '^## Directory Tree' "$f" || ! grep -q '^```text' "$f"; then
    finding "check 7 — $1 has no '## Directory Tree' with a text fence"
  fi
  while IFS= read -r h; do
    finding "check 8 — $1 carries the heading '$h' — an operating rule belongs in CLAUDE.md"
  done < <(unfenced "$f" | grep -E "$BANNED" || true)
  while IFS= read -r r; do
    finding "check 9 — $1 has a tree row '$r' with no annotation"
  done < <(unblocked "$f" | awk '
    /^```text/ { inb = 1; next }
    inb && /^```/ { inb = 0 }
    inb && /^(├|└)── / {
      row = $0; sub(/^(├|└)── /, "", row)
      name = row; sub(/[[:space:]].*$/, "", name)
      rest = substr(row, length(name) + 1); gsub(/[[:space:]]/, "", rest)
      if (rest == "") print name
    }')
}

check_workflow() { # $1 = rel dir of a workflow folder
  local d="$1" f fm v name="${1##*/}" line
  for f in STEPS.md CHECKLIST.md; do
    if [[ ! -f "$TREE/$d/$f" ]]; then finding "check 12 — $d/ has no $f"; continue; fi
    FILES_CHECKED=$((FILES_CHECKED + 1))
    fm="$(frontmatter "$TREE/$d/$f")"
    if [[ -z "$fm" ]]; then finding "check 13 — $d/$f has no routing frontmatter"; continue; fi
    v="$(fm_value workflow <<< "$fm")"
    [[ "$v" == "$name" ]] || finding "check 13 — $d/$f says workflow: '${v}'; the folder is $name"
    v="$(fm_value phase <<< "$fm")"
    [[ " $PHASES " == *" $v "* ]] || finding "check 13 — $d/$f has phase: '${v}'; expected one of: $PHASES"
    grep -q '^skills:' <<< "$fm" || finding "check 13 — $d/$f routing frontmatter has no skills:"
    grep -q '^model:' <<< "$fm" || finding "check 13 — $d/$f routing frontmatter has no model:"
    grep -q '^agent:' <<< "$fm" && finding "check 13 — $d/$f carries an agent: key — skills only (DESIGN.md D6)"
    has_header "$TREE/$d/$f" || finding "check 17 — $d/$f has no metadata header"
  done
  if [[ -f "$TREE/$d/CHECKLIST.md" ]]; then
    while IFS= read -r line; do
      finding "check 14 — $d/CHECKLIST.md item has no model tag: ${line:0:70}"
    done < <(grep -E '^[[:space:]]*- \[[ xX]\] ' "$TREE/$d/CHECKLIST.md" | grep -vE ' · _(opus|sonnet)_[[:space:]]*$' || true)
  fi
  if [[ -f "$TREE/$d/STEPS.md" ]]; then
    while IFS= read -r line; do
      finding "check 15 — $d/STEPS.md $line"
    done < <(awk '
      function close_step() {
        if (step == "") return
        if (!skill) print "step \"" step "\" does not open with > **Skill:**"
        if (!tag) print "step \"" step "\" carries neither _Substantive._ nor _Mechanical._"
      }
      /^## / { close_step(); step = ""; if ($0 ~ /^## [0-9]+\. /) { step = substr($0, 4); skill = 0; tag = 0; first = 1 }; next }
      step != "" && first && /[^[:space:]]/ { first = 0; if ($0 ~ /^> \*\*Skill:\*\*/) skill = 1 }
      step != "" && /(^|[^A-Za-z])_(Substantive|Mechanical)([ ._(]|$)/ { tag = 1 }
      END { close_step() }' < <(unfenced "$TREE/$d/STEPS.md"))
  fi
}

check_guide() { # $1 = rel
  local f="$TREE/$1" fm n h2 last
  FILES_CHECKED=$((FILES_CHECKED + 1))
  fm="$(frontmatter "$f")"
  [[ "$(fm_value type <<< "$fm")" == guide ]] || finding "check 16 — $1 frontmatter does not say type: guide"
  grep -q '^skills:' <<< "$fm" || finding "check 16 — $1 frontmatter has no skills:"
  grep -q '^model:' <<< "$fm" || finding "check 16 — $1 frontmatter has no model:"
  grep -q '^\*\*What it is\.\*\*' "$f" || finding "check 16 — $1 has no '**What it is.**' opening"
  h2="$(unfenced "$f" | grep '^## ' | sed 's/^## //; s/[[:space:]]*$//')"
  grep -qx 'How we apply it here' <<< "$h2" || finding "check 16 — $1 has no '## How we apply it here'"
  grep -qx 'Who implements it' <<< "$h2" || finding "check 16 — $1 has no '## Who implements it'"
  last="$(tail -1 <<< "$h2")"
  [[ "$last" == 'Governing standard' ]] || finding "check 16 — $1 does not end with '## Governing standard' (last H2: '${last}')"
  n="$(wc -l < "$f")"
  [[ "$n" -ge 54 && "$n" -le 82 ]] || finding "check 16 — $1 is $n lines; a guide is 54–82"
  has_header "$f" || finding "check 17 — $1 has no metadata header"
}

run_checks() {
  FINDINGS=()
  DIRS_CHECKED=0; FILES_CHECKED=0
  local d f b
  while IFS= read -r -d '' d; do
    d="${d#./}"; [[ "$d" == . ]] && d=""
    if [[ -n "$d" ]] && exempt_dir "$d"; then
      continue
    fi
    is_owned_dir "$d" || continue
    DIRS_CHECKED=$((DIRS_CHECKED + 1))
    [[ -f "$TREE/${d:+$d/}CONTEXT.md" ]] || finding "check 1 — ${d:-the root}/ has no CONTEXT.md"
    if [[ -n "$d" && ! -f "$TREE/$d/CLAUDE.md" ]]; then finding "check 2 — $d/ has no CLAUDE.md"; fi
    [[ -f "$TREE/${d:+$d/}CLAUDE.md" && -n "$d" ]] && check_claude "$d/CLAUDE.md"
    [[ -f "$TREE/${d:+$d/}CONTEXT.md" ]] && check_context "${d:+$d/}CONTEXT.md"
    if [[ "$d" =~ ^[^/]+/workflows/[0-9][0-9]-[^/]+$ ]]; then check_workflow "$d"; fi
  done < <(cd "$TREE" && find . \( -name .git -o -name build -o -name audio -o -name __pycache__ -o -name node_modules \) -prune -o -type d -print0 | sort -z)

  # ── 10. Nothing in .claude/rules/ that would load as a rule ─────────────────
  if [[ -d "$TREE/.claude/rules" ]]; then
    while IFS= read -r f; do
      f="${f#./}"
      is_owned_file "$f" || continue
      finding "check 10 — $f sits in .claude/rules/, where it would load as a rule"
    done < <(cd "$TREE" && find ./.claude/rules \( -name CONTEXT.md -o -name CLAUDE.md \) | sort)
  fi

  # ── 11. drafts/ carries README.md, never a pair ─────────────────────────────
  while IFS= read -r d; do
    d="${d#./}"
    is_owned_dir "$d" || continue
    [[ -f "$TREE/$d/README.md" ]] || finding "check 11 — $d/ has no README.md"
    if [[ -f "$TREE/$d/CONTEXT.md" || -f "$TREE/$d/CLAUDE.md" ]]; then finding "check 11 — $d/ carries a pair; a drafts/ folder carries README.md only"; fi
  done < <(cd "$TREE" && find . -name .git -prune -o -type d -name drafts -print | sort)

  # ── 16–17. Guides ───────────────────────────────────────────────────────────
  while IFS= read -r -d '' f; do
    f="${f#./}"
    is_owned_file "$f" || continue
    if is_guide "$f"; then check_guide "$f"; fi
  done < <(cd "$TREE" && find . -name .git -prune -o -path '*/docs/reference/*' -name '*.md' -print0 | sort -z)

  # ── 18. A piece folder carries its brief ────────────────────────────────────
  if [[ -d "$TREE/scripts/src/pieces" ]]; then
    while IFS= read -r d; do
      is_owned_dir "scripts/src/pieces/$d" || continue
      [[ -f "$TREE/scripts/src/pieces/$d/brief.md" ]] \
        || finding "check 18 — scripts/src/pieces/$d/ has no brief.md — a piece's status and gates live in its brief (DESIGN.md D17)"
    done < <(find "$TREE/scripts/src/pieces" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
  fi

  # ── 19. generated/, renders/ and raw/ carry README.md only ──────────────────
  while IFS= read -r d; do
    d="${d#./}"
    is_owned_dir "$d" || continue
    b="${d##*/}"
    [[ -f "$TREE/$d/README.md" ]] || finding "check 19 — $d/ has no README.md — a $b/ folder says what lands in it and that Git ignores it"
    if [[ -f "$TREE/$d/CONTEXT.md" || -f "$TREE/$d/CLAUDE.md" ]]; then finding "check 19 — $d/ carries a pair; a $b/ folder carries README.md only (DESIGN.md D42)"; fi
  done < <(cd "$TREE" && find . -name .git -prune -o -type d \( -name generated -o -name renders -o -name raw \) -print | sort)
}

# ── Self-test ────────────────────────────────────────────────────────────────

HEADER=$'**Last Updated**: 01/01/2027 **Version**: 0.1.0 **Maintained By**: Ada Example\n**Language**: British English (en_GB)'

write_pair() { # $1 = tree, $2 = rel dir ("" for root: CONTEXT only)
  local t="$1" d="$2" label="${2:-.}"
  mkdir -p "$t/${d:-.}"
  printf '# CONTEXT.md — %s/\n\nWhat this folder holds, and why.\n\n## Directory Tree\n\n```text\n%s/\n├── CONTEXT.md   ← this file\n└── CLAUDE.md    ← operating rules\n```\n\n## Cross-references\n\n- None.\n' \
    "$label" "$label" > "$t/${d:+$d/}CONTEXT.md"
  [[ -z "$d" ]] && return 0
  printf '@./CONTEXT.md\n\n# CLAUDE.md — %s/\n\nRead order: `.claude/CLAUDE.md` → this file.\n\n## Purpose (one line)\n\nOne line.\n\n## How to work here\n\n- **Routing:** none.\n\n## Guardrails\n\n- **Never overwrite.**\n\n## Output & naming\n\n- Kebab-case.\n' \
    "$d" > "$t/$d/CLAUDE.md"
}

write_fixture() { # $1 = tree
  local t="$1" d i f wf="production/workflows/02-make-a-voiceover" piece="scripts/src/pieces/003-why-the-ferry-runs-late"
  write_pair "$t" ""
  mkdir -p "$t/.claude/rules/syntek-media" "$t/.claude/skills/voiceover"
  printf '# CLAUDE.md — Probe Studio\n\nThe project brief.\n' > "$t/.claude/CLAUDE.md"
  printf '# CONTEXT.md — .claude/\n\nOrientation.\n\n## Directory Tree\n\n```text\n.claude/\n└── CLAUDE.md   ← the brief\n```\n' > "$t/.claude/CONTEXT.md"
  printf '# 01-layout-and-routing.md — layout and routing\n' > "$t/.claude/rules/syntek-media/01-layout-and-routing.md"
  write_pair "$t" .claude/skills
  printf -- '---\nname: voiceover\n---\n' > "$t/.claude/skills/voiceover/SKILL.md"
  printf 'x\n' > "$t/.claude/skills/voiceover/BUSINESS.md"
  for d in production production/docs production/docs/reference production/workflows "$wf" production/src \
           production/src/voiceover scripts scripts/src scripts/src/pieces "$piece"; do
    write_pair "$t" "$d"
  done
  printf -- '---\npiece: 003-why-the-ferry-runs-late\nstatus: idea\n---\n\n# Why the ferry runs late — brief\n' > "$t/$piece/brief.md"
  mkdir -p "$t/production/src/voiceover/generated" "$t/production/src/renders"
  printf '# generated/\n\nTakes land here; Git ignores them.\n' > "$t/production/src/voiceover/generated/README.md"
  printf '# renders/\n\nMasters land here; Git ignores them.\n' > "$t/production/src/renders/README.md"
  for f in STEPS CHECKLIST; do
    printf -- '---\nworkflow: 02-make-a-voiceover\nphase: produce\nskills: [voiceover]\nmodel: opus\n---\n\n# %s.md — make a voiceover\n\n%s\n\n' "$f" "$HEADER" > "$t/$wf/$f.md"
  done
  printf '## 1. Confirm the request\n\n> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`\n\nConfirm what was asked. _Substantive._\n' >> "$t/$wf/STEPS.md"
  printf '## Pre-Conditions\n\n- [ ] Read the brief. · _sonnet_\n\n## Execution Checklist\n\n- [ ] Generated. · _opus_\n\n## Done When\n\n- [ ] **One approved take per segment.** · _opus_\n' >> "$t/$wf/CHECKLIST.md"
  {
    printf -- '---\ntype: guide\nskills: [voiceover]\nmodel: opus\n---\n\n# Voiceover — segments and the register\n\n%s\n\n**What it is.** A voiceover is made one segment at a time.\n\n## Segments\n\n' "$HEADER"
    for i in $(seq 1 34); do printf 'Line %d of the topic.\n' "$i"; done
    printf '\n## How we apply it here\n\nOne sentence or beat per segment.\n\n## Who implements it\n\nThe voiceover skill.\n\n## Governing standard\n\nThe rules own the rule; this guide owns the explanation.\n'
  } > "$t/production/docs/reference/voiceover.md"
}

self_test() {
  local tmp t wf="production/workflows/02-make-a-voiceover" g="production/docs/reference/voiceover.md" f
  local piece="scripts/src/pieces/003-why-the-ferry-runs-late"
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  t="$tmp/gen"; TREE="$t"; load_owned "$TREE"
  write_fixture "$t"
  st_baseline "a conformant tree"

  mkdir -p "$t/handoffs"; printf '# A handoff\n' > "$t/handoffs/HANDOFF-PROBE-01-01-2027.md"
  probe_clean "a handoffs/ folder created standalone carries no pair, by design"; rm -rf "$t/handoffs"
  mkdir -p "$t/production/src/footage/raw"; write_pair "$t" production/src/footage
  printf '# raw/\n\nThe local mirror; Git ignores it.\n' > "$t/production/src/footage/raw/README.md"
  probe_clean "a raw/ folder with only README.md is a declared exception"; rm -rf "$t/production/src/footage"

  mv "$t/production/src/CONTEXT.md" "$tmp/h"; probe "check 1 fires on a folder with no CONTEXT.md" "check 1 — production/src/"; mv "$tmp/h" "$t/production/src/CONTEXT.md"
  mv "$t/production/src/CLAUDE.md" "$tmp/h";  probe "check 2 fires on a folder with no CLAUDE.md" "check 2 — production/src/"; mv "$tmp/h" "$t/production/src/CLAUDE.md"
  cp "$t/scripts/CLAUDE.md" "$tmp/h"
  sed -i '1s/.*/# no import/' "$t/scripts/CLAUDE.md";          probe "check 3 fires when the import is lost" "check 3"; cp "$tmp/h" "$t/scripts/CLAUDE.md"
  sed -i '/^Read order:/d' "$t/scripts/CLAUDE.md";             probe "check 4 fires when the read order is lost" "check 4"; cp "$tmp/h" "$t/scripts/CLAUDE.md"
  sed -i 's/^## Guardrails/## Rules/' "$t/scripts/CLAUDE.md";   probe "check 5 fires on a renamed H2" "check 5"; cp "$tmp/h" "$t/scripts/CLAUDE.md"
  printf '```text\nscripts/\n```\n' >> "$t/scripts/CLAUDE.md";   probe "check 6 fires on a tree in CLAUDE.md" "check 6"; cp "$tmp/h" "$t/scripts/CLAUDE.md"
  cp "$t/scripts/CONTEXT.md" "$tmp/h"
  sed -i 's/^## Directory Tree/## Layout/' "$t/scripts/CONTEXT.md"; probe "check 7 fires when the tree heading is lost" "check 7"; cp "$tmp/h" "$t/scripts/CONTEXT.md"
  printf '\n## Conventions\n\n- A rule.\n' >> "$t/scripts/CONTEXT.md"; probe "check 8 fires on a rule heading in CONTEXT.md" "check 8"; cp "$tmp/h" "$t/scripts/CONTEXT.md"
  sed -i 's/^└── CLAUDE.md    ← operating rules/└── CLAUDE.md/' "$t/scripts/CONTEXT.md"; probe "check 9 fires on a bare tree row" "check 9"; cp "$tmp/h" "$t/scripts/CONTEXT.md"
  printf '# x\n' > "$t/.claude/rules/CONTEXT.md";              probe "check 10 fires on a pair in .claude/rules/" "check 10"; rm -f "$t/.claude/rules/CONTEXT.md"
  mkdir -p "$t/production/src/voiceover/drafts";               probe "check 11 fires on a drafts/ with no README.md" "check 11"; rmdir "$t/production/src/voiceover/drafts"
  mv "$t/$wf/STEPS.md" "$tmp/h";                               probe "check 12 fires on a workflow with no STEPS.md" "check 12"; mv "$tmp/h" "$t/$wf/STEPS.md"
  cp "$t/$wf/CHECKLIST.md" "$tmp/h"
  sed -i 's/^workflow: .*/workflow: 02-wrong-name/' "$t/$wf/CHECKLIST.md"; probe "check 13 fires on a workflow key that is not the folder" "check 13"; cp "$tmp/h" "$t/$wf/CHECKLIST.md"
  sed -i 's/^model: opus/model: opus\nagent: editor/' "$t/$wf/CHECKLIST.md"; probe "check 13 fires on an agent key" "check 13 — $wf/CHECKLIST.md carries an agent"; cp "$tmp/h" "$t/$wf/CHECKLIST.md"
  sed -i 's/Generated\. · _opus_/Generated./' "$t/$wf/CHECKLIST.md"; probe "check 14 fires on an untagged item" "check 14"; cp "$tmp/h" "$t/$wf/CHECKLIST.md"
  cp "$t/$wf/STEPS.md" "$tmp/h"
  sed -i '/^> \*\*Skill:\*\*/d' "$t/$wf/STEPS.md";            probe "check 15 fires on a step with no Skill line" "check 15"; cp "$tmp/h" "$t/$wf/STEPS.md"
  cp "$t/$g" "$tmp/h"
  sed -i 's/^## Who implements it/## Who does it/' "$t/$g";   probe "check 16 fires on a guide missing a section" "check 16"; cp "$tmp/h" "$t/$g"
  sed -i '/^Line [0-9]* of the topic\./d' "$t/$g";            probe "check 16 fires on a guide that is too short" "check 16 — $g is"; cp "$tmp/h" "$t/$g"
  sed -i '/^\*\*Language\*\*/d' "$t/$g";                      probe "check 17 fires on a guide with no header" "check 17"; cp "$tmp/h" "$t/$g"
  mv "$t/$piece/brief.md" "$tmp/h";                           probe "check 18 fires on a piece folder with no brief" "check 18 — $piece/"; mv "$tmp/h" "$t/$piece/brief.md"
  mv "$t/production/src/renders/README.md" "$tmp/h";          probe "check 19 fires on a renders/ with no README.md" "check 19 — production/src/renders/ has no README.md"; mv "$tmp/h" "$t/production/src/renders/README.md"
  printf '# x\n' > "$t/production/src/voiceover/generated/CONTEXT.md"
  probe "check 19 fires on a generated/ that carries a pair" "check 19 — production/src/voiceover/generated/ carries a pair"
  rm -f "$t/production/src/voiceover/generated/CONTEXT.md"

  # Over syntek-author: its folders are its own audit's; media's are checked as ever.
  mkdir -p "$t/manuscript/src"; printf '# The ford\n' > "$t/manuscript/src/01-the-ford.md"
  tree_files "$t" | grep -v '^manuscript/' | grep -v '^CONTEXT.md$' > "$t.owned"; load_owned "$t"
  probe_clean "over syntek-author, a syntek-author folder without a pair is not media's to report"
  mv "$t/scripts/src/CLAUDE.md" "$tmp/h"; sed -i '\#^scripts/src/CLAUDE.md$#d' "$t.owned"; load_owned "$t"
  probe "over syntek-author, a media-owned folder without its pair is still reported" "check 2 — scripts/src/"
  rm -f "$t.owned"; SM_OWNED_MODE=false; SM_OWNED=()
  st_finish "a paired, well-shaped tree from a broken one"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  [[ -d "$SM_ROOT/template" ]] || die "no template/ directory at $SM_ROOT, and no tree given"
  TARGETS=("$SM_ROOT/template")
fi

bold "▸ $SCRIPT_NAME"
STATUS=0
for target in "${TARGETS[@]}"; do
  [[ -d "$target" ]] || die "not a directory: $target"
  TREE="$(cd "$target" && pwd)"
  load_owned "$TREE"
  run_checks
  scope=""; $SM_OWNED_MODE && scope=" (over syntek-author: media-owned folders only)"
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $TREE — $DIRS_CHECKED director(ies), $FILES_CHECKED routed file(s), all in shape$scope"
  else
    bold "✗ $TREE — ${#FINDINGS[@]} finding(s) across $DIRS_CHECKED director(ies)$scope:"
    print_findings
    STATUS=1
  fi
done
log ""
if [[ "$STATUS" -eq 0 ]]; then
  bold "✓ Every folder carries its pair; every routed file is in its house shape."
  exit 0
fi
log "  House shapes: .claude/rules/syntek-media/01-layout-and-routing.md Section 6 (the pair),"
log "  DESIGN.md Sections 4.3 (workflows and guides) and D42 (the exceptions)."
exit 1

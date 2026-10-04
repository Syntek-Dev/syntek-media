#!/usr/bin/env bash
#
# line-cap.sh — Hold every instructional Markdown file to 300 lines (DESIGN.md D31).
#
#               An instruction Claude reads is an instruction that costs context, and a long
#               one is read less carefully than a short one: past a few hundred lines the rule
#               in the middle is the rule that gets missed. syntek-author learned this from
#               three source repositories (one project memory reached 2,906 lines), and media
#               keeps its cap (syntek-author D25). So every instructional file stops at 300; a
#               file that needs more splits into SCREAMING-SNAKE-CASE.md sub-documents behind a
#               thin index.
#
#               Instructional: every .md file — docs, workflows, .claude/** (rules, skills,
#               mode files, MEMORY.md), every CONTEXT.md and CLAUDE.md, guides. Exempt
#               (DESIGN.md D31): README.md, and artefacts under any src/ folder — scripts,
#               transcripts, briefs, plans, registers — except the CONTEXT.md and CLAUDE.md
#               pair inside src/, which instructs. Pruned: generated/, renders/ and raw/
#               (README only, the rest ignored by Git), .git/, build/, node_modules/.
#
#               One check:
#                 1. An instructional .md file is longer than 300 lines.
#
#               Numbers are stable identifiers. Append, never renumber.
#
#               Over-author scope (DESIGN.md Section 7): on a tree with a <tree>.owned beside
#               it, only media-owned files are counted; syntek-author's are its audit's.
#
#               What it CANNOT check: whether a short file is short because it routes well or
#               because it says too little. Nor the guide range (54–82 lines), which is
#               docs-pairing.sh's check 16; nor a skill plus its mode file, which is
#               skill-conformance.sh's check 17.
#
# SELF-TEST. --self-test writes a fixture at runtime — a 300-line file, a long README, a long
#            src/ artefact, a long file in a renders/ folder — proves it clean, then lengthens
#            one file per probe and asserts exactly one finding.
#
# Requirements: bash, find, wc. No network.
#
# Usage: line-cap.sh [--root DIR] [--quiet] [--self-test] [--help] [<tree>...]
#        With no tree, checks template/ in the repository.
#
# Exit codes:  0 = every instructional file is within the cap
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, a tree that does not exist)

set -euo pipefail
SCRIPT_NAME="line-cap.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

CAP=300
SELF_TEST=false
TARGETS=()

usage() {
  cat <<'EOF'
line-cap.sh — Hold every instructional Markdown file to 300 lines

Usage: line-cap.sh [--root DIR] [--quiet] [--self-test] [--help] [<tree>...]

  <tree>       A render, or any directory (default: template/ in the repository)
  --root DIR   The template repository (default: this repository)
  --quiet      Print findings only
  --self-test  Prove the check still fires against a fixture written at runtime
  --help       Show this message

A <tree>.owned file marks an over-author tree: only media-owned files are counted.
Exit codes: 0 = within the cap  1 = finding(s), or the self-test no longer separates
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
CHECKED=0

instructional() { # tree-relative path
  local b="${1##*/}"
  [[ "$1" == *.md ]] || return 1
  [[ "$b" == README.md ]] && return 1
  if [[ "/$1" == */src/* ]]; then
    [[ "$b" == CONTEXT.md || "$b" == CLAUDE.md ]] || return 1
  fi
  return 0
}

run_checks() {
  FINDINGS=()
  CHECKED=0
  local f n
  while IFS= read -r -d '' f; do
    f="${f#./}"
    instructional "$f" || continue
    is_owned_file "$f" || continue
    CHECKED=$((CHECKED + 1))
    n="$(wc -l < "$TREE/$f")"
    [[ "$n" -le "$CAP" ]] || finding "check 1 — $f is $n lines; the cap is $CAP — split it into SCREAMING-SNAKE-CASE.md sub-documents behind a thin index"
  done < <(cd "$TREE" && find . \( -name .git -o -name build -o -name node_modules -o -name generated -o -name renders -o -name raw \) -prune \
             -o -type f -name '*.md' -print0 | sort -z)
}

self_test() {
  local tmp t
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  t="$tmp/gen"; TREE="$t"; load_owned "$TREE"
  mkdir -p "$t/scripts/src/pieces/003-why-the-ferry-runs-late" "$t/.claude/skills/captions" "$t/production/src/renders"
  seq 1 300 > "$t/scripts/CLAUDE.md"
  seq 1 900 > "$t/README.md"
  seq 1 900 > "$t/scripts/src/pieces/003-why-the-ferry-runs-late/script.md"
  seq 1 900 > "$t/production/src/renders/notes.md"
  seq 1 10  > "$t/scripts/src/CONTEXT.md"
  seq 1 10  > "$t/.claude/skills/captions/SKILL.md"
  st_baseline "a fixture at the cap, with exempt long files"

  seq 1 301 > "$t/scripts/CLAUDE.md";                 probe "check 1 fires on a CLAUDE.md one line over" "check 1 — scripts/CLAUDE.md"
  seq 1 300 > "$t/scripts/CLAUDE.md"
  seq 1 301 > "$t/scripts/src/CONTEXT.md";            probe "check 1 fires on a pair inside src/" "check 1 — scripts/src/CONTEXT.md"
  seq 1 10  > "$t/scripts/src/CONTEXT.md"
  seq 1 400 > "$t/.claude/skills/captions/SKILL.md";  probe "check 1 fires on a long SKILL.md" "check 1 — .claude/skills/captions/SKILL.md"
  seq 1 10  > "$t/.claude/skills/captions/SKILL.md"

  mkdir -p "$t/.claude/rules/syntek-author"; seq 1 400 > "$t/.claude/rules/syntek-author/01-layout-and-routing.md"
  tree_files "$t" | grep -v '^\.claude/rules/syntek-author/' > "$t.owned"; load_owned "$t"
  probe_clean "over syntek-author, a long syntek-author file is its own audit's"
  rm -f "$t.owned"; SM_OWNED_MODE=false; SM_OWNED=(); rm -rf "$t/.claude/rules"
  st_finish "files within the cap from files over it"
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
  scope=""; $SM_OWNED_MODE && scope=" (media-owned)"
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $TREE — $CHECKED instructional file(s)$scope, all within $CAP lines"
  else
    bold "✗ $TREE — ${#FINDINGS[@]} of $CHECKED instructional file(s)$scope over the cap:"
    print_findings
    STATUS=1
  fi
done
[[ "$STATUS" -eq 0 ]] && { log ""; bold "✓ Every instructional file is within $CAP lines."; exit 0; }
exit 1

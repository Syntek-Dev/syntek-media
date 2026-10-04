#!/usr/bin/env bash
#
# byte-identity.sh — Verify shared files are byte-identical in every render that ships them.
#
#                    DESIGN.md Section 2 ("Token discipline") makes one promise that holds the
#                    three brand kinds, six platforms and six media kinds together: outside the
#                    spine set, a file that ships in two renders is the SAME file in both. That
#                    is what lets a skill be fixed once, reviewed once and updated everywhere,
#                    and it is what makes "brand differences live in gated files and mode files"
#                    true rather than aspirational. With twelve list choices, any shared file
#                    that says "your platforms" differs between profiles — so such lists live in
#                    spine and index files (gated rows) or in per-platform gated files.
#                    check-template-tokens.sh polices the SOURCE for the tokens and blocks that
#                    would break the promise; this script checks the promise itself, on the
#                    renders — so a difference that arrives some other way (a Copier variable, a
#                    filter, a profile answer leaking into a shared file) is caught where it
#                    actually shows.
#
#                    One check:
#                      1. A file outside the spine set differs between two standalone renders
#                         that both ship it.
#
#                    Compared: every file present in at least two renders. Skipped: .git/, the
#                    answers file, build/, audio/ and __pycache__/, and the spine set — the root
#                    spine, the ten shared files, every seed, every seed-once example and every
#                    index file (computed in _common.sh from DESIGN.md and copier.yml). An
#                    over-author tree (one with a <tree>.owned beside it) is not compared: it
#                    differs by syntek-author's variant by design (DESIGN.md Section 7), and is
#                    named as skipped.
#
#                    Numbers are stable identifiers. Append, never renumber.
#
#                    What it CANNOT check: the spine set itself. A spine file may differ, but
#                    only on lines whose template source carries a variant token or block;
#                    proving that needs a line-level map from render to source that Jinja does
#                    not provide. check-template-tokens.sh keeps the spine set small instead.
#
# SELF-TEST. --self-test builds three small renders at runtime — a shared skill, a spine file
#            that legitimately differs, a mode file only one render ships — proves them clean,
#            then changes the shared file in one render and asserts exactly one finding.
#
# Requirements: bash 4+, sha1sum, awk, find. No network.
#
# Usage: byte-identity.sh [--root DIR] [--quiet] [--self-test] [--help] <tree> <tree>...
#
# Exit codes:  0 = every shared file is identical wherever it ships
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (fewer than two standalone trees, a tree that does not exist)

set -euo pipefail
SCRIPT_NAME="byte-identity.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
TARGETS=()

usage() {
  cat <<'EOF'
byte-identity.sh — Verify shared files are byte-identical in every render that ships them

Usage: byte-identity.sh [--root DIR] [--quiet] [--self-test] [--help] <tree> <tree>...

  --root DIR   The template repository whose copier.yml defines the spine set
  --quiet      Print findings only
  --self-test  Prove the check still fires against renders built at runtime
  --help       Show this message

Over-author trees (a <tree>.owned beside them) are skipped by name.
Exit codes: 0 = identical  1 = finding(s), or the self-test no longer separates
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

TREES=()
COMPARED=0
SPINE_SKIPPED=0

hash_tree() { # $1 = index, $2 = tree → index<TAB>hash<TAB>rel
  (cd "$2" && find . \( -name .git -o -name build -o -name audio -o -name __pycache__ \) -prune -o -type f -print0 \
     | xargs -0 -r sha1sum) \
    | awk -v i="$1" '{ h = $1; $1 = ""; sub(/^ +/, ""); sub(/^\.\//, ""); print i "\t" h "\t" $0 }' \
    | grep -v -e $'\t'"$SM_ANSWERS_FILE"'$' || true
}

run_checks() {
  FINDINGS=()
  COMPARED=0; SPINE_SKIPPED=0
  local i rel groups name
  local -a names=()
  for i in "${!TREES[@]}"; do names+=("$(basename "${TREES[$i]}")"); done
  while IFS=$'\t' read -r rel groups; do
    [[ -z "$rel" ]] && continue
    if [[ "$groups" == SAME ]]; then
      if spine_kind "$rel" >/dev/null; then SPINE_SKIPPED=$((SPINE_SKIPPED + 1)); else COMPARED=$((COMPARED + 1)); fi
      continue
    fi
    if spine_kind "$rel" >/dev/null; then SPINE_SKIPPED=$((SPINE_SKIPPED + 1)); continue; fi
    COMPARED=$((COMPARED + 1))
    # groups: "0,1|2" — tree indexes sharing one version, versions separated by |
    name=""
    while IFS= read -r -d '|' g; do
      local members="" idx
      for idx in ${g//,/ }; do members+="${members:+, }${names[$idx]}"; done
      name+="${name:+  ≠  }{$members}"
    done <<< "$groups|"
    finding "check 1 — $rel differs between renders: $name"
  done < <(for i in "${!TREES[@]}"; do hash_tree "$i" "${TREES[$i]}"; done | awk -F'\t' '
      { key = $3; if (!(key in seen)) { seen[key] = 1; order[++n] = key }
        cnt[key]++
        if (!((key SUBSEP $2) in hv)) { hv[key SUBSEP $2] = ++nv[key]; vlist[key, nv[key]] = $2 }
        v = hv[key SUBSEP $2]; mem[key, v] = mem[key, v] (mem[key, v] == "" ? "" : ",") $1 }
      END {
        for (k = 1; k <= n; k++) {
          key = order[k]
          if (cnt[key] < 2) continue
          if (nv[key] == 1) { print key "\tSAME"; continue }
          out = ""
          for (v = 1; v <= nv[key]; v++) out = out (v > 1 ? "|" : "") mem[key, v]
          print key "\t" out
        }
      }')
}

# ── Self-test ────────────────────────────────────────────────────────────────

self_test() {
  local tmp t
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  build_sets ""
  TREES=()
  for t in business--defaults author-fiction--defaults author-nonfiction--defaults; do
    mkdir -p "$tmp/$t/.claude/skills/captions" "$tmp/$t/.git"
    printf '# Skill: Captions\n\nShared, word for word.\n' > "$tmp/$t/.claude/skills/captions/SKILL.md"
    printf '# A %s brand\n' "$(kind_of "$t")" > "$tmp/$t/README.md"
    printf 'BRAND_KIND: %s\n' "$(kind_of "$t")" > "$tmp/$t/$SM_ANSWERS_FILE"
    printf 'ref: %s\n' "$t" > "$tmp/$t/.git/HEAD"
    TREES+=("$tmp/$t")
  done
  mkdir -p "$tmp/business--defaults/.claude/skills/write-script"
  printf '# BUSINESS.md — write-script, business mode\n' > "$tmp/business--defaults/.claude/skills/write-script/BUSINESS.md"
  st_baseline "three renders that differ only in the spine"

  printf '# Skill: Captions\n\nShared, word for word — except here.\n' > "$tmp/author-fiction--defaults/.claude/skills/captions/SKILL.md"
  probe "check 1 fires when a shared skill differs in one render" "check 1 — .claude/skills/captions/SKILL.md differs"
  printf '# Skill: Captions\n\nShared, word for word.\n' > "$tmp/author-fiction--defaults/.claude/skills/captions/SKILL.md"

  printf 'a different spine line\n' >> "$tmp/author-nonfiction--defaults/README.md"
  probe_clean "a spine file may differ between renders"

  st_finish "identical shared files from a shared file that varies"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

for target in "${TARGETS[@]}"; do
  [[ -d "$target" ]] || die "not a directory: $target"
  target="$(cd "$target" && pwd)"
  if [[ -f "$target.owned" ]]; then
    log "  · skipped $target — an over-author tree differs by syntek-author's variant by design; byte-identity runs on standalone trees"
    continue
  fi
  TREES+=("$target")
done
[[ ${#TREES[@]} -ge 2 ]] || die "give at least two standalone rendered trees — identity is a comparison"
build_sets "$SM_ROOT/copier.yml"

bold "▸ $SCRIPT_NAME — ${#TREES[@]} render(s)"
run_checks
log "  compared $COMPARED shared file(s) present in two or more renders; $SPINE_SKIPPED spine file(s) exempt"
if [[ ${#FINDINGS[@]} -eq 0 ]]; then
  bold "✓ Every shared file is byte-identical wherever it ships."
  exit 0
fi
bold "✗ ${#FINDINGS[@]} finding(s):"
print_findings
log ""
log "  A shared file must not vary by brand kind, platform or media kind (DESIGN.md Section 2)."
log "  Move the difference into a gated file or a mode file, or — if the file is an index — gate"
log "  its rows."
exit 1

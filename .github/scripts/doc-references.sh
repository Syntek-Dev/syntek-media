#!/usr/bin/env bash
#
# doc-references.sh — Verify every path and skill a rendered project's docs cite exists there.
#
#                     The governance files route rather than restate (SB rule 51): a CLAUDE.md
#                     names the workflow, the STEPS.md names the skill and the guide, the guide
#                     names the rules section. A citation that resolves to nothing is a dead end
#                     Claude walks into with full confidence. In syntek-media the risk has two
#                     shapes the house template never had. A SHARED file is byte-identical in
#                     every render, so a path it names must exist in all of them — a shared
#                     skill citing the audiobook folder is right where the project makes
#                     audiobooks and a dangling reference everywhere else. And media lives in
#                     syntek-author's repositories without depending on them: a backticked
#                     syntek-author path or skill resolves over syntek-author and dangles
#                     standalone (DESIGN.md D4, D10), and syntek-author's own audit flags it on
#                     a combined tree. Index files gate their rows, companions are named in prose
#                     "where present"; this script proves both answers held, on every render.
#
#                     Eight checks, over every .md file in a render:
#                       1. A backticked repository path does not exist in THIS tree.
#                       2. A routing frontmatter `skills:` list names a skill this tree lacks.
#                       3. A `> **Skill:**` line names a skill this tree lacks.
#                       4. A backticked skill name (one DESIGN.md Section 5.1 lists) that this
#                          tree lacks — a shared file naming a gated skill.
#                       5. A companion skill of syntek-author (DESIGN.md Section 5.2) named
#                          backticked, in `skills:`, or on a Skill line without
#                          "(syntek-author), where present" (D10).
#                       6. A backticked syntek-author path: standards/, manuscript/, library/,
#                          planning/, research/, proposal/, typeset/, world/, tooling/,
#                          handoffs/, learning/, assets/, Makefile, .claude/rules/syntek-author/,
#                          00-project.md — named in prose instead, "where present". A folder
#                          name counts only as the FIRST segment of the path: `assets/…` is
#                          syntek-author's, `production/src/assets/` is media's.
#                       7. 000-example-piece backticked in a file outside the spine set: no
#                          template-owned file names an example path (D43); the rules, the seeds
#                          and the examples may.
#                       8. A workflow cited by number alone ("workflow 02", "production 02")
#                          rather than by its full folder name (D32): a project may keep two
#                          folders with one number.
#
#                     A token is tested as a path when it has no spaces, contains a slash, and
#                     is not a placeholder: anything with < > { } * ? [ ] … | = ( ) $ % @ # , ;
#                     or the house placeholders NN, NNN, DD-MM-YYYY, YYYY; URLs; absolute paths
#                     (scrub.sh's); and generated output (anything inside a generated/,
#                     renders/ or raw/ folder but its README.md, build/, audio/). A placeholder
#                     is exempt from check 6 too: `handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md`
#                     describes a file name, it does not cite a place. A trailing :N line
#                     anchor is peeled first. A path resolves if it exists from the tree root
#                     or from any ancestor of the citing file, so `src/` inside
#                     production/CLAUDE.md means production/src/. An unresolved path led by a
#                     generic folder name (`generated/`, `renders/`, `raw/`, `docs/project/`,
#                     `workflows/local/`, `reference/`) names a class of folder, not a place,
#                     and is not a finding; one led by a top-level entry (`publishing/…`,
#                     `toolkit/…`) always is. A bare mode-file name (`BUSINESS.md`,
#                     `FICTION.md`, `NONFICTION.md`) is never a missing path: the mode paragraph
#                     names all three and exactly one ships. An example path is never check
#                     1's: a seed-once example may have been deleted, or never rendered
#                     (SEED_EXAMPLES=false), and the files allowed to name it say so.
#
#                     A citation gated exactly as the citing file is (DESIGN.md Section 3.5:
#                     the audiobook guide naming `production/src/audiobook/` or the
#                     `narrate-audiobook` skill) is never checks 1, 3 or 4's: the two ship
#                     together, and a gated file that leaked into a render without its gate is
#                     shipped-brands.sh check 6's single finding, not one more per citation.
#
#                     One fault, one finding: a companion is check 5's and never also check 2's
#                     or 3's; a syntek-author path is check 6's and never also check 1's.
#
#                     Fenced code is skipped (format samples quote invented paths). A line is
#                     exempt when it, or the line above it, carries
#                       <!-- doc-references: variant-only -->   or
#                       <!-- doc-references: ignore — reason -->
#                     Use the first sparingly: a gated row in an index file is the real answer.
#
#                     Over-author scope (DESIGN.md Section 7): on a tree with a <tree>.owned
#                     beside it, only media-owned files are read, and their citations resolve
#                     against the whole composite.
#
#                     Numbers are stable identifiers. Append, never renumber.
#
#                     What it CANNOT check: that a path that resolves is the RIGHT one; a
#                     citation written without backticks; or a mistyped relative path led by a
#                     generic folder name, which reads as a class name.
#
# SELF-TEST. --self-test builds a small tree at runtime, proves it clean (placeholders, a fenced
#            sample, a marker, a layer-relative path, generated output, a companion in prose
#            and an example path in a rules file all pass), then applies one mutation per
#            check and asserts exactly one finding each.
#
# Requirements: bash 4+, awk, find. No network. Pass trees that generate-all.sh produced.
#
# Usage: doc-references.sh [--root DIR] [--quiet] [--self-test] [--help] <rendered-tree>...
#
# Exit codes:  0 = every citation resolves in its own tree
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, a tree that does not exist)

set -euo pipefail
SCRIPT_NAME="doc-references.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
TARGETS=()

usage() {
  cat <<'EOF'
doc-references.sh — Verify every path and skill a rendered project's docs cite exists there

Usage: doc-references.sh [--root DIR] [--quiet] [--self-test] [--help] <rendered-tree>...

  --root DIR   The template repository whose copier.yml defines the spine set
  --quiet      Print findings only
  --self-test  Prove the checks still fire against a tree built at runtime
  --help       Show this message

A <tree>.owned file marks an over-author tree: only media-owned files are read.
Exit codes: 0 = every citation resolves  1 = finding(s), or the self-test no longer
separates  2 = script error
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
TOKENS=0
PATH_TESTS=0
declare -A CATALOGUE=()
declare -A COMPANION=()
while read -r s _; do [[ -n "$s" ]] && CATALOGUE["$s"]=1; done <<< "$SM_SKILLS"
for s in $SM_COMPANIONS; do COMPANION["$s"]=1; done

# Records per file: L<TAB>line<TAB>S|T<TAB>token for backticked tokens outside fences and
# markers (S = on a Skill line); F<TAB>line<TAB>-<TAB>name for each frontmatter skill;
# K<TAB>line<TAB>-<TAB>text for a Skill line's skill part, backticked spans removed; and
# W<TAB>line<TAB>-<TAB>text for a workflow cited by number alone.
EXTRACT='
NR == 1 && $0 == "---" { infm = 1; next }
infm && /^---[[:space:]]*$/ { infm = 0; next }
infm {
  if ($0 ~ /^skills:[[:space:]]*\[/) {
    s = $0; sub(/^skills:[[:space:]]*\[/, "", s); sub(/\].*$/, "", s)
    n = split(s, a, ",")
    for (i = 1; i <= n; i++) { v = a[i]; gsub(/[[:space:]"\047]/, "", v); if (v != "") print "F\t" NR "\t-\t" v }
  } else if ($0 ~ /^skills:[[:space:]]*$/) { inlist = 1 }
  else if (inlist && $0 ~ /^[[:space:]]+-[[:space:]]/) { v = $0; sub(/^[[:space:]]+-[[:space:]]*/, "", v); gsub(/[[:space:]"\047]/, "", v); print "F\t" NR "\t-\t" v }
  else inlist = 0
  next
}
/^[[:space:]]*```/ { fence = !fence; next }
fence { next }
{
  exempt = (prevmark || $0 ~ /doc-references: *(variant-only|ignore)/)
  prevmark = ($0 ~ /doc-references: *(variant-only|ignore)/)
  if (exempt) next
  skillline = ($0 ~ /^> \*\*Skill:\*\*/)
  kind = skillline ? "S" : "T"
  line = $0
  while ((i = index(line, "`")) > 0) {
    rest = substr(line, i + 1)
    j = index(rest, "`")
    if (!j) break
    tok = substr(rest, 1, j - 1)
    if (tok != "") print "L\t" NR "\t" kind "\t" tok
    line = substr(rest, j + 1)
  }
  bare = $0; gsub(/`[^`]*`/, "", bare)
  if (skillline) {
    seg = bare; sub(/^> \*\*Skill:\*\*[ \t]*/, "", seg)
    i = index(seg, " · "); if (i) seg = substr(seg, 1, i - 1)
    print "K\t" NR "\t-\t" seg
  }
  if (match(bare, /(^|[^A-Za-z0-9_-])[Ww]orkflows? +[0-9][0-9]?([^0-9A-Za-z_-]|$)/) || \
      match(bare, /(^|[^A-Za-z0-9_\/.-])(brand|scripts|production|publishing) +0[0-9]([^0-9]|$)/)) {
    print "W\t" NR "\t-\t" substr(bare, RSTART, RLENGTH)
  }
}'

is_pathlike() { # sets P to the testable path, or returns 1
  local t="$1"
  [[ "$t" =~ ^(.+):[0-9]+(:[0-9]+|-[0-9]+)?$ ]] && t="${BASH_REMATCH[1]}"
  [[ "$t" == */* ]] || return 1
  case "$t" in
    *[[:space:]]*|/*|-*|~*|http*|*://*|www.*) return 1 ;;
    *'<'*|*'>'*|*'{'*|*'}'*|*'*'*|*'?'*|*'['*|*']'*|*'…'*|*'|'*|*'='*|*'('*|*')'*) return 1 ;;
    *'$'*|*'%'*|*'@'*|*'#'*|*','*|*';'*|*"'"*|*'"'*|*'\'*|*'+'*|*'!'*|*':'*) return 1 ;;
    *NN*|*DD-MM-YYYY*|*YYYY*|*XXX*) return 1 ;;
    build|build/*|*/build/*|*/audio|*/audio/*|.git|.git/*|*node_modules*|.claude/settings.local.json) return 1 ;;
    generated/?*|*/generated/?*|renders/?*|*/renders/?*|raw/?*|*/raw/?*)
      [[ "${t##*/}" == README.md ]] || return 1 ;;
  esac
  [[ "$t" =~ ^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*/?$ ]] || return 1
  # Abbreviations, not paths: N/A, I/O, and/or — every segment two letters or fewer, or a
  # conjunction pair.
  [[ "${t%/}" =~ ^[A-Za-z]{1,2}(/[A-Za-z]{1,2})+$ || "$t" == and/or || "$t" == either/or ]] && return 1
  P="$t"
}

# A path whose first segment is a top-level entry of a media render is anchored: it must
# resolve, and a gated path (the audiobook folder in a podcast-only project) is exactly the case
# to catch. Any other path is relative to the citing file; unresolved, it is a dead end —
# unless it is led by a generic folder name, in which case it names a CLASS of folder ("each
# `generated/`", "every `docs/project/`"), not a place.
TOPLEVEL=" .claude .github brand scripts production publishing toolkit README.md CONTEXT.md .gitignore .mcp.json $SM_ANSWERS_FILE "
GENERIC=" docs src workflows local reference project generated renders raw pieces templates data "

is_class_name() { # $1 = unresolved path
  local first="${1%%/*}"
  [[ "$TOPLEVEL" == *" $first "* ]] && return 1
  [[ "$GENERIC" == *" $first "* ]]
}

resolves() { # $1 = path, $2 = citing file (tree-relative)
  local p="${1%/}" d
  [[ -e "$TREE/$p" ]] && return 0
  d="$(dirname "$2")"
  while :; do
    [[ "$d" == . ]] && break
    [[ -e "$TREE/$d/$p" ]] && return 0
    d="$(dirname "$d")"
  done
  return 1
}

# A placeholder describes a name; it never cites a place (FIXES A1): checks 1 and 6 skip it.
is_placeholder() { # $1 = token
  case "$1" in *'<'*|*'>'*|*'*'*|*NN*|*DD-MM-YYYY*) return 0 ;; esac
  return 1
}

# A syntek-author path (check 6): its two named files; its rules folder; or a path whose FIRST
# segment is one of its top-level folders (`assets/…`, never `production/src/assets/`). A
# placeholder is exempt (`handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md` names a file's shape).
author_path() { # $1 = token
  local t="$1" p
  is_placeholder "$t" && return 1
  t="${t%/}"
  [[ " $SM_AUTHOR_FILE_NAMES " == *" ${t##*/} "* && "$t" =~ ^[A-Za-z0-9._/-]+$ ]] && return 0
  for p in $SM_AUTHOR_PATH_PREFIXES; do [[ "$t" == "$p" || "$t" == "$p"/* ]] && return 0; done
  is_pathlike "$1" || return 1
  [[ " $SM_AUTHOR_PATH_HEADS " == *" ${P%%/*} "* ]]
}

# The Section 3.5 gate a path carries, in the catalogue vocabulary: the gate of the deepest
# gated catalogue entry at or above it (a gated skill folder included), or `always`. Seed-once
# examples are check 7's, so `seed` is not a gate here.
GATED_ROWS=()
while read -r _g _ _p; do
  [[ -z "$_g" || "$_g" == always || "$_g" == seed ]] && continue
  GATED_ROWS+=("$_g $_p")
done <<< "$SM_PATHS"
while read -r _s _g _; do
  [[ -z "$_s" || "$_g" == always ]] && continue
  GATED_ROWS+=("$_g .claude/skills/$_s")
done <<< "$SM_SKILLS"
unset _g _p _s

gate_of() { # $1 = tree-relative path → prints its gate
  local p="${1%/}" row g q best="always" len=0
  for row in "${GATED_ROWS[@]}"; do
    g="${row%% *}"; q="${row#* }"
    if [[ "$p" == "$q" || "$p" == "$q"/* ]] && [[ ${#q} -gt $len ]]; then best="$g"; len=${#q}; fi
  done
  printf '%s' "$best"
}

FILE_GATE=""
same_gate() { # $1 = cited path or skill folder, as a tree path — true when gated as the citing file is
  [[ "$FILE_GATE" != always ]] || return 1
  [[ "$(gate_of "$1")" == "$FILE_GATE" ]]
}

run_checks() {
  FINDINGS=()
  TOKENS=0; PATH_TESTS=0
  local f rec ln kind tok P c spine
  local -A skills=()
  if [[ -d "$TREE/.claude/skills" ]]; then
    while IFS= read -r s; do skills["$s"]=1; done < <(find "$TREE/.claude/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n')
  fi
  while IFS= read -r -d '' f; do
    f="${f#./}"
    is_owned_file "$f" || continue
    spine=false; spine_kind "$f" >/dev/null && spine=true
    FILE_GATE="$(gate_of "$f")"
    while IFS=$'\t' read -r rec ln kind tok; do
      case "$rec" in
        F)
          if [[ -n "${COMPANION[$tok]:-}" ]]; then
            finding "check 5 — $f:$ln routes to '$tok' in skills: — a companion of syntek-author is named in prose, never in frontmatter (DESIGN.md D10)"
          else
            [[ -n "${skills[$tok]:-}" ]] || finding "check 2 — $f:$ln routes to skill '$tok', which this project does not have"
          fi ;;
        K)
          for c in $SM_COMPANIONS; do
            if [[ " $tok " =~ [^A-Za-z0-9-]${c}[^A-Za-z0-9-] && "$tok" != *'(syntek-author), where present'* ]]; then
              finding "check 5 — $f:$ln names $c on its Skill line without '(syntek-author), where present'"
              break
            fi
          done ;;
        W)
          finding "check 8 — $f:$ln cites a workflow by number alone ('${tok#"${tok%%[![:space:]]*}"}') — cite it by its full folder name (DESIGN.md D32)" ;;
        L)
          TOKENS=$((TOKENS + 1))
          if [[ "$tok" == *"$SM_EXAMPLE_NAME"* ]]; then
            $spine || finding "check 7 — $f:$ln backticks \`$tok\` — no template-owned file names an example path (DESIGN.md D43)"
            continue
          fi
          if author_path "$tok"; then
            finding "check 6 — $f:$ln backticks the syntek-author path \`$tok\` — name it in prose, where present (DESIGN.md D4)"
            continue
          fi
          if [[ "$tok" =~ ^[a-z0-9-]+$ ]]; then
            if [[ -n "${COMPANION[$tok]:-}" ]]; then
              finding "check 5 — $f:$ln backticks the companion '$tok' — name it 'the $tok skill (syntek-author), where present' (DESIGN.md D10)"
            elif [[ -n "${skills[$tok]:-}" ]] || same_gate ".claude/skills/$tok"; then
              :
            elif [[ "$kind" == S ]]; then
              finding "check 3 — $f:$ln names skill '$tok' on its Skill line; this project does not have it"
            elif [[ -n "${CATALOGUE[$tok]:-}" ]]; then
              finding "check 4 — $f:$ln names the skill '$tok', which this project does not have"
            fi
            continue
          fi
          # A bare mode-file name is never a path (the mode paragraph names all three).
          [[ " $SM_MODE_FILES " == *" $tok "* ]] && continue
          if is_pathlike "$tok"; then
            PATH_TESTS=$((PATH_TESTS + 1))
            resolves "$P" "$f" || is_class_name "$P" || same_gate "$P" \
              || finding "check 1 — $f:$ln cites \`$tok\`, which does not exist in this project"
          fi ;;
      esac
    done < <(awk "$EXTRACT" "$TREE/$f")
  done < <(cd "$TREE" && find . \( -name .git -o -name build -o -name node_modules \) -prune -o -type f -name '*.md' -print0 | sort -z)
}

# ── Self-test ────────────────────────────────────────────────────────────────

self_test() {
  local tmp t g wf r
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  build_sets ""
  t="$tmp/gen"; TREE="$t"; load_owned "$TREE"
  g="$t/production/docs/reference/elevenlabs.md"
  wf="$t/production/workflows/02-make-a-voiceover"
  r="$t/.claude/rules/syntek-media/01-layout-and-routing.md"
  mkdir -p "$t/.claude/skills/voiceover" "$t/.claude/skills/captions" "$t/.claude/rules/syntek-media" \
    "$t/production/docs/reference" "$t/production/src/voiceover/generated" "$t/production/src/assets" "$wf"
  printf 'x\n' > "$t/.claude/skills/voiceover/SKILL.md"
  printf 'x\n' > "$t/production/src/voiceover/generated/README.md"
  printf 'x\n' > "$t/production/src/assets/CONTEXT.md"
  cat > "$g" <<'EOF'
---
type: guide
skills: [voiceover, captions]
model: opus
---

# ElevenLabs — the voice service

See `production/src/voiceover/` and `production/src/voiceover/generated/README.md:3`.
Placeholders are not citations: `production/src/voiceover/<piece>.toml`, `NNN-kebab-title/brief.md`,
`handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md`, `brand/src/platforms/*.md`, `https://example.com/a/b`.
Generated output is not a citation: `production/src/voiceover/generated/003-x.s01.t1.mp3`.
Commands are not citations: `python3 toolkit/media.py take add`. Nor are `N/A` or `and/or`.
The `voiceover` skill and the `captions` skill both ship; proofreading is the spelling skill
(syntek-author), where present. Procedures: `production/workflows/02-make-a-voiceover/`.

```toml
file = "production/src/voiceover/generated/003-why-the-ferry-runs-late.s04.t2.mp3"
```

<!-- doc-references: variant-only -->
- `production/src/audiobook/` — where the project makes audiobooks, marked.
EOF
  cat > "$wf/STEPS.md" <<'EOF'
---
workflow: 02-make-a-voiceover
skills: [voiceover]
---

## 1. Confirm

> **Skill:** `voiceover` · **Guide:** `docs/reference/elevenlabs.md`

## 2. Grill the brief

> **Skill:** grill-with-docs (syntek-author), where present · **Guide:** none
EOF
  printf '# 01-layout-and-routing.md\n\nThe worked example is `scripts/src/pieces/000-example-piece/brief.md`, where it was kept.\n' > "$r"
  printf '# CONTEXT.md — production/src/\n\nSmall stills live in `production/src/assets/`.\n' > "$t/production/src/CONTEXT.md"
  st_baseline "a tree whose citations all resolve"

  printf 'Read `production/src/missing.md` first.\n' >> "$g"
  probe "check 1 fires on a path that does not exist" "check 1"
  sed -i '$d' "$g"

  printf 'Narration lives in `production/src/audiobook/`.\n' >> "$g"
  probe "check 1 fires on a gated folder this tree does not ship" "check 1 — production/docs/reference/elevenlabs.md"
  sed -i '$d' "$g"

  sed -i 's/^skills: \[voiceover\]/skills: [voiceover, narrate-audiobook]/' "$wf/STEPS.md"
  probe "check 2 fires on frontmatter routing to an absent skill" "check 2"
  sed -i 's/^skills: \[voiceover, narrate-audiobook\]/skills: [voiceover]/' "$wf/STEPS.md"

  printf '\n## 3. Narrate\n\n> **Skill:** `narrate-audiobook` · **Guide:** none\n' >> "$wf/STEPS.md"
  probe "check 3 fires on a Skill line naming an absent skill" "check 3"
  head -n -4 "$wf/STEPS.md" > "$tmp/s" && cat "$tmp/s" > "$wf/STEPS.md"

  printf 'Each `generated/` carries a README; every `docs/project/` is yours.\n' >> "$g"
  probe_clean "a generic folder-class name is not a citation"
  sed -i '$d' "$g"

  printf 'Then run the `narrate-audiobook` skill.\n' >> "$g"
  probe "check 4 fires on prose naming a gated skill this tree lacks" "check 4"
  sed -i '$d' "$g"

  printf 'Then run the `spelling` skill.\n' >> "$g"
  probe "check 5 fires on a backticked companion" "check 5 — production/docs/reference/elevenlabs.md:23 backticks the companion 'spelling'"
  sed -i '$d' "$g"
  sed -i 's/^skills: \[voiceover\]/skills: [voiceover, grammar]/' "$wf/STEPS.md"
  probe "check 5 fires on a companion in skills:, never check 2" "check 5 — production/workflows/02-make-a-voiceover/STEPS.md:3 routes to 'grammar'"
  sed -i 's/^skills: \[voiceover, grammar\]/skills: [voiceover]/' "$wf/STEPS.md"
  sed -i 's/^> \*\*Skill:\*\* grill-with-docs (syntek-author), where present/> **Skill:** grill-with-docs/' "$wf/STEPS.md"
  probe "check 5 fires on a companion on a Skill line without the where-present form" "check 5 — production/workflows/02-make-a-voiceover/STEPS.md:12 names grill-with-docs"
  sed -i 's/^> \*\*Skill:\*\* grill-with-docs · /> **Skill:** grill-with-docs (syntek-author), where present · /' "$wf/STEPS.md"
  printf '\n## 3. Check\n\n> **Skill:** `fact-check` · **Guide:** none\n' >> "$wf/STEPS.md"
  probe "check 5 fires on a backticked companion on a Skill line, never check 3" "check 5"
  head -n -4 "$wf/STEPS.md" > "$tmp/s" && cat "$tmp/s" > "$wf/STEPS.md"

  printf 'The written voice is `standards/brand/brand-voice.md`.\n' >> "$g"
  probe "check 6 fires on a backticked syntek-author path, never check 1" "check 6 — production/docs/reference/elevenlabs.md:23 backticks the syntek-author path"
  sed -i '$d' "$g"
  printf 'Project settings live in `00-project.md`.\n' >> "$g"
  probe "check 6 fires on syntek-author's project settings file" "check 6"
  sed -i '$d' "$g"
  printf 'Small stills live in `assets/`, beside this file.\n' >> "$t/production/src/CONTEXT.md"
  probe "check 6 fires on a syntek-author folder as the first segment, even where it resolves below the root" "check 6 — production/src/CONTEXT.md:4 backticks the syntek-author path \`assets/\`"
  sed -i '$d' "$t/production/src/CONTEXT.md"
  printf 'Stills: `production/src/assets/`; the rules: `.claude/rules/syntek-author/<file>.md`, `standards/*/style-sheet.md`.\n' >> "$g"
  probe_clean "check 6 matches only a first segment, and never a placeholder"
  sed -i '$d' "$g"
  printf 'Exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships; see `workflows/local/02-x/`, `renders/`, `raw/`, `reference/`, `local/`, `project/`.\n' >> "$g"
  probe_clean "a bare mode-file name, and every generic folder name, is never a missing path"
  sed -i '$d' "$g"
  # A gated file citing what shares its gate: the two ship together; a leaked file is
  # shipped-brands.sh's finding, never one more per citation here.
  mkdir -p "$t/production/workflows/05-narrate-an-audiobook"
  printf '# STEPS\n\n## 1. Narrate\n\n> **Skill:** `narrate-audiobook` · **Guide:** none\n\nChunks go to `production/src/audiobook/generated/`; the `narrate-audiobook` skill owns them.\n' \
    > "$t/production/workflows/05-narrate-an-audiobook/STEPS.md"
  probe_clean "a citation gated exactly as the citing file is is never a finding"
  printf 'Read `production/src/missing.md` too.\n' >> "$t/production/workflows/05-narrate-an-audiobook/STEPS.md"
  probe "check 1 still fires in a gated file on a path its gate does not cover" "check 1 — production/workflows/05-narrate-an-audiobook/STEPS.md:8"
  rm -rf "$t/production/workflows/05-narrate-an-audiobook"

  printf 'The worked example is `scripts/src/pieces/000-example-piece/`.\n' >> "$g"
  probe "check 7 fires on an example path in a template-owned file" "check 7"
  sed -i '$d' "$g"

  printf 'Then follow workflow 02 to the end.\n' >> "$g"
  probe "check 8 fires on a workflow cited by number alone" "check 8"
  sed -i '$d' "$g"
  printf 'Then follow production 02 to the end.\n' >> "$g"
  probe "check 8 fires on a layer-and-number shorthand" "check 8"
  sed -i '$d' "$g"

  # Over syntek-author: a syntek-author file is its own audit's; media's are read as ever.
  mkdir -p "$t/manuscript"; printf 'See `manuscript/src/02-missing/` and `planning/src/outline.md`.\n' > "$t/manuscript/CONTEXT.md"
  tree_files "$t" | grep -v '^manuscript/' > "$t.owned"; load_owned "$t"
  probe_clean "over syntek-author, syntek-author's own files are not read"
  printf 'Read `production/src/missing.md` first.\n' >> "$g"
  probe "over syntek-author, a media-owned file's dead citation is still reported" "check 1"
  sed -i '$d' "$g"
  rm -f "$t.owned"; SM_OWNED_MODE=false; SM_OWNED=()

  st_finish "a tree whose citations resolve from one with dead ends"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

[[ ${#TARGETS[@]} -gt 0 ]] || die "no rendered tree given — citations are checked in the tree each reader will have (see generate-all.sh)"
build_sets "$SM_ROOT/copier.yml"

bold "▸ $SCRIPT_NAME"
STATUS=0
for target in "${TARGETS[@]}"; do
  [[ -d "$target" ]] || die "not a directory: $target"
  TREE="$(cd "$target" && pwd)"
  load_owned "$TREE"
  run_checks
  scope=""; $SM_OWNED_MODE && scope=", media-owned files only"
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $TREE — $TOKENS backticked token(s), $PATH_TESTS tested as paths, all resolve$scope"
  else
    bold "✗ $TREE — ${#FINDINGS[@]} finding(s) ($TOKENS token(s), $PATH_TESTS tested as paths$scope):"
    print_findings
    STATUS=1
  fi
done
log ""
if [[ "$STATUS" -eq 0 ]]; then
  bold "✓ Every citation resolves in the tree that carries it."
  exit 0
fi
log "  A shared file may only name what every render ships. Gate the row in its index file"
log "  (DESIGN.md Section 2), name the path in prose, or fix the path; name syntek-author's"
log "  paths and skills in prose, \"where present\" (D10)."
exit 1

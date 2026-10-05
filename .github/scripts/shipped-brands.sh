#!/usr/bin/env bash
#
# shipped-brands.sh — Verify a rendered project carries exactly what its brand should.
#
#                     One tree ships three brand kinds, nine platforms and six media kinds,
#                     and the only mechanism that separates them is a templated _exclude line
#                     per gated path (DESIGN.md Section 3.5). Nothing fails when a line is
#                     missing or wrong: a podcast-free project that receives the podcast
#                     workflow simply has it, and a skill fires on description match — so a
#                     skill that shipped without its documents "competes for work it cannot do"
#                     (SB rule 9). The opposite failure is as quiet: a gate that never opens
#                     leaves a project without the guide its rules route to. And media sits in
#                     syntek-author's repositories, so a third failure is the worst of all: a
#                     media path that syntek-author also renders is a file the two templates
#                     fight over, and an update never stops on it (DESIGN.md Section 10). This
#                     script reads a render and compares it with DESIGN.md, path by path, in
#                     both directions, and with syntek-author's frozen names.
#
#                     The expected contents come from the catalogue in _common.sh (DESIGN.md
#                     Sections 3–5 transcribed), evaluated against the answers the render
#                     recorded in .copier-answers.syntek-media.yml.
#
#                     Twelve checks:
#                       1. The answers file records BRAND_KIND, PLATFORMS and MEDIA_KINDS.
#                       2. Every skill the gates open is present, with its SKILL.md.
#                       3. No shut-gate media skill, and no skill DESIGN.md Section 5.1 does not
#                          name. In an over-author tree syntek-author's skills are skipped and
#                          counted; in a standalone one a syntek-author skill is check 5's.
#                       4. Every moded skill carries exactly one mode file, its brand kind's
#                          own; an unmoded skill carries none.
#                       5. No syntek-author-owned path in a standalone render: Makefile,
#                          .claude/hooks/, .claude/rules/syntek-author/, handoffs/, learning/,
#                          assets/, build/, its layers and supporting folder, or a folder named
#                          as one of its skills (DESIGN.md Section 9, "Media never ships").
#                       6. Every catalogued path is present exactly when its gate is open —
#                          guides, workflows, gated folders, seeds, seed-once examples.
#                       7. No numbered workflow folder in a media layer that DESIGN.md Section
#                          4.3 does not number.
#                       8. No template-only or never-ship path (copier.yml, DESIGN.md, examples/,
#                          .github/, .claude/agents/, .claude/commands/, a root CLAUDE.md or
#                          .gitattributes …).
#                       9. No template delimiter survives rendering.
#                      10. The recorded answers match what DESIGN.md says the render should
#                          record (only when generate-all.sh left a <tree>.expect beside it); a
#                          list answer is compared as its sorted values.
#                      11. No media top-level path, .claude/ path or skill folder is named in
#                          syntek-author-names.txt (DESIGN.md D27). The ten shared files, and
#                          the folders that hold them or the per-template rules folders
#                          (.claude, .claude/rules, .claude/skills), are shared by design. A path
#                          check 5 already reported is not reported again. The file is read on
#                          every run: a missing one is exit 2, never a SKIP.
#                      12. No file but its README.md in any generated/, renders/ or raw/ folder,
#                          at any depth: no stray render, no per-piece output folder and nothing
#                          in one (DESIGN.md D19, D42, D64). Copier's _exclude takes everything
#                          below each output folder and negates its README.md back in above
#                          every gated line (shipped-seeds.sh check 16), so the audiobook
#                          folder's generated/ and renders/ ship only their READMEs where the
#                          gate is open and nothing where it is shut (check 6); this check is
#                          the render's proof. Each entry directly inside an output folder is
#                          reported once, a folder with the count of files it holds.
#
#                     Numbers are stable identifiers. Append, never renumber.
#
#                     Over-author scope (DESIGN.md Section 7): on a <kind>--over-author tree,
#                     whose <tree>.owned lists the files media's copy added, checks 5 and 8 are
#                     skipped (syntek-author's paths are there by design; coexist-test.sh check 6
#                     proves ownership), and checks 3, 7, 9, 11 and 12 read media-owned paths
#                     only.
#
#                     What it CANNOT check: a file's CONTENT — a gated row inside an index file
#                     that names an absent path is doc-references.sh's, and a shared file that
#                     differs between renders is byte-identity.sh's. Nor a path DESIGN.md never
#                     named; check 7 covers workflows, the one family whose numbering is frozen.
#
# SELF-TEST. --self-test builds a business tree from the catalogue at runtime, with a fixture
#            names file, proves it clean, then applies one mutation per check and asserts
#            exactly one finding each; then proves the over-author scope on a composite tree.
#
# Requirements: bash 4+, grep, awk, find. No network. Does NOT render — pass trees that
#               generate-all.sh (or `copier copy`) produced.
#
# Usage: shipped-brands.sh [--root DIR] [--quiet] [--self-test] [--help] <rendered-tree>...
#
# Exit codes:  0 = every tree carries exactly its brand
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, a tree that does not exist, no
#                  syntek-author-names.txt)

set -euo pipefail
SCRIPT_NAME="shipped-brands.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
TARGETS=()

usage() {
  cat <<'EOF'
shipped-brands.sh — Verify a rendered project carries exactly what its brand should

Usage: shipped-brands.sh [--root DIR] [--quiet] [--self-test] [--help] <rendered-tree>...

  --root DIR   The template repository (default: this repository)
  --quiet      Print findings only
  --self-test  Prove the checks still fire against a tree built at runtime
  --help       Show this message

A <tree>.expect file beside a tree (written by generate-all.sh) adds check 10; a <tree>.owned
file marks an over-author tree and narrows the checks to media's paths.
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
EXPECT=""
AUTHOR_SKILLS_SKIPPED=0

# Shared by design: the ten copy-only files, the folders that hold them, and the per-template
# rules folder's parent (DESIGN.md Section 9, rules 2 and 3).
shared_entry() { # $1 = a top-level entry or a .claude/ path
  case "$1" in
    .claude|.claude/rules|.claude/skills) return 0 ;;
  esac
  is_shared "$1"
}

run_checks() {
  FINDINGS=()
  AUTHOR_SKILLS_SKIPPED=0
  local s g m have want mf p gate kind path rel k v got hits d l e
  local -A catalogued=() wf_known=() reported5=() tops=() claudes=() skills=()

  # ── 1. The answers ──────────────────────────────────────────────────────────
  if ! load_answers "$TREE/$SM_ANSWERS_FILE"; then
    finding "check 1 — no $SM_ANSWERS_FILE recording BRAND_KIND — the project cannot be updated, and nothing can say what it should hold"
    return 0
  fi
  if [[ -z "$A_PLATFORMS" || -z "$A_KINDS" ]]; then
    k=PLATFORMS; [[ -n "$A_PLATFORMS" ]] && k=MEDIA_KINDS
    finding "check 1 — $SM_ANSWERS_FILE records no $k — the brand's lists decide what ships"
    return 0
  fi

  # ── 2–4. Skills and their mode files ────────────────────────────────────────
  while read -r s g m; do
    [[ -z "$s" ]] && continue
    catalogued["$s"]=1
    if gate_true "$g"; then
      if [[ ! -d "$TREE/.claude/skills/$s" ]]; then
        finding "check 2 — skill $s is missing — this $A_KIND brand needs it (gate: $g)"; continue
      fi
      [[ -f "$TREE/.claude/skills/$s/SKILL.md" ]] || finding "check 2 — skill $s has no SKILL.md"
    else
      [[ -d "$TREE/.claude/skills/$s" ]] && finding "check 3 — skill $s leaked into this project (gate: $g is shut)"
      continue
    fi
    want=""
    [[ "$m" != - ]] && want="$(mode_for_kind "$A_KIND")"
    for mf in $SM_MODE_FILES; do
      have=false; [[ -f "$TREE/.claude/skills/$s/$mf" ]] && have=true
      if [[ "$mf" == "$want" ]] && ! $have; then finding "check 4 — skill $s is moded but its $mf is missing"; fi
      if [[ "$mf" != "$want" ]] && $have; then finding "check 4 — skill $s carries $mf, which belongs to another brand kind (or to no skill)"; fi
    done
  done <<< "$SM_SKILLS"
  if [[ -d "$TREE/.claude/skills" ]]; then
    while IFS= read -r d; do
      [[ -n "${catalogued[$d]:-}" ]] && continue
      if $SM_OWNED_MODE; then
        if ! is_owned_dir ".claude/skills/$d"; then AUTHOR_SKILLS_SKIPPED=$((AUTHOR_SKILLS_SKIPPED + 1)); continue; fi
      elif [[ -n "${SM_AUTHOR_SKILL[$d]:-}" ]]; then
        continue   # check 5's
      fi
      finding "check 3 — skill $d is not one DESIGN.md Section 5.1 names"
    done < <(find "$TREE/.claude/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
  fi

  # ── 5. syntek-author's paths in a standalone render ─────────────────────────
  if ! $SM_OWNED_MODE; then
    for p in $SM_AUTHOR_NEVER; do
      if [[ -e "$TREE/$p" ]]; then
        finding "check 5 — $p is syntek-author's; a standalone media render never ships it (DESIGN.md Section 9)"
        reported5["$p"]=1
      fi
    done
    for s in "${!SM_AUTHOR_SKILL[@]}"; do
      if [[ -e "$TREE/.claude/skills/$s" ]]; then
        finding "check 5 — .claude/skills/$s/ is a syntek-author skill; media never ships it (DESIGN.md D10)"
        reported5[".claude/skills/$s"]=1
      fi
    done
  fi

  # ── 6. Every catalogued path, both directions ───────────────────────────────
  while read -r gate kind path; do
    [[ -z "$gate" ]] && continue
    if gate_true "$gate"; then
      if [[ "$kind" == d && ! -d "$TREE/$path" ]]; then finding "check 6 — $path/ is missing (gate: $gate is open)"
      elif [[ "$kind" == f && ! -f "$TREE/$path" ]]; then finding "check 6 — $path is missing (gate: $gate is open)"; fi
    else
      [[ -e "$TREE/$path" ]] && finding "check 6 — $path leaked into this project (gate: $gate is shut)"
    fi
  done <<< "$SM_PATHS"

  # ── 7. Workflow folders DESIGN.md does not number ───────────────────────────
  while read -r gate kind path; do
    [[ "$path" == */workflows/[0-9][0-9]-* ]] && wf_known["$path"]=1
  done <<< "$SM_PATHS"
  for l in $SM_LAYERS; do
    [[ -d "$TREE/$l/workflows" ]] || continue
    while IFS= read -r rel; do
      [[ -n "${wf_known[$rel]:-}" ]] && continue
      is_owned_dir "$rel" || continue
      finding "check 7 — $rel/ is a workflow DESIGN.md Section 4.3 does not number (author procedures belong in workflows/local/)"
    done < <(cd "$TREE" && find "./$l/workflows" -mindepth 1 -maxdepth 1 -type d -name '[0-9][0-9]-*' | sed 's#^\./##' | sort)
  done

  # ── 8. Template-only and never-ship paths ───────────────────────────────────
  if ! $SM_OWNED_MODE; then
    for p in $SM_NEVER; do
      [[ -e "$TREE/$p" ]] && finding "check 8 — $p is in the project; it belongs to the template repository, a retired tier, or no template at all"
    done
  fi

  # ── 9. No delimiter survives ────────────────────────────────────────────────
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    is_owned_file "$rel" || continue
    hits="$(grep -cE '<%|<:|<~' "$TREE/$rel" || true)"
    finding "check 9 — $rel carries $hits line(s) with a template delimiter that survived rendering"
  done < <(cd "$TREE" && grep -rIlE --exclude-dir=.git '<%|<:|<~' . 2>/dev/null | sed 's#^\./##' | sort || true)

  # ── 10. The answers DESIGN.md expects ───────────────────────────────────────
  if [[ -n "$EXPECT" && -f "$EXPECT" ]]; then
    while IFS='=' read -r k v; do
      [[ -z "$k" ]] && continue
      case "$k" in
        PLATFORMS|MEDIA_KINDS) got="$(answer_list "$k" "$TREE/$SM_ANSWERS_FILE" | LC_ALL=C sort | paste -sd, -)" ;;
        *) got="$(answer_value "$k" "$TREE/$SM_ANSWERS_FILE")" ;;
      esac
      [[ "$k" == SEED_EXAMPLES && -z "$got" ]] && got=true
      [[ -z "$got" && "$k" == MODEL_MECHANICAL ]] && continue
      [[ "$got" == "$v" ]] || finding "check 10 — the render recorded $k=$got; DESIGN.md Section 2 gives $v for this profile"
    done < "$EXPECT"
  fi

  # ── 11. No media path is one of syntek-author's names ───────────────────────
  if $SM_OWNED_MODE; then
    for p in "${!SM_OWNED[@]}"; do
      tops["${p%%/*}"]=1
      if [[ "$p" == .claude/*/* ]]; then e="${p#.claude/}"; claudes["${e%%/*}"]=1
      elif [[ "$p" == .claude/* ]]; then claudes["${p#.claude/}"]=1; fi
      if [[ "$p" == .claude/skills/*/* ]]; then e="${p#.claude/skills/}"; skills["${e%%/*}"]=1; fi
    done
  else
    while IFS= read -r e; do tops["$e"]=1; done < <(find "$TREE" -mindepth 1 -maxdepth 1 ! -name .git -printf '%f\n')
    if [[ -d "$TREE/.claude" ]]; then
      while IFS= read -r e; do claudes["$e"]=1; done < <(find "$TREE/.claude" -mindepth 1 -maxdepth 1 -printf '%f\n')
    fi
    if [[ -d "$TREE/.claude/skills" ]]; then
      while IFS= read -r e; do skills["$e"]=1; done < <(find "$TREE/.claude/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n')
    fi
  fi
  for e in "${!tops[@]}"; do
    [[ -n "${SM_AUTHOR_TOP[$e]:-}" ]] || continue
    shared_entry "$e" && continue
    [[ -n "${reported5[$e]:-}" ]] && continue
    finding "check 11 — the top-level path $e is a syntek-author name (syntek-author-names.txt) — an update would overwrite one template's file with the other's"
  done
  for e in "${!claudes[@]}"; do
    [[ -n "${SM_AUTHOR_CLAUDE[$e]:-}" ]] || continue
    shared_entry ".claude/$e" && continue
    [[ -n "${reported5[.claude/$e]:-}" ]] && continue
    finding "check 11 — .claude/$e is a syntek-author name (syntek-author-names.txt)"
  done
  for e in "${!skills[@]}"; do
    [[ -n "${SM_AUTHOR_SKILL[$e]:-}" ]] || continue
    [[ -n "${reported5[.claude/skills/$e]:-}" ]] && continue
    finding "check 11 — the skill folder $e is a syntek-author skill (syntek-author-names.txt)"
  done

  # ── 12. An output folder ships its README.md and nothing else, at any depth ──
  # The outermost generated/, renders/ or raw/ on each path is the output folder; whatever else
  # sits in it — a stray render, a per-piece folder (D64), a README.md in one — is reported once,
  # by the entry directly inside the output folder, with what it holds.
  local -a outs=()
  local o seen_out n_in
  while IFS= read -r d; do
    d="${d#./}"; seen_out=false
    for o in "${outs[@]}"; do [[ "$d" == "$o"/* ]] && { seen_out=true; break; }; done
    $seen_out || outs+=("$d")
  done < <(cd "$TREE" && find . -name .git -prune -o -type d \( -name generated -o -name renders -o -name raw \) -print | LC_ALL=C sort)
  for o in "${outs[@]}"; do
    while IFS= read -r e; do
      e="${e#./}"; rel="$o/$e"
      if [[ -d "$TREE/$rel" && ! -L "$TREE/$rel" ]]; then
        if $SM_OWNED_MODE && [[ -z "${SM_OWNED_DIRS[$rel]:-}" ]]; then continue; fi
        n_in="$(find "$TREE/$rel" -type f | wc -l | tr -d ' ')"
        finding "check 12 — $rel/ ships inside $o/ ($n_in file(s) in it), which ships its README.md and nothing else: a per-piece output folder or anything in one never ships (D19, D42, D64)"
      else
        [[ "$e" == README.md ]] && continue
        is_owned_file "$rel" || continue
        finding "check 12 — $rel ships inside $o/, which ships its README.md and nothing else (D19, D42)"
      fi
    done < <(cd "$TREE/$o" && find . -mindepth 1 -maxdepth 1 -printf '%f\n' | LC_ALL=C sort)
  done
}

# ── Self-test ────────────────────────────────────────────────────────────────

build_tree() { # $1 = dir — every path the catalogue says the current answers open
  local t="$1" s g m gate kind path
  mkdir -p "$t/.claude/skills"
  while read -r gate kind path; do
    [[ -z "$gate" ]] && continue
    gate_true "$gate" || continue
    if [[ "$kind" == d ]]; then mkdir -p "$t/$path"; else mkdir -p "$(dirname "$t/$path")"; printf 'x\n' > "$t/$path"; fi
  done <<< "$SM_PATHS"
  while read -r s g m; do
    [[ -z "$s" ]] && continue
    gate_true "$g" || continue
    mkdir -p "$t/.claude/skills/$s"; printf -- '---\nname: %s\n---\n' "$s" > "$t/.claude/skills/$s/SKILL.md"
    [[ "$m" != - ]] && printf 'x\n' > "$t/.claude/skills/$s/$(mode_for_kind "$A_KIND")"
  done <<< "$SM_SKILLS"
  {
    printf 'BRAND_KIND: %s\nPLATFORMS:\n' "$A_KIND"; printf -- '- %s\n' $A_PLATFORMS
    printf 'MEDIA_KINDS:\n'; printf -- '- %s\n' $A_KINDS
    printf 'SEED_EXAMPLES: %s\nMODEL_MECHANICAL: opus\n' "$A_SEED"
  } > "$t/$SM_ANSWERS_FILE"
}

self_test() {
  local tmp real_names="$SM_AUTHOR_NAMES_FILE" f p
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  SM_AUTHOR_NAMES_FILE="$tmp/names.txt"
  printf '# fixture names\n%s\n' "top .claude
top CONTEXT.md
top Makefile
top README.md
top build
top manuscript
top scenes
claude CLAUDE.md
claude hooks
claude rules
claude skills
skill run-workflow
skill spelling
rules 01-layout-and-routing.md" > "$SM_AUTHOR_NAMES_FILE"
  require_author_names
  A_KIND=business; A_PLATFORMS="youtube linkedin instagram"; A_KINDS="short-video long-video voiceover"; A_SEED=true
  TREE="$tmp/gen"; EXPECT=""; load_owned "$TREE"
  build_tree "$TREE"
  st_baseline "a business tree built from the catalogue"

  mv "$TREE/$SM_ANSWERS_FILE" "$tmp/held"
  probe "check 1 fires when the answers file is missing" "check 1"
  sed '/^PLATFORMS:/,/^MEDIA_KINDS:/{/^PLATFORMS:/d;/^- /d}' "$tmp/held" > "$TREE/$SM_ANSWERS_FILE"
  probe "check 1 fires when the answers record no PLATFORMS" "check 1 — $SM_ANSWERS_FILE records no PLATFORMS"
  mv "$tmp/held" "$TREE/$SM_ANSWERS_FILE"

  mv "$TREE/.claude/skills/voiceover" "$tmp/held"
  probe "check 2 fires when an always-shipped skill is missing" "check 2 — skill voiceover"
  mv "$tmp/held" "$TREE/.claude/skills/voiceover"

  mkdir -p "$TREE/.claude/skills/narrate-audiobook"
  probe "check 3 fires when a shut-gate skill leaks" "check 3 — skill narrate-audiobook leaked"
  rm -rf "$TREE/.claude/skills/narrate-audiobook"
  mkdir -p "$TREE/.claude/skills/make-a-meme"
  probe "check 3 fires on a skill DESIGN.md does not name" "check 3 — skill make-a-meme is not one"
  rm -rf "$TREE/.claude/skills/make-a-meme"

  printf 'x\n' > "$TREE/.claude/skills/write-script/FICTION.md"
  probe "check 4 fires on a second mode file" "check 4 — skill write-script carries FICTION.md"
  rm -f "$TREE/.claude/skills/write-script/FICTION.md"

  printf 'help:\n' > "$TREE/Makefile"
  probe "check 5 fires when syntek-author's Makefile ships standalone" "check 5 — Makefile"
  rm -f "$TREE/Makefile"
  mkdir -p "$TREE/.claude/skills/spelling"
  probe "check 5 fires when a syntek-author skill ships standalone" "check 5 — .claude/skills/spelling/"
  rm -rf "$TREE/.claude/skills/spelling"

  mv "$TREE/publishing/docs/reference/linkedin.md" "$tmp/held"
  probe "check 6 fires when an open platform's guide is missing" "check 6 — publishing/docs/reference/linkedin.md is missing"
  mv "$tmp/held" "$TREE/publishing/docs/reference/linkedin.md"
  mkdir -p "$TREE/production/workflows/04-master-a-podcast-episode"
  probe "check 6 fires when a shut media kind's workflow leaks" "check 6 — production/workflows/04-master-a-podcast-episode leaked"
  rmdir "$TREE/production/workflows/04-master-a-podcast-episode"

  mkdir -p "$TREE/publishing/workflows/99-invent-a-step"
  probe "check 7 fires on an unnumbered workflow" "check 7"
  rmdir "$TREE/publishing/workflows/99-invent-a-step"

  printf 'x\n' > "$TREE/copier.yml"
  probe "check 8 fires when copier.yml leaks" "check 8 — copier.yml"
  rm -f "$TREE/copier.yml"

  printf 'Hello <%%BRAND_NAME%%>\n' >> "$TREE/README.md"
  probe "check 9 fires on a surviving token" "check 9 — README.md"
  printf 'x\n' > "$TREE/README.md"

  printf 'BRAND_KIND=business\nPLATFORMS=instagram,linkedin,tiktok\n' > "$tmp/expect"; EXPECT="$tmp/expect"
  probe "check 10 fires when the recorded platforms differ from DESIGN.md's" "check 10 — the render recorded PLATFORMS=instagram,linkedin,youtube"
  printf 'BRAND_KIND=business\nPLATFORMS=instagram,linkedin,youtube\nMEDIA_KINDS=long-video,short-video,voiceover\nSEED_EXAMPLES=true\n' > "$tmp/expect"
  probe_clean "the same lists in another order are the same answer"
  EXPECT=""

  mkdir -p "$TREE/scenes"; printf 'x\n' > "$TREE/scenes/CONTEXT.md"
  probe "check 11 fires on a top-level path syntek-author has since taken" "check 11 — the top-level path scenes"
  rm -rf "$TREE/scenes"
  # The exemption is the three shared containers (.claude, .claude/rules, .claude/skills) and
  # the ten shared files (FIXES A4) — not every .claude/ path syntek-author names.
  cp "$SM_AUTHOR_NAMES_FILE" "$tmp/names.held"; printf 'claude design\n' >> "$SM_AUTHOR_NAMES_FILE"; require_author_names
  mkdir -p "$TREE/.claude/design"; printf 'x\n' > "$TREE/.claude/design/notes.md"
  probe "check 11 fires on a .claude/ path that is not a shared container" "check 11 — .claude/design is a syntek-author name"
  rm -rf "$TREE/.claude/design"; cp "$tmp/names.held" "$SM_AUTHOR_NAMES_FILE"; require_author_names

  # 12: an output folder ships its README.md alone, at any depth.
  mkdir -p "$TREE/production/src/renders/003-ferry/cards"; printf 'x\n' > "$TREE/production/src/renders/003-ferry/cards/003-ferry.title.1920x1080.png"
  probe "check 12 fires on a per-piece output folder holding a card render" "check 12 — production/src/renders/003-ferry/ ships inside production/src/renders/ (1 file(s) in it)"
  rm -f "$TREE/production/src/renders/003-ferry/cards/003-ferry.title.1920x1080.png"
  probe "check 12 fires on an empty per-piece output folder" "check 12 — production/src/renders/003-ferry/ ships inside production/src/renders/ (0 file(s) in it)"
  printf 'x\n' > "$TREE/production/src/renders/003-ferry/README.md"; rmdir "$TREE/production/src/renders/003-ferry/cards"
  probe "check 12 fires on a README.md inside a per-piece output folder" "check 12 — production/src/renders/003-ferry/ ships inside"
  rm -rf "$TREE/production/src/renders/003-ferry"
  mkdir -p "$TREE/production/src/voiceover/generated/003-ferry/takes"; printf 'x\n' > "$TREE/production/src/voiceover/generated/003-ferry/takes/003-ferry.s01.t1.mp3"
  probe "check 12 fires on a take in a piece's takes/ folder" "check 12 — production/src/voiceover/generated/003-ferry/ ships inside production/src/voiceover/generated/"
  rm -rf "$TREE/production/src/voiceover/generated/003-ferry"
  printf 'x\n' > "$TREE/publishing/src/renders/003-ferry.youtube-short.mp4"
  probe "check 12 fires on a flat render beside the README.md" "check 12 — publishing/src/renders/003-ferry.youtube-short.mp4 ships inside publishing/src/renders/"
  rm -f "$TREE/publishing/src/renders/003-ferry.youtube-short.mp4"
  probe_clean "each output folder holding its README.md alone ships clean"

  # The over-author scope: syntek-author's files beside media's, and .owned listing media's.
  f="$tmp/oa"; TREE="$f"; build_tree "$TREE"
  mkdir -p "$f/.claude/skills/spelling" "$f/manuscript" "$f/.claude/hooks"
  printf 'x\n' > "$f/.claude/skills/spelling/SKILL.md"; printf 'help:\n' > "$f/Makefile"
  printf 'x\n' > "$f/manuscript/CONTEXT.md"; printf 'x\n' > "$f/.claude/hooks/CONTEXT.md"
  while IFS= read -r p; do
    case "$p" in .claude/skills/spelling/*|manuscript/*|.claude/hooks/*|Makefile) continue ;; esac
    is_shared "$p" && continue
    printf '%s\n' "$p"
  done < <(tree_files "$f") > "$f.owned"
  load_owned "$TREE"
  st_baseline "an over-author tree: syntek-author's Makefile, layer and skill beside media's paths"
  probe_clean "syntek-author's skills are skipped and counted, never flagged, over syntek-author"
  mkdir -p "$f/production/src/footage/raw"; printf 'x\n' > "$f/production/src/footage/raw/cam-a.mov"
  probe_clean "a file syntek-author's side left in an output folder is not media's, over syntek-author"
  printf 'production/src/footage/raw/cam-a.mov\n' >> "$f.owned"; load_owned "$TREE"
  probe "check 12 fires on a media-owned file in an output folder, over syntek-author" "check 12 — production/src/footage/raw/cam-a.mov ships inside production/src/footage/raw/"
  rm -f "$f/production/src/footage/raw/cam-a.mov"; sed -i '/cam-a.mov/d' "$f.owned"; load_owned "$TREE"
  mkdir -p "$f/standards"; printf 'x\n' > "$f/standards/notes.md"; printf 'standards/notes.md\n' >> "$f.owned"
  printf 'top standards\n' >> "$SM_AUTHOR_NAMES_FILE"; require_author_names; load_owned "$TREE"
  probe "check 11 fires on a media-owned path syntek-author also names, over syntek-author" "check 11 — the top-level path standards"
  SM_OWNED_MODE=false; SM_OWNED=()

  SM_AUTHOR_NAMES_FILE="$real_names"
  st_finish "a correctly gated render from a leaking or incomplete one"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

[[ ${#TARGETS[@]} -gt 0 ]] || die "no rendered tree given — this script asserts on trees Copier produced (see generate-all.sh)"
require_author_names
build_sets "$SM_ROOT/copier.yml"

bold "▸ $SCRIPT_NAME"
STATUS=0
for target in "${TARGETS[@]}"; do
  [[ -d "$target" ]] || die "not a directory: $target"
  TREE="$(cd "$target" && pwd)"
  EXPECT=""; [[ -f "$TREE.expect" ]] && EXPECT="$TREE.expect"
  load_owned "$TREE"
  run_checks
  scope="standalone"; $SM_OWNED_MODE && scope="over syntek-author, ${#SM_OWNED[@]} media-owned file(s), $AUTHOR_SKILLS_SKIPPED syntek-author skill(s) skipped"
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $TREE — the $A_KIND brand, exactly ($scope)"
  else
    bold "✗ $TREE — ${#FINDINGS[@]} finding(s) ($scope):"
    print_findings
    STATUS=1
  fi
done
log ""
if [[ "$STATUS" -eq 0 ]]; then
  bold "✓ ${#TARGETS[@]} tree(s): every brand carries exactly its own paths, skills and mode files, and no syntek-author name."
  exit 0
fi
log "  A path shipped where it should not, or did not ship where it should. Fix the gate in"
log "  copier.yml's _exclude (DESIGN.md Section 3.5), or the file's place under template/."
exit 1

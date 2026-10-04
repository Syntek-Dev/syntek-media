#!/usr/bin/env bash
#
# coexist-test.sh — Prove syntek-media shares a project with the real syntek-author, both ways.
#
#                   Media is applied to repositories syntek-author made (DESIGN.md D4, Section
#                   8), and both templates update the same project for years. That works only if
#                   neither can write over the other: each keeps its own answers file, its own
#                   rules folder and its own skills, and the ten files both ship are seeds in
#                   both — written by whichever came first, updated by neither (D11). Nothing
#                   fails loudly when that breaks. A copy that collides stops only for want of
#                   a terminal; an update that collides writes conflict markers into the other
#                   template's files, on some later day, in the author's project (Section 10).
#                   So this test takes the REAL syntek-author — a snapshot of the --author
#                   working tree, uncommitted work included — and, per brand kind:
#
#                     1. renders syntek-author with the paired DOC_TYPE and commits it, then runs
#                        syntek-author's own doc-references.sh on it;
#                     2. applies media over it WITHOUT --overwrite, and runs that audit again;
#                     3. changes one template-owned file in each template, and updates both;
#                     4. updates each again with nothing changed;
#                     5. deletes a shared file and updates media;
#                     6. updates media with one platform and one media kind taken away;
#                     7. applies the two the other way round in a fresh project.
#
#                   Twenty-one checks per brand kind (13 and 20 once per run):
#                     1. Media applies over the syntek-author project without --overwrite —
#                        nothing it ships collides with what is there.
#                     2. Both answers files exist, under different names.
#                     3. syntek-author's update succeeds and delivers its change.
#                     4. Media's update succeeds and delivers its change.
#                     5. Each template's changed file survives the other's update.
#                     6. No file is owned by both: a path one template renders and does not seed
#                        is never shipped by the other.
#                     7. No conflict is left behind (no *.rej file, no conflict marker).
#                     8. Media's copy changed no byte that was there.
#                     9. syntek-author's update touched only its own paths and answers file.
#                    10. Media's update touched only its own paths (B_OWNED: what media's copy
#                        added) and its answers file.
#                    11. A second syntek-author update changes nothing — no media file perturbed
#                        its three-way merge.
#                    12. The shared files are still syntek-author's, byte for byte.
#                    13. No media skill or top-level path shares a name with anything in
#                        syntek-author's template/ — every variant, read from the live tree —
#                        the shared files and the .claude/ container excepted.
#                    14. Both rules folders are present: .claude/rules/syntek-author/ and
#                        .claude/rules/syntek-media/.
#                    15. Media first, then syntek-author: both apply without --overwrite.
#                    16. A second media update with no template change leaves
#                        `git status --porcelain` empty.
#                    17. A shared file deleted and committed (.claude/skills/CLAUDE.md) stays
#                        absent after media's update. Asserted on media's step only:
#                        syntek-author's update recreates its own seeds by design.
#                    18. A media update that removes one platform and one media kind succeeds,
#                        changes only paths in B_OWNED (and media's answers file), and leaves
#                        every syntek-author file byte-identical.
#                    19. Media's copy output (without --quiet) carries every _message_after_copy
#                        line of _common.sh's lists: the shared files and the skip rule, each
#                        D13 allow, ask and Edit deny, the ELEVENLABS_MCP_BASE_PATH line, the
#                        filter.lfs.required line, the check --setup line and the -a update
#                        command; and Section 8's lines: Copier's 'conflict' then 'skip' is
#                        expected, the optional line in .claude/CLAUDE.md, and nothing to add
#                        to .gitignore or .mcp.json.
#                    20. syntek-author-names.txt equals the names of the --author tree. Drift
#                        fails: run --refresh-names, re-check every new name against media's
#                        paths, and record the new baseline in CHANGELOG.md (DESIGN.md D27).
#                    21. syntek-author's own doc-references.sh, run on the composite, reports
#                        nothing it does not report on the syntek-author-only project.
#
#                   Without syntek-author (no --author, no SYNTEK_AUTHOR_DIR, no
#                   ../syntek-author) the test prints a named SKIP and exits 0. A SKIP is never
#                   a pass, and a release is never tagged on one (D27).
#
#                   --refresh-names writes syntek-author-names.txt from the --author tree — a
#                   header naming the date and syntek-author's commit "plus working tree", then
#                   one sorted line per name — prints what moved, and runs nothing else. It is
#                   the only writer of that file.
#
#                   Copier prints a MissingFileWarning on a fresh copy (the previous answers are
#                   read through _external_data, D14). It is expected and never a finding.
#
#                   Numbers are stable identifiers. Append, never renumber.
#
#                   What it CANNOT check: a syntek-author release that does not exist yet, or a
#                   collision only some answer combination this test does not render would
#                   reveal (check 13 reads every variant's NAMES, not every variant's files).
#
# SELF-TEST. --self-test runs the whole flow with the fixture syntek-author and the fixture
#            media of _common.sh (no real syntek-author needed), proves the result clean, then
#            mutates the result once per check and asserts exactly one finding each.
#
# Requirements: bash 4.3+, git, rsync, uvx (or COPIER_CMD), python3. Network on the first uvx
#               run only. A syntek-author working tree for the real run.
#
# Usage: coexist-test.sh [--root DIR] [--author DIR] [--brand-kind K[,K…]] [--refresh-names]
#                        [--quiet] [--self-test] [--help]
#
# Exit codes:  0 = the two templates share every project cleanly, or a named SKIP
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, missing tools, an --author that is not
#                  syntek-author, --refresh-names without one)

set -euo pipefail
SCRIPT_NAME="coexist-test.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
REFRESH=false
AUTHOR_ARG=""
KINDS="$SM_KINDS"

usage() {
  cat <<'EOF'
coexist-test.sh — Prove syntek-media shares a project with the real syntek-author, both ways

Usage: coexist-test.sh [--root DIR] [--author DIR] [--brand-kind K[,K…]] [--refresh-names]
                       [--quiet] [--self-test] [--help]

  --root DIR         The syntek-media repository (default: this repository)
  --author DIR       The syntek-author working tree (default: $SYNTEK_AUTHOR_DIR, else
                     ../syntek-author; none = a named SKIP)
  --brand-kind LIST  Which kinds to test (default: business,author-fiction,author-nonfiction)
  --refresh-names    Rewrite syntek-author-names.txt from the --author tree, and stop
  --quiet            Print findings only
  --self-test        Prove the checks still fire against the fixture templates
  --help             Show this message

Exit codes: 0 = coexist cleanly, or SKIP (named)  1 = finding(s), or the self-test no longer
            separates  2 = script error
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)          [[ $# -gt 1 ]] || die "--root needs a value"; SM_ROOT="$(cd "$2" && pwd)" || die "no such directory: $2"; shift 2 ;;
    --author)        [[ $# -gt 1 ]] || die "--author needs a value"; AUTHOR_ARG="$2"; shift 2 ;;
    --brand-kind)    [[ $# -gt 1 ]] || die "--brand-kind needs a value"; KINDS="${2//,/ }"; shift 2 ;;
    --refresh-names) REFRESH=true; shift ;;
    --quiet|-q)      QUIET=true; shift ;;
    --self-test)     SELF_TEST=true; shift ;;
    --help|-h)       usage; exit 0 ;;
    *)               die "unknown argument: $1" ;;
  esac
done

A_MARK="<!-- coexist-test: a syntek-author change -->"
B_MARK="<!-- coexist-test: a syntek-media change -->"
B_RULE=".claude/rules/syntek-media/01-layout-and-routing.md"
S17_FILE=".claude/skills/CLAUDE.md"

AUTHOR_SRC=""; MEDIA_SRC=""
KIND=""; W=""; PROJ=""; A_RULE=""
A_COPY=0; B_COPY=0; A_UPDATE=0; B_UPDATE=0; A_AGAIN_STATUS=0; B_AGAIN_STATUS=0
S17_STATUS=0; S17_BACK=false; R_STATUS=0; R_WHAT=""; REV_A=0; REV_B=0
A_OWNED=(); A_ALL=(); B_TOWNED=(); B_ALL=()
A_TOP_NAMES=(); A_SKILL_NAMES=(); B_TOP_NAMES=(); B_SKILL_NAMES=()
NAMES_DRIFT=""; GLOBAL=false

# syntek-author's own doc-references.sh on a tree: its findings, sorted, in OUT; its exit
# status in OUT.status ("missing" when syntek-author has no such audit).
author_doc_references() { # $1 = syntek-author snapshot, $2 = tree, $3 = out file
  local s="$1/.github/scripts/doc-references.sh" st=0
  : > "$3"
  if [[ ! -f "$s" ]]; then printf 'missing\n' > "$3.status"; return 0; fi
  bash "$s" --quiet "$2" > "$3.raw" 2>&1 || st=$?
  printf '%s\n' "$st" > "$3.status"
  { grep -E '^[[:space:]]*· ' "$3.raw" || true; } | sed 's/^[[:space:]]*//' | LC_ALL=C sort -u > "$3"
}

# The names check 13 compares: syntek-author's from its live template/ (every variant), media's
# from its own template/.
collect_names() { # $1 = syntek-author repo, $2 = syntek-media repo
  local kind name
  A_TOP_NAMES=(); A_SKILL_NAMES=(); B_TOP_NAMES=(); B_SKILL_NAMES=()
  while read -r kind name; do
    case "$kind" in top) A_TOP_NAMES+=("$name") ;; skill) A_SKILL_NAMES+=("$name") ;; esac
  done < <(author_names "$1")
  while IFS= read -r name; do B_TOP_NAMES+=("$name"); done < <(find "$2/template" -mindepth 1 -maxdepth 1 -printf '%f\n' | LC_ALL=C sort)
  if [[ -d "$2/template/.claude/skills" ]]; then
    while IFS= read -r name; do B_SKILL_NAMES+=("$name"); done < <(find "$2/template/.claude/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | LC_ALL=C sort)
  fi
}

global_state() { # $1 = syntek-author repo, $2 = syntek-media repo
  collect_names "$1" "$2"
  if [[ -f "$SM_AUTHOR_NAMES_FILE" ]]; then NAMES_DRIFT="$(names_drift "$1")"
  else NAMES_DRIFT="missing"; fi
}

run_flow() { # $1 = BRAND_KIND, $2 = work dir — fills the state the checks read
  local kind="$1" w="$2" a="$2/a" b="$2/b" log="$2/flow.log" doc k p rp rk f
  KIND="$kind"; W="$w"; PROJ="$w/proj"; doc="$(author_doc_for_kind "$kind")"
  A_COPY=0; B_COPY=0; A_UPDATE=0; B_UPDATE=0; A_AGAIN_STATUS=0; B_AGAIN_STATUS=0
  S17_STATUS=0; S17_BACK=false; R_STATUS=0; R_WHAT=""; REV_A=0; REV_B=0
  A_OWNED=(); A_ALL=(); B_TOWNED=(); B_ALL=()
  for f in pre-media.sha post-media.sha shared-after.sha a-changed.txt b-changed.txt a-again.txt \
           b-again.txt r-changed.txt pre-remove.sha post-remove.sha b-added.txt b-copy.log; do : > "$w/$f"; done
  sm_snapshot "$AUTHOR_SRC" "$a" >>"$log" 2>&1 || die "could not snapshot $AUTHOR_SRC"
  sm_snapshot "$MEDIA_SRC" "$b" >>"$log" 2>&1 || die "could not snapshot $MEDIA_SRC"
  [[ ${#SM_COPIER[@]} -gt 0 ]] || copier_init

  # 1. syntek-author first, committed, and audited by its own doc-references.sh.
  sm_render_author "$a" "$PROJ" "$doc" >>"$log" 2>&1 || A_COPY=$?
  [[ "$A_COPY" -eq 0 ]] || return 0
  [[ -d "$PROJ/.git" ]] || sm_git "$PROJ" init -q
  sm_commit_all "$PROJ" 'syntek-author'
  while read -r k p; do
    if [[ "$k" == O ]]; then A_OWNED+=("$p"); else A_ALL+=("$p"); fi
  done < <(owned_and_all "$PROJ" "$a/copier.yml" "$SM_AUTHOR_ANSWERS")
  hash_tree "$PROJ" > "$w/pre-media.sha"
  author_doc_references "$a" "$PROJ" "$w/dr-author.txt"

  # Media alone, for what it owns.
  sm_render "$b" "$w/b-alone" "$kind" >>"$log" 2>&1 || true
  if [[ -d "$w/b-alone" ]]; then
    while read -r k p; do
      if [[ "$k" == O ]]; then B_TOWNED+=("$p"); else B_ALL+=("$p"); fi
    done < <(owned_and_all "$w/b-alone" "$b/copier.yml" "$SM_ANSWERS_FILE")
  fi

  # 2. Media over it, without --overwrite; B_OWNED is what its copy added.
  sm_render "$b" "$PROJ" "$kind" >"$w/b-copy.log" 2>&1 || B_COPY=$?
  cat "$w/b-copy.log" >> "$log"
  hash_tree "$PROJ" > "$w/post-media.sha"
  LC_ALL=C comm -13 <(cut -f1 "$w/pre-media.sha" | LC_ALL=C sort) <(cut -f1 "$w/post-media.sha" | LC_ALL=C sort) > "$w/b-added.txt"
  sm_commit_all "$PROJ" 'syntek-media'
  author_doc_references "$a" "$PROJ" "$w/dr-composite.txt"

  # 3. Both templates move on; each project takes its own template's update.
  A_RULE=".claude/skills/run-workflow/SKILL.md"
  [[ -f "$a/template/$A_RULE" ]] || A_RULE=".claude/rules/syntek-author/01-layout-and-routing.md"
  [[ -f "$a/template/$A_RULE" ]] || die "syntek-author has neither run-workflow/SKILL.md nor its layout rule — nothing template-owned to change"
  [[ -f "$b/template/$B_RULE" ]] || die "syntek-media has no $B_RULE — nothing template-owned to change"
  printf '\n%s\n' "$A_MARK" >> "$a/template/$A_RULE"; sm_commit_all "$a" 'coexist-test: a syntek-author change'
  printf '\n%s\n' "$B_MARK" >> "$b/template/$B_RULE"; sm_commit_all "$b" 'coexist-test: a syntek-media change'

  sm_update_author "$PROJ" >>"$log" 2>&1 || A_UPDATE=$?
  changed_paths "$PROJ" > "$w/a-changed.txt"; sm_commit_all "$PROJ" 'update syntek-author'
  sm_update "$PROJ" >>"$log" 2>&1 || B_UPDATE=$?
  changed_paths "$PROJ" > "$w/b-changed.txt"; sm_commit_all "$PROJ" 'update syntek-media'

  # 4. Each again, with nothing changed. The shared files are fingerprinted between the two.
  sm_update_author "$PROJ" >>"$log" 2>&1 || A_AGAIN_STATUS=$?
  changed_paths "$PROJ" > "$w/a-again.txt"; sm_commit_all "$PROJ" 'update syntek-author again'
  for p in $SM_SHARED; do
    [[ -f "$PROJ/$p" ]] && printf '%s\t%s\n' "$p" "$(sha1sum < "$PROJ/$p" | cut -d' ' -f1)"
  done | LC_ALL=C sort > "$w/shared-after.sha"
  sm_update "$PROJ" >>"$log" 2>&1 || B_AGAIN_STATUS=$?
  changed_paths "$PROJ" > "$w/b-again.txt"; sm_commit_all "$PROJ" 'update syntek-media again'

  # 5. A shared file the author deleted stays deleted through media's update.
  rm -f "$PROJ/$S17_FILE"; sm_commit_all "$PROJ" 'the author deletes a shared file'
  sm_update "$PROJ" >>"$log" 2>&1 || S17_STATUS=$?
  [[ -e "$PROJ/$S17_FILE" ]] && S17_BACK=true
  sm_commit_all "$PROJ" 'update syntek-media after a deletion'

  # 6. Media takes away one platform and one media kind that carry files.
  rp="$(removable_value PLATFORMS "$PROJ/$SM_ANSWERS_FILE" "$b/copier.yml")"
  rk="$(removable_value MEDIA_KINDS "$PROJ/$SM_ANSWERS_FILE" "$b/copier.yml")"
  if [[ -n "$rp" && -n "$rk" ]]; then
    R_WHAT="PLATFORMS without $rp, MEDIA_KINDS without $rk"
    hash_tree "$PROJ" > "$w/pre-remove.sha"
    sm_update "$PROJ" --data "PLATFORMS=$(list_without PLATFORMS "$PROJ/$SM_ANSWERS_FILE" "$rp")" \
      --data "MEDIA_KINDS=$(list_without MEDIA_KINDS "$PROJ/$SM_ANSWERS_FILE" "$rk")" >>"$log" 2>&1 || R_STATUS=$?
    changed_paths "$PROJ" > "$w/r-changed.txt"
    hash_tree "$PROJ" > "$w/post-remove.sha"
    sm_commit_all "$PROJ" 'update syntek-media without a platform and a media kind'
  else
    R_WHAT="none"
  fi

  # 7. The other order, in a fresh project: media first, then syntek-author.
  sm_render "$b" "$w/rev" "$kind" >>"$log" 2>&1 || REV_B=$?
  if [[ "$REV_B" -eq 0 ]]; then
    [[ -d "$w/rev/.git" ]] || sm_git "$w/rev" init -q
    sm_commit_all "$w/rev" 'syntek-media first'
    sm_render_author "$a" "$w/rev" "$doc" >>"$log" 2>&1 || REV_A=$?
  fi
  return 0
}

in_list() { # $1 = path, $2 = file of paths → true when listed
  grep -qxF -- "$1" "$2" 2>/dev/null
}

run_checks() {
  FINDINGS=()
  local p f n h want missing label="[$KIND]"
  local -A a_owned=() a_all=() b_towned=() b_all=() pre=() post=() rpre=() rpost=() shared=()
  if $GLOBAL; then
    # ── 13. No media name is syntek-author's ──────────────────────────────────
    for n in "${B_TOP_NAMES[@]}"; do
      case "$n" in .claude|"$SM_ANSWERS_FILE") continue ;; esac
      is_shared "$n" && continue
      for p in "${A_TOP_NAMES[@]}"; do
        [[ "$p" == "$n" ]] && finding "check 13 — media's top-level path $n is also in syntek-author's template/ — an update would overwrite one template's file with the other's"
      done
    done
    for n in "${B_SKILL_NAMES[@]}"; do
      for p in "${A_SKILL_NAMES[@]}"; do
        [[ "$p" == "$n" ]] && finding "check 13 — media's skill $n is also a syntek-author skill — the two would fight over .claude/skills/$n/"
      done
    done
    # ── 20. The frozen names are the live tree's ─────────────────────────────
    if [[ "$NAMES_DRIFT" == missing ]]; then
      finding "check 20 — $SM_AUTHOR_NAMES_FILE is missing — write it with --refresh-names --author DIR"
    elif [[ -n "$NAMES_DRIFT" ]]; then
      n="$(printf '%s\n' "$NAMES_DRIFT" | grep -c . || true)"
      finding "check 20 — syntek-author-names.txt has drifted from the --author tree ($n name(s): $(printf '%s\n' "$NAMES_DRIFT" | head -3 | paste -sd';' -)…) — run --refresh-names, re-check every new name against media's paths, and record the baseline in CHANGELOG.md"
    fi
  fi

  if [[ "$A_COPY" -ne 0 ]]; then finding "check 1 — $label syntek-author itself did not render (exit $A_COPY) — see $W/flow.log"; return 0; fi
  [[ "$B_COPY" -eq 0 ]] || finding "check 1 — $label media could not apply over the syntek-author project without --overwrite (exit $B_COPY) — something it ships collides"
  if [[ ! -f "$PROJ/$SM_AUTHOR_ANSWERS" || ! -f "$PROJ/$SM_ANSWERS_FILE" ]]; then
    finding "check 2 — $label the project does not hold both $SM_AUTHOR_ANSWERS and $SM_ANSWERS_FILE"
  fi
  # A file that vanished is check 5's; 3 and 4 judge delivery to a file that is there.
  if [[ "$A_UPDATE" -ne 0 ]]; then finding "check 3 — $label syntek-author's update failed (exit $A_UPDATE)"
  elif [[ -f "$PROJ/$A_RULE" ]] && ! grep -qF "$A_MARK" "$PROJ/$A_RULE"; then finding "check 3 — $label syntek-author's change did not reach $A_RULE"; fi
  if [[ "$B_UPDATE" -ne 0 ]]; then finding "check 4 — $label media's update failed (exit $B_UPDATE)"
  elif [[ -f "$PROJ/$B_RULE" ]] && ! grep -qF "$B_MARK" "$PROJ/$B_RULE"; then finding "check 4 — $label media's change did not reach $B_RULE"; fi
  [[ -f "$PROJ/$A_RULE" ]] || finding "check 5 — $label syntek-author's $A_RULE did not survive media's update"
  [[ -f "$PROJ/$B_RULE" ]] || finding "check 5 — $label media's $B_RULE did not survive syntek-author's update"

  # ── 6. No file owned by both ────────────────────────────────────────────────
  for p in "${A_OWNED[@]}";  do a_owned["$p"]=1; done
  for p in "${A_ALL[@]}";    do a_all["$p"]=1; done
  for p in "${B_TOWNED[@]}"; do b_towned["$p"]=1; done
  for p in "${B_ALL[@]}";    do b_all["$p"]=1; done
  for p in "${!a_owned[@]}"; do
    [[ -n "${b_all[$p]:-}" ]] && finding "check 6 — $label $p is template-owned by syntek-author and shipped by media — seed it in both (DESIGN.md D11)"
  done
  for p in "${!b_towned[@]}"; do
    [[ -n "${a_all[$p]:-}" ]] && finding "check 6 — $label $p is template-owned by media and shipped by syntek-author"
  done

  # ── 7. No conflict left behind ──────────────────────────────────────────────
  while IFS= read -r f; do
    [[ -n "$f" ]] && finding "check 7 — $label conflict left behind: $f"
  done < <(conflicts_in "$PROJ")

  # ── 8. Media's copy changed no byte that was there ──────────────────────────
  while IFS=$'\t' read -r p h; do [[ -n "$p" ]] && pre["$p"]="$h"; done < "$W/pre-media.sha"
  while IFS=$'\t' read -r p h; do [[ -n "$p" ]] && post["$p"]="$h"; done < "$W/post-media.sha"
  if [[ "$B_COPY" -eq 0 ]]; then
    for p in "${!pre[@]}"; do
      [[ "${post[$p]:-gone}" == "${pre[$p]}" ]] || finding "check 8 — $label media's copy changed syntek-author's $p"
    done
  fi

  # ── 9 and 10. Each update touched only its own paths ────────────────────────
  while IFS= read -r p; do
    [[ -z "$p" || "$p" == "$SM_AUTHOR_ANSWERS" || -n "${a_all[$p]:-}" ]] && continue
    finding "check 9 — $label syntek-author's update touched $p, which is not syntek-author's"
  done < "$W/a-changed.txt"
  while IFS= read -r p; do
    [[ -z "$p" || "$p" == "$SM_ANSWERS_FILE" ]] && continue
    in_list "$p" "$W/b-added.txt" || finding "check 10 — $label media's update touched $p, which is not one of media's own paths (B_OWNED)"
  done < "$W/b-changed.txt"

  # ── 11. A second syntek-author update is a no-op ────────────────────────────
  if [[ "$A_AGAIN_STATUS" -ne 0 || -s "$W/a-again.txt" ]]; then
    finding "check 11 — $label a second syntek-author update was not a no-op (exit $A_AGAIN_STATUS; changed: $(head -3 "$W/a-again.txt" | paste -sd' ' -))"
  fi

  # ── 12. The shared files are still syntek-author's ──────────────────────────
  while IFS=$'\t' read -r p h; do [[ -n "$p" ]] && shared["$p"]="$h"; done < "$W/shared-after.sha"
  for p in $SM_SHARED; do
    want="${pre[$p]:-absent}"
    [[ "${shared[$p]:-absent}" == "$want" ]] || finding "check 12 — $label the shared file $p is no longer syntek-author's (it differs from syntek-author's render after both updates)"
  done

  # ── 14. Both rules folders ──────────────────────────────────────────────────
  for p in .claude/rules/syntek-author .claude/rules/syntek-media; do
    [[ -d "$PROJ/$p" ]] || finding "check 14 — $label $p/ is missing from the combined project"
  done

  # ── 15. The other order ─────────────────────────────────────────────────────
  if [[ "$REV_B" -ne 0 ]]; then finding "check 15 — $label media alone did not render as the first template (exit $REV_B)"
  elif [[ "$REV_A" -ne 0 ]]; then finding "check 15 — $label syntek-author could not apply over a media-first project without --overwrite (exit $REV_A)"; fi

  # ── 16. A second media update is a no-op ────────────────────────────────────
  if [[ "$B_AGAIN_STATUS" -ne 0 || -s "$W/b-again.txt" ]]; then
    finding "check 16 — $label a second media update with no template change was not a no-op (exit $B_AGAIN_STATUS; changed: $(head -3 "$W/b-again.txt" | paste -sd' ' -))"
  fi

  # ── 17. A deleted shared file stays deleted through media's update ──────────
  if [[ "$S17_STATUS" -ne 0 ]]; then finding "check 17 — $label media's update after the author deleted $S17_FILE failed (exit $S17_STATUS)"
  elif $S17_BACK; then finding "check 17 — $label media's update recreated $S17_FILE, which the author deleted (its update-gated _exclude line, DESIGN.md D11)"; fi

  # ── 18. Taking away a platform and a media kind ─────────────────────────────
  if [[ "$R_WHAT" == none ]]; then
    finding "check 18 — $label the project's answers name no gated platform and media kind that could be taken away"
  elif [[ "$R_STATUS" -ne 0 ]]; then
    finding "check 18 — $label media's update with $R_WHAT failed (exit $R_STATUS)"
  else
    while IFS= read -r p; do
      [[ -z "$p" || "$p" == "$SM_ANSWERS_FILE" ]] && continue
      in_list "$p" "$W/b-added.txt" || finding "check 18 — $label media's update with $R_WHAT touched $p, which is not one of media's own paths"
    done < "$W/r-changed.txt"
    while IFS=$'\t' read -r p h; do [[ -n "$p" ]] && rpre["$p"]="$h"; done < "$W/pre-remove.sha"
    while IFS=$'\t' read -r p h; do [[ -n "$p" ]] && rpost["$p"]="$h"; done < "$W/post-remove.sha"
    for p in "${!rpre[@]}"; do
      in_list "$p" "$W/b-added.txt" && continue
      [[ "$p" == "$SM_ANSWERS_FILE" ]] && continue
      [[ "${rpost[$p]:-gone}" == "${rpre[$p]}" ]] || finding "check 18 — $label media's update with $R_WHAT changed syntek-author's $p"
    done
  fi

  # ── 19. The copy message ────────────────────────────────────────────────────
  while IFS= read -r missing; do
    [[ -n "$missing" ]] && finding "check 19 — $label media's copy output does not carry '$missing' (_message_after_copy, DESIGN.md D13)"
  done < <(message_missing_lines "$W/b-copy.log")

  # ── 21. syntek-author's own audit, before and after ─────────────────────────
  local sa sc
  sa="$(cat "$W/dr-author.txt.status" 2>/dev/null || echo missing)"
  sc="$(cat "$W/dr-composite.txt.status" 2>/dev/null || echo missing)"
  if [[ "$sa" == missing || "$sc" == missing ]]; then
    finding "check 21 — $label syntek-author has no .github/scripts/doc-references.sh to run on the composite"
  elif [[ "$sa" -ge 2 || "$sc" -ge 2 ]]; then
    finding "check 21 — $label syntek-author's doc-references.sh could not run (exit $sa alone, $sc on the composite)"
  else
    while IFS= read -r f; do
      [[ -n "$f" ]] && finding "check 21 — $label syntek-author's doc-references.sh reports on the composite only: ${f#· }"
    done < <(LC_ALL=C comm -13 "$W/dr-author.txt" "$W/dr-composite.txt")
  fi
}

# ── --refresh-names ──────────────────────────────────────────────────────────

refresh_names() { # $1 = syntek-author repo
  local commit drift tmp
  commit="$(git -C "$1" rev-parse --short HEAD 2>/dev/null || echo 'no commit')"
  drift=""; [[ -f "$SM_AUTHOR_NAMES_FILE" ]] && drift="$(names_drift "$1")"
  tmp="$(mktemp)"
  {
    printf '# syntek-author-names.txt — the names syntek-media never takes (DESIGN.md D27).\n'
    printf '#\n'
    printf '# Baseline: syntek-author %s plus working tree, read %s.\n' "$commit" "$(date +%d/%m/%Y)"
    printf '# Written only by: bash .github/scripts/coexist-test.sh --refresh-names --author DIR\n'
    printf '# Never edit by hand. shipped-brands.sh check 11 and skill-conformance.sh check 20 read it\n'
    printf '# on every run; coexist-test.sh check 20 fails when syntek-author moves past it.\n'
    printf '#\n'
    printf '# top <entry>     an entry of syntek-author'"'"'s template/, plus build\n'
    printf '# claude <entry>  an entry of its template/.claude/\n'
    printf '# skill <name>    a skill folder\n'
    printf '# rules <file>    a file of its rules folder\n'
    author_names "$1"
  } > "$tmp"
  mv "$tmp" "$SM_AUTHOR_NAMES_FILE"
  bold "▸ $SCRIPT_NAME --refresh-names"
  log "  wrote $(names_file_lines | grep -c .) name(s) ($(names_file_lines | grep -c '^skill ') skill(s)) from syntek-author $commit plus working tree"
  if [[ -n "$drift" ]]; then
    log "  moved since the last baseline (+ new, - gone) — re-check every new name against media's paths:"
    printf '%s\n' "$drift" | sed 's/^/    /'
  else
    log "  nothing moved since the last baseline"
  fi
  log "  record the baseline (commit and date) in CHANGELOG.md."
}

# ── Self-test ────────────────────────────────────────────────────────────────

self_test() {
  local tmp real_names="$SM_AUTHOR_NAMES_FILE"
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  copier_init
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  sm_author_fixture_template "$tmp/author" >/dev/null
  # The fixture syntek-author's own audit: a stub that reports every .md file carrying a dead
  # end, in syntek-author's finding shape.
  mkdir -p "$tmp/author/.github/scripts"
  cat > "$tmp/author/.github/scripts/doc-references.sh" <<'STUB'
#!/usr/bin/env bash
tree="${!#}"; st=0
while IFS= read -r f; do printf '  · check 1 — %s cites a dead end\n' "${f#"$tree"/}"; st=1; done \
  < <(grep -rlF --include='*.md' 'DEAD-END' "$tree" 2>/dev/null | sort)
exit "$st"
STUB
  sm_commit_all "$tmp/author" 'fixture: its doc-references audit'
  sm_fixture_template "$tmp/media" >/dev/null
  SM_AUTHOR_NAMES_FILE="$tmp/names.txt"
  { printf '# fixture names\n'; author_names "$tmp/author"; } > "$SM_AUTHOR_NAMES_FILE"
  AUTHOR_SRC="$tmp/author"; MEDIA_SRC="$tmp/media"; GLOBAL=true
  global_state "$AUTHOR_SRC" "$MEDIA_SRC"
  mkdir -p "$tmp/w"
  run_flow author-fiction "$tmp/w"
  st_baseline "the fixture media sharing a project with the fixture syntek-author"

  local h="$tmp/held"
  B_COPY=1;   probe "check 1 fires when media collides" "check 1 — [author-fiction] media could not apply"; B_COPY=0
  mv "$PROJ/$SM_ANSWERS_FILE" "$h"; probe "check 2 fires when an answers file is missing" "check 2"; mv "$h" "$PROJ/$SM_ANSWERS_FILE"
  A_UPDATE=1; probe "check 3 fires when syntek-author's update fails" "check 3"; A_UPDATE=0
  cp "$PROJ/$B_RULE" "$h"; grep -vF "$B_MARK" "$h" > "$PROJ/$B_RULE"
  probe "check 4 fires when media's change does not arrive" "check 4"; cp "$h" "$PROJ/$B_RULE"
  mv "$PROJ/$B_RULE" "$h"; probe "check 5 fires when one template's file vanishes" "check 5"; mv "$h" "$PROJ/$B_RULE"
  A_OWNED+=("README.md"); probe "check 6 fires on a shared file syntek-author owns" "check 6 — [author-fiction] README.md"; unset 'A_OWNED[-1]'
  printf 'x\n' > "$PROJ/CONTEXT.md.rej"; probe "check 7 fires on a rejected hunk" "check 7"; rm -f "$PROJ/CONTEXT.md.rej"
  cp "$W/post-media.sha" "$h"; sed -i -E '0,/^README\.md\t/s/^(README\.md\t).*/\1changed/' "$W/post-media.sha"
  probe "check 8 fires when media's copy changes a byte that was there" "check 8 — [author-fiction] media's copy changed syntek-author's README.md"; cp "$h" "$W/post-media.sha"
  printf 'brand/src/design-system/tokens.css\n' >> "$W/a-changed.txt"
  probe "check 9 fires when syntek-author's update touches a media path" "check 9"; sed -i '$d' "$W/a-changed.txt"
  printf '.claude/MEMORY.md\n' >> "$W/b-changed.txt"
  probe "check 10 fires when media's update touches a shared file" "check 10 — [author-fiction] media's update touched .claude/MEMORY.md"; sed -i '$d' "$W/b-changed.txt"
  printf 'README.md\n' > "$W/a-again.txt"; probe "check 11 fires when a second syntek-author update changes a file" "check 11"; : > "$W/a-again.txt"
  cp "$W/shared-after.sha" "$h"; sed -i -E 's/^(\.mcp\.json\t).*/\1changed/' "$W/shared-after.sha"
  probe "check 12 fires when a shared file is no longer syntek-author's" "check 12 — [author-fiction] the shared file .mcp.json"; cp "$h" "$W/shared-after.sha"
  A_TOP_NAMES+=("toolkit"); probe "check 13 fires on a top-level name syntek-author also takes" "check 13 — media's top-level path toolkit"; unset 'A_TOP_NAMES[-1]'
  A_SKILL_NAMES+=("write-script"); probe "check 13 fires on a skill name syntek-author also takes" "check 13 — media's skill write-script"; unset 'A_SKILL_NAMES[-1]'
  mv "$PROJ/.claude/rules/syntek-author" "$tmp/held-rules"; probe "check 14 fires when a rules folder is missing" "check 14 — [author-fiction] .claude/rules/syntek-author/"; mv "$tmp/held-rules" "$PROJ/.claude/rules/syntek-author"
  REV_A=1; probe "check 15 fires when syntek-author cannot follow media" "check 15"; REV_A=0
  printf 'publishing/src/publish-log.md\n' > "$W/b-again.txt"; probe "check 16 fires when a second media update changes a file" "check 16"; : > "$W/b-again.txt"
  S17_BACK=true; probe "check 17 fires when a deleted shared file comes back" "check 17 — [author-fiction] media's update recreated"; S17_BACK=false
  printf 'README.md\n' >> "$W/r-changed.txt"
  probe "check 18 fires when taking a platform away touches a shared file" "check 18 — [author-fiction] media's update with PLATFORMS without"; sed -i '$d' "$W/r-changed.txt"
  cp "$W/post-remove.sha" "$h"; sed -i -E 's#^(standards/style/style-sheet\.md\t).*#\1changed#' "$W/post-remove.sha"
  probe "check 18 fires when taking a platform away changes a syntek-author file" "check 18 — [author-fiction] media's update with PLATFORMS without youtube, MEDIA_KINDS without audiobook changed syntek-author's standards/style/style-sheet.md"; cp "$h" "$W/post-remove.sha"
  cp "$W/b-copy.log" "$h"; sed -i 's/filter\.lfs\.required/filter.lfs.(dropped)/g' "$W/b-copy.log"
  probe "check 19 fires when the copy message drops a line" "check 19 — [author-fiction] media's copy output does not carry 'filter.lfs.required'"; cp "$h" "$W/b-copy.log"
  NAMES_DRIFT="+ skill new-skill"; probe "check 20 fires when syntek-author has moved past the frozen names" "check 20"; NAMES_DRIFT=""
  printf '· check 1 — brand/CONTEXT.md cites a dead end\n' >> "$W/dr-composite.txt"
  probe "check 21 fires when syntek-author's audit reports something new on the composite" "check 21 — [author-fiction] syntek-author's doc-references.sh reports on the composite only"
  sed -i '$d' "$W/dr-composite.txt"
  probe_clean "the fixtures share the project cleanly again once every mutation is undone"

  SM_AUTHOR_NAMES_FILE="$real_names"
  st_finish "templates that coexist from templates that collide"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

resolve_author_dir "$AUTHOR_ARG"
if $REFRESH; then
  [[ -n "$SM_AUTHOR_DIR" ]] || die "--refresh-names needs syntek-author: --author DIR, SYNTEK_AUTHOR_DIR or ../syntek-author"
  refresh_names "$SM_AUTHOR_DIR"
  exit 0
fi
if [[ -z "$SM_AUTHOR_DIR" ]]; then
  bold "▸ $SCRIPT_NAME"
  skip_named "coexist-test.sh, every check" "no syntek-author working tree (--author DIR, SYNTEK_AUTHOR_DIR or ../syntek-author) — coexistence untested is not coexistence proven"
  exit 0
fi
[[ -f "$SM_ROOT/copier.yml" ]] || die "no copier.yml at $SM_ROOT"
for k in $KINDS; do [[ " $SM_KINDS " == *" $k "* ]] || die "unknown BRAND_KIND: $k"; done
copier_init
command -v python3 >/dev/null 2>&1 || die "python3 is not installed"

AUTHOR_SRC="$SM_AUTHOR_DIR"; MEDIA_SRC="$SM_ROOT"
bold "▸ $SCRIPT_NAME (syntek-author: $SM_AUTHOR_DIR, $(git -C "$SM_AUTHOR_DIR" rev-parse --short HEAD 2>/dev/null || echo '?') plus working tree)"
global_state "$AUTHOR_SRC" "$MEDIA_SRC"
STATUS=0; GLOBAL=true
for kind in $KINDS; do
  work="$(sm_mktemp)"
  run_flow "$kind" "$work"
  run_checks
  GLOBAL=false
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $kind (over $(author_doc_for_kind "$kind")) — both applied, both updated twice, $(grep -c . "$work/b-added.txt") media path(s) and ${#A_OWNED[@]} syntek-author-owned path(s) disjoint; $R_WHAT; the other order applies"
    rm -rf "$work"
  else
    bold "✗ $kind — ${#FINDINGS[@]} finding(s) (work kept in $work; Copier's output in $work/flow.log):"
    print_findings
    if [[ "${GITHUB_ACTIONS:-}" == true ]]; then
      echo "::group::Copier output for $kind (last 80 lines of flow.log)"
      tail -n 80 "$work/flow.log" 2>/dev/null || true
      echo "::endgroup::"
    fi
    STATUS=1
  fi
done
log ""
[[ "$STATUS" -eq 0 ]] && { bold "✓ syntek-media and syntek-author share every project cleanly, in either order."; exit 0; }
log "  DESIGN.md Section 9: own answers file, own rules folder, own skills, the ten shared files"
log "  seeded in both and update-gated in media; Section 10 lists what goes wrong when one slips."
exit 1

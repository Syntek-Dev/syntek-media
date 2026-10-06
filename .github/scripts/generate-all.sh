#!/usr/bin/env bash
#
# generate-all.sh — Render every brand kind and profile of the template, for the audits to read.
#
#                   A template defect is invisible until somebody generates, and whoever
#                   generates is not whoever broke it (SB rules 42–43). syntek-media renders
#                   three brand kinds from one tree, each with nine platforms and six media kinds
#                   to choose from, so a mistake in one gate shows only in the render that opens
#                   it — and the render nobody makes is the one that rots. So every audit that
#                   reads a render reads ALL of them, and the intended path — media applied over
#                   a real syntek-author project (DESIGN.md D4) — is rendered as well.
#
#                   Renders, named <kind>--<profile> (DESIGN.md D28; the kinds carry a hyphen):
#                     defaults     only the answers that have no default
#                     all          every platform and every media kind
#                     minimal      one platform, one media kind, SEED_EXAMPLES=false
#                                  (business [blog]/[long-video], author-fiction
#                                  [tiktok]/[trailer], author-nonfiction [podcast]/[audiobook]).
#                                  business ships blog WITHOUT website (DESIGN.md Section 7,
#                                  D53), so doc-references.sh check 1 catches a file of that
#                                  render backticking a path only website opens.
#                     over-author  syntek-author's matching variant (business → business,
#                                  author-fiction → fiction, author-nonfiction → theology)
#                                  rendered and committed, then media copied in WITHOUT
#                                  --overwrite, with media's defaults
#
#                   It renders from SNAPSHOTS: the working tree is copied with rsync (without
#                   .git), committed in a temporary repository, and rendered with
#                   `--vcs-ref=HEAD`. Copier reads a template over git, so rendering the real
#                   repository would render its last commit and silently ignore the work in
#                   front of you (SB rule 17). .gitignore is honoured, exactly as a commit would.
#                   syntek-author is snapshotted the same way, from whatever tree --author names
#                   (default ../syntek-author, or $SYNTEK_AUTHOR_DIR). Without one, each
#                   over-author render is a named SKIP — never a pass (DESIGN.md D27). With one,
#                   its names are compared with .github/scripts/syntek-author-names.txt first.
#
#                   Output: one directory per render, OUTDIR/<kind>--<profile>/, beside
#                     OUTDIR/<name>.log     Copier's output (and, over-author, syntek-author's)
#                     OUTDIR/<name>.expect  the answers DESIGN.md says that render should
#                                           record (shipped-brands.sh compares them)
#                     OUTDIR/<name>.owned   over-author only: the files media's copy added, one
#                                           per line — every per-tree audit's scope there
#                   and one tree path per successful render on stdout. Progress goes to stderr.
#
#                   Four checks:
#                     1. Every requested render succeeds. Over-author: syntek-author renders,
#                        media then applies over it without --overwrite, and the --author tree's
#                        names equal syntek-author-names.txt (DESIGN.md D27: a partner that has
#                        moved fails until the list is refreshed and re-checked).
#                     2. Every render carries .copier-answers.syntek-media.yml — without it a
#                        project can never be updated, and no audit can tell what it holds.
#                        Over-author: syntek-author's answers file too.
#                     3. Every examples/*.answers.yml answers exactly the questions copier.yml
#                        asks for its kind, with valid choices — values, never labels — and
#                        names its own kind (BRAND_KIND equals the file's name).
#                     4. The copy output (stderr, without --quiet) of each <kind>--defaults
#                        render carries every _message_after_copy line of _common.sh's lists
#                        (DESIGN.md D13, D73): the seventeen shared paths and the skip rule, the four allows,
#                        nine asks and two Edit denies, the ELEVENLABS_MCP_BASE_PATH line,
#                        filter.lfs.required, the setup check, and the update command with -a;
#                        and, from Section 8, that 'conflict' then 'skip' is expected, the
#                        optional line in .claude/CLAUDE.md, and nothing to add to .gitignore
#                        or .mcp.json.
#
#                   Numbers are stable identifiers. Append, never renumber.
#
#                   What it CANNOT check: anything about what the renders CONTAIN. That is the
#                   job of every per-tree audit (run-all.sh runs them over this output).
#
# SELF-TEST. --self-test builds a fixture template and a fixture syntek-author at runtime, with
#            an uncommitted file in the template, renders them, asserts the uncommitted file
#            reached the render (the snapshot works) and the over-author scope names media's
#            files only, then breaks the fixtures once per check and asserts exactly one finding
#            each — and that a missing syntek-author is a named SKIP, not a finding.
#
# Requirements: bash 4.3+, git, rsync, uvx (or COPIER_CMD). Network on the first uvx run only.
#
# Usage: generate-all.sh [OUTDIR] [--root DIR] [--author DIR] [--only NAME[,NAME…]] [--jobs N]
#                        [--list] [--quiet] [--self-test] [--help]
#        OUTDIR defaults to ${TMPDIR:-/tmp}/syntek-media-render.
#
# Exit codes:  0 = every render succeeded (a named SKIP included)
#              1 = a render failed or is incomplete, or the self-test no longer separates
#              2 = script error (bad arguments, missing tools, no copier.yml)

set -euo pipefail
SCRIPT_NAME="generate-all.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

OUT="${TMPDIR:-/tmp}/syntek-media-render"
ONLY=""
JOBS="${SM_RENDER_JOBS:-4}"   # SM_RENDER_JOBS=1 renders one at a time (a loaded machine; run-all.sh passes it through)
LIST=false
SELF_TEST=false
AUTHOR_ARG=""

usage() {
  cat <<'EOF'
generate-all.sh — Render every brand kind and profile of the template

Usage: generate-all.sh [OUTDIR] [--root DIR] [--author DIR] [--only NAME[,NAME…]] [--jobs N]
                       [--list] [--quiet] [--self-test] [--help]

  OUTDIR        Where the renders go (default: ${TMPDIR:-/tmp}/syntek-media-render)
  --root DIR    The template repository (default: this repository)
  --author DIR  The syntek-author repository for the over-author renders
                (default: $SYNTEK_AUTHOR_DIR, else ../syntek-author; none = a named SKIP)
  --only LIST   Render only these, e.g. business--defaults,author-fiction--over-author
  --jobs N      Renders to run at once (default 4, or $SM_RENDER_JOBS)
  --list        Print the render names and exit
  --quiet       Print findings only (SKIP lines are always printed)
  --self-test   Prove the checks still fire against fixture templates
  --help        Show this message

Prints one rendered tree path per line on stdout.
Exit codes: 0 = every render succeeded  1 = a render failed  2 = script error
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)      [[ $# -gt 1 ]] || die "--root needs a value"; SM_ROOT="$(cd "$2" && pwd)" || die "no such directory: $2"; shift 2 ;;
    --author)    [[ $# -gt 1 ]] || die "--author needs a value"; AUTHOR_ARG="$2"; shift 2 ;;
    --only)      [[ $# -gt 1 ]] || die "--only needs a value"; ONLY="$2"; shift 2 ;;
    --jobs)      [[ $# -gt 1 && "$2" =~ ^[1-9][0-9]*$ ]] || die "--jobs needs a positive number"; JOBS="$2"; shift 2 ;;
    --list)      LIST=true; shift ;;
    --quiet|-q)  QUIET=true; shift ;;
    --self-test) SELF_TEST=true; shift ;;
    --help|-h)   usage; exit 0 ;;
    -*)          die "unknown argument: $1" ;;
    *)           OUT="$1"; shift ;;
  esac
done

# ── The render matrix ────────────────────────────────────────────────────────
#
# name · extra --data answers. A list answer is a YAML flow list of values with no spaces
# (fields split on whitespace), which Copier parses as a list (audits map Section 8).
ALL_PLATFORMS="[${SM_PLATFORMS// /,}]"
ALL_KINDS="[${SM_MEDIA_KINDS// /,}]"
RENDERS=$(cat <<EOF
business--defaults
business--all                   PLATFORMS=$ALL_PLATFORMS MEDIA_KINDS=$ALL_KINDS
business--minimal               PLATFORMS=[blog] MEDIA_KINDS=[long-video] SEED_EXAMPLES=false
author-fiction--defaults
author-fiction--all             PLATFORMS=$ALL_PLATFORMS MEDIA_KINDS=$ALL_KINDS
author-fiction--minimal         PLATFORMS=[tiktok] MEDIA_KINDS=[trailer] SEED_EXAMPLES=false
author-nonfiction--defaults
author-nonfiction--all          PLATFORMS=$ALL_PLATFORMS MEDIA_KINDS=$ALL_KINDS
author-nonfiction--minimal      PLATFORMS=[podcast] MEDIA_KINDS=[audiobook] SEED_EXAMPLES=false
business--over-author
author-fiction--over-author
author-nonfiction--over-author
EOF
)

render_names() { awk '{ print $1 }' <<< "$RENDERS"; }
render_data()  { awk -v n="$1" '$1 == n { for (i = 2; i <= NF; i++) print $i }' <<< "$RENDERS"; }
is_over_author() { [[ "$(profile_of "$1")" == over-author ]]; }

sorted_csv() { tr ' ,' '\n\n' <<< "$1" | grep -v '^$' | LC_ALL=C sort | paste -sd, -; }

# What DESIGN.md Section 2 says the render should record: the kind's defaults, then the
# profile's answers on top. Lists are expected as their values sorted and joined by commas,
# as shipped-brands.sh reads them (the order Copier keeps is not a promise).
expect_for() { # $1 = name → KEY=value lines
  local name="$1" kind kv k v
  kind="$(kind_of "$1")"
  local -A e=([BRAND_KIND]="$kind" [PLATFORMS]="$(sorted_csv "${SM_DEFAULT_PLATFORMS[$kind]}")"
              [MEDIA_KINDS]="$(sorted_csv "${SM_DEFAULT_MEDIA_KINDS[$kind]}")" [SEED_EXAMPLES]=true
              [MODEL_MECHANICAL]="${SM_DEFAULT_MODEL[$kind]}")
  while IFS= read -r kv; do
    [[ -z "$kv" ]] && continue
    k="${kv%%=*}"; v="${kv#*=}"
    if [[ "$v" == '['*']' ]]; then v="${v#[}"; v="$(sorted_csv "${v%]}")"; fi
    e["$k"]="$v"
  done < <(render_data "$name")
  for k in BRAND_KIND PLATFORMS MEDIA_KINDS SEED_EXAMPLES MODEL_MECHANICAL; do
    [[ -n "${e[$k]:-}" ]] && printf '%s=%s\n' "$k" "${e[$k]}"
  done
  return 0
}

SELECTED=()
select_renders() {
  local n
  SELECTED=()
  if [[ -z "$ONLY" ]]; then
    mapfile -t SELECTED < <(render_names)
    return 0
  fi
  for n in ${ONLY//,/ }; do
    render_names | grep -qxF -- "$n" || die "no such render: $n (see --list)"
    SELECTED+=("$n")
  done
}

# ── Rendering ────────────────────────────────────────────────────────────────

SNAP=""
ASNAP=""
NAMES_PROBLEM=""
render_one() { # $1 = name — writes OUT/name, OUT/name.log, .status, .expect (and .owned)
  local name="$1" kind args=() kv status=0
  kind="$(kind_of "$name")"
  while IFS= read -r kv; do [[ -n "$kv" ]] && args+=(--data "$kv"); done < <(render_data "$name")
  rm -rf "${OUT:?}/$name" "$OUT/$name.log" "$OUT/$name.status" "$OUT/$name.expect" "$OUT/$name.owned"
  expect_for "$name" > "$OUT/$name.expect"
  if is_over_author "$name"; then
    if [[ -z "$ASNAP" ]]; then printf 'skip\n' > "$OUT/$name.status"; return 0; fi
    sm_render_over_author "$ASNAP" "$SNAP" "$OUT/$name" "$kind" "${args[@]}" > "$OUT/$name.log" 2>&1 || status=$?
  else
    sm_render "$SNAP" "$OUT/$name" "$kind" "${args[@]}" > "$OUT/$name.log" 2>&1 || status=$?
  fi
  printf '%s\n' "$status" > "$OUT/$name.status"
}

generate() {
  local name running=0 work any_oa=false drift
  mkdir -p "$OUT"
  OUT="$(cd "$OUT" && pwd)"
  work="$(sm_mktemp)"
  SNAP="$work/snapshot"; ASNAP=""; NAMES_PROBLEM=""
  $QUIET || note "  snapshotting $SM_ROOT (working tree, .gitignore honoured)…"
  sm_snapshot "$SM_ROOT" "$SNAP" >/dev/null || { rm -rf "$work"; die "could not snapshot $SM_ROOT"; }
  for name in "${SELECTED[@]}"; do is_over_author "$name" && any_oa=true; done
  if $any_oa; then
    resolve_author_dir "$AUTHOR_ARG"
    if [[ -z "$SM_AUTHOR_DIR" ]]; then
      for name in "${SELECTED[@]}"; do
        is_over_author "$name" && skip_named "$SCRIPT_NAME $name" "no syntek-author tree (pass --author DIR or set SYNTEK_AUTHOR_DIR); a SKIP is never a pass, and no release is tagged on one"
      done
    else
      $QUIET || note "  snapshotting syntek-author at $SM_AUTHOR_DIR ($SM_AUTHOR_SOURCE)…"
      ASNAP="$work/author"
      sm_snapshot "$SM_AUTHOR_DIR" "$ASNAP" >/dev/null || { rm -rf "$work"; die "could not snapshot $SM_AUTHOR_DIR"; }
      if [[ ! -f "$SM_AUTHOR_NAMES_FILE" ]]; then
        NAMES_PROBLEM="$SM_AUTHOR_NAMES_FILE is missing, so the --author tree cannot be held to the frozen names (write it with coexist-test.sh --refresh-names)"
      else
        drift="$(names_drift "$SM_AUTHOR_DIR" | grep -c . || true)"
        [[ "$drift" -eq 0 ]] || NAMES_PROBLEM="the --author tree's names differ from syntek-author-names.txt in $drift line(s) — run coexist-test.sh --refresh-names, re-check every new name against media's paths, and record the new baseline in CHANGELOG.md"
      fi
    fi
  fi
  for name in "${SELECTED[@]}"; do
    $QUIET || note "  rendering $name…"
    render_one "$name" &
    running=$((running + 1))
    if [[ "$running" -ge "$JOBS" ]]; then wait -n || true; running=$((running - 1)); fi
  done
  wait || true
  rm -rf "$work"
}

# ── 3. The example answers files against copier.yml ──────────────────────────

check_examples() {
  local copier="$SM_ROOT/copier.yml" f base kind key v item
  local -a questions=() choices=()
  local -A asked=() given=()
  [[ -d "$SM_ROOT/examples" && -f "$copier" ]] || return 0
  mapfile -t questions < <(registered_keys "$copier")
  for key in "${questions[@]}"; do asked["$key"]=1; done
  for f in "$SM_ROOT"/examples/*.answers.yml; do
    [[ -f "$f" ]] || continue
    base="examples/${f##*/}"; kind="${f##*/}"; kind="${kind%.answers.yml}"
    given=()
    while IFS= read -r key; do [[ -n "$key" ]] && given["$key"]=1; done \
      < <(grep -oE '^[A-Za-z_][A-Za-z0-9_]*:' "$f" | tr -d ':')
    for key in "${questions[@]}"; do
      [[ -n "${given[$key]:-}" ]] || finding "check 3 — $base does not answer $key, a question copier.yml asks every $kind project"
    done
    for key in "${!given[@]}"; do
      [[ -n "${asked[$key]:-}" ]] || finding "check 3 — $base answers $key, which copier.yml does not ask"
    done
    v="$(answer_value BRAND_KIND "$f")"
    [[ "$v" == "$kind" ]] || finding "check 3 — $base records BRAND_KIND=${v:-nothing}; the file is the $kind example"
    for key in "${questions[@]}"; do
      [[ -n "${given[$key]:-}" ]] || continue
      mapfile -t choices < <(question_choices "$key" "$copier")
      [[ ${#choices[@]} -gt 0 ]] || continue
      if grep -qE "^$key:[[:space:]]*($|\\[)" "$f"; then
        while IFS= read -r item; do
          [[ " ${choices[*]} " == *" $item "* ]] || finding "check 3 — $base lists '$item' under $key, which is not one of its values (${choices[*]})"
        done < <(answer_list "$key" "$f")
      else
        v="$(answer_value "$key" "$f")"
        [[ " ${choices[*]} " == *" $v "* ]] || finding "check 3 — $base answers $key='$v', which is not one of its values (${choices[*]})"
      fi
    done
  done
}

run_checks() {
  FINDINGS=()
  local name status err missing
  for name in "${SELECTED[@]}"; do
    status="$(cat "$OUT/$name.status" 2>/dev/null || echo 'did not run')"
    [[ "$status" == skip ]] && continue
    if [[ "$status" != 0 ]]; then
      err="$(grep -v '^[[:space:]]*$' "$OUT/$name.log" 2>/dev/null | tail -1 || true)"
      finding "check 1 — $name did not render (exit $status): ${err:-no output} — see $OUT/$name.log"
      continue
    fi
    [[ -f "$OUT/$name/$SM_ANSWERS_FILE" ]] \
      || finding "check 2 — $name has no $SM_ANSWERS_FILE — it can never be updated"
    if is_over_author "$name" && [[ ! -f "$OUT/$name/$SM_AUTHOR_ANSWERS" ]]; then
      finding "check 2 — $name has no $SM_AUTHOR_ANSWERS — syntek-author's half can never be updated"
    fi
    if [[ "$(profile_of "$name")" == defaults ]]; then
      while IFS= read -r missing; do
        [[ -n "$missing" ]] && finding "check 4 — the copy output of $name does not carry '$missing' (_message_after_copy, DESIGN.md D13)"
      done < <(message_missing_lines "$OUT/$name.log")
    fi
  done
  if [[ -n "$NAMES_PROBLEM" ]]; then
    finding "check 1 — the over-author renders: $NAMES_PROBLEM"
  fi
  check_examples
}

# ── Self-test ────────────────────────────────────────────────────────────────

write_examples() { # $1 = repository — three valid answers files for the fixture's questions
  local r="$1" k
  mkdir -p "$r/examples"
  for k in $SM_KINDS; do
    {
      printf 'BRAND_NAME: Harbour Lane Studio\nBRAND_DESCRIPTION: An invented brand that exists only to prove the audit suite.\n'
      printf 'BRAND_KIND: %s\nOWNER_NAME: Morgan Example\nDATE: 01/01/2027\n' "$k"
      printf 'PLATFORMS:\n'; printf -- '- %s\n' ${SM_DEFAULT_PLATFORMS[$k]}
      printf 'MEDIA_KINDS:\n'; printf -- '- %s\n' ${SM_DEFAULT_MEDIA_KINDS[$k]}
      printf 'SEED_EXAMPLES: false\n'
    } > "$r/examples/$k.answers.yml"
  done
}

self_test() {
  local tmp real_root="$SM_ROOT" real_out="$OUT" real_only="$ONLY" real_names="$SM_AUTHOR_NAMES_FILE" f held
  local real_author="$AUTHOR_ARG" real_env="${SYNTEK_AUTHOR_DIR:-}"
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  copier_init
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  unset SYNTEK_AUTHOR_DIR
  sm_fixture_template "$tmp/tpl" >/dev/null
  sm_author_fixture_template "$tmp/author" >/dev/null
  SM_ROOT="$tmp/tpl"; OUT="$tmp/out"; AUTHOR_ARG="$tmp/author"
  SM_AUTHOR_NAMES_FILE="$tmp/names.txt"
  { printf '# fixture names\n'; author_names "$tmp/author"; } > "$SM_AUTHOR_NAMES_FILE"
  write_examples "$SM_ROOT"
  printf '# Uncommitted\n' > "$SM_ROOT/template/UNCOMMITTED.md"

  ONLY="business--defaults,author-fiction--defaults,business--over-author"; select_renders; generate 2>/dev/null
  st_baseline "the fixture template rendered twice, and once over the fixture syntek-author"
  [[ -f "$OUT/business--defaults/UNCOMMITTED.md" ]] || {
    printf '\033[31m  ✗ an uncommitted file did not reach the render — the snapshot is not the working tree\033[0m\n' >&2; exit 2; }
  log "  ✓ an uncommitted file reached the render — the snapshot is the working tree"
  if ! grep -qx "$SM_ANSWERS_FILE" "$OUT/business--over-author.owned" \
     || grep -qxE 'README\.md|\.claude/settings\.json|Makefile' "$OUT/business--over-author.owned"; then
    printf '\033[31m  ✗ the over-author scope is wrong — .owned must name media'"'"'s files and no shared or syntek-author file\033[0m\n' >&2; exit 2
  fi
  log "  ✓ the over-author scope names media's files, and neither a shared file nor syntek-author's"

  printf '<: if BRAND_KIND == :>broken\n' > "$SM_ROOT/template/brand/src/platforms/linkedin.md"
  ONLY="business--defaults,author-fiction--defaults"; select_renders; generate 2>/dev/null
  probe "check 1 fires when one brand kind fails to render" "check 1 — business--defaults"
  git -C "$SM_ROOT" checkout -q -- template/brand/src/platforms/linkedin.md

  mv "$SM_ROOT/template/$SM_ANSWERS_FILE" "$tmp/held"
  ONLY="business--defaults"; select_renders; generate 2>/dev/null
  probe "check 2 fires when the answers file is not rendered" "check 2 — business--defaults"
  mv "$tmp/held" "$SM_ROOT/template/$SM_ANSWERS_FILE"

  mv "$tmp/author/template/$SM_AUTHOR_ANSWERS" "$tmp/held"
  cp "$SM_AUTHOR_NAMES_FILE" "$tmp/names.held"
  { printf '# fixture names\n'; author_names "$tmp/author"; } > "$SM_AUTHOR_NAMES_FILE"
  ONLY="business--over-author"; select_renders; generate 2>/dev/null
  probe "check 2 fires when an over-author render lacks syntek-author's answers file" "check 2 — business--over-author has no $SM_AUTHOR_ANSWERS"
  mv "$tmp/held" "$tmp/author/template/$SM_AUTHOR_ANSWERS"
  mv "$tmp/names.held" "$SM_AUTHOR_NAMES_FILE"

  printf 'skill a-name-syntek-author-dropped\n' >> "$SM_AUTHOR_NAMES_FILE"
  ONLY="business--over-author"; select_renders; generate 2>/dev/null
  probe "check 1 fires when the --author tree's names drift from the frozen list" "check 1 — the over-author renders"
  sed -i '$d' "$SM_AUTHOR_NAMES_FILE"

  AUTHOR_ARG=""
  ONLY="business--over-author"; select_renders; generate 2>/dev/null
  probe_clean "an over-author render with no syntek-author is a named SKIP, not a finding"
  AUTHOR_ARG="$tmp/author"

  f="$SM_ROOT/examples/author-fiction.answers.yml"; held="$(cat "$f")"
  sed -i 's/^- tiktok$/- "tiktok — vertical video"/' "$f"
  ONLY="author-fiction--defaults"; select_renders; generate 2>/dev/null
  probe "check 3 fires on an example that gives a label for a value" "check 3 — examples/author-fiction.answers.yml lists"
  printf '%s\n' "$held" > "$f"
  sed -i '/^DATE:/d' "$f"
  probe "check 3 fires on an example that leaves a question unanswered" "check 3 — examples/author-fiction.answers.yml does not answer DATE"
  printf '%s\n' "$held" > "$f"

  sed -i '/ELEVENLABS_MCP_BASE_PATH/d' "$SM_ROOT/copier.yml"
  ONLY="business--defaults"; select_renders; generate 2>/dev/null
  probe "check 4 fires when _message_after_copy loses a line" "check 4 — the copy output of business--defaults does not carry 'ELEVENLABS_MCP_BASE_PATH='"
  git -C "$SM_ROOT" checkout -q -- copier.yml

  SM_ROOT="$real_root"; OUT="$real_out"; ONLY="$real_only"; SM_AUTHOR_NAMES_FILE="$real_names"
  AUTHOR_ARG="$real_author"; [[ -n "$real_env" ]] && export SYNTEK_AUTHOR_DIR="$real_env"
  st_finish "a template that renders from one that does not"
}

if $LIST; then render_names; exit 0; fi
if $SELF_TEST; then
  self_test
  exit $?
fi

[[ -f "$SM_ROOT/copier.yml" ]] || die "no copier.yml at $SM_ROOT"
command -v git >/dev/null 2>&1 || die "git is not installed"
copier_init
select_renders

$QUIET || note "▸ $SCRIPT_NAME — ${#SELECTED[@]} render(s) into $OUT"
generate
run_checks

for name in "${SELECTED[@]}"; do
  [[ "$(cat "$OUT/$name.status" 2>/dev/null)" == 0 ]] && printf '%s\n' "$OUT/$name"
done

if [[ ${#FINDINGS[@]} -eq 0 ]]; then
  $QUIET || note "✓ ${#SELECTED[@]} render(s), every one complete or named as skipped."
  exit 0
fi
{
  printf '✗ %d finding(s):\n' "${#FINDINGS[@]}"
  print_findings
} >&2
exit 1

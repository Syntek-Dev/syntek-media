#!/usr/bin/env bash
#
# gen-mode-excludes.sh — Generate, or check, the mode-file block of copier.yml's _exclude.
#
#                        Every moded skill ships exactly ONE of BUSINESS.md, FICTION.md or
#                        NONFICTION.md (DESIGN.md D7). The other two are excluded per brand
#                        kind, one templated _exclude line per file — twenty-one lines that
#                        differ only in a folder name. Kept by hand, that block drifts the first
#                        time a mode file is added or renamed: a missing line ships a second
#                        mode file and the skill reads two domains at once; a stale line
#                        excludes nothing and hides the drift. So the block is GENERATED from
#                        the files on disk, between two markers:
#
#                          # BEGIN generated mode excludes
#                          # END generated mode excludes
#
#                        and CI runs --check, which fails on any difference.
#
#                        Each mode file gets the line that keeps it out of the other kinds,
#                        "<: if <gate> :>/<path><: endif :>", with the gate
#                          BUSINESS.md   → BRAND_KIND != 'business'
#                          FICTION.md    → BRAND_KIND != 'author-fiction'
#                          NONFICTION.md → BRAND_KIND != 'author-nonfiction'
#                        Source: template/.claude/skills/*/{BUSINESS,FICTION,NONFICTION}.md (media
#                        has no moded supporting folder). Order: folders in byte order, modes in
#                        DESIGN.md's order. A mode file inside a gated skill folder
#                        (narrate-audiobook) gets its line too: the folder's gate removes all
#                        three when the media kind is off, and the line keeps two out when on.
#
#                        Six checks (--check):
#                          1. copier.yml carries exactly one BEGIN and one END marker, in order.
#                          2. The markers sit inside the _exclude list.
#                          3. Every mode file on disk has its line in the block.
#                          4. Every line in the block names a mode file on disk.
#                          5. Every line's gate matches its file name.
#                          6. The block is byte-identical to what the generator writes (order and
#                             format) — reported only when 3–5 are clean, so one fault is one
#                             finding.
#
#                        Numbers are stable identifiers. Append, never renumber.
#
#                        What it CANNOT check: that a mode file belongs where it sits (a
#                        BUSINESS.md beside a skill DESIGN.md calls unmoded) — that is
#                        skill-conformance.sh's — or that the gate on a skill folder itself is
#                        right, which shipped-brands.sh proves on renders.
#
# SELF-TEST. --self-test builds a fixture repository at runtime, generates its block, then
#            applies one mutation per check and asserts exactly one finding each.
#
# Requirements: bash 4+, awk, sed, diff. No network.
#
# Usage: gen-mode-excludes.sh [--check | --print] [--root DIR] [--quiet] [--self-test] [--help]
#
# Exit codes:  0 = block written, printed, or in step with the files on disk
#              1 = drift (--check), or the self-test no longer separates
#              2 = script error (bad arguments, no copier.yml, markers absent when writing)

set -euo pipefail
SCRIPT_NAME="gen-mode-excludes.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

MODE="write"
SELF_TEST=false
BEGIN_MARK='# BEGIN generated mode excludes'
END_MARK='# END generated mode excludes'

usage() {
  cat <<'EOF'
gen-mode-excludes.sh — Generate, or check, the mode-file block of copier.yml's _exclude

Usage: gen-mode-excludes.sh [--check | --print] [--root DIR] [--quiet] [--self-test] [--help]

  (no flag)    Rewrite the lines between the two markers in copier.yml
  --check      Fail (exit 1) if the block differs from the files on disk
  --print      Print the generated block to stdout and change nothing
  --root DIR   The template repository (default: this repository)
  --quiet      Print findings only
  --self-test  Prove the checks still fire against a fixture written at runtime
  --help       Show this message

Exit codes: 0 = written, printed, or in step  1 = drift, or the self-test no longer
separates  2 = script error
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)     MODE=check; shift ;;
    --print)     MODE=print; shift ;;
    --root)      [[ $# -gt 1 ]] || die "--root needs a value"; SM_ROOT="$(cd "$2" && pwd)" || die "no such directory: $2"; shift 2 ;;
    --quiet|-q)  QUIET=true; shift ;;
    --self-test) SELF_TEST=true; shift ;;
    --help|-h)   usage; exit 0 ;;
    *)           die "unknown argument: $1" ;;
  esac
done

COPIER="$SM_ROOT/copier.yml"
TPL="$SM_ROOT/template"

# Every mode file, template-relative, in generator order.
mode_files() {
  local area=.claude/skills d m
  [[ -d "$TPL/$area" ]] || return 0
  while IFS= read -r d; do
    for m in $SM_MODE_FILES; do
      [[ -f "$TPL/$area/$d/$m" ]] && printf '%s/%s/%s\n' "$area" "$d" "$m"
    done
  done < <(find "$TPL/$area" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | LC_ALL=C sort)
  return 0
}

marker_indent() { # the indentation of the BEGIN marker, so items line up with it
  local l
  l="$(grep -m1 -F "$BEGIN_MARK" "$COPIER" || true)"
  printf '%s' "${l%%#*}"
}

generate_block() { # $1 = indentation
  local rel q="'"
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    printf '%s- "<: if BRAND_KIND != %s%s%s :>/%s<: endif :>"\n' "$1" "$q" "$(kind_for_mode "${rel##*/}")" "$q" "$rel"
  done < <(mode_files)
}

current_block() { # the raw lines between the markers
  awk -v b="$BEGIN_MARK" -v e="$END_MARK" '
    index($0, e) { on = 0 }
    on { print }
    index($0, b) { on = 1 }' "$COPIER"
}

unquote_item() { # one "- …" line → the bare item
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"; s="${s#- }"
  case "$s" in
    \"*) s="${s#\"}"; s="${s%%\"*}" ;;
    \'*) s="${s#\'}"; s="${s%\'*}"; s="${s//\'\'/\'}" ;;
  esac
  printf '%s' "$s"
}

run_checks() {
  FINDINGS=()
  local nb ne lb le lx lnext item cond path want got kind expected
  local -A on_disk=() in_block=()

  # ── 1. One BEGIN, one END, in order ─────────────────────────────────────────
  nb=$(grep -cF "$BEGIN_MARK" "$COPIER" || true)
  ne=$(grep -cF "$END_MARK" "$COPIER" || true)
  if [[ "$nb" -ne 1 || "$ne" -ne 1 ]]; then
    finding "check 1 — copier.yml carries $nb BEGIN and $ne END marker(s); exactly one of each is required"
    return 0
  fi
  lb=$(grep -nF "$BEGIN_MARK" "$COPIER" | cut -d: -f1)
  le=$(grep -nF "$END_MARK" "$COPIER" | cut -d: -f1)
  if [[ "$lb" -ge "$le" ]]; then
    finding "check 1 — the END marker (line $le) comes before the BEGIN marker (line $lb)"
    return 0
  fi

  # ── 2. Inside _exclude ──────────────────────────────────────────────────────
  lx=$(grep -n '^_exclude:' "$COPIER" | head -1 | cut -d: -f1)
  lnext=$(awk -v s="${lx:-0}" 'NR > s && /^[A-Za-z_][A-Za-z0-9_]*:/ { print NR; exit }' "$COPIER")
  if [[ -z "$lx" || "$lb" -le "$lx" || ( -n "$lnext" && "$le" -ge "$lnext" ) ]]; then
    finding "check 2 — the generated block (lines $lb–$le) is not inside the _exclude list"
  fi

  # ── 3–5. The block against the disk ─────────────────────────────────────────
  while IFS= read -r path; do [[ -n "$path" ]] && on_disk["$path"]=1; done < <(mode_files)
  while IFS= read -r item; do
    [[ "$item" =~ ^[[:space:]]*-[[:space:]] ]] || continue
    IFS=$'\t' read -r cond path < <(split_gated_item "$(unquote_item "$item")") || true
    if [[ -z "${path:-}" ]]; then
      finding "check 4 — an untemplated line in the generated block: $item"
      continue
    fi
    in_block["$path"]=1
    if [[ -z "${on_disk[$path]:-}" ]]; then
      finding "check 4 — the block excludes /$path, which is not a mode file on disk"
      continue
    fi
    kind="$(kind_for_mode "${path##*/}")"
    want="BRAND_KIND == '$kind'"
    got="$(negate_gate "$cond" || echo "$cond")"
    [[ "$(norm_expr "$got")" == "$want" ]] \
      || finding "check 5 — /$path is gated '$cond'; a ${path##*/} must ship exactly when $want"
  done < <(current_block)
  while IFS= read -r path; do
    [[ -z "$path" || -n "${in_block[$path]:-}" ]] || finding "check 3 — /$path is on disk but has no line in the block — it would ship in every brand kind"
  done < <(mode_files)

  # ── 6. Byte-identical to the generator ──────────────────────────────────────
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    expected="$(generate_block "$(marker_indent)")"
    if [[ "$(current_block)" != "$expected" ]]; then
      finding "check 6 — the block holds the right files but not in the generator's order or format; regenerate it"
    fi
  fi
}

write_block() {
  local tmp ind
  ind="$(marker_indent)"
  tmp="$(mktemp)"
  awk -v b="$BEGIN_MARK" -v e="$END_MARK" -v blockfile=<(generate_block "$ind") '
    index($0, b) { print; while ((getline l < blockfile) > 0) print l; skip = 1; next }
    index($0, e) { skip = 0 }
    !skip { print }' "$COPIER" > "$tmp"
  cat "$tmp" > "$COPIER"
  rm -f "$tmp"
}

# ── Self-test ────────────────────────────────────────────────────────────────

self_test() {
  local tmp real_tpl="$TPL" real_copier="$COPIER" good m
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  TPL="$tmp/template"; COPIER="$tmp/copier.yml"
  mkdir -p "$TPL/.claude/skills/write-script" "$TPL/.claude/skills/narrate-audiobook" "$TPL/.claude/skills/captions"
  for m in $SM_MODE_FILES; do : > "$TPL/.claude/skills/write-script/$m"; : > "$TPL/.claude/skills/narrate-audiobook/$m"; done
  : > "$TPL/.claude/skills/captions/SKILL.md"
  cat > "$COPIER" <<EOF
_exclude:
  - .git
  $BEGIN_MARK
  $END_MARK
_skip_if_exists:
  - /README.md
EOF
  write_block
  good="$(cat "$COPIER")"
  st_baseline "a freshly generated block"

  grep -vF "$END_MARK" <<< "$good" > "$COPIER"
  probe "check 1 fires when the END marker is lost" "check 1"

  awk -v b="$BEGIN_MARK" -v e="$END_MARK" '
    index($0, b) { hold = 1 } hold { buf = buf $0 "\n" } index($0, e) { hold = 0; next }
    !hold && !index($0, b) { print } END { printf "%s", buf }' <<< "$good" > "$COPIER"
  probe "check 2 fires when the block drifts out of _exclude" "check 2"

  grep -vF '/narrate-audiobook/FICTION.md' <<< "$good" > "$COPIER"
  probe "check 3 fires when a mode file loses its line" "check 3"

  awk -v e="$END_MARK" -v ghost="  - \"<: if BRAND_KIND != 'business' :>/.claude/skills/ghost/BUSINESS.md<: endif :>\"" \
    'index($0, e) { print ghost } { print }' <<< "$good" > "$COPIER"
  probe "check 4 fires on a line for a file that is not on disk" "check 4"

  sed "s#BRAND_KIND != 'author-nonfiction' :>/.claude/skills/write-script/NONFICTION.md#BRAND_KIND != 'author-fiction' :>/.claude/skills/write-script/NONFICTION.md#" <<< "$good" > "$COPIER"
  probe "check 5 fires on a line whose gate does not match its file" "check 5"

  awk '/write-script\/BUSINESS.md/ { held = $0; next } { print } /write-script\/FICTION.md/ { print held }' <<< "$good" > "$COPIER"
  probe "check 6 fires when the right lines sit in the wrong order" "check 6"

  TPL="$real_tpl"; COPIER="$real_copier"
  st_finish "a block in step with the disk from one that has drifted"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

[[ -f "$COPIER" ]] || die "no copier.yml at $SM_ROOT"
[[ -d "$TPL" ]] || die "no template/ directory at $SM_ROOT"

case "$MODE" in
  print)
    generate_block "$(marker_indent)"
    exit 0 ;;
  write)
    [[ $(grep -cF "$BEGIN_MARK" "$COPIER" || true) -eq 1 && $(grep -cF "$END_MARK" "$COPIER" || true) -eq 1 ]] \
      || die "copier.yml must carry exactly one '$BEGIN_MARK' and one '$END_MARK' line inside _exclude"
    write_block
    log "  wrote $(generate_block "" | grep -c . || true) mode-file exclusion line(s) into copier.yml"
    run_checks
    [[ ${#FINDINGS[@]} -eq 0 ]] || { print_findings; exit 1; }
    exit 0 ;;
  check)
    bold "▸ $SCRIPT_NAME --check"
    run_checks
    if [[ ${#FINDINGS[@]} -eq 0 ]]; then
      bold "✓ The mode-file block names all $(mode_files | grep -c . || true) mode file(s) on disk, each with its own gate."
      exit 0
    fi
    bold "✗ ${#FINDINGS[@]} finding(s):"
    print_findings
    log ""
    log "  Regenerate the block: bash .github/scripts/gen-mode-excludes.sh — never type a line"
    log "  between the markers by hand."
    exit 1 ;;
esac

#!/usr/bin/env bash
#
# run-all.sh — Run every audit and test in DESIGN.md Section 7, rendering the template once.
#
#              Fifteen scripts, three kinds of input: the template source (tokens, mode
#              excludes, pairs, line cap, scrub, isolation, seeds, skills), the renders (shipped
#              brands, byte identity, references, pairs, seeds, skills, line cap, toolkit), and
#              their own scratch projects (update, coexistence). Rendering is the expensive
#              part, so it happens once, and every per-tree audit reads the same twelve renders:
#              nine standalone, three over syntek-author. byte-identity.sh reads the standalone
#              trees only; on an over-author tree every other audit reads <render>.owned and
#              checks media's paths (DESIGN.md Section 7).
#
#              Discipline, from SB: every script's --self-test runs FIRST, because a detector
#              nobody has seen fail is a detector nobody knows works (rule 38); failures
#              ACCUMULATE rather than stopping the run, so one broken gate never hides
#              another (rule 43); and a script that could not run is an error, never a pass
#              (rule 49). A step that could not look for want of syntek-author prints a named
#              SKIP; the summary lists every one as SKIP, apart from PASS, FINDINGS and ERROR,
#              and a step that skipped anything is never recorded as PASS (DESIGN.md D27: no
#              release is tagged on a SKIP).
#
#              Three checks, on the run itself:
#                1. An audit or test reported findings (exit 1).
#                2. An audit or test could not run (exit 2, or any other failure).
#                3. A self-test no longer separates good input from bad.
#
#              Numbers are stable identifiers. Append, never renumber.
#
#              What it CANNOT check: anything the fifteen cannot. It adds no check of its own
#              to the template; it only refuses to let one of theirs go unrun or unread.
#
# SELF-TEST. --self-test points the runner at stub scripts written at runtime, proves an
#            all-green run is green, then breaks one stub per check and asserts exactly one
#            finding naming it — and that a stub which SKIPs is listed as SKIP, not PASS, and
#            is not a finding.
#
# Requirements: those of the scripts it runs (bash, git, rsync, uvx, python3, ffmpeg; uv and
#               Playwright's Chromium optional).
#
# Usage: run-all.sh [--out DIR] [--keep] [--author DIR] [--no-self-test] [--skip-integration]
#                   [--require-ffmpeg] [--skip-thumbnails] [--root DIR] [--quiet] [--self-test]
#                   [--help]
#
# Exit codes:  0 = every audit and test passed (named SKIPs included, listed apart)
#              1 = findings, or the self-test no longer separates
#              2 = something could not run (the run is incomplete — fix that first)

set -euo pipefail
SCRIPT_NAME="run-all.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SCRIPTS="$SM_SCRIPTS_DIR"
OUT=""
KEEP=false
SELF_TESTS=true
INTEGRATION=true
SMOKE_ARGS=()
AUTHOR_ARGS=()
SELF_TEST=false

usage() {
  cat <<'EOF'
run-all.sh — Run every audit and test, rendering the template once

Usage: run-all.sh [--out DIR] [--keep] [--author DIR] [--no-self-test] [--skip-integration]
                  [--require-ffmpeg] [--skip-thumbnails] [--root DIR] [--quiet] [--self-test]
                  [--help]

  --out DIR           Render into DIR (default: a temporary directory)
  --keep              Keep the renders afterwards
  --author DIR        The syntek-author repository, passed to generate-all.sh and
                      coexist-test.sh (default: $SYNTEK_AUTHOR_DIR, else ../syntek-author)
  --no-self-test      Skip each script's --self-test (faster; not for CI)
  --skip-integration  Skip update-test and coexist-test
  --require-ffmpeg    Passed to toolkit-smoke.sh
  --skip-thumbnails   Passed to toolkit-smoke.sh
  --root DIR          The template repository (default: this repository)
  --quiet             Print only failing steps and the summary
  --self-test         Prove the runner reports what it runs, against stub scripts
  --help              Show this message

Exit codes: 0 = all passed  1 = findings  2 = something could not run
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)              [[ $# -gt 1 ]] || die "--out needs a value"; OUT="$2"; shift 2 ;;
    --keep)             KEEP=true; shift ;;
    --author)           [[ $# -gt 1 ]] || die "--author needs a value"; AUTHOR_ARGS=(--author "$2"); shift 2 ;;
    --no-self-test)     SELF_TESTS=false; shift ;;
    --skip-integration) INTEGRATION=false; shift ;;
    --require-ffmpeg)   SMOKE_ARGS+=(--require-ffmpeg); shift ;;
    --skip-thumbnails)  SMOKE_ARGS+=(--skip-thumbnails); shift ;;
    --root)             [[ $# -gt 1 ]] || die "--root needs a value"; SM_ROOT="$(cd "$2" && pwd)" || die "no such directory: $2"; shift 2 ;;
    --quiet|-q)         QUIET=true; shift ;;
    --self-test)        SELF_TEST=true; shift ;;
    --help|-h)          usage; exit 0 ;;
    *)                  die "unknown argument: $1" ;;
  esac
done

STATIC=(check-template-tokens gen-mode-excludes docs-pairing line-cap scrub dev-isolation shipped-seeds skill-conformance)
PER_TREE=(shipped-brands byte-identity doc-references docs-pairing shipped-seeds skill-conformance line-cap toolkit-smoke)
INTEGRATED=(update-test coexist-test)
ALL_SCRIPTS=(check-template-tokens gen-mode-excludes generate-all shipped-brands byte-identity docs-pairing
             doc-references shipped-seeds skill-conformance line-cap update-test coexist-test
             toolkit-smoke scrub dev-isolation)

RESULTS=()   # "name<TAB>status"
ERRORS=0
STEP_SINK=""  # empty: steps print to the terminal; a path: they print there (the self-test)

emit() { if [[ -n "$STEP_SINK" ]]; then printf '%s\n' "$*" >> "$STEP_SINK"; else printf '%s\n' "$*"; fi; }
section() { if [[ -n "$STEP_SINK" ]]; then emit "━━ $1"; else bold "━━ $1"; fi; }

# Every "SKIP — <what> — <why>" line in a step's output becomes its own SKIP row (skip_named in
# _common.sh prints that shape). Prints how many it found.
record_skips() { # $1 = output
  local line what n=0
  while IFS= read -r line; do
    line="${line#"${line%%[![:space:]]*}"}"
    what="${line#SKIP — }"; what="${what%% — *}"
    RESULTS+=("  · $what"$'\t'"SKIP")
    n=$((n + 1))
  done < <(grep -E '^[[:space:]]*SKIP — ' <<< "$1" || true)
  printf '%s' "$n"
}

step() { # $1 = label, then the command — runs it, records it, never stops the run
  local label="$1" s=0 out at skips
  shift
  out="$("$@" 2>&1)" || s=$?
  at=${#RESULTS[@]}
  RESULTS+=("$label"$'\t'"")
  skips="$(record_skips "$out")"
  if [[ "$s" -eq 0 ]]; then
    if [[ "$skips" -gt 0 ]]; then
      emit "$out" ""
      RESULTS[at]="$label"$'\t'"SKIP ($skips named below)"
    else
      $QUIET || emit "$out" ""
      RESULTS[at]="$label"$'\t'"PASS"
    fi
    return 0
  fi
  emit "$out" ""
  case "$s" in
    1) RESULTS[at]="$label"$'\t'"FINDINGS"
       if [[ "$label" == *--self-test* ]]; then finding "check 3 — $label: the self-test no longer separates"
       else finding "check 1 — $label reported findings"; fi ;;
    *) RESULTS[at]="$label"$'\t'"ERROR (exit $s)"; ERRORS=$((ERRORS + 1))
       finding "check 2 — $label could not run (exit $s)" ;;
  esac
}

run_checks() {
  FINDINGS=(); RESULTS=(); ERRORS=0
  local s out trees=() standalone=() t gen=0 at skips err
  if $SELF_TESTS; then
    section "Self-tests"
    for s in "${ALL_SCRIPTS[@]}"; do step "$s --self-test" bash "$SCRIPTS/$s.sh" --self-test; done
  fi

  section "The template source"
  for s in "${STATIC[@]}"; do
    case "$s" in
      gen-mode-excludes) step "$s --check" bash "$SCRIPTS/$s.sh" --check --root "$SM_ROOT" ;;
      dev-isolation|scrub|check-template-tokens) step "$s" bash "$SCRIPTS/$s.sh" --root "$SM_ROOT" ;;
      *) step "$s (template/)" bash "$SCRIPTS/$s.sh" --root "$SM_ROOT" ;;
    esac
  done

  section "Rendering"
  out="$OUT"
  [[ -n "$out" ]] || out="$(sm_mktemp)/renders"
  mkdir -p "$(dirname "$out")"
  # The status is generate-all's own: `mapfile < <(…) || gen=$?` would read mapfile's, and a
  # failed render would pass.
  bash "$SCRIPTS/generate-all.sh" "$out" --root "$SM_ROOT" "${AUTHOR_ARGS[@]}" --quiet >"$out.trees" 2>"$out.gen-err" || gen=$?
  mapfile -t trees < "$out.trees"
  err="$(cat "$out.gen-err" 2>/dev/null || true)"
  at=${#RESULTS[@]}
  RESULTS+=("generate-all"$'\t'"")
  skips="$(record_skips "$err")"
  case "$gen" in
    0) if [[ "$skips" -gt 0 ]]; then emit "$err"; RESULTS[at]="generate-all"$'\t'"SKIP ($skips named below)"
       else RESULTS[at]="generate-all"$'\t'"PASS"; fi ;;
    1) RESULTS[at]="generate-all"$'\t'"FINDINGS"; emit "$err"; finding "check 1 — generate-all: a render failed" ;;
    *) RESULTS[at]="generate-all"$'\t'"ERROR (exit $gen)"; ERRORS=$((ERRORS + 1)); emit "$err"
       finding "check 2 — generate-all could not run (exit $gen)" ;;
  esac
  for t in "${trees[@]}"; do [[ -f "$t.owned" ]] || standalone+=("$t"); done
  $QUIET || emit "  ${#trees[@]} render(s) in $out (${#standalone[@]} standalone)" ""

  if [[ ${#trees[@]} -gt 0 ]]; then
    section "The renders"
    for s in "${PER_TREE[@]}"; do
      case "$s" in
        byte-identity)
          if [[ ${#standalone[@]} -ge 2 ]]; then step "$s (standalone renders)" bash "$SCRIPTS/$s.sh" --root "$SM_ROOT" "${standalone[@]}"; fi ;;
        toolkit-smoke)
          step "$s (renders)" bash "$SCRIPTS/$s.sh" "${SMOKE_ARGS[@]}" "${trees[@]}" ;;
        *)
          step "$s (renders)" bash "$SCRIPTS/$s.sh" --root "$SM_ROOT" "${trees[@]}" ;;
      esac
    done
  fi

  if $INTEGRATION; then
    section "Update and coexistence"
    for s in "${INTEGRATED[@]}"; do
      case "$s" in
        coexist-test) step "$s" bash "$SCRIPTS/$s.sh" --root "$SM_ROOT" "${AUTHOR_ARGS[@]}" ;;
        *)            step "$s" bash "$SCRIPTS/$s.sh" --root "$SM_ROOT" ;;
      esac
    done
  fi

  if [[ -z "$OUT" ]] && ! $KEEP; then rm -rf "$(dirname "$out")"; fi
  rm -f "$out.gen-err" "$out.trees" 2>/dev/null || true
}

summary() {
  local r st pass=0 found=0 error=0 skip=0
  printf '\033[1m━━ Summary\033[0m\n'   # always printed, --quiet or not
  for r in "${RESULTS[@]}"; do
    st="${r#*$'\t'}"
    printf '  %-48s %s\n' "${r%%$'\t'*}" "$st"
    case "$st" in
      PASS) pass=$((pass + 1)) ;;
      FINDINGS) found=$((found + 1)) ;;
      ERROR*) error=$((error + 1)) ;;
      SKIP) skip=$((skip + 1)) ;;
    esac
  done
  printf '  %s PASS · %s FINDINGS · %s ERROR · %s SKIP — a SKIP is never a pass\n' "$pass" "$found" "$error" "$skip"
}

# ── Self-test ────────────────────────────────────────────────────────────────

write_stubs() { # $1 = dir. Each stub obeys STUB_FAIL="<name>:<run|self>:<code>" and STUB_SKIP="<name>:<run|self>".
  local d="$1" s
  mkdir -p "$d"
  for s in "${ALL_SCRIPTS[@]}"; do
    cat > "$d/$s.sh" <<EOF
#!/usr/bin/env bash
mode=run; for a in "\$@"; do [ "\$a" = --self-test ] && mode=self; done
if [ "\${STUB_FAIL:-}" = "$s:\$mode:1" ]; then echo "$s: a finding"; exit 1; fi
if [ "\${STUB_FAIL:-}" = "$s:\$mode:2" ]; then echo "$s: cannot run"; exit 2; fi
if [ "\${STUB_SKIP:-}" = "$s:\$mode" ]; then echo "SKIP — $s probe — no syntek-author tree" >&2; fi
if [ "$s" = generate-all ] && [ "\$mode" = run ]; then
  out="\$1"; mkdir -p "\$out/business--defaults" "\$out/author-fiction--defaults"
  echo "\$out/business--defaults"; echo "\$out/author-fiction--defaults"
fi
exit 0
EOF
  done
}

probe_skip() { # $1 = label, $2 = the step label that must read SKIP
  ST_PROBES=$((ST_PROBES + 1))
  run_checks
  if [[ ${#FINDINGS[@]} -eq 0 ]] && printf '%s\n' "${RESULTS[@]}" | grep -q "^$2"$'\t'"SKIP"; then
    log "  ✓ $1"
  else
    ST_FAILS=$((ST_FAILS + 1))
    printf '\033[31m  ✗ %s: %d finding(s), and %s was not listed as SKIP\033[0m\n' "$1" "${#FINDINGS[@]}" "$2"
  fi
}

self_test() {
  local tmp real_scripts="$SCRIPTS"
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  write_stubs "$tmp/stubs"
  SCRIPTS="$tmp/stubs"; OUT="$tmp/out"; STEP_SINK="$tmp/sink"
  export STUB_FAIL="" STUB_SKIP=""
  st_baseline "a run of stubs that all pass"
  STUB_FAIL="scrub:run:1";         probe "check 1 fires when an audit reports findings" "check 1 — scrub reported findings"
  STUB_FAIL="byte-identity:run:2"; probe "check 2 fires when an audit cannot run" "check 2 — byte-identity (standalone renders) could not run"
  STUB_FAIL="line-cap:self:1";     probe "check 3 fires when a self-test stops separating" "check 3 — line-cap --self-test"
  STUB_FAIL="generate-all:run:1";  probe "check 1 fires when a render fails" "check 1 — generate-all: a render failed"
  STUB_FAIL=""
  STUB_SKIP="coexist-test:run";    probe_skip "a test that SKIPs is listed as SKIP, never PASS, and is not a finding" "coexist-test"
  STUB_SKIP="generate-all:run";    probe_skip "a render that SKIPs is listed as SKIP, never PASS" "generate-all"
  STUB_SKIP=""
  SCRIPTS="$real_scripts"; OUT=""; STEP_SINK=""
  st_finish "a run that reports every failure from one that hides them"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

[[ -f "$SM_ROOT/copier.yml" ]] || die "no copier.yml at $SM_ROOT"
bold "▸ $SCRIPT_NAME — $SM_ROOT"
log ""
run_checks
summary
log ""
if [[ ${#FINDINGS[@]} -eq 0 ]]; then
  printf '\033[1m✓ Every audit and test passed (any SKIP is listed above, and is not a pass).\033[0m\n'
  exit 0
fi
printf '\033[1m✗ %d failing step(s):\033[0m\n' "${#FINDINGS[@]}"
print_findings
[[ "$ERRORS" -gt 0 ]] && exit 2
exit 1

#!/usr/bin/env bash
#
# scrub.sh — Fail on personal data, secrets, source-repository names and absolute paths that ship.
#
#            syntek-media is reused by three real brands, each in its own project, and is
#            built on a machine that holds their names, channels, voices and keys. Everything
#            under template/ is copied into every project anyone generates, and examples/ is
#            published with the template; a seed that carries a real name, a channel handle,
#            a voice ID or an API key cannot be retracted by any update. So DESIGN.md D36 is
#            absolute — no real brand or person names, channel handles or URLs, account IDs,
#            ElevenLabs voice IDs, API keys, Claude Design links, follower or view counts or
#            prices — and it is enforced here, not trusted to review. A hit is fixed at the
#            source.
#
#            Eleven checks, over every text file under template/ and examples/ (and every file
#            NAME) — syntek-author's nine, then media's two:
#              1. The source author's identity: Sam, Samuel, Bailey, SamBailey, sam-dev,
#                 syntekstudio, Syntek Studio.
#              2. Health and learning-difference terms — a generic list of common diagnoses
#                 and conditions.
#              3. Source-repository names: syntek-base. (Media names its sibling syntek-author
#                 by design, DESIGN.md D4; the private repositories' names live in the
#                 deny-list, check 9.)
#              4. Absolute paths: /home/…, /Users/…, /mnt/…, /root/…, C:\Users\….
#              5. An email address outside the reserved example domains.
#              6. A telephone number (+44 …, or a UK mobile 07…).
#              7. A money amount (£ or € followed by a figure, GBP/USD/EUR and a figure).
#              8. A run of seven or more digits — the shape of an account, channel or client
#                 number (ffmpeg's sample rates and bitrates are six digits or fewer).
#              9. A pattern from the deny-list named by SCRUB_DENYLIST (one extended regular
#                 expression per line, # comments allowed), or, when that is unset, from
#                 ${XDG_CONFIG_HOME:-~/.config}/syntek-media/scrub-denylist, falling back to
#                 syntek-author's .../syntek-author/scrub-denylist, if either exists. The real
#                 brands' names, handles and project names live THERE, outside every
#                 repository, because listing them here would publish the very data the list
#                 exists to keep out. CI has no deny-list, so check 9 runs on the maintainer's
#                 machine.
#             10. A secret: an ElevenLabs-shaped key (sk_ and twenty or more characters), or an
#                 api_key / xi-api-key given a literal value. A value that is a shell variable
#                 reference — "$VAR", $VAR or ${VAR} — is the instruction, not the key
#                 (ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY"): the value must start with a
#                 key character, and a dollar sign is not one.
#             11. A real voice ID or Claude Design link: a voice_id given a twenty-character
#                 identifier, or a claude.ai/design/… project link. The design register and
#                 voice.md ship empty; real links and IDs are the author's.
#
#            A line that must keep a match carries `scrub: allow — <reason>` (in a comment).
#
#            Numbers are stable identifiers. Append, never renumber.
#
#            What it CANNOT check: a real person, brand or place named without one of these
#            shapes, a handle written as plain words, or a fabricated quotation. Examples must
#            use invented brands and people (Harbour Lane Studio, Morgan Example, Robin
#            Example), and that is a reviewer's call.
#
# SELF-TEST. --self-test writes a clean fixture at runtime (words that merely contain the
#            patterns, reserved example addresses, a bare currency sign, a key passed as a
#            variable, an empty voice ID), proves it clean, then adds one line per check and
#            asserts exactly one finding each.
#
# Requirements: bash 4+, grep. No network.
#
# Usage: scrub.sh [--root DIR] [--quiet] [--self-test] [--help] [<dir>...]
#        With no directory, scrubs template/ and examples/ in the repository.
#
# Exit codes:  0 = nothing personal found
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, a directory that does not exist, a
#                  SCRUB_DENYLIST that cannot be read or lives inside the repository)

set -euo pipefail
SCRIPT_NAME="scrub.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
TARGETS=()

usage() {
  cat <<'EOF'
scrub.sh — Fail on personal data, secrets, source-repository names and absolute paths

Usage: scrub.sh [--root DIR] [--quiet] [--self-test] [--help] [<dir>...]

  <dir>        What to scrub (default: template/ and examples/ in the repository)
  --root DIR   The template repository (default: this repository)
  --quiet      Print findings only
  --self-test  Prove the checks still fire against a fixture written at runtime
  --help       Show this message

Environment: SCRUB_DENYLIST=/path/outside/the/repo — extra patterns (check 9); default
             ${XDG_CONFIG_HOME:-~/.config}/syntek-media/scrub-denylist, else
             .../syntek-author/scrub-denylist, when present
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

DIR=""
FILES_READ=0
DENYLIST="${SCRUB_DENYLIST:-}"
if [[ -z "$DENYLIST" ]]; then
  for _sm_deny in "${XDG_CONFIG_HOME:-$HOME/.config}/syntek-media/scrub-denylist" \
                  "${XDG_CONFIG_HOME:-$HOME/.config}/syntek-author/scrub-denylist"; do
    if [[ -r "$_sm_deny" ]]; then DENYLIST="$_sm_deny"; break; fi
  done
  unset _sm_deny
fi

# check number · grep flags · pattern
PATTERNS=$(cat <<'EOF'
1	-E	(^|[^A-Za-z])(Sam|Samuel|Bailey)([^A-Za-z]|$)
1	-iE	sambailey|sam-dev|syntekstudio|syntek studio
2	-iE	autism|autistic|(^|[^A-Za-z])adhd([^A-Za-z]|$)|dyspraxi|neurodiverg|dyslexi|dyscalcul|(^|[^A-Za-z])spld([^A-Za-z]|$)
3	-iE	syntek-base
4	-E	/home/[A-Za-z]|/Users/[A-Za-z]|/mnt/[A-Za-z]|/root/|[A-Za-z]:\\(Users|home)\\
5	-E	[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}
6	-E	\+44[ 0-9()-]{9,}|(^|[^0-9])07[0-9]{3} ?[0-9]{3} ?[0-9]{3}([^0-9]|$)
7	-E	(£|€) ?[0-9]|(^|[^A-Za-z])(GBP|USD|EUR) ?[0-9]
8	-E	(^|[^0-9A-Za-z_.:-])[0-9]{7,}([^0-9A-Za-z_]|$)
10	-iE	(^|[^A-Za-z0-9_])sk_[A-Za-z0-9]{20,}|(xi-api-key|api[_-]?key)["']?[[:space:]]*[:=][[:space:]]*["']?[A-Za-z0-9_-]{16,}
11	-iE	voice[_-]?id["']?[[:space:]]*[:=][[:space:]]*["']?[A-Za-z0-9]{20}([^A-Za-z0-9]|$)|claude\.ai/design/[A-Za-z0-9/_-]{8,}
EOF
)

# Matches a reserved or non-personal address — never a person's.
EMAIL_OK='@example\.(com|org|net)|@[A-Za-z0-9.-]*\.example\b|noreply@|no-reply@|git@github\.com|@localhost'

scan() { # $1 = check, $2 = flags, $3 = pattern — over the files of DIR
  local n="$1" flags="$2" pat="$3" hit
  while IFS= read -r hit; do
    [[ -z "$hit" ]] && continue
    [[ "$hit" == *'scrub: allow'* ]] && continue
    if [[ "$n" == 5 ]] && grep -qE "$EMAIL_OK" <<< "$hit"; then continue; fi
    finding "check $n — ${hit:0:140}"
  done < <(cd "$DIR" && list_files0 . | xargs -0 -r grep -nIH "$flags" -- "$pat" 2>/dev/null || true)
}

run_checks() {
  FINDINGS=()
  local n flags pat rel line
  FILES_READ="$(cd "$DIR" && list_files0 . | tr -cd '\0' | wc -c)"
  while IFS=$'\t' read -r n flags pat; do
    [[ -z "$n" ]] && continue
    scan "$n" "$flags" "$pat"
    # Names carry data too: a file called after a brand is as public as its contents.
    if [[ "$n" -le 3 ]]; then
      while IFS= read -r -d '' rel; do
        grep -q "$flags" -- "$pat" <<< "$rel" && finding "check $n — the path $rel"
      done < <(cd "$DIR" && list_files0 .)
    fi
  done <<< "$PATTERNS"
  if [[ -n "$DENYLIST" ]]; then
    while IFS= read -r line; do
      [[ -z "$line" || "$line" == '#'* ]] && continue
      scan 9 -iE "$line"
    done < "$DENYLIST"
  fi
}

self_test() {
  local tmp f
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  DIR="$tmp/template"; mkdir -p "$DIR/production/docs/reference"
  f="$DIR/production/docs/reference/notes.md"
  cat > "$f" <<'EOF'
# Notes — the same samples, by <%OWNER_NAME%>

Write to robin@example.com. Prices are the author's (for example £ as a sign alone).
The script reads $1 and loops 2027 times at 48000 Hz and 192000 bps; the rules live in
.claude/rules/syntek-media/; temporary files go in ${TMPDIR:-/tmp}. John 3:16 is not a number.
Applied over syntek-author, where present. A risk_assessment_document_template is not a key.
Export the key first: --env ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY" and never type it.
| Use | Voice | Voice ID |
voice_id = ""
Design happens in Claude Design (claude.ai/design); the register holds each design's link.
EOF
  local denylist="$tmp/deny"
  printf '# real brand names, kept outside the repository\nharbour-and-reed\n' > "$denylist"
  DENYLIST="$denylist"
  st_baseline "a fixture of near-misses"

  local -a cases=(
    "1|Drafted by Sam on a Tuesday."
    "2|Written for a viewer with dyspraxia."
    "3|Ported from syntek-base."
    "4|See /home/someone/notes.md."
    "5|Email ada.quill@gmail.com for a copy."
    "6|Call 07700 900123 after six."
    "7|The retainer is £1,200 a month."
    "8|Channel number 2051234 on the cover."
    "9|Prepared for Harbour-and-Reed Ltd."
    "10|export ELEVENLABS_API_KEY=sk_4f9c2e7a1b8d3f6e0a5c9b2d7e4f1a8c"
    "10|api_key = \"q8Zr4LmN2pXv7TbWkY3s\""
    "11|voice_id: \"Zq9VxW2rT8yLmK4pN6aB\""
    "11|Synced from https://claude.ai/design/p/0f3a9c7e-invented-project"
  )
  local c n text
  for c in "${cases[@]}"; do
    n="${c%%|*}"; text="${c#*|}"
    cp "$f" "$tmp/held"; printf '%s\n' "$text" >> "$f"
    probe "check $n fires on: $text" "check $n"
    cp "$tmp/held" "$f"
  done
  printf 'Drafted by Sam. <!-- scrub: allow — a fixture proving the marker -->\n' >> "$f"
  probe_clean "the allow marker exempts its line"
  cp "$tmp/held" "$f"
  printf '%s\n' 'export ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY_FROM_THE_VAULT' 'xi-api-key: ${ELEVENLABS_API_KEY_FROM_THE_VAULT}' \
    '"api_key": "$ELEVENLABS_API_KEY_FROM_THE_VAULT"' >> "$f"
  probe_clean "check 10 never reads a shell variable reference — \$VAR, \${VAR}, \"\$VAR\" — as a key"
  cp "$tmp/held" "$f"
  mkdir -p "$DIR/brand/sam-dev-notes"; printf 'x\n' > "$DIR/brand/sam-dev-notes/CONTEXT.md"
  probe "check 1 fires on a file NAME carrying identity" "check 1 — the path"
  rm -rf "$DIR/brand"
  DENYLIST="${SCRUB_DENYLIST:-}"
  st_finish "clean template text from personal data"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

if [[ -n "$DENYLIST" ]]; then
  [[ -r "$DENYLIST" ]] || die "SCRUB_DENYLIST names $DENYLIST, which cannot be read"
  case "$(cd "$(dirname "$DENYLIST")" && pwd)/" in
    "$SM_ROOT"/*) die "SCRUB_DENYLIST must live outside the repository — it lists the data it keeps out" ;;
  esac
fi
if [[ ${#TARGETS[@]} -eq 0 ]]; then
  [[ -d "$SM_ROOT/template" ]] || die "no template/ directory at $SM_ROOT, and no directory given"
  TARGETS=("$SM_ROOT/template")
  [[ -d "$SM_ROOT/examples" ]] && TARGETS+=("$SM_ROOT/examples")
fi

bold "▸ $SCRIPT_NAME"
STATUS=0
for target in "${TARGETS[@]}"; do
  [[ -d "$target" ]] || die "not a directory: $target"
  DIR="$(cd "$target" && pwd)"
  run_checks
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $DIR — $FILES_READ file(s) read, nothing personal found${DENYLIST:+ (deny-list applied)}"
  else
    bold "✗ $DIR — ${#FINDINGS[@]} finding(s) across $FILES_READ file(s):"
    print_findings
    STATUS=1
  fi
done
log ""
if [[ "$STATUS" -eq 0 ]]; then
  bold "✓ Nothing personal under template/ or examples/."
  exit 0
fi
log "  DESIGN.md D36: no personal data ever enters template/ or examples/. Use the identity"
log "  tokens, invented brands and people, and placeholders flagged AUTHOR TO CONFIRM or VERIFY."
exit 1

#!/usr/bin/env bash
#
# check-template-tokens.sh — static integrity check for the token syntax under template/.
#
#                            Copier renders EVERY file under template/ with Jinja, using the
#                            house delimiters: variables between a percent pair, blocks between
#                            a colon pair, comments between a tilde pair (copier.yml _envops).
#                            A delimiter that is malformed, unregistered or unpaired fails in one
#                            of two ways, and both are invisible until somebody generates: the
#                            render dies with TemplateSyntaxError, or — worse — it succeeds and
#                            a value silently renders to nothing in every project. syntek-media
#                            ships more kinds of text than Markdown (HTML and CSS layouts, ffmpeg
#                            filter strings, SRT, TOML), and every one of them is scanned: none
#                            may carry a stray opener (DESIGN.md D2).
#
#                            syntek-media adds the failure syntek-author found. It ships three
#                            brand kinds, nine platforms and six media kinds from one tree, and
#                            DESIGN.md Section 2 ("Token discipline") allows variant tokens and
#                            conditional blocks only in a declared SPINE SET. A variant token
#                            anywhere else makes a shared file differ between renders, so a file
#                            the design says is byte-identical is not — and a shared skill that
#                            renders differently per brand is a fork nobody can review.
#
#                            Nine checks:
#                              1. Malformed variable — a lower-case name, an empty expression, or
#                                 a backslash or asterisk inside it (Prettier escaping an
#                                 underscore, or pairing it with _emphasis_).
#                              2. Unregistered name — an upper-case name that is not a question
#                                 in copier.yml, or an underscore name that is not one of
#                                 _copier_operation, _copier_answers, _copier_conf.
#                              3. Unpaired blocks — an if/for without its end, an end without its
#                                 opener, an elif/else outside an if.
#                              4. Bare opener — any of the three openers with no closer after it
#                                 on the line. Jinja fails on the opener alone.
#                              5. Stray percent inside a variable — the shape printf escaping
#                                 leaves when a token's percent signs are doubled.
#                              6. A variant token outside the spine set. Identity and locale
#                                 tokens (BRAND_NAME, BRAND_SLUG, OWNER_NAME, OWNER_FIRST_NAME,
#                                 DATE, TIMEZONE) may appear anywhere.
#                              7. A block or comment outside the spine set (raw/endraw excepted).
#                              8. A token inside _…_ emphasis in a Markdown file — Prettier pairs
#                                 the underscores and mangles the token (SB rule 14).
#                              9. An index file gating a row with an expression that is not a
#                                 shipping gate of DESIGN.md Section 3.5 — a BRAND_KIND mode gate,
#                                 or list membership exactly as written there ('youtube' in
#                                 PLATFORMS, 'audiobook' in MEDIA_KINDS), or the negation of a
#                                 templated _exclude line. A copy-only or seed-once gate
#                                 (_copier_operation, SEED_EXAMPLES) is never one: an index
#                                 never gates a row on the examples (D43).
#
#                            The spine set (DESIGN.md Section 2): the root spine
#                            (.claude/rules/syntek-media/*.md and the answers file); the ten
#                            copy-only shared files; every seed (_skip_if_exists, plus DESIGN.md
#                            Section 3.1); every seed-once example; and every index file — a
#                            CONTEXT.md or CLAUDE.md whose folder holds a gated descendant. The
#                            set is computed in _common.sh from DESIGN.md's catalogue and
#                            copier.yml together.
#
#                            Numbers are stable identifiers — other documents cite them.
#                            Append, never renumber.
#
#                            What it CANNOT check: that a token in the spine set is the RIGHT
#                            token, or that a gated row names the path its gate actually ships
#                            (shipped-brands.sh and doc-references.sh check that on renders);
#                            and Jinja syntax that spans lines — a block opener whose closer sits
#                            on the next line is reported as bare, which is the house rule anyway.
#
# SELF-TEST. --self-test writes a fixture template at runtime — a clean baseline, then one
#            mutation per check — and asserts each mutation produces exactly one finding from
#            its own check. Fixtures are never checked in, so they cannot drift.
#
# Requirements: bash 4+, git, grep, awk. No network.
#
# Usage: check-template-tokens.sh [--root DIR] [--quiet] [--self-test] [--help]
#
# Exit codes:  0 = every token and block is well formed and in its place
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, no copier.yml, no template/)

set -euo pipefail
SCRIPT_NAME="check-template-tokens.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false

usage() {
  cat <<'EOF'
check-template-tokens.sh — static integrity check for the token syntax under template/

Usage: check-template-tokens.sh [--root DIR] [--quiet] [--self-test] [--help]

  --root DIR   The template repository (default: this repository)
  --quiet      Print findings only
  --self-test  Prove the checks still fire against a fixture written at runtime
  --help       Show this message

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
    *)           die "unknown argument: $1" ;;
  esac
done

COPIER="$SM_ROOT/copier.yml"
TPL="$SM_ROOT/template"
TOKEN_COUNT=0
FILE_COUNT=0

# ── The scanner ──────────────────────────────────────────────────────────────
#
# One awk pass over every text file. It walks each line opener by opener, so two tokens on a
# line, a block inside a table row, and a raw region are all read the way Jinja reads them.
# Records come out as: check<TAB>file:line<TAB>detail.
SCANNER='
function emit(n, msg) { printf "%d\t%s:%d\t%s\n", n, rel, FNR, msg }
function trimctl(s) { sub(/^[ \t]*[-+]?[ \t]*/, "", s); sub(/[ \t]*[-+]?[ \t]*$/, "", s); return s }
function strip_strings(s) { gsub(/\047[^\047]*\047/, "", s); gsub(/"[^"]*"/, "", s); return s }
function idents(s, mode,   t, id, prev, pc) {
  t = s
  while (match(t, /[A-Za-z_][A-Za-z0-9_]*/)) {
    id = substr(t, RSTART, RLENGTH)
    prev = substr(t, 1, RSTART - 1); sub(/[ \t]+$/, "", prev); pc = substr(prev, length(prev), 1)
    t = substr(t, RSTART + RLENGTH)
    if (pc == "." || pc == "|" || pc ~ /[0-9]/) continue
    if (id in kw) continue
    if (id ~ /^[A-Z]/) {
      if (!(id in reg)) { emit(2, "unregistered token " id " — not a question in copier.yml"); continue }
      if (mode == "var") { tokens++; if (!(id in ident) && !spine) emit(6, "variant token " id " in a shared file — outside the spine set") }
    } else if (id ~ /^_/) {
      if (!(id in cvars)) { emit(2, "unregistered variable " id); continue }
      if (mode == "var" && !spine) emit(6, "copier variable " id " in a shared file — outside the spine set")
    } else if (mode == "var") {
      emit(1, "malformed token — lower-case name " id)
    }
  }
}
function check_var(c,   t) {
  if (index(c, "%") > 0) { emit(5, "stray % inside a variable opener"); return }
  t = trimctl(c)
  if (t == "") { emit(1, "malformed token — empty expression"); return }
  t = strip_strings(t)
  if (t ~ /[\\*`]/) { emit(1, "malformed token — escape or emphasis characters inside it"); return }
  idents(t, "var")
}
function check_block(c,   t, word, rest, top) {
  t = trimctl(c)
  word = t; sub(/[ \t].*$/, "", word)
  rest = t; sub(/^[^ \t]*[ \t]*/, "", rest)
  if (word == "raw") { inraw = 1; return }
  if (word == "endraw") { emit(3, "endraw with no raw before it"); return }
  if (!spine && last7 != FNR) { emit(7, "block delimiter in a shared file — outside the spine set"); last7 = FNR }
  if (word == "if" || word == "for") { stack[++depth] = word; stackline[depth] = FNR }
  else if (word == "endif" || word == "endfor") {
    top = (word == "endif") ? "if" : "for"
    if (depth == 0 || stack[depth] != top) emit(3, word " with no open " top)
    else depth--
  }
  else if (word == "elif" || word == "else") {
    if (depth == 0 || stack[depth] != "if") emit(3, word " outside an if")
  }
  if (word == "if" || word == "elif" || word == "for") {
    idents(strip_strings(rest), "block")
    if (isindex && word != "for") {
      t = rest; gsub(/"/, "\047", t); gsub(/[ \t]+/, " ", t); sub(/^ /, "", t); sub(/ $/, "", t)
      if (!(t in allowed)) emit(9, "index file gates a row with \"" t "\" — not a shipping gate from DESIGN.md Section 3.5 or copier.yml")
    }
  }
}
function finish_file() {
  if (rel == "") return
  while (depth > 0) { printf "3\t%s:%d\t%s\n", rel, stackline[depth], stack[depth] " with no matching end"; depth-- }
  if (inraw) printf "3\t%s:%d\t%s\n", rel, FNRlast, "raw with no endraw"
}
BEGIN {
  n = split("if else elif endif and or not in is true false none True False None for endfor raw endraw set loop", a, " ")
  for (i = 1; i <= n; i++) kw[a[i]] = 1
  n = split(regs, a, " "); for (i = 1; i <= n; i++) reg[a[i]] = 1
  n = split(idents_ok, a, " "); for (i = 1; i <= n; i++) ident[a[i]] = 1
  n = split(cvarlist, a, " "); for (i = 1; i <= n; i++) cvars[a[i]] = 1
}
FNR == NR {
  split($0, f, "\t")
  if (f[1] == "K") kind[f[3]] = f[2]
  else if (f[1] == "G") allowed[f[2]] = 1
  next
}
FNR == 1 {
  finish_file()
  rel = substr(FILENAME, length(base) + 1)
  k = (rel in kind) ? kind[rel] : "shared"
  spine = (k != "shared"); isindex = (k == "index")
  ismd = (rel ~ /\.md$/); inraw = 0; depth = 0; last7 = 0; files++
}
{
  FNRlast = FNR
  line = $0; pos = 1
  while (pos <= length(line)) {
    s = substr(line, pos)
    i = 0; op = ""
    i1 = index(s, "<%"); i2 = index(s, "<:"); i3 = index(s, "<~")
    if (i1 && (!i || i1 < i)) { i = i1; op = "<%" }
    if (i2 && (!i || i2 < i)) { i = i2; op = "<:" }
    if (i3 && (!i || i3 < i)) { i = i3; op = "<~" }
    if (!i) break
    closer = (op == "<%") ? "%>" : ((op == "<:") ? ":>" : "~>")
    r = substr(s, i + 2)
    j = index(r, closer)
    if (inraw) {
      if (op == "<:" && j) { c = trimctl(substr(r, 1, j - 1)); if (c == "endraw") inraw = 0 }
      pos += i + 1; continue
    }
    if (!j) {
      if (op == "<%" && index(r, "%") > 0) emit(5, "stray % in an unclosed variable opener")
      else emit(4, "bare " op " opener — no closer after it on the line")
      break
    }
    content = substr(r, 1, j - 1)
    if (op == "<%") check_var(content)
    else if (op == "<:") check_block(content)
    else if (!spine && last7 != FNR) { emit(7, "comment delimiter in a shared file — outside the spine set"); last7 = FNR }
    pos += i + j + 2
  }
  if (ismd && !inraw && line ~ /(^|[^A-Za-z0-9_*])_([^_ ][^_]*)?<%[^%]*%>[^_]*_($|[^A-Za-z0-9_])/)
    emit(8, "token inside _emphasis_ — Prettier will mangle it; use **bold**")
}
END { finish_file(); printf "T\t%d\t%d\n", tokens, files > "/dev/stderr" }
'

run_checks() {
  FINDINGS=()
  local manifest files=() f kind g regs stats line n loc msg
  build_sets "$COPIER"
  regs="$(registered_keys "$COPIER" | tr '\n' ' ')"
  manifest="$(mktemp)"
  {
    while IFS= read -r -d '' f; do
      grep -Iq . "$TPL/$f" 2>/dev/null || continue
      files+=("$TPL/$f")
      if kind="$(spine_kind "$f")"; then printf 'K\t%s\t%s\n' "$kind" "$f"; fi
    done < <(list_files0 "$TPL")
    for g in "${SM_ALLOWED_GATES[@]}"; do printf 'G\t%s\n' "$g"; done
  } > "$manifest"

  if [[ ${#files[@]} -eq 0 ]]; then
    rm -f "$manifest"; TOKEN_COUNT=0; FILE_COUNT=0; return 0
  fi
  stats="$(mktemp)"
  while IFS=$'\t' read -r n loc msg; do
    [[ -z "$n" ]] && continue
    finding "check $n — $loc — $msg"
  done < <(awk -v base="$TPL/" -v regs="$regs" -v idents_ok="$SM_IDENTITY_TOKENS" \
             -v cvarlist="$SM_COPIER_VARS" "$SCANNER" "$manifest" "${files[@]}" 2>"$stats" | sort -t$'\t' -k2,2V -k1,1n)
  line="$(grep '^T' "$stats" || true)"
  TOKEN_COUNT="$(cut -f2 <<< "$line")"; FILE_COUNT="$(cut -f3 <<< "$line")"
  rm -f "$manifest" "$stats"
}

# ── Self-test ────────────────────────────────────────────────────────────────

self_test() {
  local tmp real_tpl="$TPL" real_copier="$COPIER" q="'"
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  TPL="$tmp/template"; COPIER="$tmp/copier.yml"
  mkdir -p "$TPL/publishing/docs/reference" "$TPL/toolkit" "$TPL/brand/src/design-system"
  cat > "$COPIER" <<'EOF'
_exclude:
  - "<: if _copier_operation == 'update' :>/README.md<: endif :>"
  - "<: if not ('tiktok' in PLATFORMS) :>/publishing/docs/reference/tiktok.md<: endif :>"
  - "<: if _copier_operation == 'update' or not SEED_EXAMPLES :>/scripts/src/pieces/000-example-piece<: endif :>"
_skip_if_exists:
  - /README.md
BRAND_NAME:
  type: str
BRAND_KIND:
  type: str
OWNER_NAME:
  type: str
PLATFORMS:
  type: str
MEDIA_KINDS:
  type: str
SEED_EXAMPLES:
  type: bool
EOF
  # Clean baseline: a token, a list and a gate in a copy-only shared file, a platform-gated row
  # in an index file, an identity token in a shared file, the answers file's real Jinja, and a
  # raw block quoting every delimiter in a shared file. A CSS file is scanned as well.
  printf '# <%%BRAND_NAME%%>\n\nOn <%% PLATFORMS | join(%s, %s) %%>.\n<: if BRAND_KIND == %sbusiness%s :>Business only.<: endif :>\n' "$q" "$q" "$q" "$q" > "$TPL/README.md"
  printf '<%% _copier_answers|to_nice_yaml -%%>\n' > "$TPL/$SM_ANSWERS_FILE"
  printf '# CONTEXT.md — publishing/docs/reference/\n\n<: if %stiktok%s in PLATFORMS :>├── tiktok.md  ← the TikTok guide<: endif :>\n' "$q" "$q" > "$TPL/publishing/docs/reference/CONTEXT.md"
  printf '# Notes\n\nMaintained by **<%%OWNER_NAME%%>**.\n\n<: raw :>Quote <%%X%%> and <: if :> freely.<: endraw :>\n' > "$TPL/toolkit/notes.md"
  printf '# CONTEXT.md — toolkit/\n' > "$TPL/toolkit/CONTEXT.md"
  printf ':root { --color-bg: #ffffff; }\n' > "$TPL/brand/src/design-system/tokens.css"
  st_baseline "the fixture template"

  local shared="$TPL/toolkit/CONTEXT.md" keep index="$TPL/publishing/docs/reference/CONTEXT.md" ikeep
  keep="$(cat "$shared")"; ikeep="$(cat "$index")"
  put() { printf '%s\n%s\n' "$keep" "$1" > "$shared"; }
  iput() { printf '%s\n%s\n' "$ikeep" "$1" > "$index"; }

  put '<%brand_name%>';                                probe "check 1 fires on a lower-cased token" "check 1"
  put '<%BRAND\_NAME%>';                               probe "check 1 fires on a token Prettier escaped" "check 1"
  put '<%NOT_A_REAL_TOKEN%>';                          probe "check 2 fires on an unregistered token" "check 2"
  put '<%BRAND_NAME%> and <%_copier_secret%>';         probe "check 2 fires on an unknown copier variable" "check 2"
  printf '%s\n' "$keep" > "$shared"
  printf '<: if BRAND_KIND == %sauthor-fiction%s :>open, never closed\n' "$q" "$q" >> "$TPL/README.md"
  probe "check 3 fires on an if with no endif" "check 3"
  printf '# <%%BRAND_NAME%%>\n\nOn <%% PLATFORMS | join(%s, %s) %%>.\n<: if BRAND_KIND == %sbusiness%s :>Business only.<: endif :>\n' "$q" "$q" "$q" "$q" > "$TPL/README.md"
  put 'if "<:" in v:';                                 probe "check 4 fires on a bare block opener" "check 4"
  put 'note the <~ opener';                            probe "check 4 fires on a bare comment opener" "check 4"
  put 'a <%TRUNCATED';                                 probe "check 4 fires on an unclosed variable" "check 4"
  put '<%%BRAND_NAME%%>';                              probe "check 5 fires on a doubled opener" "check 5"
  put 'a <%TRUNCATED%';                                probe "check 5 fires on a token cut after its %" "check 5"
  put 'Every <%BRAND_KIND%> project.';                 probe "check 6 fires on a variant token in a shared file" "check 6"
  put 'On <% PLATFORMS | join(", ") %>.';              probe "check 6 fires on a list rendered in a shared file" "check 6"
  put "<: if 'youtube' in PLATFORMS :>x<: endif :>";   probe "check 7 fires on a block in a shared file" "check 7"
  put '<~ a note ~>';                                  probe "check 7 fires on a comment in a shared file" "check 7"
  put 'Signed _by <%OWNER_NAME%> alone_ today.';       probe "check 8 fires on a token inside _emphasis_" "check 8"
  printf '%s\n' "$keep" > "$shared"
  printf '/* a stray <: in a stylesheet */\n' >> "$TPL/brand/src/design-system/tokens.css"
  probe "check 4 fires on a stray opener in a CSS file" "check 4"
  printf ':root { --color-bg: #ffffff; }\n' > "$TPL/brand/src/design-system/tokens.css"
  iput "<: if 'tiktok' in MEDIA_KINDS :>├── tiktok.md  ← wrong list<: endif :>"
  probe "check 9 fires on an index row gated on the wrong list" "check 9"
  iput "<: if SEED_EXAMPLES :>├── 000-example-piece/  ← the example<: endif :>"
  probe "check 9 fires on an index row gated on the examples" "check 9"
  iput "<: if BRAND_KIND != 'business' :>├── books.md  ← not a Section 3.5 gate<: endif :>"
  probe "check 9 fires on an index gate that is not a shipping gate" "check 9"
  iput "<: if BRAND_KIND == 'author-nonfiction' :>├── NONFICTION.md  ← a mode gate<: endif :>"
  probe_clean "a BRAND_KIND mode gate is a shipping gate"
  printf '%s\n' "$ikeep" > "$index"

  TPL="$real_tpl"; COPIER="$real_copier"; SM_SETS_FOR=""
  st_finish "well-formed template syntax from broken"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

[[ -f "$COPIER" ]] || die "no copier.yml at $SM_ROOT — nothing registers a token"
[[ -d "$TPL" ]] || die "no template/ directory at $SM_ROOT"

bold "▸ $SCRIPT_NAME"
run_checks
if [[ ${#FINDINGS[@]} -eq 0 ]]; then
  bold "✓ ${TOKEN_COUNT:-0} well-formed token(s) across ${FILE_COUNT:-0} text file(s) under template/ — all registered, all in their place."
  exit 0
fi
bold "✗ ${#FINDINGS[@]} finding(s) across ${FILE_COUNT:-0} text file(s):"
print_findings
log ""
log "  Variant tokens and blocks belong in the spine set only (DESIGN.md Section 2). Move a"
log "  variant difference into a gated file or a mode file; never into a shared one."
exit 1

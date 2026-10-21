#!/usr/bin/env bash
#
# community-files.sh — Verify the root's community files: all present, the licence exact, one contact.
#
#                      GitHub reads a handful of files at a repository's root and in .github/ to
#                      show a visitor the licence, how to contribute, where a vulnerability goes
#                      and what conduct is expected, and to shape every new issue and pull
#                      request. DESIGN.md D83 fixes the set: LICENSE, CONTRIBUTING.md,
#                      SECURITY.md and CODE_OF_CONDUCT.md at the root, and CODEOWNERS,
#                      PULL_REQUEST_TEMPLATE.md and ISSUE_TEMPLATE/{bug_report.yml,
#                      template_improvement.yml, config.yml} in .github/ (SM_COMMUNITY_FILES).
#                      None ships: `_subdirectory: template` keeps the root out of every render.
#                      Every other audit reads template/, examples/, the development settings or
#                      a render, so until this script nothing looked at these files at all. A
#                      LICENSE an editor 'tidied' stops GitHub detecting the licence; a security
#                      link copied from another repository sends a report to the wrong
#                      maintainers; an address pasted into an issue form is published to every
#                      visitor. None of these fails loudly, and each reaches the public the
#                      moment it lands on the default branch.
#
#                      Six checks, over the repository root:
#                        1. Each D83 file exists, as a file and not a link, and no folder on its
#                           path (.github, .github/ISSUE_TEMPLATE) is a link: GitHub stores a link
#                           as its target's path and shows that, never the target's text, and it
#                           reads nothing through a linked folder.
#                        2. LICENSE is the approved MIT text, byte for byte: the family's reviewed
#                           LICENSE (syntek-base commit 969ab58, not yet on syntek-base's main,
#                           whose LICENSE still names the old holder), plain MIT and nothing
#                           else, so GitHub detects it and every family repository carries the
#                           same bytes. A difference is named by line and column, and trailing
#                           whitespace and a byte-order mark by name. The family's permission
#                           for generated projects lives in CONTRIBUTING.md and the README,
#                           never here. The text is embedded below rather than in _common.sh:
#                           this check alone reads it, and D83 names it without restating it, so
#                           it is no part of the catalogue _common.sh transcribes. Its sha256 pins
#                           it: an edit to the embedded text (a re-wrap, a stripped final newline,
#                           a new year) stops the script with exit 2 before any check runs, so the
#                           expectation can never drift to match a broken LICENSE.
#                        3. No Markdown file in .github/ISSUE_TEMPLATE/. A house rule, not
#                           GitHub's: GitHub lists a Markdown file there as an issue template once
#                           it gains name and about front matter, so the folder holds GitHub's own
#                           YAML files only and carries no CONTEXT.md and CLAUDE.md pair;
#                           .github/CONTEXT.md describes it instead (D83).
#                        4. Each issue form (every .yml or .yaml in that folder but config.yml)
#                           has a top-level name, description and body, each with a value (an
#                           unquoted ~ or null is none), body a list, its items at one indentation
#                           (a mapping that only holds a list deeper down is not one): GitHub
#                           refuses a form without them. And config.yml sets
#                           blank_issues_enabled to the boolean false (unquoted; 'false' in quotes
#                           is a string) and has a contact link whose url is this repository's
#                           private vulnerability reporting (SM_PRIVATE_REPORT_URL). Blank issues
#                           off hides the blank issue from outside reporters only: a user with
#                           write access still sees one, marked 'Maintainers only'.
#                        5. At most one email address across the community files, and only in
#                           CODE_OF_CONDUCT.md, whose Enforcement section names the contact: a
#                           file anywhere else that holds an address is a finding, and so is a
#                           Code of Conduct that writes an address more than once, the same one
#                           twice included, in any case. The nine files are read, and any further
#                           issue form beside them, since GitHub shows every one to the public. An
#                           address is scrub.sh check 5's shape; a GitHub handle (@name, with
#                           nothing before the @) is not one, nor is a Git remote's user@host
#                           followed by ':' or '/' (git@github.com:owner/repo.git).
#                        6. SECURITY.md names private vulnerability reporting: the phrase (a line
#                           break inside it allowed, any case) or this repository's
#                           advisories/new URL. Reports go through that route only (D83).
#
#                      Numbers are stable identifiers. Append, never renumber.
#
#                      What it CANNOT check: the full issue-form and config schema (field types,
#                      unique ids, validations, label names): the forms are read by a
#                      top-level-key reader written in awk, not a YAML parser, because PyYAML is
#                      not part of the standard library and the source job installs nothing. It
#                      reads bare and quoted keys, block scalars, CRLF line endings and a list
#                      written at the key's own indentation, which covers GitHub's documented
#                      shapes; a flow mapping ({name: …, url: …}) is not read, at the top level
#                      or as a contact link. By hand:
#                      `uvx check-jsonschema --builtin-schema vendor.github-issue-forms <form>`
#                      and `--builtin-schema vendor.github-issue-config` on config.yml. Nor can it
#                      check that private vulnerability reporting is switched on in the
#                      repository's settings (it is read by
#                      `gh api repos/Syntek-Dev/syntek-media/private-vulnerability-reporting`),
#                      that the files are on the default branch, where GitHub reads
#                      them, that a link in SECURITY.md points at this repository (the phrase
#                      alone passes check 6; config.yml's link is held to it by check 4), that
#                      the Code of Conduct's address is the maintainer's, which section of the
#                      Code of Conduct it sits in (Enforcement, by D83, is a reviewer's read),
#                      that the Code of Conduct's text is the Contributor Covenant 2.1, that the
#                      licence words in CONTRIBUTING.md and the README are the family's verbatim
#                      (a reviewer's call: they change only together with syntek-author's), or an
#                      address written to dodge the shape ('name at domain').
#
# SELF-TEST. --self-test writes a fixture root at runtime (an invented copyright holder, near
#            misses such as a GitHub handle, 'e-mail address' and an SSH remote, a form whose
#            list starts at the key's indentation, a block-scalar description), proves it
#            clean, then applies one mutation per check, several for checks 1, 2, 4 and 5, and
#            asserts exactly one finding each; it also proves CRLF YAML, a quoted url, and each
#            of check 6's two accepted forms on its own are not flagged, and that a file it
#            cannot read stops the run with exit 2 (where the user cannot read a mode-000 file;
#            root can, and that probe is then reported as not run).
#
# Requirements: bash 4+, grep, awk (mawk is enough), cmp, tr, and sha256sum or shasum. No
#               network, no python3.
#
# Usage: community-files.sh [--root DIR] [--quiet] [--self-test] [--help]
#
# Exit codes:  0 = every community file is present and holds what D83 promises
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, no sha256 tool, the embedded LICENSE text no
#                  longer matches its pinned sha256, or a community file, issue form or folder
#                  on their path that exists but cannot be read): the run is incomplete

set -euo pipefail
SCRIPT_NAME="community-files.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false

usage() {
  cat <<'EOF'
community-files.sh — Verify the root's community files: all present, the licence exact, one contact

Usage: community-files.sh [--root DIR] [--quiet] [--self-test] [--help]

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

FORMS_DIR=".github/ISSUE_TEMPLATE"
CONFIG="$FORMS_DIR/config.yml"
# The same shape as scrub.sh check 5. A GitHub handle (@Syntek-Studio) has nothing before its @.
EMAIL_RE='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
FORMS_READ=0

# ── The approved LICENSE (check 2) ───────────────────────────────────────────
#
# The family's reviewed MIT text: syntek-base commit 969ab58 `LICENSE` (not yet on syntek-base's
# main; syntek-author's uncommitted copy has the same bytes). The holder is a variable only so
# the self-test's fixture can carry an invented one; the real run assembles the bytes with this
# holder and the pin below proves them. It is the root LICENSE's own line, and the one real name
# in .github/ (.github/CLAUDE.md, 'No personal data').
LICENSE_HOLDER="Sam Bailey t/a Syntek"
LICENSE_SHA256="62d902acf87975ce2a71148f791213cc757179c1fee3f746397063fc50537cdf"

approved_license() {
  cat <<EOF
MIT License

Copyright (c) 2026 $LICENSE_HOLDER

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
}

sha256_stdin() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum | cut -c1-64
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 | cut -c1-64
  else die "neither sha256sum nor shasum is installed"; fi
}

verify_approved_text() {
  local got
  got="$(approved_license | sha256_stdin)"
  [[ "$got" == "$LICENSE_SHA256" ]] \
    || die "the approved LICENSE text embedded in this script hashes to $got, not $LICENSE_SHA256 — restore it byte for byte from the family's reviewed LICENSE (git show 969ab58:LICENSE in syntek-base)"
}

clip() { # $1 = text → at most 72 characters, quoted
  local s="$1"
  [[ ${#s} -gt 72 ]] && s="${s:0:69}..."
  printf "'%s'" "$s"
}

clip_at() { # $1 = text, $2 = a 0-based column → about 60 characters around it, quoted
  local s="$1" p="$2" start=0 pre="" post=""
  if [[ $p -gt 30 ]]; then start=$((p - 30)); pre="..."; fi
  [[ $((start + 60)) -lt ${#s} ]] && post="..."
  printf "'%s%s%s'" "$pre" "${s:start:60}" "$post"
}

# How LICENSE differs from the approved text, in one line, or nothing when it does not. Columns
# count bytes (LC_ALL=C), so a byte-order mark or a stray multibyte character counts as stored.
license_difference() { # $1 = file
  local f="$1" i n p a b LC_ALL=C
  local -a want=() got=()
  cmp -s <(approved_license) "$f" && return 0
  if grep -q $'\r' "$f"; then
    printf 'has CRLF (Windows) line endings; the approved text uses LF'; return 0
  fi
  if [[ ! -s "$f" ]]; then printf 'is empty'; return 0; fi
  if [[ "$(head -c3 "$f")" == $'\xef\xbb\xbf' ]]; then
    printf 'begins with a byte-order mark (bytes EF BB BF before line 1); the approved text has none'; return 0
  fi
  mapfile -t want < <(approved_license)
  mapfile -t got < "$f"
  n=${#want[@]}; [[ ${#got[@]} -gt $n ]] && n=${#got[@]}
  for ((i = 0; i < n; i++)); do
    if [[ $i -ge ${#got[@]} ]]; then
      printf 'ends after line %d; the approved text goes on with %s' "$i" "$(clip "${want[i]}")"; return 0
    fi
    if [[ $i -ge ${#want[@]} ]]; then
      printf 'carries more than the approved text: line %d reads %s' "$((i + 1))" "$(clip "${got[i]}")"; return 0
    fi
    a="${want[i]}"; b="${got[i]}"
    [[ "$a" == "$b" ]] && continue
    if [[ "$b" == "$a"* && "${b:${#a}}" =~ ^[[:space:]]+$ ]]; then
      printf 'line %d has trailing whitespace after column %d; the approved text has none' "$((i + 1))" "${#a}"
      return 0
    fi
    p=0
    while [[ $p -lt ${#a} && $p -lt ${#b} && "${a:p:1}" == "${b:p:1}" ]]; do p=$((p + 1)); done
    printf 'line %d differs at column %d: it reads %s where the approved text reads %s' \
      "$((i + 1))" "$((p + 1))" "$(clip_at "$b" "$p")" "$(clip_at "$a" "$p")"
    return 0
  done
  if [[ -n "$(tail -c1 "$f")" ]]; then printf 'lacks its final newline'; return 0; fi
  printf 'differs from the approved bytes (sha256 %s)' "$(sha256_stdin < "$f")"
}

# ── A top-level-key reader for GitHub's YAML files (check 4) ─────────────────
#
# Prints, per top-level key, "K key value quoted items content": the inline value unquoted and
# without its comment; 1 when that value was quoted, else 0; the count of list items under the
# key, only those at the indentation of the key's first line below it, so a list nested deeper
# in a mapping is not counted (a list written at the key's own indentation is); and the count
# of all lines under the key. It prints "U url" for every url inside contact_links. The fields
# are joined by the unit separator (octal 037), never a tab: read collapses runs of a
# whitespace separator, and an empty value would shift every field after it. Comments, blank
# lines and document markers are skipped; a trailing CR is dropped. mawk-compatible: no
# interval expressions, no gawk-only functions, the single quote built with sprintf rather than
# escaped in a regular expression, and no `.*$`: mawk 1.3.4 (20240819) fails to match an empty
# `.*` before the anchor, so `body:` would keep its colon.
yaml_top() { # $1 = file
  awk '
    function unq(s,   c, out, i, ch) {
      uq = 0
      sub(/^[ \t]+/, "", s)
      c = substr(s, 1, 1)
      if (c == "\"" || c == q) {
        uq = 1
        out = ""; i = 2
        while (i <= length(s)) {
          ch = substr(s, i, 1)
          if (c == "\"" && ch == "\\") { out = out substr(s, i + 1, 1); i += 2; continue }
          if (ch == c) {
            if (c == q && substr(s, i + 1, 1) == q) { out = out q; i += 2; continue }
            break
          }
          out = out ch; i++
        }
        return out
      }
      if (s ~ /^#/) return ""
      sub(/[ \t]+#.*/, "", s); sub(/[ \t]+$/, "", s)
      return s
    }
    function flush() {
      if (key != "") printf "K\037%s\037%s\037%d\037%d\037%d\n", key, val, vq, items, content
      key = ""
    }
    BEGIN {
      q = sprintf("%c", 39)
      bare = "^[A-Za-z_][A-Za-z0-9_-]*[ \t]*:([ \t]|$)"
      quoted = "^(\"[^\"]*\"|" q "[^" q "]*" q ")[ \t]*:([ \t]|$)"
    }
    { sub(/\r$/, "") }
    /^(---|\.\.\.)([ \t]|$)/ { next }
    /^[ \t]*$/ || /^[ \t]*#/ { next }
    $0 ~ bare || $0 ~ quoted {
      flush()
      rest = $0
      if ($0 ~ quoted) {
        c = substr($0, 1, 1); rest = substr($0, 2)
        key = substr(rest, 1, index(rest, c) - 1); rest = substr(rest, index(rest, c) + 1)
        sub(/^[ \t]*:/, "", rest)
      } else {
        key = $0; sub(/[ \t]*:.*/, "", key)
        sub(/^[^:]*:/, "", rest)
      }
      val = unq(rest); vq = uq; items = 0; content = 0; first = -1
      next
    }
    /^[^ \t-]/ { flush(); next }
    {
      if (key == "") next
      content++
      match($0, /^[ \t]*/)
      if (first < 0) first = RLENGTH
      if ($0 ~ /^[ \t]*-([ \t]|$)/ && RLENGTH == first) items++
      if (key == "contact_links") {
        line = $0
        sub(/^[ \t]*(-[ \t]+)?/, "", line)
        if (line ~ /^url[ \t]*:/) { sub(/^url[ \t]*:/, "", line); printf "U\037%s\n", unq(line) }
      }
    }
    END { flush() }
  ' "$1"
}

# ── The checks ───────────────────────────────────────────────────────────────

present() { [[ -f "$SM_ROOT/$1" && ! -L "$SM_ROOT/$1" ]]; }

# The issue forms check 4 reads and check 5 scans: every .yml or .yaml directly in the folder
# but config.yml, as files (a link is check 1's when it is a D83 file, and never read).
issue_forms() {
  [[ -d "$SM_ROOT/$FORMS_DIR" ]] || return 0
  (cd "$SM_ROOT" && find "$FORMS_DIR" -mindepth 1 -maxdepth 1 -type f \( -name '*.yml' -o -name '*.yaml' \) \
     ! -path "$CONFIG" -print | LC_ALL=C sort)
}

check_form() { # $1 = repository-relative form
  local rel="$1" kind k v quoted items content block='^[|>][-+0-9]*$' flow='^\[[[:space:]]*[^][:space:]]'
  local null='^(~|null|Null|NULL)$'
  local -A val=() vquoted=() nitems=() ncontent=()
  while IFS=$'\037' read -r kind k v quoted items content; do
    [[ "$kind" == K ]] || continue
    val["$k"]="$v"; vquoted["$k"]="$quoted"; nitems["$k"]="$items"; ncontent["$k"]="$content"
  done < <(yaml_top "$SM_ROOT/$rel")
  for k in name description; do
    v="${val[$k]-}"
    if [[ -z "${val[$k]+set}" ]]; then
      finding "check 4 — $rel has no top-level $k (GitHub requires name, description and body)"
    elif [[ "${vquoted[$k]}" -eq 0 && "$v" =~ $null ]]; then
      finding "check 4 — $rel has a top-level $k with no value ('$v' is YAML's null)"
    elif [[ -z "$v" || "$v" =~ $block ]] && [[ "${ncontent[$k]}" -eq 0 ]]; then
      finding "check 4 — $rel has a top-level $k with no value"
    fi
  done
  if [[ -z "${val[body]+set}" ]]; then
    finding "check 4 — $rel has no top-level body (GitHub requires name, description and body)"
  elif [[ "${nitems[body]}" -eq 0 && ! "${val[body]}" =~ $flow ]]; then
    finding "check 4 — $rel has a top-level body that is not a list of fields"
  fi
}

check_config() {
  local kind a b q blank="" blank_quoted=0 found=false
  while IFS=$'\037' read -r kind a b q _; do
    case "$kind" in
      K) [[ "$a" == blank_issues_enabled ]] && { blank="${b:-(empty)}"; blank_quoted="$q"; } ;;
      U) [[ "$a" == "$SM_PRIVATE_REPORT_URL" ]] && found=true ;;
    esac
  done < <(yaml_top "$SM_ROOT/$CONFIG")
  case "$blank" in
    false|False|FALSE)
      [[ "$blank_quoted" -eq 0 ]] \
        || finding "check 4 — $CONFIG sets blank_issues_enabled to the quoted string '$blank', not the boolean false — GitHub's schema refuses it; write it without quotes" ;;
    "") finding "check 4 — $CONFIG does not set blank_issues_enabled: false — outside reporters would be offered a blank issue" ;;
    *)  finding "check 4 — $CONFIG sets blank_issues_enabled to '$blank', not false — outside reporters would be offered a blank issue" ;;
  esac
  $found || finding "check 4 — $CONFIG has no contact link whose url is $SM_PRIVATE_REPORT_URL, this repository's private vulnerability reporting (D83)"
}

run_checks() {
  FINDINGS=()
  FORMS_READ=0
  local rel how raw found dir acc part linked n
  local -a scanned=() forms=() parts=() hits=()
  local -A seen_link=()

  # 1. Each D83 file exists, as a file, and no folder on its path is a link.
  for rel in $SM_COMMUNITY_FILES; do
    linked=""; acc=""
    dir="${rel%/*}"; [[ "$dir" == "$rel" ]] && dir=""
    IFS='/' read -r -a parts <<< "$dir"
    for part in "${parts[@]}"; do
      acc="${acc:+$acc/}$part"
      if [[ -L "$SM_ROOT/$acc" ]]; then linked="$acc"; break; fi
    done
    if [[ -n "$linked" ]]; then
      [[ -n "${seen_link[$linked]+set}" ]] && continue
      seen_link["$linked"]=1
      finding "check 1 — $linked/ is a link; GitHub reads nothing through a linked folder, so it never sees $rel or anything beside it — move the folder itself back (D83)"
    elif [[ -L "$SM_ROOT/$rel" ]]; then
      finding "check 1 — $rel is a link; GitHub shows a link's target path, never its text — write the file itself (D83)"
    elif [[ ! -f "$SM_ROOT/$rel" ]]; then
      finding "check 1 — $rel is missing; D83 puts it in every family repository, at the root or in .github/"
    fi
  done

  # A file or folder that is there but cannot be read makes every later check wrong, never clean:
  # the run is incomplete (exit 2), like a missing tool.
  for rel in $SM_COMMUNITY_FILES; do
    dir="${rel%/*}"
    if [[ "$dir" != "$rel" && -d "$SM_ROOT/$dir" ]] && ! [[ -r "$SM_ROOT/$dir" && -x "$SM_ROOT/$dir" ]]; then
      die "cannot read the folder $dir/ — the community files cannot be checked; restore its permissions"
    fi
    if [[ -e "$SM_ROOT/$rel" && ! -r "$SM_ROOT/$rel" ]]; then
      die "cannot read $rel — the community files cannot be checked; restore its permissions"
    fi
  done

  # 2. LICENSE is the approved text, byte for byte.
  if present LICENSE; then
    how="$(license_difference "$SM_ROOT/LICENSE")"
    [[ -z "$how" ]] || finding "check 2 — LICENSE $how — it must be the family's MIT text, byte for byte (D83)"
  fi

  # 3. No Markdown in ISSUE_TEMPLATE/.
  if [[ -d "$SM_ROOT/$FORMS_DIR" ]]; then
    while IFS= read -r rel; do
      [[ -z "$rel" ]] && continue
      finding "check 3 — $rel is Markdown; $FORMS_DIR/ holds GitHub's own YAML files only, with no pair (house rule, D83) — .github/CONTEXT.md describes the folder"
    done < <(cd "$SM_ROOT" && find "$FORMS_DIR" \( -type f -o -type l \) \( -iname '*.md' -o -iname '*.markdown' \) -print | LC_ALL=C sort)
  fi

  # 4. Issue forms and config.yml.
  mapfile -t forms < <(issue_forms)
  for rel in "${forms[@]}"; do
    [[ -z "$rel" ]] && continue
    [[ -r "$SM_ROOT/$rel" ]] || die "cannot read $rel — the community files cannot be checked; restore its permissions"
    FORMS_READ=$((FORMS_READ + 1))
    check_form "$rel"
  done
  if present "$CONFIG"; then check_config; fi

  # 5. One address at most, written once, and only in the Code of Conduct. Every occurrence is
  # counted, in any case; a Git remote's user@host followed by ':' or '/' is not an address.
  for rel in $SM_COMMUNITY_FILES "${forms[@]}"; do
    [[ -n "$rel" ]] && present "$rel" || continue
    [[ " ${scanned[*]} " == *" $rel "* ]] && continue
    scanned+=("$rel")
    raw="$(grep -oE "$EMAIL_RE(:[^[:space:]]|/)?" "$SM_ROOT/$rel")" && n=0 || n=$?
    [[ $n -gt 1 ]] && die "cannot read $rel — grep failed (exit $n); the community files cannot be checked"
    mapfile -t hits < <(grep -vE '[:/]' <<< "$raw" | grep -v '^$' | tr '[:upper:]' '[:lower:]')
    [[ ${#hits[@]} -eq 0 ]] && continue
    found="$(printf '%s\n' "${hits[@]}" | LC_ALL=C sort -u | paste -sd, - | sed 's/,/, /g')"
    if [[ "$rel" != CODE_OF_CONDUCT.md ]]; then
      finding "check 5 — $rel holds an email address ($found); the repository's one address is the Code of Conduct's enforcement contact (D83)"
    elif [[ ${#hits[@]} -gt 1 ]]; then
      finding "check 5 — CODE_OF_CONDUCT.md writes an email address ${#hits[@]} times ($found); D83 allows one, written once"
    fi
  done

  # 6. SECURITY.md names private vulnerability reporting.
  if present SECURITY.md; then
    if ! grep -qF "$SM_PRIVATE_REPORT_URL" "$SM_ROOT/SECURITY.md" \
       && ! tr -s '[:space:]' ' ' < "$SM_ROOT/SECURITY.md" | grep -qiF 'private vulnerability reporting'; then
      finding "check 6 — SECURITY.md names neither private vulnerability reporting nor $SM_PRIVATE_REPORT_URL; reports go only through that route (D83)"
    fi
  fi
}

# ── Self-test ────────────────────────────────────────────────────────────────

write_fixture() { # $1 = root; every file in its good state, with invented people and addresses
  local r="$1"
  rm -rf "$r"; mkdir -p "$r/$FORMS_DIR"
  approved_license > "$r/LICENSE"
  printf '# Contributing\n\nOpen an issue first. Contributions are made under the MIT Licence\n(inbound = outbound), with no contributor licence agreement.\n' > "$r/CONTRIBUTING.md"
  printf "# Security Policy\n\nReport a vulnerability only through GitHub's private vulnerability\nreporting: [open a private report](%s).\n" "$SM_PRIVATE_REPORT_URL" > "$r/SECURITY.md"
  cat > "$r/CODE_OF_CONDUCT.md" <<'EOF'
# Contributor Covenant Code of Conduct

## Scope

Examples include using an official e-mail address or posting via an official account.

## Enforcement

Instances of unacceptable behavior may be reported to the community leaders responsible for
enforcement at conduct@example.invalid. All complaints will be reviewed.
EOF
  printf '* @Example-Owner\n/LICENSE            @Example-Owner\n' > "$r/.github/CODEOWNERS"
  printf '## Checklist\n\n- [ ] CI is green (actions/checkout@v7 and the rest).\n- [ ] I make this contribution on the terms of CONTRIBUTING.md.\n' \
    > "$r/.github/PULL_REQUEST_TEMPLATE.md"
  cat > "$r/$FORMS_DIR/bug_report.yml" <<'EOF'
# The bug report form.
name: Bug report
description: Something in the template is broken # a trailing comment
title: "[Bug]: "
labels: [bug]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting. Never paste anybody's personal data.
  - type: textarea
    id: what-happened
    attributes:
      label: What happened
      description: Shorten paths and replace names with invented ones.
    validations:
      required: true
EOF
  cat > "$r/$FORMS_DIR/template_improvement.yml" <<'EOF'
---
"name": 'Template improvement'
description: >-
  A change to what the template generates,
  or to how it is built.
labels: [enhancement]
body:
- type: textarea
  id: problem
  attributes:
    label: The problem
EOF
  cat > "$r/$CONFIG" <<EOF
blank_issues_enabled: false
contact_links:
  - name: Security vulnerability
    url: $SM_PRIVATE_REPORT_URL
    about: Report it privately, never in a public issue.
  - name: How do I use the template?
    url: https://github.com/Syntek-Dev/syntek-media#readme
    about: The user guide.
EOF
}

# A file the script cannot read must stop the run with exit 2, never pass or mislead. Root reads a
# mode-000 file, so there the probe cannot be made: it is named as a SKIP, never counted.
probe_incomplete() { # $1 = label, $2 = fixture path to make unreadable, $3 = text the error must carry
  local label="$1" path="$2" expect="$3" rc=0 err
  chmod 000 "$path"
  if [[ -r "$path" ]]; then
    chmod 644 "$path"; skip_named "$label" "this user reads a mode-000 file, as root does"; return 0
  fi
  err="$( (run_checks) 2>&1 >/dev/null )" || rc=$?
  chmod 644 "$path"
  ST_PROBES=$((ST_PROBES + 1))
  if [[ $rc -eq 2 && "$err" == *"$expect"* ]]; then
    log "  ✓ $label"
  else
    ST_FAILS=$((ST_FAILS + 1))
    printf '\033[31m  ✗ %s exited %d, not 2: %s\033[0m\n' "$label" "$rc" "${err:-(no message)}"
  fi
}

self_test() {
  local tmp real_root="$SM_ROOT" real_holder="$LICENSE_HOLDER" r
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  r="$tmp/root"; SM_ROOT="$r"
  LICENSE_HOLDER="Morgan Example t/a Harbour Lane Studio"
  write_fixture "$r"
  st_baseline "a fixture root with every community file in order"

  # 1. Present, as files.
  rm "$r/SECURITY.md";                              probe "check 1 fires on a missing SECURITY.md" "check 1 — SECURITY.md is missing"
  write_fixture "$r"
  mv "$r/.github/CODEOWNERS" "$tmp/CODEOWNERS.real"; ln -s "$tmp/CODEOWNERS.real" "$r/.github/CODEOWNERS"
  probe "check 1 fires on a CODEOWNERS that is a link" "check 1 — .github/CODEOWNERS is a link"
  write_fixture "$r"; rm "$r/$CONFIG";              probe "check 1 fires on a missing config.yml, and check 4 leaves it alone" "check 1 — $CONFIG is missing"
  write_fixture "$r"; mv "$r/$FORMS_DIR" "$tmp/forms-elsewhere"; ln -s "$tmp/forms-elsewhere" "$r/$FORMS_DIR"
  probe "check 1 fires once on a linked ISSUE_TEMPLATE/ folder" "check 1 — $FORMS_DIR/ is a link"

  # 2. The licence, byte for byte.
  write_fixture "$r"; sed -i 's|t/a Harbour Lane Studio|Harbour Lane Studio Ltd|' "$r/LICENSE"
  probe "check 2 fires on a changed copyright holder, naming the line and column" "check 2 — LICENSE line 3 differs at column 35"
  write_fixture "$r"; sed -i 's/$/\r/' "$r/LICENSE"
  probe "check 2 fires on CRLF line endings" "check 2 — LICENSE has CRLF"
  write_fixture "$r"; printf '%s' "$(cat "$r/LICENSE")" > "$tmp/l"; mv "$tmp/l" "$r/LICENSE"
  probe "check 2 fires on a stripped final newline" "check 2 — LICENSE lacks its final newline"
  write_fixture "$r"; printf '\nSee CONTRIBUTING.md for the permission.\n' >> "$r/LICENSE"
  probe "check 2 fires on a permission appended to LICENSE" "check 2 — LICENSE carries more than the approved text"
  write_fixture "$r"; sed -i '1d' "$r/LICENSE"
  probe "check 2 fires on a LICENSE without its title" "check 2 — LICENSE line 1 differs at column 1"
  write_fixture "$r"; sed -i '5s/$/ /' "$r/LICENSE"
  probe "check 2 names a trailing space past the clipped width" "check 2 — LICENSE line 5 has trailing whitespace after column 76"
  write_fixture "$r"; { printf '\xef\xbb\xbf'; cat "$r/LICENSE"; } > "$tmp/l"; mv "$tmp/l" "$r/LICENSE"
  probe "check 2 names a byte-order mark" "check 2 — LICENSE begins with a byte-order mark"

  # 3. No Markdown in ISSUE_TEMPLATE/.
  write_fixture "$r"; printf '# CONTEXT.md — ISSUE_TEMPLATE/\n' > "$r/$FORMS_DIR/CONTEXT.md"
  probe "check 3 fires on a pair file in ISSUE_TEMPLATE/" "check 3 — $FORMS_DIR/CONTEXT.md is Markdown"

  # 4. Forms and config.
  write_fixture "$r"; sed -i '/^description:/d' "$r/$FORMS_DIR/bug_report.yml"
  probe "check 4 fires on a form whose description is only nested" "check 4 — $FORMS_DIR/bug_report.yml has no top-level description"
  write_fixture "$r"; sed -i 's/^name: Bug report$/name: ""/' "$r/$FORMS_DIR/bug_report.yml"
  probe "check 4 fires on an empty name" "check 4 — $FORMS_DIR/bug_report.yml has a top-level name with no value"
  write_fixture "$r"; sed -i 's/^name: Bug report$/name: ~/' "$r/$FORMS_DIR/bug_report.yml"
  probe "check 4 fires on a null name (~)" "check 4 — $FORMS_DIR/bug_report.yml has a top-level name with no value ('~' is YAML's null)"
  write_fixture "$r"; sed -i "s/^name: Bug report$/name: 'null'/" "$r/$FORMS_DIR/bug_report.yml"
  probe_clean "check 4 accepts a quoted 'null', which is a string"
  write_fixture "$r"; sed -i '/^body:/,$d' "$r/$FORMS_DIR/template_improvement.yml"; printf 'body:\n' >> "$r/$FORMS_DIR/template_improvement.yml"
  probe "check 4 fires on a body with no fields" "check 4 — $FORMS_DIR/template_improvement.yml has a top-level body that is not a list"
  write_fixture "$r"; sed -i '/^body:/,$d' "$r/$FORMS_DIR/template_improvement.yml"
  printf 'body:\n  type: dropdown\n  attributes:\n    options:\n      - a\n' >> "$r/$FORMS_DIR/template_improvement.yml"
  probe "check 4 fires on a body that is a mapping holding a list deeper down" "check 4 — $FORMS_DIR/template_improvement.yml has a top-level body that is not a list"
  write_fixture "$r"; printf 'name: Question\nlabels: [question]\nbody:\n  - type: textarea\n    id: q\n    attributes:\n      label: The question\n' > "$r/$FORMS_DIR/question.yml"
  probe "check 4 reads a further form, and fires on its missing description" "check 4 — $FORMS_DIR/question.yml has no top-level description"
  write_fixture "$r"; sed -i 's/^blank_issues_enabled: false$/blank_issues_enabled: true/' "$r/$CONFIG"
  probe "check 4 fires when blank issues are on" "check 4 — $CONFIG sets blank_issues_enabled to 'true'"
  write_fixture "$r"; sed -i "s/^blank_issues_enabled: false$/blank_issues_enabled: 'false'/" "$r/$CONFIG"
  probe "check 4 fires on a quoted 'false', which is a string" "check 4 — $CONFIG sets blank_issues_enabled to the quoted string 'false'"
  write_fixture "$r"; sed -i 's|syntek-media/security|syntek-author/security|' "$r/$CONFIG"
  probe "check 4 fires on a security link copied from another repository" "check 4 — $CONFIG has no contact link"
  write_fixture "$r"; sed -i 's|^\(    url: \)\(https://github.com/Syntek-Dev/syntek-media/security.*\)$|\1"\2" # quoted|' "$r/$CONFIG"
  sed -i 's/$/\r/' "$r/$CONFIG" "$r/$FORMS_DIR/bug_report.yml"
  probe_clean "a quoted url and CRLF line endings in the YAML are read"

  # 5. One address, in the Code of Conduct only.
  write_fixture "$r"; printf '\nOr write to security@example.invalid.\n' >> "$r/SECURITY.md"
  probe "check 5 fires on an address in SECURITY.md" "check 5 — SECURITY.md holds an email address (security@example.invalid)"
  write_fixture "$r"; sed -i 's/at conduct@example.invalid\./at conduct@example.invalid or deputy@example.invalid./' "$r/CODE_OF_CONDUCT.md"
  probe "check 5 fires on a second address in the Code of Conduct" "check 5 — CODE_OF_CONDUCT.md writes an email address 2 times"
  write_fixture "$r"; sed -i 's/^Examples include/Or write to CONDUCT@example.invalid. Examples include/' "$r/CODE_OF_CONDUCT.md"
  probe "check 5 fires on the same address written twice, in another case and section" "check 5 — CODE_OF_CONDUCT.md writes an email address 2 times (conduct@example.invalid)"
  write_fixture "$r"; sed -i 's|^      label: What happened$|      label: What happened\n      placeholder: reporter@example.invalid|' "$r/$FORMS_DIR/bug_report.yml"
  probe "check 5 fires on an address in an issue form" "check 5 — $FORMS_DIR/bug_report.yml holds an email address"
  write_fixture "$r"; printf '\nClone it: git clone git@github.com:Example-Owner/example.git, or\nssh://git@github.com/Example-Owner/example.git.\n' >> "$r/CONTRIBUTING.md"
  probe_clean "check 5 passes an SSH remote, which is not an address"

  # 6. SECURITY.md names the route.
  write_fixture "$r"; printf '# Security Policy\n\nOpen an issue.\n' > "$r/SECURITY.md"
  probe "check 6 fires when SECURITY.md names no private route" "check 6 — SECURITY.md names neither"
  write_fixture "$r"; printf "# Security Policy\n\nReport it only through GitHub's Private\nVulnerability Reporting.\n" > "$r/SECURITY.md"
  probe_clean "check 6 accepts the phrase alone, across a line break and in any case"
  write_fixture "$r"; printf '# Security Policy\n\n[Report it privately](%s).\n' "$SM_PRIVATE_REPORT_URL" > "$r/SECURITY.md"
  probe_clean "check 6 accepts this repository's advisories URL alone"

  # An unreadable file is an incomplete run.
  write_fixture "$r"
  probe_incomplete "an unreadable CONTRIBUTING.md stops the run with exit 2" "$r/CONTRIBUTING.md" "cannot read CONTRIBUTING.md"

  SM_ROOT="$real_root"; LICENSE_HOLDER="$real_holder"
  st_finish "a sound set of community files from a broken one"
}

for _sm_tool in awk cmp find grep paste tr; do command -v "$_sm_tool" >/dev/null 2>&1 || die "$_sm_tool is not installed"; done
unset _sm_tool
verify_approved_text
if $SELF_TEST; then
  self_test
  exit $?
fi

bold "▸ $SCRIPT_NAME — $SM_ROOT"
run_checks
if [[ ${#FINDINGS[@]} -eq 0 ]]; then
  bold "✓ $(wc -w <<< "$SM_COMMUNITY_FILES" | tr -d ' ') community files present; LICENSE is the approved MIT text; $FORMS_READ issue form(s) and config.yml well formed; at most one address, in CODE_OF_CONDUCT.md; SECURITY.md names private vulnerability reporting."
  exit 0
fi
bold "✗ ${#FINDINGS[@]} finding(s):"
print_findings
log ""
log "  DESIGN.md D83: the community files live at the repository root and never ship. LICENSE is"
log "  the family's MIT text alone; the one address is the Code of Conduct's; security reports go"
log "  only through $SM_PRIVATE_REPORT_URL."
exit 1

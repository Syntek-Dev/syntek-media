#!/usr/bin/env bash
#
# skill-conformance.sh — Verify every skill against DESIGN.md Section 5's contract.
#
#                        Skills are the only executable tier in a generated project (DESIGN.md
#                        D6: no agents, no commands), and a skill is chosen by its description
#                        alone. A description with no boundary competes for its neighbour's
#                        work; a body with no "Complete when" never knows it has finished; a
#                        shared skill without the mode paragraph never reads its mode file and
#                        applies one brand kind's procedure with no domain at all. Section 5
#                        states the contract once; this script holds every skill to it, and holds
#                        each mode file to the four headings that let the procedure find its
#                        additions. Two failures are media's own. A media skill that takes a
#                        syntek-author skill's name is a folder the two templates fight over on
#                        every update, and an update never stops on it (DESIGN.md Section 10). And
#                        an ElevenLabs call spends the author's credits: a skill that names a
#                        credit-spending tool without the guard sentence generates unasked, and one
#                        without an absolute output_directory scatters paid-for audio on the
#                        desktop (D21).
#
#                        Twenty-one checks:
#                          1. The skill folder has a SKILL.md.
#                          2. Frontmatter opens on line 1 with --- and is closed.
#                          3. `name` equals the folder name.
#                          4. `description` is present and at most 1,024 characters.
#                          5. `description` states a boundary: Not … (`other-skill`).
#                          6. No frontmatter key beyond name, description, context, agent,
#                             background, model, metadata.
#                          7. `context: fork` carries `agent:` (Explore, Plan or general-purpose)
#                             and `background:`.
#                          8. The H1 reads `# Skill: <Name> (<brand name token>)`.
#                          9. The locale line: Locale: en_GB · <timezone token> · dates DD/MM/YYYY.
#                         10. `## Governing procedures (route here — do not restate at length)`.
#                         11. Every step ends with a "Complete when:" (and there is a step).
#                         12. `## Anti-patterns`.
#                         13. `## Cross-references` is the last H2.
#                         14. A moded skill carries the mode paragraph verbatim, before step 1.
#                         15. A mode file's H2s are exactly: Paths and unit · Additions to the
#                             steps · Domain rules · Examples.
#                         16. The mode files match DESIGN.md: in template/, every mode a moded
#                             skill names and no other; in a render, exactly one; an unmoded skill
#                             carries none.
#                         17. SKILL.md plus its longest mode file stays within 300 lines.
#                         18. No .claude/agents/ or .claude/commands/ folder exists.
#                         19. The skill is one DESIGN.md Section 5.1 names.
#                         20. No media skill shares a name with a `skill` line of
#                             syntek-author-names.txt (DESIGN.md D27): a skill folder in the tree,
#                             and, in template/, every name the catalogue gives. The file is read
#                             on every run: a missing one is exit 2, never a SKIP. A folder this
#                             check claims is not also reported by check 19.
#                         21. A skill naming a credit-spending ElevenLabs tool (the nine `ask`
#                             entries of DESIGN.md D13) carries the guard sentence verbatim — "If
#                             nothing was asked, stop: never generate unasked, including as a
#                             'helpful' extra after another skill." — and the strings
#                             `output_directory` and `git rev-parse --show-toplevel` (Section 5).
#
#                        Run on template/ (the default) the H1 and locale line must carry the
#                        literal BRAND_NAME and TIMEZONE tokens; on a render, any value.
#
#                        Over-author scope (DESIGN.md Section 7): on a <kind>--over-author tree,
#                        whose <tree>.owned lists the files media's copy added, only media's skill
#                        folders are checked; syntek-author's are skipped and counted.
#
#                        Numbers are stable identifiers. Append, never renumber.
#
#                        What it CANNOT check: that a description's triggers are the right ones,
#                        or that a mode file's domain rules agree with its guide. Nor that a skill
#                        really waits for the author before a call: check 21 proves the words are
#                        there; a reviewer proves the steps keep them.
#
# SELF-TEST. --self-test writes a conformant moded skill, an unmoded one and an ElevenLabs one at
#            runtime, with a fixture names file, proves them clean, then applies one mutation per
#            check and asserts exactly one finding; then proves the over-author scope.
#
# Requirements: bash 4+, awk, grep, sed. No network.
#
# Usage: skill-conformance.sh [--root DIR] [--quiet] [--self-test] [--help] [<tree>...]
#        With no tree, checks template/ in the repository.
#
# Exit codes:  0 = every skill conforms
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, a tree that does not exist, no
#                  syntek-author-names.txt)

set -euo pipefail
SCRIPT_NAME="skill-conformance.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
TARGETS=()

usage() {
  cat <<'EOF'
skill-conformance.sh — Verify every skill against DESIGN.md Section 5's contract

Usage: skill-conformance.sh [--root DIR] [--quiet] [--self-test] [--help] [<tree>...]

  <tree>       A render (default: template/ in the repository)
  --root DIR   The template repository (default: this repository)
  --quiet      Print findings only
  --self-test  Prove the checks still fire against skills written at runtime
  --help       Show this message

A <tree>.owned file beside a tree (written by generate-all.sh) marks an over-author tree:
only media's skills are checked there.
Exit codes: 0 = conforms  1 = finding(s), or the self-test no longer separates
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
SOURCE=true
SKILLS_SEEN=0
AUTHOR_SKILLS_SKIPPED=0
GOVERNING="$SM_GOVERNING_LINE"
MODE_H2="$SM_MODE_H2S"
MODE_PARA="$SM_MODE_PARA"
GUARD="$SM_GUARD_SENTENCE"
ALLOWED_KEYS=" $SM_SKILL_KEYS "
FORK_AGENTS=" Explore Plan general-purpose "
declare -A CAT_GATE=() CAT_MODES=()
while read -r s g m; do [[ -n "$s" ]] && { CAT_GATE["$s"]="$g"; CAT_MODES["$s"]="$m"; }; done <<< "$SM_SKILLS"

frontmatter() { awk 'NR == 1 && $0 != "---" { exit } NR == 1 { next } /^---[[:space:]]*$/ { exit } { print }' "$1"; }
fm_closed()   { awk 'NR == 1 && $0 != "---" { exit 1 } NR > 1 && /^---[[:space:]]*$/ { found = 1; exit } END { exit !found }' "$1"; }
# Fenced lines (fences included) print as blank lines, so line numbers match the file and
# steps_of() agrees with mode_para_line(), which reads the file itself.
unfenced()    { awk '/^[[:space:]]*```/ { f = !f; print ""; next } f { print ""; next } { print }' "$1"; }

# The description as one string: inline, or a folded/literal block joined with spaces.
description_of() { # stdin = frontmatter
  awk '
    /^description:/ {
      v = $0; sub(/^description:[ \t]*/, "", v)
      if (v ~ /^[>|][-+]?[ \t]*$/) { block = 1; next }
      gsub(/^["\047]|["\047]$/, "", v); print v; done = 1; exit
    }
    block && /^[ \t]+/ { l = $0; sub(/^[ \t]+/, "", l); out = out (out == "" ? "" : " ") l; next }
    block { print out; done = 1; exit }
    END { if (!done && block && out != "") print out }'
}

# Steps: numbered items opening with bold, or numbered headings, outside the three closing
# sections. Prints "S<TAB>line<TAB>title<TAB>0|1" per step (1 = carries Complete when).
steps_of() {
  unfenced "$1" | awk '
    function close_step() { if (open) print "S\t" sline "\t" stitle "\t" complete; open = 0 }
    /^## / {
      close_step()
      excluded = ($0 ~ /^## (Governing procedures|Anti-patterns|Cross-references)/)
      if (!excluded && $0 ~ /^## (Step )?[0-9]+[.:)]? /) { open = 1; sline = NR; stitle = substr($0, 4); complete = 0 }
      next
    }
    excluded { next }
    /^### (Step )?[0-9]+[.:)]? / || /^[0-9]+\. \*\*/ { close_step(); open = 1; sline = NR; stitle = substr($0, 1, 50); complete = 0 }
    open && /Complete when:/ { complete = 1 }
    END { close_step() }'
}

mode_para_line() { # line number where the verbatim mode paragraph starts, or nothing
  awk -v want="$MODE_PARA" '
    function flush() { if (buf != "") { gsub(/[ \t]+/, " ", buf); sub(/^ /, "", buf); sub(/ $/, "", buf); if (buf == want) { print start; found = 1; exit } } buf = "" }
    /^[ \t]*>?[ \t]*$/ { flush(); next }
    { l = $0; sub(/^[ \t]*> ?/, "", l); if (buf == "") start = NR; buf = buf " " l }
    END { if (!found) flush() }' "$1"
}

# The file as one line: blockquote markers dropped, whitespace runs collapsed — so a sentence
# wrapped over several lines, or inside a list item or a quote, reads as written (check 21).
flat() { sed -E 's/^[[:space:]]*>[[:space:]]?//' "$1" | tr -s '[:space:]' ' '; }

# The credit-spending ElevenLabs tools a skill's files name (DESIGN.md D13, D21).
spending_tools_named() { # $1 = skill dir → one tool per line
  local t
  for t in "${SM_SETTINGS_ASK[@]}"; do
    grep -qF -- "$t" "$1"/*.md 2>/dev/null && printf '%s\n' "$t"
  done
  return 0
}

check_skill() { # $1 = folder name
  local s="$1" dir="$TREE/.claude/skills/$1" f fm desc k v n h2 last mode modes have want first_step para total longest text tools
  f="$dir/SKILL.md"
  SKILLS_SEEN=$((SKILLS_SEEN + 1))
  # ── 20, then 19. The name ───────────────────────────────────────────────────
  if [[ -n "${SM_AUTHOR_SKILL[$s]:-}" ]]; then
    finding "check 20 — .claude/skills/$s takes the name of a syntek-author skill (syntek-author-names.txt) — an update would overwrite one template's skill with the other's"
  elif [[ -z "${CAT_GATE[$s]:-}" ]]; then
    finding "check 19 — .claude/skills/$s is not a skill DESIGN.md Section 5.1 names"
  fi
  if [[ ! -f "$f" ]]; then finding "check 1 — .claude/skills/$s/ has no SKILL.md"; return 0; fi

  # ── 2–7. Frontmatter ────────────────────────────────────────────────────────
  if ! fm_closed "$f"; then
    finding "check 2 — $s/SKILL.md frontmatter does not open on line 1 with --- and close"
  else
    fm="$(frontmatter "$f")"
    v="$(awk '/^name:/ { v = $0; sub(/^name:[ \t]*/, "", v); gsub(/["\047]/, "", v); print v; exit }' <<< "$fm")"
    [[ "$v" == "$s" ]] || finding "check 3 — $s/SKILL.md says name: '${v}'; the folder is $s"
    desc="$(description_of <<< "$fm")"
    if [[ -z "$desc" ]]; then finding "check 4 — $s/SKILL.md has no description"
    elif [[ ${#desc} -gt 1024 ]]; then finding "check 4 — $s/SKILL.md description is ${#desc} characters; the limit is 1,024"; fi
    if [[ -n "$desc" ]] && ! grep -qE 'Not .*\(`[a-z0-9-]+`\)' <<< "$desc"; then
      finding "check 5 — $s/SKILL.md description states no boundary of the form Not … (\`other-skill\`)"
    fi
    while IFS= read -r k; do
      [[ "$ALLOWED_KEYS" == *" $k "* ]] || finding "check 6 — $s/SKILL.md frontmatter carries '$k', which this template does not admit"
    done < <(grep -oE '^[A-Za-z][A-Za-z0-9_-]*:' <<< "$fm" | tr -d ':')
    if grep -qE '^context:[[:space:]]*fork' <<< "$fm"; then
      v="$(awk '/^agent:/ { v = $0; sub(/^agent:[ \t]*/, "", v); print v; exit }' <<< "$fm")"
      [[ -n "$v" && "$FORK_AGENTS" == *" $v "* ]] || finding "check 7 — $s/SKILL.md forks without an admitted agent: (Explore, Plan or general-purpose)"
      grep -q '^background:' <<< "$fm" || finding "check 7 — $s/SKILL.md forks without background:"
    fi
  fi

  # ── 8–13. Body ──────────────────────────────────────────────────────────────
  if $SOURCE; then
    grep -qE "^# Skill: .+ \\($SM_SKILL_H1_TOKEN\\)\$" "$f" || finding "check 8 — $s/SKILL.md has no H1 '# Skill: <Name> ($SM_SKILL_H1_TOKEN)'"
    grep -qE 'Locale:.*en_GB.*<%TIMEZONE%>.*DD/MM/YYYY' "$f" || finding "check 9 — $s/SKILL.md has no locale line (en_GB · <%TIMEZONE%> · dates DD/MM/YYYY)"
  else
    grep -qE '^# Skill: .+ \(.+\)$' "$f" || finding "check 8 — $s/SKILL.md has no H1 '# Skill: <Name> (<brand>)'"
    grep -qE 'Locale:.*en_GB.*DD/MM/YYYY' "$f" || finding "check 9 — $s/SKILL.md has no locale line (en_GB · timezone · dates DD/MM/YYYY)"
  fi
  grep -qxF "$GOVERNING" "$f" || finding "check 10 — $s/SKILL.md has no '$GOVERNING'"
  n=0; first_step=""
  while IFS=$'\t' read -r _ line title complete; do
    [[ -z "$line" ]] && continue
    n=$((n + 1)); [[ -z "$first_step" ]] && first_step="$line"
    [[ "$complete" == 1 ]] || finding "check 11 — $s/SKILL.md step '${title:0:40}' (line $line) has no 'Complete when:'"
  done < <(steps_of "$f")
  [[ "$n" -gt 0 ]] || finding "check 11 — $s/SKILL.md has no numbered steps"
  h2="$(unfenced "$f" | { grep '^## ' || true; } | sed 's/[[:space:]]*$//')"
  grep -qx '## Anti-patterns' <<< "$h2" || finding "check 12 — $s/SKILL.md has no '## Anti-patterns'"
  last="$(tail -1 <<< "$h2")"
  [[ "$last" == '## Cross-references' ]] || finding "check 13 — $s/SKILL.md does not end with '## Cross-references' (last H2: '${last}')"

  # ── 14–17. Modes ────────────────────────────────────────────────────────────
  modes="${CAT_MODES[$s]:--}"
  have=()
  for mode in $SM_MODE_FILES; do [[ -f "$dir/$mode" ]] && have+=("$mode"); done
  if [[ "$modes" != - || ${#have[@]} -gt 0 ]]; then
    para="$(mode_para_line "$f")"
    if [[ -z "$para" ]]; then finding "check 14 — $s/SKILL.md is moded but does not carry the mode paragraph verbatim (DESIGN.md Section 5)"
    elif [[ -n "$first_step" && "$para" -gt "$first_step" ]]; then finding "check 14 — $s/SKILL.md carries the mode paragraph after step 1"; fi
  fi
  longest=0
  for mode in "${have[@]}"; do
    h2="$(unfenced "$dir/$mode" | { grep '^## ' || true; } | sed 's/^## //; s/[[:space:]]*$//' | paste -sd'|' -)"
    [[ "$h2" == "$MODE_H2" ]] || finding "check 15 — $s/$mode has H2s '${h2:-none}'; expected '$MODE_H2'"
    n="$(wc -l < "$dir/$mode")"; [[ "$n" -gt "$longest" ]] && longest="$n"
  done
  if [[ "$modes" == - ]]; then
    [[ ${#have[@]} -eq 0 ]] || finding "check 16 — $s is unmoded (DESIGN.md Section 5.1) but carries ${have[*]}"
  elif $SOURCE; then
    want="$(modes_list "$modes")"
    for mode in $want; do [[ -f "$dir/$mode" ]] || finding "check 16 — $s is moded but $mode is missing"; done
    for mode in "${have[@]}"; do [[ " $want " == *" $mode "* ]] || finding "check 16 — $s carries $mode, a mode DESIGN.md does not give it"; done
  else
    [[ ${#have[@]} -eq 1 ]] || finding "check 16 — $s carries ${#have[@]} mode file(s) in a render; exactly one ships"
  fi
  total=$(( $(wc -l < "$f") + longest ))
  [[ "$total" -le 300 ]] || finding "check 17 — $s/SKILL.md plus its longest mode file is $total lines; the cap is 300"

  # ── 21. The ElevenLabs guard ────────────────────────────────────────────────
  tools="$(spending_tools_named "$dir" | paste -sd' ' -)"
  if [[ -n "$tools" ]]; then
    text="$(flat "$f")"
    [[ "$text" == *"$GUARD"* ]] || finding "check 21 — $s names ${tools%% *} but its SKILL.md lacks the guard sentence verbatim (\"$GUARD\")"
    [[ "$text" == *output_directory* ]] || finding "check 21 — $s names ${tools%% *} but its SKILL.md never says output_directory — the server saves to the desktop without one (D21)"
    [[ "$text" == *'git rev-parse --show-toplevel'* ]] || finding "check 21 — $s names ${tools%% *} but its SKILL.md does not resolve the absolute output_directory with git rev-parse --show-toplevel"
  fi
}

run_checks() {
  FINDINGS=()
  SKILLS_SEEN=0
  AUTHOR_SKILLS_SKIPPED=0
  local d p s g m
  for d in agents commands; do
    if $SM_OWNED_MODE; then
      for p in "${!SM_OWNED[@]}"; do
        if [[ "$p" == ".claude/$d/"* ]]; then finding "check 18 — .claude/$d/ ships with media; this template ships skills only (DESIGN.md D6)"; break; fi
      done
    elif [[ -e "$TREE/.claude/$d" ]]; then
      finding "check 18 — .claude/$d/ exists; this template ships skills only (DESIGN.md D6)"
    fi
  done
  # The catalogue's own names, in template/: a collision designed in before any folder exists.
  if $SOURCE; then
    while read -r s g m; do
      [[ -z "$s" || -d "$TREE/.claude/skills/$s" ]] && continue
      [[ -n "${SM_AUTHOR_SKILL[$s]:-}" ]] && finding "check 20 — DESIGN.md Section 5.1 names the skill $s, which is a syntek-author skill (syntek-author-names.txt)"
    done <<< "$SM_SKILLS"
  fi
  [[ -d "$TREE/.claude/skills" ]] || return 0
  while IFS= read -r d; do
    if $SM_OWNED_MODE && ! is_owned_dir ".claude/skills/$d"; then
      AUTHOR_SKILLS_SKIPPED=$((AUTHOR_SKILLS_SKIPPED + 1)); continue
    fi
    check_skill "$d"
  done < <(find "$TREE/.claude/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | LC_ALL=C sort)
}

# ── Self-test ────────────────────────────────────────────────────────────────

write_skill() { # $1 = dir, $2 = name, $3 = moded (true|false), $4 = names a spending tool (true|false)
  local d="$1" s="$2" m
  mkdir -p "$d"
  {
    printf -- '---\nname: %s\ndescription: >-\n  Do one media job well, on the author'"'"'s word. Use when asked to %s. Not for captions\n  (`captions`).\n---\n\n' "$s" "$s"
    printf '# Skill: %s (<%%BRAND_NAME%%>)\n\nLocale: en_GB · <%%TIMEZONE%%> · dates DD/MM/YYYY.\n\n' "$s"
    printf '%s\n\n- `.claude/rules/syntek-media/03-production-ethics.md`\n\n' "$GOVERNING"
    if [[ "$3" == true ]]; then
      printf '> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of\n'
      printf '> `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the\n'
      printf '> domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure.\n'
      printf '> Where they disagree, the procedure wins and the disagreement is reported to the author.\n\n'
    fi
    printf '## Steps\n\n1. **Read the brief.** Read it. *Complete when:* it is read.\n'
    if [[ "$4" == true ]]; then
      printf '2. **Generate one segment.** Only when the author asked for audio.\n'
      printf "   If nothing was asked, stop: never generate unasked, including as a 'helpful' extra\n"
      printf '   after another skill. Call `mcp__elevenlabs__text_to_speech` once, with\n'
      printf '   `output_directory` set to the absolute path of the generated/ folder under the root\n'
      printf '   (`git rev-parse --show-toplevel`). *Complete when:* the take is renamed.\n\n'
    else
      printf '2. **Do the work.** Do it. *Complete when:* it is done.\n\n'
    fi
    printf '## Anti-patterns\n\n- Rewriting what was not asked for.\n\n## Cross-references\n\n- `.claude/rules/syntek-media/02-skills.md`\n'
  } > "$d/SKILL.md"
  if [[ "$3" == true ]]; then
    for m in $SM_MODE_FILES; do
      printf '# %s — %s\n\n## Paths and unit\n\nx\n\n## Additions to the steps\n\nx\n\n## Domain rules\n\nx\n\n## Examples\n\nx\n' "$m" "$s" > "$d/$m"
    done
  fi
}

self_test() {
  local tmp sk ws ca vo real_names="$SM_AUTHOR_NAMES_FILE"
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  SM_AUTHOR_NAMES_FILE="$tmp/names.txt"
  printf '# fixture names\ntop .claude\ntop manuscript\nclaude skills\nskill run-workflow\nskill spelling\nrules 01-layout-and-routing.md\n' > "$SM_AUTHOR_NAMES_FILE"
  require_author_names
  TREE="$tmp/template"; SOURCE=true; load_owned "$TREE"
  sk="$TREE/.claude/skills"; ws="$sk/write-script"; ca="$sk/captions"; vo="$sk/voiceover"
  write_skill "$ws" write-script true false
  write_skill "$ca" captions false false
  write_skill "$vo" voiceover true true
  st_baseline "a moded skill, an unmoded one and an ElevenLabs one, all conformant"

  # Shapes the checks must not flag: a block description read once (not twice, which doubled
  # its length), a fenced block above the mode paragraph (line numbers must still agree), and a
  # free ElevenLabs tool, which spends nothing and needs no guard.
  cp "$ca/SKILL.md" "$tmp/h"
  sed -i "s/^  Do one media job well/  $(printf 'word %.0s' $(seq 1 110))Do one media job well/; s/^  (\`captions\`)\.\$/&\nmodel: opus/" "$ca/SKILL.md"
  probe_clean "a 670-character block description followed by a key is read once and passes check 4"; cp "$tmp/h" "$ca/SKILL.md"
  cp "$ws/SKILL.md" "$tmp/h"
  awk -v blk="$(printf '```text\n%s\n```' "$(seq 1 12)")" '/^> \*\*Mode\./ && !d { print blk; print ""; d = 1 } { print }' "$tmp/h" > "$ws/SKILL.md"
  probe_clean "a fenced block above the mode paragraph keeps steps and paragraph on the same numbering"; cp "$tmp/h" "$ws/SKILL.md"
  cp "$ca/SKILL.md" "$tmp/h"
  printf -- '- Find the model with `mcp__elevenlabs__list_models` (free).\n' >> "$ca/SKILL.md"
  probe_clean "a skill naming only a free ElevenLabs tool needs no guard"; cp "$tmp/h" "$ca/SKILL.md"

  mv "$ca/SKILL.md" "$tmp/h"; probe "check 1 fires on a skill with no SKILL.md" "check 1"; mv "$tmp/h" "$ca/SKILL.md"
  cp "$ca/SKILL.md" "$tmp/h"
  sed -i '1d' "$ca/SKILL.md";                                   probe "check 2 fires on frontmatter that does not open" "check 2"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i 's/^name: captions/name: caption/' "$ca/SKILL.md";     probe "check 3 fires on a name that is not the folder" "check 3"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i "s/^  Do one media job well/  $(printf 'word %.0s' $(seq 1 210))Do one media job well/" "$ca/SKILL.md"; probe "check 4 fires on a description over 1,024 characters" "check 4"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i 's/Not for captions/For captions/' "$ca/SKILL.md";     probe "check 5 fires on a description with no boundary" "check 5"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i 's/^name: captions/name: captions\neffort: high/' "$ca/SKILL.md"; probe "check 6 fires on a key the template does not admit" "check 6"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i 's/^name: captions/name: captions\ncontext: fork\nbackground: false/' "$ca/SKILL.md"; probe "check 7 fires on a fork with no agent" "check 7"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i 's/^# Skill: captions .*/# captions/' "$ca/SKILL.md"; probe "check 8 fires on the wrong H1" "check 8"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i 's/(<%BRAND_NAME%>)$/(<%OWNER_NAME%>)/' "$ca/SKILL.md"; probe "check 8 fires on an H1 naming the owner, not the brand" "check 8"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i '/^Locale:/d' "$ca/SKILL.md";                          probe "check 9 fires on a missing locale line" "check 9"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i 's/^## Governing procedures.*/## Governing procedures/' "$ca/SKILL.md"; probe "check 10 fires on a shortened governing heading" "check 10"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i 's/Do it\. \*Complete when:\* it is done\./Do it./' "$ca/SKILL.md"; probe "check 11 fires on a step with no Complete when" "check 11"; cp "$tmp/h" "$ca/SKILL.md"
  sed -i 's/^## Anti-patterns/## Pitfalls/' "$ca/SKILL.md";    probe "check 12 fires on a missing Anti-patterns" "check 12"; cp "$tmp/h" "$ca/SKILL.md"
  printf '\n## Notes\n\nA trailing section.\n' >> "$ca/SKILL.md"; probe "check 13 fires when Cross-references is not last" "check 13"; cp "$tmp/h" "$ca/SKILL.md"
  cp "$ws/SKILL.md" "$tmp/h"
  sed -i 's/^> Where they disagree, the procedure wins/> Where they disagree, the mode wins/' "$ws/SKILL.md"; probe "check 14 fires on an edited mode paragraph" "check 14"; cp "$tmp/h" "$ws/SKILL.md"
  sed -i 's/brand-kind mode file/doc-type mode file/' "$ws/SKILL.md"
  probe "check 14 fires on syntek-author's mode paragraph, names unswapped" "check 14"; cp "$tmp/h" "$ws/SKILL.md"
  cp "$ws/FICTION.md" "$tmp/h"
  sed -i 's/^## Domain rules/## Rules/' "$ws/FICTION.md";      probe "check 15 fires on a renamed mode H2" "check 15"; cp "$tmp/h" "$ws/FICTION.md"
  mv "$ws/NONFICTION.md" "$tmp/h";                              probe "check 16 fires on a missing mode file" "check 16"; mv "$tmp/h" "$ws/NONFICTION.md"
  cp "$ws/SKILL.md" "$tmp/h"
  seq 1 290 | sed 's/^/- cross-reference /' >> "$ws/SKILL.md"; probe "check 17 fires when a skill and its mode pass 300 lines" "check 17"; cp "$tmp/h" "$ws/SKILL.md"
  mkdir -p "$TREE/.claude/commands";                            probe "check 18 fires on a commands folder" "check 18"; rmdir "$TREE/.claude/commands"
  write_skill "$sk/make-a-meme" make-a-meme false false;        probe "check 19 fires on a skill DESIGN.md does not name" "check 19"; rm -rf "$sk/make-a-meme"
  write_skill "$sk/spelling" spelling false false;              probe "check 20 fires on a media skill named as a syntek-author skill" "check 20 — .claude/skills/spelling takes the name"; rm -rf "$sk/spelling"
  printf 'skill storyboard\n' >> "$SM_AUTHOR_NAMES_FILE"; require_author_names
  probe "check 20 fires when the catalogue names a syntek-author skill" "check 20 — DESIGN.md Section 5.1 names the skill storyboard"
  sed -i '/^skill storyboard$/d' "$SM_AUTHOR_NAMES_FILE"; require_author_names
  cp "$vo/SKILL.md" "$tmp/h"
  sed -i "s/stop: never generate unasked/stop: do not generate unasked/" "$vo/SKILL.md"
  probe "check 21 fires when the guard sentence is reworded" "check 21 — voiceover names mcp__elevenlabs__text_to_speech but its SKILL.md lacks the guard"; cp "$tmp/h" "$vo/SKILL.md"
  sed -i 's/`output_directory`/the folder/' "$vo/SKILL.md"
  probe "check 21 fires when no output_directory is passed" "check 21 — voiceover names mcp__elevenlabs__text_to_speech but its SKILL.md never says output_directory"; cp "$tmp/h" "$vo/SKILL.md"
  sed -i 's/(`git rev-parse --show-toplevel`)/(the root)/' "$vo/SKILL.md"
  probe "check 21 fires when the root is not resolved with git" "check 21 — voiceover names mcp__elevenlabs__text_to_speech but its SKILL.md does not resolve"; cp "$tmp/h" "$vo/SKILL.md"

  # The over-author scope: syntek-author's skills beside media's, and .owned listing media's.
  SOURCE=false
  sed -i 's/(<%BRAND_NAME%>)$/(Probe Studio)/; s/<%TIMEZONE%>/Europe\/London/' "$ws/SKILL.md" "$ca/SKILL.md" "$vo/SKILL.md"
  rm -f "$ws/FICTION.md" "$ws/NONFICTION.md" "$vo/FICTION.md" "$vo/NONFICTION.md"
  mkdir -p "$sk/spelling" "$sk/run-workflow"; printf '# not a media skill\n' > "$sk/spelling/SKILL.md"; printf -- '---\nname: x\n---\n' > "$sk/run-workflow/SKILL.md"
  (cd "$TREE" && find .claude/skills -type f | grep -vE '^\.claude/skills/(spelling|run-workflow)/' | LC_ALL=C sort) > "$TREE.owned"
  load_owned "$TREE"
  st_baseline "an over-author tree: syntek-author's skills beside media's rendered ones"
  printf '\n## Notes\n\nA trailing section.\n' >> "$ca/SKILL.md"
  probe "check 13 still fires on a media skill, over syntek-author" "check 13 — captions/SKILL.md"
  rm -f "$TREE.owned"; SM_OWNED_MODE=false; SM_OWNED=()

  SM_AUTHOR_NAMES_FILE="$real_names"
  st_finish "conformant skills from broken ones"
}

if $SELF_TEST; then
  self_test
  exit $?
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  [[ -d "$SM_ROOT/template" ]] || die "no template/ directory at $SM_ROOT, and no tree given"
  TARGETS=("$SM_ROOT/template")
fi
require_author_names

bold "▸ $SCRIPT_NAME"
STATUS=0
for target in "${TARGETS[@]}"; do
  [[ -d "$target" ]] || die "not a directory: $target"
  TREE="$(cd "$target" && pwd)"
  SOURCE=false; [[ "$TREE" == "$(cd "$SM_ROOT/template" 2>/dev/null && pwd)" ]] && SOURCE=true
  load_owned "$TREE"
  run_checks
  scope=""; $SM_OWNED_MODE && scope=" (over syntek-author: $AUTHOR_SKILLS_SKIPPED syntek-author skill(s) skipped)"
  if [[ ${#FINDINGS[@]} -eq 0 && "$SKILLS_SEEN" -eq 0 ]]; then
    log "  ✓ $TREE — no media skill folder under .claude/skills/: nothing to check (clean by absence, not by inspection)$scope"
  elif [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $TREE — $SKILLS_SEEN skill(s) conform$scope"
  else
    bold "✗ $TREE — ${#FINDINGS[@]} finding(s) across $SKILLS_SEEN skill(s)$scope:"
    print_findings
    STATUS=1
  fi
done
log ""
if [[ "$STATUS" -eq 0 ]]; then
  bold "✓ Every skill meets DESIGN.md Section 5's contract, takes no syntek-author name, and guards every paid call."
  exit 0
fi
log "  The contract: DESIGN.md Section 5 (frontmatter, body, the mode paragraph, the four mode H2s,"
log "  the ElevenLabs guard); the names: syntek-author-names.txt (D27)."
exit 1

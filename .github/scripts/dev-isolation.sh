#!/usr/bin/env bash
#
# dev-isolation.sh — Verify the template's own skills cannot fire while the template is built.
#
#                    template/.claude/ is a live Claude Code configuration that happens to sit
#                    inside this repository. Claude Code loads a nested .claude/skills/ folder the
#                    first time it reads a file beneath it, and nested CLAUDE.md files on demand.
#                    So a session building the template would, the moment it opened a skill to
#                    edit it, be offered `voiceover` and `captions` as tools — and the one thing
#                    a development session must never do is spend ElevenLabs credits on a
#                    template's behalf. A generated project's rules ("never generate unasked",
#                    the production loop) would start governing work on the template itself.
#                    `_subdirectory` keeps template/ out of renders; it does nothing for
#                    development sessions.
#
#                    Three layers in the ROOT .claude/settings.json close that (DESIGN.md
#                    Section 7): permissions.deny lists Skill(<name>) for every template skill —
#                    the ten of Section 5.1 — and an unqualified deny also blocks the nested
#                    template:<name> form; skillOverrides sets each of them "off", which hides it
#                    from the session's skill list as well; claudeMdExcludes keeps the generated
#                    project's manuals out.
#
#                    Seven checks:
#                      1. The root .claude/settings.json exists and is valid JSON.
#                      2. Every skill folder under template/.claude/skills/ is denied as
#                         Skill(<name>).
#                      3. Every skill DESIGN.md Section 5.1 names is denied too, so a skill is
#                         isolated before its folder is written.
#                      4. claudeMdExcludes carries "**/template/**/CLAUDE.md" and
#                         "**/template/.claude/**".
#
#                      5. The development Codex config is valid TOML, carries no [[skills.config]]
#                         (a project file's is ignored by Codex 0.160.1, so a row there is false
#                         assurance), and enables no product manual fallback (D73).
#                      6. Development AGENTS.md and GEMINI.md route to the development manual;
#                         .agents is a real folder, never a link (Codex's sandbox refuses a
#                         read-only link, D76), holding its pair and, only where the
#                         development .claude/skills exists, skills -> ../.claude/skills;
#                         nothing else, so it never exposes template/.claude (D73, D76).
#                      7. Every skill checks 2 and 3 cover is set "off" in skillOverrides, so it
#                         is hidden from the session's skill list, not only refused (D76).
#
#                    Numbers are stable identifiers. Append, never renumber.
#
#                    What it CANNOT check: that a client honours these settings. Native
#                    Antigravity and authenticated Codex sessions are not run in CI.
#                    Claude Code behaviour requires a live session: A deny rule
#                    refuses the Skill call; it does not hide the skill. Claude Code's skills
#                    documentation says so, and a 2.1.289 session (04/10/2026) showed it: once
#                    a file under template/ was read, all ten were listed "from
#                    template/.claude/skills", some with their full descriptions. A
#                    skillOverrides "off" entry hides a skill (Claude Code settings reference,
#                    read 14/10/2026); check 7 proves the entries are present, not that a
#                    session honours them. A deny on the bare name covers the nested, directory-qualified form
#                    only from Claude Code 2.1.260. Proving the refusal needs a live session,
#                    and CI holds no credentials for one. After any Claude Code upgrade that
#                    touches skill discovery, run this probe by hand. Start
#                    `claude -p --strict-mcp-config` (no MCP server, so nothing can spend) from
#                    the repository ROOT: inside template/ the product's own settings apply,
#                    not these. Have it read a file under template/, ask it to invoke one
#                    template skill, and confirm the call is refused.
#
# SELF-TEST. --self-test writes a fixture repository at runtime, proves it clean, then applies
#            one mutation per check and asserts exactly one finding each.
#
# Requirements: bash 4+, python3. No network.
#
# Usage: dev-isolation.sh [--root DIR] [--quiet] [--self-test] [--help]
#
# Exit codes:  0 = every template skill is isolated from development sessions
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, no python3)

set -euo pipefail
SCRIPT_NAME="dev-isolation.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false

usage() {
  cat <<'EOF'
dev-isolation.sh — Verify the template's own skills cannot fire while the template is built

Usage: dev-isolation.sh [--root DIR] [--quiet] [--self-test] [--help]

  --root DIR   The template repository (default: this repository)
  --quiet      Print findings only
  --self-test  Prove the checks still fire against a fixture written at runtime
  --help       Show this message

Exit codes: 0 = isolated  1 = finding(s), or the self-test no longer separates
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

SETTINGS="$SM_ROOT/.claude/settings.json"
SKILLS="$SM_ROOT/template/.claude/skills"
EXCLUDES=("**/template/**/CLAUDE.md" "**/template/.claude/**")
ON_DISK=0

# Prints "D<TAB>entry" per deny entry, "X<TAB>pattern" per claudeMdExcludes entry and
# "O<TAB>name=value" per skillOverrides entry, or
# "E<TAB>reason" when the file is not valid JSON.
read_settings() {
  python3 - "$SETTINGS" <<'PY'
import json, sys
try:
    data = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as exc:
    print(f"E\t{exc.__class__.__name__}: {exc}"); sys.exit(0)
for d in ((data.get("permissions") or {}).get("deny") or []):
    print(f"D\t{d}")
for x in (data.get("claudeMdExcludes") or []):
    print(f"X\t{x}")
for name, value in (data.get("skillOverrides") or {}).items():
    print(f"O\t{name}={value}")
PY
}

run_checks() {
  FINDINGS=()
  ON_DISK=0
  local kind val s x
  local -A denied=() excluded=() on_disk=() hidden=()
  if [[ ! -f "$SETTINGS" ]]; then
    finding "check 1 — there is no .claude/settings.json at the repository root — nothing isolates the template's skills"
    return 0
  fi
  while IFS=$'\t' read -r kind val; do
    case "$kind" in
      E) finding "check 1 — .claude/settings.json is not valid JSON ($val)"; return 0 ;;
      D) denied["$val"]=1 ;;
      X) excluded["$val"]=1 ;;
      O) [[ "${val#*=}" == off ]] && hidden["${val%%=*}"]=1 ;;
    esac
  done < <(read_settings)

  if [[ -d "$SKILLS" ]]; then
    while IFS= read -r s; do
      on_disk["$s"]=1; ON_DISK=$((ON_DISK + 1))
      [[ -n "${denied["Skill($s)"]:-}" ]] || finding "check 2 — template skill $s is not denied as Skill($s) — it can fire in a development session"
      [[ -n "${hidden[$s]:-}" ]] || finding "check 7 — template skill $s is not set off in skillOverrides — it is listed in a development session"
    done < <(find "$SKILLS" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | LC_ALL=C sort)
  fi
  while read -r s _; do
    [[ -z "$s" || -n "${on_disk[$s]:-}" ]] && continue
    [[ -n "${denied["Skill($s)"]:-}" ]] || finding "check 3 — DESIGN.md names the skill $s, and it is not denied — it would fire the day its folder lands"
    [[ -n "${hidden[$s]:-}" ]] || finding "check 7 — DESIGN.md names the skill $s, and it is not set off in skillOverrides"
  done <<< "$SM_SKILLS"
  for x in "${EXCLUDES[@]}"; do
    [[ -n "${excluded[$x]:-}" ]] || finding "check 4 — claudeMdExcludes does not carry \"$x\""
  done

  local problem
  problem="$(python3 - "$SM_ROOT" <<'PYCLIENT'
from pathlib import Path
import sys, tomllib
root = Path(sys.argv[1])
try:
    data = tomllib.loads((root / '.codex/config.toml').read_text())
    if data.get('skills', {}).get('config'):
        print('[[skills.config]] in a project file is ignored by Codex (user and -c layers only);'
              ' document the user-level SKILL.md rule in .codex/CLAUDE.md instead')
    elif data.get('project_doc_fallback_filenames'):
        print('no product instruction fallback is allowed')
except (OSError, ValueError, TypeError, AttributeError) as error:
    print('invalid development Codex configuration: ' + str(error).splitlines()[0])
PYCLIENT
)"
  [[ -z "$problem" ]] || finding "check 5 — $problem"
  problem="$(python3 - "$SM_ROOT" <<'PYCLIENT'
from pathlib import Path
import os, sys
root = Path(sys.argv[1])
def first_problem():
    agents = (root / 'AGENTS.md').read_text()
    gemini = (root / 'GEMINI.md').read_text()
    if ('.claude/CLAUDE.md' not in agents or 'DESIGN.md' not in agents
            or 'AGENTS.md' not in gemini):
        return 'development entrypoints must route to the manual'
    folder = root / '.agents'
    if folder.is_symlink() or not folder.is_dir():
        return ('.agents must be a real folder, never a link: Codex refuses a read-only path'
                ' that is a link to a writable folder (D76)')
    entries = {e.name for e in os.scandir(folder)}
    missing = sorted({'CONTEXT.md', 'CLAUDE.md'} - entries)
    if missing:
        return '.agents lacks its pair: ' + ', '.join(missing)
    allowed = {'CONTEXT.md', 'CLAUDE.md'}
    dev_skills = root / '.claude/skills'
    if dev_skills.is_dir() and not dev_skills.is_symlink():
        allowed.add('skills')
        link = folder / 'skills'
        if not link.is_symlink() or os.readlink(link) != '../.claude/skills':
            return '.agents/skills must link to ../.claude/skills, the development skill tree'
    extra = sorted(entries - allowed)
    if extra:
        return ('.agents holds ' + ', '.join(extra) + '; it may hold only its pair'
                + (' and the skills link' if 'skills' in allowed
                   else ' (the development .claude has no skills)'))
    return ''
try:
    found = first_problem()
    if found:
        print(found)
except OSError as error:
    print('missing development entrypoint or agent folder: ' + (error.strerror or str(error)))
PYCLIENT
)"
  [[ -z "$problem" ]] || finding "check 6 — $problem"

}

self_test() {
  local tmp real_root="$SM_ROOT" s
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  SM_ROOT="$tmp"; SETTINGS="$tmp/.claude/settings.json"; SKILLS="$tmp/template/.claude/skills"
  mkdir -p "$tmp/.claude" "$SKILLS/voiceover" "$SKILLS/captions"
  write_settings() { # $1 = names to leave out of deny, $2 = excludes JSON, $3 = names left on
    local first=true
    {
      printf '{\n  "claudeMdExcludes": %s,\n  "permissions": {"deny": [' "$2"
      while read -r s _; do
        [[ -z "$s" || " $1 " == *" $s "* ]] && continue
        $first || printf ', '; first=false
        printf '"Skill(%s)"' "$s"
      done <<< "$SM_SKILLS"
      printf ']},\n  "skillOverrides": {'
      first=true
      while read -r s _; do
        [[ -z "$s" ]] && continue
        $first || printf ', '; first=false
        if [[ " ${3:-} " == *" $s "* ]]; then printf '"%s": "on"' "$s"; else printf '"%s": "off"' "$s"; fi
      done <<< "$SM_SKILLS"
      printf '}\n}\n'
    } > "$SETTINGS"
  }
  local ok='["**/template/**/CLAUDE.md", "**/template/.claude/**"]'
  write_settings "" "$ok"
  mkdir -p "$tmp/.codex"
  write_clients() {
    python3 - "$tmp" "$SM_SKILLS" <<'PYCLIENT'
from pathlib import Path
import shutil, sys
root = Path(sys.argv[1])
(root / 'AGENTS.md').write_text('Read .claude/CLAUDE.md and DESIGN.md for development.\n')
(root / 'GEMINI.md').write_text('Read root AGENTS.md for development.\n')
folder = root / '.agents'
if folder.is_symlink() or folder.is_file(): folder.unlink()
elif folder.is_dir(): shutil.rmtree(folder)
folder.mkdir()
(folder / 'CONTEXT.md').write_text('# CONTEXT.md — .agents/\n')
(folder / 'CLAUDE.md').write_text('# CLAUDE.md — .agents/\n')
if (root / '.claude/skills').is_dir(): shutil.rmtree(root / '.claude/skills')
(root / '.codex/config.toml').write_text('# Development settings for Codex.\n')
PYCLIENT
  }
  write_clients
  st_baseline "a root settings file that denies every skill"

  printf '{ "permissions": ' > "$SETTINGS";                         probe "check 1 fires on settings that are not JSON" "check 1"
  write_settings "captions" "$ok";                                    probe "check 2 fires when a skill on disk is not denied" "check 2 — template skill captions"
  write_settings "narrate-audiobook" "$ok";                           probe "check 3 fires when a catalogued skill is not denied" "check 3 — DESIGN.md names the skill narrate-audiobook"
  write_settings "" '["**/template/**/CLAUDE.md"]';                   probe "check 4 fires when an exclusion is lost" "check 4"
  write_settings "" "$ok" "captions";                                 probe "check 7 fires when a skill on disk is left on" "check 7 — template skill captions"
  write_settings "" "$ok" "narrate-audiobook";                        probe "check 7 fires when a catalogued skill is left on" "check 7 — DESIGN.md names the skill narrate-audiobook"
  write_settings "" "$ok"

  write_settings "" "$ok"
  printf 'bad = [' > "$tmp/.codex/config.toml"; probe "check 5 fires on invalid Codex TOML" "check 5"
  write_clients
  printf "[[skills.config]]\npath = '../template/.claude/skills/voiceover/SKILL.md'\nenabled = false\n" >> "$tmp/.codex/config.toml"
  probe "check 5 fires on an inert project skills.config row" "check 5 — [[skills.config]]"
  write_clients
  printf "project_doc_fallback_filenames = ['CLAUDE.md']\n" | cat - "$tmp/.codex/config.toml" > "$tmp/fallback.toml"
  mv "$tmp/fallback.toml" "$tmp/.codex/config.toml"
  probe "check 5 fires on a development product-manual fallback" "check 5"
  write_clients; rm "$tmp/GEMINI.md"
  probe "check 6 fires on a missing development entrypoint" "check 6"
  write_clients; rm -rf "$tmp/.agents"; ln -s .claude "$tmp/.agents"
  probe "check 6 fires on the 0.4.1 development link .agents -> .claude (D76)" "check 6 — .agents must be a real folder"
  write_clients; rm -rf "$tmp/.agents"; ln -s template/.claude "$tmp/.agents"
  probe "check 6 fires when the development alias exposes product skills" "check 6 — .agents must be a real folder"
  write_clients; ln -s ../template/.claude/skills "$tmp/.agents/skills"
  probe "check 6 fires when .agents/skills exposes product skills" "check 6 — .agents holds skills"
  write_clients; printf '{"mcpServers": {}}\n' > "$tmp/.agents/mcp_config.json"
  probe "check 6 fires on an MCP file in the development .agents" "check 6 — .agents holds mcp_config.json"
  write_clients; rm "$tmp/.agents/CLAUDE.md"
  probe "check 6 fires when .agents loses its pair" "check 6 — .agents lacks its pair"
  write_clients; mkdir -p "$tmp/.claude/skills"
  probe "check 6 fires when development skills exist and .agents/skills is absent" "check 6 — .agents/skills must link"
  ln -s ../.claude/skills "$tmp/.agents/skills"
  probe_clean "a development skill tree linked as .agents/skills is accepted"
  write_clients

  SM_ROOT="$real_root"; SETTINGS="$SM_ROOT/.claude/settings.json"; SKILLS="$SM_ROOT/template/.claude/skills"
  st_finish "an isolated template from a leaking one"
}

command -v python3 >/dev/null 2>&1 || die "python3 is not installed"
if $SELF_TEST; then
  self_test
  exit $?
fi

bold "▸ $SCRIPT_NAME"
run_checks
if [[ ${#FINDINGS[@]} -eq 0 ]]; then
  bold "✓ $ON_DISK template skill(s) on disk and every catalogued skill denied and set off; both CLAUDE.md exclusions and client isolation present."
  exit 0
fi
bold "✗ ${#FINDINGS[@]} finding(s):"
print_findings
log ""
log "  Add Skill(<name>) to permissions.deny and <name>: off to skillOverrides in the ROOT"
log "  .claude/settings.json (never the one under template/, which ships)."
exit 1

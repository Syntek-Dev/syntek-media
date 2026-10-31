#!/usr/bin/env bash
# pre-compact-handoff.sh — intercept context compaction; steer the session to the handoff skill.
#
# Registered in .claude/settings.json three times: under hooks.PreCompact, matcher "auto" passes
# `auto` as $1 and matcher "manual" passes `manual`; under hooks.SessionStart, matcher "compact"
# passes `compacted`. context-threshold-handoff.sh also runs it with `relay` on every prompt.
# Each entry resolves this script from the git root in the silent form, `ROOT=$(git rev-parse
# --show-toplevel …) || exit 0; [ -f … ] || exit 0; exec bash …`, so outside a git repository,
# or with this script missing, the entry exits 0 and prints nothing; from inside a repository
# nested in the project it finds no script, so an automatic compaction there goes ahead
# unannounced. An entry an earlier release wired in the `[ -f … ] && exec` form is kept as it
# was; there a missing script shows Claude Code's 'hook error' notice.
#
# A hook runs a shell command. It CANNOT invoke a skill, write a handoff or stop the session;
# only the model can. So this script's job is narrow: stop silent auto-compaction, and see that
# the person hears of it, and of a manual /compact, from a hook that can speak to them. The rule
# it enforces, and the reasons for it, live in the session-boundaries rule
# (07-session-boundaries.md in the project's rules under .claude/rules/); the procedure is the
# handoff skill (.claude/skills/handoff/SKILL.md). context-threshold-handoff.sh warns earlier,
# while the window still has room for a handoff.
#
# Claude Code discards a PreCompact hook's systemMessage, keeps its stderr at exit 0 only in the
# debug log, and promises the exit-2 stderr to the person only for a manual /compact. So each
# PreCompact run leaves a marker for its session, .claude/compaction-marker-<session_id>.tmp
# ("<trigger> <session_id>", the id reduced to letters, digits and hyphens), and a later event
# of that session that can speak shows the note and removes the marker. The script reads,
# writes and removes only the current session's marker, and reads it only where its second
# field names this session, so one session's compaction never touches another's pending note:
#
#   $1 = auto       PreCompact, automatic compaction (the window near its limit, or the session
#                   idle): BLOCK it (exit 2), remind on stderr and leave the marker `auto`.
#                   Never compact silently.
#   $1 = manual     PreCompact, /compact: ALLOW it (exit 0), never block a choice; leave the
#                   marker `manual`, and one line on stderr for the debug log.
#   $1 = compacted  SessionStart, source compact (after a compaction): where this session's
#                   marker says `manual`, remove it and print the note on /compact; where it
#                   says anything else (a stale `auto`), remove it unread; with none, do nothing.
#   $1 = relay      UserPromptSubmit, run by context-threshold-handoff.sh: where this session's
#                   marker says `auto`, remove it and print the note on the stopped compaction;
#                   otherwise print nothing and leave it.
#
# A payload with no session_id gets no marker: none is written, read or removed, `auto` still
# blocks and reminds, and `manual` still allows. Before it leaves its own marker, the script
# removes every other session's marker in the same folder last modified more than seven days ago
# (a session never resumed), a regular file only: a link is never followed or removed.
#
# A note is one JSON object on one line: its systemMessage is shown to the person, its
# hookSpecificOutput.additionalContext is added to the session's context. A note is printed
# only once its marker is gone (removed, or emptied where it cannot be removed), so it is never
# shown twice; a marker that is a link is never read, written or removed, and one that is
# not a regular file (a FIFO, a folder) is never read or written.
# stdin  = the event's JSON payload; only session_id is read (no jq, no Python).
# stdout = the note for `compacted` and `relay`; nothing for `auto` and `manual`.
# The markers are the hook's own state, ignored by the project's .gitignore (its
# compaction-marker-*.tmp line, or in an older project its *.tmp rule); one that cannot be
# written, read or removed changes no exit code.
#
# Exit codes: 2 = compaction blocked (auto) · 0 = everything else
set -uo pipefail

mode="${1:-auto}"

payload=""
[ -t 0 ] || payload="$(cat 2>/dev/null)" || payload=""

session_of() { # the payload's session_id: letters, digits and hyphens only
  local re='"session_id"[[:space:]]*:[[:space:]]*"([^"]*)"'
  if [[ $payload =~ $re ]]; then
    printf '%s' "${BASH_REMATCH[1]//[^A-Za-z0-9-]/}"
  fi
}
session="$(session_of)"

# This session's marker, beside the hooks folder; none without a session id, none through a link.
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)" || here=""
dir="" marker=""
[ -n "$here" ] && dir="$(dirname "$here")"
[ -n "$dir" ] && [ -n "$session" ] && marker="$dir/compaction-marker-$session.tmp"
[ -n "$marker" ] && [ -L "$marker" ] && marker=""

leave() { # $1 = trigger: prune other sessions' stale markers, then leave this session's
  [ -n "$marker" ] || return 0
  find "$dir/" -maxdepth 1 -type f -name 'compaction-marker-*.tmp' -mmin +10080 \
    ! -name "${marker##*/}" -exec rm -f -- {} + 2>/dev/null || true
  [ ! -e "$marker" ] || [ -f "$marker" ] || return 0   # a FIFO or a folder there: never written
  { printf '%s %s\n' "$1" "$session" > "$marker"; } 2>/dev/null || true
}

kind="" owner=""
if [ -n "$marker" ] && [ -f "$marker" ]; then
  { read -r kind owner < "$marker"; } 2>/dev/null || true
fi
[ "$owner" = "$session" ] || kind=""   # read only where it names this session

consume() { # remove the marker, or empty it where it cannot be removed; true once it is gone
  rm -f -- "$marker" 2>/dev/null || { : > "$marker"; } 2>/dev/null || true
  [ ! -s "$marker" ]
}

note() { # $1 = event, $2 = for the person, $3 = for the session: one JSON object on one line
  printf '{"systemMessage": "%s", "hookSpecificOutput": {"hookEventName": "%s", "additionalContext": "%s"}}\n' \
    "$2" "$1" "$3"
}

AUTO_PERSON="Automatic compaction was stopped. Run /handoff to save where you are, then /clear to start a fresh session. If /handoff has no room to run, run /compact yourself (it is allowed), then /handoff."
AUTO_SESSION="Claude Code tried to compact this session automatically (as the context window neared its limit, or after the session sat idle), and the project's pre-compact hook, .claude/hooks/pre-compact-handoff.sh, stopped it, so nothing was summarised. The person has been shown: '${AUTO_PERSON}' The session-boundaries rule in the project's rules (.claude/rules/) asks for a handoff instead of compaction: durable knowledge recorded in its real home first, then the handoff skill, then the handoff's path printed and the turn stopped, so the person can run /clear. Where the window has no room left to write the handoff, the session says so rather than starting a handoff it cannot finish: the person may run /compact, which the project allows, and then /handoff."
MANUAL_PERSON="This session was compacted by hand with /compact. That works, but a handoff gives a cleaner break: next time, run /handoff to save where you are, then /clear to start a fresh session."
MANUAL_SESSION="This session was compacted by hand with /compact, which the project allows. The earlier conversation is now a summary, which keeps conclusions and can drop the reasons behind them, so a decision that matters is worth checking against the files before it is relied on. The session-boundaries rule in the project's rules (.claude/rules/) prefers a handoff to compaction: at the next natural stopping point, the handoff skill writes one and the person runs /clear. Where the person compacted to make room for a handoff, as the note after a stopped automatic compaction suggests, the session offers the handoff skill now. The person has been shown: '${MANUAL_PERSON}'"

remind() {
  cat >&2 <<'MSG'
STOP: compaction intercepted. Do not compact this session; hand off instead.

House rule: the session-boundaries rule in the project's rules (.claude/rules/): hand off,
never compact.
  1. Record any durable knowledge in its real home FIRST: .claude/MEMORY.md (through its gate),
     the brief of the work in hand, or the folder's CONTEXT.md / CLAUDE.md.
  2. Invoke the `handoff` skill. It writes the handoff in the folder and filename form the
     project's rules give (by default handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md), including
     the part its mode files say this project must never drop.
  3. Print the handoff path and STOP the turn.
  4. The author or owner runs /clear and resumes from the handoff in a fresh context window.
MSG
}

case "$mode" in
  manual)
    leave manual
    printf 'Manual /compact allowed; the note to hand off next time follows the compaction (SessionStart, compact).\n' >&2
    exit 0
    ;;
  compacted)
    if [ "$kind" = "manual" ]; then
      consume && note SessionStart "$MANUAL_PERSON" "$MANUAL_SESSION"
    elif [ -n "$kind" ]; then
      consume || true
    fi
    exit 0
    ;;
  relay)
    if [ "$kind" = "auto" ]; then
      consume && note UserPromptSubmit "$AUTO_PERSON" "$AUTO_SESSION"
    fi
    exit 0
    ;;
esac

# Auto-compaction (and any other argument): block it, so nothing is silently summarised.
leave auto
remind
exit 2

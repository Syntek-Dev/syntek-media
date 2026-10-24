#!/usr/bin/env bash
# context-threshold-handoff.sh — warn the session before its context window runs out.
#
# Registered in .claude/settings.json under hooks.UserPromptSubmit (no matcher). The entry
# resolves this script from the git root and guards it with [ -f … ], so a missing script is a
# silent no-op, never an error.
#
# A hook CANNOT invoke a skill, write a handoff or stop a turn; only the model can. So this
# script measures and reminds, and the session-boundaries rule (07-session-boundaries.md in the
# project's rules under .claude/rules/) carries the behaviour. pre-compact-handoff.sh makes the
# same split, later: by the time compaction fires the window is spent, and a handoff written
# under that pressure is the worst one of the session.
#
#   >= 50%  advise  — once per session: steer towards a stopping point.
#   >= 75%  insist  — on every prompt: hand off now.
#
# The size in use is the usage of the last MAIN-CHAIN assistant record in the transcript (its
# input, cache-creation, cache-read and output tokens). Sidechain records are subagent windows,
# never this one, and are skipped. A line that does not parse is skipped, never fatal.
#
# Nothing in the transcript reports the window's size, so it is assumed: 200000 tokens unless
# CLAUDE_CONTEXT_WINDOW says otherwise (set it under "env" in .claude/settings.local.json for a
# larger window). A wrong guess fires early rather than never. CLAUDE_CONTEXT_ADVISE_PCT and
# CLAUDE_CONTEXT_INSIST_PCT move the thresholds.
#
# stdin  = the UserPromptSubmit JSON payload (transcript_path, session_id).
# stdout = added to the model's context.
# Exit code: always 0. A miscounted token must never block a prompt; without python3, without a
# transcript or without a usable record it prints nothing.
set -uo pipefail

command -v python3 >/dev/null 2>&1 || exit 0

IFS= read -r -d '' PROBE <<'PY'
import json
import os
import re
import sys

TAIL = 4 * 1024 * 1024


def number(name, default):
    try:
        value = int(os.environ.get(name, "") or default)
    except ValueError:
        return default
    return value if value > 0 else default


def usage_of(line):
    try:
        record = json.loads(line)
    except ValueError:
        return None
    if not isinstance(record, dict) or record.get("type") != "assistant":
        return None
    if record.get("isSidechain") is True:
        return None
    message = record.get("message")
    usage = message.get("usage") if isinstance(message, dict) else None
    if not isinstance(usage, dict):
        return None
    total = 0
    for key in ("input_tokens", "cache_creation_input_tokens",
                "cache_read_input_tokens", "output_tokens"):
        value = usage.get(key)
        if isinstance(value, int) and not isinstance(value, bool) and value > 0:
            total += value
    return total


def last_usage(lines):
    for line in reversed(lines):
        if line.strip():
            found = usage_of(line)
            if found is not None:
                return found
    return None


def measure(path):
    with open(path, "rb") as handle:
        handle.seek(0, os.SEEK_END)
        size = handle.tell()
        start = max(0, size - TAIL)
        handle.seek(start)
        lines = handle.read().decode("utf-8", "replace").splitlines()
        if start > 0 and lines:
            lines = lines[1:]
        found = last_usage(lines)
        if found is not None or start == 0:
            return found
        handle.seek(0)
        return last_usage(handle.read().decode("utf-8", "replace").splitlines())


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return
    if not isinstance(payload, dict):
        return
    path = payload.get("transcript_path")
    if not isinstance(path, str) or not path or not os.path.isfile(path):
        return
    session = re.sub(r"[^A-Za-z0-9-]", "", str(payload.get("session_id") or "")) or "unknown"
    window = number("CLAUDE_CONTEXT_WINDOW", 200000)
    advise = number("CLAUDE_CONTEXT_ADVISE_PCT", 50)
    insist = number("CLAUDE_CONTEXT_INSIST_PCT", 75)
    try:
        used = measure(path)
    except OSError:
        return
    if not used:
        return
    pct = used * 100 // window
    size = f"about {pct}% ({used} of an assumed {window} tokens)"
    note = ""
    if used > window:
        note = ("\nThe count is past the assumed window, so the window is larger: set "
                "CLAUDE_CONTEXT_WINDOW to its size.")

    if pct >= insist:
        print(f"""STOP: context at {size}, past the {insist}% threshold. Hand off now, before the window forces it.

House rule: the session-boundaries rule in the project's rules (.claude/rules/): hand off, never compact.
  1. Record any durable knowledge in its real home FIRST: .claude/MEMORY.md (through its gate),
     the brief of the work in hand, or the folder's CONTEXT.md / CLAUDE.md.
  2. Invoke the `handoff` skill. It writes the handoff in the folder and filename form the
     project's rules give (by default handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md).
  3. Print the handoff path and STOP the turn.
  4. The author or owner runs /clear and resumes from the handoff in a fresh context window.

Start no new piece of work. Finish only what cannot safely be left mid-flight.{note}""")
        return

    if pct < advise:
        return

    # Advice fires once per session: a notice repeated on every prompt spends the context it
    # exists to protect. The insist tier repeats deliberately.
    state = os.path.join(os.environ.get("TMPDIR") or "/tmp", f"claude-context-advise-{session}")
    if os.path.exists(state):
        return
    try:
        open(state, "a").close()
    except OSError:
        pass
    print(f"""NOTE: context at {size}: half the window is gone. Steer towards a handoff.

House rule: the session-boundaries rule in the project's rules (.claude/rules/).
  - Finish the step in flight; open no new piece of work that will not fit.
  - Record durable knowledge in its real home as it settles, not at the end.
  - Name the natural stopping point to the author or owner and offer /handoff.
  - At {insist}% this becomes an instruction, not a suggestion.{note}""")


try:
    main()
except Exception:
    pass
PY

python3 -I -c "$PROBE" 2>/dev/null || true
exit 0

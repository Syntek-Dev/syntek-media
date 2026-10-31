#!/usr/bin/env bash
# how-to-read-only.sh — stop a session's file tools editing or writing in the user guide, how-to/.
#
# Registered in .claude/settings.json under hooks.PreToolUse, matcher
# "Edit|Write|MultiEdit|NotebookEdit". The entry resolves this script from the git root and
# exits 0 where there is no root or no script, so a missing script is a silent no-op: it runs
# before every edit, and an error there would show on each one.
#
# how-to/ is the user guide the project's templates ship, and it is read-only. The project's
# rules say so, .claude/settings.json denies edits there, and every template update puts the
# guide's files back as the template wrote them. This hook refuses a file tool's edit or write
# at or under the project's how-to/ whatever the settings say, so a deny rule that was removed,
# or a session started in a subfolder, never opens the guide. It judges the path the tool
# names, as written and as the disk resolves it, never the file's contents. It does not read
# shell commands: the rules alone keep a shell command out of the guide, and a template's
# update, which runs as a shell command, is never stopped. Written for macOS, Linux and WSL;
# on native Windows it may let a write through.
#
# It needs Python 3.14 or later (PYTHON_MIN, below). On an older python3 it judges nothing: it
# lets the call through and prints, on stdout, the JSON that has Claude Code warn the person
# (systemMessage) and the session (additionalContext) that it did NOT work and that Python needs
# upgrading. It makes no permission decision there, so the deny rule still applies. The Python
# below parses as Python 3.8, so an old python3 reaches that warning, never a SyntaxError.
#
# stdin  = the PreToolUse JSON payload (tool_name, tool_input, cwd).
# stderr = on a refusal, the reason, which the session reads.
# stdout = on a python3 older than PYTHON_MIN, the warning JSON; otherwise nothing.
# Exit codes: 2 = refused (the target is in how-to/) · 0 = anything else, an older python3 (with
# its warning), bad input, a missing python3 and the hook's own errors included: a guard that
# errs must never block other work.
set -uo pipefail

command -v python3 >/dev/null 2>&1 || exit 0
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." 2>/dev/null && pwd)" || exit 0

IFS= read -r -d '' GUARD <<'PY'
import json
import os
import sys

# The one place the minimum is set: the move to a newer Python changes this line and the
# header above, nothing else.
PYTHON_MIN = (3, 14)
FIELDS = {"Edit": "file_path", "Write": "file_path", "MultiEdit": "file_path",
          "NotebookEdit": "notebook_path"}
GUIDE = "how-to"
REASON = ("how-to/ is the user guide this project's templates ship, and it is read-only: no "
          "session edits, writes or deletes a file there, and every template update puts the "
          "guide's files back. Record how this project departs from the guide where the "
          "project's rules under .claude/rules/ say a departure is recorded, and keep the "
          "project's own notes outside how-to/.")


def within(path, top):
    a, b = os.path.normcase(path), os.path.normcase(top)
    try:
        return os.path.commonpath([a, b]) == b
    except ValueError:
        return False


def refused(payload, root):
    tool, given = payload.get("tool_name"), payload.get("tool_input")
    if not isinstance(tool, str) or tool not in FIELDS or not isinstance(given, dict):
        return False
    target = given.get(FIELDS[tool])
    if not isinstance(target, str) or not target:
        return False
    base = payload.get("cwd")
    if not isinstance(base, str) or not os.path.isabs(base):
        base = os.getcwd()
    target = os.path.normpath(os.path.join(base, os.path.expanduser(target)))
    tops = {os.path.normpath(root), os.path.realpath(root)}
    if any(within(target, os.path.join(top, GUIDE)) for top in tops):
        return True
    guide = os.path.join(root, GUIDE)
    if os.path.isdir(guide) and not os.path.islink(guide):
        # A link into the guide, or the guide named in another letter case on a disk that
        # ignores case. Only where the guide is a real folder: a guide that is a link would
        # otherwise lock whatever folder it points at.
        if within(os.path.realpath(target), os.path.realpath(guide)):
            return True
        for top in tops:
            if within(target, top):
                first = os.path.relpath(target, top).split(os.sep)[0]
                if first != GUIDE and first.casefold() == GUIDE:
                    try:
                        if os.path.samefile(os.path.join(top, first), guide):
                            return True
                    except OSError:
                        pass
    return False


def too_old(version):
    """The warning JSON for a python3 older than PYTHON_MIN: no permission decision, so the call
    goes ahead under the usual rules; Claude Code shows systemMessage to the person and adds
    additionalContext to the session."""
    need, have = "%d.%d" % PYTHON_MIN, "%d.%d" % tuple(version[:2])
    person = ("WARNING: the guide guard did NOT work: python3 here is Python %s, and the guard needs "
              "Python %s or later. It let this call through unchecked, leaving the deny rule alone to "
              "keep edits out of how-to/. Upgrade to Python %s or later." % (have, need, need))
    session = ("The project's guide guard, .claude/hooks/how-to-read-only.sh, did not run for this call: "
               "python3 here is Python %s, and the guard needs Python %s or later, so it let the call "
               "through unchecked and will do so for every edit until Python is upgraded. how-to/ is still "
               "read-only. The person has to upgrade to Python %s or later for the guard to work, and "
               "needs to hear this from the session." % (have, need, need))
    return json.dumps({"systemMessage": person,
                       "hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": session}})


def main():
    if sys.version_info < PYTHON_MIN:
        try:
            sys.stdin.buffer.read()   # the whole call, so the client never writes to a closed pipe
        except Exception:
            pass
        sys.stdout.write(too_old(sys.version_info) + "\n")
        sys.stdout.flush()
        return 0
    try:
        payload = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
    except ValueError:
        return 0
    if isinstance(payload, dict) and refused(payload, sys.argv[1]):
        sys.stderr.write(REASON + "\n")
        return 2
    return 0


try:
    code = main()
except Exception:
    code = 0
sys.exit(code)
PY

rc=0
python3 -I -c "$GUARD" "$ROOT" || rc=$?
[ "$rc" -eq 2 ] && exit 2
exit 0

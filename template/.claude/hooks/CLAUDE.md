@./CONTEXT.md

# CLAUDE.md — .claude/hooks/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `.claude/CONTEXT.md` →
this folder's `CONTEXT.md` (the hook registry and exit codes, imported above) → this file.

## Purpose (one line)

Keep the session hooks small, fast and honest, so the warning before the window fills, the
guard against silent compaction and the guard on the user guide keep working.

## How to work here

- **Routing:** a hook change is a shell edit plus its registration in `.claude/settings.json`; the
  rule a hook enforces lives in the project's rules under `.claude/rules/`, and the work it
  steers to lives in a skill.
- **Model:** **Opus**: a hook runs unattended in every session, so a mistake here repeats silently.
- **Concrete steps:** confirm the change with the owner → edit the script → run
  `bash -n` on it → run it by hand with each argument (or, for the threshold hook, with a
  payload naming a copy of a real transcript on stdin) and check the exit code and the output →
  for a hook that runs Python, run it again with a `python3` older than its `PYTHON_MIN` first
  on `PATH` → keep its header, its `settings.json` entry and the table in `CONTEXT.md` in step.
- **Definition of done:** the script is executable and parses; `pre-compact-handoff.sh auto`
  exits 2, printing the reminder, and `pre-compact-handoff.sh manual` exits 0, each leaving that
  session's marker (none for a payload with no `session_id`) and removing any other session's
  marker more than seven days old, never a link; with that marker, `compacted` (manual) and
  `relay` (auto) of the same session exit 0 and print one JSON object, `systemMessage` and
  `hookSpecificOutput.additionalContext`, and remove it, while another session's run prints
  nothing and leaves it; outside a Git repository, or with its script missing, each entry exits
  0 and prints nothing; `context-threshold-handoff.sh` exits 0 on every input, prints the
  relayed note when there is one, else nothing below 50%, advises once a session from 50% and
  insists from 75%; the header, the settings entry and the `CONTEXT.md` table agree.
  `how-to-read-only.sh` exits 2 for an edit or write under `how-to/` and 0 for every other path,
  tool and bad input. On a `python3` older than `PYTHON_MIN`, both hooks that run Python exit 0
  on every input and print one JSON object, `systemMessage` and
  `hookSpecificOutput.additionalContext` saying it did NOT work and to upgrade, and no permission
  decision; their Python parses as Python 3.8 (`ast.parse(…, feature_version=(3, 8))`).

## Guardrails

- **Never weaken `pre-compact-handoff.sh`.** It blocks auto-compaction (exit 2) and allows a
  manual `/compact` (exit 0), and the person hears of each: the stopped one on their next prompt,
  the manual one once it is done. Silent compaction is the failure it exists to prevent.
- **`context-threshold-handoff.sh` always exits 0.** A miscounted token must never block a
  prompt; on any doubt (no `python3`, no transcript, no readable record) it prints nothing. On a
  `python3` older than `PYTHON_MIN` it prints the warning JSON on every prompt instead.
- **Never weaken `how-to-read-only.sh`.** It refuses a file tool's edit or write under
  `how-to/`; it fails open only on bad input, a missing `python3`, a `python3` older than
  `PYTHON_MIN` (where it judges nothing and warns on every call) or its own error, never on a
  path it judged.
- **One Python minimum, and loud below it.** Each hook that runs Python sets `PYTHON_MIN` once,
  in its Python, and checks it before anything else; a move to a newer Python changes that line
  and the header. Below it a hook never blocks: it lets the action through, exits 0 and prints
  the warning JSON on stdout, because Claude Code shows nothing a hook prints on stderr with
  exit 0. Keep its Python parseable as Python 3.8, so an old `python3` reaches the warning.
- **Count the main chain only.** Sidechain records are a subagent's window, never this
  session's; counting one fires the warning on a context that is not ours.
- **Verify a threshold change by replaying a real transcript**, never by reasoning about one:
  the transcript's fields are Claude Code's, and a silent change there silences the hook.
- **A hook cannot do the model's job.** It cannot invoke a skill, write a handoff or end a turn.
  Anything that needs judgement belongs in a skill.
- **Never make a hook slow.** It runs inside the session; a hook that hangs stalls the owner.
- **Never let a hook write to the work** (any `src/` folder), or to any file the owner owns. The
  only files a hook writes in the project are its own git-ignored markers, one per session,
  `.claude/compaction-marker-<session_id>.tmp`: it writes the current session's alone, and
  removes another session's only once it is more than seven days old.
- **Fail open on absence, never on error.** In the seed's `|| exit 0` form a missing script is
  silent: its entry exits 0 and prints nothing. An entry an earlier release wired shows a 'hook
  error' notice until it is switched by hand (`CONTEXT.md`, 'Conventions'). A script that runs
  must report what it found, never a pass it did not check. The one exception is a guard
  (`how-to-read-only.sh`): it also fails open on bad input, an older `python3` (with its loud
  warning) or its own error, never on a path it judged, because a guard that errs must never
  block other work.
- **The shipped scripts and this pair are shared.** A template's update replaces
  `pre-compact-handoff.sh`, `context-threshold-handoff.sh`, `how-to-read-only.sh`, this file and
  `CONTEXT.md` only while they are unchanged; an edited one is kept, frozen and reported. A
  project-specific change belongs in a new script of its own, or in the project's rules.
- Changing a hook requires the owner's explicit instruction.

## Output & naming

- **Hand-written:** each `kebab-case.sh` script, executable, with its header. Nothing here is
  generated.
- One script per job, named for the event, the measure or the folder it guards, and its purpose
  (`pre-compact-handoff.sh`, `context-threshold-handoff.sh`, `how-to-read-only.sh`).

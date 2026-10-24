@./CONTEXT.md

# CLAUDE.md — .claude/hooks/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `.claude/CONTEXT.md` →
this folder's `CONTEXT.md` (the hook registry and exit codes, imported above) → this file.

## Purpose (one line)

Keep the session hooks small, fast and honest, so the warning before the window fills and the
guard against silent compaction keep working.

## How to work here

- **Routing:** a hook change is a shell edit plus its registration in `.claude/settings.json`; the
  rule a hook enforces lives in the project's rules under `.claude/rules/`, and the work it
  steers to lives in a skill.
- **Model:** **Opus**: a hook runs unattended in every session, so a mistake here repeats silently.
- **Concrete steps:** confirm the change with the owner → edit the script → run
  `bash -n` on it → run it by hand with each argument (or, for the threshold hook, with a
  payload naming a copy of a real transcript on stdin) and check the exit code and the output →
  keep its header, its `settings.json` entry and the table in `CONTEXT.md` in step.
- **Definition of done:** the script is executable and parses; `pre-compact-handoff.sh auto`
  exits 2 and `pre-compact-handoff.sh manual` exits 0, both printing the reminder;
  `context-threshold-handoff.sh` exits 0 on every input, prints nothing below 50%, advises once
  a session from 50% and insists from 75%; the header, the settings entry and the `CONTEXT.md`
  table agree.

## Guardrails

- **Never weaken `pre-compact-handoff.sh`.** It blocks auto-compaction (exit 2) and only warns on
  a manual `/compact`. Silent compaction is the failure it exists to prevent.
- **`context-threshold-handoff.sh` always exits 0.** A miscounted token must never block a
  prompt; on any doubt (no `python3`, no transcript, no readable record) it prints nothing.
- **Count the main chain only.** Sidechain records are a subagent's window, never this
  session's; counting one fires the warning on a context that is not ours.
- **Verify a threshold change by replaying a real transcript**, never by reasoning about one:
  the transcript's fields are Claude Code's, and a silent change there silences the hook.
- **A hook cannot do the model's job.** It cannot invoke a skill, write a handoff or end a turn.
  Anything that needs judgement belongs in a skill.
- **Never make a hook slow.** It runs inside the session; a hook that hangs stalls the owner.
- **Never let a hook write to the work** (any `src/` folder), or to any file the owner owns.
- **Fail open on absence, never on error.** A missing script is a no-op; a script that runs must
  report what it found, never a pass it did not check.
- **The shipped scripts and this pair are shared.** A template's update replaces
  `pre-compact-handoff.sh`, `context-threshold-handoff.sh`, this file and `CONTEXT.md` only while
  they are unchanged; an edited one is kept, frozen and reported. A project-specific change
  belongs in a new script of its own, or in the project's rules.
- Changing a hook requires the owner's explicit instruction.

## Output & naming

- **Hand-written:** each `kebab-case.sh` script, executable, with its header. Nothing here is
  generated.
- One script per job, named for the event or the measure and its purpose
  (`pre-compact-handoff.sh`, `context-threshold-handoff.sh`).

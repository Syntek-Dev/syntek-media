# CONTEXT.md — .claude/hooks/

Shell hooks that Claude Code runs at fixed moments in a session, registered in
`.claude/settings.json`. Three ship here. Two turn the rule "hand off, never compact" (the
session-boundaries rule in the project's rules under `.claude/rules/`) from advice into a
guard: `context-threshold-handoff.sh` measures the context window and warns while there is
still room to hand off, and `pre-compact-handoff.sh` blocks the compaction that would follow and,
once a compaction is stopped or run by hand, sees that you hear of it.
The third, `how-to-read-only.sh`, stops the session's file tools editing or writing in the user
guide in `how-to/`, which is read-only (on macOS, Linux and WSL).
Judgement never lives here: a hook can measure, block and remind, but only a skill can do the work.

## Directory Tree

```text
.claude/hooks/
├── CONTEXT.md                      ← this file (shared)
├── CLAUDE.md                       ← operating rules for hooks (shared)
├── context-threshold-handoff.sh    ← UserPromptSubmit: advises at 50% of the window, insists at 75% (shared)
├── how-to-read-only.sh             ← PreToolUse: refuses edits and writes under how-to/ (shared)
└── pre-compact-handoff.sh          ← PreCompact: blocks auto-compaction, allows /compact; SessionStart: the note after /compact (shared)
```

## What's here

| Hook | Matcher | Script | Effect |
|---|---|---|---|
| `UserPromptSubmit` | none | `context-threshold-handoff.sh` | Measures the window; at 50% advises once a session, at 75% insists on every prompt that the session hands off now (always exit 0); on a `python3` older than the minimum below it measures nothing and warns on every prompt that it did not work; on the first prompt after an automatic compaction was stopped in this session, it shows that note instead (`pre-compact-handoff.sh relay`, which needs no Python) |
| `PreCompact` | `auto` | `pre-compact-handoff.sh auto` | Blocks compaction (exit 2), as the window nears its limit or while the session sits idle, and leaves this session's marker for the note your next prompt in it shows |
| `PreCompact` | `manual` | `pre-compact-handoff.sh manual` | Allows (exit 0); a deliberate `/compact` is not overridden, and it leaves this session's marker for the note shown once the compaction is done |
| `SessionStart` | `compact` | `pre-compact-handoff.sh compacted` | After a `/compact`, shows the note and tells the session its earlier conversation is now a summary (always exit 0); after any other compaction it says nothing |
| `PreToolUse` | `Edit\|Write\|MultiEdit\|NotebookEdit` | `how-to-read-only.sh` | Refuses (exit 2) a file tool's edit or write at or under `how-to/`, the read-only user guide, whatever the settings say; exits 0 for every other path and tool, and on bad input or its own error; on a `python3` older than the minimum below it judges nothing, lets every call through (exit 0) and warns on each that it did not work |

`pre-compact-handoff.sh` works as a pair with `"autoCompactEnabled": false` and
`"idleCompaction": false`, which the seed `.claude/settings.json` sets beside each other: the
first stops compaction starting on its own as the window fills, the second keeps idle compaction
(of a long session you have stepped away from) off even where the first is turned back on, and
the hook catches any compaction that starts anyway. Claude Code fires `PreCompact` with the
`auto` matcher for an idle compaction too, so without the second a pause could end in the note
to hand off with the window far from full; a version older than 2.1.290 ignores the key,
harmlessly. A copy over a `settings.json` the project already had, or the next update, adds each
with the value false where the file has no such key, once, in the file's own layout. A value you
set yourself is kept, and the copy or update says once that the handoff hooks assume false; a
key you delete after that is not added back. Without the settings, the hook still blocks
compaction when it starts.

**The compaction notes.** Claude Code promises to show what a `PreCompact` hook prints only
when it blocks a `/compact` you typed, so `pre-compact-handoff.sh` leaves a small marker, one per
session, `.claude/compaction-marker-<session_id>.tmp`, and a later event of that session that can
speak shows the note and removes it. The hook reads, writes and removes only the current
session's marker, so a compaction in one session never touches another's note; where Claude
Code sends no session id, it leaves no marker (an automatic compaction is still stopped and a
`/compact` still goes ahead, but no note follows). Before it leaves a marker it removes any other
session's marker last modified more than seven days ago, so the markers of sessions never resumed
do not pile up; a link is never removed.
After an automatic compaction it stopped, your next prompt in that session shows 'Automatic
compaction was stopped. Run /handoff to save where you are, then /clear to start a fresh
session. If /handoff has no room to run, run /compact yourself (it is allowed), then /handoff.'
After a `/compact`, a note says the session was compacted by hand: that works, but a handoff
gives a cleaner break, so next time run `/handoff`, then `/clear`; where you compacted to make
room for a handoff, the session offers it now. Each note also reaches the session. The markers
are the hook's own state, never your work; the project's `.gitignore` ignores them, and a marker
the hook cannot write changes nothing it blocks or allows.

**The window threshold.** `context-threshold-handoff.sh` reads the session's transcript and
takes the usage of the last main-chain reply as the size in use; a subagent's records are never
counted, and a line it cannot read is skipped. Nothing reports the window's size, so it assumes
200,000 tokens. For a larger window, set `CLAUDE_CONTEXT_WINDOW` under `"env"` in
`.claude/settings.local.json`; `CLAUDE_CONTEXT_ADVISE_PCT` and `CLAUDE_CONTEXT_INSIST_PCT` move
the thresholds. It needs `python3` and stays silent without it, and it never blocks a prompt.

**Python 3.14 or later.** The two hooks that run Python, `context-threshold-handoff.sh` and
`how-to-read-only.sh`, need Python 3.14 or later, set once in each as `PYTHON_MIN`. On an older
`python3` neither blocks anything: each lets the prompt or the call go ahead and warns, every
time, that it did NOT work, naming the Python it found and asking you to upgrade. The warning
reaches you on screen and reaches the session, so the session can pass it on. Until you
upgrade, the deny rule alone keeps the guide read-only, and nothing measures the window.

**Exit codes.** `exit 0` lets the action go ahead; Claude Code keeps what such a hook prints on
stderr in its debug log, not in the session. `exit 2` blocks the action, and stderr becomes the
message. Any other exit is a non-blocking error. With `exit 0`, a JSON object printed on stdout
can warn you (`systemMessage`) and add a note to the session's context
(`hookSpecificOutput.additionalContext`) without deciding anything, which is how the two hooks
above warn on an older Python. `PreCompact` is the exception: Claude Code discards its
`systemMessage`, so nothing a `PreCompact` hook prints with `exit 0` reaches you, which is why
its notes wait for the next prompt or the `SessionStart` after the compaction. For
`UserPromptSubmit`, plain text printed on stdout with `exit 0` is added to the session's
context, which is how the threshold hook speaks to the model.

**Ownership.** Every file listed above is **shared**: every template of the family that ships
it ships the same bytes, the first template applied to the project writes it, and no template's
update renders, merges or deletes it. The update of a template that ships them replaces one
only while it still holds a version that template wrote here, and writes one new in its release
that the project never had; one you have changed, or one holding another template's version, is
kept and named in the update report, with the commands to compare it and take the new one. That update,
like a copy over an existing `.claude/settings.json`, also adds each hook entry the template
lists and has not offered before, and never removes or changes one. A
hook added for this project gets its own script here and its own entry in
`.claude/settings.json`, which is the project's.

**Conventions.** Every script is `bash` with `set -uo pipefail`, executable, and opens with a
header naming its `settings.json` entry, its matchers and its exit codes. Settings resolve each
script from the git root in the silent form,
`ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0; [ -f … ] || exit 0; exec bash …`,
so outside a Git repository, or with the script missing, an entry exits 0 and prints nothing.
Git's top level is that of the folder the session works in, so in a repository nested inside the
project the entry finds no script and is silent too: an automatic compaction that starts there
goes ahead with no note.
An entry an earlier release wired keeps its `[ -f … ] && exec` form: an update recognises an
entry by its event, matcher and script, never rewrites one and adds no second. There a missing
script shows Claude Code's 'hook error' notice (a non-blocking error: the action goes ahead), and
you can switch the entry to the silent form by hand in `.claude/settings.json`.

## Cross-references

- `.claude/rules/` — the project's rules: the session-boundaries rule the hooks enforce, and
  why, and where the project keeps its handoffs.
- `.claude/skills/handoff/SKILL.md` — the procedure the hooks steer to.
- `.claude/settings.json` — where the hooks are registered, beside `autoCompactEnabled` and
  `idleCompaction`.
- `handoffs/` — the default home of handoffs.

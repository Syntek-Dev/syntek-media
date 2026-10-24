# CONTEXT.md — .claude/hooks/

Shell hooks that Claude Code runs at fixed moments in a session, registered in
`.claude/settings.json`. Two ship here, and they turn the rule "hand off, never compact" (the
session-boundaries rule in the project's rules under `.claude/rules/`) from advice into a guard:
`context-threshold-handoff.sh` measures the context window and warns while there is still room
to hand off, and `pre-compact-handoff.sh` blocks the compaction that would follow. Judgement
never lives here: a hook can measure, block and remind, but only a skill can do the work.

## Directory Tree

```text
.claude/hooks/
├── CONTEXT.md                      ← this file (shared)
├── CLAUDE.md                       ← operating rules for hooks (shared)
├── context-threshold-handoff.sh    ← UserPromptSubmit: advises at 50% of the window, insists at 75% (shared)
└── pre-compact-handoff.sh          ← PreCompact: blocks auto-compaction, warns on /compact (shared)
```

## What's here

| Hook | Matcher | Script | Effect |
|---|---|---|---|
| `UserPromptSubmit` | none | `context-threshold-handoff.sh` | Measures the window; at 50% advises once a session, at 75% insists on every prompt that the session hands off now (always exit 0) |
| `PreCompact` | `auto` | `pre-compact-handoff.sh auto` | Blocks compaction (exit 2) and steers the session to the `handoff` skill |
| `PreCompact` | `manual` | `pre-compact-handoff.sh manual` | Warns (exit 0); a deliberate `/compact` is not overridden |

`pre-compact-handoff.sh` works as a pair with `"autoCompactEnabled": false`, which the seed
`.claude/settings.json` sets: the setting stops compaction starting on its own, and the hook
catches any compaction that starts anyway. A copy over a `settings.json` the project already
had, or the next update, adds `"autoCompactEnabled": false` where the file has no such key, once,
in the file's own layout. A value you set yourself is kept, and the copy or update says once that
the handoff hooks assume false; a key you delete after that is not added back. Without the
setting, the hook still blocks compaction when it starts.

**The window threshold.** `context-threshold-handoff.sh` reads the session's transcript and
takes the usage of the last main-chain reply as the size in use; a subagent's records are never
counted, and a line it cannot read is skipped. Nothing reports the window's size, so it assumes
200,000 tokens. For a larger window, set `CLAUDE_CONTEXT_WINDOW` under `"env"` in
`.claude/settings.local.json`; `CLAUDE_CONTEXT_ADVISE_PCT` and `CLAUDE_CONTEXT_INSIST_PCT` move
the thresholds. It needs `python3` and stays silent without it, and it never blocks a prompt.

**Exit codes.** `exit 0` lets the action go ahead, and anything on stderr is shown as a warning.
`exit 2` blocks the action, and stderr becomes the message. Any other exit is a non-blocking
error. For `UserPromptSubmit`, what the script prints on stdout with `exit 0` is added to the
session's context, which is how the threshold hook speaks to the model.

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
script from the git root (`git rev-parse --show-toplevel`) and guard it with `[ -f … ]`, so a
missing script is a no-op rather than an error.

## Cross-references

- `.claude/rules/` — the project's rules: the session-boundaries rule the hooks enforce, and
  why, and where the project keeps its handoffs.
- `.claude/skills/handoff/SKILL.md` — the procedure the hooks steer to.
- `.claude/settings.json` — where the hooks are registered, beside `autoCompactEnabled`.
- `handoffs/` — the default home of handoffs.

# CONTEXT.md — handoffs/

Session bridges. Each file carries the live thread of one session (where the work stands, what is
half-done, and the next move) so that a fresh session can resume cleanly after `/clear`. This is
the project's alternative to letting a session compact (the session-boundaries rule,
`07-session-boundaries.md` in the project's rules under `.claude/rules/`). It is a transient
bridge, not a memory store, and nothing in it is the work.

This is the default home. A project that keeps its handoffs elsewhere, or names them another
way, says so in its rules under `.claude/rules/`, and that wins.

## Directory Tree

```text
handoffs/
├── CONTEXT.md                            ← this file
├── CLAUDE.md                             ← operating rules
└── HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md    ← one per handed-over session; pruned once resumed
```

## What's here

- `HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md` — written by the `handoff` skill. The descriptor names
  **the work, not the session**: `HANDOFF-OPENING-SECTIONS-03-10-2026.md`, never
  `HANDOFF-TUESDAY-03-10-2026.md`.
- Each handoff carries the goal, what landed, what is in flight (with `path:line` anchors), the
  part the skill's mode files say this kind of project must never drop, the next move, the
  skills to load, and every artefact by path.
- The folder is empty apart from this pair until the first handoff, and it returns to empty as
  handoffs are pruned.

**Durable knowledge is not kept here.** It is recorded in its real home before the handoff is
written: decisions and facts in `.claude/MEMORY.md`, a piece of work's decisions in its brief, a
folder rule in that folder's `CLAUDE.md`. Work that spans many sessions by design belongs in a
decision map (the `wayfinder` skill; the project's rules name the folder).

**Ownership.** This pair is shared: every template of the family that ships it ships the same
bytes, the first template applied to the project writes it, and no template's update renders,
merges or deletes it. The update of a template that ships it replaces one only while it still
holds a version that template wrote here; one you have changed, or one holding another
template's version, is kept and named in the update report, with the commands to compare it and
take the new one. The handoffs beside it are the project's.

## Cross-references

- `.claude/skills/handoff/SKILL.md` — the skill that writes these files, and their format.
- `.claude/rules/` — the session-boundaries rule (why the project hands off instead of
  compacting) and where the project keeps its handoffs.
- `.claude/hooks/context-threshold-handoff.sh` — the hook that warns as the window fills.
- `.claude/hooks/pre-compact-handoff.sh` — the hook that blocks compaction and points here.
- `.claude/MEMORY.md` — the durable memory a handoff deliberately does not duplicate.

# CONTEXT.md — scripts/workflows/

The scripts layer's ordered procedures: the recipes you start a piece from. Where
`scripts/docs/` explains how a brief, a script or a storyboard is made and `scripts/src/` holds
them, this folder holds the steps, in order, with the skill and guide named at each one and a
model-tagged checklist to tick as you go. **Never brief, script or board a piece straight into
`scripts/src/` from memory.** Start here.

## Directory Tree

```text
scripts/workflows/
├── CONTEXT.md                  ← this file
├── CLAUDE.md                   ← operating rules and the 'You want to…' table
├── 01-brief-a-piece/           ← one piece from idea to an agreed brief, in its own folder
├── 02-write-a-script/          ← a scripted piece's words, timed, reported on and approved
├── 03-storyboard-a-piece/      ← a picture for every spoken line, a source for every shot
└── local/                      ← your own procedures; same slug overrides a template one
```

## What's here

- **Four files per procedure**, always: `CONTEXT.md` (when to reach for it), `CLAUDE.md` (how
  to run it), `STEPS.md` (the ordered steps) and `CHECKLIST.md` (pre-conditions, execution,
  done-when, each item tagged with its model tier).
- **Numbers are frozen and append-only**, unique within this layer across every brand kind,
  platform and media kind, so a gap in the sequence is a procedure that belongs to another kind
  of project, not a missing one. Every file cites a procedure by its full folder name.
- **Each procedure moves a piece one rung**, and its checklist names the gate it passes: briefed
  (M1), scripted (M2) and storyboarded (M3). A recorded piece reaches `scripted` through the
  production layer instead, at `production/workflows/08-bring-in-a-recording/`.
- `local/` — procedures written for this project, in their own numbering.

## Cross-references

- `scripts/docs/reference/` — the guides these procedures cite.
- `scripts/src/` — where every procedure's output lands.
- `scripts/docs/reference/the-piece-ladder.md` — the gates each procedure's checklist cites.
- `.claude/skills/run-media-workflow/SKILL.md` — the router that picks a procedure, `local/`
  first.

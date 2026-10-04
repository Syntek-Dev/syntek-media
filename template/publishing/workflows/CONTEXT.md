# CONTEXT.md — publishing/workflows/

The publishing layer's ordered procedures: the recipes a publishing task starts from. Where
`publishing/docs/` explains how a deliverable is made and posted and `publishing/src/` holds the
record, this folder holds the steps, in order, with the skill and guide named at each one and a
model-tagged checklist to tick as you go. They are numbered in the order a piece usually meets
them, from an approved master to a logged post. **Never cut, caption or schedule from memory.**
Start here.

## Directory Tree

```text
publishing/workflows/
├── CONTEXT.md                        ← this file: the index
├── CLAUDE.md                         ← operating rules and the 'You want to…' table
├── 01-plan-the-cut-downs/            ← one master → an agreed plan of short cuts, per platform
├── 02-cut-for-a-platform/            ← render and verify every deliverable of the brief and the plan
├── 03-caption-a-piece/               ← time, check, and burn or attach captions for every deliverable
├── 04-brief-a-thumbnail/             ← brief, lay out, render and check a thumbnail or cover
├── 05-prepare-a-post/                ← the post package, the disclosure and the schedule rows
├── 06-record-a-publication/          ← log what the author posted; close the piece when all is out
├── 07-refresh-the-platform-specs/    ← re-read stale platform data; record corrections as overrides
<: if 'podcast' in PLATFORMS :>├── 08-publish-the-podcast-feed/     ← a self-hosted show's register, tagged audio, checked feed and upload copy
<: endif :>└── local/                            ← your own procedures; same slug overrides a template one
```

## What's here

- **Four files per procedure**, always: `CONTEXT.md` (when to reach for it), `CLAUDE.md` (how
  to run it), `STEPS.md` (the ordered steps) and `CHECKLIST.md` (pre-conditions, execution,
  done-when, each item tagged with its model tier).
- **Gates** (of `scripts/docs/reference/the-piece-ladder.md`):
  `publishing/workflows/02-cut-for-a-platform/` serves M5,
  `publishing/workflows/03-caption-a-piece/` M6, and `publishing/workflows/04-brief-a-thumbnail/`
  and `publishing/workflows/05-prepare-a-post/` M7<: if 'podcast' in PLATFORMS :>, with
  `publishing/workflows/08-publish-the-podcast-feed/` for a feed episode<: endif :>.
  `publishing/workflows/06-record-a-publication/` closes a piece as published, which is not a
  gate; the other two move no piece.
- **Numbers are frozen and append-only**, unique within this layer across every brand kind,
  platform and media kind.
- `local/` — procedures written for this project, in their own numbering.

## Cross-references

- `publishing/docs/reference/` — the guides these procedures cite.
- `publishing/src/` — where every procedure's output lands.
- `.claude/skills/run-media-workflow/SKILL.md` — the router that picks a procedure, `local/`
  first.

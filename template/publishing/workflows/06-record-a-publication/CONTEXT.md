# CONTEXT.md — publishing/workflows/06-record-a-publication/

The short procedure for keeping the schedule and the publish log true once the author has posted,
moved or dropped a deliverable: the schedule row moves on, a log row records what the author
reports (the date, the address, the label that was set, the captions), and when every row for a
piece is posted or dropped, the piece is marked published. Nothing is logged that the author did
not report, and nothing is posted from here. Published is not a gate: this procedure records it.

## Directory Tree

```text
publishing/workflows/06-record-a-publication/
├── CONTEXT.md        ← this file: when to use it, what it produces
├── CLAUDE.md         ← how to run it; guardrails
├── STEPS.md          ← the ordered procedure
└── CHECKLIST.md      ← tick as you go; model-tagged
```

## When to use this

Every time something happens to a scheduled deliverable:

- the author has posted it, and can give its URL;
- the author has moved its date, or dropped it;
- an earlier schedule or log entry turns out to be wrong.

Reach for a **different** procedure when the task is writing or revising a package
(`publishing/workflows/05-prepare-a-post/`), or anything in syntek-author's content calendar (the
social-media-documents skill (syntek-author), where present).

## What it produces, and where

- **Updated schedule rows** in `publishing/src/schedule.md`, each with its status moved on.
- **A log row** in `publishing/src/publish-log.md` for every post the author reports.
- **The brief's `status` set to `published`,** once every row for the piece is out or dropped.
- **A hand-back** of one line per change, and everything still to go out.

## The failure this procedure exists to prevent

A log that records what was planned instead of what happened: a URL built from a handle, a label
recorded as set because the package said to set it, a piece marked published while one of its
cuts still waits. Decisions about the next post, and answers to anyone who asks what went out and
how it was disclosed, are made from this log, so a row that flatters the plan is worse than none.

## Cross-references

- `publishing/docs/reference/posting-and-the-log.md` — the schedule, the log, and when a piece
  is published.
- `publishing/src/CONTEXT.md` — where the schedule and the log live.
- `publishing/workflows/05-prepare-a-post/` — the procedure that hands over to this one.

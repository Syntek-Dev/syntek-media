# CONTEXT.md — scripts/workflows/01-brief-a-piece/

The procedure for turning an idea into a piece the author has agreed to make: its number, its
folder with its own pair, and a brief that says what it is for, who it is for, what it hooks
with, what it asks, what it must disclose and what it needs cleared. It ends with the brief
agreed, at `status: briefed` with M1 (idea → briefed) recorded, ready for its script or its
recording. It writes no script and touches nothing in the production or publishing layers.

## Directory Tree

```text
scripts/workflows/01-brief-a-piece/
├── CONTEXT.md          ← this file (when to use, what it produces)
├── CLAUDE.md           ← operating rules for this workflow
├── STEPS.md            ← ordered steps to execute
└── CHECKLIST.md        ← verification checklist before marking complete
```

## When to use this

- Before any script, recording, voiceover or cut is made for a new piece. Producing without a
  brief is producing from memory.
- When a talk, interview or conversation has been recorded and is to become a piece: it is
  briefed first, as a recorded piece, and then brought in.
- When a piece's purpose, deliverables or disclosure have to change materially: re-brief the
  existing piece with this procedure, never open a second one.

Reach for a **different** procedure when: the brief is agreed and the next job is the words
(`scripts/workflows/02-write-a-script/`); the piece is recorded and briefed and the next job is
its transcript (`production/workflows/08-bring-in-a-recording/`); the request is a cut-down of a
piece that already exists (`publishing/workflows/01-plan-the-cut-downs/`); or it is a social
media plan, a content calendar or a text-only post (the social-media-documents skill
(syntek-author), where present).

## What it produces, and where

- `scripts/src/pieces/<piece>/` — the piece's folder, with its `CONTEXT.md` and `CLAUDE.md`
  written from the skeleton in `scripts/src/pieces/CLAUDE.md`.
- `scripts/src/pieces/<piece>/brief.md` — the brief, at `status: briefed`, with `M1` dated in
  `verified`.
- A row in `scripts/src/piece-register.md`, added for a new piece or confirmed for a re-brief.
- Decisions that pass the memory gate, recorded in `.claude/MEMORY.md`.

## The failure this procedure exists to prevent

A piece produced from a plan that lived only in the conversation. The next session cannot see
what it was for, the script drifts from the purpose, a deliverable nobody chose gets cut, a
synthetic voice goes out undisclosed, and a stock clip or a face nobody cleared is found only
when the post is ready. A written, agreed brief is what lets a fresh session script, cut and
post the piece without re-deciding what it promised.

## Cross-references

- `scripts/docs/reference/the-piece-ladder.md` — the ladder, M1 and how a gate is recorded.
- `scripts/src/pieces/CLAUDE.md` — the skeletons of a piece folder's pair and of its brief.
- `publishing/docs/reference/ai-disclosure.md` — what the disclosure plan must cover.
- `production/docs/reference/rights-and-consent.md` — what counts as a rights need.
- The grill-with-docs skill (syntek-author), where present — the questioning, the lookup order
  and the memory gate.

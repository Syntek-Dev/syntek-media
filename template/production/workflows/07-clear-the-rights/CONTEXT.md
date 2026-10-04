# CONTEXT.md — production/workflows/07-clear-the-rights/

The procedure for clearing everything a piece uses that someone else owns, or that shows or
sounds like a real person: music, stock, footage of people or private places, a likeness, a
cloned voice, quoted text, a scripture translation, a font, artwork, generated material. Every
item is matched to its row in `production/src/rights-register.md`, its evidence checked against
the use in hand, missing permissions requested by the author, answers recorded, and anything
that cannot be cleared cut or replaced. It is the rights part of M7; it posts nothing, and it
never requests a permission on the author's behalf.

## Directory Tree

```text
production/workflows/07-clear-the-rights/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- A piece is captioned and heading for its post package, and its rights rows are not all
  `cleared`.
- A storyboard has opened `needed` rows, and the author wants to start requesting early.
- A licence is about to expire, or a piece is to be posted again on a new platform.
- A guest, a narrator or a cloned voice needs its release or consent recorded.

Reach for a **different** procedure when the file itself still needs logging
(`production/workflows/01-log-source-media/`), or when the job is the post package
(`publishing/workflows/05-prepare-a-post/`), which checks this procedure's result.

## What it produces, and where

- **Rights rows** in `production/src/rights-register.md`: each item the piece uses, with its
  holder, licence or permission, evidence, expiry and status, and the piece in Pieces.
- **A list of what blocks M7**, handed back to the author: rows not `cleared`, and what was
  cut or replaced because of a refusal.

## The failure this procedure exists to prevent

A piece published with something it had no right to use. A track licensed for one platform posted
on another, a release that never came back, a voice cloned on a verbal yes: each surfaces only
after the piece is live, when the cost is a takedown, a claim or a broken trust. Every permission
is recorded with its evidence before the piece is scheduled, so none is assumed.

## Cross-references

- `production/docs/reference/rights-and-consent.md` — what needs a row, statuses, consent.
- `production/src/rights-register.md` — the register itself.
- `scripts/docs/reference/the-piece-ladder.md` — M7, which needs every row the piece uses
  `cleared`.

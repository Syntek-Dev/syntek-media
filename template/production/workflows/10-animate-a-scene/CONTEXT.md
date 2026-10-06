# CONTEXT.md — production/workflows/10-animate-a-scene/

Draw a scene piece from its accepted voice timings, the author's brand art and indexed real
sources. Review each still and the preview with the author before dating `M4.stills` and M4.

## Directory Tree

```text
production/workflows/10-animate-a-scene/
├── CHECKLIST.md        ← model-tagged review checks
├── CLAUDE.md           ← operating rules
├── CONTEXT.md          ← this file
└── STEPS.md            ← index sources, draw, review and render native masters
```

## When to use this

- The shot list has Type `scene` and the preceding M4 sub-checks hold.
- The author has supplied the art and agreed the storyboard's current timing.
- A stills or preview note has returned from the timing procedure.

## What it produces, and where

- The accepted real index and scene Python in `production/src/scenes/`.
- A fresh ignored page, first/middle board stills, their report and a master per aspect in the
  piece's production renders folder; their paths printed for review.
- Agreed Timing notes, and `M4.stills` and M4 dates once every preceding sub-check holds.

## The failure this procedure exists to prevent

A character standing frozen on guessed timing, or a cropped vertical copy hiding words and
mouths that the author never checked against their approved voice.

## Cross-references

- `production/docs/reference/scenes-as-code.md` — the neutral kit and exact frame clock.
- `production/workflows/09-time-the-voice/` — accepted timing and the route for Timing notes.
- `scripts/docs/reference/the-piece-ladder.md` — ordered sub-checks and their clearing rules.

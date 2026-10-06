# CONTEXT.md — production/workflows/09-time-the-voice/

Time a scene piece's approved joined voice, agree that it says the script, and re-time its
boards before animation. This procedure works towards M4 through `M4.words` and `M4.cues`;
`lipsync` supplies mouth data alongside alignment, but the author first checks its mouths at
`M4.stills` in production/workflows/10-animate-a-scene/. It spends nothing and fetches no models.

## Directory Tree

```text
production/workflows/09-time-the-voice/
├── CHECKLIST.md        ← model-tagged checks, open beside the steps
├── CLAUDE.md           ← operating rules
├── CONTEXT.md          ← this file
└── STEPS.md            ← join, align, lip sync and re-time with the author
```

## When to use this

- The scene piece's takes are approved and archived, and its joined voice needs timing.
- A take was re-rolled, so the old word and mouth timings no longer describe the voice.
- Stills or a preview yielded a Timing note that moves time, keeping M3 and the approved words.

A note replacing a shot or changing words returns to `scripts/workflows/03-storyboard-a-piece/`.
A new take returns first to `production/workflows/02-make-a-voiceover/` for its approval.

## What it produces, and where

- Working timing in the piece's ignored production timing output folder, reported by each command.
- Accepted words/check and mouth JSON in `production/src/timing/`, only through explicit `-o`.
- Accepted `<piece>.cues.json` in `production/src/scenes/`, only through explicit `-o`.
- The author-agreed storyboard re-time, shot Seconds and Timing notes, with its version raised.
- `M4.words` and `M4.cues` recorded in order in the brief; dependent dates cleared by a change.

## The failure this procedure exists to prevent

Animating estimates before hearing and checking the real voice, then mistaking an old timing
file or gate date for approval of a new take. Timing is accepted before it drives the scene.

## Cross-references

- `production/docs/reference/voiceover.md` — the segments, join and offline timing.
- `scripts/docs/reference/storyboards-and-shot-lists.md` — boards, references and the re-time.
- `scripts/docs/reference/the-piece-ladder.md` — M4's ordered sub-checks and clearing rules.

# CONTEXT.md — production/workflows/04-master-a-podcast-episode/

The procedure for an episode's audio master. An audio-only edit decision list (`size = ""`,
`loudness = "podcast"`) is written with the author: clips from a recorded conversation or talk,
or the approved voiceover of a scripted episode, with an intro and outro bed that fades and ducks
under speech. `python3 toolkit/media.py assemble` makes `production/src/renders/<piece>.master.wav`,
which is measured against the podcast target and heard through by the author; M3 is recorded as
`n/a — no picture` and M4 is dated. It does not encode the feed files
(`publishing/workflows/02-cut-for-a-platform/`) or write the episode's description
(`publishing/workflows/05-prepare-a-post/`).

## Directory Tree

```text
production/workflows/04-master-a-podcast-episode/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- A recorded episode's transcript is approved and its recording logged.
- A scripted episode's script is approved and its voiceover (or the host's recorded reading)
  approved and archived.
- An episode is cut from a recorded talk that is also a video piece.
- The author wants a change to an episode's master: a new version of the same list.

Reach for a **different** procedure when the master has a picture
(`production/workflows/03-assemble-the-master/`), or when the episode still needs its transcript
(`production/workflows/08-bring-in-a-recording/`).

## What it produces, and where

- **The audio edit decision list** `production/src/edits/<piece>.toml`, with the author.
- **The master** `production/src/renders/<piece>.master.wav`, git-ignored and regenerable.
- **The brief's** `verified` entries for M3 (`n/a — no picture`) and M4, and its `status`.

## The failure this procedure exists to prevent

An episode that sounds unlike the last one, or that misleads its listeners. Episodes are heard
back to back: a level off target, a bed that starts dead or a missing intro is noticed at once.
And an episode voiced synthetically without a spoken disclosure breaks Apple's guideline for the
whole feed it goes out on.

## Cross-references

- `scripts/docs/reference/podcast-episodes.md` — how an episode is shaped.
- `production/docs/reference/edit-decision-lists.md` — the list, with `size = ""`.
- `production/docs/reference/sound-and-loudness.md` — the podcast target, beds and fades.
- `.claude/skills/cut-for-platform/SKILL.md` — the skill that writes the list and renders.

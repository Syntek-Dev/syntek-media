# CONTEXT.md — production/workflows/08-bring-in-a-recording/

The procedure for turning an existing recording (a talk, an interview, a conversation) into a
piece's script. The recording is logged as source media (copied, never moved), its audio
extracted, and `transcript.md` made in the piece folder: through ElevenLabs speech-to-text only
when the author asks, or from the author's own words. Every beat is anchored to its start on the
recording; the author approves the transcript, which passes M2 for a recorded piece and records
M3 as `n/a — recorded`; then the recording-timed captions are aligned. It does not cut the master
(`production/workflows/03-assemble-the-master/`) or caption any cut-down
(`publishing/workflows/03-caption-a-piece/`).

## Directory Tree

```text
production/workflows/08-bring-in-a-recording/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- A talk, sermon, lecture or interview has been recorded and is to be published or cut down.
- A conversation recorded for a podcast episode needs its transcript before the edit.
- An old recording is to be repurposed into a new piece.

Reach for a **different** procedure when the piece is to be written and then voiced or filmed
(`scripts/workflows/02-write-a-script/`), or when the file is only a source for another piece and
needs no transcript of its own (`production/workflows/01-log-source-media/`).

## What it produces, and where

- **A footage row** for the recording in `production/src/footage/manifest.toml`, and its ID in
  the brief's `source_media`.
- **The transcript** `scripts/src/pieces/<piece>/transcript.md`, beat by beat, anchored on the
  recording, approved by the author.
- **Recording-timed captions** `publishing/src/captions/<piece>.<FID>.en-GB.srt`.
- **A credits-log row** in `production/src/credits-log.md` when speech-to-text was used.
- **The brief's** `verified` entries for M2 and M3, and its `status`.

## The failure this procedure exists to prevent

Words put into a speaker's mouth, or captions that drift away from the voice. A transcript
tidied into what the speaker should have said is no longer a record, and a fact-check run on it
checks the wrong thing; captions aligned over a whole recording without anchors drift a little
more with every minute, until every cut-down inherits the error.

## Cross-references

- `production/docs/reference/recorded-pieces.md` — the transcript, its anchors, the caption chain.
- `production/docs/reference/elevenlabs.md` — the base path, the cost and speech-to-text.
- `scripts/docs/reference/writing-for-the-ear.md` — the format a transcript shares with a script.
- `.claude/skills/captions/SKILL.md` — the skill that runs this procedure.

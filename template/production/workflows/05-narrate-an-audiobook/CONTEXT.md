# CONTEXT.md — production/workflows/05-narrate-an-audiobook/

The procedure for planning an audiobook and voicing it chapter by chapter. The chapter register
and the credits are written and approved first (the piece's M2: an audiobook has no script), and
the route is chosen per channel with the author (`human`, `ai` or `external`). On the AI route
each chapter's text is made by
`python3 toolkit/media.py audiobook text`, costed, voiced one chunk per call through the
user-scope MCP server `elevenlabs`, renamed and logged by `take add`, and heard by the author; on
the human route each recorded chapter is logged as source media; on the external route the
register records the package made outside this template. It masters nothing
(`production/workflows/06-master-an-audiobook/`).

## Directory Tree

```text
production/workflows/05-narrate-an-audiobook/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- The author asks to start an audiobook (its chapters and credits planned), or to voice or record
  its next chapters.
- The author asks to regenerate a part of a chapter, or to re-record one.
- A channel is added, and its route needs choosing.

Never run it unasked. Reach for a **different** procedure when the brief is not yet agreed
(`scripts/workflows/01-brief-a-piece/`), or when the chapters are voiced and need mastering
(`production/workflows/06-master-an-audiobook/`). An audiobook never goes through
`scripts/workflows/02-write-a-script/`.

## What it produces, and where

- **The chapter register** `production/src/audiobook/<piece>.md`: the route per channel, then one
  row per chapter and the credit rows `ch00` and `ch99`, approved as M2; the credits' words in
  `<piece>.ch00.md` and `<piece>.ch99.md` beside it.
- **The brief's** `verified` entries for M2 and M3 (`n/a — no picture`), and its `status`.
- **Chunks and takes** in `production/src/audiobook/generated/`, git-ignored: chapter text never
  enters a tracked file.
- **Footage rows** for each human recording, and for any take the author wants archived.
- **Credits-log rows** in `production/src/credits-log.md`, one per call, written by `take add`.

## The failure this procedure exists to prevent

An audiobook made for a channel that will not take it, or paid for twice. ACX and Audible take
human narration unless the author is authorised otherwise, and some channels take synthetic
narration only as ElevenLabs' own package, so a route chosen too late wastes a whole book of
credits. And a chapter cannot be voiced again the same way, so its approved master is archived
(`production/workflows/06-master-an-audiobook/`).

## Cross-references

- `production/docs/reference/audiobook-narration.md` — the routes, the channels, chapter text.
- `production/docs/reference/elevenlabs.md` — the call discipline every take follows.
- `production/src/audiobook/` — the register, and the git-ignored chunks and takes.
- `.claude/skills/narrate-audiobook/SKILL.md` — this procedure in skill form.

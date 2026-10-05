# CONTEXT.md — production/workflows/02-make-a-voiceover/

The procedure for making a piece's voiceover through ElevenLabs, on the author's request. The
approved script is split into segments, one per spoken sentence or short beat; each is voiced
with the brand's recorded narrator and model through the user-scope MCP server `elevenlabs`, one
call at a time, renamed and logged the moment it lands by `python3 toolkit/media.py take add`,
heard by the author, and archived once approved. The offline plan states characters and calls
before spending anything; it writes no rate and edits no register.
It does not write or change the script (`scripts/workflows/02-write-a-script/`) and does not
assemble the master (`production/workflows/03-assemble-the-master/`).

## Directory Tree

```text
production/workflows/02-make-a-voiceover/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- The author asks for a voiceover for a scripted piece: an explainer, a trailer, an episode's
  narration, or a piece that is only a voiceover.
- The author asks to regenerate a segment, or to hear another take of one.
- The author asks for a scratch or timing track before a voice is chosen or paid for.

Never run it unasked. Reach for a **different** procedure when the script is not yet approved
(`scripts/workflows/02-write-a-script/`), when the piece is a recording
(`production/workflows/08-bring-in-a-recording/`), or when the job is an audiobook's chapters
(the narrate-audiobook skill, where the project makes audiobooks).

## What it produces, and where

- **The segment register** `production/src/voiceover/<piece>.toml`: one row per segment, with
  its script lines, words, request, take, file, characters, pause and status.
- **Takes** in the piece's `production/src/voiceover/generated/<piece>/takes/`, named
  `<piece>.sNN.tN.mp3` (`.pcm` for a raw format), git-ignored; a scratch track beside that
  folder in `generated/<piece>/`, never among the takes.
- **Credits-log rows** in `production/src/credits-log.md`, one per call, written by `take add`.
- **The narrator record** in `brand/src/voice/voice.md`, the first time.
- **Archived takes:** each approved take logged in `production/src/footage/manifest.toml`.
- **Joined voice:** `voice join` writes a mono 16-bit WAV at the register's rate to
  `production/src/renders/<piece>/<piece>.voice.wav`, in register order with pauses.
- **For a scene piece:** `M4.takes` dated in its brief after approval and archiving.

## The failure this procedure exists to prevent

Spending the author's credits without a yes, and losing what was paid for. Every call costs
credits, so a batch is costed and waits for the author's word; the server names a file by the
second and can overwrite one, so each take is renamed and logged the moment it lands; and a take
cannot be made again, so an approved one is archived before a master depends on it.

## Cross-references

- `production/docs/reference/voiceover.md` — segments, the register, and script to request.
- `production/docs/reference/elevenlabs.md` — the server, the base path, cost, calls, fallback.
- `brand/src/voice/voice.md` — the narrator, the model and the pronunciations.
- `.claude/skills/voiceover/SKILL.md` — this procedure in skill form.

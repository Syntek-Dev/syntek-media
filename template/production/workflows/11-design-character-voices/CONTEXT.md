# CONTEXT.md — production/workflows/11-design-character-voices/

The procedure for designing a character's voice from the author's own cloned voice, on the
author's request. Each character's description is drafted from the manuscript or the script and
agreed with the author; `python3 toolkit/media.py voice remix plan` builds the one request
offline, and `voice remix run --approve-call` sends it to ElevenLabs, the one call the toolkit
makes to it directly, writing the previews into a voice-trial folder. The author listens and
chooses; the chosen preview is saved as a voice through the user-scope MCP server `elevenlabs`;
and the character's row is recorded in `brand/src/voice/voice.md`, its consent the source
clone's. It does not voice a piece (`production/workflows/02-make-a-voiceover/`), and it never
clones a voice: the clone and its consent come first.

## Directory Tree

```text
production/workflows/11-design-character-voices/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- The author asks for a character's own voice: 'design a voice for the ferrywoman', 'remix my
  voice for a character', 'make the narrator's voice older for the grandfather'.
- The author wants to hear another remix of a character's voice before choosing one.
- The author wants to hear a saved character voice say a few lines before it voices a piece.

Never run it unasked. Reach for a **different** procedure when the job is voicing a piece's lines
(`production/workflows/02-make-a-voiceover/`), when the author's own clone or its consent is not
yet recorded (`brand/workflows/05-write-the-spoken-voice/`), or when the question is how a
character's written dialogue reads (the character-voice skill (syntek-author), where present).

## What it produces, and where

- **Remix previews** in `production/src/voiceover/generated/voice-trials/<name>/`, named
  `<name>.pNN.mp3`, beside `<name>.remix.json`, which records the date, the source voice, the
  description, the text and each preview's `generated_voice_id`; git-ignored, never a take.
- **A credits-log row** in `production/src/credits-log.md` for each remix run, written by
  `voice remix run` itself, with `—` for the piece; one for each save or trial call, written by
  the `voiceover` skill.
- **A saved voice** in the author's ElevenLabs account, made from the preview the author chose.
- **The character's row** in `brand/src/voice/voice.md`: Use `character:<name>`, the saved
  voice and its ID, the model and settings, and, in Consent, the source clone's rights ID.
- **Optionally, a voice trial** of the saved voice on a few lines, in its own voice-trial folder.

## The failure this procedure exists to prevent

A character voice nobody consented to, paid for without a yes, or chosen and then lost. A remix
is made only from the author's own clone with its consent cleared; the call is planned, stated
and approved before it is sent; and the preview the author chose is saved and recorded at once,
because a preview that is not saved cannot be made again.

## Cross-references

- `production/docs/reference/character-voices.md` — descriptions, remixing, choosing and saving.
- `production/docs/reference/elevenlabs.md` — the server, the base path, cost and one call at a time.
- `brand/src/voice/voice.md` — the source clone's row and every character's row.
- `production/src/rights-register.md` — the source clone's `voice-consent` row.
- `.claude/skills/voiceover/SKILL.md` — the skill that runs this procedure.

# CONTEXT.md — brand/src/voice/

How the brand sounds when it is heard: one file, `voice.md`, holding the spoken style, the
narrator chosen for each use and every pronunciation a narrator needs. The `voiceover` skill
reads it before every call and uses exactly what it records, so two pieces voiced months apart
sound like one brand. The written voice is not here: where syntek-author is applied, it lives in
that template's voice files, and `voice.md` cites them in one line.

## Directory Tree

```text
brand/src/voice/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
└── voice.md            ← seed: spoken style, narrators, pronunciations
```

## What's here

- `voice.md` — four sections: `## Spoken style` (pace in words a minute, register, how the brand
  name is said, words never said aloud), `## Written voice` (one line pointing to the written
  voice, where present), `## Narrators` (one row per use: `voiceover`, `narration`,
  `podcast-host`, `character:<name>`) and `## Pronunciations` (word, IPA, respelling, source).
  **It is the only file in the project that holds a voice ID.**
- The `Use` of each narrator row is what a voiceover's segment register names as its
  `voice_use`, so a register always points at one recorded narrator.

## Cross-references

- `brand/docs/reference/the-spoken-voice.md` — spoken against written, narrators, consent.
- `brand/workflows/05-write-the-spoken-voice/` — the procedure that settles the voice.
- `production/docs/reference/elevenlabs.md` — the server, models, credits and the fallback.
- `production/src/rights-register.md` — the recorded consent behind any cloned voice.

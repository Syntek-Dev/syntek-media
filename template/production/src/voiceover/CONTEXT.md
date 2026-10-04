# CONTEXT.md — production/src/voiceover/

One segment register per piece, recording its voiceover from script line to approved take: each
segment's words, the request sent to ElevenLabs, the take, the file, the characters billed, the
pause after it and its status. The takes themselves sit in
`production/src/voiceover/generated/`, git-ignored. `assemble` joins a register's approved
segments into the voice track, and `captions from-segments` times captions from them exactly.

## Directory Tree

```text
production/src/voiceover/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules and the register skeleton
├── <piece>.toml        ← one piece's segment register, named for its piece folder
└── generated/          ← the takes, <piece>.sNN.tN.mp3 (git-ignored; README only)
```

## What's here

- `<piece>.toml` — a `[voiceover]` table (the piece, the narrator's use in
  `brand/src/voice/voice.md`, the model, the output format, the cue rule), then one `[[segment]]`
  per spoken sentence or short beat. **`production/docs/reference/voiceover.md` explains every
  field**; the voiceover skill writes the register and `python3 toolkit/media.py take add`
  fills each segment's `take` and `file`.
- `production/src/voiceover/generated/` — every take, renamed by `take add` the moment it lands.
  Ignored by `production/src/.gitignore`; an approved take is archived as source media.
- This folder ships with every project, whatever its media kinds: every brand narrates
  something.

## Cross-references

- `production/workflows/02-make-a-voiceover/` — the procedure that fills a register.
- `production/docs/reference/elevenlabs.md` — the call discipline every take follows.
- `production/src/credits-log.md` — the row each take's call writes.
- `production/src/edits/` — where a register is used, as `vo:<piece>`.

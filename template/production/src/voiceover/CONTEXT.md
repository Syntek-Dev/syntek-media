# CONTEXT.md — production/src/voiceover/

One segment register per piece, recording its voiceover from script line to approved take: each
segment's words, the request sent to ElevenLabs, the take, the file, the characters billed, the
pause after it and its status. The takes themselves sit in the piece's own folder in
`production/src/voiceover/generated/`, git-ignored. `assemble` joins a register's approved
segments into the voice track using the same join as `voice join`, and `captions from-segments`
times captions from them exactly. `speak plan` prints requests offline without changing a row.

## Directory Tree

```text
production/src/voiceover/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules and the register skeleton
├── <piece>.toml        ← one piece's segment register, named for its piece folder
└── generated/          ← <piece>/takes/ holds a piece's takes, <piece>.sNN.tN.mp3 (git-ignored; README only)
```

## What's here

- `<piece>.toml` — a `[voiceover]` table (the piece, the narrator's use in
  `brand/src/voice/voice.md`, the model, the output format, the cue rule), then one `[[segment]]`
  per spoken sentence or short beat. **`production/docs/reference/voiceover.md` explains every
  field**; the voiceover skill writes the register and `python3 toolkit/media.py take add`
  fills each segment's `take` and `file`, and resets its `status` to `generated` and `archived`
  to empty, because a new take is unheard and unarchived.
- `production/src/voiceover/generated/` — a folder per piece: its takes in `<piece>/takes/`,
  each renamed by `take add` the moment it lands, and its espeak-ng scratch tracks in
  `<piece>/` itself; voice trials, which no piece owns, in `voice-trials/<name>/`. Ignored by
  `production/src/.gitignore`; an approved take is archived as source media.
- **A take an earlier release left flat** at the top of `generated/` stays where it is: its row's
  `file` names it, every reader opens the path the row names, and `take add` numbers the next
  take after the highest in either place.
- This folder ships with every project, whatever its media kinds: every brand narrates
  something.

## Cross-references

- `production/workflows/02-make-a-voiceover/` — the procedure that fills a register.
- `production/docs/reference/elevenlabs.md` — the call discipline every take follows.
- `production/src/credits-log.md` — the row each take's call writes.
- `production/src/edits/` — where a register is used, as `vo:<piece>`.

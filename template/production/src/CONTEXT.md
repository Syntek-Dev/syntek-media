# CONTEXT.md — production/src/

The material every master is made from, and the records that make it reproducible: one manifest
of every source file, one register of every licence and consent, one log of every credit spent,
and per piece a segment register, an edit decision list and its cards, and for a scene piece its
timing and scene files. The tracked files are small and flat, each under its piece's name;
footage lives in external storage, and renders and generated audio are git-ignored, in a folder
per piece. The brief, script and storyboard a master follows live in `scripts/src/pieces/`, not
here.

## Directory Tree

```text
production/src/
├── CONTEXT.md              ← this file
├── CLAUDE.md               ← operating rules and the writer table
├── .gitignore              ← keeps renders, the footage mirror and generated audio out of Git
├── credits-log.md          ← seed: one row per credit-spending call, written as the call is made
├── rights-register.md      ← seed: every licence, release and consent, RR0001 onwards
├── assets/                 ← small committed images and text captures, under 10 MB each
<: if 'audiobook' in MEDIA_KINDS :>├── audiobook/              ← <piece>.md chapter registers; generated/ and renders/ (README only)
<: endif :>├── cards/                  ← <piece>.<card>.html title and end cards from the brand's component
├── edits/                  ← <piece>.toml edit decision lists, from which masters are assembled
├── footage/                ← manifest.toml (seed): every source file; raw/ is the ignored local mirror
├── renders/                ← <piece>/: its masters, joined voice, extracts, card PNGs and working copies (git-ignored; README only)
├── scenes/                 ← a scene piece's <piece>.cues.json and .real.json (through -o) and <piece>.scene.py
├── timing/                 ← a piece's <piece>.words.json, .words-check.md and .mouth.json (through -o)
└── voiceover/              ← <piece>.toml segment registers; generated/<piece>/takes/ holds the takes (README only)
```

## What's here

- `production/src/footage/manifest.toml` — **the one list of every source file**: camera
  footage, recorded audio, music beds, stock, images and archived takes, each with a permanent
  footage ID, a checksum and the location of its master copy.
- `production/src/rights-register.md` — **the one record of what each piece may use.** It ships
  empty; `storyboard` opens rows and the author clears them.
- `production/src/credits-log.md` — every credit-spending call, whichever skill made it.
- `production/src/voiceover/` — one segment register per piece, and the takes, git-ignored, in
  a folder per piece.
- `production/src/edits/` and `production/src/cards/` — what `assemble` builds a master from.
- `production/src/timing/` and `production/src/scenes/` — a piece's tracked timing (its words,
  the words check and its mouth cues) and a scene piece's cue index, real index and scene file:
  flat under the piece's name, each tool-written file reaching here only through `-o`.
- `production/src/assets/` — small images and text captures, committed; captures have home paths and host names removed.
- `production/src/renders/` — git-ignored and regenerable, a folder per piece: its masters, its
  joined voice, its extracts, its card PNGs and the working copies of its timing and scene files;
  at the top only what no piece owns (an extract of a footage file, and brand-kit proofs, each
  set in a dated folder of `proofs`).
<: if 'audiobook' in MEDIA_KINDS :>- `production/src/audiobook/` — one chapter register per audiobook; chapter text chunks, takes
  and mastered chapters, git-ignored.
<: endif :>- `production/src/.gitignore` — template-owned. It ships with every project, so generated audio
  and renders stay out of Git even after a media kind is turned off.

The seeds ship with headings and writing rules but no entries. `copier update` recreates a seed
you delete and never touches one you have edited.

## Cross-references

- `production/docs/reference/source-media.md` — the manifest and the mirror.
- `production/docs/reference/edit-decision-lists.md` — the edit decision list, field by field.
- `production/docs/reference/rights-and-consent.md` — the register and its statuses.
- `production/docs/reference/elevenlabs.md` — how a credit is spent, and logged.
- `production/docs/reference/voiceover.md` — segments, takes, and timing the joined voice.
- `scripts/src/pieces/` — the briefs, scripts, transcripts, storyboards and shot lists.

# CONTEXT.md — production/

The production layer: everything a piece's master is made from, and the master itself. Source
footage, recorded sound, music beds and archived takes are logged here; voiceover is generated
here, one segment per spoken sentence or beat; the edit decision lists, the cards and the rights
register live here; and `python3 toolkit/media.py assemble` turns them into a master. This layer
does **not** hold the brief, the script or the storyboard (those are `scripts/`), the cut-downs,
captions, thumbnails and posts made from a master (`publishing/`), or the brand's tokens and
spoken voice (`brand/`).

## Directory Tree

```text
production/
├── CONTEXT.md                  ← this file
├── CLAUDE.md                   ← operating rules for the layer
├── docs/                       ← guides: source media, edits, sound, rights, ElevenLabs, voiceover
│   ├── reference/              ← template-owned guides, updated by copier update
│   └── project/                ← your own guides; a same-named file overrides reference/
├── src/                        ← the material and its registers; renders and audio stay out of Git
│   ├── .gitignore              ← keeps renders, the footage mirror and generated audio out of Git
│   ├── credits-log.md          ← seed: one row per credit-spending call
│   ├── rights-register.md      ← seed: every licence, release and consent a piece relies on
│   ├── assets/                 ← small committed stills, logos and graphics
<: if 'audiobook' in MEDIA_KINDS :>│   ├── audiobook/              ← a chapter register per audiobook; generated/ and renders/ ignored
<: endif :>│   ├── cards/                  ← title and end cards, copied from the brand's card component
│   ├── edits/                  ← one edit decision list per piece
│   ├── footage/                ← manifest.toml (seed): every source file; raw/, the ignored mirror
│   ├── renders/                ← a folder per piece: masters, the joined voice, card PNGs (git-ignored)
│   ├── scenes/                 ← a scene piece's cue index, real index and scene code
│   ├── timing/                 ← a piece's word timings, words check and mouth cues
│   └── voiceover/              ← one segment register per piece; generated/ is ignored, a folder per piece
└── workflows/                  ← the procedures, one folder per production job
    ├── NN-verb-first-name/     ← template procedures: CONTEXT · CLAUDE · STEPS · CHECKLIST
    └── local/                  ← your own procedures; a same-slug local workflow wins
```

## What's here

- `production/docs/reference/` — the guides: `source-media.md`, `edit-decision-lists.md`,
  `sound-and-loudness.md`, `rights-and-consent.md`, `elevenlabs.md`, `voiceover.md` and
  `recorded-pieces.md` for every project<: if 'audiobook' in MEDIA_KINDS :>, and
  `audiobook-narration.md` for audiobooks<: endif :>.
- `production/docs/project/` — your own guides. The template ships only the folder's pair.
- `production/src/` — the material. **`production/src/footage/manifest.toml` is the one list of
  every source file**, and **`production/src/rights-register.md` the one record of what each
  piece may use**; `production/src/credits-log.md` shows every credit spent. A piece's timing
  and a scene piece's indexes and code sit flat in `production/src/timing/` and
  `production/src/scenes/`. Renders and generated audio stay out of Git
  (`production/src/.gitignore`), in a folder per piece.
- `production/workflows/` — one procedure per production job, numbered and frozen: log source
  media, make a voiceover, assemble the master,
<: if 'podcast' in MEDIA_KINDS :>  master a podcast episode,
<: endif :><: if 'audiobook' in MEDIA_KINDS :>  narrate an audiobook, master an audiobook,
<: endif :>  clear the rights, bring in a recording.

## Cross-references

- `.claude/rules/syntek-media/01-layout-and-routing.md` — the layer table, the piece, the pair
  rule and the ownership classes this layer follows.
- `.claude/rules/syntek-media/03-production-ethics.md` — who decides, credits, disclosure, and
  rights and consent.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` — the toolkit commands this layer runs.
- `scripts/src/pieces/` — the brief, the script or transcript, the storyboard and the shot list
  a master is made from.
- `scripts/docs/reference/the-piece-ladder.md` — the gates; this layer's work ends at M4.
- `publishing/` — where a master goes next: cut-downs, captions, thumbnails and posts.

# CONTEXT.md — production/src/footage/

Every source file a piece is cut from (camera footage, recorded audio, music beds, stock, images
and archived takes) listed once in `production/src/footage/manifest.toml`, with its checksum and
the location of its master copy. The files themselves live in external storage by decision;
`production/src/footage/raw/` is this machine's git-ignored mirror of the ones it needs. Small
committed stills and logos belong in `production/src/assets/`, and exported brand designs in
`brand/src/exports/`, not here.

## Directory Tree

```text
production/src/footage/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules and the table skeleton
├── manifest.toml       ← seed: one [[file]] table per source file, F0001 onwards
└── raw/                ← the local mirror (git-ignored; README only)
```

## What's here

- `production/src/footage/manifest.toml` — **the one list of every source file.** Each table
  carries `id`, `path`, `kind`, `sha256`, `bytes`, `duration`, `location`, `recorded`, `rights`
  and `notes`; `production/docs/reference/source-media.md` explains each.
  `python3 toolkit/media.py footage add` copies a file into the mirror (it never moves the
  original), measures it and appends its table; it refuses a file whose hash is already listed.
- `production/src/footage/raw/` — the mirror. Everything in it but its README is ignored by
  `production/src/.gitignore`; `python3 toolkit/media.py footage verify` proves it against the
  manifest, fails on a changed byte or an unlisted file, and lists the entries not mirrored here.
- **Every kind of source sits here:** a recorded talk that becomes a piece, a music bed under a
  trailer, a stock clip, and each approved ElevenLabs take or mastered chapter, which cannot be
  made again once lost.

## Cross-references

- `production/workflows/01-log-source-media/` — the procedure that logs a file.
- `production/workflows/08-bring-in-a-recording/` — a recording logged as a piece's source.
- `production/docs/reference/source-media.md` — why footage lives outside Git, field by field.
- `production/src/rights-register.md` — the rights row a licensed or identifiable file cites.
- `production/src/edits/` — the edit decision lists that cite footage by ID.

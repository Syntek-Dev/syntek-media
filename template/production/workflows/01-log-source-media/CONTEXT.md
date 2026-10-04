# CONTEXT.md — production/workflows/01-log-source-media/

The procedure for logging a source file so that an edit can name it: camera footage, a recorded
talk or interview, a music bed, stock, an image. Each file is copied (never moved) into the
git-ignored local mirror, hashed and measured by `python3 toolkit/media.py footage add`, given a
permanent footage ID in `production/src/footage/manifest.toml`, its master copy's location
recorded and its rights row linked; the run ends with `footage verify`. It does not edit, trim or
re-encode anything, and it does not open a recording as a piece of its own
(`production/workflows/08-bring-in-a-recording/` does that, through the same command).

## Directory Tree

```text
production/workflows/01-log-source-media/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- New footage arrives from a shoot, or a recording from a session, before any edit names it.
- The author licenses a music bed, a stock clip or an image for a piece.
- The project moves to another machine, and the mirror needs checking or fetching.
- An approved take or master needs archiving outside the skill that made it.

Reach for a **different** procedure when the recording is itself a piece: a talk, interview or
conversation to be transcribed and cut (`production/workflows/08-bring-in-a-recording/`). The
voiceover skill archives its own approved takes as it goes, and the audiobook skill, where the
project makes audiobooks, its approved masters.

## What it produces, and where

- **Manifest rows** in `production/src/footage/manifest.toml`: footage ID, path, kind, checksum,
  size, duration, location label, recorded date, rights ID and notes.
- **Copies** in `production/src/footage/raw/`, git-ignored; the originals stay where they were.
- **Rights rows** opened as `needed` in `production/src/rights-register.md` for any file that is
  licensed or shows people or private places, where none existed.

## The failure this procedure exists to prevent

An edit made from a file nobody can find again. Footage lives outside Git, so the manifest is the
only record of what a master was cut from: a file logged without its location cannot be fetched
on another machine, a file without its checksum can be swapped silently for a different take,
and a licensed file without its rights row reaches a post uncleared.

## Cross-references

- `production/docs/reference/source-media.md` — why footage lives outside Git, field by field.
- `production/docs/reference/rights-and-consent.md` — which files need a rights row.
- `production/src/footage/` — the manifest and the mirror.

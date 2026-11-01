@./CONTEXT.md

# CLAUDE.md — production/src/footage/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/src/CONTEXT.md` → `production/src/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep a checked, permanent record of every file a master is cut from, so every edit can be rebuilt
on any machine and every source traced to its rights.

## How to work here

- **Routing:** workflow `production/workflows/01-log-source-media/`, or
  `production/workflows/08-bring-in-a-recording/` for a recording that becomes a piece; guide
  `production/docs/reference/source-media.md`; commands `python3 toolkit/media.py footage add`
  and `footage verify`. A skill archiving an approved take runs the same command. On a data
  root, the resolver's `add` that a `footage verify` warning names files a copy
  (`.claude/rules/syntek-media/06-global-rules.md` Section 12).
- **Model:** **Opus** for deciding what a file is, where its master copy lives and whether it
  needs a rights row; the mechanical tier for running the toolkit and filling a row the author
  has already decided (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the file and its kind → find or open its rights row → agree the
  location label → `footage add` → fill `recorded` and `notes` with the author →
  `footage verify`.
- **Definition of done:** the file has a footage ID, a checksum and a location label;
  `footage verify` passes; a licensed or identifiable file names its rights ID.

## Guardrails

- **IDs are permanent.** An edit decision list cites a footage ID; renumbering one breaks every
  master cut from it.
- **Copy, never move.** `footage add` copies a file into the mirror; the original stays where it
  was until the author has backed it up at its location.
- **Never edit, trim or re-encode a file in the mirror.** A derived file is a render, made by the
  toolkit; a changed byte fails `footage verify`.
- **Never commit footage**, and never force a file past `production/src/.gitignore`.
- **A location is a label, never a secret.** Name the drive, the NAS or the cloud folder; never
  paste a link that carries a token.
- **Never overwrite a table.** A correction is noted in `notes` with its date; a re-recorded take
  is a new file with a new ID.
- **File on a data root only on the author's word,** with the resolver's `add` and the role
  `footage`, or `approved-take` for a `generated` file, never another role; tell the author media
  files its footage under those two alone. A filed copy is evidence and is never replaced; never
  edit the resolver's storage manifest, and never work round a refusal.

## Output & naming

- **Seeded:** `manifest.toml`, header comments only; `copier update` restores it empty if it is
  deleted and never touches it once filled.
- **Written by the toolkit (with the author):** one table per file, appended by `footage add`;
  the author fills `recorded` and `notes`:

```toml
[[file]]
id = "F0001"                 # permanent, never reused
path = "raw/<file name>"     # relative to production/src/footage/; footage add copies the file here
kind = "video"               # video | audio | music | stock | image | generated
sha256 = ""                  # written by footage add
bytes = 0                    # written by footage add
duration = 0.0               # seconds; 0.0 for an image
location = ""                # where the master copy lives: a label, never a secret URL
recorded = ""                # DD/MM/YYYY
rights = ""                  # RRNNNN when licensed or showing people
notes = ""                   # generated: the take or chapter it archives
```

- **Written by the resolver (never hand-edit):** the storage manifest in this folder, where the
  project keeps its files on a data root, one row per filed copy, committed.
- **Generated (never hand-edit):** nothing else tracked; the mirror's files are ignored.

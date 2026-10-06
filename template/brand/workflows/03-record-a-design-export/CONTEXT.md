# CONTEXT.md — brand/workflows/03-record-a-design-export/

The short procedure for filing a design asset exported from Claude Design, or made from one: a
logo, a cover, a background plate, a lower-third, a print file. It decides the file's folder by
its size, makes sure Git LFS is ready before a large file goes in, names the file so nothing is
overwritten, and writes its row in the design register with the design's link. When the author
approves a revision, it moves every live reference to it and keeps the original for reference. It
never edits the design, and it never touches footage or renders.

## Directory Tree

```text
brand/workflows/03-record-a-design-export/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- The author has exported a design and wants it in the repository.
- A revised version of an earlier export replaces it, or the author approves a revision already
  filed, and the files that name the original must move to it.
- A podcast show's cover is ready, or a partner site wants an image in its own branding: both are
  exports, encoded here for their deliverables.
- `python3 toolkit/media.py check` reports a large file outside the LFS folder, or a file in it
  stored as a plain blob.

Reach for a **different** procedure when the file is recorded or licensed footage, a music bed
or an approved take (`production/workflows/01-log-source-media/`), or when the change is to the
kit itself (`brand/workflows/01-set-up-the-brand-kit/`).

## What it produces, and where

- **The file**, in `brand/src/exports/` (10 MB or less) or `brand/src/exports/large/` (over
  10 MB, stored by Git LFS), under a kebab-case name no other export uses.
- **Its row** in `brand/src/design-register.md`: design, Claude Design link, export path,
  storage, date exported, and the rights IDs of anything licensed in it.
- **A superseded mark** on the row of any export it replaces; the original file stays beside its
  revision for reference.
- **The moved references**, once the author approves a revision: every live file that named the
  original names the revision, and the hand-back lists what was moved and what was left.

## The failure this procedure exists to prevent

A large file committed whole into plain Git, where it stays in every clone for ever; a revision
saved over the export a published piece still uses; or an approved revision that half the brand's
files never switch to. The size test and the LFS check come before the file is added, because
neither of the first two mistakes can be undone by a later commit; the register row comes with it,
because an export with no link and no date cannot be traced or replaced with confidence; and the
references move in one listed pass, agreed with the author, so none is missed.

## Cross-references

- `brand/docs/reference/design-exports.md` — small and large, the tripwire, and the register.
- `brand/src/exports/large/` — the LFS folder and its `.gitattributes`.
- `production/src/rights-register.md` — the rows for anything licensed in an export.

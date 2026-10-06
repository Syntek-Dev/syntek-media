@./CONTEXT.md

# CLAUDE.md — brand/src/exports/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/src/CONTEXT.md` → `brand/src/CLAUDE.md` → this folder's `CONTEXT.md` (imported above)
→ this file.

## Purpose (one line)

Keep the brand's exported design assets in Git, each one registered, so a piece can use them and
a later design can supersede them without losing the record.

## How to work here

- **Routing:** workflow `brand/workflows/03-record-a-design-export/`; guide
  `brand/docs/reference/design-exports.md`.
- **Model:** **Opus** for deciding with the author what an export is and whether it supersedes
  another; the mechanical tier for filing it and writing its register row
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the design and its link with the author → check the file's size
  → 10 MB or less: here; over 10 MB: `large/` → name it → register row →
  `python3 toolkit/media.py check`.
- **Definition of done:** the file is in the right folder under a name no other export uses,
  its register row is complete, and `media.py check` reports nothing about it.

## Guardrails

- **Never overwrite an export.** A revised design is a new file under a new name; the old row is
  marked superseded with the date.
- **Over 10 MB goes in `large/`.** A large file committed here sits in plain Git for ever, in
  every clone.
- **Every export is registered.** A file with no row in `brand/src/design-register.md` has no
  link back to its design and no date.
- **Licensed content is cleared first.** An export that carries a licensed font, image or
  piece of music has its rows in `production/src/rights-register.md` before a piece using it is
  scheduled.
- **No secret goes in a file name.** A Claude Design link belongs in the register's link column,
  never in a name or a note here.

## Output & naming

- **Hand-written (by the author, or filed with Claude):** `<design>.<ext>`, kebab-case, with a
  variant suffix where one design has several (`<design>-<variant>.<ext>`).
- **Sprites:** `<sprite>-<pose>-mouth-<shape>` whole frames, or `<sprite>-<pose>` and a
  `<sprite>-mouth-<shape>` layer at the recorded native mouth origin; shapes a–h/x. Optional
  `<sprite>-<pose>-blink` overlays the pose. Register every art file and its scale/origin notes.
- **Not here:** renders (`production/src/renders/`, `publishing/src/renders/`), footage
  (`production/src/footage/`).
- **Generated (never hand-edit):** nothing here.

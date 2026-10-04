@./CONTEXT.md

# CLAUDE.md — brand/workflows/03-record-a-design-export/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/workflows/CONTEXT.md` → `brand/workflows/CLAUDE.md` → this folder's `CONTEXT.md`
(imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

File each exported design asset where its size says, stored the way Git can bear, and
registered with its link, so it can be used, traced and superseded safely.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative: `opus` items are judgement; `sonnet` items belong to the mechanical tier.

- **Routing:** no skill; this is record-keeping, done with the author against
  `brand/docs/reference/design-exports.md`. Checks: `python3 toolkit/media.py check`, and for a
  large file `git lfs version`, `git config --get filter.lfs.process` and `git check-attr`.
- **Model:** the mechanical tier for measuring, filing, checking and writing the row; **Opus**
  for deciding with the author whether an export supersedes another and what rights it carries
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the export and its link → check its rights → measure it and choose
  its folder → for a large file, check LFS first → name and place it → write the register row →
  run the checks → hand back.
- **Definition of done:** the file is in the folder its size requires, under a name no other
  export uses; a large file is stored as an LFS pointer; its register row is complete; and
  `media.py check` reports nothing about it.

## Guardrails

- **Never overwrite an export.** A revision is a new file and a new row; the old row is marked
  superseded with the date, because a published piece may still use the old file.
- **Over 10 MB goes in the LFS folder, and only once LFS is ready.** A large file committed
  without LFS sits in plain Git history for ever.
- **If `git add` fails with `clean filter 'lfs' failed`, the tripwire is working.** The fix is
  git-lfs and `git lfs install`; never unset `filter.lfs.required` or move the file to get past
  it.
- **Never run `git lfs track`.** It writes a root `.gitattributes`, a shared file no template
  seeds.
- **The link comes from the author.** Never guess a Claude Design link, and never write one
  anywhere but the register.

## Output & naming

- **Produces:** `<design>.<ext>` (or `<design>-<variant>.<ext>`) in `brand/src/exports/` or
  `brand/src/exports/large/`.
- **Also writes:** the export's row in `brand/src/design-register.md`, and a superseded mark on
  any row it replaces.
- **Does not touch:** the kit, footage, renders, or any piece's files.

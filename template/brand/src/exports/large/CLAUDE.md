@./CONTEXT.md

# CLAUDE.md — brand/src/exports/large/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/src/CONTEXT.md` → `brand/src/CLAUDE.md` → `brand/src/exports/CONTEXT.md` →
`brand/src/exports/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep the brand's large exports in Git LFS, never as whole files in plain Git history.

## How to work here

- **Routing:** workflow `brand/workflows/03-record-a-design-export/`; guide
  `brand/docs/reference/design-exports.md`; readiness through
  `brand/workflows/06-check-the-setup/`.
- **Model:** the mechanical tier for checking LFS, filing the file and writing its row; **Opus**
  for anything the author must decide (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** `git lfs version` and `git config --get filter.lfs.process` (or
  `filter.lfs.clean`) → if either is empty, stop: the author installs git-lfs and runs
  `git lfs install` → place the file → `git check-attr filter -- <path>` reports `lfs` →
  register row with Storage `lfs` → `python3 toolkit/media.py check`.
- **Definition of done:** the file is stored as an LFS pointer, its register row says `lfs`, and
  `media.py check` reports no plain blob here.

## Guardrails

- **If `git add` fails with `clean filter 'lfs' failed`, the tripwire is working.** Install
  git-lfs and run `git lfs install`; never unset `filter.lfs.required`, and never move the file
  out of this folder to get past it.
- **Never run `git lfs track`.** It writes a root `.gitattributes`, a shared file no template
  seeds; this folder's own `.gitattributes` already does the job.
- **Never edit `.gitattributes` here.** It is template-owned, and its three exemptions keep it
  and this pair readable as text.
- **Never overwrite a large export.** A revision is a new file and a new row; LFS keeps every
  version, and the quota counts them all.

## Output & naming

- **Hand-written (by the author, or filed with Claude):** `<design>.<ext>`, kebab-case.
- **Template-owned:** `.gitattributes`, this pair.
- **Generated (never hand-edit):** nothing here.

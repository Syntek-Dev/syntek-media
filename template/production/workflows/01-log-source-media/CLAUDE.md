@./CONTEXT.md

# CLAUDE.md — production/workflows/01-log-source-media/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md`
open).

## Purpose (one line)

Give every source file a permanent ID, a checksum and a known home before any edit depends on it.

## How to work here

- **Routing:** no skill; this is a logging procedure. Guide
  `production/docs/reference/source-media.md`; commands `python3 toolkit/media.py footage add`
  and `footage verify`.
- **Model:** **Opus** for deciding what a file is, where its master copy lives and whether it
  needs a rights row; the mechanical tier for running the toolkit and filling the rows the author
  has decided (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are
  authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm what
  is coming in → check the rights → agree the location → add each file → verify the mirror →
  hand back.
- **Definition of done:** every file has its manifest row with a checksum and a location label,
  every licensed or identifiable file names its rights row, and `footage verify` passes.

## Guardrails

- **Copy, never move.** `footage add` copies a file into the mirror; the original stays where it
  is until the author has it safe at its location.
- **A location is a label, never a secret.** Never paste a link that carries a token.
- **A duplicate is reported, not logged twice.** `footage add` refuses a hash already listed:
  give the author the existing footage ID instead.
- **Never edit the manifest to make `footage verify` pass.** A mismatch means the file changed;
  report it.
- **Never commit footage**, and never force a file past `production/src/.gitignore`.

## Output & naming

- **Produces:** one `[[file]]` table per file in `production/src/footage/manifest.toml`, IDs
  `F0001` onwards; copies in `production/src/footage/raw/`.
- **Also writes:** a `needed` row in `production/src/rights-register.md` where one was missing.
- **Does not touch:** the originals, any edit decision list, or any brief.

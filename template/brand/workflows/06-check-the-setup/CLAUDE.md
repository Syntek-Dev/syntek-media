@./CONTEXT.md

# CLAUDE.md — brand/workflows/06-check-the-setup/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/workflows/CONTEXT.md` → `brand/workflows/CLAUDE.md` → this folder's `CONTEXT.md`
(imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Find every missing tool, permission and server setting before the work needs it, and fix each
with the author or record what it blocks.

## How to work here

- **Routing:** no skill; the check is `python3 toolkit/media.py check --setup`, read against
  `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 4, with the ElevenLabs setup in
  `production/docs/reference/elevenlabs.md`.
- **Model:** the mechanical tier for running the check and recording its result; **Opus** for
  explaining a finding to the author and agreeing its fix
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: run the check
  → read each finding with its fix → fix with the author, one at a time → run it again → record
  → hand back.
- **Definition of done:** the check exits 0, or every finding left open is recorded with the
  commands it blocks and the author has accepted it; no credit-spending batch is started while an
  ElevenLabs line is open.

## Guardrails

- **The check changes nothing.** It reads the repository's `.claude/settings.json` and one key
  of the user's Claude Code configuration, and prints no other value from it; never print or
  copy anything else from that file.
- **Never report a check as passed when it could not run.** Exit 2 means it could not run: say
  which tool is missing.
- **The author changes the machine.** Give the exact command for each fix; installing software
  or re-adding the server is the author's to do.
- **`.claude/settings.json` is a shared file.** Another template may have written it; add an
  entry only on the author's explicit word, and change nothing else in it. An entry kept in a
  local or user settings file is reported absent, because the toolkit never reads a file Git
  ignores.
- **No spend while an ElevenLabs line is open**
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 4).
- **The API key is never typed or written.** It is exported in the author's shell; never on a
  command line, in a file or in a message.

## Output & naming

- **Produces:** the report, in the hand-back.
- **Also writes:** a dated Status line in `.claude/MEMORY.md`; entries in `.claude/settings.json`
  only on the author's word.
- **Does not touch:** any brand, script, production or publishing file.

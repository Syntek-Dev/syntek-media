@./CONTEXT.md

# CLAUDE.md — scripts/workflows/01-brief-a-piece/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `scripts/CONTEXT.md` →
`scripts/CLAUDE.md` → `scripts/workflows/CONTEXT.md` → `scripts/workflows/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Brief one piece with the author and leave a folder and a brief that any later session can
script, cut and post from.

## How to work here

- **Routing:** no media skill runs this procedure. The questioning is the grill-with-docs skill
  (syntek-author), where present; where it is not, ask the same questions in rounds, each with a
  recommended answer (`.claude/rules/syntek-media/06-global-rules.md` Section 8). Guide
  `scripts/docs/reference/the-piece-ladder.md`; deliverable keys from
  `toolkit/data/platforms.toml` through `python3 toolkit/media.py presets`.
- **Model:** **Opus** for every judgement: purpose, audience, hook, deliverables, disclosure and
  rights. The mechanical tier only for creating the folder, writing the agreed brief and ticking
  boxes (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.
- **Definition of done:** the author has agreed the brief, M1 is dated, and a fresh session could
  script or bring in the piece without asking what it is for.

## Guardrails

- **One piece per run.** Briefing every idea at once produces a shelf of briefs and nothing
  made; brief the next piece to be made.
- **The author decides purpose, deliverables and disclosure.** Ask; never infer them from an
  earlier piece and write them down as settled. M1 passes with no flag in the brief, so an
  undecided point keeps the piece at `idea`.
- **Ask nothing the repository can answer.** Read MEMORY, the register, the platform profiles,
  the voice file and any parent piece first.
- **Full-length deliverables only.** A cut-down belongs in the parent's cut-down plan, never in
  a brief.
- **Never overwrite** an existing brief or piece folder. Re-brief in place with the author's
  confirmation, keeping the piece's number and folder name.

## Output & naming

- **Produces:** `scripts/src/pieces/<piece>/brief.md`, in a folder named `NNN-kebab-title`
  with its own pair.
- **Also writes:** the register row in `scripts/src/piece-register.md`; MEMORY entries that pass
  the memory gate.
- **Does not touch:** any script, transcript or storyboard; the rights register (rows are opened
  when the piece is boarded or its rights are cleared); anything in the production or publishing
  layers.

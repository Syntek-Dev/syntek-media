@./CONTEXT.md

# CLAUDE.md — brand/workflows/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → the chosen procedure's own four
files.

## Purpose (one line)

Hold the brand layer's procedures, so that the kit, the voice and every platform are set up the
same way, checked the same way and recorded in the same place, whoever runs the job.

## How to work here

Two modes: **running** a procedure (the normal case) and **changing** one (rare).

**Running one.** Pick by what you are doing. Check `brand/workflows/local/` first: a local
procedure with the same slug replaces the one here (`run-media-workflow` does this for you).

| You want to… | Procedure |
|---|---|
| Set the brand's colours, type, spacing, caption style and layouts | `brand/workflows/01-set-up-the-brand-kit/` |
| Bring a component across between the kit and Claude Design | `brand/workflows/02-sync-with-claude-design/` |
| File a logo, cover, plate or other exported design asset | `brand/workflows/03-record-a-design-export/` |
| Set up the brand's account and choices on one platform | `brand/workflows/04-set-up-a-platform/` |
| Decide how the brand sounds aloud, who narrates, how words are said | `brand/workflows/05-write-the-spoken-voice/` |
| Check the tools, permissions and ElevenLabs server before spending | `brand/workflows/06-check-the-setup/` |

Read the procedure's `CONTEXT.md` → `CLAUDE.md` → `STEPS.md`, then work `STEPS.md` in order
with `CHECKLIST.md` open.

- **Routing:** each `STEPS.md` names its skill and guide on every step; here every step's skill
  is `none` or a companion from syntek-author, where present, because the author makes every
  brand decision. `run-media-workflow` resolves an intent to a procedure.
- **Model:** the `_opus_` / `_sonnet_` tags in each `CHECKLIST.md` are authoritative: Opus for
  every judgement, the mechanical tier for running checks, writing rows the author dictated and
  ticking boxes (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (changing one):** confirm with the author first → change all four files
  together → keep steps numbered and marked _Substantive._ or _Mechanical._ → record anything
  that overturns an earlier decision in `.claude/MEMORY.md`. A new procedure goes in
  `brand/workflows/local/`, never here.
- **Definition of done (running):** every checklist item ticked or explicitly waived with a
  reason; the brand file is where the procedure says it should be; every check it names has run
  and its result has been reported.

## Guardrails

- **Order is load-bearing.** The written brand is read before a token is set; the kit is
  committed before a sync; the setup is checked before the first credit is spent. Reversed, each
  produces work that has to be redone.
- **Procedures cite rules; they never restate them.** If a step explains why consent comes
  before a cloned voice, that explanation belongs in the rules file. Point at it.
- **The author chooses.** Every procedure offers options; none picks a colour, a font, a
  narrator or a handle on the author's behalf.
- **A waived step is recorded, not silent.** Say which step and why in the hand-back.
- **Numbers are frozen.** Never renumber or reuse a procedure number; the template appends.

## Output & naming

- **Hand-written:** nothing here by the author; template procedures are template-owned and
  replaced by `copier update`. The author's procedures go in `brand/workflows/local/`.
- **Folders:** `<NN>-<verb-first-name>/`, four files each, always.
- **Procedures produce nothing here.** Their output lands in `brand/src/`, and a proof in the
  git-ignored `production/src/renders/`.

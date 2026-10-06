@./CONTEXT.md

# CLAUDE.md — production/workflows/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file → the chosen
procedure's own four files.

## Purpose (one line)

Hold the production layer's procedures, so that every source is logged, every take paid for once
and every master made, checked and approved the same way, whoever runs the job.

## How to work here

Two modes: **running** a procedure (the normal case) and **changing** one (rare).

**Running one.** Pick by what you are doing. Check `production/workflows/local/` first: a local
procedure with the same slug replaces the one here (`run-media-workflow` does this for you).

| You want to… | Procedure |
|---|---|
| Log footage, a recording, a music bed, stock or an image before an edit names it | `production/workflows/01-log-source-media/` |
| Voice a script through ElevenLabs, or try another take of a line | `production/workflows/02-make-a-voiceover/` |
| Build a piece's master, or change one | `production/workflows/03-assemble-the-master/` |
<: if 'podcast' in MEDIA_KINDS :>| Master a podcast episode's audio | `production/workflows/04-master-a-podcast-episode/` |
<: endif :><: if 'audiobook' in MEDIA_KINDS :>| Plan an audiobook (its chapter register and credits), or voice or record its chapters | `production/workflows/05-narrate-an-audiobook/` |
| Master, check and package an audiobook's chapters | `production/workflows/06-master-an-audiobook/` |
<: endif :>| Clear the music, footage, voices and quotations a piece uses | `production/workflows/07-clear-the-rights/` |
| Bring in a recorded talk, interview or conversation as a piece | `production/workflows/08-bring-in-a-recording/` |
| Agree a scene piece's words and re-time its boards on the approved joined voice | `production/workflows/09-time-the-voice/` |

Read the procedure's `CONTEXT.md` → `CLAUDE.md` → `STEPS.md`, then work `STEPS.md` in order
with `CHECKLIST.md` open.

- **Routing:** each `STEPS.md` names its skills in its frontmatter and its skill and guide on
  every step; `run-media-workflow` resolves an intent to a procedure.
- **Model:** the `_opus_` / `_sonnet_` tags in each `CHECKLIST.md` are authoritative: Opus for
  every judgement, the mechanical tier for logging files, running the toolkit and ticking boxes
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (changing one):** confirm with the author first → change all four files
  together → keep steps numbered and marked _Substantive._ or _Mechanical._ → record anything
  that overturns an earlier decision in `.claude/MEMORY.md`. A new procedure goes in
  `production/workflows/local/`, never here.
- **Definition of done (running):** every checklist item ticked or explicitly waived with a
  reason; the output is where the procedure says it should be; every credit spent is logged.

## Guardrails

- **Order is load-bearing.** A file is logged before an edit names it; the cost is stated
  before anything is generated; a take is approved before it is archived, and archived before a
  master depends on it (an audiobook archives its approved masters); the author watches a master
  through before any gate is recorded.
  Reversed, each produces work that has to be redone, or credits spent twice.
- **Procedures cite rules; they never restate them.** If a step explains why credits are never
  spent unasked, that explanation belongs in `.claude/rules/syntek-media/03-production-ethics.md`.
  Point at it.
- **The author chooses.** Every procedure offers options; none picks a voice, a take, a cut or a
  permission on the author's behalf.
- **A waived step is recorded, not silent.** Say which step and why in the hand-back.
- **Numbers are frozen.** Never renumber or reuse a procedure number; the template appends.

## Output & naming

- **Hand-written:** nothing here by the author; template procedures are template-owned and
  replaced by `copier update`. The author's procedures go in `production/workflows/local/`.
- **Folders:** `<NN>-<verb-first-name>/`, four files each, always.
- **Procedures produce nothing here.** Registers and edit decision lists land in
  `production/src/`; renders and generated audio land in its git-ignored folders.

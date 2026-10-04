@./CONTEXT.md

# CLAUDE.md — publishing/src/cut-downs/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/src/CONTEXT.md` → `publishing/src/CLAUDE.md` → this folder's
`CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold one agreed cut-down plan per piece, so every cut is chosen, timed and framed with the author
before a render is made.

## How to work here

- **Routing:** a new or revised plan → `publishing/workflows/01-plan-the-cut-downs/` with
  `repurpose`; rendering it → `publishing/workflows/02-cut-for-a-platform/` with
  `cut-for-platform`, which moves each row's Status from `approved` to `rendered` and `checked`.
- **Model:** **Opus** for choosing moments, hooks and frames; the mechanical tier for a Status the
  owning skill reports (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the brief, the script or transcript and the master's captions → read
  the platform guides for the deliverables → propose the cuts → agree them with the author →
  write the plan → hand it to the cutting procedure.
- **Definition of done:** every cut stands alone, sits inside its deliverables' limits, cites the
  lines it carries and times them on the master; the author has approved the plan.

## Guardrails

- **One plan per piece.** Revise it; never start a second.
- **Times are on the master.** In and Out are `HH:MM:SS.mmm` on the master, read from its
  captions or edit decision list, never guessed by ear and never timed to a recording.
- **Cut numbers are permanent.** A dropped cut keeps its `cNN` and its row, marked in its notes.
- **No near-identical batch.** Each cut carries a different moment
  (`publishing/docs/reference/cut-downs.md`).
- **Never overwrite** a plan without confirming with the author.

## Output & naming

- **Hand-written (with the author):** `<piece>.md`, named for the piece's folder, in this shape:

```markdown
---
piece: NNN-kebab-title                  # equals the piece's folder name
master: NNN-kebab-title.master.mp4      # the master render the cuts are taken from
approved: ""                            # DD/MM/YYYY once the author agrees the plan
---

# <Title> — cut-down plan

| Cut | Deliverables | Lines | In | Out | Frame | Hook | Status |
|---|---|---|---|---|---|---|---|
| c01 | <platform>.<format>, … | <beat.line–beat.line> | HH:MM:SS.mmm | HH:MM:SS.mmm | centre · crop x=<px> · pad | <opening words> | planned |

## c01 — <hook>

<Opening words, on-screen title, caption width, its own thumbnail or not, and why this moment stands alone; one sentence per line.>
```

- **A silent loop** (`website.hero_loop`) is a row like any cut, its Lines `—` and its note naming
  any cut it shares frames with; the rules that a cut stands alone in whole sentences and differs
  from every other cut do not bind it.
- **Kept current by skills:** each row's Status (`planned · approved · rendered · checked`).
- **Generated:** nothing here; the cuts are renders in `publishing/src/renders/`.

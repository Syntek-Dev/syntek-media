@./CONTEXT.md

# CLAUDE.md — publishing/workflows/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file → the chosen
procedure's own four files.

## Purpose (one line)

Hold the publishing layer's ordered procedures, so every deliverable is cut, captioned, briefed,
packaged and logged the same way every time, whoever runs it.

## How to work here

- **Routing:** pick by what you want; `run-media-workflow` checks `local/<slug>/` before the
  template's folder of the same slug.

| You want to… | Procedure |
|---|---|
| Plan the short cuts of a finished master | `publishing/workflows/01-plan-the-cut-downs/` |
| Render the deliverables of a piece, full-length or cut | `publishing/workflows/02-cut-for-a-platform/` |
| Caption a piece's deliverables, burned or as sidecars | `publishing/workflows/03-caption-a-piece/` |
| Make a thumbnail or a cover | `publishing/workflows/04-brief-a-thumbnail/` |
| Write the post package, decide the disclosure and schedule it | `publishing/workflows/05-prepare-a-post/` |
| Log what the author posted, moved or dropped | `publishing/workflows/06-record-a-publication/` |
| Re-check the platform limits and record corrections | `publishing/workflows/07-refresh-the-platform-specs/` |

- **Model:** the `_opus_` / `_sonnet_` tags in each `CHECKLIST.md` are authoritative: Opus for
  every judgement; the mechanical tier only for renders, file creation, table edits and ticks
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (running one):** read the procedure's `CONTEXT.md` → `CLAUDE.md` →
  `STEPS.md`, then work `STEPS.md` in order with `CHECKLIST.md` open.
- **Concrete steps (changing one):** only on the author's instruction. Copy it to `local/` under
  the same slug and change all four files together; keep steps ordered, numbered and marked
  _Substantive._ or _Mechanical._.
- **Definition of done (running):** every checklist item ticked or waived with a reason; the
  output is where the procedure says it is; the gate it serves is recorded in the brief, or its
  `n/a` reason is; **nothing was posted**.

## Guardrails

- **Order is load-bearing.** Plan before cutting, caption before or with the cut, package before
  scheduling, and log only after the author has posted.
- **Procedures cite rules; they never restate them.** A gate is cited from
  `scripts/docs/reference/the-piece-ladder.md` by number and the move it guards, never restated.
- **A waived step is recorded, not silent.** Say which step, and why, in the hand-back; a waived
  gate is recorded in the brief's `verified` with the date and the author's reason.
- **Never renumber or reuse a number.** Numbering is frozen and append-only; a template procedure
  you do not want is overridden in `local/`, not deleted.
- **Template folders are template-owned.** Never edit them in place.

## Output & naming

- **Folders:** `NN-verb-first-kebab-name/`, four files each. Nothing here is generated.
- **Procedures produce nothing here.** Their output lands in `publishing/src/`, with renders in
  `publishing/src/renders/`.

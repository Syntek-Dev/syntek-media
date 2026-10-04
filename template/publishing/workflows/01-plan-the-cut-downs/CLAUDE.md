@./CONTEXT.md

# CLAUDE.md — publishing/workflows/01-plan-the-cut-downs/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/workflows/CONTEXT.md` → `publishing/workflows/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Agree with the author, before anything is rendered, which moments of a master become short cuts,
for which platforms, and how each is framed and opened.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative: `opus` items are judgement; `sonnet` items belong to the mechanical tier.

- **Routing:** skill `repurpose` (this procedure in skill form; its mode file carries what a
  moment is for this brand). Guides: `publishing/docs/reference/cut-downs.md`,
  `publishing/docs/reference/platform-specs.md` and the guide for each platform a cut goes to.
  Tools: `python3 toolkit/media.py presets` and `captions retime`.
- **Model:** **Opus** for choosing moments, hooks and frames: that is the whole task. The
  mechanical tier for reading presets and writing the agreed rows
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the master → read the brief, the script or transcript and any
  calendar entries → read each platform's keys → get the master's timing → find the moments →
  frame them → check lengths and refuse near-identical cuts → propose → write the plan → hand
  back.
- **Definition of done:** every cut stands alone, opens on its hook, cites its lines, is timed on
  the master, is framed for its deliverables and sits inside every `max_seconds`; the author has
  approved every row.

## Guardrails

- **Plan; never render.** Nothing is cut, encoded or burned in this procedure.
- **The author chooses.** Propose with a reason per cut; a row is `approved` only on the author's
  word, and a declined cut is not written.
- **Times come from the record.** In and Out are read from the master-timed captions or the edit
  decision list, never estimated by ear.
- **Refuse near-identical cuts,** however many deliverables the calendar asks for.
- **The calendar is read, never rewritten.** Where syntek-author's content calendar is present,
  its entries for this piece are read here; a change to it belongs to the social-media-documents
  skill (syntek-author), where present.
- **Never overwrite** an approved plan without confirming with the author; revise it.

## Output & naming

- **Produces:** `publishing/src/cut-downs/<piece>.md`.
- **Also writes:** a recorded piece's master-timed captions, retimed from its recording's, where
  they do not exist yet; `publishing/workflows/03-caption-a-piece/` checks them later.
- **Does not touch:** the brief's deliverables, the master or any render.

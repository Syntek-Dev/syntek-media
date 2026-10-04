@./CONTEXT.md

# CLAUDE.md — publishing/workflows/02-cut-for-a-platform/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/workflows/CONTEXT.md` → `publishing/workflows/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Render every deliverable of a piece through the toolkit, verify each against its preset, and have
the author see it, so nothing reaches a platform that the platform will reject or crop.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative: `opus` items are judgement; `sonnet` items belong to the mechanical tier.

- **Routing:** skill `cut-for-platform`. Guides: `publishing/docs/reference/cut-downs.md`,
  `publishing/docs/reference/platform-specs.md`, `publishing/docs/reference/captions.md` and the
  guide for each platform a deliverable goes to. Tools: `python3 toolkit/media.py` (`presets`,
  `encode`, `cut`, `still-video`, `probe`).
- **Model:** the mechanical tier for running the toolkit and recording results; **Opus** for
  deciding burned or sidecar captions, diagnosing a failed verification and judging a render
  with the author (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the master and the plan → list the deliverables → read each preset
  → decide captions per deliverable → encode the full-length deliverables → cut each approved cut
  → verify every output → the author watches each → record the gate → hand back.
- **Definition of done:** every deliverable of the brief and every approved cut is rendered,
  exits 0, probes as its preset says, and has been seen by the author; the gate is recorded.

## Guardrails

- **Every render goes through the toolkit.** Never call ffmpeg by hand for a deliverable, never
  use stream copy for a frame-accurate cut, and never hand-edit a render.
- **Exit 1 is a finding, not a nuisance.** A render that fails its verification is remade from
  its sources after the cause is found; it is never posted anyway.
- **Exit 2 names what is missing.** Say which tool or input is absent and which deliverable it
  blocks; never report a deliverable as made when the command could not run.
- **Cut from the master only,** so every deliverable inherits its loudness, rights and disclosure.
- **The gate is the author's.** M5 is recorded only once the author has seen or heard every
  deliverable.
- **Renders stay out of Git.** Never force one past `publishing/src/.gitignore`.

## Output & naming

- **Produces:** renders in `publishing/src/renders/`, named
  `<piece>[--cNN].<platform>-<format>[.burned].<ext>`.
- **Also writes:** each cut's Status in `publishing/src/cut-downs/<piece>.md`; the brief's
  `status` and `verified`.
- **Does not touch:** the master, the edit decision list, the captions' words or the plan's
  choices.

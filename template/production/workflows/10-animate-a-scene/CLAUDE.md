@./CONTEXT.md

# CLAUDE.md — production/workflows/10-animate-a-scene/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md`, with `CHECKLIST.md` open.

## Purpose (one line)

Animate the author's art on accepted voice timings and agree its stills and preview before M4.

## How to work here

- **Routing:** skill `cut-for-platform`; guide `production/docs/reference/scenes-as-code.md`.
- **Model:** **Opus** for writing the scene and every visual judgement; the mechanical tier
  for commands and recording, as the checklist tags specify.
- **Concrete steps:** check timing → index real sources → write the scene and audio edit →
  draw stills → open each printed path → review mouths and preview → apply notes → render aspects.
- **Definition of done:** author-agreed stills and preview, measured masters per required aspect,
  current `M4.stills` and M4, with every earlier sub-check dated or reasoned `n/a`.

## Guardrails

- **No spending or model fetch.** This procedure draws local art and plays approved sound.
- **The author approves the art and sound.** Generated effects/music are separately approved,
  logged and cleared; the edit's audio rows supply their mix, linked by cue ID where instructed.
- **No recorded video in a scene.** Index only images and small captures; use assemble for footage.
- **Open only printed still paths.** Read the printed findings; never browse ignored folders.
- **Timing notes return through `production/workflows/09-time-the-voice/`.** A re-time keeps M3;
  changed words or replaced shots return to boarding and clear its dependent gates.
- **Never crop one scene aspect into another.** Lay it out and render natively.
- **Never hand-edit the page, reports or JSON.** Edit the source and run the producing command.

## Output & naming

- **Writes with the author:** `<piece>.scene.py` in `production/src/scenes/` and the existing edit.
- **Accepts through `-o`:** `<piece>.real.json` in that scene folder, existing output Git-clean.
- **Generated:** scene page, still PNGs/report and masters in `production/src/renders/<piece>/`.
- **Records:** the author's Timing notes and approval, `M4.stills`, M4 and `last_updated`.

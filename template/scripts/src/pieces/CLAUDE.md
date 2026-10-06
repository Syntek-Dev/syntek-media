@./CONTEXT.md

# CLAUDE.md — scripts/src/pieces/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `scripts/CONTEXT.md` →
`scripts/CLAUDE.md` → `scripts/src/CONTEXT.md` → `scripts/src/CLAUDE.md` → this folder's
`CONTEXT.md` (imported above) → this file → the target piece's `CONTEXT.md` and `CLAUDE.md`.

## Purpose (one line)

Hold one folder per piece, each opened the same way with its own pair, so any later session can
find what a piece is for and where it stands without asking.

## How to work here

- **Routing:** a new piece → `scripts/workflows/01-brief-a-piece/`, which takes the number from
  `scripts/src/piece-register.md`, opens the folder, and writes its pair and its brief from the
  skeletons below. The files inside a piece have the writers in `scripts/src/CLAUDE.md`'s table;
  a brief's `status` and `verified` move only through the procedure that serves each gate.
- **Model:** **Opus** for a piece's purpose, traps and definition of done; the mechanical tier
  for creating the folder and copying the skeletons
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps for a new piece folder** (normally done by
  `scripts/workflows/01-brief-a-piece/`):
  1. Confirm the register row; the folder takes exactly the name in its Piece column,
     `NNN-kebab-title`.
  2. Create the folder with its `CONTEXT.md` and `CLAUDE.md` from the pair skeleton below. The
     `CONTEXT.md` says what the piece is for and which deliverables it is made for; the
     `CLAUDE.md` names its particular traps and a definition of done phrased as what the viewer
     or listener can do or feel at the end. Both route to the brief instead of restating it.
  3. Write `brief.md` from the brief skeleton below; the gates it records are defined in
     `scripts/docs/reference/the-piece-ladder.md`.
  4. Leave the script or transcript, the storyboard and the shot list to their procedures; add
     each to the piece's tree when it is written.
- **Definition of done:** every piece folder has its pair and a brief, its name matches its
  register row, and its pair routes to the brief rather than repeating it.

## Guardrails

- **One piece per folder.** A cut-down is not a piece: it lives in its parent's cut-down plan. A
  piece re-scripted or re-cut is the same piece, re-briefed in place.
- **Folder names are keys.** Every file the piece makes in the production and publishing layers
  carries its name; never rename a piece folder once one exists, and never reuse a number.
- **The pair routes; the brief records.** A status, a deliverable or a date copied into the pair
  drifts from the brief within days. Point at `brief.md` instead.
- **Nothing generated lives here.** Audio, footage, renders and caption files belong to the
  production and publishing layers, never to a piece folder.
- **Never overwrite** a piece's pair, brief, words or boards without confirming with the author.

## Output & naming

- **Hand-written (with the author):** `NNN-kebab-title/`, its pair and `brief.md`, one sentence
  per line in the body. Shape and Metaphor always have an answer; `n/a` is valid, blank is not.
  A brief that passed M1 before these headings keeps its date until it is next re-briefed:

  ```markdown
  ---
  piece: NNN-kebab-title     # equals the folder name
  title: ""                  # the working title, as it will appear
  kind: short-video          # short-video | long-video | podcast | audiobook | trailer | voiceover
  origin: scripted           # scripted | recorded
  picture: true              # false for audio-only pieces: M3 reads n/a
  status: idea               # idea · briefed · scripted · storyboarded · produced · cut · captioned · scheduled · published
  deliverables: []           # full-length deliverables only: keys of toolkit/data/platforms.toml
  source_media: []           # recorded: its footage IDs, e.g. [F0001]; [] until it is logged
  target_seconds: 0
  words_per_minute: 150
  parent: ""                 # the piece this was cut or adapted from
  source: ""                 # written work it adapts (read, never edited)
  synthetic_voice: none      # none | stock | designed | own-clone | other-clone
  ai_visuals: none           # none | assisted | generated
  music: none                # none | licensed | own | generated
  rights: []                 # rights-register IDs, e.g. [RR0003]
  verified: {}               # gate or M4 sub-check: DD/MM/YYYY | 'n/a — reason' | 'waived DD/MM/YYYY — reason'
  last_updated: DD/MM/YYYY
  ---

  # <Title> — brief

  ## Purpose
  ## Audience
  ## Shape
  ## Metaphor
  ## Hook
  ## Key points
  ## Call to action
  ## Disclosure plan
  ## Rights needs
  ## Draws on
  ## Notes
  ```

- **Written by skills:** `script.md` (`write-script`), `transcript.md` (`captions`),
  `storyboard.md` and `shot-list.md` (`storyboard`). An audiobook's folder holds only its brief
  and pair: its plan is its chapter register, in the audiobook folder, where the project makes
  audiobooks.
- **The pair a new piece folder gets.** Copy both files, replace every `<…>` slot, keep the
  four H2s of `CLAUDE.md` exactly, and fit the tree to the files the piece has: `transcript.md`
  in place of `script.md` for a recorded piece, no script for an audiobook, and no storyboard or
  shot list where M3 is `n/a`.

  ````markdown
  # CONTEXT.md — scripts/src/pieces/<piece>/

  <One paragraph: what the piece is, in words (its kind, scripted or recorded), what it must do
  for its viewer or listener, and the deliverables it is made for. Its status and dates are in
  brief.md; never copy them here.>

  ## Directory Tree

  ```text
  scripts/src/pieces/<piece>/
  ├── CONTEXT.md        ← this file
  ├── CLAUDE.md         ← this piece's traps and its definition of done
  ├── brief.md          ← the plan, its status and its gates
  ├── script.md         ← the words, one spoken sentence per line
  ├── storyboard.md     ← a picture for every spoken line
  └── shot-list.md      ← a source for every shot
  ```

  ## What's here

  - `brief.md` — **where this piece stands:** its plan, its `status` and its `verified` record.
  - `script.md` — <the words, approved or not; for a recorded piece, `transcript.md`, the words
    as said, each beat anchored on the recording>.
  - `storyboard.md` and `shot-list.md` — <the boards and shots, or one line saying why there are
    none: M3 recorded n/a for no picture, or for a recording>.
  - Elsewhere under this piece's name: <its edit decision list, cards and voiceover register in
    the production layer; its cut-down plan, captions, thumbnails and post package in the
    publishing layer, as each is made>.

  ## Cross-references

  - `scripts/docs/reference/the-piece-ladder.md` — the gates this piece passes.
  - <the guide for the piece's kind, where the project makes that kind>.
  - <the parent piece, or the written work it adapts, where there is one>.
  ````

  ```markdown
  @./CONTEXT.md

  # CLAUDE.md — scripts/src/pieces/<piece>/

  Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `scripts/CONTEXT.md` →
  `scripts/CLAUDE.md` → `scripts/src/CONTEXT.md` → `scripts/src/CLAUDE.md` →
  `scripts/src/pieces/CONTEXT.md` → `scripts/src/pieces/CLAUDE.md` → this folder's `CONTEXT.md`
  (imported above) → this file.

  ## Purpose (one line)

  <What this piece must do for its viewer or listener, in one sentence.>

  ## How to work here

  - **Routing:** start every task on this piece from the procedure that serves its next gate (the
    `run-media-workflow` skill reads `brief.md` to find it); never change a file here outside a
    procedure.
  - **Model:** **Opus** for every line a viewer or listener will hear or read, and every
    judgement; the mechanical tier for ticks and renames
    (`.claude/rules/syntek-media/05-model-allocation.md`).
  - **Concrete steps:** read `brief.md` in full → read the file the procedure changes → change
    it → check that the brief, the words and the boards still agree.
  - **Definition of done:** <what the viewer or listener can do, believe or feel at the end, and
    the status the piece is working towards>.

  ## Guardrails

  - <This piece's particular traps: a claim still to check, a name to say right, a person or a
    place to clear, a disclosure its brief records.>
  - **Never overwrite** this piece's brief, words, storyboard or shot list without confirming
    with the author.

  ## Output & naming

  - **Hand-written (with the author):** `brief.md`.
  - **Written by skills:** <`script.md` (`write-script`) or `transcript.md` (`captions`);
    `storyboard.md` and `shot-list.md` (`storyboard`)>.
  - **Elsewhere, under this piece's name:** <the production and publishing files it has>.
  ```

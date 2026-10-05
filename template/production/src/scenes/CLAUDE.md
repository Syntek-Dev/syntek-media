@./CONTEXT.md

# CLAUDE.md — production/src/scenes/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/src/CONTEXT.md` → `production/src/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep, once per scene piece, the indexes and the code its picture is drawn from, so its masters
can be rendered again, frame for frame, from tracked files.

## How to work here

- **Routing:** skills `storyboard` (the cue index, once the voice is timed) and
  `cut-for-platform` (the real index and the scene file), in the procedures
  `production/workflows/CLAUDE.md` names for a scene piece; guides
  `scripts/docs/reference/storyboards-and-shot-lists.md` and
  `production/docs/reference/edit-decision-lists.md`.
- **Model:** **Opus** for the scene and every judgement on its timing, with the author; the
  mechanical tier for running the commands
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (an index):** run the command without `-o`, which writes its working copy and
  prints what it found → read that output with the author → once the author accepts the run,
  run it again with `-o` naming the file here → commit it.
- **Concrete steps (the scene):** read the re-timed storyboard, the shot list and the brand's
  tokens → write `<piece>.scene.py` with the author → check it in stills and a preview render →
  apply the author's notes → render.
- **Definition of done:** both indexes match the piece's current words and shot list, the scene
  file renders the piece's masters, and nothing tool-written here was edited by hand.

## Guardrails

- **Indexes are tool-written, never hand-edited.** A wrong time or source is put right in the
  storyboard, the shot list or the voice, and the command run again.
- **Replaced only through `-o`, and only while Git holds the old version.** The command that
  makes an index is the only one that replaces it, with `-o` naming it, and only while Git
  reports no uncommitted change to it (`.claude/rules/syntek-media/04-toolkit-pipeline.md`
  Section 3).
- **Never open a working copy.** The copies in `production/src/renders/<piece>/timing/` are
  git-ignored; read the command's output instead
  (`.claude/rules/syntek-media/06-global-rules.md` Section 12).
- **Run the scene by its path, never import it.** A file named for its piece cannot be imported
  by name, and an import would leave a cache folder here.
- **The look is the brand's.** A scene reads its colours, faces and spaces from the brand's
  tokens and its art from the brand's design exports; it never sets a look of its own.
- **Images and text captures only.** A scene shows what it draws, the images and the text
  captures its real index lists, never a video or a sound; a piece that shows recorded video is
  a footage piece, assembled from its edit decision list.
- **Never overwrite the scene file** without confirming with the author; a change is an edit to
  it, never a second scene file.

## Output & naming

- **Written by the toolkit, through `-o`, once the author accepts the run:**
  `<piece>.cues.json` by `media.py cues` and `<piece>.real.json` by `media.py real`, JSON with
  finite numbers, each named for the piece's folder.
- **Written by skills (with the author):** `<piece>.scene.py`, by `cut-for-platform`.
- **Working copies and output (never committed):** the indexes' working copies in
  `production/src/renders/<piece>/timing/`; the scene's page, stills and masters elsewhere in
  `production/src/renders/<piece>/`. A tracked file never sits in a per-piece folder, and a file
  in one is never moved here by hand.

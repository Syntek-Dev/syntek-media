@./CONTEXT.md

# CLAUDE.md — production/src/timing/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/src/CONTEXT.md` → `production/src/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep, once per piece, the accepted timing of its joined voice, so its captions and its scene can
be made again from tracked files without timing the voice again.

## How to work here

- **Routing:** skills `captions` (the words and the words check) and `voiceover` (the mouth
  cues), in the procedure `production/workflows/CLAUDE.md` names for timing a scene piece's
  voice; guide `production/docs/reference/voiceover.md`.
- **Model:** **Opus** for reading the words check with the author and for whether a run is
  accepted; the mechanical tier for running the commands
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** every segment approved and archived and the voice joined → run the command
  without `-o`, which writes its working copy and prints what it found → read that output with
  the author → once the author accepts the run, run the same command again with `-o` naming the
  file here → commit it.
- **Definition of done:** the words, the words check and the mouth cues of the piece's current
  joined voice are here, the author has signed the words check, and nothing here was edited by
  hand.

## Guardrails

- **Tool-written, never hand-edited.** A wrong time is put right by running its command again
  (or by a new take), never by editing the JSON.
- **Replaced only through `-o`, and only while Git holds the old version.** The command that
  makes a file is the only one that replaces it, with `-o` naming it, and only while Git reports
  no uncommitted change to it; an uncommitted change or an untracked copy is refused. Commit an
  accepted file before the next run replaces it
  (`.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3).
- **Never open a working copy.** The copies in `production/src/renders/<piece>/timing/` are
  git-ignored; the command printed what it found, so read its output instead
  (`.claude/rules/syntek-media/06-global-rules.md` Section 12).
- **One joined voice, one set of files.** A take added after the voice was joined makes every
  file here stale: join the voice again, then time it again.
- **Flat, never per piece.** A file here stays under its `<piece>.` name; a folder per piece
  belongs only inside a git-ignored output folder.
- **No levels file here.** Window levels are a working copy only, in the piece's renders folder.

## Output & naming

- **Written by the toolkit, through `-o`, once the author accepts the run:**
  `<piece>.words.json` and `<piece>.words-check.md` by `media.py transcribe`, and
  `<piece>.mouth.json` by `media.py lipsync`, each named for the piece's folder.
- **The data is JSON**, because a scene's page reads it, and every number in it is finite; the
  words check alone is Markdown, written for the author to read.
- **`<piece>.words.json`:** one entry per word, in order, with `word` (as the register's `text`
  spells it, never a respelling), `start` and `end` (seconds in the joined voice), `score` (the
  aligner's confidence) and `segment` (the register segment it was said in).
- **`<piece>.mouth.json`:** Rhubarb Lip Sync's JSON, its `mouthCues` each a `start`, an `end`
  (whole centiseconds) and a `value`, the shape `A`–`H` or the rest shape `X`; its `soundFile`
  repository-relative. Whatever reads it takes a frame's shape at the frame's middle.
- **Working copies (never committed, never opened):** the same names, in
  `production/src/renders/<piece>/timing/`.

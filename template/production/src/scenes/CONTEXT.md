# CONTEXT.md — production/src/scenes/

The tracked files a scene piece's picture is drawn from, flat under the piece's `<piece>.` names:
the cue index that says when each board, line and word starts and ends in the joined voice, the
index of the real sources the scene shows, and the scene itself, written as code. A scene piece is
one whose picture is drawn rather than filmed (its shot list types its shots `scene`); every other
piece is assembled from its edit decision list and keeps nothing here.

## Directory Tree

```text
production/src/scenes/
├── CONTEXT.md              ← this file
├── CLAUDE.md               ← operating rules
├── <piece>.cues.json       ← each board's, line's and word's start and end in the joined voice (tool-written)
├── <piece>.real.json       ← the images and text captures the scene shows, each with its hash (tool-written)
└── <piece>.scene.py        ← the piece's scene as code, run by its path and never imported
```

## What's here

- Cue JSON has separate `beats`, `boards`, `lines`, `words` and `events` lists. Events retain
  script delivery/SFX/MUSIC instructions; effect/music IDs link through edit audio rows' `cue`
  field to their logged source and mix. All timings are exact seconds relative to the joined voice.
- `<piece>.cues.json` — written by `python3 toolkit/media.py cues <piece>` from the script's beats
  and lines, the storyboard's boards and the tracked words in `production/src/timing/`. The
  storyboard is re-timed from what the command prints; nothing rewrites the storyboard itself.
- `<piece>.real.json` — written by `python3 toolkit/media.py real <piece>`: every source the
  piece's shot list names in its Source column, the scene file aside, each an image or a text
  capture in `production/src/assets/` or the footage ID of an image, with its hash. A scene never
  shows a video or a sound; a piece that shows recorded video is a footage piece, assembled.
- `<piece>.scene.py` — the piece's scene, written with the author from the re-timed storyboard. It
  composes the toolkit's scene kit, which reads the cue index, the words and mouth cues in
  `production/src/timing/` and the real index, and draws only in the brand's look. The toolkit's
  `scene.py` runs it by its path, never importing it, so nothing but the file itself lands here;
  the page it writes, and the stills and masters made from it, are git-ignored, in the piece's
  own folder in `production/src/renders/`.
- **The working copies** of the two indexes sit in the piece's git-ignored
  `production/src/renders/<piece>/timing/`, where a run can be repeated freely; the tracked copy
  here is written only through `-o`, once the author has accepted the run.
- This folder ships with every project, holding only its pair until a scene piece is made.

## Cross-references

- `production/src/timing/` — the words and mouth cues every scene is timed from.
- `scripts/src/pieces/` — the storyboard and shot list a scene is written from.
- `production/src/assets/` — the small images and text captures a scene may show.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 — the working copy, `-o`, and the
  named exception that lets an index be replaced.
- `production/workflows/CLAUDE.md` — the procedures, among them those that time a scene piece's
  voice and animate its scene.

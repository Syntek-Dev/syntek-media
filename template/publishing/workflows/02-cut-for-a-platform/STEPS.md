---
workflow: 02-cut-for-a-platform
phase: convert
skills: [cut-for-platform]
model: opus
---

# STEPS.md — cut and encode a piece for its platforms

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for rendering and verifying every deliverable of a piece. Each step names
the skill and guide it uses, and the toolkit command it runs. **Run in order** — the ordering is
load-bearing — and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`), then
> `publishing/docs/reference/cut-downs.md` and `publishing/docs/reference/platform-specs.md`. The
> `cut-for-platform` skill makes every render; read it before step 1.

## 1. Confirm the piece is ready to cut

> **Skill:** `cut-for-platform` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Read the brief, `scripts/src/pieces/<piece>/brief.md`: its `verified` dates M4. Find the master in
`production/src/renders/`; a missing master is remade by
`production/workflows/03-assemble-the-master/` first. Where the piece has cuts, its plan in
`publishing/src/cut-downs/` is `approved`. **Nothing is cut from an unapproved master or plan.**
_Mechanical._

## 2. List the deliverables

> **Skill:** `cut-for-platform` · **Guide:** `publishing/docs/reference/cut-downs.md`

Write out every deliverable to make: each full-length key in the brief's `deliverables`, and each
key of each `approved` cut in the plan, with the cut's In, Out and Frame beside it. A silent loop
(`website.hero_loop`) is listed like any cut. A poster, a share, featured or preview image and a
GIF preview are not: they are the thumbnail brief's, made in
`publishing/workflows/04-brief-a-thumbnail/`. That list is what M5 is checked against.
_Mechanical._

## 3. Read each preset

> **Skill:** `cut-for-platform` · **Guide:** `publishing/docs/reference/platform-specs.md`

Run `python3 toolkit/media.py presets KEY` for every deliverable on the list. Note its size,
`max_seconds`, `safe_zone`, `caption_formats`, each override the toolkit prints and every key in
`verify`; read the platform's guide in `publishing/docs/reference/` for its traps. _Mechanical._

## 4. Decide each deliverable's captions

> **Skill:** `cut-for-platform` · **Guide:** `publishing/docs/reference/captions.md`

A deliverable whose table has `caption_formats = []`, or whose brief asks for burned captions, is
burned; the rest take a sidecar, video for a site of the website or blog profile always so. A
table with `audio_tracks = 0` (a silent loop) takes none, and neither does an audio deliverable. Where a deliverable is to be burned and its caption file already
exists and passes `captions check --script`, it goes into this pass. Where it does not exist yet,
render without it and leave captions to `publishing/workflows/03-caption-a-piece/`.
_Substantive._

## 5. Encode the full-length deliverables

> **Skill:** `cut-for-platform` · **Guide:** `publishing/docs/reference/platform-specs.md`

For each full-length key, run `python3 toolkit/media.py encode <master> --deliverable KEY`, adding
`--frame crop` or `--frame pad` where its aspect differs from the master's. An audio piece bound
for a video platform is a still under its audio:
`python3 toolkit/media.py still-video <image> <audio> --deliverable KEY`. **A feed episode's
`podcast.feed_audio`** is encoded the same way, untagged and needing no register, from the audio
master or, for a talk published as an episode, from the picture master, whose sound alone it
takes; its tags and chapters are written at M7, through the podcast-feed workflow where the
project has it. _Mechanical._

## 6. Cut each approved cut

> **Skill:** `cut-for-platform` · **Guide:** `publishing/docs/reference/cut-downs.md`

For each deliverable of each `approved` cut, take In, Out and Frame from the plan and run one
pass:

```bash
python3 toolkit/media.py cut <master> --deliverable KEY --in HH:MM:SS.mmm --out HH:MM:SS.mmm \
  --cut cNN --frame crop --x <px> --captions publishing/src/captions/<piece>--cNN[.<platform>-<format>].en-GB.srt
```

Burn the file made at this deliverable's line width: its rewrapped copy where
`publishing/workflows/03-caption-a-piece/` made one (the `.<platform>-<format>` qualifier, the
key's dot and underscores as hyphens: `.instagram-story`), or the cut's own file where that passes
`captions check --deliverable KEY`. Leave out `--captions` where step 4 found none to burn, and
`--x` where the frame is `pad` or centred. _Mechanical._

## 7. Verify every output

> **Skill:** `cut-for-platform` · **Guide:** `.claude/rules/syntek-media/04-toolkit-pipeline.md`

Exit 0 only. Exit 1 means the render failed its verification (size, codecs, length over
`max_seconds`, the index not at the front): find the cause in the input or the plan, fix it there
and render again. Exit 2 means the command could not run: name the missing tool or input and the
deliverable it blocks. Run `python3 toolkit/media.py probe` on every output and keep the result
for the hand-back; a cut whose every deliverable has passed moves its Status to `rendered`.
_Mechanical (running); the diagnosis of a failure is substantive._

## 8. Have the author watch each one

> **Skill:** `cut-for-platform` · **Guide:** `publishing/docs/reference/cut-downs.md`

Give the author every render, with its key and its probe. Burned captions are checked by eye,
inside the safe zone and in time with the speech. A render the author approves moves its cut's
Status to `checked`; one the author rejects goes back to the step that caused it. _Substantive._

## 9. Record the gate

> **Skill:** `cut-for-platform` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

When every deliverable on the list has passed and the author has seen each one, set the brief's
`status` to `cut` and date M5 in `verified`. Where every deliverable that needs captions had them
burned in this pass and passing their check, date M6 too and set `status` to `captioned`: both
dates are recorded. Where a gate was waived, record it as the ladder says, with the author's
reason. _Mechanical._

## 10. Hand back

> **Skill:** `cut-for-platform` · **Guide:** `publishing/docs/reference/cut-downs.md`

Report what was rendered, each probe, every `verify` key relied on and anything that failed and
why. Point at the next procedures: `publishing/workflows/03-caption-a-piece/` where captions are
still owed, and `publishing/workflows/04-brief-a-thumbnail/` for the thumbnails. _Substantive._

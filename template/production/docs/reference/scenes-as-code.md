---
type: guide
skills: [cut-for-platform]
model: opus
---

# Scenes as code — the author's drawings timed to their approved voice

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A scene piece draws its picture from tracked Python and accepted voice timings.
Its shot list contains Type `scene`; stills, cards and recorded footage keep the assemble route.
The neutral kit supplies timing and movement; the brand supplies the look and sprite exports.

## The scene file and its clock

Keep one `production/src/scenes/<piece>.scene.py`, defining `build_scene(root, piece)`.
It returns `Scene(root, piece, frames, layout, fps=30)` from `toolkit/media_scene.py`.
`layout(width, height, safe)` returns `Element` objects arranged for that native frame size.
Set the length in frames and the frame rate; each draw is a function of its frame number.
Python computes every state; the page's inline JavaScript only paints it. Never add a timer,
randomness, CSS animation or transition. A design pixel is one frame pixel at device scale one.
Use the brand's custom properties in `style`, and local brand CSS in `stylesheets`.
Every run writes the ignored scene page afresh; never edit that page.

## Typed lines, movement and anchors

Elements have a unique `name`, `kind`, `x`, `y`, `width`, `height` and fixed `layer` order.
A text element's `typed=True` and `type_hold` reveal characters at whole-frame intervals.
Its `start` and `end`, and a `Keyframe.at`, may name `beat:1`, `board:b01`, `line:1.1` or
`word:0`; add `:end` for that interval's end. Word indexes refer to accepted original words.
Integer times name master frames. Voice references include the edit voice row's `at` offset.
Keyframes set positions or `anchor='label.left'`; define that local point in the label's
`anchors`. Movement holds for the element's whole-frame `hold` and snaps to pixels.
A keyframe can set `pose` and `facing`; walk poses step at the sprite's `walk_hold`.
At arrival, its `response` can highlight the target with a brand token, `nudge` it by whole
pixels or `reveal` it. The character faces and points at it in the pose the author names.

## Sprites and their mouths

A sprite element takes a `Sprite(folder, name, extension, scale)`; scale is a whole number.
Whole frames are `<sprite>-<pose>-mouth-<shape>`, shapes A–H and X in lower case; a revised pose is `<pose>-vN`, filed whole, and a revised mouth layer makes a new sprite, `<sprite>-vN`.
With `layered=True`, use `<sprite>-<pose>` plus `<sprite>-mouth-<shape>` at the native `mouth`
origin. Optional `<sprite>-<pose>-blink` overlays blink by frame; missing blink art does not blink.
`breathe_hold` bobs an idle sprite by one sprite pixel; `walk` names its cycle's poses.
The mouth samples `(frame + 0.5) / fps` minus the voice offset, inside each half-open cue.
It rests at X in gaps; a sub-frame cue may not appear. Missing required art is exit 2 by name.

## Real sources, stills and masters

Accept words and mouths into `production/src/timing/`, and cues and real data into
`production/src/scenes/`, through their producing commands' `-o`; never edit the JSON.
A source element names a `source` in real JSON: `{piece, sources: [{source, kind, path, sha256}]}`.
Kinds are `image` and `text`, paths repository-relative. Text captures appear as literal text.
Only indexed images and captures load; recorded video belongs to a footage piece.
Run `uv run toolkit/scene.py stills <piece> --size WxH` at each aspect, repeating `--size`.
It writes first/middle board frames and a report `{piece, fps, stills}`; each still records
`board`, `size`, `frame`, `path`, measured `boxes` and `findings`. Open every printed PNG path.
Text overlaps, overflow, boxes outside the combined safe zone and fractional positions are
findings, exit 1. Safe margins take the largest edge of that aspect's brief and cut deliverables.
The preview is `uv run toolkit/scene.py render <piece>`; further aspects use `--size WxH`.
Masters use the edit's size by default, and its audio rows, sample rate and loudness key.
The accepted joined voice drives both mouths and sound; clip and overlay rows are refused.
The first master is `<piece>.master.mp4`, others `<piece>.master.<W>x<H>.mp4`; render natively.
`--memory-max SIZE` overrides `MEDIA_MEMORY_MAX`; systemd caps memory with swap disabled where
available. Otherwise the run reports that it is uncapped. Frame count and held sound are checked.

## How we apply it here

- Apply Timing notes through `production/workflows/09-time-the-voice/`, then review new stills.
- The author checks mouths and the preview before dating `M4.stills`; keep the ladder's order.
- Animate the author's own art as `ai_visuals: assisted`; use a native master for each cut aspect.

## Who implements it

- **Workflow:** `production/workflows/10-animate-a-scene/`; **skill:** `cut-for-platform`.

## Governing standard

`.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 owns rendering; rules 06 Section 12 permits still review.
The piece ladder owns M4; this guide owns the neutral scene kit and its review.

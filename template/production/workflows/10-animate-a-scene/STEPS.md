---
workflow: 10-animate-a-scene
phase: produce
skills: [cut-for-platform]
model: opus
---

# STEPS.md — animate a scene

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

Run in order with `CHECKLIST.md` open. This procedure completes `M4.stills` and M4
(storyboarded → produced) for a scene piece; the piece ladder owns the gate.

## 1. Read the piece and accepted timing

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/scenes-as-code.md`

Read the brief, script, re-timed storyboard, shot list, accepted words/check, mouths and cues,
and the brand tokens and art register. Confirm Type `scene` and the preceding M4 sub-checks.
Missing or changed timing returns to `production/workflows/09-time-the-voice/`; never animate
estimated word times. Record the author's own art animated by code as `ai_visuals: assisted`.
_Substantive._

## 2. Index the real sources

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/scenes-as-code.md`

Run `python3 toolkit/media.py real <piece>` and read its findings. The shot list names only
images and small text captures; a video or sound cannot become a scene source. Fix the source
record, never the working JSON. Once accepted, repeat with
`-o production/src/scenes/<piece>.real.json`, then commit the tracked index. _Mechanical._

## 3. Write the scene and its sound edit

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/scenes-as-code.md`

Write the one tracked scene with `build_scene(root, piece)` returning `Scene`; make its layout
for every required native aspect. Set its frame count, typed lines, sprite poses, walk cycle,
blinks, breathing and anchor interactions on accepted beat, line or word boundaries. The look
comes from the brand tokens and art. The edit has no clip/overlay rows; its audio rows mix the
same joined voice with approved music/effects, linked to their script event IDs by `cue`.
Keep the author's chosen size, audio rate and loudness key. Ask before replacing an approved
scene or edit; never change generated output. _Substantive._

## 4. Draw and review the stills

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/scenes-as-code.md`

Run `uv run toolkit/scene.py stills <piece> --size WxH`, repeating `--size` for each aspect.
Read every finding; open every first/middle PNG by its printed path. Check mouths, text,
walks, pointing and responses with the author, including the safe zones. Resolve overlaps,
overflow and fractional positions in the scene. Missing art is supplied as a brand export,
never guessed. Timing notes go back through `production/workflows/09-time-the-voice/`, then
make and review new stills. Do not date the sub-check from JSON alone. _Substantive._

## 5. Render and agree the preview

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/scenes-as-code.md`

Run `uv run toolkit/scene.py render <piece>` at the edit's size; this preview is the first
master itself. Offer the author the printed path to play. Apply notes to the tracked source,
route Timing notes as above, then repeat stills and preview. The author agrees the current
mouths and picture against the voice before dating `M4.stills`, after its preceding sub-checks.
The optional `--memory-max SIZE` or user-scope `MEDIA_MEMORY_MAX` bounds a heavy render where
systemd is available; read the capped/uncapped note. _Substantive._

## 6. Render the other native aspects and hand back

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/scenes-as-code.md`

Render each further aspect with `uv run toolkit/scene.py render <piece> --size WxH`.
Read frame-count, sound-length and loudness findings; probe every master and quote the evidence.
Record M4 only once its sub-checks and measured masters hold, and update `last_updated`.
Give every master path and outstanding rights/disclosure work. The cut-down plan lists the
masters, default first, and uses Frame `native` for cuts from the matching aspect. _Mechanical._

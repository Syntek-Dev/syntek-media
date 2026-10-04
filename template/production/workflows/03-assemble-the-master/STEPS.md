---
workflow: 03-assemble-the-master
phase: produce
skills: [cut-for-platform]
model: opus
---

# STEPS.md — assemble the master

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for building a piece's master from its edit decision list. Each step names
the skill and guide it uses. **Run in order** (no list is assembled before every source it names
verifies) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). The
> `cut-for-platform` skill runs every step but the retiming of a recorded piece's captions.

## 1. Confirm the piece is ready

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/edit-decision-lists.md`

Read the piece's brief. Its `status` is `storyboarded`, or `scripted` with M3 recorded as not
applicable (a recorded piece, or a piece with `picture: false`, such as a standalone voiceover,
whose master is an audio master); its script or transcript is approved. If a gate before M4 is
open, say which and stop: route to the procedure that closes it.
_Substantive._

## 2. Check every source

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/source-media.md`

Go through the shot list (or the transcript's beats, or for a piece with no picture the
script's): every shot has a source. Run
`python3 toolkit/media.py footage verify`; every footage ID the edit will use must be logged and
must verify. Every asset is in `production/src/assets/`; every voiceover segment the edit uses is
`approved` and archived in its register; every licensed or identifiable item has its rights row.
Anything missing goes to `production/workflows/01-log-source-media/`,
`production/workflows/02-make-a-voiceover/` or `production/workflows/07-clear-the-rights/`
first. _Mechanical._

## 3. Copy the cards

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/edit-decision-lists.md`

For each card the storyboard names (a title, an end card), copy the brand's component
`brand/src/design-system/previews/card.html` (or `toolkit/templates/card.html` where the brand
has none) to `production/src/cards/<piece>.<card>.html`, fix its stylesheet link to
`../../../brand/src/design-system/tokens.css`, and write the card's words with the author. Delete
from the copy the brand component's own `AUTHOR TO CONFIRM` line about the brand's layout: the
brand file keeps it and `media.py flags` reports it there, so it never counts against the piece.
Run `uv run toolkit/card.py check` on each. Never edit the brand's component here. _Substantive._

## 4. Write the edit decision list

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/edit-decision-lists.md`

With the author, write `production/src/edits/<piece>.toml`: the `[edit]` table (the master's
frame, chosen with the author from the brief's deliverables, or `""` for an audio master; the
sample rate; the loudness target), then the clips in timeline order from the storyboard rows, or
from a recorded piece's transcript anchors; overlays for cards over the picture; and `[[audio]]`
for the voice (`vo:<piece>`), each music bed with its fades and ducking, and any effects.
_Substantive._

## 5. Assemble

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/edit-decision-lists.md`

Run `python3 toolkit/media.py assemble production/src/edits/<piece>.toml`. It renders any card
PNG that is missing or stale with `uv run toolkit/card.py` first; exit 2 names uv or Chromium
when it cannot, so report the install hint it prints and stop. Exit 1 means the master failed
its own verification: report what failed, correct the list, and assemble again. _Mechanical._

## 6. Probe and measure

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/sound-and-loudness.md`

Run `python3 toolkit/media.py probe` on the master and `loudness measure` on it. Quote the
duration, the frame, the streams, the integrated loudness and the true peak against the target
the list names. A master off its target goes back to step 4, never to a hand adjustment.
_Mechanical._

## 7. Carry a recorded piece's captions to the master

> **Skill:** none · **Guide:** `production/docs/reference/recorded-pieces.md`

For a recorded piece only: run `python3 toolkit/media.py captions retime` on the recording-timed
captions (`publishing/src/captions/<piece>.<FID>.en-GB.srt`) with `--edl` naming this list,
`--source` the recording's footage ID and `-o publishing/src/captions/<piece>.en-GB.srt` (without
`-o` it writes to the terminal). Those master-timed captions are what the cut-down plan reads.
Skip this step for a scripted piece, and say so. _Mechanical._

## 8. Watch it through and record M4

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/edit-decision-lists.md`

The author watches or hears the whole master. A change goes back to step 4 as a new `version` of
the list. On the author's yes, and not before, record M4 in the brief's `verified` with today's
date and set `status` to `produced`. _Substantive._

## 9. Hand back

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/edit-decision-lists.md`

Report the master's name and measurements, the list's version, the sources and takes it uses,
and the cards it shows. Point to `publishing/workflows/01-plan-the-cut-downs/` for the cut-downs
and `publishing/workflows/02-cut-for-a-platform/` for the deliverables. _Substantive._

---
workflow: 04-master-a-podcast-episode
phase: produce
skills: [cut-for-platform]
model: opus
---

# STEPS.md — master a podcast episode

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for an episode's audio master. Each step names the skill and guide it uses.
**Run in order** (no list is assembled before every source it names verifies) and tick
`CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). The
> `cut-for-platform` skill runs every step.

## 1. Confirm the episode

> **Skill:** `cut-for-platform` · **Guide:** `scripts/docs/reference/podcast-episodes.md`

Read the episode's brief: `kind: podcast`, `picture: false`, and M2 dated (the script approved,
or the transcript for a recorded episode). If M2 is open, say so and stop: route to
`scripts/workflows/02-write-a-script/` or `production/workflows/08-bring-in-a-recording/`.
_Substantive._

## 2. Record M3 as not applicable

> **Skill:** `cut-for-platform` · **Guide:** `scripts/docs/reference/podcast-episodes.md`

An episode has no picture, so it has no storyboard. If the brief's `verified` has no M3 entry
yet, record `M3: 'n/a — no picture'` and leave `status` at `scripted`. _Mechanical._

## 3. Check every source

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/source-media.md`

Run `python3 toolkit/media.py footage verify`: every recording, music bed and sting the episode
uses must be logged and must verify. A music bed has its rights row; a guest has a signed release
in the rights register; any voiceover segment the episode uses is `approved` and archived.
Anything missing goes to `production/workflows/01-log-source-media/`,
`production/workflows/02-make-a-voiceover/` or `production/workflows/07-clear-the-rights/`
first. _Mechanical._

## 4. Write the audio edit decision list

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/edit-decision-lists.md`

With the author, write `production/src/edits/<piece>.toml` with `size = ""`,
`loudness = "podcast"` and the sample rate: clips from the recording in order, their `in` and
`out` from the transcript's anchors (or `vo:<piece>` for a voiced episode), and `[[audio]]` for
the intro and outro bed, with `fade_in`, `fade_out` and `duck = true` under speech. Where a
synthetic voice speaks, place its spoken disclosure line in the episode. Every cut that removes
more than a pause or a false start is the author's decision. _Substantive._

## 5. Assemble

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/edit-decision-lists.md`

Run `python3 toolkit/media.py assemble production/src/edits/<piece>.toml`. Exit 1 means the
master failed its own verification: report what failed, correct the list, and assemble again;
exit 2 means it could not run, so report the reason it gives and stop. _Mechanical._

## 6. Measure against the podcast target

> **Skill:** `cut-for-platform` · **Guide:** `production/docs/reference/sound-and-loudness.md`

Run `python3 toolkit/media.py probe` (audio only, at the expected length) and `loudness measure`
on the master, and quote the integrated loudness and true peak against
`[platform.podcast.apple_rss_audio]`. A master off target goes back to step 4. _Mechanical._

## 7. Listen through and record M4

> **Skill:** `cut-for-platform` · **Guide:** `scripts/docs/reference/podcast-episodes.md`

The author hears the whole episode. A change goes back to step 4 as a new `version` of the list.
On the author's yes, and not before, record M4 in `verified` with today's date and set `status`
to `produced`. _Substantive._

## 8. Hand back

> **Skill:** `cut-for-platform` · **Guide:** `scripts/docs/reference/podcast-episodes.md`

Report the master's name, length and measurements, the list's version and the sources it uses,
and whether a disclosure line is in the audio. Point to
`publishing/workflows/02-cut-for-a-platform/` for the feed files and
`publishing/workflows/05-prepare-a-post/` for the episode and show descriptions, which carry the
disclosure too. _Substantive._

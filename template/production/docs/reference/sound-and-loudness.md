---
type: guide
skills: [cut-for-platform]
model: opus
---

# Sound and loudness — where each sound sits, and how loud the master lands

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A master has one voice, sometimes a music bed and effects, and one loudness
target. The voice comes first: music sits under it, ducks when it speaks, and fades in and out
rather than starting or stopping dead. The target is set by the deliverable, never by ear, and
the toolkit measures it rather than trusting a meter on screen.

## The targets

| Deliverable | Target | Where it comes from |
|---|---|---|
| Social video | −14 LUFS integrated, −1 dBTP true peak | a house decision, because no social platform publishes one: `[house]` in `toolkit/data/platforms.toml` |
| Podcast episode | the platform's own published recommendation | `[platform.podcast.apple_rss_audio]`, its `loudness_lufs` and `true_peak_db` |
| Audiobook chapter | RMS, peak and noise floor, not LUFS | `[audiobook.acx]`, set out in the audiobook narration guide where the project makes audiobooks |

`loudness` in an edit decision list (`social`, `podcast` or `none`) chooses the master's target.
`python3 toolkit/media.py loudness normalise FILE --target social|podcast|acx` applies one in two
passes, always resampling the output, then measures again: within ±1 LU and under the peak, or it
fails. `loudness measure` reports integrated loudness, true peak and range. The social value is a
house decision and is recorded as one; if a platform ever publishes a target, the data file
changes, not this guide.

## Where a music bed goes

- A music bed is source media: a footage row with `kind = "music"` and a rights row
  (`production/docs/reference/source-media.md`).
- It goes in an `[[audio]]` table with `role = "music"`, `at` where it starts on the timeline,
  and `in` and `out` when only part of the track is used.
- `duck = true` lowers it whenever the voice speaks; set `gain_db` so it sits well under the voice
  even where nobody is speaking.
- Effects (`role = "effect"`) are placed the same way and are never ducked.

## Fades

`fade_in` and `fade_out` on an `[[audio]]` table are in seconds. Every bed fades in and out: a
hard start or stop sounds like a mistake. A picture cross-fade (`transition = "fade"` on a clip)
carries the clip's own sound across with it. Under a recorded speaker's pauses, keep the room's
own sound rather than cutting to digital silence.

## How we apply it here

- Mix the voice first, then the bed under it, then the effects; the target is met on the
  finished mix, never on a part of it.
- Measure the master with `loudness measure` before calling it done, and quote the figures.
- Each deliverable is encoded to its own target in the cutting pass, never adjusted by ear.
- An episode's master is an audio master with `loudness = "podcast"`, made by its own procedure
  where the project makes podcasts.
- Never lift a quiet recording past its noise: record it again or accept it, with the author.

## Who implements it

- **Workflow:** `production/workflows/03-assemble-the-master/`.
- **Skill:** `cut-for-platform` sets `loudness` and each bed's `gain_db`, `duck` and fades, then
  runs `assemble` and `loudness measure`.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the ladder, whose M4 needs the
master within its target; `toolkit/data/platforms.toml` owns every platform number. This guide
owns where each sound sits and how its level is set.

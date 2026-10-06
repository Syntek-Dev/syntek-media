---
type: guide
skills: [cut-for-platform]
model: opus
---

# Edit decision lists — the master as a list of decisions, rebuilt on demand

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A master is never edited by hand. It is described, clip by clip, in
`production/src/edits/<piece>.toml`, and `python3 toolkit/media.py assemble` builds it from that
list, the logged footage, the cards and the approved voiceover. Change the list and assemble
again: the master is generated, and the list is the record. It is written with the author from
the storyboard and shot list or, for a recorded piece, from its transcript.

## The edit and its clips

`[edit]` holds `piece`, `version`, `size` (the master's frame; `""` for an audio master, which
takes sound only from its clips), `audio_rate` and `loudness` (`social · podcast · none`). Then
one `[[clip]]` per clip, in timeline order:

| Field | Holds |
|---|---|
| `id` | `c01` onwards, permanent within the list |
| `source` | a footage ID, an asset under `production/src/assets/`, or a card under `production/src/cards/` |
| `in`, `out` | a video or audio source's range, `HH:MM:SS.mmm` |
| `seconds` | how long a still, a card or a colour clip holds |
| `colour` | `"#RRGGBB"` with no source: a blank clip of `seconds` |
| `frame`, `x` | `fit · crop · pad`, and the crop offset in source pixels |
| `mute` | `true` drops the clip's own sound |
| `motion` | stills and cards only: `none · push-in` (a slow zoom) |
| `transition`, `transition_seconds` | how the clip enters: `cut · fade` (a cross-fade) |

In a picture master every clip has a picture; a sound with no picture goes in `[[audio]]`.

## Overlays and sound

- `[[overlay]]` lays a card, rendered with a transparent background, over the picture from `at`
  to `until`, each on the frame it rounds to as a clip's start does: an overlay timed to a
  clip's start or end starts or ends with that clip, and one that would show on no frame is refused.
- `[[audio]]` places a sound on the timeline at `at`. Its `source` is `vo:<piece>` (the piece's
  approved voiceover segments, joined in order with their pauses), a footage ID or an asset;
  `in` and `out` take part of it; `gain_db`, `fade_in` and `fade_out` shape it; `role` is
  `voice · music · effect`, and `duck = true` lowers a music bed under the voice.
  Optional `cue = "e02"` links a script SFX/MUSIC event; `media.py cues` copies this row's mix.

## Stills, cards and the trailer kit

A trailer or explainer made of stills and cards is a list like any other: still and card clips
with `seconds`, `motion = "push-in"` where one should drift, `transition = "fade"` between them,
and a music bed in `[[audio]]`. Cards are HTML files in `production/src/cards/`, copied from the
brand's card component; `assemble` renders any card PNG that is missing or older than its HTML
or the brand's tokens before it composites, so a master always rebuilds from tracked files.
Every clip starts and ends on the master's frame nearest its running total, never rounded clip by
clip: 187 stills of 0.16 s end on the frame nearest 29.92 s, one holding a frame more or less.
Each still, card and colour is framed alone to the master's size, so stills of any size, format
or orientation with no push-in or fade between them are one input, read an image at a time, and
a long run needs no more memory than a short one; each video, push-in or fade opens another.
Transitions beyond a cross-fade, motion beyond a push-in and layered picture are not in this version.

## How we apply it here

- One list per piece, named for the piece; raise `version` when the author approves a new cut.
- Every source is logged and verifies first (`production/docs/reference/source-media.md`).
- Cuts are frame-accurate: the toolkit re-encodes a cut and never stream-copies one.
- Probe every master before reporting it, and quote what was measured.
- An audio master is the same list with `size = ""`: an episode is cut from a recorded talk this
  way, by its own procedure, where the project makes podcasts.

## Who implements it

- **Workflow:** `production/workflows/03-assemble-the-master/`.
- **Skill:** `cut-for-platform` writes the list with the author, copies the cards and runs
  `assemble`.

## Governing standard

`.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 owns how the toolkit renders, and
`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the ladder whose gate M4 the
master passes. This guide owns how an edit is written down.

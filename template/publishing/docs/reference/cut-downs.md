---
type: guide
skills: [repurpose, cut-for-platform]
model: opus
---

# Cut-downs — one long piece, several short ones that stand alone

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A cut-down is a short deliverable cut from a piece's master: a talk's sharpest
moment as a Short, a trailer's first line as a reel, an explainer's one idea as a vertical post.
It is planned in `publishing/src/cut-downs/<piece>.md` before it is cut, so every cut's moment,
frame and hook are agreed with the author before a render is made. A cut-down is never a new
piece: it carries the master's lines under the master's brief, and lives only in the plan.

## The plan

| Column | Holds |
|---|---|
| Cut | `c01`, `c02` …, permanent; a dropped cut keeps its number and its row |
| Deliverables | the `toolkit/data/platforms.toml` keys the cut is rendered for |
| Lines | the script or transcript lines it carries, as `beat.line` ranges (`3.2–3.9`) |
| In, Out | `HH:MM:SS.mmm` on the master, never on a recording or on another cut |
| Frame | `centre`, `crop x=<px>` or `pad` |
| Hook | the words the cut opens on |
| Status | `planned · approved · rendered · checked` |

Under the table, one `## cNN — <hook>` section per cut gives its opening words, its on-screen
title, its caption width, whether it needs its own thumbnail, and why this moment stands alone.

## Finding the moments

- **A cut stands alone.** A viewer who has never seen the master understands it from its first
  line. A line that leans on an earlier beat ('as I said') is left out, or the cut starts earlier.
- **The hook comes first,** in words and on screen. A cut that warms up loses its viewer before
  the point arrives.
- **Times come from the record, not the ear.** In and Out are read from the master-timed captions
  or the edit decision list; for a recorded piece, from the captions its transcript was aligned
  and retimed into (`production/docs/reference/recorded-pieces.md`).
- **A silent loop** for a web page (`website.hero_loop`) is a cut with no words (Lines `—`),
  outside the stand-alone and near-identical rules; its note names any cut it shares frames with.
  A GIF preview is not a cut but a thumbnail brief's (`publishing/docs/reference/thumbnails.md`).

## Framing and safe zones

- A landscape master reframed to vertical is cropped (`crop x=<px>`, the speaker kept in frame)
  or padded (`pad`, the whole picture kept); the storyboard's Vertical framing column is the first
  answer, and the author's eye is the last.
- Faces, on-screen text and captions stay inside the deliverable's `safe_zone`; a `safe_zone`
  named in its table's `verify` is unconfirmed, so leave margin and flag it.
- A cut's length stays inside its deliverable's `max_seconds`; `media.py cut` fails its
  verification on one that does not, and the plan is changed, never the limit.

## Near-identical batches

YouTube's monetisation policy names 'inauthentic content' (renamed from repetitious content on
15/07/2025): mass-produced, generic or repetitive uploads, such as template-made content without
the creator's own insight. A batch of cuts that differ only in crop or caption reads that way on
every platform, so each cut earns its place with a different moment, and `repurpose` refuses a
batch that does not. Source: https://support.google.com/youtube/answer/1311392 (checked 03/10/2026). <!-- scrub: allow — help-centre article number -->

## How we apply it here

- Plan first, cut second: no cut is rendered before its row is `approved`.
- Cut from the master only, so every cut inherits the master's loudness, rights and disclosure.
- Make a cut's captions before cutting it where they can be, so the cutting pass burns them in.

## Who implements it

- **Workflows:** `publishing/workflows/01-plan-the-cut-downs/` plans the cuts;
  `publishing/workflows/02-cut-for-a-platform/` renders and verifies them.
- **Skills:** `repurpose` proposes the moments and writes the plan; `cut-for-platform` renders
  each cut through `python3 toolkit/media.py cut` and verifies it against its preset.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 1 owns who decides (every cut is
approved by the author) and Section 3 owns the ladder a rendered cut serves;
`.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 owns how renders are made. The rules
own the requirement; this guide owns choosing, timing and framing the moments.

---
type: guide
skills: [thumbnail-brief]
model: opus
---

# Thumbnails — one promise, read at the size it is seen

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A thumbnail or cover is the still that sells a deliverable before it plays: one
promise, in a few words and one image, read at the size of a fingertip. Each is briefed in words
first, then laid out in HTML from the brand's own layout and rendered to PNG by the toolkit, so a
thumbnail is always remade from tracked files and the brand's tokens. A piece has one brief, or
one per cut where a cut needs its own (`--cNN`).

## The brief

`publishing/src/thumbnails/<piece>[--cNN].md` carries frontmatter `piece`, `cut` (`cNN`, or empty
for the full-length deliverables), `deliverables` (the keys it is rendered for), `html` (its
layout) and `approved` (DD/MM/YYYY, or empty). Its body:

| Section | Holds |
|---|---|
| `## Promise` | the one thing a viewer gets by pressing play, in a sentence |
| `## Words on the image` | the words, as few as carry the promise, and never the title repeated |
| `## Image` | the picture: a frame of the master, a still, or the brand alone |
| `## Variants` | any second version, and why it exists |
| `## Checks` | each check below, with its result |

## The layout

The layout is a copy of the brand's component, `brand/src/design-system/previews/thumbnail.html`,
or of `toolkit/templates/thumbnail.html` where the brand has none, saved as
`publishing/src/thumbnails/<piece>[--cNN].html` with its stylesheet link fixed to the brand's
`tokens.css`. One file serves every aspect through media queries; text stays inside the
`--safe-*` variables `card.py` sets from the preset; images load by relative path, never over the
network. A layout changed in the brand reaches every later piece, never an earlier copy. A frame
used as the image is made with `python3 toolkit/media.py frame -o` into `production/src/assets/`,
a small committed still, never pointed at a render, because renders are ignored by Git.

## Which deliverables take one

- A deliverable with a thumbnail or cover table in `toolkit/data/platforms.toml` renders at that
  table's size: `uv run toolkit/card.py render <html> --deliverable KEY`.
- A table without a pixel size (its `verify` names `width` and `height`) renders with `--size` at
  a size the author confirms, flagged `VERIFY`.
- A platform with no thumbnail table at all (LinkedIn, Facebook and TikTok on 03/10/2026) renders
  at its video deliverable's size, flagged `VERIFY` in the brief and the platform's guide.

## Checks at thumbnail size

- **Legible small:** look at the PNG at a fingertip's width before anyone approves it.
- **Inside the safe zone,** clear of the platform's controls and overlays.
- **Inside the grid crop** where Instagram shows it: titles stay within
  `platform.instagram.grid_aspect`, a `verify` key.
- **The table's `notes`:** a platform's own art advice (avoid text, no transparency) is read there.
- **Rights:** a face, a stock image or a font that needs one has a `cleared` row in
  `production/src/rights-register.md`.

## How we apply it here

- Brief before layout; layout before render; the author approves the PNG, not the HTML.
- Renders land in `publishing/src/renders/` as `<html-stem>.<platform>-<format>.png`.
- A thumbnail promises nothing the deliverable does not deliver.

## Who implements it

- **Workflow:** `publishing/workflows/04-brief-a-thumbnail/`.
- **Skill:** `thumbnail-brief` writes the brief, copies and fills the layout, checks it with
  `uv run toolkit/card.py check` and renders each deliverable.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the ladder (M7 needs every
thumbnail approved where the platform takes one) and Section 6 owns rights;
`.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 owns renders. The rules own the
requirement; this guide owns how a thumbnail is briefed, laid out and checked.

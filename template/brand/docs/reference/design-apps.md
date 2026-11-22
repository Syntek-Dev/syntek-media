---
type: guide
skills: []
model: opus
---

# Design apps — made in an app outside the repository, brought back as exports

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** The brand's tokens and its two layouts are plain files in
`brand/src/design-system/`, written by hand and rendered by `card.py`. Everything else the brand
draws — a logo, a photograph for a thumbnail, a sprite, a one-sheet — is made in a desktop app
outside the repository and comes back as an export in `brand/src/exports/`, one register row each.
No app writes into the kit, and no app's project file is kept here.

## Who takes each job

| Job | App | Comes back as |
|---|---|---|
| Logo, marks, wordmark | VectorCraft | an SVG master with PNG or WebP variants |
| Photographs, retouching, composites for a thumbnail or card | PhotoCraft; VectorCraft for graphic art | PNG, JPEG or WebP, placed by the layout |
| A graded still from the piece's own footage | DaVinci Resolve (still export, `VERIFY`) | PNG; its Notes name the footage ID |
| Sprite poses and mouth shapes for a code-animated scene | VectorCraft, one artboard each, text outlined (`VERIFY`) | one SVG per pose or mouth shape |
| A one-sheet or press kit, where the brand wants one | DesignCraft | PDF or PNG; never a card or thumbnail |
| Palette, type, spacing | none: `tokens.css`, written by hand | the kit itself |

- VectorCraft is ArtCraft's open-source vector illustration app, PhotoCraft its raster editor and
  DesignCraft its page-layout app (`VERIFY`, as every format in the table). VectorCraft draws and
  edits; it does not propose a look, so the design thinking is the author's, with the session.
- A VectorCraft swatch export as CSS (`VERIFY`) may be read and copied into `tokens.css` by hand;
  it never overwrites the file.
- A moving shot (a push-in, a build-up, a lower third) is not a design job:
  `production/docs/reference/complex-shots.md` brings it back as footage.

## The round trip

1. Make or revise the design in its app, from the tokens and the brand's own fonts.
2. Export at the size the layout or platform needs. Size is set by artboard or page size times a
   scale, not by pixel width and height (`VERIFY` per app).
3. Name the file as `brand/docs/reference/design-exports.md` says, and file it through
   `brand/workflows/03-record-a-design-export/`: the register's second column names the app, its
   version and the project file's label, never a path or a link.
4. AVIF is not written by VectorCraft or DesignCraft, and by PhotoCraft only in some builds
   (`VERIFY`): `media.py image` makes it from the PNG where a platform needs it.

## Project files, versions and MCP

- The app's project file (`.vectorcraft`, `.pcraft`, `.designcraft`, a Resolve project; `VERIFY`)
  stays outside the repository, whatever its format; the export is the evidence.
- The ArtCraft apps are early alpha and release every few days (`VERIFY`, checked 22/11/2026): pin
  the version you use, and check every flag, format and setting against it before relying on it.
- The template offers no app's MCP server. An owner who wants one adds it at user scope, confined
  to read `brand/src/` and write only `brand/src/exports/`: VectorCraft and DesignCraft take read
  and write roots; PhotoCraft takes them with its headless switch, always given, or it may drive
  the app's own folders (`VERIFY` every flag). A bridge to a running app is not confined, so the
  owner watches it. Any Resolve server is a third party's, chosen and supervised by the owner.

## How we apply it here

- Every design, however it was made, ends in an export and its register row; an MCP session too.
- An export with sound (an animation, a graded clip) is footage, logged with `footage add`; its
  loudness is set and checked by `media.py` against `toolkit/data/platforms.toml`, never by the
  app's own normalisation. Stills, SVG and PDF carry no sound.
- A claim about an app is `VERIFY` until it is checked against the installed version.

## Who implements it

- **Workflows:** `brand/workflows/01-set-up-the-brand-kit/` writes the tokens and layouts;
  `brand/workflows/03-record-a-design-export/` files each export.
- **Skills:** none; the author makes the design, and Claude checks, files and records it.

## Governing standard

`.claude/rules/syntek-media/06-global-rules.md` Section 4 owns never overwriting a brand file or an
exported design asset, and Section 8 the grilling pass design work opens with;
`.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 owns loudness and what never leaves
the toolkit. The rules own the requirements; this guide owns which app takes which design job and
how its work comes back.

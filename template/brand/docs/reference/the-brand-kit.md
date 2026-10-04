---
type: guide
skills: [thumbnail-brief]
model: opus
---

# The brand kit — one set of tokens behind every layout

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** The brand kit is the part of the brand a renderer can read: the CSS custom
properties in `brand/src/design-system/tokens.css`, the font files beside them, and seven preview
cards, two of which are the brand's own thumbnail and title-card layouts. Every thumbnail, card
and burned-in caption is drawn from it, so a colour or a typeface changes in one place and every
later piece follows. It is not the brand guide's words or the written voice: where syntek-author
is applied, those stay in its brand files, and the kit agrees with them.

## The required tokens

`tokens.css` is plain CSS: one `:root` block of custom properties, and one font-face rule per
font file above it. There is no `tokens.json`; nothing else holds a token.

| Group | Required properties | Rule |
|---|---|---|
| Colour | `--color-bg`, `--color-surface`, `--color-text`, `--color-text-muted`, `--color-accent`, `--color-on-accent` | `#RRGGBB`; text on background and on surface, and on-accent on accent, at least 4.5:1 (WCAG 2.2 AA) |
| Type | `--font-display`, `--font-body`, `--weight-display`, `--weight-body` | a family loaded from the fonts folder, or a generic family |
| Space | `--space-unit`, `--radius` | layouts multiply the unit; never a fixed margin typed into a card |
| Captions | `--caption-font`, `--caption-weight`, `--caption-size`, `--caption-text`, `--caption-outline`, `--caption-outline-width` | sizes in `vh`; colours `#RRGGBB`; `captions burn` turns them into the burned style |

`python3 toolkit/media.py tokens` and `uv run toolkit/card.py check` fail when one is missing or
will not parse. The brand may add tokens of its own beside them.

## Fonts

- Each face is a file in `brand/src/design-system/fonts/`, loaded by its own font-face rule
  with a relative source, so every render works offline; nothing loads over the network.
- Every font has a `font` row in `production/src/rights-register.md` before a piece using it is
  scheduled. A licence for print or the desktop does not always cover video or thumbnails.
- `--caption-font` names a family in the fonts folder or one installed on the machine;
  `captions burn` fails rather than burn a caption in a fallback face.

## The previews and the two layouts

Each card in `brand/src/design-system/previews/` opens on line 1 with
`<!-- @dsCard group="…" -->`, the line Claude Design indexes, and links ../tokens.css. Five show
the kit; `thumbnail.html` and `card.html` (group `Components`) are the brand's layouts.
`thumbnail-brief` copies the first for a piece's thumbnails and covers, and `cut-for-platform`
copies the second into `production/src/cards/` for its title and end cards, each falling back to
`toolkit/templates/` only where the brand's file is absent. A copy belongs to its piece, so a
changed layout reaches every later piece and never one already copied.

## Agreeing with the written brand

Where syntek-author is applied, its brand guide, standards/brand/brand-guide.md (or the Brand
folder its 00-project.md Paths name), where present, owns the logo rules and the print palette,
and its voice files own the words. Read its colour and type entries before a token is set, and
use the same values unless the author decides otherwise for the screen; a disagreement is
reported to the author with both values, never resolved silently.

## How we apply it here

- The author decides every value; Claude offers options with a recommendation and leaves the
  group's `/* AUTHOR TO CONFIRM: … */` slot until the decision is made.
- Captions are judged at the narrowest vertical size, in a proof of the captions card, and again
  in the first burned deliverable.
- A change to the kit is committed on its own, before any sync with Claude Design, so each
  sync's diff is readable.

## Who implements it

- **Workflow:** `brand/workflows/01-set-up-the-brand-kit/`.
- **Skills:** `thumbnail-brief` copies and renders the thumbnail layout; `cut-for-platform`
  copies the card layout; the grill-with-docs skill (syntek-author), where present, settles the
  kit with the author.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 1 owns who decides a brand fact;
`.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 1 owns the pipeline that reads the
tokens, and Section 3 the rule that renders are never hand-edited. The rules own the
requirements; this guide owns what the kit holds and how it is kept.

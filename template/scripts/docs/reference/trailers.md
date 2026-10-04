---
type: guide
skills: [write-script, storyboard, voiceover]
model: opus
---

# Trailers — a promise built from stills, cards, a voice and music

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A trailer sells a feeling and a question, not a summary: a book, a launch or a
series, briefly, ending on where to find it. In this version of the template a trailer is built
from what the toolkit can assemble without a motion-graphics tool — stills, title and end cards,
colour clips, cross-fades and a slow push-in on a still or a card — under a voiceover and a
music bed. Anything more elaborate is made elsewhere and brought in as footage.

## What a trailer promises

- **The hook:** a single image or line that raises a question the viewer wants answered.
- **The tone:** the voice, the music and the type on the cards tell the viewer what kind of
  thing this is before any word says so.
- **The withheld answer:** the trailer stops before the story resolves; it never gives away the
  turn that the book or the launch exists to deliver.
- **The call to action:** the title, and where and when to find it, on the end card and said
  aloud. A release date or a price not yet settled is `AUTHOR TO CONFIRM`, never a guess.

## Building from stills and cards

Every picture is a shot on the shot list. A still or a card holds for its `seconds` and may carry
`motion = "push-in"`; any clip may enter with `transition = "fade"`; a colour clip fills a beat
between images. Title and end cards are copied from the brand's card component into
`production/src/cards/`, so they share the brand's type and colour. Board the pace first:
how long each image holds is the trailer's rhythm, and the voice is timed to it. In the script, a
`{pause S}` at the end of a line holds the picture after it, so `script time` counts what the
pictures carry as well as the narration, and M2 measures the whole trailer.

## Voice and music

The voiceover is made one segment per spoken sentence or beat, so its timing and its captions
stay exact. A synthetic voice, the brand owner's own cloned voice included, is disclosed. The
music bed is a footage row of its own, licensed and cleared, ducked under the voice and faded
out under the end card; generated music is disclosed like any other generated material.

## Rights a trailer needs

Cover art, stock images, fonts, music and every quotation on a card each need a rights row. A
line of praise is quoted only from a real review, with permission where its source requires it,
and never invented, trimmed to change its sense or attributed to someone who did not say it.

## How we apply it here

- Write the trailer's script after its brief has settled the one question it raises.
- Read the script against the boards: every spoken line has a picture, and every card's words
  appear in a `TEXT:` cue.
- Keep a trailer's cards and stills inside each deliverable's safe zone, read from
  `toolkit/data/platforms.toml`.

## Who implements it

- **Workflows:** `scripts/workflows/02-write-a-script/` writes the script;
  `scripts/workflows/03-storyboard-a-piece/` boards it and lists every still and card;
  `production/workflows/02-make-a-voiceover/` voices it.
- **Skills:** `write-script`, `storyboard` and `voiceover`, in that order.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 6 owns rights and consent, Section 7
forbids a fabricated quotation or endorsement, and Section 5 owns AI disclosure. The rules own
the requirements; this guide owns how a trailer is built.

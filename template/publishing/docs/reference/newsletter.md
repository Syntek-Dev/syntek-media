---
type: guide
skills: [prepare-post, cut-for-platform, thumbnail-brief, captions]
model: opus
---

# Newsletter — email issues: a linked preview image or GIF, never video

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How this project's media reaches an issue of a list in the newsletter profile:
as a still or a short GIF with a play button drawn on it, linked to the page that plays the
piece, because email clients do not play video reliably (`platform.newsletter.video_tag_supported`).
A list is a row of `## Lists` in `brand/src/platforms/newsletter.md`, named by a frozen slug.
Limits are read with `media.py presets KEY`. The issue (its body, blurbs, subject line,
preheader, send time, consent and unsubscribe) is the written side's: media never sends an email
and never holds a subscriber list.

## Deliverables and their keys

| Deliverable | Key | Notes |
|---|---|---|
| A preview image | `newsletter.preview_image` | a frame or the thumbnail layout with its play button; within `max_size` |
| A GIF preview | `newsletter.preview_gif` | a short range of the master under the layout's overlay; plays within `max_seconds` |

- Both are the thumbnail brief's, made with the piece's other images towards M7, never at M5:
  `card.py render <layout> --deliverable KEY` draws the play button (an element carrying
  `data-play-button`), `--transparent` gives the GIF its overlay, and
  `media.py cut <master> --deliverable newsletter.preview_gif --in … --out … --overlay <png>`
  makes the GIF. Its In and Out, and what its first frame shows, go in the brief's `## Image`.
- The GIF keeps to `fps_max` and `colours_max`; over `max_size` the toolkit halves its frame rate,
  then quarters it, and otherwise fails, naming the size.

## Email clients

- **The first frame carries the message:** classic Outlook for Windows shows only a GIF's first
  frame, so the play button and the words are on it, from the overlay.
- **Outlook for Microsoft 365** plays a GIF three times and then shows its own play button over
  it; a GIF that loops past that is cut short, so the toolkit's play count keeps it inside
  `max_seconds` (no email offers a pause control, WCAG 2.2 SC 2.2.2).
- **Dark mode:** a client may invert the issue's colours; the play button is a solid disc with
  its own outline, so it survives inversion. Check the preview on a dark background.
- **Images, not video:** send only `platform.newsletter.image_formats`; WebP and video are not
  shown everywhere. The image is shown at `platform.newsletter.display_width`.
- **Clipping:** some clients clip an issue whose HTML passes `platform.newsletter.html_clip_kb`;
  the house budget is `platform.newsletter.html_target_kb`. The issue's HTML is the written
  side's; the package names the key so the author can check it.

## Placements and agreements

- **A placement** is the one file the issue shows first, the GIF, or the still where there is no
  GIF: `## <key>[ — cNN] — newsletter:<slug>`, with Placement (slug, issue, route), Written piece
  (the issue, by path in prose, read and never edited), Alt text (naming the video and saying the
  image opens it), Links to (the page that plays the piece, posted first, and its publish-log
  URL), Agreement, Disclosure, Images (the still behind a GIF, as a bullet), Render, Calendar,
  Scheduled (the issue's send time, cited) and Limits. Captions read `n/a — no speech`.
- **The agreement** is `own`, or the dated record in the list's row for a list the brand does not
  own: no placement there is `ready` without it.
- **Worked placement:** the studio's monthly list showing a cut's GIF is
  `## newsletter.preview_gif — c03 — newsletter:studio-monthly`, linked to the watch page.

## How we apply it here

- The page a preview links to is a website or blog placement, or an upload, posted before the
  issue is sent; the website and blog guides cover it where the project has those platforms.
- The disclosure line goes beside the preview in the issue, as the house line (no platform label).

## Who implements it

- **Workflows:** `publishing/workflows/04-brief-a-thumbnail/` makes the preview image and the
  GIF; `publishing/workflows/05-prepare-a-post/` writes the placement and its schedule row.
- **Skills:** `thumbnail-brief` makes both images; `cut-for-platform` owns the `cut` they use;
  `prepare-post` writes the placement; `captions` has nothing to do here (no speech).

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the ladder (M7's placements
and agreements), Section 5 disclosure and Section 7 never fabricating a client's behaviour or a
limit. The rules own the requirement; this guide owns how the newsletter keys apply here.

---
piece: 000-example-piece
cut: ""
<: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>deliverables:
<: if 'youtube' in PLATFORMS :>  - youtube.short_thumbnail
<: endif :><: if 'tiktok' in PLATFORMS :>  - tiktok.video
<: endif :><: if 'instagram' in PLATFORMS :>  - instagram.reel_cover
<: endif :><: if 'linkedin' in PLATFORMS :>  - linkedin.video_vertical
<: endif :><: if 'facebook' in PLATFORMS :>  - facebook.reel
<: endif :><: else :>deliverables: []              # no platform this project uses takes a thumbnail here
<: endif :>html: 000-example-piece.html
approved: ""
---

<: if BRAND_KIND == 'business' :># One line before every meeting — thumbnail brief

<!-- WORKED EXAMPLE: the thumbnail brief of the example piece, <: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>for every full-length deliverable at once, because all of them are 9:16.<: else :>with no deliverable, because no platform this project uses takes its vertical video.<: endif :>
     It is not approved: its renders wait for the master, which is never made. -->

## Promise

One habit that stops the next meeting from drifting, in thirty seconds.

## Words on the image

'Write the decision first', in the display face, the largest thing on the image.
Kicker 'Meetings', so the subject reads before the promise.
The brand's name sits under the words, small.
The title, 'One line before every meeting', is never repeated here: the title card and the platform's own title carry it.

## Image

None yet: the layout sets no picture, so the brand's surface colour stands in and the layout renders as it is.
Once the master exists, a frame of the presenter mid-sentence in the close-up of 1.1 goes behind the words, made with `python3 toolkit/media.py frame` and kept as a small committed still in `production/src/assets/`.
<: elif BRAND_KIND == 'author-fiction' :># Count the stones — thumbnail brief

<!-- WORKED EXAMPLE: the thumbnail brief of the example piece, <: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>for every full-length deliverable at once, because all of them are 9:16.<: else :>with no deliverable, because no platform this project uses takes its vertical video.<: endif :>
     It is not approved: its renders wait for the master, which is never made. -->

## Promise

A crossing in the dark, and the question of what moves in the river.

## Words on the image

'What moves in the river?', in the display face, the largest thing on the image.
Kicker 'A new novel', so a stranger knows it is a book before reading the question.
The brand's name sits under the words, small.
The title, 'Count the stones', is never repeated here: the title card and the platform's own title carry it.

## Image

None yet: the layout sets no picture, so the brand's surface colour stands in and the layout renders as it is.
Once the master exists, a frame of the author by the lamp in the close-up of 1.1 goes behind the words, made with `python3 toolkit/media.py frame` and kept as a small committed still in `production/src/assets/`.
<: else :># The second visit — thumbnail brief

<!-- WORKED EXAMPLE: the thumbnail brief of the example piece, <: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>for every full-length deliverable at once, because all of them are 9:16.<: else :>with no deliverable, because no platform this project uses takes its vertical video.<: endif :>
     It is not approved: its renders wait for the master, which is never made. -->

## Promise

The test every welcome has to pass, in the time it takes to read this.

## Words on the image

'Remember their name?', in the display face, the largest thing on the image.
Kicker 'From the next book', so the question reads as an argument, not an advert.
The brand's name sits under the words, small.
The title, 'The second visit', is never repeated here: the title card and the platform's own title carry it.

## Image

None yet: the layout sets no picture, so the brand's surface colour stands in and the layout renders as it is.
Once the master exists, a frame of the author mid-sentence in the medium close-up of 2.2 goes behind the words, made with `python3 toolkit/media.py frame` and kept as a small committed still in `production/src/assets/`.
<: endif :>
## Variants

<: if 'youtube' in PLATFORMS or 'tiktok' in PLATFORMS or 'instagram' in PLATFORMS or 'linkedin' in PLATFORMS or 'facebook' in PLATFORMS :>None: one layout serves every deliverable above, because each is 9:16.
<: else :>None: the example has no deliverable in this project, so the layout is never rendered.
<: endif :><: if 'instagram' in PLATFORMS or 'facebook' in PLATFORMS :>A story cut takes no thumbnail, so the cut-down plan needs no brief of its own.
<: endif :>
## Checks

- **Legible small:** to be judged on each rendered PNG at a fingertip's width, before approval.
- **Safe zone:** the words sit inside the `--safe-*` variables `card.py` sets from each deliverable's preset.
<: if 'instagram' in PLATFORMS :>- **Grid crop:** the words sit in the middle band, inside `platform.instagram.grid_aspect`, a `verify` key.
<: endif :>- **Rights:** nothing to clear yet; the frame added later shows the person under RR0000, the likeness row the brief names.
<: if 'tiktok' in PLATFORMS :><!-- VERIFY: tiktok has no thumbnail table in toolkit/data/platforms.toml, so its image renders at tiktok.video's size until the platform's own cover size is confirmed. -->
<: endif :><: if 'linkedin' in PLATFORMS :><!-- VERIFY: linkedin has no thumbnail table in toolkit/data/platforms.toml, so its image renders at linkedin.video_vertical's size until the platform's own cover size is confirmed. -->
<: endif :><: if 'facebook' in PLATFORMS :><!-- VERIFY: facebook has no thumbnail table in toolkit/data/platforms.toml, so its image renders at facebook.reel's size until the platform's own cover size is confirmed. -->
<: endif :>
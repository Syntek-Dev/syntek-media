# BUSINESS.md — prepare-post, business mode

The domain for packaging a business's video and audio for posting: the social plan each post
belongs to, the claims a post may make, and the people it may show.

## Paths and unit

- **Unit:** one piece; its package is `publishing/src/posts/<piece>.md`, one section per
  deliverable, every agreed cut included.
- **Procedures:** `publishing/workflows/05-prepare-a-post/` and
  `publishing/workflows/06-record-a-publication/`.
- **The social plan:** syntek-author's social-media family, on by default in a business project.
  Where present, its plan, content calendars and operating procedure (its library layer's
  social-media folder) own what each sets per platform, bios and text-only posts included, and
  often a blog's cadence; read the calendar, and never edit any of them.
- **Profiles:** `brand/src/platforms/<platform>.md`, holding only delivery facts while the social
  plan is present, and all of it otherwise.
- **Written voice:** syntek-author's brand voice, where present (by default
  standards/brand/brand-voice.md; its project settings file, 00-project.md, names the brand
  folder); otherwise the profile's `## Tone on this platform`.
- **Guides:** `publishing/docs/reference/posting-and-the-log.md` and
  `publishing/docs/reference/ai-disclosure.md`.

## Additions to the steps

- **Step 2 — also** a deliverable with no calendar entry is asked about, never scheduled around:
  the author adds the entry through the social-media-documents skill (syntek-author), where
  present, or says the post goes out unplanned, and the schedule row's Notes say which.
- **Step 4 — also** a post that promotes the business is advertising: every objective claim has
  its evidence; a paid partnership, gifted product or affiliate link is labelled as one; a
  testimonial is genuine, attributed and used with the customer's recorded permission. The copy
  follows the brand voice's mechanics, so no em dash goes out where it forbids them.
- **Step 5 — also** a placement on a second site the business writes for, owned by a partner,
  cites the dated agreement in that site's website-profile row (invented: `website:second-site`,
  'partner agreement, approved 02/10/2026'); without one, the placement waits.
- **Step 9 — also** a client named, tagged or shown, and a client's logo, needs its row `cleared`
  for promotional use before the post is `ready`.
- **Step 11 — also** name, in the hand-over, who approves posts, where the social media plan's
  governance names someone other than the author.

## Domain rules

- **The social plan leads; media delivers.** Where syntek-author's social media plan is present,
  a media post fills one of its calendar entries and repeats none of its decisions.
- **Specificity over superlatives.** A result is stated as the checkable detail the author
  supplies, never as 'the best' or 'unbeatable'.
- **Endorsements are real or absent.** No review, rating, client quotation or partnership is
  claimed that the business cannot show, with permission, on the day it posts.
- **Clients appear only by consent.** A client's name, face, premises or logo in a post or its
  description has a `cleared` row that covers social use.

## Examples

An invented section of a Harbour Lane Studio post package:

```markdown
## youtube.long

- **Title:** Price it once: a quote you can defend
- **Description:** the fenced block below.
- **Hashtags:** #smallbusiness #pricing
- **Disclosure:** altered or synthetic content setting off, because the narration is the owner's own cloned voice and the guide's YouTube row exempts that for a voiceover (checked 03/10/2026). Description line: the third line below. Spoken line: none.
- **Captions:** 004-price-it-once.en-GB.srt, sidecar.
- **Thumbnail:** 004-price-it-once.youtube-thumbnail.png
- **Render:** 004-price-it-once.youtube-long.mp4
- **Calendar:** YouTube calendar, November, week 2, the 'Pricing' pillar.
- **Scheduled:** 14/11/2026 09:30, <%TIMEZONE%>
- **Limits:** title 37 against platform.youtube.title_max_chars · description 284 against platform.youtube.description_max_chars · hashtags 2 against platform.youtube.hashtags_ignored_over
```

Its description, one sentence per line:

```text
Most quotes are too low for one reason: they price the hours, not the certainty.
In seven minutes, Harbour Lane Studio shows the one line that fixes it.
The narration uses an AI voice made from the owner's own voice.
Book a pricing review through the link in the channel's about page.
```

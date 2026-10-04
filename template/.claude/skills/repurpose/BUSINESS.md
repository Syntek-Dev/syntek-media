# BUSINESS.md — repurpose, business mode

The domain for cutting down a business's long pieces: explainers, recorded talks and webinars, cut
into short clips that each give one useful thing and one next step.

## Paths and unit

- **Unit:** one piece: a long explainer, a recorded talk or a webinar, in
  `scripts/src/pieces/NNN-kebab-title/`. **Cut:** one moment of it: one tip, one answer or one
  result.
- **Procedure:** `publishing/workflows/01-plan-the-cut-downs/`.
- **Master:** `production/src/renders/<piece>.master.mp4`. **Plan:**
  `publishing/src/cut-downs/<piece>.md`.
- **Profiles:** `brand/src/platforms/<platform>.md`, for the deliverables each platform uses.
  Where syntek-author's social-media family is present (it is on by default in a business
  project), its social media plan owns cadence, tone, the call to action and hashtags, and the
  profile holds only delivery facts.
- **Written voice:** syntek-author's brand voice, where present (by default
  standards/brand/brand-voice.md; its project settings file, 00-project.md, names the brand
  folder). The on-screen title and the hook follow it.
- **Guides:** `publishing/docs/reference/cut-downs.md`; the short-video and long-video guides in
  `scripts/docs/reference/`, where the project makes those kinds.

## Additions to the steps

- **Step 1 — also** read the brief's `## Call to action`: every cut ends on that action, or on a
  shorter form of it the author agrees.
- **Step 3 — also** read the content calendar of syntek-author's social-media family, where
  present, for the video slots it plans, and say which cuts could fill them; scheduling stays with
  `prepare-post`, and the calendar is never edited from here.
- **Step 4 — also** prefer the moment that answers one question a customer actually asks: the
  problem in the opening line, the answer, the next step. A moment that needs the slide before it
  is not a cut. A cut that shows or names a client, or quotes a customer, needs that person's row
  in `production/src/rights-register.md`; name the row in the cut's note.
- **Step 7 — also** list as questions, never as cuts, any moment whose claim the business could
  not evidence on its own: a figure, a result, a comparison with a competitor.

## Domain rules

- **A promotional clip is advertising.** Every objective claim in a cut has its evidence before
  the cut is agreed, checked with the fact-check skill (syntek-author), where present; a claim
  trimmed of its condition ('for most clients', 'in our experience') is a new claim, and is not
  made.
- **One cut, one useful thing.** A tip, an answer or a result, never a montage of the whole talk.
- **Faces and names need consent.** A client, a colleague or a member of an audience shown or
  named has a `likeness` or `quotation` row, `cleared` before the cut is posted.
- **The business's voice is set elsewhere.** This mode never invents a tone for the brand; where
  syntek-author's brand voice is absent, the profile's `## Tone on this platform` is the record,
  and a gap there is a question for the author.

## Examples

An invented plan for an invented Harbour Lane Studio explainer on pricing a job:

```markdown
| Cut | Deliverables | Lines | In | Out | Frame | Hook | Status |
|---|---|---|---|---|---|---|---|
| c01 | youtube.short, instagram.reel | 2.1–2.4 | 00:01:12.400 | 00:01:41.900 | crop x=656 | Your quote is too low if it skips this line. | approved |
| c02 | linkedin.video_vertical | 4.2–4.5 | 00:03:05.120 | 00:03:36.800 | crop x=640 | Clients pay for certainty, not for hours. | planned |

## c01 — Your quote is too low if it skips this line

Opening words: 'Your quote is too low if it skips this line.'
On-screen title: 'The line most quotes forget'.
Caption width: vertical; one caption file serves both deliverables.
Thumbnail: the Short takes the piece's; the reel needs a cover (thumbnail-brief).
Stands alone: one mistake, its fix, and the call to action from the brief.
```

An invented question kept out of the plan:

```text
Line 3.4 says jobs priced this way 'never run over'. Can the business evidence that,
or should the cut stop at 3.3?
```

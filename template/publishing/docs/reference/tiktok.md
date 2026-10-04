---
type: guide
skills: [prepare-post, cut-for-platform]
model: opus
---

# TikTok — vertical video, burned captions and the AI-generated label

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How this project's deliverables meet TikTok: the one deliverable key it reads in
`toolkit/data/platforms.toml`, why its captions are burned in, how its cover is handled, where
TikTok's AI label lives, and what TikTok removes whatever the label. TikTok's help centre gives
few numbers, so more of its table is in `verify` than any other platform's: read it with
`python3 toolkit/media.py presets tiktok.video` before every render. The brand's own handle,
cadence and tone on TikTok live in its profile in `brand/src/platforms/`.

## Deliverables and their keys

| Deliverable | Key | Captions | Cover |
|---|---|---|---|
| A vertical video | `tiktok.video` | burned in: its `caption_formats` is empty (and in `verify`) | no cover table: rendered at the video's size, flagged `VERIFY` |

- The size, the audio codec, the length and the safe zone are all in `verify`: they are the best
  official values found, not confirmed ones.
- `tiktok.video.max_seconds_some_creators` applies only where the author's account has it.

## Words

- The caption is held to `platform.tiktok.caption_max_chars`, the limit the posting API
  documents; the in-app figure, `platform.tiktok.caption_max_chars_app`, is a third-party report
  in `verify`. Write to the documented one.
- The disclosure line goes in the caption, as on every platform.

## Disclosure

TikTok's label is 'AI-generated content', switched on under More options when posting. Its rule,
source and checked date are in `publishing/docs/reference/ai-disclosure.md`: realistic
AI-generated images, audio or video need it. TikTok does not say whether an owner's own cloned
voice counts, so the house treats it as realistic synthetic audio and sets the label (`VERIFY`).
A label TikTok applies itself, from Content Credentials, cannot be removed. The API field that
sets the label, `platform.tiktok.ai_flag_api_field`, matters only to tools that post for you;
this project never does.

## Traps

- **The safe zone is derived, not published.** TikTok publishes overlay files, not numbers, and
  its overlay grows with the caption; the table takes the larger of YouTube's and Meta's margins
  on each edge. Keep titles and captions well inside it.
- **Removed even when labelled:** fake authoritative sources or crisis events, public figures in
  false contexts, and the likeness of a minor or a private adult without permission
  (`production/docs/reference/rights-and-consent.md`).
- **Auto-captions** are TikTok's own and unchecked against the script: the house burns its own.

## How we apply it here

- Read the `notes` of `tiktok.video` before trusting any of its values, and name every `verify`
  key relied on in the hand-back.
- Burn captions in every TikTok deliverable, checked against the script before M6.
- A cover is rendered only where the author wants one, at the video's size, flagged `VERIFY`.

## Who implements it

- **Workflows:** `publishing/workflows/05-prepare-a-post/` writes the TikTok package;
  `publishing/workflows/02-cut-for-a-platform/` renders the deliverable with its captions burned.
- **Skills:** `prepare-post` keeps the caption inside its key and sets out the disclosure;
  `cut-for-platform` renders and verifies the deliverable.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 5 owns disclosure, Section 6 owns
consent for a likeness, and Section 7 owns never fabricating a platform rule or limit. The rules
own the requirement; this guide owns how TikTok's keys and rules are applied here.

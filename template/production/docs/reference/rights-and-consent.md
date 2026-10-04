---
type: guide
skills: [storyboard, prepare-post, voiceover]
model: opus
---

# Rights and consent — cleared before publishing, consented before a likeness or a voice

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** Everything a piece uses that someone else owns, or that shows or sounds like a
real person, needs a permission the author can produce. `production/src/rights-register.md` holds
one row per item, opened when the item is first planned and cleared before the piece is
scheduled. No voice is cloned, and no identifiable person appears, without that person's recorded
consent.

## What needs a row

| Kind | When |
|---|---|
| `music` | any track or bed not made for the brand by the author |
| `stock` | stock footage, stills or sound effects |
| `footage-release` | a recognisable person on camera or on tape |
| `location` | a private place, filmed or recorded |
| `likeness` | a person's image used beyond a release: a thumbnail, a card |
| `voice-consent` | any cloned voice, the owner's own included |
| `quotation` | quoted text, read aloud or shown on screen |
| `scripture` | a Bible translation quoted, read aloud or shown |
| `font` | a brand font, under its licence |
| `artwork` | a cover, an illustration or a logo that is not the brand's |
| `generated` | AI-generated music, images or video, under the service's terms |

## The register

IDs run from `RR0001`, permanent and never reused. Status moves `needed · requested · cleared`, or
ends `refused` or `expired`. Evidence says where the licence, release or consent is filed (the
document itself stays outside the repository when it holds personal data); Expires is DD/MM/YYYY
or `—`. `storyboard` opens a `needed` row for every licensed or identifiable item it plans; the
author requests and records each permission; `prepare-post` will not schedule a piece with a row
that is not `cleared`.

## Consent before a likeness or a voice

- A voice is cloned only with the person's recorded consent, kept as evidence and cited by its
  rights ID in the narrator's row of `brand/src/voice/voice.md`.
- The owner's own cloned voice is still synthetic, and is disclosed like any other.
- A recognisable person in footage signs a release before the footage reaches a master.
- Never make a real person appear to say or do what they did not.

## Quotations and scripture

Quoted text read aloud or shown on screen needs clearing like anything else: whether a short
quotation is fair dealing is the author's call, recorded in Notes, never assumed. A
translation's licence may treat print and audio differently, so check its terms for the use in
hand before reading it aloud, record the translation and any notice it asks for, and say or show
that notice where the licence requires it.

## How we apply it here

- Open the row when the item is planned, not when the piece is about to post.
- Never fabricate a permission, a statistic, a quotation, a testimonial or an endorsement.
- A refusal is final for that piece: cut, replace or re-shoot, and never publish around it.
- Check an expiring permission before every re-post; a piece that outlives it comes down.

## Who implements it

- **Workflow:** `production/workflows/07-clear-the-rights/`.
- **Skills:** `storyboard` opens rows; `voiceover` checks consent before a cloned voice speaks;
  `prepare-post` checks every row is `cleared` before a post is scheduled.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 6 owns rights and consent, and its
Section 7 owns never fabricating. This guide owns how a permission is recorded and cleared.

# BUSINESS.md — write-script, business mode

The domain for scripting a business's pieces: social shorts, explainers and talks in the brand's
spoken voice, each built on one checkable promise and ending on one call to action, to book or to
get in touch.

## Paths and unit

- **Unit:** one piece: a social short, an explainer, or a talk the brand gives to camera.
  **Beat:** one point the viewer can act on, typically one to four spoken lines.
- **Procedure:** `scripts/workflows/02-write-a-script/`.
- **Brief:** `scripts/src/pieces/<piece>/brief.md`. **Script:**
  `scripts/src/pieces/<piece>/script.md`.
- **Spoken voice:** `brand/src/voice/voice.md`. **Written voice:** syntek-author's brand voice,
  standards/brand/brand-voice.md, where present (or the brand folder its project settings name),
  read for word choice and never restated.
- **Platforms:** `brand/src/platforms/` — the call to action and the tone each platform takes;
  where syntek-author's social media plan is present, it owns both and the profile cites it.
- **Facts:** the author, the `Facts` heading of `.claude/MEMORY.md`, and, in a combined project,
  the client facts and disclaimers where syntek-author's project settings put them.
- **Guides:** `scripts/docs/reference/writing-for-the-ear.md`, and the short-video and long-video
  guides beside it where this project makes those kinds.

## Additions to the steps

- **Step 2 — also read the offer and the call to action.** Read the profile of each deliverable's
  platform in `brand/src/platforms/`, syntek-author's brand voice and disclaimers, where present,
  and the brief's `## Call to action`: one action (book, call, get in touch, visit) that names
  what the brand actually offers. A brief with no call to action stops here for the author.
- **Step 3 — also take every business fact from its owner.** Prices, dates, turnarounds,
  guarantees, results, client names and testimonials come only from the author or an agreed
  document, never from the website or from memory. A client named, shown or quoted needs that
  client's permission, listed for a `likeness` or `quotation` rights row. A statistic carries its
  source and date, or `VERIFY`.
- **Step 5 — also open on the viewer's problem, not the company.** The hook names the problem in
  the viewer's own words, in the first beat; the brand name is said as `voice.md` says it, and not
  in the hook unless the brief asks. One promise per piece, made checkable. Speak as 'we' or 'I',
  whichever the spoken style in `voice.md` gives. The last beat is the call to action, spoken once
  and repeated as a `TEXT:` cue.
- **Step 5 — also write for the sound off.** Where the audience test watches without sound, every
  key point has a `TEXT:` cue of a few words, and no line depends on a sound effect to make sense.
- **Step 8 — also read it as a regulator would.** Propose cutting each superlative ('the best',
  'guaranteed', 'instant'), or making it checkable with evidence the author supplies. A disclaimer
  is quoted verbatim from syntek-author's disclaimers file, where present, never paraphrased. No em
  dash in on-screen text, as in all client copy.
- **Step 10 — also list the commitments.** Name every commitment the script makes aloud (a price,
  a turnaround, a guarantee, a free offer) by its line, each traced to the brief or marked new, for
  the author to confirm.

## Domain rules

- **Never fabricate a statistic, quotation, testimonial or endorsement**
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 7): a result the brand cannot
  evidence is not said.
- **Consent before a client, a customer or a member of staff is named, quoted or shown**
  (Section 6).
- **One promise and one call to action per piece**, both from the brief; a second offer is a
  second piece.
- **Specificity over superlatives**: a claim the viewer cannot check is cut, or made checkable by
  the author.
- **The spoken voice is `brand/src/voice/voice.md`**; the written brand voice stays
  syntek-author's, where present, and is never restated in a script.

## Examples

An invented explainer for Harbour Lane Studio, its gaps left visible:

```markdown
## 1. Hook (target 00:04)

ON: Your site gets visitors, but nobody books.
TEXT: Visitors, but no bookings?

## 2. The form asks too much (target 00:14)

ON: {steady} Most booking forms ask for too much before they ask for a date. <!-- VERIFY: a source for this claim, or cut it -->
TEXT: Ask for the date first

## 3. Call to action (target 00:08)

ON: If that sounds like your form, book a free review with us.
ON: We reply to every request within one working day.
TEXT: Book a free review: link below <!-- AUTHOR TO CONFIRM: is the review free, and until when? -->
```

An invented commitments list from the hand-back:

```text
Commitments said aloud (for the author to confirm):
- 'a free review' · 3.1 · not in the brief: new
- 'within one working day' · 3.2 · the brief, Call to action
```

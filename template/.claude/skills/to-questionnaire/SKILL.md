---
name: to-questionnaire
description: >-
  Turn a decision the author cannot settle alone into a questionnaire for someone else to fill
  in: a subject expert, a beta or specialist reader, a collaborator, an adviser or a supplier.
  Settles the send in one grilling round (who receives it, what must come back, by when), writes
  the questionnaire into the project's questionnaires folder, and records what stays blocked
  until it returns; when the answers come back, they resolve the decision by its normal route.
  Invoke by typing /to-questionnaire, or, with the author's agreement, when a grilling pass or a
  decision-map node stalls because the answer lives with a person who is not in the session: a
  stall may propose it, never run it unasked. Never sends anything. Not for a hard question the author can answer
  (`grill-with-docs`), not for a fresh session taking over the work (`handoff`), and never for an
  empirical fact (the project's research or fact-checking skill).
---

# Skill: To-questionnaire

Grilling assumes the author can answer. Sometimes they cannot, because the knowledge sits with
someone else: the specialist who knows how the period worked, the reader who can say where the
draft lost them, the adviser who knows which treatment applies. This skill turns that blocked
decision into a document that person can fill in without anyone from the session present.

**It is the way out of a stalled grilling pass, not a replacement for one.** Reach for it when the
blocker is *who holds the answer*, never when the question is merely hard.

**Paths.** This file names folders and files by their role ('the questionnaires folder', 'the
voice guide'). The project's rules in `.claude/rules/` give each role its path, and the mode files
add their own.

Locale: en_GB · dates DD/MM/YYYY.

## Governing procedures (route here — do not restate at length)

- `.claude/skills/grilling/SKILL.md` — the round shape step 1 uses.
- The project's global rules — confidentiality: a questionnaire leaves the project, so it carries
  nothing the recipient may not see.
- The project's memory rules — the `Open questions` heading that records the block while the
  questionnaire is out.
- The planning procedure and the decision-map guide — where the blocked decision usually sits,
  and where its answer lands.

The mode files add who this kind of project asks, and which recipients belong to another skill.

## The governing rule: grill the send, not the subject

Do **not** interview the author about the subject: that is exactly what they cannot answer, and
it is why this skill was invoked. Interview them about the **send**, which they can always answer:
who receives it, and what they need back. The questions in the document then aim at the gap
between what the recipient knows and what the author needs. Getting this backwards produces a
questionnaire full of the author's guesses with blanks around them.

## Steps

> **Mode.** Before step 1, read the mode files beside this one (the upper-case `.md` files in this folder) that the project's rules route the work at hand to; where they name none, read every one. A mode file owns the domain (paths, the unit of work, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the owner.

1. **Check the boundaries, then settle the send.** First test the request against Boundaries,
   below, and the mode files' own: a recipient or a subject another skill owns goes there
   instead, and the author is told which and why. Then one grilling round, covering only: **who
   receives it** (their role, what they know that the author does not, the relationship), which
   fixes the register and how much context the document must carry; **what must come back** (the
   specific decisions or facts blocked on them); **the deadline**, and whether it is filled in
   alone or worked through together; and **what the recipient may see**. *Complete when:* no
   boundary applies, the recipient is known, and the return list is concrete, each item something
   the author will be able to decide once it is answered.
2. **Write the questionnaire.** Into the questionnaires folder, named
   `QUESTIONNAIRE-<SLUG>-DD-MM-YYYY.md` unless the project's rules give another form, in the
   document shape below. **Most important first:** answered alone, it may get one pass and no
   follow-up. **One idea per question:** a compound question gets a compound answer that resolves
   neither half. **Each question carries its context, its options and the recommended answer**
   where it is a decision, so the recipient corrects a position rather than starting from a blank;
   a question about the recipient's own experience (a reader's) carries neither, because a
   recommended answer would lead it. **An answer stub under every question**, so the recipient
   types into a shape, not a blank. **Group under `##` headings by theme** once there are more than a handful. **A *why
   this matters* line only where a question could be misread** or would invite a throwaway answer.
   **Never ask what the repository can answer:** look it up and state it as context, so the
   recipient corrects it rather than researches it. *Complete when:* the file exists in the shape
   below, every question is one idea with a stub, and nothing the repository answers is asked.
3. **Read it as the recipient.** Check the register against the table below and the mode files,
   and the voice against the project's voice guide, where its rules name one. Strip internal
   shorthand, file paths, flags and anything confidential: name what the recipient needs, never
   paste a draft they are not meant to see. *Complete when:* a stranger to the project could answer every question, and
   nothing in it is confidential to them.
4. **Hand it back, and record the block.** Give the author the path, what stays blocked until it
   returns, and the date it is due. Record the block under the `Open questions` heading of
   `.claude/MEMORY.md` (under the name the project's rules map it to), naming the questionnaire's
   path and what it blocks; where it gates a decision-map node, mark the node as handed off to
   that path. The questionnaire is the evidence, not the record. **The author sends it;** set its
   `Status` line to `sent` with the date only on their word. *Complete when:* the path is given,
   the block is recorded where the next session will meet it, and nothing has been sent by the
   session.
5. **When the answers come back, resolve the decision by its normal route.** Save the returned
   copy beside the original as `…-RETURNED.md`, never editing the recipient's words, and set the
   original's `Status` to `returned` with the date. Then resume the grilling pass through
   `grill-with-docs` (each usable answer opens the round as a `Settled` line citing the returned
   file), settle the map node, or write the artefact; supersede the `Open questions` entry. A
   checkable claim in an answer goes to the project's fact-checking skill before anything relies
   on it. *Complete when:* every returned answer is either recorded in its home through
   `grill-with-docs`, sent for checking, or named as still open, and the block is cleared or
   restated.

## Register

| Recipient | Register |
|---|---|
| A subject expert or specialist reader | Precise; their field's own terms are fair game; say what the work is and who reads it, in two lines |
| A general or beta reader | Plain; no project vocabulary, no craft terms; ask about their experience, never for a verdict on a choice |
| A collaborator, adviser, client or supplier | The project's house voice, plain; the formality their relationship to the author sets |

The mode files add the recipients this kind of project has.

## Document shape

```text
# <Title: the decision it unblocks>

**Purpose:** why this exists and what is riding on it.
**From:** <the author> · **To:** <recipient> · **By:** <DD/MM/YYYY>
**Status:** draft · sent DD/MM/YYYY · returned DD/MM/YYYY
**How your answers are used:** <where they land, and who will see them>

## Context
One short paragraph for a reader who was not in the room. Enough to answer well, not a briefing.

## How to answer
Rough effort, and the deadline. Partial answers and 'I don't know' are useful: flag uncertainty
rather than skipping the question.

## <Theme>
### <One question, one idea>
<its context, in a line or two>
*Why this matters: <only where it could be misread>.*

1. <option> — <one line>
2. <option> — <one line>

**Recommended:** <option, and the reason in one line>

> <answer stub>

## Anything else?
What did we fail to ask that you would expect us to need?
```

## Boundaries

- **This is not a handoff.** `handoff` addresses a fresh session with the whole repository; a
  questionnaire addresses a person with none of it.
- **An empirical fact is not a question for a person.** What a source says, when something
  happened, what a figure is: the project's research or fact-checking skill. An expert's view
  may inform a decision; it never stands in for a cited source.
- **A register of record is not a questionnaire.** A permission, an approval or a signed term is
  recorded where the project's rules say; a questionnaire may gather what fills one, and never
  replaces it.
- **Approaching someone for a yes is not a questionnaire.** An endorsement, a submission or an
  offer goes to the skill the mode files name.
- **A review of sensitive material is not a questionnaire.** Whether to engage a sensitivity
  reader, and what they review, belongs to the skill the mode files name.

## Anti-patterns

- **Grilling the subject.** The author cannot answer it; that is why the skill was invoked.
- **The author's guesses with blanks around them.** Ask for what the recipient knows.
- **A questionnaire for a hard question the author could settle.** That is a grilling round.
- **Sending it, or marking it sent, without the author's word.**
- **Pasting confidential material** for a recipient who may not see it.
- **Letting the answers sit.** A returned questionnaire nobody resolved is a decision still open.

## Cross-references

- `.claude/skills/grilling/SKILL.md` — the round shape used in step 1.
- `.claude/skills/grill-with-docs/SKILL.md` — where the returned answers are recorded.
- `.claude/skills/wayfinder/SKILL.md` — hands task nodes here when only someone else can supply
  them.
- `.claude/skills/handoff/SKILL.md` — the other kind of hand-over, to a fresh session.
- The project's rules in `.claude/rules/` — the questionnaires folder, the voice guide, the memory
  headings and the confidentiality rule, by path.

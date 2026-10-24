---
name: wait-what
description: >-
  Re-pitch the last reply that did not land: lead with the conclusion, then the context it
  assumed, in plain sentences and the project's own words, without simplifying the substance.
  Where the miss was a gap in knowledge rather than a dense delivery, offer once, briefly, to
  open a lesson on it. Invoke by typing /wait-what, or when the author says 'wait, what?', 'I
  didn't follow that', 'say that again more simply', 'what does that mean?' or 'you lost me'.
  Never invoked by the model on its own. Not for learning a skill over several sessions (the
  project's teaching skill, where it has one), and not for sharpening an undecided design
  (`grilling`).
---

# Skill: Wait-what

The previous reply failed. Not the work behind it: the **explanation**. Re-pitch it.

Locale: en_GB · dates DD/MM/YYYY.

## Governing procedures (route here — do not restate at length)

**None.** This is a conversational mechanic, not a step in any workflow; it gates nothing, and
the one artefact it can lead to is written by `handoff`, not here. It is the counterpart of the
grilling rule that a vague answer is restated precisely: here the author is telling the model
that its answer was the vague one. The project's own words, which a re-pitch must use, are in
the terminology file the project's rules in `.claude/rules/` name.

## What went wrong (assume one of these)

- **Missing context.** The reply began three steps in, from a premise never stated.
- **Unshared vocabulary.** It used a term this project has not defined, or a defined term
  loosely.
- **Too dense.** Correct, and unreadable.
- **Buried answer.** The reasoning arrived before the conclusion.

## Steps

> **Mode.** Before step 1, read the mode files beside this one (the upper-case `.md` files in this folder) that the project's rules route the work at hand to; where they name none, read every one. A mode file owns the domain (paths, the unit of work, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the owner.

1. **Lead with the conclusion.** One sentence the author could repeat to someone else.
   *Complete when:* the re-pitch opens with that sentence.
2. **Give the context it assumed.** What was already true before this started, and why it
   matters, before any detail. *Complete when:* nothing in the re-pitch rests on a premise it
   does not state.
3. **Write simple, direct sentences in the project's own words.** One idea each, active voice,
   short words over precise but obscure ones; a long word that is load-bearing stays and is
   defined inline, once. Use the terms in the project's terminology file and the names the
   project's files use; a synonym invented on the spot is what caused the miss. *Complete when:*
   every term is either the project's own or defined where it first appears.
4. **Keep the substance whole.** The claim, the trade-off and the caveats survive intact; only
   the delivery changes. Name the step most likely to have missed, and expand that one hardest.
   *Complete when:* nothing the original reply asserted has been dropped or softened, and the
   likely gap is named.
5. **Offer a lesson only for a knowledge gap, after the re-pitch.** Too dense and buried answer
   are delivery failures: the re-pitch is the whole fix, and the turn ends. Missing context and
   unshared vocabulary are knowledge gaps: after the re-pitch, in two lines at most, name the
   topic as a kebab-case slug (the topic folder the project's teaching skill would use in its
   learning workspace, both named in the project's rules), say whether that folder already exists
   (resume it) or not (the first lesson creates it), name the opening lesson (the concept that
   just missed), and offer the route: a teaching-detour handoff, then a new session that runs the
   teaching skill. Where the project has no teaching skill, name the gap and stop there. Ask once
   per topic per session; if declined, drop it.
   *Complete when:* the turn ends after the re-pitch, or after one short offer for a knowledge
   gap.

## Rules

- **Do not repeat the original wording.** If it had landed, this skill would not have been
  invoked; saying it louder is the failure.
- **Do not apologise, and do not narrate the correction.** Re-pitch and move on.
- **Stay scannable.** A re-pitch is licence to spend the words differently, not to write an
  essay.
- **The teaching-detour handoff is `handoff`'s to write**, in full, with the descriptor
  `HANDOFF-TEACH-<TOPIC>-DD-MM-YYYY.md`, a `Teaching detour` line (the topic, the concept that
  missed, the opening lesson) and the teaching skill first among the next skills.

## Anti-patterns

- **Simplifying the substance** to make it land. An explanation that lands by being wrong is
  worse than one that missed.
- **Offering a lesson before the re-pitch**, or more than once. It reads as a deflection.
- **Inventing a new term** to explain an old one.

## Cross-references

- `.claude/skills/grilling/SKILL.md` — the same problem in the other direction.
- The project's teaching skill, where it has one — where a knowledge gap is closed for good.
- `.claude/skills/handoff/SKILL.md` — the session boundary a teaching detour crosses.
- The project's rules in `.claude/rules/` — the terminology file, the teaching skill and its
  learning workspace, by path.

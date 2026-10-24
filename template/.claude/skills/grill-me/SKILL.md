---
name: grill-me
description: >-
  Grill an idea and write nothing down: the grilling interview, in frontier rounds with a
  recommended answer on every question, that sharpens a half-formed plan, argument, plot turn,
  name, offer or piece of work and leaves no trace in the repository. Invoke by typing /grill-me,
  or when the author says 'grill me on this', 'poke holes in it', 'talk me through whether this
  works' or 'don't record this'. If an answer turns out to be load-bearing, it says so and offers
  to switch. Not for decisions that must outlive the session (`grill-with-docs`), and not for work
  too big for one sitting (`wayfinder`).
---

# Skill: Grill-me

Run a grilling session and save nothing. `.claude/skills/grilling/SKILL.md` is the engine and its
mode files are the domain: **they own the round shape, the question format, the recommendation
rule and the surfaces; this file does not restate them.** Grill until the idea is settled and the
author confirms shared understanding.

Use this when the interview itself is the point and there is no artefact to update yet. Typical
openings:

- testing whether an argument, a plot turn, an offer or a plan actually holds before it is
  committed to a brief;
- working out, out loud, what the work really wants to say about something;
- thinking through what a name or a word should sound like before anything is coined
  (grilling's mode files set which question opens such a round);
- rehearsing a difficult reply, or a position the author is drawn to, before it hardens.

Locale: en_GB · dates DD/MM/YYYY.

## Governing procedures (route here — do not restate at length)

**No governing workflow.** A `grill-me` session sits before any procedure, and records nothing for
one to pick up. The engine's own procedures are listed in `.claude/skills/grilling/SKILL.md`; the
rule it serves is in the project's global rules in `.claude/rules/` (design work opens with
grilling).

## Steps

> **Mode.** Before step 1, read the mode files beside this one (the upper-case `.md` files in this folder) that the project's rules route the work at hand to; where they name none, read every one. A mode file owns the domain (paths, the unit of work, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the owner.

1. **Load the engine and its modes.** Read `.claude/skills/grilling/SKILL.md` and, under its Mode
   paragraph, the mode files beside it that the project's rules route the work to, then run its
   step 1 against the record. *Complete when:* the engine's step 1 is done and the first round
   is ready to send.
2. **Grill in frontier rounds, recording nothing.** Follow the engine exactly. Write no file,
   edit no brief, touch no `.claude/MEMORY.md` entry. *Complete when:* the frontier is empty and
   the author has said yes to the summary.
3. **Name any decision with no home.** Because nothing is recorded, a session that settles
   something load-bearing (an interpretation the work adopts, a scope boundary, a model the work
   borrows from, a price) has produced a decision nobody will find next month. If that happened,
   say so at the end and offer to re-run that part under `grill-with-docs`, or to record it
   directly through that skill's gate. *Complete when:* every load-bearing answer is either named
   with the offer made, or there was none and the session says so.

## Anti-patterns

- **Writing anything down.** That is `grill-with-docs`; switch openly rather than half-recording.
- **Restating the engine** here or in the conversation instead of following it.
- **Letting a load-bearing decision evaporate.** A conclusion nobody recorded is argued again.
- **Settling a fact by asking.** Empirical questions go to the project's fact-checking or research
  skill, exactly as the engine says.

## Cross-references

- `.claude/skills/grilling/SKILL.md` — the engine this runs, and its mode files.
- `.claude/skills/grill-with-docs/SKILL.md` — the stateful twin that records each decision.
- `.claude/skills/wayfinder/SKILL.md` — for work too big to settle in one sitting.

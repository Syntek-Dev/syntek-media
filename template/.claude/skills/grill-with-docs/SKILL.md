---
name: grill-with-docs
description: >-
  Grill a design and record what it settles: the grilling interview, in frontier rounds with a
  recommended answer on every question, writing each decision into its existing home the moment
  it resolves (the brief, the plan files the mode files name, the terminology file, and
  `.claude/MEMORY.md` through the decision gate). The design-work default: the opening move for
  planning a piece of the work, settling an argument, a plot turn, a world element, a name, a
  document's scope or a plan. Invoke by typing /grill-with-docs, or when the author says 'let's
  plan the next part', 'settle the scope of this proposal', 'decide what this name should sound
  like', 'work out the ending and write it down'. Not for a conversation that must
  leave no trace (`grill-me`), not for work too big for one sitting (`wayfinder`), not for a
  decision only someone else can answer (`to-questionnaire`), and never for an empirical
  question (the project's fact-checking skill).
---

# Skill: Grill-with-docs

Run a grilling session that leaves a paper trail. `.claude/skills/grilling/SKILL.md` is the engine
and its mode files are the domain: **they own the round shape, the question format, the
recommendation rule and the surfaces; this file owns only where each answer is written.** As each
decision resolves, record it in the right **existing** artefact. Never invent a new format, and
never a new file where a section of an existing one will do.

This file also keeps the **decision gate** that `.claude/MEMORY.md` points to. Memory headings are
named here as the template names them (`Decisions`, `Facts`, `Open questions`); the project's
rules map each to the project's own heading.

**Paths.** This file names folders, files and procedures by their role ('the brief', 'the
terminology file', 'the planning procedure'). The project's rules in `.claude/rules/` give each
role its path, and the mode files add their own. 'A piece of the work' is whatever one brief
covers; the mode files name it.

Locale: en_GB · dates DD/MM/YYYY.

## Governing procedures (route here — do not restate at length)

Follow the procedure's `STEPS.md` against its `CHECKLIST.md`; this skill is its questioning and
recording in skill form.

- The planning procedure — the questioning, the brief and its first gate, and the recording.
- The whole-work review procedure — the author decides; this records it.
- The project's memory rules — where a decision lives, the memory gate, and the entry form.
- The project's global rules — never self-edit; design opens with grilling; internal notes for
  deliberate deviations.
- The brief guide — the brief's frontmatter and body slots.

The mode files add their own procedures and records.

## Where each decision goes

| When a decision… | Record it in |
|---|---|
| settles a piece's scope, its job, its parts or what it draws on | its brief, in the slot the brief guide gives each |
| commits the piece to a position | the brief's settled-positions slot (the mode names it) |
| is a note for whoever drafts the piece, or a change the author declined and why | the brief's draft-notes slot |
| changes the shape or the order of the whole work | the outline |
| is project-wide and passes the decision gate below | `.claude/MEMORY.md`, the `Decisions` heading, dated |
| is a fact a later session needs and cannot read off the files | `.claude/MEMORY.md`, the `Facts` heading |
| is still open, and only the author can settle it | `.claude/MEMORY.md`, the `Open questions` heading, naming what it blocks |
| is still open, and only someone outside the session can settle it | the same heading, with a questionnaire through `to-questionnaire` |
| pins a term: one canonical word per concept | the terminology file, rejected synonyms under **Avoid** |
| authorises a departure from a standard in one artefact | that artefact's internal note |
| sets a rule for one folder, on the author's explicit word | that folder's `CLAUDE.md` |
| changes a standard | the standard, **author-confirmed first, always**, then noted in `MEMORY.md` |

The mode files add the rows for this kind of project. A decision settled on a decision map lands
in its home here, and the map's `Resolved decisions` entry links to it.

## The decision gate

A decision enters the `Decisions` heading of `.claude/MEMORY.md` **only when all three hold
together**: it is **hard to reverse**, it would be **surprising without its context**, and it
settled a **genuine trade-off**. It must also pass the memory gate (needed again, not readable off
the files, costly if wrong: the project's memory rules). That keeps the log signal-dense enough to
be read. A decision that fails the gate is still written down, in the narrower home the table
gives it; say which.

## Steps

> **Mode.** Before step 1, read the mode files beside this one (the upper-case `.md` files in this folder) that the project's rules route the work at hand to; where they name none, read every one. A mode file owns the domain (paths, the unit of work, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the owner.

1. **Load the engine, and read the homes.** Read `.claude/skills/grilling/SKILL.md` and its mode
   files, run its step 1, and read every home in the tables above that this subject touches, so a
   decision already recorded opens the round as a `Settled` line. *Complete when:* the engine's
   step 1 is done and every relevant home has been read.
2. **Grill in frontier rounds.** Follow the engine exactly; this skill changes nothing about the
   rounds. *Complete when:* each round has gone out in the engine's format and its answers are
   restated and confirmed.
3. **Record each decision the moment it resolves.** Write it inline, in its home, before the next
   round, not batched at the end: a session that stops early should still have left every settled
   decision where it belongs. Write only what the author has confirmed; an inferred
   conclusion written down is worse than none, because later sessions treat it as settled.
   *Complete when:* every confirmed decision sits in its home, and nothing unconfirmed was written.
4. **Gate anything bound for `MEMORY.md`.** Apply the decision gate and the memory gate; write a
   passing entry in the house form (`- **DD/MM/YYYY** — **Headline.** Body, including why and
   what was rejected.`), superseding rather than deleting an older one. *Complete when:* every
   `MEMORY.md` entry passed both gates, and every decision that failed went to its narrower home.
5. **Close with the summary and the record.** Summarise the settled design, get the explicit yes,
   then list each file written and the decision it now holds; anything left open is under the
   `Open questions` heading. *Complete when:* the yes is given, the list is reported, and nothing open is
   held only in the conversation.
6. **Agree the brief (a piece being planned).** When the subject is a piece of the work, write or
   complete its brief exactly as the planning procedure's brief step sets out, in the brief
   guide's shape. Read it back to the author and apply the corrections. Only on the author's agreement
   has the procedure's first gate passed: record it, dated, as that step says. Any other subject
   skips this step. *Complete when:* the author has agreed the brief and its first gate is
   dated, or the subject is not a piece of the work.

## Guardrails

- **Never record a decision the author has not confirmed.**
- **Never settle an empirical question by grilling.** Route it to the project's fact-checking or
  research skill and record what comes back, with its verdict.
- **A standards change is author-confirmed, always**, and so is any change to a folder `CLAUDE.md`
  (the project's global rules: never self-edit).
- **The internal note is load-bearing.** A deviation the author authorises is recorded in the
  artefact itself as well as its wider home, naming the rule, the reason and the date, so a later
  pass does not 'correct' it back.
- **Record a declined proposal where the next session will meet it**, so the same suggestion is
  not made again next month.

## Anti-patterns

- **Batching the record at the end.** The session that collapses before the summary loses it all.
- **A new file for one decision** when a section of an existing artefact is its home.
- **Writing everything to `MEMORY.md`.** A log that records every choice is a log nobody reads.
- **Restating the engine's round shape** instead of following it.

## Cross-references

- `.claude/skills/grilling/SKILL.md` — the engine this runs, and its mode files.
- `.claude/skills/grill-me/SKILL.md` — the stateless twin that records nothing.
- `.claude/skills/wayfinder/SKILL.md` — sends map nodes here, and links to where they land.
- `.claude/MEMORY.md` — the log the decision gate protects.
- `.claude/skills/to-questionnaire/SKILL.md` — when the answer sits with someone else.
- The project's rules in `.claude/rules/` — the path of every role this file names, the
  terminology file (the home of every pinned term) among them.

---
name: grilling
description: >-
  The grilling engine: a relentless Socratic interview, asked in frontier rounds as chat prose
  with a recommended answer on every question, that sharpens a brief, an argument, a plot turn, a
  world element, a name, a document or a plan before any of it is made. `grill-me` and
  `grill-with-docs` load it, and `wayfinder` sends it batches of decision nodes; load it directly
  when the author asks to be interviewed, challenged or stress-tested ('pressure-test the ending',
  'what have I not decided about this proposal?'). Not for recording what is settled
  (`grill-with-docs`), not for a conversation that must leave no trace (`grill-me`), not for a
  decision only someone else can answer (`to-questionnaire`), and never for settling a fact (the
  project's fact-checking or research skill).
---

# Skill: Grilling

Grilling is how this project interrogates a design **before** making it. It replaces the usual
posture (make a reasonable call and carry on) with *interrogate first*: the model interviews the
author until the brief, the argument, the plot, the document or the plan is sharp enough to make
without further clarification. For design work it is the opening move, not an optional extra.

This skill is the shared **engine**, and it owns the interview's shape. Two entry points wrap it:
`grill-me` (stateless: interview only, record nothing) and `grill-with-docs` (stateful: record
each decision the moment it resolves). `wayfinder` sends it batches of related decision nodes
from a map, and `to-questionnaire` uses one round of it when the answer sits with someone else.

> **Everything else routes here and never restates the shape.** A workflow or skill that opens a
> grilling pass names its **subject matter** and leaves the round mechanics, the question format
> and the recommendation rule to this file; a restatement drifts the moment this file changes.

**Paths.** Folders, files and procedures are named by role; the project's rules in
`.claude/rules/` give each its path; the mode files add their own, and name what one brief covers.

Locale: en_GB · dates DD/MM/YYYY.

## Governing procedures (route here — do not restate at length)

Grilling runs inside these procedures: follow the procedure's `STEPS.md` against its
`CHECKLIST.md`, and this file for the shape of every round. The mode files add their own.

- The planning procedure — from an outline row to an agreed brief.
- The whole-work review procedure — a review's open decisions.
- The project's global rules — design work opens with grilling.
- The project's authorship rules — the author decides; the AI recommends.
- The method standard — evidence before the work; flag, never fabricate.
- The brief and decision-map guides — what a brief settles; when the work needs a map.

## How to grill

A session runs the **same process every time**: that predictability is the point, not the same
output, and every rule below serves it.

> **Mode.** Before step 1, read the mode files beside this one (the upper-case `.md` files in this folder) that the project's rules route the work at hand to; where they name none, read every one. A mode file owns the domain (paths, the unit of work, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the owner.

### 1. Read the record, then map the decision tree

Decisions hang off other decisions. Before asking anything, read what is already written down, in
the mode file's lookup order: `.claude/MEMORY.md` (the `Decisions`, `Open questions`, `Feedback`
and `Sensitivities` headings, under the names the project's rules map them to), the brief or
artefact being grilled, and the files the mode names. Then sort every question the subject raises
into three piles:

- **Settled** — a record already answers it (see *A decision already recorded is a fact*, below).
- **Frontier** — unblocked: everything it rests on is settled.
- **Blocked** — waiting on an answer not yet heard, or on a fact not yet looked up.

An **empirical** question (is this true, when did it happen, what does the source say) is in none
of the piles: it goes to the project's fact-checking skill for a claim or its research skill for
a question, and the decisions that depend on it stay blocked until the answer is back. A question
only someone outside the session can answer is blocked on that person: `to-questionnaire` turns
it into a document they can fill in. The mode file lists this project's surfaces and the
decisions each turns on: draw the questions from the surface the work touches. Some surfaces have
one question that gates all the others; where the mode file names one, it opens the first round
alone.

*Complete when:* every question is settled, frontier or blocked; every empirical question is with
the fact-checking or research skill; and the frontier is known before anything is asked.

### 2. Ask the whole frontier in one round

Put the `Settled` lines and the entire frontier in a single message, numbered, in the exact format
below. Then **stop and wait.** Two failures to avoid:

- **Trickling** — one question per message. A ten-decision design becomes ten exchanges.
- **Front-loading** — a question still blocked by another in the same round. Its answer would be
  a guess. Hold it for the next round.

Never block a round on a lookup in flight: it holds back only the questions it may answer.

*Complete when:* one message carries the `Settled` lines and every unblocked question, each with
options and a recommendation, and the turn has ended.

### 3. Let the answers redraw the tree

Each answer settles decisions and unblocks others. Restate any vague answer precisely and confirm
it before building on it; an answer that contradicts a record is put back with both cited. Then
recompute the frontier and ask the next round.

*Complete when:* every answer is restated as a decision the author recognises, and the next
frontier is drawn from what is now settled.

### 4. Stop when the frontier is empty, then confirm

Every branch visited, nothing silently assumed. Summarise the settled design in a few lines and
get an explicit 'yes' before any downstream work (a brief, a draft, a map, a document). **Never
act on a design the author has not confirmed.** Then hand back to the entry point: `grill-me`
records nothing; `grill-with-docs` has already recorded each decision in its home. Loaded
directly, with no entry point: behave as `grill-me` — record nothing, and name any decision with
no home, offering to re-run that part under `grill-with-docs`.

*Complete when:* the author has said yes to the summary, nothing downstream started before that
yes, and, loaded directly, every load-bearing decision has been named.

## Question format — exact

Ask in the chat as prose. **Never the `AskUserQuestion` tool:** it is denied in
`.claude/settings.json`, because a multiple-choice widget makes the interview stilted, and
grilling depends on the author answering, countering or redirecting freely.

```text
**Settled — <title>:** <answer> (<path:line>, or 'this conversation')

**Q1 — <question title>**

<one line of context, only if the title is not self-explanatory>

1. **<Option title>** — <explanation, one line>
2. **<Option title>** — <explanation, one line>
3. **<Option title>** — <explanation, one line>

**Recommendation: 2** — <the reason, one line>
```

- **Options are brief.** One line each. An option that needs a paragraph is two options.
- **Two to four options.** One is not a question; five means the question is unscoped.
- **Always recommend, always justify.** Name the option and the reason in one line. Grilling is
  collaborative decision-making, not a blank-page interrogation.
- **Open-ended is allowed** where options would be invented: drop the list, keep the title and
  the recommendation.
- The author answers by number, or overrides freely. Both are normal.

## Facts you look up; decisions you ask

If the repository can answer it, **find it yourself**; never ask the author for it. Do not ask
'is there a brief for this yet?': look in the briefs folder. **Do** ask 'should this re-argue the
point or lean on the one before it?': that is a decision with a real trade-off.

### A decision already recorded is a fact

Most questions a procedure lists were settled upstream, and the answer is written down: in
`.claude/MEMORY.md`, in the brief, in the plan files, in an earlier `grill-with-docs` pass, or
earlier in this conversation. Reading those is part of step 1, so every question one of them
answers leaves the frontier before the round is drawn.

- **Show what was pre-answered, then ask the residue.** One `Settled` line per pre-answered
  question, citing where it is recorded, so a wrong reading is corrected in one reply.
- **A recorded decision is reopened only on contrary evidence.** When the work has moved (a
  passage now contradicts it, a source has changed), ask, citing both the record and the evidence.
  Never re-ask a settled question merely because a procedure lists it.
- **An empty residue is a normal outcome.** Say that nothing is left to ask and confirm the
  settled design, rather than inventing a question to have one.

**A floor is not the process.** Where a standard names questions every piece of its kind must
answer (the mode file says which), grilling settles those the record cannot, then keeps going
into the decisions that actually shape the work.

## Anti-patterns

- **Trickling and front-loading** — the two round failures in step 2.
- **Asking what the repository already answers**, including a decision a record already holds.
- **Settling an empirical question by asking.** A figure, a date or a quotation half-remembered by
  either party is worth nothing to the work; route it to the fact-checking or research skill.
- **Accepting a vague answer.** Restate it precisely and confirm before moving on.
- **Sycophancy.** Never soften a recommendation because the author leaned the other way; phrase
  questions neutrally, give an honest best answer, then record the author's decision.
- **Grilling trivia.** Escalate decisions with real consequence; make reasonable calls on minor
  details and say so as you go.
- **Essay-length options.** The format is a scan, not a briefing.
- **Auditing a definition by re-reading its wording.** Count its real uses first; a term that fits
  none of them is wrong however well it reads.
- **Acting before the yes**, or reaching for `AskUserQuestion`.

## Cross-references

- `.claude/skills/grill-me/SKILL.md` · `.claude/skills/grill-with-docs/SKILL.md` — the entry
  points.
- `.claude/skills/wayfinder/SKILL.md` — sends batches of related map nodes here.
- `.claude/skills/to-questionnaire/SKILL.md` — when the answer sits with someone else.
- The project's rules — the fact-checking and research skills, and the memory rules.
- `.claude/settings.json` — the `AskUserQuestion` deny that keeps questions in chat prose.

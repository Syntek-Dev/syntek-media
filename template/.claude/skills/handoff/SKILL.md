---
name: handoff
description: >-
  Write a handoff so a fresh session resumes the work cleanly, then stop: the goal, what landed,
  what is in flight with path:line anchors, the part this kind of project must never drop, the
  next action, the skills to load, and every artefact by path. This project's replacement for
  compaction: the seed settings turn auto-compaction off, the context-threshold hook warns as
  the window fills and the PreCompact hook blocks compaction. Invoke by typing /handoff, when
  either hook fires, or when the author says 'hand this off', 'we'll pick this up tomorrow',
  'wrap up the session' or 'write a handoff'. Not a memory store: durable decisions are recorded first
  (`grill-with-docs`), and work that spans many sessions by design belongs on a decision map
  (`wayfinder`).
---

# Skill: Handoff

Handoff **compacts the current conversation by hand** into one document, so a **fresh session**
can resume the work across a boundary: a context window filling, a day ending, other work taking
over. It carries the live thread of *this* session only: where the work sits, what is half-done
and the next move. A handoff is a transient bridge, not a memory store; durable knowledge has
other homes and goes to them first.

**Paths.** This file names folders and files by their role ('the brief', 'the evidence folder').
The project's rules in `.claude/rules/` give each role its path, and the mode files add their own.

Locale: en_GB · dates DD/MM/YYYY.

## Governing procedures (route here — do not restate at length)

**No governing workflow.** This skill is a session mechanic, invoked directly, not a step in any
layer's procedures. The rule it carries out:

- The project's session-boundaries rule — hand off, never compact: the rule, how it is
  enforced, and what a handoff is not.
- The project's global rules — confidentiality: a handoff is committed, so nothing confidential
  is pasted into it.
- The project's memory rules — where durable knowledge goes instead.

## Hand off; never compact

Compaction summarises lossily, without knowing which details were load-bearing; in a project
like this the detail it drops is usually the one that matters (an interpretation the author chose
an hour ago, a line they rejected and why, which of two drafts is live). **This is enforced, not
merely encouraged.** The seed `.claude/settings.json` sets `autoCompactEnabled` and
`idleCompaction` to false, so the harness never compacts on its own, neither as the window fills
nor while the session sits idle. A copy over a project's own `settings.json`, or an update, adds
each as false where the key is absent and reports any other value it leaves alone. Two hooks,
registered in the same file, back it up:

- `.claude/hooks/context-threshold-handoff.sh` (`UserPromptSubmit`) measures the window: it
  advises a handoff once when the session passes half of it, and insists on every prompt past
  three quarters.
- `.claude/hooks/pre-compact-handoff.sh` (`PreCompact`) catches anything that still reaches a
  compaction: on `auto` it **blocks** it, and the author's next prompt shows that automatic
  compaction was stopped and to run `/handoff`, then `/clear` (or, where `/handoff` has no room
  to run, `/compact` first, which the project allows, then `/handoff`); a manual `/compact` goes
  ahead, the author's choice, and once it is done (`SessionStart`) a note says that a handoff
  gives a cleaner break, so next time `/handoff`, then `/clear`.

No setting or hook can write the handoff: a hook has only an exit code and a message. That part
is the model's. Notice the window filling, hand off **before** it is full (a compaction blocked at
the hard limit leaves the current request to fail), and stop. Where the window has no room left
to write one, say so rather than start a handoff that cannot finish: the author may run
`/compact`, then `/handoff`. After a `/compact` the author ran to make room for one, offer the
handoff at once.

## Where the handoff lives

The handoffs folder, in the filename form the project's rules give (by default
`handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md`, the form used below), committed so it travels with
the repository. The descriptor names **the work, not the session**:
`HANDOFF-OPENING-SECTIONS-03-10-2026.md`, never `HANDOFF-TUESDAY-03-10-2026.md`. Prune a handoff
once its work has resumed and landed.

## How to write a handoff

> **Mode.** Before step 1, read the mode files beside this one (the upper-case `.md` files in this folder) that the project's rules route the work at hand to; where they name none, read every one. A mode file owns the domain (paths, the unit of work, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the owner.

1. **Record durable knowledge in its real home first.** A decision or fact goes to
   `.claude/MEMORY.md` through the gate; a decision about one piece of the work to its brief; a
   folder rule to that folder's `CLAUDE.md` on the author's word; where a passage came from to the
   project's record of provenance, where its rules name one. Use `grill-with-docs` for anything
   the author has just decided. *Complete when:* nothing the handoff is about to mention exists
   only in the conversation.
2. **State the goal.** One or two sentences naming what the work is trying to achieve, so the
   fresh session orients before any detail. Look facts up rather than recalling them.
   *Complete when:* the goal sits in one or two sentences at the top.
3. **Record what is done.** The work landed this session (files written, passages drafted or
   finished, decisions recorded, checks passed), each named by its repository path.
   *Complete when:* every finished item is a one-liner with its path.
4. **Pin what is in flight.** For each open thread, the exact `path:line` anchor and its
   mid-change state; say plainly which draft is live and which is superseded. This is the
   load-bearing part: the fresh session resumes here. *Complete when:* every in-flight item has a
   `path:line` anchor and a one-line status.
5. **Carry the part this project must never drop.** The mode file names it and what it lists.
   *Complete when:* every item the mode names is listed with its path, or the handoff says the
   session did not touch it.
6. **Name the next action.** The single next step, concrete enough to start without re-deriving
   it. *Complete when:* the next action is one imperative sentence.
7. **Name the skills to load next.** The skills best suited to continue, from the skill rosters in
   the project's rules. *Complete when:* the handoff names them, in the
   order the next session loads them.
8. **Reference artefacts by path; never paste them.** Briefs, drafts, records, notes, maps,
   commits: by path, so the fresh session opens them itself. Anything confidential is named
   and located, never reproduced. *Complete when:* every artefact is a path, and no confidential
   value or quoted passage of the work appears.
9. **Write the file, print the path, then stop.** Write the handoff in the handoffs folder, in
   the filename form the project's rules name (by default
   `handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md`), print that path for the author, and
   **end the turn**, so the author can run `/clear` and resume from the file in a fresh window.
   *Complete when:* the file exists there, its path is printed, and the turn has stopped.

## What the handoff carries

A complete handoff has these parts, top to bottom; treat the list as the final check.

- **Goal** — what the work achieves, in one or two sentences.
- **Done** — landed work, each by path.
- **In flight** — open threads, each with a `path:line` anchor and its status.
- **The mode's part** — what this kind of project must never drop.
- **Next** — the single immediate action.
- **Next skills** — what the next session loads.
- **Artefacts** — everything else the work touches, by path.

Add an **Open questions** line only when the session left a decision genuinely unresolved, and make
sure it is also under the `Open questions` heading of `.claude/MEMORY.md` (under the name the
project's rules map it to). A **teaching detour** (the work pauses while a gap is closed with the
project's teaching skill) is named in the descriptor, `HANDOFF-TEACH-<TOPIC>-DD-MM-YYYY.md`, with a
`Teaching detour` line giving the topic, the concept that missed and the opening lesson, and the
teaching skill first among the next skills.

## What stays out

- Facts, decisions, feedback, status and sensitivities: each under its heading in
  `.claude/MEMORY.md`.
- What a piece of the work argues, tells or commits to: its brief.
- What the evidence supports: the evidence folder; a researched question: the research notes
  folder.
- An unresolved decision blocking a body of work: the `Open questions` heading of
  `.claude/MEMORY.md`, or the frontier of a decision map in the decision-maps folder.
- A question only someone outside the session can answer: a questionnaire, through
  `to-questionnaire`.

## Anti-patterns

- **Carrying on after the handoff.** A handoff followed by more work is stale before it is read.
- **An in-flight item with no anchor.** 'The draft is partly done' is not a handoff.
- **Pasting the work.** A handoff that quotes half a passage has recreated the context it was
  meant to replace.
- **Durable knowledge only in the handoff.** It is pruned; the decision goes with it.
- **Editing an old handoff** to bring it up to date: write a new one and prune the old.
- **Waiting for the hook.** The hook is the backstop; the rule is to hand off before it fires.

## Cross-references

- The project's session-boundaries rule (`.claude/rules/`) — the rule this skill carries out,
  and the rule both hooks cite.
- `.claude/hooks/context-threshold-handoff.sh` · `.claude/hooks/pre-compact-handoff.sh` — the
  `UserPromptSubmit`, `PreCompact` and `SessionStart` hooks; registered in `.claude/settings.json`.
- `handoffs/CONTEXT.md` — the folder and its naming.
- `.claude/skills/grill-with-docs/SKILL.md` — how durable decisions are recorded before a handoff.
- `.claude/skills/wayfinder/SKILL.md` — work whose continuity spans many sessions by design.
- `.claude/skills/wait-what/SKILL.md` and the project's teaching skill — the teaching detour.
- `.claude/MEMORY.md` — the durable memory a handoff deliberately does not duplicate.

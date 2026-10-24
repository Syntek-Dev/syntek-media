---
name: wayfinder
description: >-
  Chart work too big for one sitting into a decision map, then settle it across sessions. SUGGEST
  mines open questions, open flags and stalled plans for bodies of work worth mapping; CHART pins
  the destination and maps the frontier of open decisions into a MAP-<TOPIC>.md in the project's
  decision-maps folder; RESOLVE settles the next batch of related nodes, hands task nodes off and
  graduates each answer to its real home. Invoke by typing /wayfinder suggest, /wayfinder chart
  <topic> or /wayfinder resolve <map>, or when the author says 'map out the second half', 'where
  do we even start with the world?', 'what is left to decide before drafting?' or 'this is too big
  to settle today'. Not for one surface in one sitting (`grill-with-docs`), not for a question
  only someone else can answer (`to-questionnaire`), and it never drafts the work itself.
---

# Skill: Wayfinder

Wayfinder takes on work too big to hold in one head (a large part of the work, a world and its
peoples, a programme of documents or productions) and turns the fog into a **map** of open
decisions, settled in related batches across sessions. Instead of charging at an unclear
**destination**, it charts the route first: surface the decisions, order them, then settle them
until the way is clear.

**Scope, against grilling.** Grilling sharpens **one** surface in a sitting. Wayfinder maps a
whole body of work's **frontier** and sends batches of related nodes to grilling. Wayfinder is the
cartographer; grilling is the per-node engine. Reach straight for `grill-with-docs` when the work
is one surface.

**The map is a Markdown index, never a vault:** `MAP-<TOPIC>.md` in the decision-maps folder the
project's rules name, registered in the index table in that folder's `CONTEXT.md`. Detail lives in
the brief, note, plan file or `.claude/MEMORY.md` entry each node links to. Facts are looked up,
never asked; only decisions with a real trade-off go to the author.

**Paths.** This file names folders, files and checks by their role ('the decision-maps folder',
'the outline', 'the open-flags check'). The project's rules in `.claude/rules/` give each role its
path, and the mode files add their own.

Locale: en_GB · dates DD/MM/YYYY.

## Governing procedures (route here — do not restate at length)

- The decision-map guide — when a map earns its place, its node types, where a settled node
  goes.
- The decision-maps folder's `CONTEXT.md` and `CLAUDE.md` — the index and the folder's rules.
- The project's memory rules — where a decision lives, and the memory gate.
- `.claude/skills/grilling/SKILL.md` — the round shape every grilling node is settled in.

The mode files name the procedures that chart with a map.

## Steps

> **Mode.** Before step 1, read the mode files beside this one (the upper-case `.md` files in this folder) that the project's rules route the work at hand to; where they name none, read every one. A mode file owns the domain (paths, the unit of work, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the owner.

A session runs in one of three modes: **SUGGEST** (optional, before there is a topic), **CHART**
(one session) or **RESOLVE** (each later session). Steps are numbered across all three.

### SUGGEST (steps 1 to 3)

1. **Read the unfinished business.** The `Open questions` heading of `.claude/MEMORY.md` (under
   the name the project's rules map it to); every open flag, through the open-flags check the
   project's rules name; questionnaires still out; stalled plans (an outline row with no brief, a
   brief that has not moved status, a review in the reviews folder whose decisions were
   deferred). *Complete when:* every open item is in view with where it came from.
2. **Cluster into candidate bodies of work.** Group items that share a cause, a surface or a
   dependency: five flags waiting on one undecided reading are one map, not five. An item that one
   grilling sitting would settle is not a map; say so and route it to `grill-with-docs`.
   *Complete when:* every item is in a cluster or routed elsewhere.
3. **Put the candidates, ranked.** For each: what it would settle, why it hangs together, what
   stays open if it is not taken. Rank by how much each unblocks against its size. **Suggest
   only**: write nothing. *Complete when:* the author has picked one, deferred them all or
   redirected.

### CHART (steps 4 to 8)

4. **Pin the destination.** Open a `grill-with-docs` pass to say what 'done' looks like in one
   or two lines, and the bounds: what is in, and what is consciously out. Look the repository up
   before asking. *Complete when:* the destination and the out-of-scope bounds are written and
   confirmed.
5. **Map the frontier, breadth first.** Walk every file the work touches (the outline, the
   briefs, the plan files, the research, the files the mode names) and surface every decision
   that can be stated now. Anything too vague to state goes to **Fog of war**. *Complete when:*
   every knowable decision is a node or is parked in Fog of war.
6. **Wire the blocking edges.** In a second pass, give each node its blockers as prose links to
   the nodes it depends on, so the unblocked edge is visible at a glance. *Complete when:* every
   frontier node names its blockers (or 'none') and at least one is unblocked.
7. **Write the map and register it.** Create `MAP-<TOPIC>.md` in the decision-maps folder in the
   shape below, tag each frontier node with its
   type, and add a row to the index table in that folder's `CONTEXT.md` (Map · Destination ·
   Frontier open? · Charted).
   *Complete when:* the map exists, is indexed, and reads as a route rather than a store of answers.
8. **Dispatch the research nodes, then stop.** Send research nodes (facts, not decisions) to the
   project's research or fact-checking skill now; they need no human. Settle nothing else in a chart session.
   *Complete when:* the research nodes are dispatched and the session ends with the frontier
   drawn but unresolved.

### RESOLVE (steps 9 to 13)

9. **Load the map, then re-check what it asserts.** Read the map; open linked files only as
   needed. Re-check every load-bearing claim the next batch leans on (a cited line, a count, a
   status), because a drifted citation still reads plausibly. *Complete when:* the destination and
   the current frontier are in view and the batch's claims are re-checked.
10. **Take the next batch, not the next node.** Start from the author's pick or the unblocked
    frontier, and gather nodes that belong together: a **shared subject**, **mutual dependence**
    (one's answer changes another's) or **shared evidence**. Split off any node with open blockers
    or of another type; parents before dependants. Order the batches by what unblocks the most
    downstream nodes, and split a batch past what one sitting can hold honestly. *Complete when:*
    the batch is named, every member is unblocked, why they belong together is one line, and no
    other unblocked batch would free more of the map.
11. **Settle the batch by type.** Research legs first, so the grilling round opens with the facts
    in hand. Grilling nodes go to `grill-with-docs` as **one** pass: the batch is its first round.
    A prototype node runs the project's prototyping skill. A task node is **handed off, never
    done by the map**: to the project's record of permissions and approvals, where its rules name
    one and the task is a permission or an approval; to the `Open questions` heading of
    `.claude/MEMORY.md`; or to a questionnaire through `to-questionnaire` where only someone else
    can supply it. It stays on the frontier, marked
    with where it went, until its result is back. Any node may first be probed with a prototype.
    *Complete when:* every grilling and prototype node in the batch has a decision, made and
    confirmed, and every task node is handed off with its destination on the map.
12. **Graduate each outcome.** Record every settled decision in its real home through the
    graduation table; never leave an answer only on the map. *Complete when:* each outcome lives
    in its home and each `Resolved decisions` entry links to it.
13. **Redraw the frontier once.** Move the batch to `Resolved decisions`, turn Fog-of-war items the
    outcomes sharpened into nodes, re-wire the edges, and update the index row's `Frontier open?`.
    *Complete when:* the frontier shows the new unblocked edge and no settled node remains on it.

## Reference

### The map

```text
# MAP-<TOPIC> — <title>
## Destination           one or two lines: what this body of work reaches
## Notes                 the layers it touches, skills to load, standing preferences
## Resolved decisions    settled; each links to the brief, note, plan file or MEMORY entry it became
## Frontier              open decisions in dependency order; blocking edges as prose links
## Fog of war            in scope, not yet sharp enough to be a node
## Out of scope          consciously ruled out, and why
```

### Node types

- **Research** — a fact: looked up through the research or fact-checking skill, never asked.
- **Prototype** — a rough throwaway piece that raises fidelity on a foggy node (the prototyping
  skill).
- **Grilling** — a decision with a real trade-off, settled with the author in `grill-with-docs`.
- **Task** — manual unblocking work someone must do outside the map: obtaining a source, a
  permission, a confirmation, a figure. The map hands it off (step 11); it never does it.

### Graduation table (step 12)

| A settled decision that is… | Graduates to… |
|---|---|
| project-wide, hard to reverse, surprising without context, a genuine trade-off | `.claude/MEMORY.md`, the `Decisions` heading, through the gate in `grill-with-docs` |
| about what one piece of the work does, its scope or its parts | that piece's brief |
| about the shape or order of the whole work | the outline |
| a checked fact | an evidence entry in the evidence folder, through the fact-checking skill |
| an answered question | a note in the research notes folder, through the research skill |
| a term | the terminology file |
| a rule for the whole work | the standard, **author-confirmed**, then noted in `.claude/MEMORY.md` |
| still open and blocking | `.claude/MEMORY.md`, the `Open questions` heading, naming what it blocks |

The mode files add this project's rows. `grill-with-docs` owns *which* home a decision lands in;
wayfinder only makes sure it lands.

### When each session is done

A **suggest** session, when every open item is clustered and the candidates are put; a **chart**
session, when every knowable decision is on the map and the frontier is ordered; a **resolve**
session, when the batch is settled, graduated and the frontier redrawn. A **map** is done when
Frontier and Fog of war are both empty; it stays as the record.

## Anti-patterns

- **Resolving during a chart session.** Charting draws the frontier; it settles nothing.
- **Storing decision detail on the map.** The map is a low-resolution index.
- **Drafting the work from a map session, or doing a task node.** A map spawns work; it does
  not do it.
- **Asking what the repository can answer**, or settling an empirical node by asking.
- **Grilling the whole body of work in one sitting.** That is what the frontier is for.
- **A map for one surface.** One sitting's worth of decisions is a `grill-with-docs` pass.

## Cross-references

- `.claude/skills/grilling/SKILL.md` · `.claude/skills/grill-with-docs/SKILL.md` — the engine and
  the recorder a grilling node goes to.
- `.claude/skills/to-questionnaire/SKILL.md` — where a task node goes when only someone else can
  supply it.
- The project's rules in `.claude/rules/` — the research, fact-checking and prototyping skills,
  the decision-maps folder and its index, and the path of every other role this file names.
- `.claude/MEMORY.md` — the `Open questions` heading that SUGGEST mines, and the `Decisions`
  heading that nodes graduate to (under the names the project's rules map them to).

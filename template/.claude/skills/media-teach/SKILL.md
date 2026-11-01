---
name: media-teach
description: >-
  Open a practice workspace where the author learns a media craft, tool or platform without
  touching the real work: one concept per lesson at the edge of current ability, unaided recall
  before any re-reading, a worked practice piece in a house format with invented people and
  organisations only, and a spaced review schedule kept in the topic's progress file. Reads the
  project freely as reference; writes text only, inside its own topics in the learning folder,
  and spends, publishes and files nothing. Use when the author says 'teach me to storyboard',
  'help me practise writing for the ear', 'I want to get better at editing', 'quiz me on the
  toolkit' or 'pick up where my last lesson left off'. Not for
  re-explaining one reply that did not land (`wait-what`). Not for the real work
  (`run-media-workflow`). Not for a writing topic, or one another template's teaching skill
  keeps (the teach skill (syntek-author), where present).
---

# Skill: Media Teach (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

This skill opens a **learning workspace** where <%OWNER_FIRST_NAME%> practises a media craft, a
tool or a platform without touching the work. The posture is the inverse of a normal task: the goal
is not a finished piece but a durable skill, built through **lessons** pitched at the edge of what
the author can already do, drilled by **unaided recall**, and consolidated on a **spaced review**
schedule. The project is read freely as reference; every practice piece, example and note lands in
the topic's own folder only, as text.

It follows the teach skill (syntek-author), where present, and runs beside it: that skill keeps its
own topics, writing craft among them, and this one keeps media's. Neither stands aside for the
other, and neither touches the other's topics.

## Governing procedures (route here — do not restate at length)

**No layer's procedure runs this skill.** It is a sandbox, not a step towards any gate. What
governs it:

- If a layer's `workflows/local/` holds a procedure of the author's that names this skill, follow
  that procedure instead: the author's local procedure governs (`run-media-workflow`, step 2).
- `.claude/rules/syntek-media/03-production-ethics.md` Section 4 — never spend unasked, which a
  lesson never does; Section 7 — never fabricate, which a lesson does not relax: a source not to
  hand is named as missing, never recalled.
- `.claude/rules/syntek-media/06-global-rules.md` Section 7 — supportive proofreading, which every
  recall answer receives; Section 10 — confidentiality.
- `.claude/rules/syntek-media/02-skills.md` Section 4 — the teaching role, routed by the work at
  hand, looking in both places.

The mode file adds this project's domain family and the house sources each family practises
against.

## The one rule: the project is read-only during a lesson

A lesson reads the real work, the guides, the brand and the toolkit as reference, and writes
**only** inside its own topic ('Where a topic lives'), as text.

- **Nothing is spent, published or filed.** No credit-spending call (ElevenLabs or any other
  service), no post, no schedule, register, rights or credits-log row, and no piece number. No
  `footage add`, and never the data-root resolver's `add`: a lesson files nothing.
- **Every clip and render goes outside the repository.** A tone or clip made for a lesson
  (`ffmpeg -f lavfi`), anything the author records to practise with, and every render of it go in
  a temporary folder outside the repository, made for the session and named in the lesson, never
  under any raw, generated or renders folder. The lesson keeps the commands as text.
- **No practice piece is ever promoted**, numbered, voiced, posted or left where it could be taken
  for a real piece. A good one is a reason to make the real piece properly, through its procedure.

Each topic is one folder, made at its first lesson. This skill draws the layout itself, because
the learning folder's pair, where it stands, is syntek-author's:

```text
<topic>/
├── MISSION.md     ← the H1 naming the topic, then the Template line; why it is learned, the goal, the family
├── RESOURCES.md   ← the primary source and the house source for each lesson
├── PROGRESS.md    ← the recall log, each lesson's next-review date, what is consolidated
└── LESSONS/       ← worked practice pieces, text only
```

## Where a topic lives

Decide this each time the skill runs, from the names of the answers files at the project root (the
folder that holds `.copier-answers.syntek-media.yml`), and never record the answer anywhere. The
test reads file names only, never an answers file's contents, and no question or setting stands in
for it.

- **Alone or shared.** Another template shares the project while any other file matching
  `.copier-answers.*.yml` stands at the root beside `.copier-answers.syntek-media.yml`. Alone, a
  new topic is `learning/<topic>/`. Shared, it is `learning/syntek-media/<topic>/`, in a folder
  made with its first topic. Never write a `CONTEXT.md` or `CLAUDE.md` in the learning folder, in
  this template's folder there or in a topic: the learning folder's pair, where present, is
  syntek-author's and is its only manual.
- **What a topic is.** A topic is a folder holding a mission file or a progress file
  (`learning/<topic>/MISSION.md` or `learning/<topic>/PROGRESS.md`, or the same inside
  `learning/syntek-media/<topic>/`). A folder at the top of the learning folder named
  syntek-media or syntek-author, or named for the `<name>` of any `.copier-answers.<name>.yml` at
  the root, is a template's folder, never a topic.
- **Resume a topic where it stands.** Look for it in `learning/syntek-media/<topic>/` first, then
  in `learning/<topic>/`, and resume the first found where it is: never move or copy it, into
  this template's folder or out of it, whichever template came first. Where a folder of that name
  at the top of the learning folder holds neither file (an adopted or hand-made record), ask
  whether it is this topic before starting another. Only a new topic goes into this template's
  folder.
- **Whose a topic is.** A new topic's mission file carries, alone on the line after its H1,
  exactly `Template: syntek-media`. While another template shares the project, a topic at the top
  of the learning folder without a `Template:` line is <%OWNER_FIRST_NAME%>'s to name: take its
  family as a hint only, ask once, and write the answer as its `Template:` line, the one line this
  skill writes in a topic that may not be its own. Ask; never infer it, and never decide by
  which template was applied first. Where that topic holds a progress file but no mission file,
  the answer goes in a new `learning/<topic>/MISSION.md` holding only an H1 naming the topic and the
  `Template:` line. In a project of media's alone, a topic without the line is media's.
- **Another template's topics follow its rules.** Another template's folder, and a topic whose
  `Template:` line names another template, are governed by that template's teaching skill and
  rules, never this one's, and stay <%OWNER_FIRST_NAME%>'s work: never resume, list or edit them.
  If <%OWNER_FIRST_NAME%> names one, say so and route to that skill (the teach skill
  (syntek-author), where present).
- **No topic is named after a template:** not syntek-media, not syntek-author, and not the
  `<name>` of any answers file at the root. Where a new topic's folder would take such a name, ask
  for another.
- **A redirect** of the learning folder under the Overrides section of syntek-author's
  00-project.md, where present, carries all of this with it: read that path in place of the
  learning folder, and place, resume and name topics there by the same rules.
- **The version this needs.** Where both templates keep lessons, the project runs syntek-author
  `v0.8.0` or later (syntek-author D57), whose teaching skill places its own topics by the same
  rules. This skill never checks the version; the update report and the user guide say it.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Place the topic.** Work out, from the answers files' names, whether the project is alone or
   shared, and find the topic as 'Where a topic lives' says: resume it where it stands, ask once
   whose a line-less one is, route another template's topic away, or choose the folder for a new
   one. *Complete when:* the topic's folder is known and is this skill's, or the request has been
   routed to the other template's teaching skill and nothing was written.

2. **Clarify the mission.** Read the topic's mission file if it exists. If it is missing or thin,
   ask why <%OWNER_FIRST_NAME%> wants this skill and what 'can do it' looks like, in the grilling
   posture (the `grilling` skill, where present, owns the shape: a round of questions, each with a
   recommended answer; where it is absent, ask in rounds yourself). Record the goal, the
   **family** from the mode file (craft, tool, platform or the mode's domain) and, in a new topic,
   the line `Template: syntek-media` after the H1. *Complete when:* the mission file states the
   goal and the family in the author's own words, and a new topic's mission file names its
   template.

3. **Assess the level; set the next lesson.** Read the progress file for what is consolidated, and
   look the real subject up in the project first: the guide, the procedure, the toolkit's own help
   (`python3 toolkit/media.py --help`), the brand's files and finished pieces that already do it
   well. Never ask what the project already answers. Pick the **one** next lesson at the edge of
   the current level: a step that cannot yet be done alone but can with support. A topic arriving
   from `wait-what`, through a teaching-detour handoff, already names its opening lesson: start
   there. *Complete when:* the next lesson is named as a single, tightly scoped concept.

4. **Gather the resources.** Put in the resources file the **primary source** and the **house
   source** the mode names for the family: the house format the author will practise in. Where the
   subject is a platform's rule, a licence, a consent or disclosure rule or a tool's behaviour, the
   primary source is read through `media-research`, never recalled; a writing subject's source is
   the teach skill's (syntek-author), where present. Cite; never paraphrase from memory, and if a
   source is not to hand, say so. *Complete when:* the resources file points at a primary source
   and the house source for this lesson.

5. **Run the lesson: recall, then build.** Teach the concept, then close the loop:
   - **Recall:** pose a short question, wait for the answer, then confirm or correct. Effortful
     recall builds retention; a re-read only feels like it.
   - **Build to learn:** the author makes a small throwaway piece in the topic's lessons folder,
     in the real house format (a script beat, a storyboard row, an edit decision list, a cut-down
     plan, a card layout, a post package), with **invented people, places and organisations
     only**. A command the lesson runs reads the project or the temporary folder and writes only
     there, and the lesson records it as text.

   *Complete when:* the concept has been recalled unaided and a worked piece sits in the topic's
   lessons folder.

6. **Capture the lesson; schedule the review.** Append to the progress file: what was learned, the
   recall result, any misconception to drill again, and the next-review date on a widening curve
   (one day, three days, seven days, as DD/MM/YYYY). *Complete when:* the progress file holds a
   dated entry with a next-review date.

7. **Close the session cleanly.** Update the mission and resources files if the goal or sources
   shifted, and leave the progress file naming what is consolidated and what the next session
   opens on. Delete nothing the author made; say where the temporary folder is, so the author can
   remove it. *Complete when:* a fresh session could resume from the topic's files alone, and
   nothing outside the topic has changed but a `Template:` line the author named.

## Lesson design

- **One concept per lesson**, small enough to finish in a sitting.
- **Interleave:** bring recall from earlier lessons into a new one, so retrieval stays effortful.
- **Ground every lesson in the mission.** A lesson that does not move towards the stated goal is
  the wrong lesson; go back to step 3.
- **Quiz cleanly.** Phrase recall so the shape of the question does not give the answer away.
- **Recall is judged on substance**, never on spelling or arithmetic form: reflect the correct
  form back naturally, and never comment on how an answer was written.
- **Cite the primary source** in the lesson, so the author can go deeper than the lesson does.
- **Practise on the house formats**, so what is learned transfers to the real procedure unchanged.

## Anti-patterns

- **Writing outside the topic:** a practice beat into a real script, a mock row in a register or
  the schedule, a stray change to a guide, a brand file or a profile, or any change to another
  template's lessons.
- **Spending to practise:** a voice generated, a transcription made or any other paid call, even
  'just to hear it'.
- **Filing a practice clip,** or leaving one under a raw, generated or renders folder.
- **Practising on a real person, brand or client,** or on their real figures: a practice piece
  that names one will one day be found and read as real.
- **Asking what the project already answers.** Look it up first (step 3).
- **Re-reading in place of recall,** or teaching ahead of the edge: a lesson that cannot be
  attempted is wasted, and one already mastered is a re-read.
- **A wall of lessons at once.** Teach one, drill it, schedule its review, then the next.
- **Moving a topic,** into this template's folder or out of it: it is resumed where it was begun.
- **Guessing whose a topic is** from its family or from which template came first.
- **Writing the learning folder's pair,** or a pair in this template's folder or a topic.

## Cross-references

- `media-research` — how a lesson's primary source is read, for a platform, a licence, a consent
  rule or a tool.
- `wait-what`, where present · `handoff`, where present — the teaching detour a topic can arrive
  through.
- `grilling`, where present — the questioning posture step 2 borrows.
- `run-media-workflow` — the real work, when a lesson shows the author is ready for it.
- The teach skill (syntek-author), where present — its own topics, writing craft among them.
- `.claude/rules/syntek-media/02-skills.md` Section 4 — the teaching role, beside syntek-author's.

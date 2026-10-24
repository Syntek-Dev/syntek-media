# 02-skills.md — the media skills, the family-shared skills and companions, and the mode files

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

Skills live in `.claude/skills/<skill>/SKILL.md`. This file is syntek-media's roster: which media
skills ship here, what each does and which carry a mode file; the family-shared skills every
Syntek template ships, and the media path each of their roles takes; and which of syntek-author's
skills media uses where they are present. The `.claude/skills/` pair routes here.

---

## 1. Skills only

**syntek-media ships no commands and no agents.** Every media procedure is a skill. A skill runs
when it is named (`/write-script`) or when the author describes its job ('cut this for TikTok'). A
media job no skill claims, 'what's next on the trailer?' or 'pick up the voiceover', goes to
`run-media-workflow`, which resolves it to a workflow. A skill that carries out a workflow runs
the project's alias for it (the Workflow aliases of syntek-author's 00-project.md, where present)
or the same-named procedure in `workflows/local/` instead, where one exists. Where work benefits
from a separate context, the skill runs itself as a forked subagent (`context: fork`).

**The skills in Section 3 are template-owned by syntek-media**, even where
`.claude/skills/CONTEXT.md`, written by whichever template was applied first, calls any skill
outside its own roster the author's own. A media skill that is not listed here does not ship in
this project on purpose: never recreate one, and never improvise a substitute under its name;
say which skill is missing and why it matters. The family-shared skills of Section 4 belong to no
one template, and Section 4 says how they are kept.

---

## 2. Modes

<: if BRAND_KIND == 'business' :>**The mode file in this project is `BUSINESS.md`, and beside a family-shared skill `MEDIA-BUSINESS.md`.**
<: endif :><: if BRAND_KIND == 'author-fiction' :>**The mode file in this project is `FICTION.md`, and beside a family-shared skill `MEDIA-FICTION.md`.**
<: endif :><: if BRAND_KIND == 'author-nonfiction' :>**The mode file in this project is `NONFICTION.md`, and beside a family-shared skill `MEDIA-NONFICTION.md`.**
<: endif :>That sentence names the mode of media's work only: syntek-author's skills, where present,
carry their own mode files, and its rules name theirs. A moded media skill's `SKILL.md` is the
same in every brand kind; the domain lives in the one mode file that ships beside it. Every moded
media `SKILL.md` carries this paragraph before step 1:

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

Every family-shared skill (Section 4) carries the neutral form instead, because another Syntek
template in the same project may ship mode files of its own beside it:

> **Mode.** Before step 1, read the mode files beside this one (the upper-case `.md` files in this folder) that the project's rules route the work at hand to; where they name none, read every one. A mode file owns the domain (paths, the unit of work, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the owner.

This is the routing that paragraph means. Media ships one mode file beside five of them
(`grilling`, `grill-with-docs`, `handoff`, `to-questionnaire` and `wayfinder`), named with a
`MEDIA-` prefix so that it never collides with another template's. **For media work (a piece, the
brand kit, the spoken voice, a platform, a post), read the `MEDIA-` mode file named above and no
other.** Any other upper-case file there is another template's: apply it only to work in the
layers that template's rules route, never to media's. `grill-me` and `wait-what` have no media
mode file, and for media work they read none. Where work touches both templates and their mode
files disagree, say so to the author rather than choosing silently.

Every mode file has the same four sections: `## Paths and unit`, `## Additions to the steps`
(keyed by step number), `## Domain rules` and `## Examples`; its unit is one piece, or the
brand-wide subject it names. **A mode file applies only when its `SKILL.md` carries one of the
Mode paragraphs above**: a project's own skill kept under a skill's name does not, so the mode
file beside it is ignored.

---

## 3. Media skills

| Skill | What it does | Mode |
|---|---|---|
| `run-media-workflow` | The router for media work no other skill claims, 'what's next?' or 'pick up the trailer': syntek-author's Workflow aliases first, where present, then each media layer's `workflows/local/`, then its index (or its workflow folders, where the index has no table); loads `STEPS.md` with `CHECKLIST.md` open, obeys the M-gates, routes a storyboarded scene on its first undated `M4.*` sub-check, and biases towards finished, approved deliverables | none |
| `write-script` | Brief to spoken script for one scripted piece (hook, beats, call to action), timed with `media.py script time`; adapts from written work without editing it; revises on the author's notes; records approval (M2), and M3 `n/a — no picture` for a piece with no picture; never an audiobook | moded |
| `storyboard` | Script to storyboard and shot list: a picture for every spoken line, vertical framing, on-screen text, sound and a source for every shot; opens a `needed` rights row for anything licensed or identifiable (M3); scene boards use `scene` and `native`, timing-only re-times keep M3, and other pieces record the four `M4.*` as `n/a`; never for a recorded piece | moded |
| `repurpose` | One long piece to a cut-down plan per selected platform: the lines each cut carries, its In and Out on the master, hook, framing and caption width; a silent loop for a web page as a cut with no words; refuses near-identical batches | moded |
| `thumbnail-brief` | Brief and HTML layout for a piece's thumbnails, covers and other images, copied from the brand's thumbnail layout; renders them with `card.py`, encodes posters, share, featured and preview images with `media.py image`, makes the GIF preview under its overlay, and checks legibility, the safe zone and the grid crop | moded |
| `prepare-post` | The post package per deliverable and per placement on the brand's own channels (title, description, hashtags, disclosure, captions, thumbnail, rights; a placement's own bullets and agreement), a feed episode's register words and feed check, and its schedule row (M7); never posts; writes the publish-log row from what the author reports | moded |
| `voiceover` | ElevenLabs text-to-speech, one segment per spoken sentence or beat: the narrator, the request text, the cost stated and agreed, one call at a time, `take add`, listening, approved takes archived, `voice join`, offline `transcribe` and `lipsync` for scene timing with accepted files in `production/src/timing/`; a character's voice remixed from the author's cleared clone (`voice remix plan` and `run`), chosen, saved and recorded through `production/workflows/11-design-character-voices/`; espeak-ng only as a scratch track | moded |
<: if 'audiobook' in MEDIA_KINDS :>| `narrate-audiobook` | An audiobook, planned in its chapter register with its credits (its M2: an audiobook has no script), then chapter by chapter by the route each channel accepts (human, AI or external): text through `media.py audiobook text`, takes one call at a time, mastering and the ACX check through the toolkit, every approved master archived, disclosure always | moded |
<: endif :>| `captions` | Captions by four timing routes, aligned known words included; a recorded piece's transcript; speech-to-text only when asked; SRT and VTT to house limits; `captions check`; burned or sidecar per platform; published transcripts (M6); model fetch left to the author | none |
| `cut-for-platform` | Every render through the toolkit: the footage edit and cards through `assemble`, or the scene kit through stills/preview review and native masters (M4), `cut` and `encode` per deliverable with captions burned in the same pass (web video, silent loops and a feed episode's untagged audio among them), loudness, and a probe of every output (M5); `feed tag` at M7 | none |

---

## 4. Family-shared skills, the paths they reach, and the companions from syntek-author

Seven working-practice skills are **family-shared**: every Syntek template ships their `SKILL.md`
byte for byte, so a project with two templates keeps one copy.

| Skill | What it does | Media mode file |
|---|---|---|
| `grilling` | The engine: an interview in frontier rounds, every unblocked question in one message with a recommended answer, that sharpens a brief, the brand kit, the spoken voice or a plan before any of it is made; `grill-me` and `grill-with-docs` load it | yes |
| `grill-me` | Grilling that records nothing: the interview is the point | none |
| `grill-with-docs` | Grilling that records each decision as it resolves, in its home or in `.claude/MEMORY.md` through the gate; the design-work default (`.claude/rules/syntek-media/06-global-rules.md` Section 8) | yes |
| `wayfinder` | Charts work too big for one sitting (a series, a launch, a channel's first season) into a decision map, settled across sessions in batches; hands tasks off, never does them | yes |
| `handoff` | Writes a handoff and stops: run instead of compacting, and when either session hook fires (`.claude/rules/syntek-media/07-session-boundaries.md`) | yes |
| `to-questionnaire` | Turns a decision only someone outside the session can answer into a questionnaire, on the author's word only, and records what stays blocked; never sends it | yes |
| `wait-what` | Re-pitches a reply that did not land, conclusion first, in the project's own words | none |

**How they are kept.** Each family-shared `SKILL.md` is copy-only shared, like the hooks in
`.claude/hooks/` and the `handoffs/` pair: a copy writes it where it is absent and skips it where
it stands, and media's `copier update` never renders, changes or recreates it. A project updated
from a media release before 0.5.0 therefore has none of them until it takes them by hand, as
`.claude/syntek-media-agents.md` says, unless syntek-author's copy or update has written them;
every media file that names one says what to do where it is missing. Never edit one, and never
write one from memory: tailor the work in a project rule instead. The `MEDIA-` mode files beside
them are template-owned and updated like the media skills.

A family-shared `SKILL.md` names no path that only one template ships: it names a **role**, and
this table gives each role its path for media work. syntek-author's rules give the same roles
their paths for its own work, where it is applied. Where the Paths of syntek-author's
00-project.md give a shared row below (handoffs, memory headings, decision maps) another path,
that path wins.

| Role, as the shared skills name it | Path for media work |
|---|---|
| The project's rules | `.claude/rules/syntek-media/`, beside syntek-author's rules, where present, with its 00-project.md first |
| Mode files | <: if BRAND_KIND == 'business' :>`MEDIA-BUSINESS.md`<: endif :><: if BRAND_KIND == 'author-fiction' :>`MEDIA-FICTION.md`<: endif :><: if BRAND_KIND == 'author-nonfiction' :>`MEDIA-NONFICTION.md`<: endif :> beside the `SKILL.md` (Section 2) |
| Skill rosters | this file, and syntek-author's own roster, where present |
| Global rules (never self-edit; design opens with grilling; internal notes; confidentiality) | `.claude/rules/syntek-media/06-global-rules.md` Sections 3, 8, 9 and 10 |
| Authorship rules (the author decides; the AI recommends) | `.claude/rules/syntek-media/03-production-ethics.md` Section 1 |
| Method standard (evidence before the work; flag, never fabricate) | `.claude/rules/syntek-media/03-production-ethics.md` Sections 7 and 8 |
| Memory rules (where a decision lives; the memory gate; the entry form) | `.claude/rules/syntek-media/08-naming-and-memory.md` Sections 2 to 4 |
| Session-boundaries rule | `.claude/rules/syntek-media/07-session-boundaries.md` |
| Memory headings (`Decisions`, `Facts`, `Feedback`, `Status`, `Open questions`, `Sensitivities`) | the headings of `.claude/MEMORY.md`, under the names the Memory headings of syntek-author's 00-project.md map them to, where present |
| Handoffs folder and filename | the Paths of syntek-author's 00-project.md, where present; otherwise `handoffs/HANDOFF-<DESCRIPTOR>-DD-MM-YYYY.md` |
| A piece of the work (what one brief covers) | a piece, `scripts/src/pieces/NNN-kebab-title/` (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 5) |
| Brief, briefs folder, and the brief guide | `scripts/src/pieces/<piece>/brief.md`; `scripts/src/pieces/`; `scripts/docs/reference/the-piece-ladder.md` (settled positions: `## Key points`; draft notes: `## Notes`) |
| Plan files | the mode file names them: the piece register, the schedule and the rights register |
| Outline | `scripts/src/piece-register.md` for which pieces exist, and `publishing/src/schedule.md` for their order |
| Planning procedure | `scripts/workflows/01-brief-a-piece/` (questioning: steps 3 to 7; the brief and M1: steps 8 and 9; recording: step 10) |
| Whole-work review procedure, and the reviews folder | none in media: a review across pieces is a decision map |
| Decision-maps folder and its index, and the questionnaires folder | syntek-author's, at the path its 00-project.md gives, where present; standalone, none ships: agree a folder with the author, record it under 'Project-specific rules' in `.claude/CLAUDE.md`, and write its pair before the first file |
| Decision-map guide | syntek-author's, where present; otherwise the Reference section of the `wayfinder` skill |
| Terminology file | syntek-author's style sheet and terminology, where present (`.claude/rules/syntek-media/06-global-rules.md` Section 1); spoken names and pronunciations live in `brand/src/voice/voice.md` |
| Voice guide | `brand/src/voice/voice.md`, the spoken voice, beside syntek-author's written voice, where present |
| Evidence folder, and research notes folder | syntek-author's, where present; otherwise a source and the date it was read go in the brief or guide that relies on it |
| Record of provenance | none: media keeps no ledger (below); each item a piece uses has its row in `production/src/rights-register.md` |
| Record of permissions and approvals | `production/src/rights-register.md` for a licence, permission, release or consent; a piece's approvals are the dates in its brief's `verified` |
| Open-flags check | `python3 toolkit/media.py flags` |
| Fact-checking and research skills | the fact-check and research skills (syntek-author), where present (below) |
| Prototyping and teaching skills, and the learning workspace | syntek-author's, where present; media ships none |

**Companions from syntek-author.** These are syntek-author's skills, and unlike the family-shared
skills above they never ship here. Media names each one unbackticked, in one fixed form, 'the
spelling skill (syntek-author), where present', never in `skills:` frontmatter, and a skill
checks for `.claude/skills/<skill>/SKILL.md` at run time before it names the step. Where a
companion is absent, say which skill is missing and what it would have checked; never recreate
it.

| Companion (syntek-author), where present | Applies to | How media uses it |
|---|---|---|
| spelling, grammar | scripts, transcripts, post copy, caption text | a supportive report; fixes applied only when accepted (a transcript's words are what was said: only a mis-transcription is fixed); part of M2 |
| comprehension | scripts | a report, read as the audience test (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 1) |
| flow | scripts | a report on order, rhythm and repetition across beats |
| fact-check | every factual claim in a script, transcript or post | verdicts; an unresolved claim stays `VERIFY`; M2 and M7 need none open |
| improve-section | a script the author drafted | report, then the agreed edits only; no ledger entry and no status change, said before it runs |
| adapt-section | a script revised from the author's notes | report, then the agreed edits only; no ledger entry; the revise step of `write-script` is the fallback |
| research | platform policies, the facts behind a script | as practice; sources and dates recorded where the guide says |
| social-media-documents | social media plans, content calendars, operating procedures, bios, channel voice, text-only posts | owns what each document sets for a platform where present, document by document; media's profiles, schedule and posts cite them, never duplicate them |
| run-workflow | — | a boundary only: writing work goes there, a blog post's or a newsletter issue's own words included |
| pronounce | — | never run by media; its IPA is the source for constructed names in `brand/src/voice/voice.md` |

The provenance ledger belongs to syntek-author's content layer, so improve-section and
adapt-section run on a script with no ledger step, and the revise step of `write-script` takes
over when a companion refuses a file that is not a section draft.

---

## 5. Working with skills

- **Read the whole `SKILL.md`, then its mode file if it carries a Mode paragraph, before
  step 1**: for a family-shared skill, its `MEDIA-` mode file (Section 2). Each step ends with a
  completion test; a step is not done until its test passes.
- **Skills never edit themselves or each other** without the author's explicit instruction
  (`.claude/rules/syntek-media/06-global-rules.md` Section 3).
- **A project-specific change to how a skill behaves** is an entry in the Overrides of
  syntek-author's 00-project.md, where present, or a project rule
  (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10), never an edit of the skill.
- **A skill that spends credits** carries the call discipline of
  `.claude/rules/syntek-media/03-production-ethics.md` Section 4 in its own steps.
- **A skill of the author's own** goes in a new folder whose name collides with no media or
  syntek-author skill; its frontmatter `name` equals the folder, and Copier never touches it.

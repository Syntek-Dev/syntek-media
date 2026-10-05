# 02-skills.md — the media skills, the companions from syntek-author, and the mode files

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

Skills live in `.claude/skills/<skill>/SKILL.md`. This file is syntek-media's roster: which media
skills ship here, what each does, which carry a mode file, and which of syntek-author's skills
media uses where they are present. The `.claude/skills/` pair routes here.

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
say which skill is missing and why it matters.

---

## 2. Modes

<: if BRAND_KIND == 'business' :>**The mode file in this project is `BUSINESS.md`.**
<: endif :><: if BRAND_KIND == 'author-fiction' :>**The mode file in this project is `FICTION.md`.**
<: endif :><: if BRAND_KIND == 'author-nonfiction' :>**The mode file in this project is `NONFICTION.md`.**
<: endif :>That sentence names the mode of media's skills only: syntek-author's skills, where present,
carry their own mode files, and its rules name theirs. A moded skill's `SKILL.md` is the same in
every brand kind; the domain lives in the one mode file that ships beside it. Every moded
`SKILL.md` carries this paragraph before step 1:

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

Every mode file has the same four sections: `## Paths and unit`, `## Additions to the steps`
(keyed by step number), `## Domain rules` and `## Examples`; its unit is one piece. **A mode file
applies only when its `SKILL.md` carries the Mode paragraph above**: a project's own skill kept
under a media skill's name does not, so the mode file beside it is ignored.

---

## 3. Media skills

| Skill | What it does | Mode |
|---|---|---|
| `run-media-workflow` | The router for media work no other skill claims, 'what's next?' or 'pick up the trailer': syntek-author's Workflow aliases first, where present, then each media layer's `workflows/local/`, then its index (or its workflow folders, where the index has no table); loads `STEPS.md` with `CHECKLIST.md` open, obeys the M-gates, and biases towards finished, approved deliverables | none |
| `write-script` | Brief to spoken script for one scripted piece (hook, beats, call to action), timed with `media.py script time`; adapts from written work without editing it; revises on the author's notes; records approval (M2), and M3 `n/a — no picture` for a piece with no picture; never an audiobook | moded |
| `storyboard` | Script to storyboard and shot list: a picture for every spoken line, vertical framing, on-screen text, sound and a source for every shot; opens a `needed` rights row for anything licensed or identifiable (M3); never for a recorded piece | moded |
| `repurpose` | One long piece to a cut-down plan per selected platform: the lines each cut carries, its In and Out on the master, hook, framing and caption width; a silent loop for a web page as a cut with no words; refuses near-identical batches | moded |
| `thumbnail-brief` | Brief and HTML layout for a piece's thumbnails, covers and other images, copied from the brand's thumbnail layout; renders them with `card.py`, encodes posters, share, featured and preview images with `media.py image`, makes the GIF preview under its overlay, and checks legibility, the safe zone and the grid crop | moded |
| `prepare-post` | The post package per deliverable and per placement on the brand's own channels (title, description, hashtags, disclosure, captions, thumbnail, rights; a placement's own bullets and agreement), a feed episode's register words and feed check, and its schedule row (M7); never posts; writes the publish-log row from what the author reports | moded |
| `voiceover` | ElevenLabs text-to-speech, one segment per spoken sentence or beat: the narrator, the request text, the cost stated and agreed, one call at a time, `take add`, listening, approved takes archived, `voice join`, offline `transcribe` and `lipsync` for scene timing with accepted files in `production/src/timing/`; espeak-ng only as a scratch track | moded |
<: if 'audiobook' in MEDIA_KINDS :>| `narrate-audiobook` | An audiobook, planned in its chapter register with its credits (its M2: an audiobook has no script), then chapter by chapter by the route each channel accepts (human, AI or external): text through `media.py audiobook text`, takes one call at a time, mastering and the ACX check through the toolkit, every approved master archived, disclosure always | moded |
<: endif :>| `captions` | Captions by four timing routes, aligned known words included; a recorded piece's transcript; speech-to-text only when asked; SRT and VTT to house limits; `captions check`; burned or sidecar per platform; published transcripts (M6); model fetch left to the author | none |
| `cut-for-platform` | Every render through the toolkit: the edit decision list and its cards, `assemble` to the master (M4), `cut` and `encode` per deliverable with captions burned in the same pass (web video, silent loops and a feed episode's untagged audio among them), loudness, and a probe of every output (M5); `feed tag` at M7 | none |

---

## 4. Companion skills from syntek-author

These are syntek-author's skills, and they never ship here. Media names each one unbackticked, in
one fixed form, 'the spelling skill (syntek-author), where present', never in `skills:`
frontmatter, and a skill checks for `.claude/skills/<skill>/SKILL.md` at run time before it names
the step. Where a companion is absent, say which skill is missing and what it would have checked;
never recreate it.

| Companion (syntek-author), where present | Applies to | How media uses it |
|---|---|---|
| spelling, grammar | scripts, transcripts, post copy, caption text | a supportive report; fixes applied only when accepted (a transcript's words are what was said: only a mis-transcription is fixed); part of M2 |
| comprehension | scripts | a report, read as the audience test (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 1) |
| flow | scripts | a report on order, rhythm and repetition across beats |
| fact-check | every factual claim in a script, transcript or post | verdicts; an unresolved claim stays `VERIFY`; M2 and M7 need none open |
| improve-section | a script the author drafted | report, then the agreed edits only; no ledger entry and no status change, said before it runs |
| adapt-section | a script revised from the author's notes | report, then the agreed edits only; no ledger entry; the revise step of `write-script` is the fallback |
| research | platform policies, the facts behind a script | as practice; sources and dates recorded where the guide says |
| grilling, grill-with-docs | the brief, the brand kit, the spoken voice, design decisions | as practice (`.claude/rules/syntek-media/06-global-rules.md` Section 8) |
| handoff | session boundaries | `.claude/rules/syntek-media/07-session-boundaries.md`; without it, the handoff is written by hand |
| wayfinder | a large series or a launch | as practice |
| social-media-documents | social media plans, content calendars, operating procedures, bios, channel voice, text-only posts | owns what each document sets for a platform where present, document by document; media's profiles, schedule and posts cite them, never duplicate them |
| run-workflow | — | a boundary only: writing work goes there, a blog post's or a newsletter issue's own words included |
| pronounce | — | never run by media; its IPA is the source for constructed names in `brand/src/voice/voice.md` |

The provenance ledger belongs to syntek-author's content layer, so improve-section and
adapt-section run on a script with no ledger step, and the revise step of `write-script` takes
over when a companion refuses a file that is not a section draft.

---

## 5. Working with skills

- **Read the whole `SKILL.md`, then its mode file if it carries the Mode paragraph, before
  step 1.** Each step ends with a completion test; a step is not done until its test passes.
- **Skills never edit themselves or each other** without the author's explicit instruction
  (`.claude/rules/syntek-media/06-global-rules.md` Section 3).
- **A project-specific change to how a skill behaves** is an entry in the Overrides of
  syntek-author's 00-project.md, where present, or a project rule
  (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10), never an edit of the skill.
- **A skill that spends credits** carries the call discipline of
  `.claude/rules/syntek-media/03-production-ethics.md` Section 4 in its own steps.
- **A skill of the author's own** goes in a new folder whose name collides with no media or
  syntek-author skill; its frontmatter `name` equals the folder, and Copier never touches it.

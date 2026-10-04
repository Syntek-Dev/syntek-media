# 01-layout-and-routing.md — the brand, where everything lives, and how work finds its folder

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

This file owns the brand brief and the shape of syntek-media's part of the repository: its
layers, the piece, the folder pair, routing frontmatter, who owns which files, the read order,
and which rule wins (Section 10). Every other media file that needs a path routes here.

---

## 1. The brand

**This is the brand brief**, rendered from `.copier-answers.syntek-media.yml` and replaced by every
update, so a re-answered name or list arrives here on its own. Where syntek-author was applied
first, `.claude/CLAUDE.md` is its file and never mentions the brand: every media session reads
the brand here.

- **Brand:** <%BRAND_NAME%>, in exactly this form on screen, in captions, credits and metadata;
  never shortened, expanded or re-punctuated.
- **Brand kind:** <%BRAND_KIND%> (its mode file: `.claude/rules/syntek-media/02-skills.md` Section 2).
- **What the channel is for:** <%BRAND_DESCRIPTION%>
- **Audience test** (every script is written for this person, and the comprehension skill
  (syntek-author), where present, reads as them): <%AUDIENCE_TEST%>
- **Owner:** <%OWNER_NAME%>, 'the author' in every media file; in chat, <%OWNER_FIRST_NAME%>.
- **Platforms:** <% PLATFORMS | join(', ') %>
- **Media kinds:** <% MEDIA_KINDS | join(', ') %>

The rest lives in the brand's own files (`brand/src/design-system/tokens.css`,
`brand/src/voice/voice.md`, `brand/src/platforms/`) and the running state in `.claude/MEMORY.md`.
The written voice and brand guide stay syntek-author's, where present, cited and never restated.

---

## 2. Layers

| Layer | Kind | Purpose |
|---|---|---|
| `.claude/` | config | The manual, these rules in `.claude/rules/syntek-media/`, `MEMORY.md`, settings, and media's skills beside any other template's |
| `brand/` | production | Design tokens and preview cards (the thumbnail and card layouts among them), design exports and their register, the spoken voice, one profile per platform |
| `scripts/` | production | One folder per piece: brief, script or transcript, storyboard, shot list; the piece register |
| `production/` | production | Source media and its manifest, voiceover segments, edit decision lists, cards, rights and credits<: if 'audiobook' in MEDIA_KINDS :>, audiobook chapter registers<: endif :> |
| `publishing/` | production | Cut-down plans, captions and published transcripts, thumbnails and other images, post packages, the schedule and the publish log<: if 'podcast' in PLATFORMS :>, and the show registers and feeds of a self-hosted podcast (`publishing/src/podcast/`)<: endif :> |
| `toolkit/` | supporting | `media.py` and `card.py`, the platform data and the fallback layouts; every render runs through it |

`run-media-workflow` reads the workflow indexes of these four production layers and no others.
The writing router of syntek-author, where present, reads only the layers its own rules list.

---

## 3. The kinds of layer

- **Production layers** hold content made through repeatable, multi-step procedures, so each
  splits into the same sublayers (Section 4).
- **The supporting layer**, `toolkit/`, is run, not produced inside; it stays flat
  (`.claude/rules/syntek-media/04-toolkit-pipeline.md`).
- **Generated output** (each renders and generated folder in `production/src/` and
  `publishing/src/`) is git-ignored by the nested `.gitignore` files, never hand-edited, and can
  be made again, except an approved take or audiobook master, which is archived as source media.
- **Media has no working folders of its own.** The handoffs, learning and assets folders at the
  root are syntek-author's, where it is applied; media's binaries live in its own layers.

---

## 4. Sublayers of a production layer

| Sublayer | Holds | Read it for |
|---|---|---|
| `docs/reference/` | Guides shipped by the template, replaced by `copier update` | how this kind of work is done |
| `docs/project/` | The author's own guides; a same-named file here overrides the reference guide | how this project departs |
| `src/` | The artefact: the prose, the plans, the evidence | the work itself |
| `workflows/NN-name/` | Template procedures: `CONTEXT.md` + `CLAUDE.md` + `STEPS.md` + `CHECKLIST.md` | the steps to follow |
| `workflows/local/NN-name/` | The author's procedures, in their own numbering; a same-slug folder overrides the template's | the author's steps |

Template workflow numbers are **frozen and append-only**, unique within a layer across every
brand kind, platform and media kind; gaps are deliberate. `run-media-workflow` checks the
Workflow aliases of syntek-author's 00-project.md first, where present, then `workflows/local/`,
and every skill that carries out a workflow runs the alias or same-slug local procedure instead.
**Cite a workflow by its full folder name** (`production/workflows/02-make-a-voiceover/`), never
by its number alone: a project may keep two folders with one number.

---

## 5. The piece

- **A piece** is one deliverable work: a short, an explainer, a talk, a trailer, a podcast
  episode, an audiobook or a standalone voiceover. It lives at
  `scripts/src/pieces/NNN-kebab-title/` (three digits, frozen, never reused; `000` is reserved
  for the worked example), and its name is the key every other media file uses.
- **Its folder** holds `brief.md`, `script.md` or `transcript.md`, `storyboard.md` and
  `shot-list.md`, and its own pair (Section 6). The brief holds the plan, `status` and `verified`.
- **A piece is scripted or recorded.** A recorded piece (a talk, an interview) comes in through
  `production/workflows/08-bring-in-a-recording/`; its approved transcript stands in for the
  script wherever a script is read, and its storyboard gate reads `n/a — recorded`.
- **The ladder** `idea · briefed · scripted · storyboarded · produced · cut · captioned ·
  scheduled · published` moves only through the gates of
  `scripts/docs/reference/the-piece-ladder.md`; the requirement that they bind is
  `.claude/rules/syntek-media/03-production-ethics.md` Section 3.
- **The register**, `scripts/src/piece-register.md`, holds numbers, kinds, origins, parents and
  retirements, never a status.

---

## 6. The folder pair

**Every directory carries a `CONTEXT.md` and a `CLAUDE.md`.** `CONTEXT.md` is orientation: what
is here and why, as a directory tree with `←` notes, then what's here and cross-references. It
would stay true if nobody worked here again. `CLAUDE.md` is operating rules: it opens with
`@./CONTEXT.md`, then a `Read order:` line naming every ancestor pair, then exactly four sections:
`## Purpose (one line)`, `## How to work here` (**Routing**, **Model**, **Concrete steps**,
**Definition of done**), `## Guardrails` and `## Output & naming`.

The exceptions are syntek-author's, unchanged, then media's:

- Every `build`, `.git`, `audio`, `__pycache__` and `node_modules` folder is generated; nothing in
  them is read for guidance.
- `.claude/rules/` holds rules only: Claude Code loads every Markdown file there at launch, so a
  `CONTEXT.md` placed there would load as a rule.
- The inside of each `.claude/skills/<skill>/` folder: a skill is its own manual.
- Each `drafts` and `.base` folder carries only a `README.md`; its parent's pair governs it.
- Each `generated`, `renders` and `raw` folder carries only a tracked `README.md`; everything else
  in it is git-ignored, and its parent's pair governs it.
- A handoffs folder these rules create without syntek-author carries no pair, and Claude never
  writes one there: its pair is syntek-author's, and one written here would collide with it.
- **Every piece folder carries its own pair**, written when the piece is opened
  (`scripts/workflows/01-brief-a-piece/`) from the skeleton in `scripts/src/pieces/CLAUDE.md`.

The repository root's operating file is `.claude/CLAUDE.md`, not a root `CLAUDE.md`.

---

## 7. Routing frontmatter

Guides and workflow files say which skill and model the work needs, in YAML frontmatter above the
H1. **Read it first and obey it.**

| File | Keys |
|---|---|
| Guide (`docs/**/*.md`) | `type: guide` · `skills: [..]` · `model:` |
| `STEPS.md` and `CHECKLIST.md` | `workflow:` · `phase:` · `skills: [..]` · `model:` |
| `CONTEXT.md` and `CLAUDE.md` | none: the pair is navigation, not routing |

The phase is one of plan, research, produce, review, publish, convert or author. The template's
files carry no `agent:` key: the template uses skills only. A `skills:` list names media skills
only; a companion from syntek-author is named in prose on a step, never there. Piece files and
registers carry no `model:` key (`.claude/rules/syntek-media/05-model-allocation.md`).

---

## 8. Who owns which files

| Class | What `copier update` does | Files |
|---|---|---|
| **Template-owned** | merges the template's changes in | `.claude/rules/syntek-media/**`, the media skills' folders, every `docs/reference/` and `workflows/NN-name/`, the governance pairs (except the seeded ones), `toolkit/**`, every nested `.gitignore` and `.gitattributes`, the READMEs of the generated, renders and raw folders, and Copier's `.copier-answers.syntek-media.yml` |
| **Seed-if-missing** | creates the file only if it is absent, then never touches it | the seeds below |
| **Copy-only shared** | written by a copy only where absent; never touched by an update, even to recreate it | the ten shared files below |
| **Seed-once example** | ships at generation only; once deleted, stays deleted | the worked example piece, when one was generated |
| **Author-owned** | never touches | everything you write: pieces, register rows, `docs/project/` guides, `workflows/local/` procedures, edit lists, cards, plans and packages |

**Seeds** (deleting one brings back the empty seed; a platform's profile goes with its
platform): the design register, `tokens.css` and the preview cards of `brand/src/`,
`brand/src/voice/voice.md`, the platform profiles and `overrides.toml` in
`brand/src/platforms/`, `scripts/src/piece-register.md`, `production/src/rights-register.md`,
`production/src/credits-log.md`, `production/src/footage/manifest.toml`,
`publishing/src/schedule.md`, `publishing/src/publish-log.md`, and every layer's `docs/project/`
and `workflows/local/` pair.

**The ten shared files** (`README.md`, `CONTEXT.md`, `.gitignore`, `.mcp.json`, and in `.claude/`
`CLAUDE.md`, `CONTEXT.md`, `MEMORY.md`, `settings.json` and the `skills/` pair) are written by
whichever template is applied first; nothing media needs lives only in them, and media never
edits one.

**Never edit a template-owned file.** Override instead: a same-named guide in `docs/project/`, a
same-slug workflow in `workflows/local/`, an entry in the Workflow aliases or Overrides of
syntek-author's 00-project.md, where present, or a project rule (Section 10).

---

## 9. Read order

1. `.claude/CLAUDE.md`: the project brief. It imports the root `CONTEXT.md`, and these rules load
   with it, this file's Section 1 among them (and syntek-author's rules, where present).
2. `.claude/MEMORY.md`, under the headings the Memory headings of syntek-author's 00-project.md
   map, where present.
3. Each ancestor folder's `CONTEXT.md` then `CLAUDE.md`, from the top down.
4. The target folder's `CONTEXT.md` (imported by its `CLAUDE.md`), then its `CLAUDE.md`.
5. The routing frontmatter of the file you are about to open (Section 7).

---

## 10. Project settings and precedence

**syntek-media ships no settings file.** Where syntek-author's project settings file,
00-project.md, is present, it outranks these rules as it outranks syntek-author's own, and Claude
reads it at run time, never through Copier: its Paths say where project rules and handoffs go;
its Memory headings map the headings of `.claude/MEMORY.md`; its Workflow aliases may name a
media workflow by full folder path, checked first; its Overrides may name a media rules file and
section, or a media skill and step. Where it is absent, project rules go in `.claude/CLAUDE.md`,
under the heading 'Project-specific rules'.

**Precedence**, highest first: (1) syntek-author's 00-project.md, where present; (2) the project
rules; (3) these rules files, beside syntek-author's own, where present; (4) a folder's
`CLAUDE.md`, which adds and never relaxes; then a skill; then its mode file, where the procedure
wins. Follow the higher rule, and report the conflict to the author with both locations.

**Living beside syntek-author.** These four production layers sit beside any that syntek-author
lists. `README.md`, the root `CONTEXT.md`, `.claude/CLAUDE.md` and `.claude/skills/CONTEXT.md`
may have been written by another template and not mention them: for media's layers, skills and
rules, this file is the authority.

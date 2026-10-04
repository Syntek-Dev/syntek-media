# CLAUDE.md — <%BRAND_NAME%>

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB) **Timezone**: <%TIMEZONE%>

@../CONTEXT.md

> Read this file first, then `.claude/MEMORY.md`, then the `CONTEXT.md` and `CLAUDE.md` of
> whichever folder you are about to work in — in that order — before editing anything. The
> template's rules in `.claude/rules/syntek-media/` load automatically with this file.

---

## 1. Project

<: if BRAND_KIND == 'business' :>**<%OWNER_NAME%>** makes the video and audio of **<%BRAND_NAME%>** in this repository: a
business's social video, recorded talks and explainers.
<: endif :><: if BRAND_KIND == 'author-fiction' :>**<%OWNER_NAME%>** makes the video and audio of **<%BRAND_NAME%>** in this repository: a
novelist's book trailers, audiobooks and author socials.
<: endif :><: if BRAND_KIND == 'author-nonfiction' :>**<%OWNER_NAME%>** makes the video and audio of **<%BRAND_NAME%>** in this repository: a
non-fiction author's talks, podcast, audiobooks and author socials.
<: endif :>
- **Brand:** <%BRAND_NAME%>
- **The brand's name** is used in exactly the form above on screen, in captions, credits, titles
  and metadata; never shorten, expand or re-punctuate it. In chat, address the owner as
  <%OWNER_FIRST_NAME%>.
- **Brand kind:** <%BRAND_KIND%>
- **What the channel is for:** <%BRAND_DESCRIPTION%>
- **Audience test** (every script is written for this person): <%AUDIENCE_TEST%>
- **Platforms:** <% PLATFORMS | join(', ') %>
- **Media kinds:** <% MEDIA_KINDS | join(', ') %>
- **Near-term goal:** not yet set. <!-- AUTHOR TO CONFIRM: the near-term goal and its date, such as a first published short, a trailer for a launch date or a first podcast episode. -->

This brief was written once, from the answers. The brand brief every session reads, kept current
by every update, is Section 1 of `.claude/rules/syntek-media/01-layout-and-routing.md`. Release
cadence, the next publish date and the running status live in `.claude/MEMORY.md`.

---

## 2. Where the rules live

The rules are the files `01-` to `08-` in `.claude/rules/syntek-media/`. Claude Code loads them
at launch, alongside this file, so there is no need to open them before working; open one when a
task turns on its subject.

| File | Owns |
|---|---|
| `.claude/rules/syntek-media/01-layout-and-routing.md` | the brand brief, the layers, the piece, the folder pair, routing frontmatter, ownership, read order, precedence |
| `.claude/rules/syntek-media/02-skills.md` | the media skill roster, the companions from syntek-author, and the mode-file contract |
| `.claude/rules/syntek-media/03-production-ethics.md` | who decides what, the production loop, the piece ladder, credits, AI disclosure, rights and consent, never fabricate, the two flags |
| `.claude/rules/syntek-media/04-toolkit-pipeline.md` | the toolkit, its commands and what it needs |
| `.claude/rules/syntek-media/05-model-allocation.md` | which model does which work |
| `.claude/rules/syntek-media/06-global-rules.md` | locale, route not restate, never self-edit, never overwrite, proofreading, confidentiality, answers, what Git ignores |
| `.claude/rules/syntek-media/07-session-boundaries.md` | hand off, never compact |
| `.claude/rules/syntek-media/08-naming-and-memory.md` | naming patterns, and what goes in `.claude/MEMORY.md` |

**They are template-owned; never edit one.** `copier update` replaces them, so an edit there is
lost or turned into a conflict. To add a rule of the project's own, write it under
'Project-specific rules' below; to change a guide or a procedure, add a same-named guide in a
layer's `docs/project/` or a same-slug workflow in its `workflows/local/`.

---

## 3. Project-specific rules

Add a rule as a bold-led bullet with its date and its reason. It applies to this project on top
of the template's rules files, and where the two conflict, this section wins. If syntek-author is
applied to this project later, its project settings file outranks this section and says where
project rules go.

_No project rules yet._

@./CONTEXT.md

# CLAUDE.md — publishing/src/posts/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/src/CONTEXT.md` → `publishing/src/CLAUDE.md` → this folder's
`CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold one approved post package per piece, so the author posts every deliverable from words, a
disclosure and files that were checked and agreed in advance.

## How to work here

- **Routing:** skill `prepare-post`, through `publishing/workflows/05-prepare-a-post/`; guides
  `publishing/docs/reference/posting-and-the-log.md`, `publishing/docs/reference/ai-disclosure.md`
  and the guide for each platform a section names.
- **Model:** **Opus** for every word a viewer reads and for each disclosure decision; the
  mechanical tier for counting characters against keys and filling render names
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the brief, the cut-down plan, the captions and the thumbnails → read
  the calendar entry, where syntek-author's is present → write one section per deliverable →
  count every limit against its key → proofread → the author approves → schedule rows.
- **Definition of done:** every deliverable of the brief and the cut-down plan has a section;
  every count sits inside its key; the disclosure follows `ai-disclosure.md`; the author has
  approved the package.

## Guardrails

- **Never post.** A package is handed to the author; the author posts.
- **Limits by key.** Every count names its `toolkit/data/platforms.toml` key; a `verify` key is
  flagged, and hashtags above `platform.instagram.hashtags_max` are warned about.
- **Media deliverables only.** A text-only post, a bio or a calendar entry belongs to the
  social-media-documents skill (syntek-author), where present; cite its calendar entry, never copy
  or rewrite it.
- **Never invent** a claim, a quotation, a statistic, a testimonial or a link; a factual claim in
  a description is checked like one in the script.
- **Never overwrite** an approved package without confirming with the author.

## Output & naming

- **Hand-written (with the author):** `<piece>.md`, in this shape:

```markdown
---
piece: NNN-kebab-title             # equals the piece's folder name
approved: ""                       # DD/MM/YYYY once the author approves the whole package
---

# <Title> — post package

## <platform>.<format>[ — cNN]

- **Title:** <as it will be pasted>
- **Description:** <a fenced block, one sentence per line, holding the description's words exactly, the disclosure line included; a blank line between paragraphs>
- **Hashtags:** <the set>
- **Disclosure:** <label and setting, and the rule it rests on> · <description line> · <spoken or on-screen line, or none>
- **Captions:** <caption file> · <burned or sidecar>
- **Thumbnail:** <render name, or n/a with the reason>
- **Render:** <render name>
- **Calendar:** <the content calendar entry, where syntek-author's is present; otherwise none>
- **Scheduled:** DD/MM/YYYY HH:MM, <%TIMEZONE%>
- **Limits:** <each count against its platforms.toml key>
```

- **Generated:** nothing here; renders are in `publishing/src/renders/`.

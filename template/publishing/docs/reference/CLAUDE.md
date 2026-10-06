@./CONTEXT.md

# CLAUDE.md — publishing/docs/reference/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/docs/CONTEXT.md` → `publishing/docs/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → the guide you need.

## Purpose (one line)

Serve the template's publishing guides read-only, so every project cuts, captions and posts the
same way until its author decides otherwise in `publishing/docs/project/`.

## How to work here

- **Routing:** check `publishing/docs/project/` for a same-named guide first; if one exists, it
  wins. Otherwise read the guide here that matches the task:
  - planning or cutting a short deliverable from a master → `cut-downs.md` (skills `repurpose`,
    `cut-for-platform`);
  - timing, checking or burning captions → `captions.md` (skill `captions`);
  - briefing or rendering a thumbnail or cover → `thumbnails.md` (skill `thumbnail-brief`);
  - deciding a post's AI label and disclosure lines → `ai-disclosure.md` (skill `prepare-post`);
  - writing a post package, scheduling it or logging an upload → `posting-and-the-log.md` (skill
    `prepare-post`);
<: if 'youtube' in PLATFORMS :>  - anything posted to YouTube → `youtube.md`;
<: endif :><: if 'tiktok' in PLATFORMS :>  - anything posted to TikTok → `tiktok.md`;
<: endif :><: if 'instagram' in PLATFORMS :>  - anything posted to Instagram → `instagram.md`;
<: endif :><: if 'linkedin' in PLATFORMS :>  - anything posted to LinkedIn → `linkedin.md`;
<: endif :><: if 'facebook' in PLATFORMS :>  - anything posted to Facebook → `facebook.md`;
<: endif :><: if 'podcast' in PLATFORMS :>  - anything sent to Apple Podcasts or Spotify → `podcast.md`, and a show the brand serves
    itself, its register and its feed → `podcast-feed.md`;
<: endif :><: if 'website' in PLATFORMS :>  - anything placed on one of the brand's sites → `website.md`;
<: endif :><: if 'blog' in PLATFORMS :>  - anything placed in a blog post → `blog.md`;
<: endif :><: if 'newsletter' in PLATFORMS :>  - anything shown in a newsletter issue → `newsletter.md`;
<: endif :>  - scoring title–thumbnail options → `scoring-options.md`;
  - reading or correcting a platform limit → `platform-specs.md`.
- **Model:** **Opus** for reading a guide into a judgement; nothing here is written
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the guide → read the rules section it names at its foot → read the
  `platforms.toml` keys it cites with `python3 toolkit/media.py presets KEY` → apply it through the
  workflow it names → if the practice does not fit this project, propose a project guide to the
  author rather than bending the reference one.
- **Definition of done:** the guide's practice was applied through its workflow, and any point
  where it did not fit has been reported to the author rather than improvised around.

## Guardrails

- **Read-only.** These files are template-owned and updated by `copier update`. To change one for
  this project, copy it to `publishing/docs/project/` under the same name and edit the copy, with
  the author's instruction.
- **A limit is read, never remembered.** Every platform guide cites keys; the value is whatever
  `media.py presets` prints today, overrides applied. A `verify` key is unconfirmed, and is
  flagged wherever it is relied on.
- **A guide never outranks the rules.** Where a guide and the rules file it names disagree, the
  rules file wins; report the disagreement.

## Output & naming

- **Template-owned:** every guide here, and this pair. Nothing in this folder is generated or
  written by a skill.
- **Hand-written by the author:** nothing here; project guides go in `publishing/docs/project/`.

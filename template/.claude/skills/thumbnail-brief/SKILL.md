---
name: thumbnail-brief
description: >-
  Brief, lay out and render the thumbnails, covers and other images of one piece, one per cut where
  a cut needs its own: agree the promise and the few words on the image, copy the brand's thumbnail
  layout, set the words and a tracked image, render it with card.py at each deliverable's size (the
  video's, flagged VERIFY, where a platform publishes none), and encode posters, share, featured and
  newsletter images and the GIF preview with media.py. Checks legibility at small size, the safe
  zone and the grid crop of platform.instagram.grid_aspect. Never edits the brand's layout or
  tokens. Use when the author says 'make a thumbnail for the explainer', 'brief the cover for this
  reel', 'we need episode art', 'a poster for the website video', 'make the newsletter GIF' or 'will
  the title survive the grid?'. Not the title, description or hashtags (`prepare-post`). Not a card
  inside the video (`cut-for-platform`).
---

# Skill: Thumbnail Brief (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

A thumbnail is a promise made at the size of a fingernail. This skill writes that promise down as
a brief, lays it out from the brand's own thumbnail component, and renders it at every size the
piece's platforms ask for, so the image a viewer judges the piece by is chosen on purpose and
checked where it will be seen. **The image promises only what the piece delivers**: a thumbnail
that oversells costs the viewer's trust in every piece after it.

The layout is the brand's, `brand/src/design-system/previews/thumbnail.html`, kept in step with
the brand's Claude Design project. It is copied once per thumbnail, so a layout change synced into
the brand reaches every later piece and never rewrites an approved one. This skill edits the copy
only, never the brand's component and never `tokens.css`; <%OWNER_FIRST_NAME%> approves every
thumbnail before it is used.

## Governing procedures (route here — do not restate at length)

- `publishing/workflows/04-brief-a-thumbnail/` — this skill is that procedure in skill form. Run
  its `STEPS.md` with `CHECKLIST.md` open.
- If the layer's `workflows/local/` holds a folder with the same `NN-name` as the procedure above,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `publishing/docs/reference/thumbnails.md` — what a thumbnail and a cover must do, thumbnails per
  cut, platforms with no thumbnail table, and a piece's other images: posters, share, featured and
  preview images and the GIF preview (each channel's keys in its own guide, where it ships).
- `brand/docs/reference/the-brand-kit.md` — the tokens, the required tokens, the fonts, and the
  two layout components the pieces copy.
- `publishing/src/thumbnails/CLAUDE.md` — the brief's format, and the names of a brief and its
  layout.
- `publishing/docs/reference/platform-specs.md` — how `toolkit/data/platforms.toml` is read:
  `verify`, absent keys and the brand's overrides.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` Sections 2 and 3 — `card.py`, and renders
  that are generated, regenerable and never hand-edited.
- `.claude/rules/syntek-media/03-production-ethics.md` Sections 5 and 6 — AI disclosure, and
  rights and consent for every image and likeness.

The mode file adds what this brand kind's thumbnails promise, the images it may use, and the words
it never puts on one.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Fix the piece and what needs a thumbnail.** Confirm the piece and read its `brief.md`
   (`deliverables`, `ai_visuals`, `rights`) and its cut-down plan,
   `publishing/src/cut-downs/<piece>.md`, where it has one. A cut whose note says it needs its own
   thumbnail gets its own brief, `<piece>--cNN`; the rest share the piece's. For each brief, list
   the thumbnail or cover deliverables it serves from the platforms' tables in
   `toolkit/data/platforms.toml`; a platform with no thumbnail table takes its video deliverable's
   key, and that render is flagged `VERIFY`. **Every other image of the piece is this skill's
   too**: a poster for each self-hosted video, a share image, a blog's featured image, a
   newsletter's preview image or GIF preview, for each placement the brief or the post package
   names on the brand's own sites, blogs and newsletters. A show's cover is never a piece's: it is
   a design export (`brand/workflows/03-record-a-design-export/`). Where a brief or layout already
   exists, this is a revision: never overwrite it without the author's word.
   *Complete when:* every brief to write is named with its deliverables, and every existing file
   is named.

2. **Read the deliverables.** Print each with
   `python3 toolkit/media.py presets <platform>.<format>`: its `width`, `height`, `aspect`,
   `formats`, `max_size`, `safe_zone`, `notes` and every key in its `verify` list. Some art
   takes no words at all, and its `notes` say so. For a reel cover, read
   `platform.instagram.grid_aspect` too, a `verify` key: the profile grid shows only that centre
   crop. Read each platform's guide in `publishing/docs/reference/`. Never take a size from
   memory.
   *Complete when:* every deliverable's size, formats, safe zone and notes are listed, with each
   `verify` key named.

3. **Read the brand kit.** Read `brand/src/design-system/tokens.css` and the brand's layout,
   `brand/src/design-system/previews/thumbnail.html`; where it is absent,
   `toolkit/templates/thumbnail.html` is the fallback, and say so. Run
   `uv run toolkit/card.py check` on the layout you will copy. A layout still carrying
   `AUTHOR TO CONFIRM` slots, or failing its check, is the brand kit's to fix
   (`brand/workflows/01-set-up-the-brand-kit/`): report it, and go on only if the author says to.
   *Complete when:* the layout to copy is named, and its check has passed or its failures are
   reported.

4. **Agree the brief.** Propose, for each brief, the five parts its format gives:
   `## Promise` (what the viewer gets, in one sentence the piece keeps), `## Words on the image`
   (the fewest words that carry the promise, adding to the title rather than repeating it),
   `## Image` (what is shown and where it comes from, with every moment taken from a render: each
   poster's `--at` on its video's render, the GIF's In and Out on the master and what its first
   frame shows), `## Variants` (only those the author asks for) and `## Checks` (filled at
   step 8). Wait for the author's answer, then write `publishing/src/thumbnails/<piece>[--cNN].md`
   with its frontmatter, `approved` left empty.
   *Complete when:* each brief is written as the author agreed it, one sentence per line.

5. **Choose and place the image.** Take a still from the master where the brief asks for one
   (`python3 toolkit/media.py frame <master> --at <HH:MM:SS.mmm>`), or use an asset the author
   names. With the author's agreement, copy each still a layout uses into
   `production/src/assets/`: a still left in a renders folder is git-ignored, and a layout must
   rebuild from tracked files. A person who can be recognised needs a `likeness` row in
   `production/src/rights-register.md`, and licensed art or stock its own row. An AI-generated or
   AI-assisted image is recorded in the brief's `ai_visuals`, and the author is told it changes
   the piece's disclosure.
   *Complete when:* every image the layout uses is a tracked file, with a rights row where it needs
   one, and any AI image is recorded in the brief.

6. **Copy the layout and set it.** Copy the layout named at step 3 to
   `publishing/src/thumbnails/<piece>[--cNN].html`. Fix every relative path in the copy, the
   tokens link first, so that from `publishing/src/thumbnails/` it reaches
   `brand/src/design-system/tokens.css`, and point each image at its tracked file. Delete the
   brand layout's own `AUTHOR TO CONFIRM` line from the copy: the brand file keeps it, and
   `media.py flags` reports it there rather than against the piece. Set the words and the image
   the brief agreed, keep every word inside the `--safe-*` variables, and load nothing over the
   network. For a `newsletter.*` key, the copy needs the play-button hook (an element carrying
   `data-play-button`): where the brand's layout predates it, add the element and its rules from
   `toolkit/templates/thumbnail.html` to the copy, and tell the author the brand's layout lacks it.
   Change the copy only.
   *Complete when:* the copy links the brand's tokens, uses only tracked images, carries the
   brief's words, and nothing outside the copy changed.

7. **Check and render.** Run `uv run toolkit/card.py check` on the copy and fix what it reports,
   in the copy. Then render each deliverable with
   `uv run toolkit/card.py render <html> --deliverable <platform>.<format>`, passing `-o` with its
   name in `publishing/src/renders/<piece>/` (a cut's brief too, never a folder of its own),
   `<html-stem>.<platform>-<format>.png`. A deliverable whose table has no `width` and `height`
   renders with `--size` at a size the author agrees, flagged `VERIFY`. If `card.py` exits 2 (no
   uv, or no Chromium), report the install line it prints and stop: never report a thumbnail as
   rendered when it could not run. Then make every other file through the toolkit, never ffmpeg
   by hand: each format a table lists beyond PNG with
   `python3 toolkit/media.py image <png> --deliverable KEY [--format FMT]`; each poster with
   `media.py image <video render> --deliverable KEY --at TC`, no layout needed; the GIF preview by
   rendering the layout's overlay with
   `card.py render <html> --deliverable newsletter.preview_gif --transparent -o <png>`, then
   `media.py cut <master> --deliverable newsletter.preview_gif --in TC --out TC --overlay <png>`,
   towards M7 and never at M5. An exit 1 names what failed (a size, `max_size`, a range over
   `max_seconds`): fix it at its source.
   *Complete when:* every deliverable has its files, or the run has stopped and named what is
   missing.

8. **Look at every render.** Open each PNG and judge it as a viewer will: scaled down to the size
   the platform shows it in a feed or a search list, the words still read; every word and face
   sits inside the safe zone; on a reel cover, the title sits inside the centre crop of
   `platform.instagram.grid_aspect`; the file meets the deliverable's `formats` and `max_size`,
   which `media.py image` verified. A newsletter preview's first frame carries the play button
   and the words, and survives a dark background; a GIF plays within its `max_seconds`. Write each
   result, each `VERIFY` flag and each rights row into the brief's `## Checks`.
   *Complete when:* `## Checks` records every check for every render, with its result.

9. **Approve and hand back.** Show the author every render and apply only the edits they agree,
   rendering again after each. On the author's word, date `approved` in the brief. Report the
   briefs, layouts and renders by path, every open `VERIFY` flag and rights row, and the next move:
   the post package names each approved render (`prepare-post`).
   *Complete when:* the author has the report, and `approved` is dated only where the author
   approved.

## Anti-patterns

- **A promise the piece does not keep.** A face, a result or a question the piece never answers
  spends the viewer's trust in every later piece.
- **Editing the brand's component or tokens from here.** A layout change goes through the brand
  workflows, so every later piece gets it on purpose.
- **An image that lives only in a renders folder.** It is git-ignored; a layout that points at it
  cannot be rebuilt.
- **Judging at full size.** A thumbnail is read small; one checked only at its upload size has not
  been checked.
- **A size from memory.** Every size, aspect and crop comes from `media.py presets`; a platform
  with no thumbnail table is flagged `VERIFY`, never guessed silently.
- **A recognisable face with no rights row.** Every likeness, licensed image and piece of artwork
  has its row before the thumbnail is approved.
- **Words on art that takes none.** Where a deliverable's `notes` ask for no text, the image
  carries none.
- **Hand-editing a render.** A PNG is made again from its layout; every fix goes in the HTML.
- **Running ffmpeg by hand** for a JPEG, WebP, AVIF, poster or GIF: `media.py image` and
  `media.py cut` verify what they write.
- **A GIF whose message is not on its first frame.** Some email clients show nothing else.

## Cross-references

- `prepare-post` — names each approved render in the post package.
- `repurpose` — the cut-down plan, which says which cuts need their own thumbnail.
- `cut-for-platform` — title and end cards inside the video, from the brand's card component.
- `brand/src/design-system/previews/thumbnail.html` — the brand's layout;
  `toolkit/templates/thumbnail.html` where it is absent.
- `brand/workflows/02-sync-with-claude-design/` — how a change to the brand's layout arrives from
  Claude Design.
- `production/src/rights-register.md` — likeness, artwork, font and stock rows.
- syntek-author's brand guide, where present (by default standards/brand/brand-guide.md) — the
  brand's visual rules in words; a disagreement with `tokens.css` is reported, never resolved here.

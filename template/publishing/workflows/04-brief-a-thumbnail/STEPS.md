---
workflow: 04-brief-a-thumbnail
phase: publish
skills: [thumbnail-brief]
model: opus
---

# STEPS.md — brief, lay out and render a thumbnail

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for a piece's thumbnails, covers and other images (posters, share,
featured and preview images, and a GIF preview), from the promise in words to files the author
has approved. Each step names the skill and guide it uses, and the command it runs. **Run
in order** — the ordering is load-bearing — and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`), then
> `publishing/docs/reference/thumbnails.md`. The `thumbnail-brief` skill is this procedure in
> skill form; read it, and its mode file, before step 1.

## 1. Confirm the piece and its deliverables

> **Skill:** `thumbnail-brief` · **Guide:** `publishing/docs/reference/thumbnails.md`

Read the brief's deliverables and the cut-down plan's notes, which say which cuts need their own
thumbnail, and the post package or the brief for each placement on the brand's own sites,
blogs and newsletters: each needs its poster, share, featured or preview image, or its GIF. Read
an existing brief in `publishing/src/thumbnails/` before starting another; a second brief for the
same piece and cut is a revision, never a new file. _Mechanical._

## 2. Decide which deliverables take a thumbnail

> **Skill:** `thumbnail-brief` · **Guide:** `publishing/docs/reference/platform-specs.md`

For each platform, run `python3 toolkit/media.py presets` and find its thumbnail, cover and
other image tables (`kind = "image"`), and each table's `formats`. A table with no pixel size (its
`verify` names `width` and `height`) needs a size the author confirms; a platform with no
thumbnail table takes its video deliverable's size. Both are flagged `VERIFY` in the brief. A
poster needs no layout: it is a frame of its own video's render. _Substantive._

## 3. Brief it in words

> **Skill:** `thumbnail-brief` · **Guide:** `publishing/docs/reference/thumbnails.md`

With the author, write the promise in one sentence, the words on the image (as few as carry it,
never the title repeated), the image, and any variant with its reason, in the brief's skeleton
(`publishing/src/thumbnails/CLAUDE.md`). The mode file says what a promise is for this brand.
**No layout is touched until the promise is agreed.** _Substantive._

## 4. Copy the brand's layout

> **Skill:** `thumbnail-brief` · **Guide:** `brand/docs/reference/the-brand-kit.md`

Copy `brand/src/design-system/previews/thumbnail.html` (or `toolkit/templates/thumbnail.html`
where the brand has none) to `publishing/src/thumbnails/<piece>[--cNN].html`, and fix its
stylesheet link so it reaches the brand's `tokens.css` by relative path. Delete from the copy the
brand layout's own `AUTHOR TO CONFIRM` line about the brand's layout: the brand file keeps it and
`media.py flags` reports it there, so it never counts against the piece at M7. For a
`newsletter.*` key, check the copy for the play-button hook (an element carrying
`data-play-button`); where the brand's layout predates it, add the element and its rules from
`toolkit/templates/thumbnail.html` to the copy and tell the author the brand's layout lacks it.
Never edit the brand's file. _Mechanical._

## 5. Fill the layout

> **Skill:** `thumbnail-brief` · **Guide:** `publishing/docs/reference/thumbnails.md`

Put the agreed words in, and the image by relative path. A frame of the master is taken with
`python3 toolkit/media.py frame <master> --at HH:MM:SS.mmm -o <path>` and kept as a small
committed still in `production/src/assets/`, because a render is ignored by Git and would leave
the layout broken on a fresh checkout. Keep every word inside the `--safe-*` variables.
_Substantive._

## 6. Check the layout

> **Skill:** `thumbnail-brief` · **Guide:** `brand/docs/reference/the-brand-kit.md`

Run `uv run toolkit/card.py check publishing/src/thumbnails/<piece>.html` (with `--cNN` in the
name for a cut): the tokens are linked, every required token resolves, the brand's fonts load.
Fix every finding before rendering. _Mechanical._

## 7. Render each deliverable

> **Skill:** `thumbnail-brief` · **Guide:** `publishing/docs/reference/thumbnails.md`

For each deliverable, run `uv run toolkit/card.py render <html> --deliverable KEY -o <png>`, or
`--size WxH` for a size the author confirmed in step 2, writing
`publishing/src/renders/<piece>/<html-stem>.<platform>-<format>.png`, in the piece's own folder.
Exit 2 names a missing uv or Chromium, with its install command: report it, and stop.
_Mechanical._

## 8. Make the posters, the other formats and the GIF

> **Skill:** `thumbnail-brief` · **Guide:** `publishing/docs/reference/thumbnails.md`

Every format a table lists beyond PNG, and every poster, goes through the toolkit, never ffmpeg by
hand:

```bash
python3 toolkit/media.py image <png> --deliverable KEY [--format webp]
python3 toolkit/media.py image <video render> --deliverable KEY --at HH:MM:SS.mmm
uv run toolkit/card.py render <html> --deliverable newsletter.preview_gif --transparent -o <overlay png>
python3 toolkit/media.py cut <master> --deliverable newsletter.preview_gif --in <In> --out <Out> --overlay <overlay png>
```

Each file lands beside the PNGs in `publishing/src/renders/<piece>/`; name the overlay's PNG
there too with `-o`. Record each poster's `--at`, and the GIF's In and Out on the master with
what its first frame shows, under `## Image`, so a remade file equals the approved one. Exit 1
names what failed (a size, `max_size`, a range over `max_seconds`): fix it at its source.
_Mechanical._

## 9. Check it at thumbnail size

> **Skill:** `thumbnail-brief` · **Guide:** `publishing/docs/reference/thumbnails.md`

Look at every PNG at a fingertip's width. Check the words read; nothing sits under the platform's
controls; where Instagram shows it, the title sits inside `platform.instagram.grid_aspect`; the
table's `notes` are met; and every face, stock image or font that needs one has a `cleared` row in
`production/src/rights-register.md`. Record each result under `## Checks`. _Substantive._

## 10. Have the author approve it

> **Skill:** `thumbnail-brief` · **Guide:** `publishing/docs/reference/thumbnails.md`

Show the author every image at the size it will be seen, the GIF playing, with the checks. On approval, date
`approved` in the brief; on a change, go back to the step it touches. A variant the author does
not choose is recorded as declined under `## Variants`. _Substantive._

## 11. Hand back

> **Skill:** `thumbnail-brief` · **Guide:** `publishing/docs/reference/thumbnails.md`

Report each render and its deliverable, every size flagged `VERIFY`, any rights row still open,
and what M7 still needs. Point at `publishing/workflows/05-prepare-a-post/`. _Substantive._

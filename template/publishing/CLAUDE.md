@./CONTEXT.md

# CLAUDE.md — publishing/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → this folder's `CONTEXT.md` (imported
above) → this file → the procedure in `publishing/workflows/` that matches the task.

## Purpose (one line)

Turn an approved master into checked platform deliverables and approved post packages, and keep a
true record of what the author scheduled and posted, without ever posting anything.

## How to work here

- **Routing:** start from the matching procedure in `publishing/workflows/` (an author procedure
  in `publishing/workflows/local/` wins; `run-media-workflow` resolves it). Skills: `repurpose`
  plans the cut-downs; `cut-for-platform` renders every deliverable through the toolkit;
  `captions` times, checks and burns captions and makes published transcripts; `thumbnail-brief`
  briefs and renders thumbnails, covers and every other image; `prepare-post` writes the post
  package and the schedule row (a placement's too) and, once the author has posted, the log row.
- **Model:** **Opus** for every judgement a viewer or listener will meet: which moments to cut,
  what a caption, a title or a thumbnail says, the disclosure decision. The mechanical tier for
  renders, schedule dates, log rows and checklist ticks
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Read the piece's brief (`scripts/src/pieces/<piece>/brief.md`) for its `status`, its
     deliverables and its disclosure plan; never work from memory of an earlier session.
  2. Read the guide for each platform a deliverable goes to, in `publishing/docs/reference/`.
  3. Run the procedure; output lands in `publishing/src/`, renders in the piece's own
     `publishing/src/renders/<piece>/`.
  4. Record the gate the procedure passed in the brief, and hand back.
- **Definition of done:** every deliverable the brief and the cut-down plan name is rendered,
  verified and seen by the author; its captions and thumbnail are approved; its post package is
  approved and inside every limit; the schedule and the log match what the author did; nothing was
  posted.

## Guardrails

- **The author posts.** No skill posts, uploads, sends an email, edits a website's code or calls
  a platform's API. The log records what the author reports, in the author's words, and nothing
  else.
- **Platform numbers come from `toolkit/data/platforms.toml`,** by key, with the brand's
  confirmed corrections in `brand/src/platforms/overrides.toml`. Never write a limit from memory
  into a plan, a package or a guide.
- **Disclose by the rule.** Set each platform's AI label exactly when its current rule requires
  it, and always add the description line (`publishing/docs/reference/ai-disclosure.md`).
- **Renders are generated.** Never hand-edit one, never commit one and never force one past
  `publishing/src/.gitignore`; remake it from its sources.
- **Rights before posting.** A deliverable that uses anything not `cleared` in
  `production/src/rights-register.md` is not scheduled.
- **Where syntek-author's content calendar is present, it owns the plan.** The schedule lists
  media deliverables only and cites the calendar entry; the calendar, bios and text-only posts
  belong to the social-media-documents skill (syntek-author), where present, and a blog post's or
  a newsletter issue's words to the writing router of syntek-author, where present.
- **Confirm before overwriting** a plan, a caption file, a thumbnail layout, a post package, a
  schedule row or a log row.

## Output & naming

- **Hand-written (with the author):** everything in `src/` except `src/renders/`; the files and
  their names are listed in `publishing/src/CONTEXT.md`.
- **Generated (never hand-edit):** deliverables, burned versions, thumbnail PNGs and every other
  image, GIF and chapters file, in the piece's own `publishing/src/renders/<piece>/`, and what no
  piece owns, such as a feed's upload copy, at the top of `publishing/src/renders/`; all made by
  `python3 toolkit/media.py` and `uv run toolkit/card.py`.
- **Not here:** the master and its edit decision list (`production/`), the brief and the script
  (`scripts/`), the brand's layouts and platform profiles (`brand/`).

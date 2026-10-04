# CONTEXT.md — publishing/workflows/05-prepare-a-post/

The procedure for a piece's post package and its schedule: one section per deliverable, holding
the words the author will paste, the disclosure the platform's rule and the house's line require,
the caption file, the thumbnail and the render, with every count checked against its key, the
rights checked and every flag cleared. Once the author has approved the whole package, each
deliverable gets its schedule row, and the piece moves from captioned to scheduled. It never
posts: the author does, and `publishing/workflows/06-record-a-publication/` records what happened.

## Directory Tree

```text
publishing/workflows/05-prepare-a-post/
├── CONTEXT.md        ← this file: when to use it, what it produces
├── CLAUDE.md         ← how to run it; guardrails
├── STEPS.md          ← the ordered procedure
└── CHECKLIST.md      ← tick as you go; model-tagged
```

## When to use this

- A piece is captioned (or its M6 is `n/a`), its deliverables are rendered and checked, and its
  thumbnails are approved where a platform takes one.
- A package needs revising before the author posts it.
- A new deliverable joins a piece already scheduled, such as a cut added to the plan.

Reach for a **different** procedure when the task is a text-only post, a bio or the content
calendar (the social-media-documents skill (syntek-author), where present), a blog post's or a
newsletter issue's own words (the writing router of syntek-author, where present), a feed
episode's register, tags and feed (the podcast-feed workflow, where the project serves its own
podcast feed, which runs beside this one), recording a post the
author has made (`publishing/workflows/06-record-a-publication/`), or the platform's own account
details (`brand/workflows/04-set-up-a-platform/`).

## What it produces, and where

- **A post package** at `publishing/src/posts/<piece>.md`, approved by the author, with a section
  per deliverable and per placement on the brand's own sites, blogs and newsletters.
- **Schedule rows** in `publishing/src/schedule.md`, one per deliverable and per placement.
- **The gate** in the brief: `status: scheduled` and M7 dated in `verified`.

## The failure this procedure exists to prevent

A post that goes out with its description cut off mid-sentence, hashtags the platform ignores, an
AI label set where the rule did not ask (misleading viewers about what is synthetic) or missing
where it did (risking the post), a licensed track not yet cleared, or a `VERIFY` flag left in the
words. Every one is cheap to catch in a package and expensive to put right once posted.

## Cross-references

- `publishing/docs/reference/posting-and-the-log.md` — the package, the schedule and the log.
- `publishing/docs/reference/ai-disclosure.md` — each platform's rule for its label.
- `.claude/skills/prepare-post/SKILL.md` — this procedure in skill form.
- `publishing/src/posts/CLAUDE.md` — the package's skeleton.

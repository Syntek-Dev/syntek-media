# CONTEXT.md — brand/workflows/04-set-up-a-platform/

The procedure for filling one platform profile with the author: the account (or, for the brand's
own sites, blogs and newsletters, one row per site or list with its agreement), the deliverables
the brand uses there, and, where no written-side document sets them, its cadence, tone, call to
action and hashtag sets. Where syntek-author's social-media documents are present, whichever sets
a value for the platform owns it, and the profile cites it. A difference the author has confirmed between
the platform data and what the platform says today becomes an override, never an edit to the
data. The procedure never posts, and never calls a platform.

## Directory Tree

```text
brand/workflows/04-set-up-a-platform/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- A platform was chosen when the project was generated, or added since, and its profile is
  still a seeded stub.
- The account, the deliverables used or the brand's choices on a platform change.
- The author has confirmed that a platform now says something different from the platform data.

Reach for a **different** procedure when the job is the written social plan, a content calendar,
bios or a text-only post (the social-media-documents skill (syntek-author), where present),
re-checking the platform data's sources (`publishing/workflows/07-refresh-the-platform-specs/`),
or preparing one piece's post (`publishing/workflows/05-prepare-a-post/`).

## What it produces, and where

- **The profile**, `brand/src/platforms/<platform>.md`, its account and deliverables filled and
  every other section filled or citing the social media plan, its flags cleared.
- **An `[[override]]` table** in `brand/src/platforms/overrides.toml` for each confirmed
  correction, with the platform's words, the source and the date.
- **Dated decisions** in `.claude/MEMORY.md`.

## The failure this procedure exists to prevent

Two sources for one decision. A profile that restates a social media plan's cadence or hashtags
drifts from it within weeks, and the posts follow whichever was read last; a limit typed into a
profile, or edited into the template's platform data, is silently undone by the next update or
outlives the platform's own change. The profile holds only what the brand decides and nothing
else owns; the plan and the data keep theirs.

## Cross-references

- `brand/docs/reference/platform-profiles.md` — what a profile holds, overrides, the
  social-media family.
- `publishing/docs/reference/platform-specs.md` — how the platform data is read.
- `brand/src/platforms/` — the profiles and `overrides.toml`.

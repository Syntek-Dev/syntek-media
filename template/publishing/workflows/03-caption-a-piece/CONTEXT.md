# CONTEXT.md — publishing/workflows/03-caption-a-piece/

The procedure for captioning every deliverable of a piece that has speech and picture: choosing a
timing route, making each SRT with the toolkit from the script's or the approved transcript's own
words, rewrapping it where a deliverable needs its own width, checking it against its source, and
then burning it in or attaching it, as each platform takes it. When every deliverable that needs
captions has them, checked, the piece moves from cut to captioned. Captions can be made before the
cut, so that `publishing/workflows/02-cut-for-a-platform/` burns them in its one pass; a
recording's own captions are made when it is brought in, by
`production/workflows/08-bring-in-a-recording/`.

## Directory Tree

```text
publishing/workflows/03-caption-a-piece/
├── CONTEXT.md        ← this file: when to use it, what it produces
├── CLAUDE.md         ← how to run it; guardrails
├── STEPS.md          ← the ordered procedure
└── CHECKLIST.md      ← tick as you go; model-tagged
```

## When to use this

- A piece is `cut` and a deliverable with speech and picture has no checked captions.
- Before cutting, to make each cut's captions so the cutting pass burns them in.
- A caption file failed its check, the script or transcript changed, or a cut was retimed.

Reach for a **different** procedure when the task is a recording's transcript or its
recording-timed captions (`production/workflows/08-bring-in-a-recording/`), or rendering the
deliverables themselves (`publishing/workflows/02-cut-for-a-platform/`).

## What it produces, and where

- **Caption files** in `publishing/src/captions/`, named for what each is timed to, each passing
  its check against the script or transcript.
- **Burned deliverables** in `publishing/src/renders/`, where a platform takes no sidecar.
- **The gate** in the brief: `status: captioned` and M6 dated in `verified`, or M6 recorded
  `n/a` with its reason.

## The failure this procedure exists to prevent

Captions that drift a beat behind the speech, break a name across two lines, run faster than
anyone can read, or put words in a speaker's mouth; or a deliverable posted bare because its
platform took no sidecar and nobody burned one in. Making every file from the script's own words,
checking it against them, and deciding per platform what is burned prevents all of them.

## Cross-references

- `publishing/docs/reference/captions.md` — house limits, names, the three timing routes, burned
  or sidecar.
- `production/docs/reference/recorded-pieces.md` — a recorded piece's transcript and its anchors.
- `.claude/skills/captions/SKILL.md` — the skill that runs every caption command.
- `publishing/src/captions/CONTEXT.md` — which file is timed to what.

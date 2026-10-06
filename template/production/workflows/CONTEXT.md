# CONTEXT.md — production/workflows/

The production layer's ordered procedures: one per kind of production job, each a folder of four
files (`CONTEXT.md`, `CLAUDE.md`, `STEPS.md`, `CHECKLIST.md`). Numbers are frozen and never
reused, so gaps are normal; which procedures ship depends on the media kinds chosen when the
project was generated. The author's own procedures live in `production/workflows/local/`.
**Never make a master from memory or by hand.** Start here.

## Directory Tree

```text
production/workflows/
├── CONTEXT.md                      ← this file
├── CLAUDE.md                       ← operating rules and the 'You want to…' index
├── 01-log-source-media/            ← a source file logged, hashed, located and verified
├── 02-make-a-voiceover/            ← a take for each spoken sentence, on the author's request only
├── 03-assemble-the-master/         ← the edit decision list, the cards and the master, watched through
<: if 'podcast' in MEDIA_KINDS :>├── 04-master-a-podcast-episode/    ← an episode's audio master, cut from a recording under a bed
<: endif :><: if 'audiobook' in MEDIA_KINDS :>├── 05-narrate-an-audiobook/        ← the plan approved (M2), chapters voiced or recorded per channel
├── 06-master-an-audiobook/         ← chapters mastered, checked to the ACX targets and packaged
<: endif :>├── 07-clear-the-rights/            ← every licence, release and consent a piece uses, cleared
├── 08-bring-in-a-recording/        ← a recording logged, transcribed, anchored and approved
├── 09-time-the-voice/             ← approved words and mouth timing, boards re-timed before animation
└── local/                          ← your own procedures; a same-slug folder here wins
```

Each procedure folder holds:

```text
NN-verb-first-name/
├── CHECKLIST.md        ← model-tagged checklist: Pre-Conditions, Execution Checklist, Done When
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← when to use it, what it produces, the failure it exists to prevent
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## What's here

- `production/workflows/01-log-source-media/`, `production/workflows/02-make-a-voiceover/`,
  `production/workflows/03-assemble-the-master/`, `production/workflows/07-clear-the-rights/`,
  `production/workflows/08-bring-in-a-recording/`, `production/workflows/09-time-the-voice/` — for every project.
<: if 'podcast' in MEDIA_KINDS :>- `production/workflows/04-master-a-podcast-episode/` — podcast episodes.
<: endif :><: if 'audiobook' in MEDIA_KINDS :>- `production/workflows/05-narrate-an-audiobook/`, `production/workflows/06-master-an-audiobook/` —
  audiobooks.
<: endif :>- `production/workflows/local/` — **author-owned**; the template ships only its pair.
- **Four files per procedure**, always, and **numbers are frozen and append-only**, unique
  across every brand kind and media kind, so a gap is a procedure this project does not ship,
  not a missing one.

## Cross-references

- `.claude/rules/syntek-media/01-layout-and-routing.md` — routing frontmatter, frozen numbering
  and the local override rule.
- `production/docs/reference/` — the guides each step cites.
- `scripts/docs/reference/the-piece-ladder.md` — the gates a checklist cites by number.
- `.claude/skills/run-media-workflow/SKILL.md` — the router that picks a procedure.

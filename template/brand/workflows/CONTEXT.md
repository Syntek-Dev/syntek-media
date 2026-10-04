# CONTEXT.md — brand/workflows/

The brand layer's ordered procedures: one per kind of brand job, each a folder of four files
(`CONTEXT.md`, `CLAUDE.md`, `STEPS.md`, `CHECKLIST.md`). Numbers are frozen and never reused, so
a gap would be a procedure that was retired, not a missing one. None of these procedures moves a
piece up the ladder; they set up what every piece is later drawn from. **Never improvise a
thumbnail, a caption style or a narrator for one piece.** Settle it here. The author's own
procedures live in `brand/workflows/local/`.

## Directory Tree

```text
brand/workflows/
├── CONTEXT.md                      ← this file
├── CLAUDE.md                       ← operating rules and the 'You want to…' index
├── 01-set-up-the-brand-kit/        ← tokens, fonts and the two layout components, settled and checked
├── 02-sync-with-claude-design/     ← one component at a time, between the kit and its design project
├── 03-record-a-design-export/      ← an exported asset filed by size, stored right and registered
├── 04-set-up-a-platform/           ← a platform profile: the account, the deliverables, the choices
├── 05-write-the-spoken-voice/      ← the spoken style, a narrator for each use, pronunciations
├── 06-check-the-setup/             ← tools, permissions, Git LFS and ElevenLabs, before the first spend
└── local/                          ← your own procedures; a same-slug folder here wins
```

Each procedure folder holds:

```text
NN-verb-first-name/
├── CHECKLIST.md        ← model-tagged checklist: Pre-Conditions, Execution Checklist, Done When
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← when to use it, what it produces, the failure it prevents
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## What's here

- **Four files per procedure**, always: `CONTEXT.md` (when to reach for it), `CLAUDE.md` (how
  to run it), `STEPS.md` (the ordered steps) and `CHECKLIST.md` (pre-conditions, execution,
  done-when, each item tagged with its model tier).
- **Numbers are frozen and append-only**, unique within this layer across every brand kind,
  platform and media kind; every file cites a procedure by its full folder name.
- **No skill runs these procedures.** Each is done with the author, step by step; the toolkit's
  checks (`python3 toolkit/media.py tokens`, `uv run toolkit/card.py check`,
  `python3 toolkit/media.py check --setup`) do the verifying.
- `local/` — procedures written for this project, in their own numbering.

## Cross-references

- `.claude/rules/syntek-media/01-layout-and-routing.md` — routing frontmatter, frozen numbering
  and the local override rule.
- `brand/docs/reference/` — the guides each step cites.
- `scripts/docs/reference/the-piece-ladder.md` — the gates a checklist cites; none applies here.
- `.claude/skills/run-media-workflow/SKILL.md` — the router.

@./CONTEXT.md

# CLAUDE.md — publishing/docs/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold the publishing layer's guides (the template's in `reference/`, the author's in `project/`),
each deferring to the media rules file that governs it.

## How to work here

- **Routing:** you are usually reading a guide to apply it in `publishing/src/`. Look in
  `project/` first; a same-named guide there overrides `reference/`.
- **Model:** **Opus** for any substantive change to a guide; the mechanical tier only for a typo or
  a broken link (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps to change a guide:**
  1. Read the guide's governing rules file and section, named at its foot.
  2. Confirm the change is a practice change, not a rule change. The rules files are
     template-owned; a project rule goes where `.claude/rules/syntek-media/01-layout-and-routing.md`
     Section 10 says, with the author's confirmation first.
  3. Write it in `project/` under the reference guide's name, in the same shape: routing
     frontmatter, `# Title — gloss`, metadata header, `**What it is.**`, two to five topic
     sections, `## How we apply it here`, `## Who implements it`, `## Governing standard`.
  4. Grep `publishing/src/` and `publishing/workflows/` for anything citing it, and reconcile.
- **Definition of done:** short, practical and scannable; defers to its rules section; names its
  skill and workflow; nothing in `src/` or `workflows/` contradicts it.

## Guardrails

- **A guide never outranks the rules.** If a guide and the rules file it names disagree, the rules
  file is right; report the disagreement to the author.
- **No platform number in a guide.** A limit is cited by its key in
  `toolkit/data/platforms.toml`, which is dated and refreshed; a number copied into prose goes
  stale silently.
- **A guide never weakens a gate.** The gates in `scripts/docs/reference/the-piece-ladder.md` bind
  every piece; a project guide may add a check, never remove one.
- **Never self-edit.** No guide is rewritten without the author's explicit instruction
  (`.claude/rules/syntek-media/06-global-rules.md`).

## Output & naming

- **Hand-written:** guides in `project/`, and this pair.
- **Template-owned:** everything in `reference/`.
- **Naming:** kebab-case `.md`, named for the question the guide answers.
- **Not here:** plans, captions, thumbnails and post packages (`publishing/src/`).

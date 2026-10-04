@./CONTEXT.md

# CLAUDE.md — production/docs/reference/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/docs/CONTEXT.md` → `production/docs/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Explain the everyday calls of making a master for any project made from this template, without
holding a single fact about this project's pieces.

## How to work here

- **Routing:** read the guide the current workflow names. Check `production/docs/project/` for a
  same-named file first; if one exists, it replaces the guide here.
- **Model:** **Opus** when applying a guide's judgement; nothing here calls for the mechanical
  tier, because these files are read, never edited
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Open the guide the workflow step names (the `**Guide:**` half of the step's dispatch line).
  2. Apply its `## How we apply it here` rules to the job in hand.
  3. Follow `## Governing standard` when a guide and a rule seem to disagree: the rule wins, and
     the disagreement is reported to the author.
- **Definition of done:** the job was done the way the guide describes, or the departure was
  agreed with the author and recorded in `production/docs/project/`.

## Guardrails

- **Template-owned: never edit these files.** `copier update` overwrites them and the edit is
  lost. Put the change in `production/docs/project/` under the same filename.
- **A guide never outranks a rule.** It explains how a requirement in
  `.claude/rules/syntek-media/` is met day to day.
- **Guides hold no project facts.** A voice ID, a footage location or a licence belongs in the
  brand's files or in a register under `production/src/`, never in a guide.
- **Platform numbers are not written here.** A guide cites a key of
  `toolkit/data/platforms.toml`; only the ACX targets and the house loudness values are stated,
  in the guides that own them.

## Output & naming

- **Hand-written:** nothing; the template writes these files. The table below shows which guides
  ship with which media kinds chosen when the project was generated.
- **Generated:** nothing here.

| Guide | Ships with |
|---|---|
| `source-media.md`, `edit-decision-lists.md`, `sound-and-loudness.md`, `rights-and-consent.md`, `elevenlabs.md`, `voiceover.md`, `recorded-pieces.md` | every project |
<: if 'audiobook' in MEDIA_KINDS :>| `audiobook-narration.md` | the audiobook media kind |
<: endif :>
@./CONTEXT.md

# CLAUDE.md — how-to/workflows/syntek-media/01-finish-a-copy/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/workflows/CONTEXT.md` → `how-to/workflows/CLAUDE.md` →
`how-to/workflows/syntek-media/CONTEXT.md` → `how-to/workflows/syntek-media/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Take a fresh copy of syntek-media to its first commit, with nothing left that would let a
session spend a credit unasked.

## How to work here

- **Routing:** no skill; this is a command-and-review procedure, and `run-media-workflow` never
  routes it. Guide `how-to/docs/syntek-media/finishing-a-copy.md`; the server is set up as
  `production/docs/reference/elevenlabs.md` says, and the check is
  `brand/workflows/06-check-the-setup/`.
- **Model:** **Opus** for reading what the copy printed and for every change to a settings file;
  the mechanical tier only for running a command the author has agreed
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go. A
  collision at step 1 ends this procedure: report it with
  `how-to/workflows/syntek-media/03-report-a-template-problem/`.
- **Definition of done:** the copy and `.copier-answers.syntek-media.yml` committed together,
  every entry the author agreed in place, the set-up check clean or each finding accepted, and
  nothing under `how-to/` changed by hand.

## Guardrails

- **The author decides** every settings entry and every command that reaches outside the
  project: a session never adds an entry, registers a server or runs `git lfs install` on its
  own judgement.
- **Never type or print a key.** The ElevenLabs key is exported in the author's shell and read
  from it; it never appears on a command line, in a file or in the session
  (`.claude/rules/syntek-media/06-global-rules.md` Section 10).
- **Never edit under `how-to/`**, even when asked: Claude Code's deny in `.claude/settings.json`
  and the guide guard `.claude/hooks/how-to-read-only.sh` refuse it, and the next update puts
  it back (`.claude/rules/syntek-media/06-global-rules.md` Section 3). A departure is recorded in
  syntek-author's project settings file, 00-project.md, under Overrides or Workflow aliases,
  where that file is present, and otherwise in `.claude/CLAUDE.md` under the heading
  'Project-specific rules' (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10).
- **Never edit `.copier-answers.syntek-media.yml` by hand.** A wrong answer is changed through
  an update (`how-to/workflows/syntek-media/02-change-the-answers/`), after the first commit.
- **No credit is spent here.** The set-up check spends nothing; no ElevenLabs tool is called.

## Output & naming

- **Writes:** entries in `.claude/settings.json` and the other clients' settings files, the
  optional index lines the author agrees, this repository's own Git settings through
  `git lfs install`, and the commit; the server goes into the author's user-scope Claude Code
  configuration, outside the project.
- **Does not touch:** the template's files, the answers file or anything under `how-to/`.

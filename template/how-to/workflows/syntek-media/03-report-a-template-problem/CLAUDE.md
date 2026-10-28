@./CONTEXT.md

# CLAUDE.md — how-to/workflows/syntek-media/03-report-a-template-problem/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/workflows/CONTEXT.md` → `how-to/workflows/CLAUDE.md` →
`how-to/workflows/syntek-media/CONTEXT.md` → `how-to/workflows/syntek-media/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Turn a fault in the template into an issue the maintainers can reproduce, with nothing in it
that should stay private.

## How to work here

- **Routing:** no skill; this is a command-and-review procedure, and `run-media-workflow` never
  routes it. Guide `how-to/docs/syntek-media/reporting-a-template-problem.md`; what to try
  before reporting is in `how-to/src/TEMPLATE-GUIDE/syntek-media/13-troubleshooting.md`.
- **Model:** **Opus** for judging whose fault it is, for every redaction and for the draft; the
  mechanical tier only for running a command that collects a version
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go. Where step 1
  finds the project's own edit, this procedure ends there.
- **Definition of done:** the author holds a redacted draft and knows where to file it, or,
  for a security problem, where to report it privately; nothing in the project changed.

## Guardrails

- **A session drafts; the author files.** A session never opens, files or comments on an issue,
  and never writes the source's web address: it names the source as `_src_path` records it.
- **Redact before anything is shown.** No API key, voice ID, account ID, Claude Design link,
  real person's details from a release form, private correspondence or home path goes into the
  draft (`.claude/rules/syntek-media/06-global-rules.md` Section 10).
- **A security problem is reported privately**, through the source's private vulnerability
  reporting, never in a public issue, discussion or pull request.
- **Reproduce without spending.** No ElevenLabs tool is called and no credit spent to show a
  fault; a stopped update is never run again here, only by its recovery procedure.
- **Never edit under `how-to/`**, even to show a fix: Claude Code's deny in
  `.claude/settings.json` and the guide guard `.claude/hooks/how-to-read-only.sh` refuse it, and
  the next update puts it back (`.claude/rules/syntek-media/06-global-rules.md` Section 3). A
  departure while the fault stands is recorded in syntek-author's project settings file,
  00-project.md, under Overrides or Workflow aliases, where that file is present, and otherwise
  in `.claude/CLAUDE.md` under the heading 'Project-specific rules'
  (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10).

## Output & naming

- **Writes:** nothing in the project. The draft is given to the author in the session; the
  temporary folder step 1 may render into is outside the project, and the author removes it.
- **Names:** the draft's title says what failed and where, in a line, such as the command or the
  file and the error it gave.

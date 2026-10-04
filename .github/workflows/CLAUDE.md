@./CONTEXT.md

# CLAUDE.md — .github/workflows/

Read order: `.claude/CLAUDE.md` → `CONTEXT.md` → `.github/CONTEXT.md` → `.github/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep `audit-template.yml` a thin, honest runner of `.github/scripts/`: every check on every push.

## How to work here

- **Routing:** what a check does → `.github/scripts/<script>.sh`; this folder decides only when
  and where it runs, and whether syntek-author is there for the scripts that need it.
- **Model:** **Opus** for a change to triggers, permissions or job structure; the mechanical tier
  for adding a script to an existing loop.
- **Concrete steps:**
  1. A new audit joins the loop of the job that matches its input (source, renders, or its own
     scratch project), with its `--self-test` immediately before its real run.
  2. Check the file still holds no dollar-brace-brace sequence:
     `grep -c '[$][{][{]' .github/workflows/audit-template.yml` must print 0 (the bracket form
     works in every grep; an escaped `\{` is an interval to GNU grep, which then exits 2).
  3. Lint it: `uvx --from actionlint-py actionlint .github/workflows/audit-template.yml`.
- **Definition of done:** actionlint is clean, the file holds no expression syntax, and the run
  on the branch is green — or red only with findings the template must fix.

## Guardrails

- **No path filter and no branch filter on push.** The defect this catches is invisible in the
  branch that caused it.
- **`permissions: contents: read`, and nothing more.** The audits read; they never write.
- **No dollar-brace-brace sequence, ever** — no matrix, no concurrency group, no expression in a
  `run:` block, no secret. GitHub parses that syntax anywhere in the file. Use shell loops,
  `$RUNNER_TEMP` and `$GITHUB_ENV`.
- **syntek-author arrives through a plain shell step**, never a second checkout action: a clone
  that fails must degrade to a warning and a named SKIP, not a red job, and must never be
  reported as a pass.
- **Accumulate, never fail fast.** Each loop records `status=1` with an `::error::` line and exits
  at the end, so one broken gate never hides the next.
- **Self-test before real run, always.** A green real run means nothing from a detector nobody
  has seen fail.
- **Never give the workflow an ElevenLabs key.** No test calls the service, and a key in CI is a
  key that can spend.

## Output & naming

- **Hand-written:** `audit-template.yml`, named for the job it does, as in syntek-author and
  syntek-base.
- **Generated (never commit):** everything a run produces, the syntek-author clone included,
  stays under `$RUNNER_TEMP`.

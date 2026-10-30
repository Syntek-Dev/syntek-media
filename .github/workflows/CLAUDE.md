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
  2. Check the dollar-brace-brace sequence appears only in the `concurrency` block (`group` and
     `cancel-in-progress`): `grep -n '[$][{][{]' .github/workflows/audit-template.yml` must
     print those two lines and no other (the bracket form works in every grep; an escaped `\{`
     is an interval to GNU grep, which then exits 2).
  3. Lint it: `uvx --from actionlint-py actionlint .github/workflows/audit-template.yml`.
- **Definition of done:** actionlint is clean, the dollar-brace-brace sequence appears nowhere
  outside the `concurrency` block, and the run on the branch is green — or red only with
  findings the template must fix.

## Guardrails

- **No path filter and no branch filter on push.** The defect this catches is invisible in the
  branch that caused it.
- **`permissions: contents: read`, and nothing more.** The audits read; they never write.
- **The dollar-brace-brace sequence stays out of the steps.** It appears only in the
  `concurrency` block (`group` and `cancel-in-progress`); no `run:` step, matrix or secret uses
  it (the one step condition, `if: always()`, needs none). GitHub parses it anywhere in the
  file, even inside a `run:` block. Use shell loops, `$RUNNER_TEMP` and `$GITHUB_ENV`.
- **syntek-author arrives through a plain shell step**, never a second checkout action: a clone
  that fails must degrade to a warning and a named SKIP, not a red job, and must never be
  reported as a pass.
- **Accumulate, never fail fast.** Each loop records `status=1` with an `::error::` line and exits
  at the end, so one broken gate never hides the next.
- **Self-test before real run, always.** A green real run means nothing from a detector nobody
  has seen fail.
- **Python 3.14 everywhere, named twice.** Every job's `setup-python` installs 3.14 and the
  workflow's `env` keeps `UV_PYTHON` on it; a job without either runs Copier, and the family
  scripts inside it, on whatever Python uv finds (D81).
- **Never give the workflow an ElevenLabs key.** No test calls the service, and a key in CI is a
  key that can spend.

## Output & naming

- **Hand-written:** `audit-template.yml`, named for the job it does, as in syntek-author and
  syntek-base.
- **Generated (never commit):** everything a run produces, the syntek-author clone included,
  stays under `$RUNNER_TEMP`.

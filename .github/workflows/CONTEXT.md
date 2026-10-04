# CONTEXT.md — .github/workflows/

The template repository's CI. One workflow, `audit-template.yml`, runs every audit and test in
`.github/scripts/` on every push to every branch, on pull requests and on demand. It exists because
a template defect is invisible until somebody generates, and whoever generates is not whoever
broke it: a gate that waits for a pull request lets a branch drift unseen for as long as it lives.

This folder holds the template's own workflow only. Media ships no workflow to a generated
project (DESIGN.md D11).

## Directory Tree

```text
.github/workflows/
├── CONTEXT.md            ← this file
├── CLAUDE.md             ← operating rules for the workflow
└── audit-template.yml    ← three parallel jobs: template source, renders, update and coexistence
```

## What's here

- `audit-template.yml` — three jobs, each running every script's `--self-test` before its real
  run and reporting failures as `::error::` lines that accumulate:
  - **[1/3] Template source** — tokens, the mode-file block, pairs and shapes, the line cap,
    personal data, development isolation, seeds, skills.
  - **[2/3] Renders** — installs uv and ffmpeg, renders every brand kind and profile once (and
    each kind over syntek-author where it could be fetched), and runs the per-render audits over
    all of them, the toolkit smoke test under `--require-ffmpeg`. Playwright's Chromium is not
    installed, so the thumbnail and card renders are named as skipped, never passed.
  - **[3/3] Update and coexistence** — a real `copier update` in its own scratch project, and
    media applied over a real syntek-author project and the other way round.
- Jobs 2 and 3 first clone syntek-author into the runner's temporary folder with a plain shell
  step and export `SYNTEK_AUTHOR_DIR`; when the clone fails they print a warning, and the scripts
  that need it report a named SKIP (DESIGN.md D27).

## Cross-references

- `.github/scripts/CONTEXT.md` — what each script checks.
- `.github/scripts/run-all.sh` — the same run, locally, in one command.
- `DESIGN.md` Section 7 — the CI paragraph: every push, no path filter, the three jobs, the
  syntek-author clone, no expression syntax.

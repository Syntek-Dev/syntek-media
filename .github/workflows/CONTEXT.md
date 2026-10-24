# CONTEXT.md — .github/workflows/

The template repository's CI. One workflow, `audit-template.yml`, runs every audit and test in
`.github/scripts/` on every push to every branch, on pull requests and on demand; a newer run on the
same branch or pull request cancels the one it supersedes (never on `main`). It exists because
a template defect is invisible until somebody generates, and whoever generates is not whoever
broke it: a gate that waits for a pull request lets a branch drift unseen for as long as it lives.

This folder holds the template's own workflow only. Media ships no workflow to a generated
project (DESIGN.md D11).

## Directory Tree

```text
.github/workflows/
├── CONTEXT.md            ← this file
├── CLAUDE.md             ← operating rules for the workflow
└── audit-template.yml    ← three parallel jobs (source, renders, update and coexistence) and an advisory fourth
```

## What's here

- `audit-template.yml` — three required jobs, each running every script's `--self-test` before
  its real run and reporting failures as `::error::` lines that accumulate:
  - **[1/3] Template source** — tokens, the mode-file block, pairs and shapes, the line cap,
    personal data, development isolation, the community files at the root (D83), seeds, skills;
    then, in the same step, the vendored `migrations/agents-outside-link.py --self-test` (D85)
    and, with `SYNTEK_DATA_ROOT` unset, the vendored data-root resolver's and permissions
    script's, `template/.claude/syntek-media-dataroot.py` and `syntek-media-permissions.py` (D80).
  - **[2/3] Renders** — installs uv and ffmpeg, renders every brand kind and profile once (and
    each kind over syntek-author where it could be fetched), and runs the per-render audits over
    all of them, the toolkit smoke test under `--require-ffmpeg`. Playwright's Chromium is not
    installed, so the thumbnail and card renders are named as skipped, never passed.
  - **[3/3] Update and coexistence** — a real `copier update` in its own scratch project, and
    media applied over a real syntek-author project and the other way round.
- Jobs 2 and 3 first clone syntek-author, at the tag in the workflow's `SYNTEK_AUTHOR_TAG` (the
  release media vendors from, D85), into the runner's temporary folder with a plain shell step and
  export `SYNTEK_AUTHOR_DIR`; when the clone fails they print a warning, and the scripts that need
  it report a named SKIP (DESIGN.md D27).
- **syntek-author main (advisory)** runs `coexist-test.sh` against syntek-author's default
  branch and prints what it finds as warnings; it always exits 0 and is not a required check, so a
  syntek-author merge shows here before media adopts it, without turning the run red.

## Cross-references

- `.github/scripts/CONTEXT.md` — what each script checks.
- `.github/scripts/run-all.sh` — the same run, locally, in one command.
- `DESIGN.md` Section 7 — the CI paragraph: every push, no path filter, the three jobs and the
  advisory fourth, the pinned syntek-author clone, the dollar-brace-brace sequence only in the
  `concurrency` block.

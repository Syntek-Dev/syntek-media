# CONTEXT.md — .github/

The template repository's own continuous integration: the audits and tests that prove
syntek-media still generates what `DESIGN.md` promises — on its own and applied over a real
syntek-author project — and the workflow that runs them on every push. Nothing here is rendered:
`_subdirectory: template` keeps the repository root out of every generated project, so nothing
here ships, and nothing here may assume it will. Media ships no `.github/` of its own at all
(DESIGN.md D11); a syntek-author business project's Drive workflows are syntek-author's.

## Directory Tree

```text
.github/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← operating rules for the audits and their workflow
├── scripts/          ← one script per DESIGN.md Section 7 audit, the runner, the shared library, the frozen syntek-author names
└── workflows/        ← audit-template.yml: every audit, every push, no path filter
```

## What's here

- `scripts/` — fifteen audits and tests in syntek-author's house shape (a header saying why the
  check exists, numbered checks, what it cannot check, a `--self-test`, exit codes 0/1/2),
  `run-all.sh` to run them all against one set of renders, `_common.sh`, the one reader of
  `copier.yml` and the one transcription of `DESIGN.md`'s catalogue, and
  `syntek-author-names.txt`, the names media must never take (D27). **A change to `DESIGN.md`
  changes `_common.sh` in the same commit.**
- `workflows/` — `audit-template.yml`, three parallel jobs (template source, renders, update and
  coexistence) that run every self-test before every real run.

## Why the audits exist

Every promise `DESIGN.md` makes about a generated project — this brand kind gets these mode files
and not those, a removed platform takes its two files and nothing else, a shared file is never
touched by an update, a seed ships empty, nothing media ships collides with syntek-author — rests
on one line of `copier.yml` or one file under `template/`, and none of them fails loudly when that
line is wrong. Copier renders successfully either way, and a collision with syntek-author shows up
only as conflict markers inside its files on some later update. These scripts are the only place
the failure becomes visible before an author meets it.

## Cross-references

- `DESIGN.md` Section 7 — the audit list and what each one checks; this folder implements it.
- `copier.yml` — the gates, seeds, shared files, messages and questions the audits read.
- `examples/` — the invented answers files `scripts/generate-all.sh` holds to the questions.
- syntek-author — the coexistence partner the over-author renders and `scripts/coexist-test.sh`
  apply media to: `--author DIR` locally, `SYNTEK_AUTHOR_DIR` in CI.

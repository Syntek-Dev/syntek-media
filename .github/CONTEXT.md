# CONTEXT.md — .github/

The template repository's own continuous integration: the audits and tests that prove
syntek-media still generates what `DESIGN.md` promises — on its own and applied over a real
syntek-author project — and the workflow that runs them on every push; and the files GitHub
shows contributors, the issue forms, the pull-request template and the code owners (D83).
Nothing here is rendered: `_subdirectory: template` keeps the repository root out of every
generated project, so nothing here ships, and nothing here may assume it will. Media ships no
`.github/` of its own at all (DESIGN.md D11); a syntek-author business project's Drive workflows
are syntek-author's.

## Directory Tree

```text
.github/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← operating rules for the audits and their workflow
├── scripts/          ← one script per DESIGN.md Section 7 audit, the runner, the shared library, the frozen syntek-author names
├── workflows/        ← audit-template.yml: every audit, every push, no path filter
├── ISSUE_TEMPLATE/   ← two issue forms (bug report, template improvement); config.yml: no blank issues; no pair
├── PULL_REQUEST_TEMPLATE.md   ← the pull-request checklist, the contribution licence confirmation included
└── CODEOWNERS        ← @Syntek-Studio on every path, with the closer reads named
```

## What's here

- `scripts/` — sixteen audits and tests in syntek-author's house shape (a header saying why the
  check exists, numbered checks, what it cannot check, a `--self-test`, exit codes 0/1/2),
  `run-all.sh` to run them all against one set of renders, `_common.sh`, the one reader of
  `copier.yml` and the one transcription of `DESIGN.md`'s catalogue, and
  `syntek-author-names.txt`, the names media must never take (D27). **A change to `DESIGN.md`
  changes `_common.sh` in the same commit.**
- `workflows/` — `audit-template.yml`, three parallel jobs (template source, renders, update and
  coexistence) that run every self-test before every real run, and an advisory fourth against
  syntek-author's `main`.
- `ISSUE_TEMPLATE/`, `PULL_REQUEST_TEMPLATE.md`, `CODEOWNERS` — the community files GitHub reads
  from this folder (D83); `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md` and `CODE_OF_CONDUCT.md`
  sit at the repository root. `ISSUE_TEMPLATE/` holds two issue forms, a bug report and a
  template improvement, each with a required personal-data checkbox, and `config.yml`, which
  turns blank issues off and links this repository's private vulnerability reporting,
  syntek-author's issues (for its own files) and the README: an outside reporter sees only the
  forms, while a user with write access still sees a blank issue marked 'Maintainers only'.
  **The folder holds GitHub's own YAML files only, with no `CONTEXT.md` and `CLAUDE.md` pair**:
  GitHub lists a Markdown file there as an issue template once it gains `name` and `about` front
  matter, so the house keeps Markdown out of it, and this file describes it instead. The
  pull-request template's checklist ends with the contributor's confirmation that the
  contribution is made on the terms of `CONTRIBUTING.md` ('Licence'). `CODEOWNERS` names
  `@Syntek-Studio` on every path. `scripts/community-files.sh` checks them all, the YAML-only
  rule included (check 3).

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
- `CONTRIBUTING.md`, `SECURITY.md` — the front door the issue forms and the pull-request template
  serve, and the one route for a vulnerability report (D83).
- syntek-author — the coexistence partner the over-author renders and `scripts/coexist-test.sh`
  apply media to: `--author DIR` locally, `SYNTEK_AUTHOR_DIR` in CI.

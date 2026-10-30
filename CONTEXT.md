# CONTEXT.md — syntek-media/

The repository of a Copier template that adds audio and video production to a project, in three brand kinds: `business`, `author-fiction` and `author-nonfiction`.
It has two halves. **`template/` is the product**: everything a generated project receives, at its real path, rendered by Copier with the house delimiters.
**Everything else is the template's own state**: its contract, its questions, its audits, its example answers, its development manual and its licence and community files — none of it ships.
Nobody records, cuts or publishes anything here; a generated project — usually a syntek-author project the template has been applied to — is where the production happens.

## Directory Tree

```text
syntek-media/
├── CONTEXT.md                ← this file: the map of the repository
├── README.md                 ← the user guide: applying over syntek-author, standalone, the questions, updating, coexistence, audio, audits, the licence
├── DESIGN.md                 ← the build contract; where any file disagrees with it, DESIGN.md wins
├── copier.yml                ← questions, gated _exclude, _skip_if_exists, messages, _tasks, _migrations
├── VERSION                   ← the template's release number (0.5.0)
├── CHANGELOG.md              ← the template's history, Keep a Changelog
├── family-shared.json        ← the family-shared files and blocks media vendors from syntek-author's release tag, with their sizes and hashes (D80)
├── LICENSE · CONTRIBUTING.md · SECURITY.md · CODE_OF_CONDUCT.md   ← community files (D83), never shipped: MIT; changes to the template; private vulnerability reports; Contributor Covenant 2.1
├── AGENTS.md                 ← Codex development entrypoint; reads the development manual
├── GEMINI.md                 ← Antigravity development entrypoint
├── .mcp.json                 ← development MCP: code-review-graph only (never shipped)
├── .gitignore                ← development only: the code-review-graph database and the handoff files (/handoffs/HANDOFF-*.md)
├── .agents/                  ← real folder (D76) holding only its pair: no skills, no MCP file
├── .codex/                   ← Codex development isolation settings and their folder pair
├── .claude/                  ← the DEVELOPMENT manual and dev-isolation settings (never shipped)
│   ├── CLAUDE.md             ← how to work on the template: contract, tokens, recipes, audits
│   ├── CONTEXT.md            ← what this .claude/ folder holds
│   └── settings.json         ← denies every template skill; keeps template manuals out of sessions
├── .github/
│   ├── CONTEXT.md · CLAUDE.md
│   ├── scripts/              ← the audits and tests (DESIGN.md Section 7) and syntek-author-names.txt
│   ├── workflows/audit-template.yml   ← CI: every audit, on every push
│   ├── ISSUE_TEMPLATE/       ← bug report and template improvement forms; config.yml turns blank issues off (three YAML files, no pair, D83)
│   ├── PULL_REQUEST_TEMPLATE.md   ← the pull-request checklist, the contribution licence confirmation included
│   └── CODEOWNERS            ← @Syntek-Studio reviews every path, with the closer reads named
├── handoffs/                 ← development handoffs between sessions, never shipped
│   └── CONTEXT.md · CLAUDE.md · HANDOFF-*.md
├── migrations/               ← update-time scripts, never shipped: media's own v0.4.2-agents-folder.py and v0.6.0-how-to.py (D76, D84); agents-outside-link.py and family-update.py, vendored from syntek-author (D85, D81); family-refresh.json, media's own refresh data (D81)
│   └── CONTEXT.md · CLAUDE.md
├── examples/                 ← invented answers files, one per brand kind
│   ├── CONTEXT.md · CLAUDE.md
│   └── business · author-fiction · author-nonfiction .answers.yml
└── template/                 ← EVERYTHING that ships, at its real path
    ├── .copier-answers.syntek-media.yml   ← renders the project's answers record
    ├── README.md · CONTEXT.md · .gitignore · .mcp.json   ← copy-only shared files (written only where absent; .mcp.json is offered the two family MCP servers once, D81)
    ├── AGENTS.md · GEMINI.md · opencode.json · .agents/ · .codex/ · .gemini/   ← coding-agent files, copy-only shared, for the clients ticked in AGENT_CLIENTS (D80)
    ├── handoffs/             ← its pair only, copy-only shared: syntek-author's bytes (D80)
    ├── how-to/               ← the user guide, read-only and put back by every full update (D84): the family's shared pairs and chapters, media's own under its syntek-media/ folders
    ├── .claude/              ← CLAUDE.md, CONTEXT.md, MEMORY.md, settings.json (copy-only shared) · hooks/ (the two handoff hooks and the guide guard) and the seven working-practice skills (copy-only shared, syntek-author's bytes, refreshed by the update script while the owner never changed them, D81) · the bridge, data-root and permissions files · rules/syntek-media/ · skills/
    ├── brand/                ← the visual tokens and layouts, the spoken voice, one profile per platform
    ├── scripts/              ← pieces: briefs, scripts or transcripts, storyboards, shot lists
    ├── production/           ← footage manifest, voiceover, timing and scene files, edit decision lists, cards, masters, rights, credits; audiobook (gated)
    ├── publishing/           ← cut-downs, captions, thumbnails, post packages, schedule, publish log
    └── toolkit/              ← supporting: media.py (ffmpeg; each piece's output in a folder of its own), card.py (HTML → PNG), platform data, fallback layouts
```

## What's here

- `DESIGN.md` — the decisions (D1–D76 and D80–D85; D77–D79 are reserved, and later decisions take D86 onwards), the questions, the ownership classes and gating table, the generated tree, the skills, the formats, the audits, applying over syntek-author and coexistence. **Read the sections your change touches before changing anything**; comments in `copier.yml` cite it by section.
- `copier.yml` — the contract Copier executes. **Every gated path is one `_exclude` line whose gate is copied verbatim from DESIGN.md Section 3.5** (`'youtube' in PLATFORMS`, `'audiobook' in MEDIA_KINDS`), each of the fifty shared paths has an update-gated `_exclude` line beside its `_skip_if_exists` line (and `/.claude/mcp_config.json` one more, unconditional, that stops a copy shipping it, D76), each coding agent's files carry syntek-author's gate on `AGENT_CLIENTS` (D80), the fifteen family-shared questions sit last, between syntek-author's own marker lines, byte for byte (D80), the only reads of `_external_data` are `BRAND_KIND`'s validator, that block and `_message_after_update` (D14 as D80 widens it and D81 corrects its text), `_tasks` runs media's three copy-only tasks, then D84's warning where syntek-author's answers file stands without its guide, and last syntek-author's `baseline` task (D81), `_migrations` runs D76's outside-link pair, then `v0.4.2`, then `v0.6.0`'s report (D84), and closes with the family 'update' block (D81), the one path ever negated back in is an output folder's own `README.md`, listed above every gated line (DESIGN.md Section 3.5, D19), and the mode-file block between its `BEGIN`/`END generated mode excludes` markers is written by `.github/scripts/gen-mode-excludes.sh`, never by hand.
- `template/` — the product. **Every file in it is rendered**, so the delimiters `<%`, `<:` and `<~` appear only where a token is meant (token discipline: `.claude/CLAUDE.md` Section 4), HTML, CSS, TOML and SRT included.
- `.claude/` — the development manual. Its settings deny every skill under `template/.claude/skills/` and exclude the template's `CLAUDE.md` files from development sessions, so the product's instructions never steer the people building it.
- `.github/scripts/` — the audits, each with a `--self-test`; `README.md` lists what each checks. CI runs all of them on every push. `syntek-author-names.txt` freezes the names media must never take (D27).
- `examples/` — invented answers files, one per brand kind, for `copier copy --data-file` and for the audits; together they turn on every platform and every media kind, and each answers the fifteen family-shared questions as syntek-author's matching example does (D80). Over syntek-author, an edited copy drops its `DATA_*`, client and model lines, so the family questions default to syntek-author's record (D14, D81). There are no adoption scripts (DESIGN.md Section 8).
- `VERSION`, `CHANGELOG.md` — the template's own release state. A generated project starts its own history; nothing here is copied into it.
- `migrations/` — the scripts `copier update` runs, mostly when a project crosses a release that moves something an author or a shared path holds; none ships. Media's own are `v0.4.2-agents-folder.py`, which replaces an `.agents -> .claude` link with the real folder (D76), and `v0.6.0-how-to.py`, the report-only crossing script that says where the guide starts and what the release leaves to the owner (D84). Two are syntek-author's family-shared bytes, vendored from its `v0.8.0` tag and never edited here (D85, D81), and each runs on every update, unversioned: `agents-outside-link.py`, whose pair of entries opens `_migrations`, holding an `.agents` link that leaves the project aside before the render and restoring it after (D76), and `family-update.py`, whose 'update' entry closes it and which the copy's `baseline` task also runs: on Python 3.14 it reports, refreshes the listed family files the owner never changed, offers the listed settings entries and MCP servers once each, and puts the guide back. `family-refresh.json` is media's own data for that script, listed in no manifest. The rule and the house shape are in `copier.yml`, under `_migrations`.
- `family-shared.json` — media's record, in the family's format (syntek-author D48), of every family-shared file and block it vendors from one syntek-author release tag (D80): each file's family path, its source under media's name, its size, SHA-256 and mode or link target, and each block's marker lines, size and SHA-256, the four blocks being 'questions', 'migrations', 'update' and 'rules-web-tools'. It never ships. Only `bash .github/scripts/shipped-seeds.sh --write-manifest` writes it, after a new tag is vendored, never a hand edit; `shipped-seeds.sh` holds the tree and every render to it, and `coexist-test.sh` holds it to syntek-author's own, entry by entry.
- `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` and, in `.github/`, `CODEOWNERS`, `PULL_REQUEST_TEMPLATE.md` and `ISSUE_TEMPLATE/` — the community files (D83). **None of them ships**: `_subdirectory: template` keeps the whole root out of every generated project, so none needs an `_exclude` line, and a generated project's licence stays its owner's choice. Each repository of the family writes its own. `LICENSE` is the MIT Licence alone, 'Copyright (c) 2026 Sam Bailey t/a Syntek', byte for byte the family's, so GitHub detects it; the licence and its permission for generated projects are in the README's 'Licence' section and `CONTRIBUTING.md` ('Licence'), in the family's words, and `CONTRIBUTING.md` takes contributions under the same terms (inbound = outbound), with no CLA. `SECURITY.md` takes reports only through GitHub's private vulnerability reporting; `CODE_OF_CONDUCT.md` is the Contributor Covenant 2.1 and the one file that names its enforcement contact. `ISSUE_TEMPLATE/` holds GitHub's own YAML files and no pair, a house rule that `.github/CONTEXT.md` explains; `.github/scripts/community-files.sh` checks them all.

## Cross-references

- `README.md` — what a user of the template needs: applying it over a syntek-author project without `--overwrite`, the hand edits after a copy, standalone generation, the user guide, the questions, the five ownership classes, updating with `-a`, coexistence, large files, ElevenLabs and Claude Design, and the licence.
- `.claude/CLAUDE.md` — what a maintainer needs: dev isolation, token discipline, how to add a skill, a mode file, a gated path, a workflow, a seed, a question, a platform or a media kind, and how to release.
- `DESIGN.md` Section 3 — ownership classes and the gating table; Section 7 — this repository's root and audits; Section 8 — applying syntek-media; Section 9 — coexistence with syntek-author; Section 10 — hazards.

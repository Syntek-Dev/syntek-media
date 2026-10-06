# CONTEXT.md — syntek-media/

The repository of a Copier template that adds audio and video production to a project, in three brand kinds: `business`, `author-fiction` and `author-nonfiction`.
It has two halves. **`template/` is the product**: everything a generated project receives, at its real path, rendered by Copier with the house delimiters.
**Everything else is the template's own state**: its contract, its questions, its audits, its example answers and its development manual — none of it ships.
Nobody records, cuts or publishes anything here; a generated project — usually a syntek-author project the template has been applied to — is where the production happens.

## Directory Tree

```text
syntek-media/
├── CONTEXT.md                ← this file: the map of the repository
├── README.md                 ← the user guide: applying over syntek-author, standalone, the questions, updating, coexistence, audio, audits
├── DESIGN.md                 ← the build contract; where any file disagrees with it, DESIGN.md wins
├── copier.yml                ← questions, gated _exclude, _skip_if_exists, messages, _tasks, _migrations
├── VERSION                   ← the template's release number (0.4.0)
├── CHANGELOG.md              ← the template's history, Keep a Changelog
├── AGENTS.md                 ← Codex development entrypoint; reads the development manual
├── GEMINI.md                 ← Antigravity development entrypoint
├── .agents                   ← relative link to the development .claude tree
├── .codex/                   ← Codex development isolation settings and their folder pair
├── .claude/                  ← the DEVELOPMENT manual and dev-isolation settings (never shipped)
│   ├── CLAUDE.md             ← how to work on the template: contract, tokens, recipes, audits
│   ├── CONTEXT.md            ← what this .claude/ folder holds
│   └── settings.json         ← denies every template skill; keeps template manuals out of sessions
├── .github/
│   ├── CONTEXT.md · CLAUDE.md
│   ├── scripts/              ← the audits and tests (DESIGN.md Section 7) and syntek-author-names.txt
│   └── workflows/audit-template.yml   ← CI: every audit, on every push
├── examples/                 ← invented answers files, one per brand kind
│   ├── CONTEXT.md · CLAUDE.md
│   └── business · author-fiction · author-nonfiction .answers.yml
└── template/                 ← EVERYTHING that ships, at its real path
    ├── .copier-answers.syntek-media.yml   ← renders the project's answers record
    ├── README.md · CONTEXT.md · .gitignore · .mcp.json   ← copy-only shared files (written only where absent)
    ├── .claude/              ← CLAUDE.md, CONTEXT.md, MEMORY.md, settings.json (copy-only shared) · rules/syntek-media/ · skills/
    ├── brand/                ← the visual tokens and layouts, the spoken voice, one profile per platform
    ├── scripts/              ← pieces: briefs, scripts or transcripts, storyboards, shot lists
    ├── production/           ← footage manifest, voiceover, timing and scene files, edit decision lists, cards, masters, rights, credits; audiobook (gated)
    ├── publishing/           ← cut-downs, captions, thumbnails, post packages, schedule, publish log
    └── toolkit/              ← supporting: media.py (ffmpeg; each piece's output in a folder of its own), card.py (HTML → PNG), platform data, fallback layouts
```

## What's here

- `DESIGN.md` — the decisions (D1–D74), the questions, the ownership classes and gating table, the generated tree, the skills, the formats, the audits, applying over syntek-author and coexistence. **Read the sections your change touches before changing anything**; comments in `copier.yml` cite it by section.
- `copier.yml` — the contract Copier executes. **Every gated path is one `_exclude` line whose gate is copied verbatim from DESIGN.md Section 3.5** (`'youtube' in PLATFORMS`, `'audiobook' in MEDIA_KINDS`), each of the seventeen shared root paths has an update-gated `_exclude` line beside its `_skip_if_exists` line, the one path ever negated back in is an output folder's own `README.md`, listed above every gated line (DESIGN.md Section 3.5, D19), and the mode-file block between its `BEGIN`/`END generated mode excludes` markers is written by `.github/scripts/gen-mode-excludes.sh`, never by hand.
- `template/` — the product. **Every file in it is rendered**, so the delimiters `<%`, `<:` and `<~` appear only where a token is meant (token discipline: `.claude/CLAUDE.md` Section 4), HTML, CSS, TOML and SRT included.
- `.claude/` — the development manual. Its settings deny every skill under `template/.claude/skills/` and exclude the template's `CLAUDE.md` files from development sessions, so the product's instructions never steer the people building it.
- `.github/scripts/` — the audits, each with a `--self-test`; `README.md` lists what each checks. CI runs all of them on every push. `syntek-author-names.txt` freezes the names media must never take (D27).
- `examples/` — invented answers files, one per brand kind, for `copier copy --data-file` and for the audits; together they turn on every platform and every media kind. There are no adoption scripts (DESIGN.md Section 8).
- `VERSION`, `CHANGELOG.md` — the template's own release state. A generated project starts its own history; nothing here is copied into it.
- There is no `migrations/` folder yet. The first release that renames a folder holding author work, or stops shipping a seed, creates it (the rule is in `copier.yml`, under `_migrations`).

## Cross-references

- `README.md` — what a user of the template needs: applying it over a syntek-author project without `--overwrite`, the hand edits after a copy, standalone generation, the questions, the five ownership classes, updating with `-a`, coexistence, large files, ElevenLabs and Claude Design.
- `.claude/CLAUDE.md` — what a maintainer needs: dev isolation, token discipline, how to add a skill, a mode file, a gated path, a workflow, a seed, a question, a platform or a media kind, and how to release.
- `DESIGN.md` Section 3 — ownership classes and the gating table; Section 7 — this repository's root and audits; Section 8 — applying syntek-media; Section 9 — coexistence with syntek-author; Section 10 — hazards.

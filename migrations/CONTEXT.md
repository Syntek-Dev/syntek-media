# CONTEXT.md — migrations/

The scripts `copier update` runs when a project crosses a release that moved something an author, or a shared path, holds.
Copier only tracks what it generated: a renamed folder takes its governance pair to the new place and leaves the author's work behind, and a copy-only shared path (D11) is never touched by an update at all, so a release that must change one can reach it only here.
A migration acts where exactly one result is correct and reports everything else.
Nothing here ships: `_subdirectory: template` keeps this folder out of every generated project, and `copier.yml` runs each script from the template clone through `_copier_conf.src_path`.

## Directory Tree

```text
migrations/
├── CONTEXT.md                  ← this file
├── CLAUDE.md                   ← operating rules for writing a migration
├── agents-outside-link.py      ← every update: an .agents link outside the project held aside and restored (D76)
└── v0.4.2-agents-folder.py     ← .agents -> .claude link → real .agents/ folder (D76)
```

## What's here

- `agents-outside-link.py` — **every brand kind, every update; the one script not keyed to a release.** Copier refuses any destination that resolves outside the project before it reads `_exclude` (Copier 9.17.1), so where `.agents` is a link to a folder outside the project, the files under `.agents/` stop every update. Two unversioned entries run it: `hold` at `_stage == 'before'` renames only such a link to `.agents.syntek-held` and prints the hand fix, `mv .agents.syntek-held .agents`, before the render; `restore` at `_stage == 'after'`, declared before the v0.4.2 entry, renames it back (or removes the held link where the update put the identical one back) and reports anything else. Net change zero; the link's target is never touched; standard-library Python 3, always exits `0`; `--help` prints its header. D11's second, transient exception. An update that stops between the stages leaves the link held, and the next update refuses the dirty tree until that `mv` is run. A copy runs no migration: its hand recipe is in the bridge and `README.md`.
- `v0.4.2-agents-folder.py` — **every brand kind.** Releases 0.3.0 to 0.4.1 shipped `.agents` as a link to `.claude`, which makes every sandboxed Codex command fail (D76). Only where `.agents` is a symbolic link whose target is exactly `.claude` or `.claude/`, it builds the folder beside the link, swaps it in, links `.agents/skills -> ../.claude/skills`, and moves `.claude/mcp_config.json` to `.agents/mcp_config.json` where that path is free. Everything else is left and reported, with every tracked line that still describes the old layout. Standard-library Python 3, idempotent, never deletes author content, always exits `0`; `--help` prints its header. D11's first stated exception: media changes a shared path only here and, transiently, through `agents-outside-link.py`.
- **How each runs.** One `_migrations` entry per script in `copier.yml`, keyed by `version:` and run at `_stage == 'after'`, from the project root; the one exception is `agents-outside-link.py`, whose two unversioned entries run at both stages of every update. Copier runs a versioned entry only when the update crosses its version, read from the template's git tags; an update to an untagged `HEAD` still numbered below it does not, and no migration ever runs on `copier copy`.
- **By hand.** The update's clone of the template is deleted when the update ends, so each script ends by printing the command that clones the release from the source in the answers file and runs it again; `agents-outside-link.py` needs no clone, and prints its one-line `mv` instead.

## Cross-references

- `DESIGN.md` D76 — the `.agents` folder; D11 — copy-only shared paths; D32 — frozen names; Section 10 — hazards.
- `copier.yml` `_migrations` — the entries and the house shape every script follows.
- `.github/scripts/update-test.sh` — renders at the previous tag, updates across the release and proves each migration, and a second run that changes nothing.

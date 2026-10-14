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
└── v0.4.2-agents-folder.py     ← .agents -> .claude link → real .agents/ folder (D76)
```

## What's here

- `v0.4.2-agents-folder.py` — **every brand kind.** Releases 0.3.0 to 0.4.1 shipped `.agents` as a link to `.claude`, which makes every sandboxed Codex command fail (D76). Only where `.agents` is a symbolic link whose target is exactly `.claude` or `.claude/`, it builds the folder beside the link, swaps it in, links `.agents/skills -> ../.claude/skills`, and moves `.claude/mcp_config.json` to `.agents/mcp_config.json` where that path is free. Everything else is left and reported, with every tracked line that still describes the old layout. Standard-library Python 3, idempotent, never deletes author content, always exits `0`; `--help` prints its header. D11's one stated exception: media changes a shared path only here.
- **How each runs.** One `_migrations` entry per script in `copier.yml`, keyed by `version:` and run at `_stage == 'after'`, from the project root. Copier runs it only when the update crosses that version, read from the template's git tags; an update to an untagged `HEAD` still numbered below it does not, and it never runs on `copier copy`.
- **By hand.** The update's clone of the template is deleted when the update ends, so each script ends by printing the command that clones the release from the source in the answers file and runs it again.

## Cross-references

- `DESIGN.md` D76 — the `.agents` folder; D11 — copy-only shared paths; D32 — frozen names; Section 10 — hazards.
- `copier.yml` `_migrations` — the entries and the house shape every script follows.
- `.github/scripts/update-test.sh` — renders at the previous tag, updates across the release and proves each migration, and a second run that changes nothing.

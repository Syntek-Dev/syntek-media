@./CONTEXT.md

# CLAUDE.md — migrations/

Read order: `.claude/CLAUDE.md` → `CONTEXT.md` → this folder's `CONTEXT.md` (imported above) → this file → the header of the script you are about to change.

## Purpose (one line)

Carry a project across a release that moves author work, stops shipping a seed or, by a stated exception, changes a shared path, so that no update strands or breaks it.

## How to work here

- **Routing:** the rules are DESIGN.md D11, D32 and Section 10, and the decision that needs the migration; the entry and house shape are in `copier.yml` under `_migrations`; the proof is `.github/scripts/update-test.sh`.
- **Model:** **Opus** for a new migration or any change to what one moves; the mechanical tier for report wording.
- **Concrete steps:**
  1. Write it in the same change as the release that needs it, named `vX.Y.Z-<what>.sh` or `.py`, keyed to the release the change shipped in, never the release somebody noticed.
  2. Header: what moved and why the update strands it, the map, when it acts, what it never does, how it runs, `Exit codes: 0 = always`.
  3. Guard on markers, never on guesses: act only on the exact state the old release left (a link with one target, a retired folder's missing `CONTEXT.md`), and re-check it immediately before the one change.
  4. Add its `_migrations` entry: `version:`, `command:` from `<% _copier_conf.src_path %>/migrations/`, `when: "<% _stage == 'after' %>"` plus any variant test.
  5. Prove it in `update-test.sh`: render at the previous tag, set up every state the script must act on or leave, update to the snapshot tagged with `VERSION`, assert the result, then run it again and assert nothing changes.
  6. End the report with the command that runs it again.
- **Definition of done:** an update across the release fixes every project with exactly one correct result, reports every other, and a second run changes nothing.

## Guardrails

- **Always exit 0.** A non-zero exit aborts every later migration and leaves the project half-upgraded.
- **Never overwrite, never delete a file anyone wrote.** An existing destination is reported and both stay. Remove only what the old release shipped and this run replaces, after its replacement is complete.
- **Standard library only.** bash, or python3 without third-party packages.
- **Never read a git-ignored file** (D50): `git grep`, never `grep -r`.
- **No personal data.** Fixtures use invented brands and files.

## Output & naming

- **Hand-written:** `vX.Y.Z-<what>.sh` or `.py`, executable, one per change that needs one.
- **Report format:** a `▸` heading; one line per action (`removed`, `created`, `linked`, `moved`); every path left, with its reason; stale lines as `file:line`; the re-run command.

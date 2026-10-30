@./CONTEXT.md

# CLAUDE.md — migrations/

Read order: `.claude/CLAUDE.md` → `CONTEXT.md` → this folder's `CONTEXT.md` (imported above) → this file → the header of the script you are about to change.

## Purpose (one line)

Carry a project across a release that moves author work, stops shipping a seed or, by a stated exception, changes a shared path, so that no update strands or breaks it.

## How to work here

- **Routing:** the rules are DESIGN.md D11, D32 and Section 10, and the decision that needs the migration; the entry and house shape are in `copier.yml` under `_migrations`; the proof is `.github/scripts/update-test.sh`.
- **Model:** **Opus** for a new migration or any change to what one moves; the mechanical tier for report wording.
- **Concrete steps:**
  1. Write it in the same change as the release that needs it, named `vX.Y.Z-<what>.sh` or `.py`, keyed to the release the change shipped in, never the release somebody noticed. The two stated exceptions are unversioned and vendored, because each runs on every update: `agents-outside-link.py` (D76, D85) and `family-update.py`, run by the family 'update' entry (D81); never add another without the maintainer's approval and a DESIGN.md decision.
  2. Header: what moved and why the update strands it, the map, when it acts, what it never does, how it runs, `Exit codes: 0 = always` (the vendored `agents-outside-link.py` and `family-update.py` excepted: they follow syntek-author's shape).
  3. Guard on markers, never on guesses: act only on the exact state the old release left (a link with one target, a retired folder's missing `CONTEXT.md`), and re-check it immediately before the one change.
  4. Add its `_migrations` entry after the last versioned one and before the family 'update' block's BEGIN marker: `version:`, `command:` from `<% _copier_conf.src_path %>/migrations/`, `when: "<% _stage == 'after' %>"` plus any variant test. A new media script runs through `'"<% _copier_python %>" "<% _copier_conf.src_path %>/migrations/<script>.py"'`, the interpreter running Copier, as `v0.6.0` does, and so must parse and exit 0 on Python 3.10; `v0.4.2` keeps its `python3` entry (D85 as D84 amends it).
  5. Prove it in `update-test.sh`: render at the previous tag, set up every state the script must act on or leave, update to the snapshot tagged with `VERSION`, assert the result, then run it again and assert nothing changes.
  6. End the report with the command that runs it again (the vendored `agents-outside-link.py` excepted: it prints the hand fix instead; `family-update.py` prints its own report).
- **Definition of done:** an update across the release fixes every project with exactly one correct result, reports every other, and a second run changes nothing.

## Guardrails

- **Always exit 0.** A non-zero exit aborts every later migration and leaves the project half-upgraded. The vendored `agents-outside-link.py` keeps the rule where an update runs it: each stage always exits 0 (`--self-test`, which no update runs, exits 1 when a probe fails).
- **Never overwrite, never delete a file anyone wrote.** An existing destination is reported and both stay. Remove only what the old release shipped and this run replaces, after its replacement is complete.
- **Standard library only.** bash, or python3 without third-party packages. Python 3.14 is media's base since 0.6.0 (D81); a script run on Copier's own Python parses and exits 0 on Python 3.10 (no `match`, no `tomllib`, no 3.12 f-string quoting), the oldest Copier 9.12.0 supports (D84).
- **Never edit `agents-outside-link.py`, `family-update.py` or their blocks here.** They are syntek-author's family-shared bytes (syntek-author D48), vendored byte for byte from a syntek-author release tag and checked against that tag's `family-shared.json` (D81, D85): each script whole, and each block as the lines strictly between syntek-author's `# BEGIN`/`# END family-shared migrations (D48)` or `# BEGIN`/`# END family-shared update (D48)` markers in `copier.yml`; `shipped-seeds.sh` checks 21, 22 and 26 pin them, and check 20 holds the 'update' block last. Every family-shared file media carries comes from that one tag, and each adoption re-vendors and re-checks them all, with the texts that describe them; a change goes to syntek-author first and arrives with its next tag.
- **`family-refresh.json` is media's own data**, never vendored: change what the update script refreshes, restores or offers there, never in the script. Its family lists are held to the tag's by `coexist-test.sh` check 22, and its shape by `shipped-seeds.sh` check 31; an entry is offered only where the seed `template/.claude/settings.json` holds it too; the data-root guard is never listed in it (D13). An entry once listed reaches every project and cannot be withdrawn.
- **Never read a git-ignored file** (D50): `git grep`, never `grep -r`.
- **No personal data.** Fixtures use invented brands and files.

## Output & naming

- **Hand-written:** `vX.Y.Z-<what>.sh` or `.py`, executable (Git mode 100755), one per change that needs one. `agents-outside-link.py` and `family-update.py`, the two unversioned scripts, are vendored, not hand-written (D81, D85); `family-refresh.json` is data the update script reads.
- **Report format:** a `▸` heading; one line per action (`removed`, `created`, `linked`, `moved`); every path left, with its reason; stale lines as `file:line`; the re-run command (the vendored scripts excepted: they follow syntek-author's shape). A report-only crossing script (`v0.6.0-how-to.py`) acts on nothing, so it prints what it found under its heading, each list capped, and still ends with the clone-and-rerun command.

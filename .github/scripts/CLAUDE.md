@./CONTEXT.md

# CLAUDE.md — .github/scripts/

Read order: `.claude/CLAUDE.md` → `CONTEXT.md` → `.github/CONTEXT.md` → `.github/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file → the header of the script you are about
to run or change.

## Purpose (one line)

Run, read and maintain the audits that prove the template keeps every promise `DESIGN.md` makes.

## How to work here

- **Routing:** the contract → `DESIGN.md`; its transcription → `_common.sh`; one audit → its own
  header; all of them → `run-all.sh`; CI → `.github/workflows/audit-template.yml`; the
  coexistence partner → a syntek-author checkout, named with `--author DIR` (default
  `../syntek-author`) or `SYNTEK_AUTHOR_DIR`.
- **Model:** **Opus** to add or change a check, or to diagnose a failure; the mechanical tier to
  run the suite and report its output.
- **Concrete steps:**
  1. Everything: `bash .github/scripts/run-all.sh --author ../syntek-author`
     (`--no-self-test`, `--skip-integration` and `--skip-thumbnails` shorten a local loop;
     `--keep --out DIR` keeps the renders to inspect). Invoke every script with `bash` and pass
     each argument as its own word: an interactive zsh does not split a quoted pair.
  2. One audit on the source: `bash .github/scripts/<script>.sh`. One audit on renders:
     `bash .github/scripts/generate-all.sh DIR > trees.txt`, then
     `bash .github/scripts/<script>.sh $(cat trees.txt)`.
  3. Regenerate the mode-file block after adding or removing a `BUSINESS.md`, `FICTION.md` or
     `NONFICTION.md`: `bash .github/scripts/gen-mode-excludes.sh` — never type a line between
     its markers by hand.
  4. When syntek-author has moved: `bash .github/scripts/coexist-test.sh --refresh-names --author
     DIR`, re-check every new name against media's paths, and record the new baseline in
     `CHANGELOG.md`.
  5. The integration tests on one brand kind while iterating:
     `bash .github/scripts/update-test.sh --brand-kind author-fiction` and
     `bash .github/scripts/coexist-test.sh --brand-kind author-fiction --author DIR`. The toolkit
     on one render: `bash .github/scripts/toolkit-smoke.sh DIR/business--all` (about a minute a
     render; `--skip-thumbnails` drops the Chromium steps by name, `--require-ffmpeg` is CI's).
     A failed run keeps its scratch folder and names it: read the step's log there.
  6. Adding a check: give it the next number, say in the header why it exists and what it cannot
     check, add ONE mutation to the `--self-test` that produces exactly ONE finding from it, and
     run the self-test before and after.
  7. Lint after any change:
     `uvx --from shellcheck-py shellcheck -x -P SCRIPTDIR -S warning .github/scripts/*.sh`.
     Write awk that mawk also runs (no multibyte bracket classes — use `(├|└)`, not `[├└]`; no
     `{n}` intervals).
- **Definition of done:** the changed script's `--self-test` passes, and `run-all.sh` exits 0
  with no SKIP, or exits 1 only with findings that are genuinely the template's to fix.

## Guardrails

- **Fix the template, never the expectation.** A check that fails is reporting a promise the
  template broke.
- **Fix the check, never the expectation.** A self-test that stops separating good input from bad
  is a broken detector; editing the probe until it passes hides that.
- **Never mark a skip as a pass.** A skip prints `SKIP — <what> — <why>` (`skip_named`), and
  `run-all.sh` lists it as SKIP. Missing input that is not syntek-author is exit 2.
- **Never tag a release on a coexist SKIP** (DESIGN.md D27).
- **Never call a credit-spending ElevenLabs tool from a test.** Fixtures are tones and clips
  written at runtime; no script names an `mcp__elevenlabs__` tool except to check a skill's text
  or a settings file. A "take" in `toolkit-smoke.sh` is a tone or a few fake bytes.
- **A SKIP is an absent tool; n/a is an absent need.** No ffmpeg, uv, Chromium or syntek-author
  prints `SKIP — …`; a render that does not make audiobooks lists the audiobook step as n/a, which
  is not a SKIP and not a pass of anything.
- **Never write into syntek-author.** It is read through a snapshot (`sm_snapshot`) and
  `git check-ignore`; run no `git status` there, which rewrites its index.
- **Append, never renumber.** Check numbers are cited in reports, findings and other files.
- **One finding per mutation.** A probe that trips two checks proves neither; narrow the mutation
  or let one check claim the fault (a companion is check 5's, never also check 3's).
- **Self-test fixtures are written at runtime, never checked in** — a checked-in fixture drifts
  from the checks it was meant to prove.
- **Exit 2 means the run is incomplete.** Never turn a missing tool or input into a pass.
- **Mirror `DESIGN.md`, do not interpret it.** When `DESIGN.md` and `_common.sh` disagree,
  `DESIGN.md` wins and `_common.sh` changes in the same commit.
- **Never write under `template/`, and never commit a render.** Scratch goes to `${TMPDIR:-/tmp}`
  (`syntek-media-audit.XXXXXX`); `syntek-author-names.txt` is written by `--refresh-names` only.
- **No personal data, anywhere.** Fixtures use invented brands and people.

## Output & naming

- **Hand-written:** `<audit>.sh` exactly as `DESIGN.md` Section 7 names it; shared code only in
  `_common.sh`, with the `SM_`/`sm_` prefix. Finding text starts `check N — <path>` so it can be
  grepped by number; a skip reads `SKIP — <what> — <why>`.
- **Generated (never hand-edit, never commit):** renders (`<kind>--<profile>/`), their `.log`,
  `.status`, `.expect` and, over syntek-author, `.owned` sidecars, and the logs the integration
  tests keep when they fail.

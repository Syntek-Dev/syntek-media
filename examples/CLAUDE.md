@./CONTEXT.md

# CLAUDE.md — examples/

Read order: `.claude/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep one invented, valid answers file per brand kind, so a user has a `--data-file` to copy and the three together exercise every platform and every media kind.

## How to work here

- **Routing:** the questions are DESIGN.md Section 2 and `copier.yml`; the user steps are `README.md`, "Applying to a syntek-author project"; the check is `.github/scripts/generate-all.sh` check 3.
- **Model:** **Opus** for a new key or a changed value; the mechanical tier for re-ordering or re-running the check.
- **Concrete steps:**
  1. A question added to `copier.yml` gets its key in all three files, in `copier.yml`'s order, in the same change.
  2. A choice added to `PLATFORMS` or `MEDIA_KINDS` is turned on in at least one file, by its value.
  3. Render each file once from a snapshot of the working tree, with `--data-file`, and read the answers file it writes.
  4. Run `bash .github/scripts/generate-all.sh`, and its `--self-test`.
- **Definition of done:** every file renders, records exactly the questions `copier.yml` asks for its kind, and the three together still turn on every platform and every media kind of `copier.yml`'s choices.

## Guardrails

- **Invented values only in `examples/`.** No real brand, author, client, trading name, channel handle, URL, ElevenLabs voice ID or path, ever — these files are public. Use syntek-author's inventions: Harbour Lane Studio (Casey), Morgan Example, Robin Example.
- **Keys equal `copier.yml`'s questions for that kind**, and nothing else (`generate-all.sh` check 3): a missing key is asked or defaulted, so a file can fall behind `copier.yml` without a render failing.
- **Lists hold values, never labels.** `youtube`, not 'youtube — long videos, Shorts and thumbnails'; Copier refuses a label with 'Invalid choice'.
- **`SEED_EXAMPLES: false` in every file.** These are answers for a project already in use, which has no use for an invented example piece.
- **Never `--overwrite`** in any command that uses these files.

## Output & naming

- **Hand-written:** `examples/<brand-kind>.answers.yml`, where `<brand-kind>` is a `BRAND_KIND` choice, with a header saying the values are invented.
- **Generated (never commit):** a render made from one of these files goes to a temporary directory and stays there.

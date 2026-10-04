# CONTEXT.md — .github/scripts/

The audits and tests of `DESIGN.md` Section 7, one script per row, in syntek-author's house shape:
a header saying why the check exists (the failure it prevents), numbered checks, what it CANNOT
check, a `--self-test` that proves each check fires on its own mutation with exactly one finding,
and exit codes 0 (clean), 1 (findings, or a self-test that no longer separates) and 2 (could not
run). Check numbers are stable identifiers: append, never renumber. A check that could not look
for want of syntek-author prints a named SKIP, and a SKIP is never a pass.

Nothing here is rendered, and nothing here writes under `template/`.

## Directory Tree

```text
.github/scripts/
├── CONTEXT.md                ← this file
├── CLAUDE.md                 ← how to run, read, add to and change the audits
├── _common.sh                ← sourced library: copier.yml readers, DESIGN.md catalogue, harness, scope, names, fixtures
├── syntek-author-names.txt   ← syntek-author's names at the baseline, which media never takes (D27); written only by coexist-test.sh --refresh-names
├── run-all.sh                ← renders once, runs every self-test and audit, keeps PASS, FINDINGS, ERROR and SKIP apart
├── check-template-tokens.sh  ← token syntax, registration, the spine-set discipline, list-membership index gates
├── gen-mode-excludes.sh      ← writes, or --check's, copier.yml's generated BRAND_KIND mode-file block
├── docs-pairing.sh           ← folder pairs; CONTEXT, CLAUDE, workflow, guide and header shapes; piece briefs; README-only folders
├── line-cap.sh               ← 300 lines for every instructional .md
├── scrub.sh                  ← personal data, secrets, voice IDs, Claude Design links, absolute paths
├── dev-isolation.sh          ← template skills denied in the root settings; CLAUDE.md excludes
├── shipped-seeds.sh          ← seeds wired and empty; examples and shared files copy-only; the D13 settings seed
├── skill-conformance.sh      ← DESIGN.md Section 5's contract for every skill and mode file; the ElevenLabs guard
├── generate-all.sh           ← renders every BRAND_KIND × profile from a snapshot, and each over syntek-author
├── shipped-brands.sh         ← a render carries exactly its brand: skills, modes, gated paths, no syntek-author name
├── byte-identity.sh          ← shared files identical in every standalone render that ships them
├── doc-references.sh         ← every cited path and skill exists in that render; companions and syntek-author paths in prose
├── toolkit-smoke.sh          ← the toolkit's self-tests and commands on synthetic clips; ignore and LFS rules; no ElevenLabs call
├── update-test.sh            ← a real copier update keeps author work, delivers template work, refuses a BRAND_KIND change
└── coexist-test.sh           ← real syntek-author first, then media, per brand kind: both apply, both update, neither touches the other
```

## What's here

Grouped by what each script reads:

- **The template source** (`copier.yml`, `template/`, `examples/`, the root settings):
  `check-template-tokens.sh`, `gen-mode-excludes.sh`, `docs-pairing.sh`, `line-cap.sh`,
  `scrub.sh`, `dev-isolation.sh`, `shipped-seeds.sh`, `skill-conformance.sh`.
- **The renders** that `generate-all.sh` produces (twelve, named `<kind>--<profile>` because the
  kinds carry a hyphen: business, author-fiction and author-nonfiction × defaults, all, minimal,
  and over-author; `business--minimal` ships `blog` without `website`, so a file that backticks a
  path only `website` opens fails there): `shipped-brands.sh`, `byte-identity.sh` (standalone
  trees only), `doc-references.sh`, `toolkit-smoke.sh`, and `docs-pairing.sh`, `shipped-seeds.sh`,
  `skill-conformance.sh`, `line-cap.sh` again. On an over-author tree each reads `<render>.owned`,
  the files media's copy added, and checks only those.
- **Their own scratch projects**: `update-test.sh` (fifteen checks per brand kind: author work
  kept, template work delivered, a `BRAND_KIND` change refused, a removed platform taking exactly
  the files it generated — the one with the most catalogue paths, so `podcast` where a project has
  it, with a fixture show register and saved feed that must survive in its folder) and
  `coexist-test.sh` (twenty-one checks: the real syntek-author first, then media, both updated
  twice, the other order, a removed platform and media kind, syntek-author's own
  `doc-references.sh` on the composite). Their self-tests run the whole flow against the two
  fixture templates in `_common.sh` (a minimal syntek-media and a minimal syntek-author), so they
  prove the harness even while the real template is incomplete. `coexist-test.sh` and the
  over-author renders need a syntek-author checkout (`--author DIR`, `SYNTEK_AUTHOR_DIR`, or
  `../syntek-author`) and SKIP, named, without one.
- **`toolkit-smoke.sh`** copies each render into a scratch Git repository and runs its toolkit for
  real on clips, tones and stills made with `ffmpeg -f lavfi` — never an ElevenLabs call; since
  0.2.0 that includes `image` in every format, the newsletter GIF read from its own loop
  extension, the silent loop and web video, the podcast feed end to end offline on a fixture show,
  and the published transcript (checks 15–19). It records what each step did in a results file and
  judges that; its self-test writes a clean results file at run time and mutates one fact per
  probe, so it needs no ffmpeg or Chromium. A missing tool is a named SKIP; a step a render does
  not need (no audiobook folder) is n/a.
- **`_common.sh`** is the single reader of `copier.yml` (list items, registered keys, question
  choices, gated paths, gate negation with list membership) and the single transcription of
  `DESIGN.md` (the skill catalogue, every gated path, the seeds, the examples, the ten shared
  files, the spine set, the companions, the D13 settings lists and the `_message_after_copy`
  lines). **It changes in the same commit as `DESIGN.md`.**
- **`syntek-author-names.txt`** is never transcribed by hand: `coexist-test.sh --refresh-names
  --author DIR` writes it (a dated header naming syntek-author's commit "plus working tree", then
  one sorted `top`, `claude`, `skill` or `rules` line per name). `shipped-brands.sh` check 11 and
  `skill-conformance.sh` check 20 read it on every run (a missing file is exit 2, never a SKIP),
  and `coexist-test.sh` check 20 fails when the live syntek-author tree has moved past it.
- **`_common.sh`'s last two sections** hold what the integration tests share (which files a
  template owns, what a step changed, a byte fingerprint of a tree, conflicts, a Copier message
  without Copier's file lines, a gated value an update can take away) and the reader of
  `copier.yml`'s LFS tripwire task, which `toolkit-smoke.sh` check 8 applies as written.

## The spine set, as the audits compute it

`DESIGN.md` Section 2 allows variant tokens and conditional blocks only in the spine set. The
audits compute it from `DESIGN.md` and `copier.yml` together: the root spine (the eight rules
files and the answers file); the ten copy-only shared files; every `_skip_if_exists` seed; every
seed-once example; and every index file — a `CONTEXT.md` or `CLAUDE.md` whose folder holds a
gated descendant. An index file's gates must be shipping gates: a `BRAND_KIND` mode gate, list
membership exactly as `DESIGN.md` Section 3.5 writes it (`'youtube' in PLATFORMS`), or the
negation of a templated `_exclude` line — never a copy-only or seed-once gate.

## Cross-references

- `DESIGN.md` Section 7 — the audit list and the over-author scope; Sections 2–6 — the contract
  the audits check; D27 — the frozen names and the SKIP rule.
- `copier.yml` — read by most scripts; written only by `gen-mode-excludes.sh`, between its markers.
- `examples/` — the three invented answers files `generate-all.sh` check 3 holds to the questions.
- `.github/workflows/audit-template.yml` — runs these scripts in CI.

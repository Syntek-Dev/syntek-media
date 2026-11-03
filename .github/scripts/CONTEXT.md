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
├── _common.sh                ← sourced library: copier.yml readers, DESIGN.md catalogue, the family-shared set and its manifest reader, harness, scope, names, fixtures
├── syntek-author-names.txt   ← syntek-author's names at the baseline, which media never takes (D27); written only by coexist-test.sh --refresh-names
├── run-all.sh                ← renders once, runs every self-test (the four vendored family scripts' too) and audit, keeps PASS, FINDINGS, ERROR and SKIP apart, and names and counts every SKIP
├── check-template-tokens.sh  ← token syntax, registration, the spine-set discipline, list-membership index gates; the rules' frontmatter closed and token-free (D87)
├── gen-mode-excludes.sh      ← writes, or --check's, copier.yml's generated BRAND_KIND mode-file block (MEDIA-*.md beside the family skills included)
├── docs-pairing.sh           ← folder pairs; CONTEXT, CLAUDE, workflow, guide and header shapes, media's how-to procedures and guides included; piece briefs; README-only folders; every shown Copier command run as uvx --python '>=3.14' copier (check 20)
├── line-cap.sh               ← 300 lines for every instructional .md, the chapters under how-to/src/ included
├── scrub.sh                  ← personal data, secrets, voice IDs, Claude Design links, absolute paths
├── dev-isolation.sh          ← template skills (media's thirteen and the seven family skills) denied and off in the root settings; CLAUDE.md excludes; Codex product-skill exclusions, development entrypoints and the real .agents/ folder
├── community-files.sh        ← the root's community files (D83): all present as files, not links, LICENSE byte-exact, no Markdown in ISSUE_TEMPLATE/, issue forms and config.yml, one address, private reporting
├── shipped-seeds.sh          ← seeds wired and empty; copy-only files; D13 settings; output README negations above gates; family-shared.json and every vendored file and block it records (--write-manifest writes it); D86's data-root map, and in a render each mapped folder present with its storage manifest committable; in a render, only media's own seed rules wait for the permissions script's --write; the baseline task, the refresh data and the v0.6.0 entry; nothing under learning/ and the frozen name kept; the v0.7.0 entry and its report script; rules 04's globs, none dead and no toolkit workflow left out (D87)
├── skill-conformance.sh      ← DESIGN.md Section 5's contract for every skill and mode file (the family skills' vendored H1, locale and Mode paragraph excepted); the ElevenLabs guard; media-teach's placement words, and no other media skill or mode file naming learning/
├── generate-all.sh           ← renders every BRAND_KIND × profile from a snapshot, and each over syntek-author
├── shipped-brands.sh         ← skills, modes, gates (AGENT_CLIENTS's included), no syntek-author name but the family's; output folders ship only their README; nothing under how-to/ outside the family's paths and media's three folders; nothing at or under learning/; the start-up budget, media's share within the family ceiling and rules 04's frontmatter (D87, D88)
├── byte-identity.sh          ← shared files identical in every standalone render that ships them
├── doc-references.sh         ← every cited path and skill exists in that render; companions and syntek-author paths, its how-to folders included, in prose (family-shared text excepted)
├── toolkit-smoke.sh          ← the toolkit's self-tests and commands on synthetic clips; ignore and LFS rules; footage verify on the data root; MEDIA_CHROMIUM's errors; no ElevenLabs call
├── update-test.sh            ← a real copier update keeps author work, lessons included, delivers template work, refuses a BRAND_KIND change; the v0.7.0 report
└── coexist-test.sh           ← real syntek-author first, then media, per brand kind: both apply, both update, neither touches the other, nor the lessons; media's family-shared.json against the --author tree's; the two data-root maps never overlap; neither update strips the other's rules frontmatter (D87); media's share within the family ceiling (D88)
```

## What's here

Grouped by what each script reads:

- **The template source** (`copier.yml`, `template/`, `examples/`, the root settings and
  community files, and the root `family-shared.json`): `check-template-tokens.sh`,
  `gen-mode-excludes.sh`, `docs-pairing.sh`, `line-cap.sh`, `scrub.sh`, `dev-isolation.sh`,
  `community-files.sh`, `shipped-seeds.sh`, `skill-conformance.sh`. `community-files.sh` is the one audit of the root's GitHub files
  (D83); it holds the approved `LICENSE` text itself, pinned by its sha256, and reads the issue
  forms with a top-level-key reader in awk, since the source job installs no YAML library.
  `docs-pairing.sh` check 20 (D3, D81), ported from syntek-author's check 21, holds every shown
  Copier copy, update or recopy command to `uvx --python '>=3.14' copier`, quoted
  (`SM_UVX_COPIER`): in every text file of a tree and, run on the source, in every file of the
  repository outside `template/` that Git holds or would add, the community files and the
  `README.md` included, but never `CHANGELOG.md` or this folder. A printf placeholder beside the
  quoted minimum, the `'>=%s'` of a script that sets `PYTHON_MIN = (3, 14)`, and the bare form
  on a comment or a line pointing to a section ('see', 'gives' or 'shows') pass
  (`.claude/CLAUDE.md` Section 9).
- **The family-shared set** (DESIGN.md D80, D85; syntek-author D48): the files and blocks media
  vendors byte for byte from one syntek-author tag. The root `family-shared.json` records them
  in the family's own format (owner `syntek-media`, each file's source, bytes, sha256 and mode,
  the link's target, each block's markers, bytes and sha256, and `rules-web-tools`'s
  `destination`), so that syntek-author's `family-shared.sh --sibling` can read it too.
  Today the set is 43 files and four blocks ('questions', 'migrations', 'update' and
  'rules-web-tools') from syntek-author's `v0.9.1` tag (`SM_FAMILY_RELEASE`).
  `shipped-seeds.sh --write-manifest` alone writes it, after a re-vendor; `shipped-seeds.sh`
  checks 21–27 hold the vendored files, the four blocks and the renders to it, and
  `coexist-test.sh` check 22 holds it, entry by entry, to the `--author` tree's own manifest (in
  CI the pinned tag, `SYNTEK_AUTHOR_TAG`). No hash is copied into a script. One list,
  `SM_FAMILY_SHARED` in `_common.sh`, drives every audit's family exemption: the D27 name checks
  (`shipped-brands.sh` 3, 5, 11 and 13, `skill-conformance.sh` 8, 9, 14 and 20,
  `coexist-test.sh` 13), and `doc-references.sh` 5 and 6, which never read a family file's
  text. `run-all.sh` runs the vendored outside-link script's, data-root resolver's,
  permissions script's and, since 0.6.0, update script's (`migrations/family-update.py`) own
  `--self-test`, with `SYNTEK_DATA_ROOT` unset (D81). What is media's own around that script
  is held by `shipped-seeds.sh` checks 30–32: the `baseline` task last in `_tasks`, line for
  line as `SM_BASELINE_TASK` transcribes it from the tag (30); `migrations/family-refresh.json`,
  the refresh data no manifest lists (31); the `v0.6.0` entry's place in `_migrations` (32);
  and, since 0.7.0 (D86), the `v0.7.0` entry's place and its report script, which parses as
  Python 3.10, names no lesson and writes nothing (36).
- **The learning folder** (D86; syntek-author D57): media ships nothing under `learning/`, and
  `media-teach` places lessons there at run time, the one run-time exception to the frozen name
  'top learning'. `shipped-brands.sh` check 17 refuses a rendered path there; `shipped-seeds.sh`
  checks 33 and 34 keep it out of `copier.yml`, the refresh data and `template/`, and keep the
  name frozen and excepted from no list; `skill-conformance.sh` checks 22 and 23 hold
  `media-teach`'s placement words and keep every other skill and mode file off the folder;
  `doc-references.sh` checks 1 and 6 hold the placeholders unchanged (its self-test proves a
  backticked `learning/CLAUDE.md` is a finding); `update-test.sh` check 25 and `coexist-test.sh`
  checks 26 and 27 plant lessons and prove every byte survives copies and updates, and that
  syntek-author's pair and media's render record are untouched.
- **The data root** (D86): `shipped-seeds.sh` check 28 holds media's map to exactly its one
  footage folder and two evidence roles, and check 35 proves in every render that the folder
  stands and its storage manifest is not ignored; `coexist-test.sh` check 28 proves the two
  maps never overlap and that syntek-author's own resolver reads media's; `toolkit-smoke.sh`
  check 30 runs `footage verify` under both stores, and the command its warning names.
- **The start-up budget and the scoped rule** (D87; syntek-author D59): rules 04 alone opens
  with `paths` frontmatter, and `_common.sh` transcribes DESIGN.md Section 4.1's list as
  `SM_RULE_PATHS_04`. `check-template-tokens.sh` check 10 keeps every rules file's frontmatter
  closed and free of delimiters; `shipped-brands.sh` checks 18 and 19, ported from
  syntek-author's checks 24 and 25 (its regex byte for byte, counting characters), hold a
  standalone render's always-loaded set to `SM_STARTUP_BUDGET`, the scoped rule to
  `SM_SCOPED_LIMIT` and its frontmatter to the list, and log every render's total, over
  syntek-author never a finding; check 18 also holds media's unscoped share, in every render,
  to `SM_COMPANION_SHARE`, the family ceiling agreed with syntek-author (D88); `shipped-seeds.sh`
  check 37 proves on the source that no glob is dead and no toolkit workflow is left out; and
  `coexist-test.sh` check 29 proves neither update strips or adds either template's frontmatter,
  and check 30 holds media's share to the same cap in both orders after both updates (D88).
- **The user guide** (D84): `docs-pairing.sh` reads the family's pairs under `how-to/` as any
  pair, and its checks 12–17 reach media's procedures and guides there; `line-cap.sh` caps the
  chapters of `how-to/src/`, which are instructional; `doc-references.sh` check 6 treats
  syntek-author's guide folders under `how-to/` as syntek-author paths; and `shipped-brands.sh`
  check 16 refuses a path media ships there outside the family's thirteen and media's three
  `syntek-media/` folders.
- **The renders** that `generate-all.sh` produces (twelve, named `<kind>--<profile>` because the
  kinds carry a hyphen: business, author-fiction and author-nonfiction × defaults, all, minimal,
  and over-author; `business--minimal` ships `blog` without `website`, so a file that backticks a
  path only `website` opens fails there): `shipped-brands.sh`, `byte-identity.sh` (standalone
  trees only), `doc-references.sh`, `toolkit-smoke.sh`, and `docs-pairing.sh`, `shipped-seeds.sh`,
  `skill-conformance.sh`, `line-cap.sh` again. On an over-author tree each reads `<render>.owned`,
  the files media's copy added, and checks only those.
- **Their own scratch projects**: `update-test.sh` (twenty-six checks per brand kind: author
  work kept, template work delivered, a `BRAND_KIND` change refused, agent copy/update
  preservation, the v0.4.2 `.agents` migration (converted, idempotent, other shapes left alone)
  and D76's outside-link hold and restore, the hand fix the hold stage itself prints and no bare
  `mv` anywhere else, the crash pointer the update prints, a stop after the render undone by the
  hand fix step by step, with `.agents` absent after the stop and standing again after a discard
  (the bare `mv`'s hazard shown in a control, and a held link committed beside `.agents`
  reported, not moved), a removed platform taking exactly the files it generated — the one with
  the most catalogue paths, so `podcast` where a project has it, with a fixture show register
  and saved feed that must survive in its folder, and, since 0.5.0, a project copied at the
  newest earlier release tag and updated to the working tree, standalone and over
  syntek-author: the clients and store the family questions default to recorded, no client file
  written, the update script run, no copy-only family file created but those the update script
  may write where the project never had them, media's own files delivered, the after-update
  message printed, and, where the update crosses 0.6.0, the guide delivered and the crossing
  report printed; since 0.7.0 planted lessons kept byte for byte through two updates, and,
  where the update crosses 0.7.0, the v0.7.0 report printed once, the footage folder's records
  left as they were) and
  `coexist-test.sh` (thirty checks per brand kind, 13, 20, 22 and 23 once per run: the
  real syntek-author first, then media, both updated twice, the other order, a removed platform
  and media kind, syntek-author's own `doc-references.sh` on the composite, the vendored set
  against its manifest, D84's warning on a copy over a syntek-author without its guide,
  syntek-author's `make lint` and `make flags` on media's chapters, each hook entry and MCP
  server standing once in both orders, and, since 0.7.0, lessons in every placement kept
  through both copies and updates in both orders, syntek-author's `learning/` pair and media's
  render record untouched, and the two data-root maps apart under either store; since 0.8.0,
  both templates' rules frontmatter kept through both updates, the composite's total logged;
  since D88, media's unscoped share within the family ceiling). Their self-tests run the whole flow against the two
  fixture templates in `_common.sh` (a minimal syntek-media and a minimal syntek-author), so they
  prove the harness even while the real template is incomplete. `coexist-test.sh`, the
  over-author renders and the over-author half of `update-test.sh` check 24 need a syntek-author
  checkout (`--author DIR`, `SYNTEK_AUTHOR_DIR`, or `../syntek-author`) and SKIP, named, without
  one; `update-test.sh` check 24 also SKIPs, named, where the repository has no release tag
  older than `VERSION`, and `coexist-test.sh` check 24 where the `--author` tree is older than
  v0.6.0 or `make` is missing.
- **`toolkit-smoke.sh`** copies each render into a scratch Git repository and runs its toolkit for
  real on clips, tones and stills made with `ffmpeg -f lavfi` — never an ElevenLabs call; since
  0.2.0 that includes `image` in every format, the newsletter GIF read from its own loop
  extension, the silent loop and web video, the podcast feed end to end offline on a fixture show,
  and the published transcript (checks 15–19), plus offline voice preparation and the Git-clean
  timing overwrite guard (checks 20 and 23), known-word alignment and captions from words (22),
  real-source asset hashes and offline footage-image metadata, with video/sound refusals (24),
  native Rhubarb mouth cues (21), and optional/broken WhisperX and Rhubarb setup checks (26). No audit fetches models or builds WhisperX; live alignment needs
  a prepared user interpreter or SKIPs by name. Check 27 observes ffmpeg in the requested
  systemd memory scope, requires zero swap and checks the uncapped note; scope-dependent cases
  SKIP by name without a user service manager. Browser scripts run from one fixed, locked cache
  workspace across renders, using the toolkit's uv helper rather than building an environment
  per temporary copy. Check 28 draws two-board CSS-sprite fixtures at two native aspects, reads
  mouth pixels independently, tests box findings/missing art, and verifies frame count, sound
  length and loudness on both masters. Check 30 (D86) logs a clip and runs `footage verify`
  under `external`, with a root of its own, and under `repo`, and runs the `add` its warning
  names; check 31 sets `MEDIA_CHROMIUM` to each bad value and a stand-in that will not start,
  for `card.py`, `scene.py` and `check --setup`. The driver unsets `MEDIA_CHROMIUM` and
  `SYNTEK_DATA_ROOT` first, so no other check sees either. It records each step in a results file and
  judges that; its self-test writes a clean results file at run time and mutates one fact per
  probe, so it needs no ffmpeg or Chromium. A missing tool is a named SKIP; a step a render does
  not need (no audiobook folder) is n/a.
- **Python 3.14** (D81): `_common.sh` holds the one copy of the floor, `SM_PYTHON_MIN`, pins
  `UV_PYTHON` to `python3` where it is unset (CI sets it to 3.14), and refuses an older
  `python3` or `UV_PYTHON` with exit 2 before anything runs, so every Copier the audits run, and
  the family scripts inside it, runs on 3.14.
- **`_common.sh`** is the single reader of `copier.yml` (list items, registered keys, question
  choices, gated paths, gate negation with list membership) and the single transcription of
  `DESIGN.md` (the skill catalogue and the family skills, every gated path, the seeds, the
  examples, the copy-only shared paths and the two client folders' update gates, the spine set,
  the companions, the D13 settings lists with the family's asks, deny and hooks, the
  `_message_after_copy` lines, the family-shared set, the D83 community files with the
  private-reporting URL and, since 0.8.0, D87's `SM_STARTUP_BUDGET`, `SM_SCOPED_LIMIT`,
  `SM_SCOPED_RULES` and `SM_RULE_PATHS_04`). **It changes in the same commit as `DESIGN.md`.**
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
files and the answers file); the fifty copy-only shared paths (D11's nineteen, D80's seventeen
and D84's fourteen: the family client files that carry the shared question keys among them); every
`_skip_if_exists` seed; every seed-once example; and every index file — a `CONTEXT.md` or
`CLAUDE.md` whose folder holds a gated descendant. An index file's gates must be shipping gates:
a `BRAND_KIND` mode gate, list membership exactly as `DESIGN.md` Section 3.5 writes it
(`'youtube' in PLATFORMS`, `'codex' in AGENT_CLIENTS`), or the negation of a templated
`_exclude` line — never a copy-only or seed-once gate.

## Cross-references

- `DESIGN.md` Section 7 — the audit list and the over-author scope; Sections 2–6 — the contract
  the audits check; D27 — the frozen names and the SKIP rule; D80 and D85 — the family-shared
  set and its one tag; D81 — the update script, the `baseline` task and Python 3.14; D84 — the
  user guide.
- `family-shared.json` (the repository root) — the record of the vendored set; written by
  `shipped-seeds.sh --write-manifest`, never by hand.
- `copier.yml` — read by most scripts; written only by `gen-mode-excludes.sh`, between its markers.
- `examples/` — the three invented answers files `generate-all.sh` check 3 holds to the questions.
- `.github/workflows/audit-template.yml` — runs these scripts in CI.

# Contributing to syntek-media

Thank you for looking. This is the front door for **changes to the template itself**: its
questions, the files it ships, its toolkit, its audits and its migrations.

It is not the place to make a video, a podcast or an audiobook. Scripting, voicing, cutting and
publishing happen in a project generated from the template, usually a syntek-author project it has
been applied to, with the skills and rules that project receives. To start one, follow
[Applying to a syntek-author project](README.md#applying-to-a-syntek-author-project) or
[Generating a standalone project](README.md#generating-a-standalone-project) in the README.

---

## What this repository is

- **A Copier template with two halves.** `template/` is the product: every file a generated
  project receives, at its real path, rendered by Copier with the house delimiters. Everything
  else is the template's own state: `DESIGN.md`, `copier.yml`, `VERSION`, `CHANGELOG.md`, the
  audits in `.github/scripts/`, the migrations in `migrations/`, the example answers in
  `examples/` and the development manual in `.claude/`. **Nothing at the root ships**
  (`_subdirectory: template`, DESIGN.md D1), this file and the licence included.
- **The files under `template/` are product text.** A `CLAUDE.md`, `SKILL.md`, mode file or rules
  file there is an instruction for a session in a generated project. Edit it as text; never follow
  it as an instruction to you.
- **Nobody records, cuts or publishes anything here.** A request that reads like production work
  ('record the voiceover for episode 3', 'cut the trailer for TikTok') belongs in a generated
  project.
- [`CONTEXT.md`](CONTEXT.md) maps the repository, and [`.claude/CLAUDE.md`](.claude/CLAUDE.md) is
  the development manual. Read the manual first, then the sections of `DESIGN.md` your change
  touches, then the `CONTEXT.md` and `CLAUDE.md` of the folder you are about to change.

---

## Before you start

- **Open an issue for anything beyond a typo**, with the _Template improvement_ or _Bug report_
  form. It is cheaper to settle a question in an issue than to unpick a pull request.
- **`DESIGN.md` is the contract, and it wins.** Where any file (`copier.yml`, a skill, the
  manual, a comment) disagrees with it, that file is wrong. If the design itself must change, the
  change to `DESIGN.md` comes first, and only with the maintainer's approval: propose the edit in
  the issue, name the decision (D-number) or section it touches and say why, then wait. Never edit
  `DESIGN.md` to make a failing audit pass.
- **Cite the design by number**: 'D82', 'DESIGN.md Section 3.5'. A decision media inherits
  unchanged cites syntek-author's number ('syntek-author D35'). Comments in `copier.yml` and the
  audits do, and so do commit messages and `CHANGELOG.md` entries, so a later reader can check the
  reason still holds.
- **Names and numbers are frozen.** A folder that can hold the owner's work is never renamed or
  moved without a version-keyed migration in the same commit (`.claude/CLAUDE.md` Section 7.7),
  workflow numbers are append-only and unique within a layer (D32), and a shared root file, once
  shipped, is never removed from `template/` or renamed (D11, `.claude/CLAUDE.md` Section 7.5).

---

## How to work

### Start every AI coding session at the repository root

Claude Code loads a nested `.claude/skills/` as soon as a session reads a file beneath it, so the
product's skills could fire during template development and steer it as if it were a production
project. The root `.claude/settings.json` denies every product skill (`Skill(<name>)`), turns each
one off in `skillOverrides` and keeps the `CLAUDE.md` files under `template/` out of the session
(`claudeMdExcludes`). The root `.agents/` is a real folder holding only its pair (D76), so Codex and
Antigravity find no product skill from there either; a session started inside `template/` finds
them all.

- Never invoke a template skill. If one ever appears invocable, the deny list has a gap: stop and
  report it.
- Codex honours `[[skills.config]]` only from the user config and `-c` flags, never from a project
  file, so `.codex/CLAUDE.md` gives the user-level rule to copy into yours.
- A new template skill needs its deny line, its `skillOverrides` entry and its line in that Codex
  recipe. That changes this repository's permission settings, so propose the exact lines and leave
  the edit to the maintainer (`.claude/CLAUDE.md` Section 3).
- Never run `code-review-graph install` here: it writes hooks, skills and rules-file text the dev
  isolation refuses (`.claude/CONTEXT.md`).

### No paid calls, no media files

- **Never call ElevenLabs or any other paid API**, from a session, a test or a script. Nothing
  here needs one: tests use tones, clips and stills made at run time (`ffmpeg -f lavfi`), and a
  skill's handling of the server is proved on the files around the call.
- **Never commit rendered output, audio, video, images or fonts.** `template/` ships no binary: a
  layout is HTML and CSS, and a fixture is generated at run time. Renders, logs and scratch
  projects go under a temporary directory and stay there (`.claude/CLAUDE.md` Section 8).

### Token discipline

Every file under `template/` is rendered with the house delimiters. Only registered tokens may
appear inside one: the question keys of `copier.yml`, plus `_copier_operation`, `_copier_answers`
and `_copier_conf`. Never write a delimiter you do not mean, and never put a token inside `_…_`
emphasis, which a formatter rewrites. Variant tokens and blocks belong only in the spine set and in
index files, where each gated row is wrapped in the exact gate of DESIGN.md Section 3.5; every
other shipped file is byte-identical in every render that ships it, so a brand-kind difference
goes in a mode file and a platform or media-kind difference in a gated file, never in a
conditional. The delimiters and the full rules are in `.claude/CLAUDE.md` Section 4;
`check-template-tokens.sh` and `byte-identity.sh` enforce them.

### Personal data never enters `template/` or `examples/`

- No real brand or person, channel handles or URLs, platform account IDs, ElevenLabs voice IDs or
  API keys, Claude Design links, follower or view counts, prices, credentials, absolute paths or
  syntek-base's name (D36, `.claude/CLAUDE.md` Section 5). Use the `BRAND_NAME`, `OWNER_NAME` and
  `OWNER_FIRST_NAME` tokens.
- Examples use invented brands and people only: Harbour Lane Studio, Morgan Example and Robin
  Example, syntek-author's own inventions, so a combined render tells one story. Never fabricate a
  statistic, quotation, testimonial, platform rule or limit: use a clearly marked placeholder and a
  `VERIFY` flag. Platform limits live, dated and sourced, in `template/toolkit/data/platforms.toml`,
  never as numbers in a guide (D26).
- Seeds ship empty of entries. A seed is a one-way door: once a project has it, no update can
  correct it.
- `scrub.sh` fails the build on a hit, a run of seven or more digits included. Fix the hit at its
  source; never allow-list it. Never paste a piece's script or transcript, a recording or a key
  into an issue either.

### Living beside syntek-author

- **Check every new name first.** A new top-level folder, `.claude/` path, skill folder or rules
  file is checked against `.github/scripts/syntek-author-names.txt` before it is written (D27): an
  update over a syntek-author project overwrites a same-named file and leaves conflict markers in
  it (DESIGN.md Section 10). Only `coexist-test.sh --refresh-names` rewrites the names file.
- **syntek-author and syntek-base are read-only from here.** Read them to port a format; never
  change them. syntek-author is still moving, so re-read its `DESIGN.md` and the file you copy
  before you port it, and record any drift that changes this contract in `CHANGELOG.md`.
- **Companions are named, never shipped** (D10): in prose, never backticked and never in
  `skills:`, as 'the spelling skill (syntek-author), where present'.

### House formats, in brief

- Every directory under `template/` has a `CONTEXT.md` and `CLAUDE.md` pair, apart from the
  declared exceptions `docs-pairing.sh` names (D42).
- Every instructional Markdown file stays within 300 lines (D31).
- British English (en_GB), single quotation marks, DD/MM/YYYY in prose, `DD-MM-YYYY` in
  filenames, timecodes `HH:MM:SS.mmm`, and 'Section 3.2', never the section sign.
- A workflow is cited by its full folder name (`production/workflows/02-make-a-voiceover/`), never
  by its number alone (D32).
- Metadata headers, workflow folders, guides, skills and mode files follow DESIGN.md Sections 4
  and 5; `.claude/CLAUDE.md` Section 6 is the checklist.

### Recipes

`.claude/CLAUDE.md` Section 7 holds the step-by-step recipes: add a skill, a mode file, a gated
path, a workflow, a seed, a question, a platform or a media kind; rename or move a folder (avoid
it). Each ends with the audits and a `CHANGELOG.md` entry. The mode-file block of `copier.yml` is
generated by `gen-mode-excludes.sh`; never type a line in it.

---

## Testing

With a syntek-author checkout beside this one, one command renders every brand kind in three
profiles and over syntek-author, from a copy of your working tree into a temporary directory, and
runs every self-test and audit against those renders, then the update and coexistence tests:

```bash
git clone https://github.com/Syntek-Dev/syntek-author ../syntek-author
bash .github/scripts/run-all.sh --author ../syntek-author
```

It exits `0` when everything passes, `1` on a finding and `2` when something could not run.

- **A SKIP is never a pass.** Without a syntek-author checkout, the renders over it and
  `coexist-test.sh` print a named SKIP, and no release is tagged while `coexist-test.sh` reports
  one (D27).
- **Fix the template, never the expectation** (`.github/CLAUDE.md`). Changing an audit, run its
  `--self-test` before and after the change; check numbers are appended, never renumbered.
- **A quicker loop while you work:** `--no-self-test` (never in CI), `--skip-integration` (skips
  `update-test.sh` and `coexist-test.sh`), `--skip-thumbnails` (drops the Chromium steps),
  `--out DIR --keep` to inspect the renders, `--quiet` for failures and the summary only.

One audit at a time: a source audit as `bash .github/scripts/<script>.sh`; a per-tree audit on the
trees `generate-all.sh` prints, one path per line. Each script's header says what its numbered
checks mean; [`.github/scripts/CONTEXT.md`](.github/scripts/CONTEXT.md) lists them all, and
`community-files.sh` checks the root community files, this one included. A change to
`copier.yml`, a gate or a seed is not done until a render proves it. CI
(`.github/workflows/audit-template.yml`) runs everything on every push to every branch.

**What the tools need.** Versions follow the README's [Requirements](README.md#requirements) and
the CI workflow:

| Tool | Needed for |
|---|---|
| bash and rsync | The runner and the renders |
| git, with a user name and email set | Copier reads the template over git and commits in the update and coexistence tests' scratch repositories |
| [uv](https://docs.astral.sh/uv/) (`uvx`) | Copier 9.6.0 or newer (`_min_copier_version` in `copier.yml`), and the toolkit's browser scripts |
| Python 3.11 or newer (CI uses 3.12) | The toolkit, the migrations and the audits' helpers |
| ffmpeg and ffprobe, with libass, x264 and mp3lame | `toolkit-smoke.sh`; without them it prints a named SKIP |
| Playwright 1.63.0's Chromium | Cards, thumbnails and scenes in `toolkit-smoke.sh`; `--skip-thumbnails` drops them |
| Rhubarb and a WhisperX interpreter (optional) | Their `toolkit-smoke.sh` checks, which SKIP by name without them |
| A network connection | The first time `uvx` fetches each tool, and the syntek-author clone |

---

## Pull requests

- **Work on a branch from `main`**, named for its kind: `feat/…`, `fix/…`, `docs/…`, `chore/…`.
- **Commit subjects follow [Conventional Commits](https://www.conventionalcommits.org/)**:
  `feat: …`, `fix(toolkit): …`, `chore(audit): …`, `chore(dev): …`, `docs(changelog): …`,
  `ci: …`. Name the decision in the subject or body where one applies.
- **One concern per pull request.**
- **Add a `CHANGELOG.md` entry under `[Unreleased]`**, in the section that fits (Added, Changed,
  Fixed, Deferred), citing the decision or section.
- **A change to `DESIGN.md` changes `.github/scripts/_common.sh` in the same commit**, where the
  audits' transcription of the catalogue has to follow it (`.github/CONTEXT.md`).
- **Do not bump the version.** `VERSION` and `CHANGELOG.md` move together in the maintainer's
  release commit, and the maintainer tags releases (`.claude/CLAUDE.md` Section 9).
- **CI must be green.** Its three jobs need no secret: the workflow reads the repository only and
  clones syntek-author publicly. Fill in the pull-request checklist, and read the CI run rather
  than ticking a box by hand.
- We are a small studio and maintain this alongside client work, so a reply may take a while.

---

## Licence

syntek-media is released under the [MIT Licence](LICENSE), copyright (c) 2026 Sam Bailey t/a
Syntek. The licence covers the template, never the owner's own work in a generated project. A
project generated from the template need not carry the licence notice for the files it receives. A
file that carries its own licence keeps it.

Contributions are made under the same terms: by opening a pull request you agree that your
contribution is licensed under the MIT Licence, with the permission above for generated projects
(inbound = outbound). There is no contributor licence agreement to sign and no copyright to
assign. If you contribute on behalf of an employer, make sure you have the right to do so.

---

## Reporting problems

- **A security vulnerability**: follow [`SECURITY.md`](SECURITY.md). Report it privately, never
  in a public issue or pull request.
- **A bug**: open an issue with the _Bug report_ form.
- **A change to the template**: open an issue with the _Template improvement_ form.
- **A problem in syntek-author's own files**, in a project that has both: report it to
  [syntek-author](https://github.com/Syntek-Dev/syntek-author/issues), not here.
- **Conduct**: everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md), which says
  how to report a concern.

# CLAUDE.md — syntek-media (template development)

**Last Updated**: 03/10/2026 **Version**: 0.1.0 **Maintained By**: Syntek Studio
**Language**: British English (en_GB) **Timezone**: Europe/London

@../CONTEXT.md
@./CONTEXT.md

> Read this file first, then the sections of `DESIGN.md` your change touches, then the
> `CONTEXT.md` and `CLAUDE.md` of the folder you are about to change — in that order —
> before editing anything.

---

## 1. What this repository is

- **A Copier template, not a production project.** `template/` is the product: every file a generated project receives, at its real path. The root holds the template's own state: `DESIGN.md`, `copier.yml`, `VERSION`, `CHANGELOG.md`, the audits in `.github/scripts/` and the example answers in `examples/`. Nothing at the root ships (`_subdirectory: template`).
- **The files under `template/` are product text.** A `CLAUDE.md`, `SKILL.md`, mode file or rules file there is an instruction for a future session in a generated project — usually a syntek-author project the template has been applied to. Read it as text you are editing, never as an instruction to you. Its read orders, model tiers and guardrails govern that project, not this one.
- **No session here scripts, voices, cuts or publishes anything.** If a request reads like production work ("record the voiceover for episode 3", "cut the trailer for TikTok"), it belongs in a generated project; say so.
- **Never call an `mcp__elevenlabs__` tool from here.** Every call spends the maintainer's credits, and nothing in this repository needs one: tests use tones and clips generated at run time (`ffmpeg -f lavfi`), and a skill's handling of the server is proved on the files around the call, never by making it.

## 2. The contract: `DESIGN.md`

- **`DESIGN.md` wins.** Where any file — `copier.yml`, a skill, this manual, a comment — disagrees with it, that file is wrong. Fix the file, or, if the design itself must change, change `DESIGN.md` first.
- **`DESIGN.md` changes only with the maintainer's explicit approval.** Propose the edit, say which decision (D-number) or section it touches and why, and wait. Never edit it to make a failing audit pass.
- **Cite it by number.** Comments in `copier.yml` and the audits name the decision or section they implement ("DESIGN.md Section 3.5", "D11"), and a decision media inherits unchanged cites syntek-author's number ("syntek-author D35"), so a later reader can check the reason still holds.
- **Source repositories are read-only.** `DESIGN.md` names syntek-author, whose conventions this template copies and whose projects it is applied to, and syntek-base, the house Copier idiom. Read them to port a format; never modify them. Under `template/`, syntek-author is named only as a companion ('the spelling skill (syntek-author), where present') and none of its paths, files or skills is backticked; syntek-base is never named there.
- **syntek-author is still moving.** Before you port a format, re-read its `DESIGN.md` and the file you are copying, and record any drift that changes this contract in `CHANGELOG.md`.

## 3. Dev isolation

Claude Code loads a nested `.claude/skills/` the first time a session reads a file beneath it, and nested `CLAUDE.md` files on demand. Without isolation, opening `template/` would load the product's skills and manuals into this session, where they would fire on description match and steer template development as if it were a production project.

- **Layer 1 — `.claude/settings.json` denies `Skill(<name>)` for every skill under `template/.claude/skills/`**, the ten of DESIGN.md Section 5.1 in that order. An unqualified deny also blocks the nested `template:<name>` form.
- **Layer 2 — `claudeMdExcludes`** keeps `template/**/CLAUDE.md` and everything under `template/.claude/` out of this session's memory.
- **Never invoke a template skill.** If one appears invocable (listed as `template:<name>`, or offered for files under `template/`), the deny list has a gap: stop and report it rather than using it.
- **Adding a skill to the template means adding its deny line.** That is a change to this repository's permission settings, so it is the maintainer's to make or approve; propose the exact line.
- `.github/scripts/dev-isolation.sh` proves both layers on every push.

## 4. Token discipline

Every file under `template/` is rendered (`_templates_suffix: ""`) with the house delimiters, chosen because none occurs in any source text:

| Form | Meaning |
|---|---|
| `<% NAME %>` | A variable: a question key from `copier.yml` |
| `<: if X :>…<: endif :>` | A block |
| `<~ … ~>` | A comment (never rendered) |

- **Registered tokens** are the question keys in `copier.yml` (every top-level `UPPER_SNAKE` key) plus `_copier_operation`, `_copier_answers` and `_copier_conf`. Nothing else may appear inside a delimiter. `check-template-tokens.sh` derives the set from `copier.yml`, so only questions may be top-level `UPPER_SNAKE` keys there.
- **Identity and locale tokens may appear anywhere:** `BRAND_NAME`, `BRAND_SLUG`, `OWNER_NAME`, `OWNER_FIRST_NAME`, `DATE`, `TIMEZONE`.
- **Variant tokens and `<: if :>` blocks appear only in the spine set** (DESIGN.md Section 2): the root spine (`.claude/rules/syntek-media/*.md` and `.copier-answers.syntek-media.yml`); the ten copy-only shared files; every seed and seed-once example; and **index files**. Variant tokens are `BRAND_KIND`, `PLATFORMS`, `MEDIA_KINDS`, `BRAND_DESCRIPTION`, `AUDIENCE_TEST`, `SEED_EXAMPLES`, `MODEL_MECHANICAL` and every later answer.
- **An index file** is a `CONTEXT.md` or `CLAUDE.md` whose folder is an ancestor of a gated path. It wraps each row, tree line or cross-reference that names a gated path in `<: if GATE :>…<: endif :>`, where `GATE` is the exact string of DESIGN.md Section 3.5 — the same string `copier.yml` negates for that path — or names the path only in prose. It never gates a row on `SEED_EXAMPLES` and never names an example path (D43).
- **Every other shipped file is shared and byte-identical** in every render that ships it. Put a brand-kind difference in a mode file and a platform or media-kind difference in a gated file, never in a conditional. A shared or mode file never backticks a path or skill gated by `PLATFORMS` or `MEDIA_KINDS`: it names it in prose ("the audiobook folder, where the project makes audiobooks"), or the line carries `<!-- doc-references: variant-only -->`. `byte-identity.sh` enforces this.
- **A multiselect is a list.** Gate with `'tiktok' in PLATFORMS`, never `PLATFORMS == 'tiktok'`; render it with `<% PLATFORMS | join(', ') %>`, never a loop variable inside `<% %>` (the token audit rejects lower-case names), or one gated line per item.
- **Never put a token inside `_…_` emphasis.** Prettier rewrites the underscores and the token stops rendering.
- **Never write a delimiter you do not mean.** HTML, CSS, TOML, SRT and ffmpeg filter strings may hold `{{` and `{%` freely, because the house delimiters differ, but never `<%`, `<:` or `<~`. A guide that must show one wraps it in `<: raw :>…<: endraw :>`; otherwise rephrase.

## 5. Personal data never enters `template/`

- **Never under `template/` or in `examples/`:** a real brand's or person's name (use `<%BRAND_NAME%>`, `<%OWNER_NAME%>` and `<%OWNER_FIRST_NAME%>`), channel handles and URLs, platform account IDs, ElevenLabs voice IDs and API keys, Claude Design links, follower or view counts, prices, credentials, absolute paths, syntek-base's name, or project state written into a skill.
- **Examples use invented brands and people only:** Harbour Lane Studio, Morgan Example and Robin Example, syntek-author's own inventions, so a combined render tells one story. Never fabricate a statistic, quotation, testimonial, endorsement, platform rule or limit: use a clearly marked placeholder and a `VERIFY` flag.
- **`template/` ships no binary** — no audio, video, image or font. A layout is HTML and CSS; a fixture is generated at run time.
- **Seeds ship empty of entries** — headings, writing rules and the seeded-stub banner in Markdown, header comments only in TOML, `AUTHOR TO CONFIRM` slots in the brand seeds. A seed cut from a real project is a one-way door: once it exists in a generated project no update can correct it.
- `scrub.sh` fails the build on a hit. A hit is fixed at the source, never allow-listed. It also flags any run of seven or more digits (write a bitrate as `8M`, never in full) and a currency sign before a figure.

## 6. House formats (the owner is `DESIGN.md`; this is the checklist)

- **Every directory under `template/` has a `CONTEXT.md` and `CLAUDE.md` pair**, except syntek-author's exceptions (`build/`, `.git/`, `audio/`, `__pycache__/`, `node_modules/`, `.claude/rules/`, the inside of each skill folder, each `drafts/` and each `.base/`), the template root (`CONTEXT.md` only), and media's own (D42): each `generated/`, `renders/` and `raw/` folder carries only its `README.md`, and a `handoffs/` folder created in a standalone project carries no pair at all. Every piece folder carries its own pair.
- **Metadata header** on guides, rules, STEPS, CHECKLIST and seeds: `**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>`, then `**Language**: British English (en_GB)`.
- **Workflow folders** hold `CONTEXT.md`, `CLAUDE.md`, `STEPS.md` and `CHECKLIST.md`, with routing frontmatter (`workflow`, `phase`, `skills`, `model`; no `agent` key). STEPS steps open `> **Skill:** … · **Guide:** …` and end `_Substantive._` or `_Mechanical._`; CHECKLIST items end ` · _opus_` or ` · _sonnet_`. Every CHECKLIST's `> **See**` line names its guide and the ladder gate it serves, as `M2 (briefed → scripted)`, or the fixed gate-less form of DESIGN.md D17.
- **Guides** follow DESIGN.md Section 4.3 (54–82 lines; `skills:` lists only skills that ship whenever the guide does). **Skills** follow DESIGN.md Section 5, moded skills carry the mode paragraph verbatim, and mode files use the four H2s of D7.
- **Cite a workflow by its full folder name** (`production/workflows/02-make-a-voiceover/`), never by its number alone (D32).
- **Companions are named, never shipped** (D10): unbackticked, never in `skills:`, always 'the spelling skill (syntek-author), where present'.
- **Every instructional `.md` stays within 300 lines** (D31); `src/` artefacts and `README.md` are exempt.
- **Locale:** en_GB, single quotation marks, DD/MM/YYYY in prose, `DD-MM-YYYY` in filenames, timecodes `HH:MM:SS.mmm`, "Section 3.2" and never the section sign.

## 7. How to change the template

Each recipe ends the same way: run the audits (Section 8) and add a `CHANGELOG.md` entry under `[Unreleased]`.

- **Check every new name first.** A new top-level folder, `.claude/` path, skill folder or rules file is checked against `.github/scripts/syntek-author-names.txt` before it is written. A copy over a syntek-author project stops on a collision, but an update does not: it overwrites syntek-author's file and leaves conflict markers in it (DESIGN.md Section 10).

**7.1 Add a skill.**

1. Add its row to DESIGN.md Section 5 (approved first, Section 2 above). A name in `syntek-author-names.txt` is refused (D27).
2. Write `template/.claude/skills/<name>/SKILL.md` to the conformance rules of DESIGN.md Section 5. A moded skill gets one mode file per brand kind (7.2).
3. A gated skill gets one `_exclude` line in its block of `copier.yml`: `"<: if not (GATE) :>/.claude/skills/<name><: endif :>"`.
4. Add its row to `template/.claude/rules/syntek-media/02-skills.md` Section 3, wrapped in its gate, and to the skill catalogue in `.github/scripts/_common.sh`.
5. Propose its `Skill(<name>)` deny line for the root `.claude/settings.json` (Section 3).

**7.2 Add or remove a mode file.** Write `BUSINESS.md`, `FICTION.md` or `NONFICTION.md` beside the `SKILL.md` with the four H2s, then regenerate the block of `copier.yml` between the `BEGIN`/`END generated mode excludes` markers:

```bash
bash .github/scripts/gen-mode-excludes.sh
bash .github/scripts/gen-mode-excludes.sh --check
```

Never type a line in that block; `--check` fails CI when the block and the files disagree.

**7.3 Add a gated path.**

1. Add the path and its gate to DESIGN.md Section 3.5 (and its layer table in Section 4.3).
2. Add one line to the right block of `copier.yml`: `"<: if not (GATE) :>/path<: endif :>"`, `GATE` copied verbatim, its item single-quoted and with no parentheses inside it. A membership test on `PLATFORMS` or `MEDIA_KINDS` needs no `BRAND_KIND` test (D15); a gate on a list question hidden by `when:` does, because a hidden question keeps its default in the render context.
3. Wrap every index row, tree line and cross-reference that names the path in `<: if GATE :>…<: endif :>`, or name it in prose.
4. If the path is also a seed or an example, it needs its gate line **and** its seed or seed-once line.

**7.4 Add a workflow.** Numbers are frozen and append-only, unique within a layer across every brand kind, platform and media kind (D32). Take the next unused number, write all four files, add the row to the layer's `workflows/CLAUDE.md` table and `workflows/CONTEXT.md` (gated if the workflow is), and gate the folder in `copier.yml` if it is gated. Cite it everywhere by its full folder name.

**7.5 Add a seed.** Add it to DESIGN.md Section 3.1 and to `_skip_if_exists` in `copier.yml`, **anchored with a leading slash** (an unanchored name matches at every depth and would freeze template-owned files of the same name). Ship it empty of entries. A gated seed also needs its `_exclude` line. **Never stop shipping a seed** without a migration that preserves it first: a seed the template drops is deleted from every project on its next update, filled in or not. **A shared root file, once shipped, is never removed from `template/` or renamed, and neither of its two lines in `copier.yml` is ever deleted** (D11, DESIGN.md Section 10).

**7.6 Add a question.** Add it to DESIGN.md Section 2 and to `copier.yml` in its group: an `UPPER_SNAKE` key, `>-` help written to the person answering, a validator as `<: if bad :>message<: endif :>`, and `when:` with its `BRAND_KIND` test if it is hidden for some kinds. A default must never open a gate in a render that hides the question, and `_external_data` is read in a validator only (D14). Then add a row to the questions table in `README.md` and the key to all three `examples/*.answers.yml`.

**7.7 Rename or move a folder.** Do not, if it can hold author work: names and numbers are frozen. If a release must, it ships a version-keyed migration in the same commit (`copier.yml`, under `_migrations`, has the house shape). The same applies when a release changes what a seed must contain, or stops shipping one.

**7.8 Add a platform or a media kind.**

1. Its value and label in `choices` (DESIGN.md Section 2 and `copier.yml`), and in a brand kind's default only where every project of that kind should have it.
2. Its gated paths (7.3): for a platform, its profile seed `brand/src/platforms/<platform>.md` (also a seed line, 7.5) and its guide `publishing/docs/reference/<platform>.md`; for a media kind, its guide in `scripts/docs/reference/` and anything that serves only it.
3. Its tables in `toolkit/data/platforms.toml`, each with `checked`, `source` and `verify`: limits live there, never as numbers in a guide (D26).
4. Its line in `_message_before_update`, naming every file removing it deletes, workflows by full folder name (D16).
5. Its row in `README.md`'s platforms or media-kinds table, and its rows in `_common.sh`'s path catalogue.
6. Turn it on in at least one `examples/*.answers.yml`, so the three still cover every value, and check that it appears in the `all` renders and not in the `minimal` ones.

## 8. Before you commit

- **Run the audits.** All of them, or at least those your change touches:

  ```bash
  bash .github/scripts/run-all.sh --author ../syntek-author
  ```

  `generate-all.sh` renders every brand kind and profile from a copy of the working tree; `shipped-brands.sh <tree>` checks one rendered tree. A change to `copier.yml`, a gate or a seed is not done until a render proves it. The renders over syntek-author and `coexist-test.sh` need a syntek-author checkout (`--author DIR`); without one they report SKIP, which is never a pass.
- **Never commit rendered output, audio, video or images.** Renders go to a temporary directory and stay there; fixtures are generated at run time (`ffmpeg -f lavfi …`).
- **Commit only when the maintainer asks**, on a branch, with a `CHANGELOG.md` entry.

## 9. Releasing

- `VERSION` and `CHANGELOG.md` move together; the release is tagged `vX.Y.Z`. `copier copy` takes the latest tag, so unreleased work is rendered with `--vcs-ref=HEAD`.
- **Never tag a release while `coexist-test.sh` reports SKIP** (D27). Run it against a syntek-author checkout and see it pass.
- **Refresh the frozen names when syntek-author has moved:** `bash .github/scripts/coexist-test.sh --refresh-names --author DIR` rewrites `syntek-author-names.txt`. Re-check every new name against media's paths before anything else.
- **Every release entry in `CHANGELOG.md` names the syntek-author baseline** its coexist test passed against: the commit, and the date it was read.
- A migration is keyed to the release its change shipped in, never the release somebody noticed.
- Updates of generated projects need `-a .copier-answers.syntek-media.yml` (D3); every instruction that shows an update command says so.

---
name: media-research
context: fork
agent: general-purpose
background: true
description: >-
  Answer one question about making or publishing media from its primary source: a platform's own
  help, policy or developer pages, a music, stock or footage library's licence, a consent, release
  or disclosure rule, a format, codec, loudness or caption convention, a tool's documentation, or
  the source of a pronunciation. Looks in both places first, reads every claim at its origin,
  records conflicts rather than averaging them, and records each source and the date it was read
  in the file that uses it, keeping no notes folder. A background agent. Use when the author says
  'check what the platform allows now', 'is this track cleared for ads?', 'what does the platform
  say about AI labels?' or 'how is this name really said?'. Not for a piece's subject or a claim's
  verdict (the research and fact-check skills (syntek-author), where present). Not for writing the
  post (`prepare-post`).
---

# Skill: Media Research (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

This skill answers a question about making or publishing media that the project cannot yet answer,
by reading **primary sources**: the platform's own page, the library's own licence, the rule's own
text, the tool's own documentation. Every claim it hands back carries its source and the date it
was read, and lands in the file that uses it, never in a notes folder of media's own. A secondary
report, a forum or a search result points to a change; it never confirms one.

It runs as a **forked background agent**, so the session that called it carries on while it reads.
A forked agent cannot talk to the author: anything only <%OWNER_FIRST_NAME%> can answer goes back
to the caller as a question, never as a guess.

It runs beside the research skill (syntek-author), where present, and never stands aside for it:
that skill reads a piece's subject and the facts behind written work, and this one reads media's
own questions. Route by the work at hand, and look in both places.

## Governing procedures (route here — do not restate at length)

- `publishing/workflows/07-refresh-the-platform-specs/` — step 3, re-reading each stale platform
  table at its source; this skill is that reading. Run its `STEPS.md` with `CHECKLIST.md` open.
- If the layer's `workflows/local/` holds a folder with the same `NN-name` as the procedure above,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `publishing/docs/reference/platform-specs.md` — how the platform data is read, what `verify`,
  `chosen` and an absent key mean, overrides and staleness.
- `.claude/rules/syntek-media/03-production-ethics.md` Sections 5 to 8 — disclosure, rights and
  consent, never fabricate a platform rule or limit, and the two flags.
- `.claude/rules/syntek-media/02-skills.md` Section 4 — the research role, and the evidence and
  research-notes row: a source and the date it was read go in the file that relies on it.
- `.claude/rules/syntek-media/06-global-rules.md` Section 13 — the web and code tools: the
  plainest fetch first, and every page fetched recorded with where and when.

The mode file adds this project's primary sources and the questions its brand kind asks most.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Take one answerable question.** Reduce the ask to one sentence a source can settle, and name
   the piece or the table it serves. A question about a piece's subject (what happened, what a
   study found, what a book says) or a claim's verdict is not this skill's: hand it back for the
   research or fact-check skill (syntek-author), where present, after checking its
   `.claude/skills/<skill>/SKILL.md` exists. Where neither is present, a subject question is
   answered here for that one piece only, in its brief, and every claim it leaves open stays
   `VERIFY`. A question that will not reduce to one sentence goes back with the reframing it
   needs. *Complete when:* the question is one sentence, it is media's own or a standalone subject
   question for one piece, and the piece or table it serves is named.

2. **Look in both places first.** Read media's records: `python3 toolkit/media.py presets KEY`
   (which prints a table of `toolkit/data/platforms.toml` as the toolkit will use it, with its
   `verify` keys and every override in `brand/src/platforms/overrides.toml` applied), the briefs' `## Draws on` and `## Notes`, `production/src/rights-register.md` and
   `brand/src/voice/voice.md`. Then, where syntek-author is present, its research notes and
   evidence (the paths rules 02 Section 4 gives the role), read and never edited. An answer
   checked within the stale-after window of `publishing/workflows/07-refresh-the-platform-specs/`
   (`presets --stale-after 183`) is reported with its date, not redone, unless the caller asks
   for a fresh read. *Complete when:* every record that could hold the answer has been read, and
   the answer is either held and fresh, or still needed.

3. **Name what a complete answer needs.** Before searching: the exact value or rule asked for,
   the kind of source that owns it (the mode file lists them), and the platform, format, region,
   account type and date it must hold for. *Complete when:* the basis is written down at the head
   of the hand-back.

4. **Read every claim at its primary source.** Fetch with the plainest tool that does the job
   (rules 06 Section 13), and follow the chain back to the page that owns the fact: the platform's
   own help, policy, developer or ads pages; the library's own licence text; the rule's own text;
   the tool's own documentation. **Searching finds; reading cites:** a search result, a tool's
   summary of a page or another model's answer is a lead, never a citation, and a figure, a limit
   or a quotation is taken only from the source's own text. A page behind a sign-in or a paywall
   is reported as unavailable, never worked round. *Complete when:* every claim traces to a
   primary source actually read, with its address and the date read.

5. **Keep going past the convenient source; record every conflict.** When a source agrees with
   what the project hoped, keep looking. Agreement among secondary sources is not corroboration.
   Where two sources disagree (the help page and the developer page, two regions, a policy and its
   summary), name both and say which governs and why; never average them into a value neither
   states. A value no primary source states stays absent or in `verify`, never filled from memory
   or from another platform. *Complete when:* every conflict is stated with the source that
   governs, and every unconfirmed value is named.

6. **Record the source where it is used.** Keep no notes folder. While a brief has passed no gate,
   write the source and the date read into its `## Draws on`; past a gate, nothing is written until the
   caller has raised it with the author, because a claim added reopens the gate
   (`scripts/docs/reference/the-piece-ladder.md`), and then only into `## Notes`. Everything else
   is **proposed**, never written here: an `[[override]]` row (`key`, `value`, `why`, `source`,
   `checked`) for the refresh procedure's own step to record on the author's word; a licence,
   release or permission term for the rights register, through
   `production/workflows/07-clear-the-rights/`; a pronunciation and its source for `voice.md`,
   through `brand/workflows/05-write-the-spoken-voice/`. *Complete when:* each source sits in the
   file that uses it or in a proposal for the procedure that writes that file, and nothing was
   written past a gate without the author's word.

7. **Hand back.** Report to the caller: the answer, each claim with its source and the date read,
   the conflicts and which source governs, what could not be found or reached, every value still
   in `verify`, the proposals of step 6, any deliverable already rendered or packaged that the
   answer affects, the questions only the author can answer and **what tells against the
   project's convenience**. *Complete when:* the caller has the report, and every proposal names
   the procedure that would record it.

## Anti-patterns

- **Citing the scout.** A press report, a forum, a blog or a search summary is not the platform.
- **Answering from memory** because a limit feels familiar; platforms change them without notice.
- **Averaging two sources** into a value neither supports, or borrowing one platform's limit for
  another.
- **Editing `toolkit/data/platforms.toml`.** It is template-owned; a correction is an override,
  proposed.
- **Writing into a register, `voice.md` or a profile.** Each has its procedure; this skill
  proposes.
- **Adding a claim to a brief past its gate** without the author's word.
- **Keeping a notes folder**, or a source with no date.
- **Giving a claim its verdict,** or researching a piece's subject, which is the research
  skill's (syntek-author), where present.
- **Asking the author from inside the fork.** Return the question to the caller.

## Cross-references

- `prepare-post`, `cut-for-platform`, `thumbnail-brief` — the skills that read the platform data
  this skill keeps fresh.
- `media-teach` — reads a lesson's primary source through this skill.
- `media-tone` — reads the profile's tone this skill never sets.
- `brand/src/platforms/overrides.toml` — where a confirmed correction lives, on the author's word.
- `production/src/rights-register.md` — where a licence or consent term is recorded, through its
  procedure.
- The research and fact-check skills (syntek-author), where present — a piece's subject, and a
  claim's verdict.

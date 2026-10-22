# Pull request

## Summary

<!-- One or two sentences: what is different after this merges, and why. Link the issue: Closes #123 -->

## Decision

<!--
The DESIGN.md decision (D-number) or section this implements. If it changes DESIGN.md, link the
issue or comment where the maintainer approved the change, and give the date. DESIGN.md is the
contract: where any other file disagrees with it, that file is wrong.
-->

---

## Checklist

CI (`.github/workflows/audit-template.yml`) runs every audit on every push to every branch; read
its run. Tick the audit box only for a local run you saw finish.

**Contract**

- [ ] `DESIGN.md` changed only with the maintainer's approval, given on DD/MM/YYYY (linked above), or not at all
- [ ] A `CHANGELOG.md` entry under `[Unreleased]`, citing the decision or section
- [ ] If `DESIGN.md` changed: `.github/scripts/_common.sh` changed with it, in the same commit

**Template**

- [ ] Token discipline kept: registered tokens only, variant tokens and blocks only in the spine set and index files, no delimiter I did not mean (`.claude/CLAUDE.md` Section 4)
- [ ] Every new gated path has its `_exclude` line, its gate copied verbatim from DESIGN.md Section 3.5, and every index row, tree line or cross-reference that names it is gated
- [ ] Every new top-level folder, `.claude/` path, skill folder or rules file checked against `.github/scripts/syntek-author-names.txt` (D27)
- [ ] No shared root path removed from `template/` or renamed, and neither of its two lines in `copier.yml` deleted (D11)
- [ ] Seeds ship empty of entries
- [ ] If a folder that can hold the owner's work moves, or a seed's required content changes: a version-keyed migration in this pull request (`.claude/CLAUDE.md` Section 7.7)
- [ ] If a template skill was added: its deny line, `skillOverrides` entry and Codex recipe line proposed for the maintainer (`.claude/CLAUDE.md` Section 3)

**Audits**

- [ ] `bash .github/scripts/run-all.sh --author ../syntek-author` exited 0 locally with no SKIP, against syntek-author commit: <!-- git -C ../syntek-author rev-parse --short HEAD -->

**Safety**

- [ ] No rendered output, audio, video, image or font committed (renders, logs and scratch projects stay in a temporary directory)
- [ ] No ElevenLabs or other paid call made, by me or by a test
- [ ] No personal data under `template/` or in `examples/`: brands and people invented, no key, voice ID or Claude Design link
- [ ] No template skill invoked while working on this
- [ ] British English (en_GB), single quotation marks, DD/MM/YYYY in prose

**Licence**

- [ ] I agree that my contribution is licensed under the MIT Licence, with the permission for generated projects (inbound = outbound), as `CONTRIBUTING.md` ('Licence') says

---

## Anything reviewers should know

<!-- Trade-offs you weighed, audits you could not run and why, what you deliberately left out. -->

---
workflow: 07-refresh-the-platform-specs
phase: review
skills: []
model: opus
---

# CHECKLIST.md — refresh the platform specs

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `publishing/docs/reference/platform-specs.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] Read `platform-specs.md` and `ai-disclosure.md`. · _opus_
- [ ] Today's date known, for `--today` and for every `checked`. · _sonnet_

## Execution Checklist

**Finding what is stale**

- [ ] `media.py presets --stale-after 183 --today DD/MM/YYYY` run; every stale table listed. · _sonnet_
- [ ] Every `verify` key about to be relied on added to the list. · _sonnet_
- [ ] The list narrowed to the platforms and deliverables this project uses. · _sonnet_

**Re-reading**

- [ ] **Each table's `source` and `extra_sources` re-read on the platform's own pages,** and dated. · _opus_
- [ ] Nothing confirmed from a press report or a third party; what only they state stays `VERIFY`. · _opus_
- [ ] No value filled from memory or from another platform. · _opus_

**Recording**

- [ ] Each confirmed difference drafted as an `[[override]]` row with `key`, `value`, `why`, `source` and `checked`. · _sonnet_
- [ ] **The author confirmed every row** before it was written. · _opus_
- [ ] Rows appended to `brand/src/platforms/overrides.toml`; `toolkit/data/platforms.toml` untouched. · _sonnet_
- [ ] `media.py presets KEY` prints every new override, applied. · _sonnet_
- [ ] Overrides the data file now agrees with proposed for retirement, and removed only on the author's word. · _opus_
- [ ] Each disclosure rule the project relies on re-read; a changed one reported, and recorded in a same-named project guide on the author's word. · _opus_
- [ ] Handed back: tables re-read, overrides added or retired, values still unconfirmed, deliverables affected, the next refresh date. · _opus_

## Done When

- [ ] **No table the project relies on is stale, or each one still stale is named with the reason.** · _opus_
- [ ] Every confirmed difference is an override the toolkit applies and prints. · _sonnet_
- [ ] The refresh date is recorded, and the next one named. · _sonnet_

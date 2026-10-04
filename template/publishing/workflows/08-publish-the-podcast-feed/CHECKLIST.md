---
workflow: 08-publish-the-podcast-feed
phase: publish
skills: [prepare-post, cut-for-platform]
model: opus
---

# CHECKLIST.md — publish the podcast feed

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `publishing/docs/reference/podcast-feed.md` and the `prepare-post` skill. This
> procedure serves a feed episode's part of M7 (captioned → scheduled) of
> `scripts/docs/reference/the-piece-ladder.md`, beside `publishing/workflows/05-prepare-a-post/`;
> the gate is cited by number and the move it guards, and this list never restates it.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] Read `podcast-feed.md` and the register's skeleton in `publishing/src/podcast/CLAUDE.md`. · _opus_
- [ ] **The brief lists `podcast.feed_audio` and dates M6;** the M5 render, the master-timed `.vtt` and the published transcript exist. · _sonnet_

## Execution Checklist

**The show and the row**

- [ ] The show opened once with `feed new`, its feed URL confirmed with the author first; never typed or edited by hand. · _opus_
- [ ] The show's details written with the author, the disclosure sentence in its description where needed, `approved` dated. · _opus_
- [ ] The episode added with `feed add`, once; no row deleted. · _sonnet_
- [ ] The row's words, `pub_date`, art, page, transcript and chapters written, every length counted against its key, and approved by the author. · _opus_

**The files**

- [ ] `feed tag` exits 0; `render`, `bytes` and `seconds` written into the row. · _sonnet_
- [ ] `feed chapters` written into the renders folder. · _sonnet_
- [ ] **`feed check` exits 0;** every finding fixed in the register, never in a feed. · _sonnet_
- [ ] The row set `ready`; the schedule row left to the post procedure, which records M7. · _sonnet_
- [ ] The upload copy written with `feed write --as-of` the episode's `pub_date`. · _sonnet_

**The hand-back**

- [ ] Upload list given in order: audio, art, `.vtt`, chapters; then the feed at `pub_date`, not before. · _opus_
- [ ] The `curl` tests given where the show or its host is new; the hand steps given: the Spotify transcript upload (`VERIFY`), the YouTube playlist. · _opus_
- [ ] Each episode page on another site sent to the post procedure as a placement. · _opus_
- [ ] The author asked to report the feed live, for the publication procedure. · _sonnet_

## Done When

- [ ] **The row is `ready`, its file tagged, its feed checked, and nothing was uploaded.** · _opus_
- [ ] Every GUID was written by the toolkit, once. · _sonnet_
- [ ] The author knows what to upload, in what order, and when the feed goes up. · _opus_

---
name: prepare-post
description: >-
  Package one piece for posting, one section per deliverable or placement: title, description and
  hashtags inside each platform's limits, the AI-disclosure plan, captions, thumbnail, render and
  rights, then the schedule row, citing syntek-author's calendar entry, where present (M7); for the
  brand's own sites and newsletters, alt text, links and agreements; for a self-hosted podcast, the
  episode's register words and feed check. Never posts: the publish log records only what the author
  reports. Use when the author says 'prepare the post', 'write the description and hashtags', 'get
  this ready to publish', 'what disclosure does this need?', 'publish the podcast feed' or 'it's up,
  here's the link'. Not text-only posts, bios or a blog post's or newsletter's own words (the
  social-media-documents skill or the writing router of syntek-author, where present). Not the
  captions (`captions`). Not the thumbnail (`thumbnail-brief`).
---

# Skill: Prepare Post (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

The last step before a piece meets its audience, and the first record of how it went out. This
skill gathers everything one upload needs into a post package, one section per deliverable, so
<%OWNER_FIRST_NAME%> can post without opening another file: the words, the disclosure, the
captions, the thumbnail, the render and the time. **It never posts**: no platform is called and
no upload is made from here. The author posts, and the publish log records what the author
reports, exactly as reported.

Disclosure is the one judgement here that is not about taste. Each platform's own rule decides
its AI label or toggle; the house rule decides the words: wherever a piece uses a synthetic voice,
AI visuals or generated music, every description says so, whatever the toggle.

## Governing procedures (route here — do not restate at length)

- `publishing/workflows/05-prepare-a-post/` — this skill is that procedure in skill form; it moves
  the piece from captioned to scheduled. Run its `STEPS.md` with `CHECKLIST.md` open.
- `publishing/workflows/06-record-a-publication/` — logging what the author posted, until the
  piece is published.
- If the layer's `workflows/local/` holds a folder with the same `NN-name` as a procedure above,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `publishing/docs/reference/ai-disclosure.md` — each platform's rule for its AI label or toggle,
  with its source and checked date, and the house's description line.
- `publishing/docs/reference/posting-and-the-log.md` — the package, the schedule, the publish log,
  what published means, and the content calendar where syntek-author's is present.
- `publishing/docs/reference/platform-specs.md` — how `toolkit/data/platforms.toml` is read:
  `verify`, absent keys and the brand's overrides.
- `brand/docs/reference/platform-profiles.md` — what a platform profile holds, and what the social
  media plan holds instead where syntek-author's is present.
- `production/docs/reference/rights-and-consent.md` — what `cleared` means for each kind of row.
- `scripts/docs/reference/the-piece-ladder.md` — M7 (captioned → scheduled) and the definition of
  published; never restated here.
- `publishing/src/posts/CLAUDE.md` — the post package's format and name.
- `.claude/rules/syntek-media/03-production-ethics.md` Sections 5, 6 and 7 — AI disclosure, rights
  and consent, and never fabricate.

The mode file adds where this brand kind's social plan lives, the claims its posts may make, and
the people they may show.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Fix the piece and its deliverables.** Confirm the piece and read its `brief.md`: `status`,
   `verified`, `deliverables`, `synthetic_voice`, `ai_visuals`, `music` and `rights`. Read its
   cut-down plan, `publishing/src/cut-downs/<piece>.md`, where it has one. The deliverables to
   package are the brief's and every agreed cut's: media deliverables only, because a text-only
   post belongs to the social-media-documents skill (syntek-author), where present. Where M6 is
   neither dated nor recorded as n/a with its reason, a package may be drafted but nothing is
   scheduled: say which gate is open. Where a package exists, read it, and never overwrite it
   without the author's word.
   *Complete when:* every deliverable to package is listed, with the piece's status and any open
   gate named.

2. **Read the plan the posts belong to.** Check whether the social-media-documents skill
   (syntek-author) is present, by its `.claude/skills/<skill>/SKILL.md`. Where it is, each of
   syntek-author's social-media documents (the plan, the content calendar, an operating
   procedure, in its library layer's social-media folder) owns what it sets for a platform,
   platform by platform: find the calendar entry each deliverable fills and read it, and never
   edit those documents; an entry missing there is the author's to add through that skill. The
   platform profile, `brand/src/platforms/<platform>.md`, holds what none sets.
   *Complete when:* every deliverable names its calendar entry or its profile as the source of its
   tone, call to action and hashtags, and every missing entry is listed.

3. **Read the limits and the rules.** Print the tables with `python3 toolkit/media.py presets`
   (each platform's limits on titles, descriptions, captions or post text and hashtags, and each
   deliverable's own), brand overrides applied and every `verify` key named. Read each platform's
   guide in `publishing/docs/reference/`, and its row in
   `publishing/docs/reference/ai-disclosure.md` with its checked date. Never take a limit or a
   platform rule from memory.
   *Complete when:* every field of every deliverable has the key that limits it, or is recorded as
   having none, and every `verify` key is named.

4. **Draft the words.** For each deliverable, propose the **Title**, the **Description** (a fenced
   block, one sentence per line) and the **Hashtags**, in the brand's written voice and from the
   sources step 2 named: the hook from the script or transcript, the call to action from the
   brief. Every factual claim is one the piece makes and its sources support; anything unchecked
   carries `<!-- VERIFY: … -->`. Run the spelling and grammar skills (syntek-author), where
   present, as one supportive report, and the fact-check skill (syntek-author), where present, on
   every claim; check each `.claude/skills/<skill>/SKILL.md` first, and name any that is missing.
   *Complete when:* every deliverable has its three fields drafted, and every report is with the
   author.

5. **Package each placement on the brand's own channels.** A piece placed on a site of the
   website or blog profile, or in an issue of a list in the newsletter profile, gets one section
   per placement: the one file that page or issue plays or shows first (the video, the embed of
   the YouTube upload, the GIF, or a still where there is no GIF), headed
   `## <platform>.<format>[ — cNN] — <platform>:<slug>`, with the bullets its channel's guide
   gives, where the project has that platform. Media writes only the words outside the written
   body (an embed's or figure's title, alt text, Links to, the structured-data values, the
   agreement); the post's, page's or issue's own words, standfirst, link text and date are the
   written side's. Read the written piece, never edit it, never record its status; take the
   placement's date from it. A site or list the brand does not own needs its profile row's dated
   agreement. An embed or player snippet goes to the author in chat, on request, never to a file.
   *Complete when:* every placement has its section, its written piece read and its date cited,
   and its agreement named or listed as blocking.

6. **Package a feed episode.** Where the brief lists `podcast.feed_audio`, the episode's title,
   description and chapters are written with the author in its show register (the podcast folder
   of `publishing/src/`, where the project has the podcast platform), never in the package: its
   `## podcast.feed_audio` section cites them, and adds Episode page, Feed and On YouTube. The
   register's part of M7 (`feed add`, the words approved, `feed tag`, `feed chapters`,
   `feed check`, the upload copy) runs through the podcast-feed workflow and guide. An episode
   page on another site is a placement (step 5); a `youtube.long` carrying it adds Playlist.
   *Complete when:* the section cites its register row, and `feed check` is clean.

7. **Plan the disclosure.** Where the brief records a synthetic voice (the owner's own clone
   included), AI visuals or generated music, plan three things for every deliverable: the
   platform's AI label or toggle, set exactly when that platform's current rule requires it, with
   the rule and its checked date; a disclosure line in the description, on every platform, always;
   and the spoken or on-screen line, where the piece carries one. A podcast discloses in the audio
   itself and in the episode and show metadata too: a master without the spoken line goes back to
   production before it is scheduled. Where a platform's rule is unclear or its checked date is
   old, flag `VERIFY` and ask. On the brand's own channels there is no label: the house line goes
   beside the media. A piece whose brief records none of these says so in its **Disclosure**.
   *Complete when:* every deliverable's **Disclosure** names the toggle decision and its rule, the
   description line and the spoken or on-screen line, or records that none is needed.

8. **Attach the render, captions and thumbnail.** For each deliverable, name its render in
   `publishing/src/renders/` and confirm it with `python3 toolkit/media.py probe`; name its
   captions file in `publishing/src/captions/` and whether it is burned or a sidecar (a deliverable
   whose `caption_formats` is empty takes burned captions; a placement names its `.vtt` and its
   published transcript); and, where the platform takes one, its approved thumbnail or images.
   Anything missing goes back to its owner: `cut-for-platform`, `captions` or `thumbnail-brief`.
   *Complete when:* every deliverable names an existing render, its captions and any thumbnail its
   platform takes, or the missing item and its owner are listed.

9. **Check every limit and every right.** Count each field's characters exactly, never by eye, and
   record each count against its key in **Limits**. A count over a hard limit is cut, never posted.
   Above `platform.instagram.hashtags_max`, a `verify` key, warn by that key with the value
   `presets` printed and let the author decide; warn the same way at any other hashtag key. Check
   that every rights row the piece uses (the brief's `rights`, the shot list's Rights column) is
   `cleared` in `production/src/rights-register.md` and unexpired on the scheduled date. Run
   `python3 toolkit/media.py flags --piece <piece> --strict`, which gathers the piece's files
   across the scripts, production and publishing layers by their house names.
   *Complete when:* every count is recorded against its key, every row is `cleared` or listed as
   blocking, and the flags run is clean or its flags are listed.

10. **Write the package and the schedule rows.** Present the package and wait. Then write what
    the author agreed to `publishing/src/posts/<piece>.md` in the format its folder's `CLAUDE.md`
    gives, one H2 per deliverable or placement. Add one row per deliverable and per placement
    (`<platform>:<slug>`) to `publishing/src/schedule.md`, at the date and time the author chose,
    or the written piece's own (<%TIMEZONE%>), status `planned`, its Notes citing the calendar
    entry where syntek-author's is present.
    *Complete when:* the package holds exactly what the author agreed, and every deliverable and
    placement has its schedule row.

11. **Record M7, and hand over.** When the author approves the package and every check of step 9
    passes, date `approved` in the package, set each schedule row to `ready`, and in the brief date
    M7 in `verified`, set `status: scheduled` and set `last_updated`, as
    `scripts/docs/reference/the-piece-ladder.md` gives it. Report what is ready, when each post is
    due, and what the author sets by hand at upload, platform by platform. When the author is ready
    to post a deliverable, give its title and its description in chat as paste-ready text: the
    fenced lines joined into paragraphs, one sentence per line being only how the file keeps them;
    never write that joined text to a file. The author posts.
    *Complete when:* the author has the hand-over, and the brief's status moved only on the author's
    approval.

12. **Log each post the author reports.** Only when the author says a deliverable is up, add its
    row to `publishing/src/publish-log.md` with the URL the author gives and the disclosure and
    captions as the author reports them set, and mark its schedule row `posted`; a post that will
    not go out is `dropped`, on the author's word. Where the report differs from the package (a
    toggle left off, another time), record it as reported and point out the difference. When every
    schedule row for the piece is `posted` or `dropped`, and each posted row has its log row, set
    the brief's `status: published`, as `publishing/workflows/06-record-a-publication/` gives it;
    for a feed episode it also sets the register row `published` and writes the tracked feed.
    *Complete when:* every reported upload has exactly one log row, and the brief reads `published`
    only when every row is settled.

## Anti-patterns

- **Posting, or saying it was posted.** No platform is called from here; a package is not a post,
  and the log records only what the author reports.
- **A toggle by habit.** A label the platform's rule does not ask for can mislead viewers about
  what is synthetic; a label it does ask for is never skipped. The rule and its date decide.
- **A synthetic voice with no description line.** Whatever the toggle, the description says so.
- **A limit from memory, or a count by eye.** Every limit comes from `media.py presets`; every
  count is exact.
- **An invented URL, figure or endorsement.** The URL is the one the author gives, and a claim is
  one the piece's sources support.
- **Duplicating the social plan.** Where syntek-author's social-media family is present, its
  calendar plans the posts; the media schedule lists media deliverables only, and cites it.
- **Writing the written side's words.** A placement never drafts a post's, page's or issue's
  body, standfirst or link text, and media never edits a website or sends an email.
- **Scheduling past an open gate.** No schedule row is `ready` until M6 is recorded, every rights
  row is `cleared` and the flags run is clean.
- **Rewriting the log.** A publish-log row is never deleted or edited over; a correction is a
  dated note in its Notes.

## Cross-references

- `cut-for-platform` — the render each deliverable names.
- `captions` — the captions each deliverable names, burned or sidecar.
- `thumbnail-brief` — the approved thumbnail each deliverable names.
- `repurpose` — the cut-down plan whose agreed cuts are packaged here.
- `publishing/src/schedule.md` and `publishing/src/publish-log.md` — the schedule and the log this
  skill keeps.
- `production/src/rights-register.md` — the rows M7 needs `cleared`.
- `brand/src/platforms/` — each platform's profile: the handle, the deliverables used and, where
  no social plan is present, the cadence, tone, call to action and hashtag sets.
- The social-media-documents skill (syntek-author), where present — the social media plan, the
  content calendar, bios and text-only posts.

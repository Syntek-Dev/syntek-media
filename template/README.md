# <%BRAND_NAME%>

> <%BRAND_DESCRIPTION%>

<: if BRAND_KIND == 'business' :>The video and audio of <%BRAND_NAME%>, a business: social video, recorded talks and explainers,
made by <%OWNER_NAME%> from plain files under Git, with Claude Code as a production partner.
<: endif :><: if BRAND_KIND == 'author-fiction' :>The video and audio of <%BRAND_NAME%>, a novelist's brand: book trailers, audiobooks and author
socials, made by <%OWNER_NAME%> from plain files under Git, with Claude Code as a production partner.
<: endif :><: if BRAND_KIND == 'author-nonfiction' :>The video and audio of <%BRAND_NAME%>, a non-fiction author's brand: talks, a podcast, audiobooks
and author socials, made by <%OWNER_NAME%> from plain files under Git, with Claude Code as a
production partner.
<: endif :>Generated from the syntek-media template on <%DATE%>.

---

## Overview

- **Brand:** <%BRAND_NAME%>
- **Brand kind:** <%BRAND_KIND%>
- **Platforms:** <% PLATFORMS | join(', ') %>
- **Media kinds:** <% MEDIA_KINDS | join(', ') %>
- **Owner:** <%OWNER_NAME%>
- **Audience test:** <%AUDIENCE_TEST%>

The brief above is a starting point. The working version, kept current by every update, is the
brand section of `.claude/rules/syntek-media/01-layout-and-routing.md`, and the running state
(release cadence, the next publish date, where each piece stands) is in `.claude/MEMORY.md`.

---

## How the repository is laid out

| Folder | Kind | Holds |
|---|---|---|
| `brand/` | production | The brand kit: design tokens, preview cards and the thumbnail and card layouts, design exports, the spoken voice, and one profile per platform |
| `scripts/` | production | The pieces: one folder per piece with its brief, script or transcript, storyboard and shot list |
| `production/` | production | Source media and its manifest, voiceover, edit decision lists, cards, timing and scene files<: if 'audiobook' in MEDIA_KINDS :>, audiobook chapters<: endif :>, the rights register and the credits log |
| `publishing/` | production | Cut-down plans, captions, thumbnails, post packages, the schedule and the publish log |
| `toolkit/` | supporting | The command line every render runs through, the platform data and the fallback layouts |
| `.claude/` | config | Claude Code's manual, rules, memory, settings and skills |

Each production layer has `docs/` (guides), `src/` (the work) and `workflows/` (step-by-step
procedures). Every folder carries a `CONTEXT.md` (what is here) and a `CLAUDE.md` (how to work
here). The full map is `CONTEXT.md`.

---

## The production loop

Each piece (a short, an explainer, a talk, a trailer, an episode, an audiobook) climbs one
ladder, and you decide every step:

1. **Brief.** You and Claude settle what the piece is for, who it is for, its hook, its call to action, what it must disclose and what it needs to clear.
2. **Script, or recording.** Claude drafts a script written for the ear, or brings in a recording you made and transcribes it<: if 'audiobook' in MEDIA_KINDS :>, or, for an audiobook, plans its chapters and credits instead<: endif :>; you approve it.
3. **Storyboard.** Every spoken line gets a picture, and every shot a source.
4. **Voice and footage.** Claude makes a voiceover only when you ask, after telling you what it will cost; your footage is logged, never moved.
5. **Master.** The toolkit assembles the master from tracked files; you watch or hear it through.
6. **Cut-downs and captions.** One cut per platform, each verified against that platform's specification, with captions burned in or alongside.
7. **Thumbnail and post.** Claude prepares the post package and the schedule row; you post, then tell Claude the link for the publish log.

A piece moves up only when its gate passes and you say so. The gates are in
`scripts/docs/reference/the-piece-ladder.md`, and the rules behind them in
`.claude/rules/syntek-media/03-production-ethics.md`.

---

## Producing

```sh
python3 toolkit/media.py --help                 # every command, with its arguments
python3 toolkit/media.py check --setup          # what this machine still needs, before the first spend
python3 toolkit/media.py script time scripts/src/pieces/<piece>/script.md
python3 toolkit/media.py assemble production/src/edits/<piece>.toml
python3 toolkit/media.py cut <master> --deliverable <platform>.<format> --in <start> --out <end>
python3 toolkit/media.py captions check <captions>.srt --script <script or transcript>
python3 toolkit/media.py flags                  # every AUTHOR TO CONFIRM and VERIFY still open
uv run toolkit/card.py render <layout>.html --deliverable <platform>.<format>
python3 toolkit/media.py image <png or render> --deliverable <platform>.<format>   # JPEG, WebP, AVIF, posters
<: if 'podcast' in PLATFORMS :>python3 toolkit/media.py feed check <show>           # a self-hosted show's register and feed, offline
<: endif :>```

Renders are generated: never edit one by hand; change the source and render again. Masters,
deliverables and generated audio are ignored by Git, and source footage lives in external
storage, listed in `production/src/footage/manifest.toml`. An approved voiceover take cannot be
made again, so archive it when you approve it.
Each piece's output has its own ignored folder in `production/src/renders/`,
`production/src/voiceover/generated/` (takes in its takes subfolder) and
`publishing/src/renders/`. Tracked timing and scene files stay flat under the piece's name in
`production/src/timing/` and `production/src/scenes/`. `python3 toolkit/media.py where <piece>`
lists its tracked files and names its output folders without listing their contents.

**Audio** comes from ElevenLabs, through an MCP server named `elevenlabs` that you add once at
user scope; the template adds nothing to `.mcp.json`, and your API key never enters the
repository. The server's base path must contain this project, or speech-to-text refuses every
file in it. The exact command is in `production/docs/reference/elevenlabs.md`.

**Requirements:** `git`; Python 3.11 or later; `ffmpeg` and `ffprobe` built with libass, x264
and mp3lame; `uv`, for Copier and for `toolkit/card.py`, with Playwright's Chromium
(`uv run --with playwright==1.62.0 playwright install chromium`); `git-lfs`, if you keep large
design exports; and `espeak-ng` (optional, for a scratch voice track). `check --setup` reports
each one.

---

## Working with Claude Code

- Open Claude Code at the root of this repository. `.claude/CLAUDE.md` and the template's rules
  load automatically.
- Say what you want in plain words ('brief a 30-second short on the new opening hours', 'cut this
  for every platform', 'caption the talk') and the skill for that job runs; a request no skill
  matches, or 'what's next?', goes to the `run-media-workflow` skill, which finds the procedure.
  Skills can also be called by name, such as `/write-script`.
- Claude never spends credits unasked: it states the characters, the calls and the estimated
  credits, waits for your yes, and the settings make every credit-spending tool ask again.
- Claude never posts. It prepares each post and its schedule row; you post.
- Anything Claude cannot settle on its own is left in the text as an `AUTHOR TO CONFIRM` or
  `VERIFY` flag. `python3 toolkit/media.py flags` lists them.
- When a session grows long, Claude writes a handoff and stops, rather than compacting. Run
  `/clear` and continue from the handoff.

---

## Conventions

- British English (en_GB); single quotation marks; dates DD/MM/YYYY; 24-hour time; timecodes
  HH:MM:SS.mmm.
- Write 'Section 3.2', never the section sign.
- In `src/` folders, one sentence per line; a script is one spoken sentence per line.
- A piece is named `NNN-kebab-title` (`003-why-the-ferry-runs-late`), and every file about it
  starts with that name.

---

## Updating from the template

The template improves over time. To take its changes, commit or stash your own work first, then:

```sh
uvx copier update --trust -a .copier-answers.syntek-media.yml
git diff                  # review every change before committing
```

Copier may print a `MissingFileWarning` about `.copier-answers.syntek-media.yml`. It is expected
and harmless: the template reads your previous answers so it can refuse a changed `BRAND_KIND`.

- **What updates:** the template's own files: the rules in `.claude/rules/syntek-media/`, the
  skills, the reference guides, the template workflows, the toolkit and its platform data.
- **What never changes:** your work, and the files seeded for you once: the registers and logs,
  the footage manifest, the design tokens and preview cards, the voice file and the platform
  profiles. If you delete one of those seeds, the update brings back an empty one.
- **The shared files are written once and never again:** this README, `CONTEXT.md`, `.gitignore`,
  `.mcp.json`, `.claude/CLAUDE.md`, `.claude/CONTEXT.md`, `.claude/MEMORY.md`,
  `.claude/settings.json` and the `.claude/skills/` pair. An update never touches them, and one
  you delete stays deleted. If you delete the worked example, it stays deleted too.
- **Never edit the rules in `.claude/rules/syntek-media/`**, or any other file the template owns:
  the next update overwrites the edit or turns it into a conflict. Put your own rules under
  'Project-specific rules' in `.claude/CLAUDE.md`, your own guides in a layer's `docs/project/`,
  and your own procedures in its `workflows/local/`.
- **Never edit `.copier-answers.syntek-media.yml` by hand.** To change an answer, give it to the
  update; the brand section of the rules follows it on its own:

  ```sh
  uvx copier update --trust -a .copier-answers.syntek-media.yml --data AUDIENCE_TEST='…'
  ```

- **`BRAND_KIND` never changes.** An update refuses a different brand kind and touches nothing; a
  different brand kind is a new project.

### Removing a platform or a media kind deletes its files

Removing a platform from `PLATFORMS`, or a media kind from `MEDIA_KINDS`, on an update deletes
**every file it generated, including seeds you have filled in**. Git keeps the last committed
copy, but copy out anything you still need and commit before you run the update. Files you
created yourself are never deleted. A list answer replaces the whole list:
`--data 'PLATFORMS=[youtube, podcast]'` removes every platform not named. In this project:

<: if 'youtube' in PLATFORMS :>- Without `youtube`: `brand/src/platforms/youtube.md` (your profile) and
  `publishing/docs/reference/youtube.md` are deleted.
<: endif :><: if 'tiktok' in PLATFORMS :>- Without `tiktok`: `brand/src/platforms/tiktok.md` (your profile) and
  `publishing/docs/reference/tiktok.md` are deleted.
<: endif :><: if 'instagram' in PLATFORMS :>- Without `instagram`: `brand/src/platforms/instagram.md` (your profile) and
  `publishing/docs/reference/instagram.md` are deleted.
<: endif :><: if 'linkedin' in PLATFORMS :>- Without `linkedin`: `brand/src/platforms/linkedin.md` (your profile) and
  `publishing/docs/reference/linkedin.md` are deleted.
<: endif :><: if 'facebook' in PLATFORMS :>- Without `facebook`: `brand/src/platforms/facebook.md` (your profile) and
  `publishing/docs/reference/facebook.md` are deleted.
<: endif :><: if 'podcast' in PLATFORMS :>- Without `podcast` among the platforms: `brand/src/platforms/podcast.md` (your profile),
  `publishing/docs/reference/podcast.md`, `publishing/docs/reference/podcast-feed.md`,
  `publishing/workflows/08-publish-the-podcast-feed/` and the pair of `publishing/src/podcast/`
  are deleted; your show registers and saved feeds stay.
<: endif :><: if 'website' in PLATFORMS :>- Without `website`: `brand/src/platforms/website.md` (your profile, its sites and their
  agreements) and `publishing/docs/reference/website.md` are deleted.
<: endif :><: if 'blog' in PLATFORMS :>- Without `blog`: `brand/src/platforms/blog.md` (your profile) and
  `publishing/docs/reference/blog.md` are deleted.
<: endif :><: if 'newsletter' in PLATFORMS :>- Without `newsletter`: `brand/src/platforms/newsletter.md` (your profile, its lists) and
  `publishing/docs/reference/newsletter.md` are deleted.
<: endif :><: if 'audiobook' in MEDIA_KINDS :>- Without `audiobook`: the `narrate-audiobook` skill, `production/src/audiobook/` (its pair
  and the README files of its generated and renders folders; your chapter registers stay),
  `production/workflows/05-narrate-an-audiobook/`, `production/workflows/06-master-an-audiobook/`
  and `production/docs/reference/audiobook-narration.md` are deleted.
<: endif :><: if 'podcast' in MEDIA_KINDS :>- Without `podcast` among the media kinds: `scripts/docs/reference/podcast-episodes.md` and
  `production/workflows/04-master-a-podcast-episode/` are deleted.
<: endif :><: if 'trailer' in MEDIA_KINDS :>- Without `trailer`: `scripts/docs/reference/trailers.md` is deleted.
<: endif :><: if 'short-video' in MEDIA_KINDS :>- Without `short-video`: `scripts/docs/reference/short-video.md` is deleted.
<: endif :><: if 'long-video' in MEDIA_KINDS :>- Without `long-video`: `scripts/docs/reference/long-video.md` is deleted.
<: endif :><: if 'voiceover' in MEDIA_KINDS :>- Without `voiceover`: `scripts/docs/reference/standalone-voiceovers.md` is deleted; the
  `voiceover` skill and its workflow stay.
<: endif :>
**After any change of platforms or media kinds, edit by hand the files that describe them**,
because Copier never rewrites them: this README, `CONTEXT.md`, Section 1 of `.claude/CLAUDE.md`,
and any rows for a removed platform in `brand/src/platforms/overrides.toml`. The brand section of
the rules updates itself.

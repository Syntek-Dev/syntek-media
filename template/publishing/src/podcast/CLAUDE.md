@./CONTEXT.md

# CLAUDE.md — publishing/src/podcast/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/src/CONTEXT.md` → `publishing/src/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep one register per self-hosted show and its feed as last published, so every value Apple
Podcasts and Spotify read is written once, reviewed, and never changed by accident.

## How to work here

- **Routing:** workflow `publishing/workflows/08-publish-the-podcast-feed/`; skills
  `prepare-post` (the words, the status, the tracked feed) and `cut-for-platform` (`feed tag`);
  guide `publishing/docs/reference/podcast-feed.md`.
- **Model:** **Opus** for every word a listener reads and every chapter title, with the author;
  the mechanical tier for `feed new`, `feed add`, `feed tag`, `feed chapters`, `feed check` and
  `feed write` (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** `feed new` once per show → the show's details with the author, `approved`
  dated → per episode, `feed add` → its words and chapters, approved → `feed tag` →
  `feed chapters` → `feed check` → `ready` → the upload copy → on the author's report, `published`
  and the tracked feed.
- **Definition of done:** `feed check SHOW` exits 0; no `AUTHOR TO CONFIRM` is left in the
  register; the tracked feed equals the copy the author uploaded.

## Guardrails

- **Identity is for life.** Never type, recompute or edit `feed_url`, `podcast_guid` or a row's
  `guid`; `feed new --rekey` alone corrects them, and only while nothing is published.
- **Never delete an episode row.** An episode taken down is `withdrawn`: kept here, left out of
  the feed.
- **Never hand-edit a feed.** The tracked `<show>.feed.xml` is written only by `feed write -o`,
  after the author reports the upload live; a feed check that fails is fixed in the register.
- **A corrected file gets a new URL** in `audio_url`; its `guid` never changes.
- **Plain text only:** no `<` or `>` in a title or a description; the disclosure sentence in the
  show's description and every episode's where a synthetic voice speaks.
- **The owner address is public:** a role address, never a person's own.

## Output & naming

- **Written by skills (with the author):** `<show>.toml`, from this skeleton, which
  `media.py feed new` writes (it also flags `owner_email` for the author to confirm):

```toml
[show]
show = "<show>"              # kebab slug, frozen: names this file and its feed
title = ""                    # no episode numbers; within platform.podcast.tag_max_chars
site = ""                     # the website profile's slug of the site serving the feed, where that platform is chosen; else "" and the podcast profile names the server
feed_url = ""                 # written by feed new from --feed-url: the feed's permanent https URL, for life (D58); feed new --rekey alone changes it, before anything is published
new_feed_url = ""             # only while moving the feed: a redirect too, for platform.podcast.feed_move_min_days
link = ""                     # the show's page
media_base = ""               # the URL folder the audio, art, captions and chapters are published under
language = "en-gb"
author = ""
owner_name = ""
owner_email = ""              # public: the directories send their ownership codes here; a role address (feed new flags it)
copyright = ""
category = ""                 # Apple's category, exactly as Apple spells it
subcategory = ""
explicit = false
type = "episodic"             # episodic | serial (serial: every episode numbered)
cover = ""                    # the published name of the podcast.cover render; a new cover gets a new name
id3_cover = ""                # the podcast.id3_cover render encode embeds in every episode; "" = none
podcast_guid = ""             # written once by feed new; never recomputed (feed new --rekey only while nothing is published)
locked = true                 # no other host may import the feed
complete = false
block = false
youtube_route = "upload"      # upload | rss | none (D58: never upload and rss for one show)
description = """
"""                           # plain text, one sentence per line; within platform.podcast.show_description_max_bytes; the disclosure sentence where any episode uses a synthetic voice (D25)
approved = ""                 # DD/MM/YYYY: the author approved the show's details
last_updated = ""

[[episode]]                   # one row per episode, in any order; never deleted
piece = ""                    # the piece (D17)
guid = ""                     # written once by feed add; NEVER changes, even when the title or the URL does
title = ""                    # no episode or season number, no show name
number = 0                    # 0 = left out (serial needs it)
season = 0
type = "full"                 # full | trailer | bonus
explicit = false
pub_date = ""                 # DD/MM/YYYY HH:MM, the project's timezone: <pubDate>; the schedule row's time
render = ""                   # written by feed tag: the podcast.feed_audio render's name
audio_url = ""                # "" = media_base + the render's name; a corrected file gets a NEW url, the guid stays
bytes = 0                     # written by feed tag; equals the served Content-Length
seconds = 0.0                 # written by feed tag: the render's probed duration
art = ""                      # the published name of a podcast.episode_art render; "" = the show's cover
page = ""                     # the episode page on the feed's site (pages on other sites are placements, D61)
transcript = ""               # the published name of the master-timed VTT; "" = none
description = """
"""                           # plain text (no < or >), one sentence per line; within platform.podcast.episode_description_max_chars; the disclosure sentence (D25)
status = "planned"            # planned (feed add) · ready (M7, the feed workflow) · published (the author's report, publishing/workflows/06-record-a-publication/) · withdrawn (kept here, left out of the feed)
notes = ""

[[episode.chapter]]           # optional; at least platform.podcast.chapters_min, the first at 00:00:00.000
start = "00:00:00.000"        # on the master (D29)
title = ""                    # within platform.podcast.chapter_title_max_chars; title case
```

- **Statuses:** `planned` (`feed add`) · `ready` (M7, through the feed workflow) · `published`
  (the author's report) · `withdrawn`.
- **Written by the toolkit, tracked:** `<show>.feed.xml`, by `feed write -o` only.
- **Generated (never hand-edit), in `publishing/src/renders/`:** each episode's
  `<piece>.podcast-feed-audio.mp3`, its `<piece>.chapters.json`, and the upload copy
  `<show>.feed.xml`.

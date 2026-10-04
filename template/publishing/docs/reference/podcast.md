---
type: guide
skills: [prepare-post, cut-for-platform]
model: opus
---

# Podcast — Apple Podcasts and Spotify: audio, artwork, disclosure in the audio

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How this project's audio reaches podcast apps: the keys of
`toolkit/data/platforms.toml` each deliverable reads, the show's cover and each episode's art,
and why a podcast discloses synthetic speech in the audio itself as well as in its text. One feed
reaches Apple Podcasts and Spotify alike, so an episode is made once, to the stricter of the two.
Every limit is cited by key and read with `python3 toolkit/media.py presets KEY`, overrides
applied. The brand's own show details, cadence and tone live in its profile in
`brand/src/platforms/`.

## Deliverables and their keys

| Deliverable | Key | Notes |
|---|---|---|
| An episode for the feed | `podcast.apple_rss_audio` | AAC recommended over MP3; its loudness is the podcast target |
| An episode for Apple Podcasts Connect | `podcast.apple_connect_audio` | a single-channel file is rejected: mono is sent as two identical channels |
| An episode for Spotify | `podcast.spotify_audio` | no loudness published (`verify`): the feed's target serves |
| The show's cover | `podcast.cover` | square; no transparency (`alpha = false`) |
| An episode's art | `podcast.episode_art` | Apple advises no logo or text: the title shows beneath it |

- Loudness for every episode comes from `[platform.podcast.apple_rss_audio]`, and is set when the
  master is made (`production/docs/reference/sound-and-loudness.md`); an episode is encoded from
  that master with `media.py encode`, never re-levelled by hand.
- Episodes are mastered by the podcast-episode workflow in `production/workflows/`, where the
  project makes podcast episodes.

## Words

- Spotify's specification advises keeping every listener-facing field except descriptions short
  enough for every app; read its `notes`, and treat it as advice the package follows.
- The episode description carries the disclosure sentence, and the show description its own.

## Disclosure

Apple's guideline 1.11 asks for synthetic voices and other AI-generated audio to be disclosed
prominently in the content and in the metadata of each episode and of the show; Spotify has no
such rule, but the same feed reaches both, so Apple's rule governs every episode. That means a
spoken line in the episode, a sentence in the episode description and one in the show
description (`publishing/docs/reference/ai-disclosure.md`). Spotify removes a show that
impersonates another creator's likeness without permission.

## Traps

- **Captions:** a podcast needs none unless its brief asks for a transcript, so M6 reads `n/a`
  for it, with that reason.
- **The host, not the toolkit, publishes:** the author uploads each episode to the show's host;
  the log records the episode's public link as the author gives it.
- **An episode on a video platform** is a still under its audio, made with `media.py still-video`
  and posted under that platform's own guide.

## How we apply it here

- Read `presets` for every key above before an encode or a package, and name each `verify` key
  relied on in the hand-back.
- Write the spoken disclosure line into the script before the episode is recorded or generated.

## Who implements it

- **Workflows:** `publishing/workflows/05-prepare-a-post/` writes the episode's package;
  `publishing/workflows/02-cut-for-a-platform/` encodes each deliverable from the master.
- **Skills:** `prepare-post` writes the descriptions and the disclosure; `cut-for-platform`
  encodes and verifies each deliverable.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 5 owns disclosure and Section 7 owns
never fabricating a platform rule or limit. The rules own the requirement; this guide owns how the
podcast keys and rules are applied to this project's episodes.

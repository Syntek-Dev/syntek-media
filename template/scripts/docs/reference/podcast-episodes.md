---
type: guide
skills: [write-script, cut-for-platform]
model: opus
---

# Podcast episodes — an episode's shape, its voices and its disclosure

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** An episode is a piece made to be heard, usually through earphones and often while
the listener does something else. It is `kind: podcast` with `picture: false`, so its M3 is
`n/a — no picture`, and it needs captions only where its brief asks for a transcript. It is
either scripted (a solo episode, a narrated feature) or recorded (a conversation, an interview,
a talk), and either way it is cut to an audio master.

## The shape of an episode

| Part | Does |
|---|---|
| Cold open | The best moment of the episode, or the question it answers, in the first lines. |
| Introduction | The show, the host, the guest and the promise of this episode, briefly. |
| Segments | One subject each, opened and closed in words, because a listener cannot see a heading. |
| Close | What was said, the one thing to do next, and the credits. |

Each part is a beat in the script, or an anchored beat in the transcript of a recorded episode.

## Host and guest

A scripted episode writes every spoken line under `HOST:`, `GUEST:` or `NARRATOR:`. A
conversation is not scripted line by line: its brief carries the questions and the order of
subjects, the conversation is recorded, and the transcript is made from the recording. Signpost
in speech what a reader would see on a page: who is talking, what is coming, where a segment
ends.

## Disclosure in the audio

An episode that uses a synthetic voice, generated music or generated sound says so in the audio
itself, in the episode's notes and in the show's details, as well as in each platform's own way.
The disclosure plan in the brief names the line and where it is spoken; the platform rules and
their sources are in `publishing/docs/reference/ai-disclosure.md`.

## The audio master

The master is audio only: an edit decision list with `size = ""`, cut from the recording's clips
or the voiceover segments, under a music bed that is trimmed and faded. Its loudness target is
read from the podcast audio table in `toolkit/data/platforms.toml`, never written here. An
episode that also goes to a video platform goes as a still under the audio, made with
`python3 toolkit/media.py still-video`.

## How we apply it here

- Name the episode's one promise in the brief's `## Hook`, and keep it before the close.
- A guest's words are theirs: a transcript is corrected only for a mis-transcription, and a
  recorded claim that proves wrong is cut, corrected in the episode notes or accepted by the
  author, and never re-voiced.
- Music beds, idents and guest appearances each need a rights row before M7.

## Who implements it

- **Workflows:** `scripts/workflows/02-write-a-script/` writes a scripted episode;
  `production/workflows/04-master-a-podcast-episode/` cuts and masters every episode.
- **Skills:** `write-script` writes the script; `cut-for-platform` writes the edit decision list
  and renders the master.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 5 owns AI disclosure, including
disclosure in the audio for a podcast, and Section 6 owns rights and consent. The rules own the
requirements; this guide owns how an episode is shaped to be heard.

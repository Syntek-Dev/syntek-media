---
type: guide
skills: [narrate-audiobook]
model: opus
---

# Audiobook narration — three routes, chosen per channel, disclosed always

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** An audiobook is one piece whose deliverables are `audiobook.<store>` keys and
whose chapters are made one by one and recorded in `production/src/audiobook/<piece>.md`. It has
no script: that register, with its credit rows `ch00` and `ch99`, is its plan, and the author's
approval of it is its M2. How a chapter is voiced depends on where it is going, because stores
disagree about synthetic narration: the route is chosen per channel with the author, and recorded.

## Three routes

| Route | Narrator | Made and checked | For |
|---|---|---|---|
| `human` | the author, or a narrator they engage | recorded, logged as source media, mastered and checked by the toolkit | any channel; the only route to ACX and Audible unless the author is authorised otherwise |
| `ai` | an ElevenLabs voice through the MCP | `audiobook text`, one call per chunk, `take add`, then mastered and checked by the toolkit | only a channel that accepts such a master, with its disclosure set |
| `external` | ElevenLabs' own audiobook product | outside this template: the register records the export, where it is kept and its disclosure | a channel that takes only that product's package |

`narrate-audiobook` refuses to generate or master for a channel on the `external` route.

## Where each channel stands

| Channel (its `channels` name in the register) | Synthetic narration | Checked |
|---|---|---|
| ACX and Audible (`acx`) | not accepted: human narration only, unless ACX authorises otherwise | 03/10/2026; an author's own voice replica as an authorised route is `VERIFY` |
| Spotify for Authors (`spotify_authors`) | accepted, with its digital voice narration box ticked; Spotify adds a line to the description | 03/10/2026; its bitrate and level rules are `VERIFY` |
| Voices by INaudio (`inaudio`) | accepted only as an unmodified LPF package from ElevenLabs' own product (or two other named providers); a plain MP3 master does not qualify | 03/10/2026; its audio specs are `VERIFY` |
| Google Play Books (`google_play`) | its own auto-narration accepted; third-party synthetic files reported accepted | `VERIFY`, 03/10/2026 |
| Kobo Writing Life (none yet: the toolkit has no table for it) | reported to accept synthetic narration, labelled as such | `VERIFY`, 03/10/2026 |
| Apple Books (none yet: the toolkit has no table for it) | its own digital narration, through partners; other synthetic narration not addressed | `VERIFY`, 03/10/2026 |

A store changes its rule without notice: re-check its row before relying on it.

## Chapter text

`python3 toolkit/media.py audiobook text SOURCE --piece PIECE --chapter chNN` reads a chapter
from its source (a syntek-author unit whose status is `final`, where present, unless the author
says otherwise, or a text the author provides). It strips section markers, comments, citation
keys and Pandoc divs and spans, handles footnotes as the mode file says, applies the
pronunciations in `brand/src/voice/voice.md`, and lists every word or reference with no spoken
form before anything is spent. It writes chunks at paragraph boundaries, under the recorded
model's character limit, to `production/src/audiobook/generated/`, and ends a chunk at every
pause (a scene break is `{pause 2}`), recording it in the chapter's `<piece>.chNN.chunks.toml`:
no pause mark is ever sent to ElevenLabs as text. Chapter text is never copied into a tracked
file; the credits' words are written in their own files beside the register.

## Mastering to the ACX targets

`audiobook master` joins a chapter's approved takes, with the pauses its chunk sidecar records,
or masters its recording, with room tone at head and tail. `audiobook check` measures every file
against `[audiobook.acx]` in `toolkit/data/platforms.toml`, by key, never by a number copied here:
RMS, peak and noise floor; room tone at head and tail; length; sample rate and constant bitrate;
and the same channels in every file (mono by house choice). The credits are files of their own; a
retail sample is cut from a mastered chapter with `media.py cut --deliverable audiobook.acx`,
within `sample_max_seconds`. A take re-encoded up to ACX's bitrate meets the letter, not the intent.

## How we apply it here

- Disclosure always: a synthetic narrator is named as one on every channel, whatever its toggle.
- Recordings and approved mastered chapters are archived as source media; a chunk take only where
  the author wants it kept, because the master is what M4 reads.
- A register row moves `planned · generated · recorded · mastered · checked · packaged`.

## Who implements it

- **Workflows:** `production/workflows/05-narrate-an-audiobook/` and
  `production/workflows/06-master-an-audiobook/`.
- **Skill:** `narrate-audiobook`, with the call discipline of
  `production/docs/reference/elevenlabs.md`.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 4 owns credits and Section 5 owns
disclosure; `[audiobook.acx]` in `toolkit/data/platforms.toml` holds the targets the toolkit
checks. This guide owns how an audiobook is voiced, mastered and sent.

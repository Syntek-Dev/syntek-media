---
type: guide
skills: [prepare-post, cut-for-platform, thumbnail-brief, captions]
model: opus
---

# Blog — posts that carry the brand's media: video, transcripts, featured and share images

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How this project's media reaches a blog post on a site of the blog profile, the
brand's own or one it writes for: the keys each file reads, the video's two routes, the captions
and transcript under the player, the featured and share images, and the tests a self-hosted file
must pass. A site is a row of `## Sites` in `brand/src/platforms/blog.md`; where the project also
has the website platform, the blog reuses the website profile's slugs. Limits are read with
`media.py presets KEY`. The post (its body, headings, standfirst, figure captions, link text,
slug and date) is the written side's; media supplies the files and the words outside the body.

## Deliverables and their keys

| Deliverable | Key | Notes |
|---|---|---|
| A video in the post | `blog.video` | WebVTT sidecar; a full-width layout takes a website key instead |
| Its poster | `blog.poster` | `media.py image` of the video's render at `--at` |
| The featured image | `blog.featured_image` | `card.py render`, then `media.py image` once per format: the JPEG is the `<img>` fallback |
| A share image | `blog.og_image` | as the website's share image: a project may have a blog without a website |
| An embed | `youtube.long` | a placement of the upload: no render of its own |

## Placements and agreements

- **A placement** is the one file the post plays or shows first: `## <key>[ — cNN] — blog:<slug>`,
  with Placement (slug, post, route), Written piece (by path in prose, read, never edited), Title
  (a figure's or an embed's only), Alt text, Links to, Structured data (the VideoObject values),
  Agreement, Disclosure, Captions, Images (poster, featured and share images), Render, Calendar,
  Scheduled (the post's own date, cited) and Limits.
- **A post that plays nothing** of the piece places its featured image; a text-only post's
  featured image is a design export (`brand/workflows/03-record-a-design-export/`).
- **The agreement** is `own`, or the dated record for a site the brand does not own; where the
  website profile lists the site, the blog row reads 'see website' and the placement cites that.
- **An embed** follows the website guide's rule where the project has it: the privacy-enhanced
  host behind a click-to-load facade, its consent the site's (`VERIFY`), linked to the upload.
- **Worked placement:** a cut of a talk in a post on the studio's site is
  `## blog.video — c01 — blog:studio`, Written piece the post's unit, Agreement 'see website'.

## Captions, transcripts and search

- The video's `.vtt` loads by `<track kind="captions" srclang="en-GB">`, never burned
  (`platform.blog.captions_required`); the post publishes the transcript of exactly what it plays
  right under the player, or a link to it there: one per distinct cut placed.
- The featured image meets `platform.blog.featured_min_width` and the other structured-data
  minimums of `[platform.blog]`; it is never lazy-loaded, and its alt text says what it shows.
- A script for a piece bound for a post says aloud what the picture shows (no audio description).

## Hosting tests

Run by the author on the published URLs and cited by the Render bullet; the toolkit never fetches:

```text
curl -sI <video_url>       # 200; Content-Length and Content-Type: video/mp4
curl -s --range 0-99 <video_url> -o /dev/null -w '%{http_code} %{size_download}\n'   # 206 100
curl -sI -H 'Origin: https://<post domain>' <vtt_url>   # text/vtt; Access-Control-Allow-Origin
```

## How we apply it here

- A placement's status is the post's, read at M7: a post that is not `final` is a warning.
- A podcast episode page inside a post is a placement of the feed's audio, as the podcast-feed
  guide sets out, where the project has the podcast.

## Who implements it

- **Workflows:** `publishing/workflows/02-cut-for-a-platform/` (video),
  `publishing/workflows/03-caption-a-piece/` (`.vtt`, transcript),
  `publishing/workflows/04-brief-a-thumbnail/` (images), `publishing/workflows/05-prepare-a-post/`.
- **Skills:** `cut-for-platform`, `captions`, `thumbnail-brief` and `prepare-post`.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the ladder (M6 on a profile
site, M7's placements and agreements), Section 5 disclosure and Section 7 never fabricating a
limit. The rules own the requirement; this guide owns how the blog keys and routes apply here.

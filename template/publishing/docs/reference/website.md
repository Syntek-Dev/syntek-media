---
type: guide
skills: [prepare-post, cut-for-platform, thumbnail-brief, captions]
model: opus
---

# Website — the sites the brand publishes to: self-hosted or embedded video, posters, share images

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** How this project's media reaches the sites of the website profile, the brand's
own and any it writes for: the keys each file reads, the two routes a page plays a video by, the
captions and transcript every such site carries, and the tests a self-hosted file must pass. A
site is a row of `## Sites` in `brand/src/platforms/website.md`, named by a frozen slug, and one
render serves every page that uses its key. Limits are read with `media.py presets KEY`. Media
owns the files and the words outside the page's body; the page is the written side's.

## Deliverables and their keys

| Deliverable | Key | Notes |
|---|---|---|
| A self-hosted video | `website.video`, `website.video_720` | WebVTT sidecar; the lighter one for a narrow player |
| A silent loop | `website.hero_loop` | a cut of the plan; no sound track (`audio_tracks = 0`), no captions |
| A poster | `website.poster`, `website.poster_720` | `media.py image` of the video's render at `--at`; the 720 one fronts the lighter video and the loop |
| A share image | `website.og_image` | `card.py render`, then `media.py image` |
| An embed | `youtube.long` | a placement of the upload: no render of its own |

## Placements and agreements

- **A placement** is the one file a page plays or shows first: `## <key>[ — cNN] — website:<slug>`,
  with Placement (slug, page, route), Written piece (by path in prose, read, never edited), Title
  (an embed's or figure's only), Alt text, Links to, Structured data (the VideoObject values),
  Agreement, Disclosure, Captions, Images (poster, share image), Render, Calendar, Scheduled (the
  written piece's own date, cited) and Limits. Standfirsts and link text are the written piece's.
- **The agreement** is `own`, or the dated record in the site's row: no placement on a site the
  brand does not own is `ready` without it. An image in that site's own branding is a design
  export (`brand/workflows/03-record-a-design-export/`).
- **An embed** loads from `platform.website.embed_host` behind a click-to-load facade, at least
  `platform.website.embed_min_width` wide; consent is the site's (`VERIFY`). It Links to the
  upload, posted first.
- **Worked placement:** the talk on the studio's own site is `## website.video — website:studio`,
  Agreement `own`; a cut on a second site is `## website.video_720 — c02 — website:second-site`.

## Captions, transcripts and motion

- A self-hosted video with speech carries its `.vtt` by `<track kind="captions" srclang="en-GB">`,
  never burned, from the same origin or with CORS (`platform.website.captions_required`).
- Every piece or cut with speech placed on a page has its published transcript of exactly what
  that page plays, right under the player or linked there; an embed keeps the upload's captions.
- A loop starts by itself, so its page gives it a pause control and a still for reduced motion
  (WCAG 2.2 SC 2.2.2, the site's code), and nothing in it flashes (SC 2.3.1).
- Video for the brand's sites takes the house loudness, as social video does.

## Hosting tests

Run by the author on the published URLs and cited by the Render bullet; the toolkit never fetches:

```text
curl -sI <video_url>       # 200; Content-Length and Content-Type: video/mp4
curl -s --range 0-99 <video_url> -o /dev/null -w '%{http_code} %{size_download}\n'   # 206 100
curl -sI -H 'Origin: https://<page domain>' <vtt_url>   # text/vtt; Access-Control-Allow-Origin
```

## How we apply it here

- A poster is never lazy-loaded above the fold; alt text says what the image shows.
- A site serving a self-hosted podcast feed names it under Carries; the feed itself is the
  podcast-feed guide's. The blog and newsletter guides take the same placement rule.

## Who implements it

- **Workflows:** `publishing/workflows/02-cut-for-a-platform/` (video and loop),
  `publishing/workflows/03-caption-a-piece/` (`.vtt`, transcript),
  `publishing/workflows/04-brief-a-thumbnail/` (images), `publishing/workflows/05-prepare-a-post/`.
- **Skills:** `cut-for-platform`, `captions`, `thumbnail-brief` and `prepare-post`.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the ladder (M6 on a profile
site, M7's placements and agreements), Section 5 disclosure and Section 7 never fabricating a
limit. The rules own the requirement; this guide owns how the website keys and routes apply here.

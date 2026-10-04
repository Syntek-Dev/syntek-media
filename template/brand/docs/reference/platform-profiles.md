---
type: guide
skills: [prepare-post]
model: opus
---

# Platform profiles — the brand's own choices for each platform, and its corrections

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A profile, `brand/src/platforms/<platform>.md`, holds what the brand decides for
one platform: the account (or its sites or lists), the deliverables it uses there and, where no
written-side document sets them, its cadence, tone, call to action and hashtag sets. One ships for
each platform chosen. The platform's own facts (sizes, lengths, limits, codecs, its AI label) live,
dated and sourced, in `toolkit/data/platforms.toml`, read as `platform-specs.md` explains.

## What a profile holds

| Section | Holds |
|---|---|
| `## Account` | the handle and URL, exactly as the platform shows them; flagged until the author gives them |
| `## Sites` (website, blog) | one row per site, its own or one it writes for: slug, domain, owner, CMS, player, captions, what it carries, agreement |
| `## Lists` (newsletter) | one row per list: slug, sender, service, owner, where its images are hosted, agreement; never a subscriber or a count |
| `## The social plan` | one line: the written-side documents own what they set for this platform |
| `## Cadence` | how often, on which days and at what time the brand posts there |
| `## Tone on this platform` | how the brand's voice shifts there |
| `## Call to action` | what a viewer or listener is asked to do, in the brand's words |
| `## Hashtag sets` | named sets, each counted against the platform's hashtag keys, where it has any |
| `## Deliverables used` | the `<platform>.<format>` keys the brand uses there, from `python3 toolkit/media.py presets` |
| `## Overrides` | one line pointing to `brand/src/platforms/overrides.toml` |

- **One agreement per site:** a site or list the brand does not own needs its row's Agreement to
  name a dated record before any placement there is `ready`; where the project has both the
  website and the blog platforms, the website row holds it once and the blog row reads 'see
  website'. A slug is frozen once a schedule row uses it.

## The social-media family

- Where syntek-author's social-media family is present (a business project, by default), its
  documents own what they set, platform by platform and document by document: the social media
  plan, the content calendar or an operating procedure. A document **covers** a platform when it
  names the platform with a cadence; whichever sets cadence, tone, call to action or hashtags owns
  that value, and the calendar owns when each post goes out.
- The profile always holds its delivery facts (the account, sites or lists, the deliverables
  used), cites each such document in prose, and holds a value itself only where none sets it;
  `publishing/src/schedule.md` lists only media deliverables, each citing its calendar entry.
- Text-only posts, bios and the channel voice belong to the social-media-documents skill
  (syntek-author), where present. Standalone, or in a book project, the profile holds all of it.

## Overrides

- An override is a confirmed difference between `toolkit/data/platforms.toml` and what the
  platform says today: one `[[override]]` table in `brand/src/platforms/overrides.toml`, with the
  field's key (`<platform>.<format>.<field>`), the value, the platform's words, the source and
  the date checked. The toolkit applies it, and `media.py presets` prints it.
- Never edit `platforms.toml` itself: it is template-owned, and `copier update` refreshes it.
- A value not yet confirmed is cited by its key, never by a number; `prepare-post` warns above
  `platform.instagram.hashtags_max`, for example, without the profile stating it.
- Most overrides come from `publishing/workflows/07-refresh-the-platform-specs/`.

## How we apply it here

- A handle, domain, sender or URL comes from the author, exactly as written; never guessed.
- A profile is a seed: `copier update` never overwrites it, and restores it empty if it is
  deleted. Removing its platform from the answers deletes it, filled in or not; `overrides.toml`
  always ships, so a confirmed correction survives and is removed by hand.
- No platform number is written in a profile, a post or a guide.

## Who implements it

- **Workflow:** `brand/workflows/04-set-up-a-platform/`.
- **Skill:** `prepare-post` reads the profile for every deliverable on its platform, and the
  social-media-documents skill (syntek-author), where present, owns the written social plan.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 7 owns never fabricating a platform
rule or limit; `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 2 owns the `presets`
command that applies the overrides; `.claude/rules/syntek-media/02-skills.md` Section 4 owns what
the social-media-documents skill takes over. The rules own the requirements; this guide owns
what the brand records for each platform.

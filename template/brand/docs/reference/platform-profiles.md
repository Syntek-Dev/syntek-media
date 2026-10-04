---
type: guide
skills: [prepare-post]
model: opus
---

# Platform profiles — the brand's own choices for each platform, and its corrections

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A profile, `brand/src/platforms/<platform>.md`, holds what the brand decides for
one platform: the account, the deliverables it uses there and, where no social media plan covers
them, its cadence, tone, call to action and hashtag sets. One ships for each platform chosen when
the project was generated. The platform's own facts (sizes, lengths, limits, codecs, its AI
label) are not the brand's to decide: they live, dated and sourced, in
`toolkit/data/platforms.toml`, read as `publishing/docs/reference/platform-specs.md` explains.

## What a profile holds

| Section | Holds |
|---|---|
| `## Account` | the handle and URL, exactly as the platform shows them; flagged until the author gives them |
| `## The social plan` | one line: whether a social media plan owns cadence, tone, call to action, hashtags and bios |
| `## Cadence` | how often, on which days and at what time the brand posts there |
| `## Tone on this platform` | how the brand's voice shifts there |
| `## Call to action` | what a viewer or listener is asked to do, in the brand's words |
| `## Hashtag sets` | named sets, each counted against the platform's hashtag keys, where it has any |
| `## Deliverables used` | the `<platform>.<format>` keys the brand uses there, from `python3 toolkit/media.py presets` |
| `## Overrides` | one line pointing to `brand/src/platforms/overrides.toml` |

## The social-media family

- Where syntek-author's social-media family is present (a business project, by default), its
  social media plan owns cadence, tone, call to action, hashtags and bios, and its content
  calendar owns when each post goes out.
- The profile then holds only delivery facts, the account and the deliverables used, and cites
  the plan in prose for the rest; `publishing/src/schedule.md` lists only media deliverables, each
  citing its calendar entry; `prepare-post` reads that entry and packages media deliverables only.
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
- `publishing/workflows/07-refresh-the-platform-specs/` re-checks old values and is where most
  overrides come from.

## How we apply it here

- A handle or URL comes from the author, exactly as written; Claude never guesses one.
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

---
type: guide
skills: [prepare-post]
model: opus
---

# AI disclosure — each platform's rule for its label, the house's line for the words

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A piece that uses a synthetic voice (the brand owner's own cloned voice
included), AI-generated visuals or AI-generated music records it in its brief, in
`synthetic_voice`, `ai_visuals` and `music`, and every post of it discloses it. The platform's own
AI label is set exactly when that platform's current rule requires it, because a label a platform
does not ask for can mislead viewers about what is synthetic. A plain disclosure line goes in the
description on every platform, always, because the house is more open than any one platform asks.

## The house rule

1. **The label follows the platform.** Set it when, and only when, the platform's rule below
   covers the content, and record the rule the decision rests on.
2. **The description line is always there,** on every platform, whatever the label rule. It says
   what is synthetic (the voice, the visuals, the music) and, for a cloned voice, whose voice it is.
3. **A podcast discloses in the audio and in the metadata:** a spoken line in each episode, and a
   sentence in the episode description and in the show description.
4. **An unclear case is the author's call,** dated, with its reason; never a label 'to be safe'.

## Each platform's rule

| Platform | The label, and where it is set | When the platform requires it | Source (checked 03/10/2026) |
|---|---|---|---|
| YouTube | the altered or synthetic content question at upload in YouTube Studio ('AI use', under Attributes) | realistic content that AI meaningfully made or altered: a real person saying or doing what they did not, real events or places altered, realistic scenes that did not happen, AI music as the main focus. Exempt: cloning one's own voice for voiceovers or dubs; production help such as a script, title or thumbnail; captions | https://support.google.com/youtube/answer/14328491 <!-- scrub: allow — help-centre article number --> |
| TikTok | 'AI-generated content', under More options when posting | all AI-generated content with realistic images, audio or video; it also asks for a label on content significantly edited by AI. A label TikTok applies from Content Credentials cannot be removed | https://www.tiktok.com/support/faq_detail?id=7636670084747893268 <!-- scrub: allow — help-centre article number --> |
| Instagram and Facebook | 'AI info', when posting | photorealistic video or realistic-sounding audio digitally created or altered; Meta names a reel narrated with a realistic AI-generated voiceover, and AI-generated vocals. Not required for cartoon-style video or for still images, which Meta may label itself | https://www.meta.com/en-gb/help/artificial-intelligence/1783222608822690/ <!-- scrub: allow — help-centre article number --> |
| LinkedIn | no toggle documented: disclose in the post text | synthetic or manipulated media that depicts a person saying or doing something they did not, without clear disclosure; Content Credentials show an icon by themselves | https://www.linkedin.com/legal/professional-community-policies |
| Apple Podcasts | no toggle documented: disclose in the audio and in the metadata | guideline 1.11: audio or video generated with AI, synthetic voices included, disclosed prominently in the content and the metadata of each episode and of the show | https://podcasters.apple.com/support/content-and-subscription-guidelines |
| Spotify podcasts | no toggle documented | no disclosure rule found; Spotify removes shows that impersonate another creator's or host's likeness without permission, AI voice cloning included | https://newsroom.spotify.com/2026-05-19/podcast-verification-trust-creators-listeners/ |

## Cases the sources leave open

- **The owner's own cloned voice** is exempt on YouTube, but TikTok and Meta do not say: treat it
  as realistic synthetic audio and set their label, `VERIFY` at the next refresh.
- **A stock or designed voice on YouTube** that is not presented as a real person sits outside
  the help page's examples. That is a reading, not a quotation: the author decides, and the
  package records the decision.
- **LinkedIn and the owner's own script:** the policy targets words a person did not say; whether
  it reaches an owner's clone reading the owner's script is `VERIFY`. The description line covers
  it either way.
- **One podcast feed reaches Apple and Spotify,** so Apple's rule governs every episode.
- **Audiobooks** carry their stores' own rules, in the audiobook narration guide in
  `production/docs/reference/`, where the project makes audiobooks.

## Recording the decision

A post package's **Disclosure** bullet records, per deliverable, the label and its setting with the
rule (or the author's dated decision) it rests on, the description line, and any spoken or
on-screen line. The publish log's `Disclosure set` column records what the author actually set.

## How we apply it here

- Read the brief's three fields before writing a package; where all three are `none`, the package
  says no disclosure is needed.
- Generated audio never claims to be human narration, in a description, a credit or a caption.
- Labelling never cures a breach: TikTok removes some content even when labelled, such as public
  figures in false contexts or the likeness of a private person or a minor without permission
  (`production/docs/reference/rights-and-consent.md`).
- A rule that has changed goes into a same-named project guide on the author's word, never here.

## Who implements it

- **Workflow:** `publishing/workflows/05-prepare-a-post/` decides the label and writes the lines;
  `publishing/workflows/06-record-a-publication/` records what was set.
- **Skill:** `prepare-post` writes each deliverable's disclosure and checks it against this guide.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 5 owns the requirement (each
platform's rule for its label; a description line always), and Section 6 owns consent for a
cloned voice or a likeness. The rules own the requirement; this guide owns each platform's rule,
its source and the date it was checked.

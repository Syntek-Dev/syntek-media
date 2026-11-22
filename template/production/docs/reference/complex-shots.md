---
type: guide
skills: [storyboard, cut-for-platform]
model: opus
---

# Complex shots — made in an outside editor, brought back as footage

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** `assemble` makes a small set of shots well. A shot beyond that set is made in an
outside editor, exported as one video file and logged as footage, so the edit decision list uses
it as an ordinary clip and the toolkit stays the record of the master.

## What assemble makes, and what it does not

- **The toolkit's own:** footage cut frame-accurately, stills and cards held, colour clips, cuts,
  cross-fades and one slow push-in on a still (`production/docs/reference/edit-decision-lists.md`).
  A code-animated scene is the scene kit's (`production/docs/reference/scenes-as-code.md`).
- **A complex shot:** a moving or eased push-in or pan, parallax, a text build-up animated word by
  word or letter by letter, an animated lower third, a speed ramp, a composite of several layers,
  or a transition beyond a cross-fade. Never force one through `assemble`.

## The editors

- **DaVinci Resolve**, with Fusion for compositing: any complex shot.
- **EffectCraft**, ArtCraft's open-source motion-graphics and compositing app: keyframed
  transforms with sub-pixel sampling, text animators and templates (`VERIFY`). The closest fit
  for a push-in, a build-up or a lower third.
- **FilmCraft**, ArtCraft's open-source non-linear editor, for a short edited sequence (`VERIFY`).
- **AniCraft**, ArtCraft's open-source 2D vector animation app, for vector titles and reveals
  (`VERIFY`).
- The ArtCraft apps are alpha and change every few days (`VERIFY`, checked 22/11/2026): pin the
  version you use, and check each flag and setting against that version before relying on it.

## The round trip

1. The storyboard types the shot `edited`, its Source `to render`, and its Picture names the
   editor and the motion. The board sheet shows it as a labelled placeholder until it is logged.
2. The author makes the shot, or Claude does through an editor's own command line where the
   author has installed it, running only what the author agreed.
3. It is exported as one video file at the master's size and frame rate: ProRes 422 HQ, ProRes
   4444 where it needs alpha, or a high-bitrate H.264 where ProRes is not offered (`VERIFY` per
   editor). The toolkit makes every delivery encode from the master.
4. `python3 toolkit/media.py footage add FILE --kind video --location LABEL` logs it; fill its
   `notes` with the author: the editor, its version and the project file's label, never a path.
5. The shot's Source becomes that footage ID, and the edit decision list cuts it with `in` and
   `out` like any clip. A re-export is a new file, so a new footage ID; the old row stays.

## Project files, MCP and the editor's own AI

- The editor's project file stays outside the repository; the logged export is the evidence.
- The template offers no editor's MCP server. An owner who wants one adds it at user scope,
  confined to the project's folders where the editor supports read and write roots: EffectCraft
  and AniCraft do; FilmCraft's own server does not, so use only its bridge to a running app the
  owner watches (`VERIFY` every flag). Every change made that way ends in the same export and
  `footage add`.
- A picture the editor's AI makes is a `generated` shot under the brief's `ai_visuals`, with its
  rights row, and a person or a licensed item in an edited shot keeps its rights row.

## How we apply it here

- `to render` blocks the edit decision list exactly as `to shoot` does.
- The master's assembly and final encode, loudness, captions, the platform checks, the footage
  manifest, rights and credits never leave the toolkit.
- Log an export before an edit names it; never trim or re-encode a logged file.
- A claim about an outside app is `VERIFY` until it is checked against the installed version.

## Who implements it

- **Workflows:** `scripts/workflows/03-storyboard-a-piece/` types the shot;
  `production/workflows/01-log-source-media/` logs the export; and
  `production/workflows/03-assemble-the-master/` cuts it into the master.
- **Skills:** `storyboard` boards the shot; `cut-for-platform` writes it into the edit decision
  list and refuses it while it is still `to render`.

## Governing standard

`.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 owns what the toolkit renders and
what never leaves it, and `.claude/rules/syntek-media/03-production-ethics.md` Section 6 owns
rights and consent. This guide owns how a complex shot is made outside and brought back.

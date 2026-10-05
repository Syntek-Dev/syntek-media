# BUSINESS.md — voiceover, business mode

The domain for voicing a business's pieces: explainers, walk-throughs of a product or a service,
and the spoken frame around a recorded talk, in one brand voice that says the business's name and
its terms the same way every time.

## Paths and unit

- **Unit:** one piece. **Segment:** one spoken sentence, or one short beat read as one breath.
- **Procedure:** `production/workflows/02-make-a-voiceover/`.
- **Voiced lines:** the script's `VO:` lines. An `ON:` line is the speaker's own, on camera, and
  is never voiced, even to patch a fluffed take.
- **Register:** `production/src/voiceover/<piece>.toml`; takes in
  `production/src/voiceover/generated/<piece>/takes/` (git-ignored).
- **Joined voice:** `production/src/renders/<piece>/<piece>.voice.wav`, from `voice join`;
  a scene piece dates `M4.takes` after its used takes are approved and archived.
- **Narrator:** the `voiceover` row of `brand/src/voice/voice.md`.
- **Written voice:** syntek-author's brand voice, standards/brand/brand-voice.md, where present;
  the spoken style in `voice.md` follows it and never restates it.
- **Guides:** `production/docs/reference/voiceover.md` and
  `brand/docs/reference/the-spoken-voice.md`.

## Additions to the steps

- **Step 2 — also check the claims are settled.** A figure, a result or a customer's words in a
  `VO:` line is voiced only once the script's claims are verified (M2): a spoken claim is far
  harder to correct than a caption.
- **Step 3 — also keep one voice across a series.** A second narrator for one series of
  explainers is the author's decision, recorded as its own use in `voice.md`, never a trial that
  stuck.
- **Step 5 — also spell out what the listener hears.** The business's name, its product names and
  any abbreviation said as letters are substituted from `voice.md`; where a name has no row, ask
  the author how it is said before anything is sent, and add the row.
- **Step 9 — also play the hook and the call to action first.** They carry the piece; if either
  reads wrongly, the rest waits.

## Domain rules

- **A client's or a customer's name is voiced only with their recorded permission**, a `cleared`
  row in `production/src/rights-register.md` (`.claude/rules/syntek-media/03-production-ethics.md`
  Section 6).
- **Never voice a testimonial, an endorsement or a statistic the script does not source**
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 7).
- **The owner's own cloned voice is still synthetic**: the brief's `synthetic_voice` reads
  `own-clone`, and the disclosure follows `publishing/docs/reference/ai-disclosure.md`.
- **Figures are said as the script writes them for the ear**, never rounded or expanded by the
  voice; a figure that reads badly aloud goes back to the script (`write-script`).

## Examples

An invented register for Harbour Lane Studio, its first segment approved and archived:

```toml
[voiceover]
piece = "007-booking-a-studio-slot"
voice_use = "voiceover"
model_id = "eleven_v4"
output_format = "mp3_44100_128"
per_cue = false

[[segment]]
id = "s01"
script_lines = "1.1"
text = "Booking a slot at Harbour Lane takes under a minute."
request = "Booking a slot at Harbour Lane takes under a minute."
take = 2
file = "generated/007-booking-a-studio-slot/takes/007-booking-a-studio-slot.s01.t2.mp3"
characters = 52
pause_after = 0.4
status = "approved"
archived = "F0012"
```

Take 1 was rejected for a rushed 'Harbour Lane'; the old file stays in the piece's takes folder,
and only take 2 is archived.

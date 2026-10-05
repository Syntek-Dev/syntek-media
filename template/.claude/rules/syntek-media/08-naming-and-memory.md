# 08-naming-and-memory.md — what media things are called, and what goes in project memory

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

Names are how files find each other, so they follow one pattern each. Memory is how sessions find
what earlier sessions settled, so it has one home and a gate.

---

## 1. Naming conventions

Files and folders are kebab-case unless a pattern says otherwise; the examples illustrate a
pattern and are not files in this project.

| Pattern | Example | Used for |
|---|---|---|
| `NNN-kebab-title` | 003-why-the-ferry-runs-late | a piece: its folder, and the key every other file uses (frozen) |
| `<piece>/` | 003-why-the-ferry-runs-late/ | a piece's output folder inside `production/src/renders/`, `production/src/voiceover/generated/` and `publishing/src/renders/`, made by the toolkit: git-ignored, never holding a tracked file, with no pair and no README |
| `proofs/<what>-DD-MM-YYYY/` | proofs/brand-kit-05-10-2026/ | brand-kit proofs, which no piece owns, in `production/src/renders/` |
| `voice-trials/<name>/` | voice-trials/warm-narrator/ | voice trials, which no piece owns, in `production/src/voiceover/generated/`, made by `speak plan --trial <name>`: never a take, never in a register |
| `<platform>.<format>` / `<platform>-<format>` | youtube.short / youtube-short; linkedin.video_vertical / linkedin-video-vertical | a deliverable key of `toolkit/data/platforms.toml` / its form in a file name, where the dot and every underscore become hyphens, in a render, a thumbnail and a caption qualifier alike |
| `<piece>.master.mp4` (`.wav`) | 003-….master.mp4 | the master, in `production/src/renders/<piece>/` |
| `<piece>.<card>.html` / `<piece>.<card>.<W>x<H>[.transparent].png` | 003-….title.html / 003-….title.1920x1080.png | a card in `production/src/cards/` / its render in `production/src/renders/<piece>/cards/`, with `.transparent` for an overlay's, so a card used as a clip and as an overlay at one size keeps both renders |
| `<piece>[--cNN].<platform>-<format>[.burned].<ext>` | 003-…--c01.youtube-short.burned.mp4 | a deliverable, in `publishing/src/renders/<piece>/` |
| `<piece>[--cNN].md` / `.html` → `<html-stem>.<platform>-<format>.png` | 003-…--c02.youtube-short.png | a thumbnail brief and layout → its render, in `publishing/src/renders/<piece>/` |
| `<piece>[--cNN\|.<FID>][.<platform>-<format>].en-GB.srt` | 003-…--c01.youtube-short.en-GB.srt | captions timed to the master, a cut or a recording; a `.vtt` beside each |
| `<piece>.sNN.tN.mp3` (`.pcm`) | 003-….s04.t2.mp3 | a voiceover take, in `production/src/voiceover/generated/<piece>/takes/` |
| `<piece>.voice.wav` | 003-….voice.wav | the piece's approved takes joined in register order with their pauses, mono, by `voice join`, in `production/src/renders/<piece>/` |
| `<piece>.words.json` / `<piece>.words-check.md` | 003-….words.json | the joined voice's word timings / the check the author signs, tracked in `production/src/timing/` |
| `<piece>.mouth.json` | 003-….mouth.json | the joined voice's mouth shapes, tracked in `production/src/timing/`; `levels` writes `<piece>.levels.json` only as a working copy, in `production/src/renders/<piece>/timing/` |
| `<piece>.cues.json` / `<piece>.real.json` | 003-….cues.json | the piece's cue index / the index of the real sources its scene shows, tracked in `production/src/scenes/` |
| `<piece>.scene.py` / `<piece>/scene/index.html` | 003-….scene.py | a piece's scene as code, tracked in `production/src/scenes/` and run by its path / the page it writes, in `production/src/renders/` |
| `<piece>.bNN[.mid].<W>x<H>.png` / `<piece>.stills.json` | 003-….b02.mid.1080x1920.png | a board's first (or middle) frame, `bNN` its storyboard number in lower case / every box and flag of the piece's stills; both in `production/src/renders/<piece>/stills/` |
| `<sprite>-<pose>-mouth-<shape>` · `<sprite>-<pose>` with `<sprite>-mouth-<shape>` · `<sprite>-<pose>-blink` | host-point-mouth-d.svg | a character's whole frame · a mouthless pose and its mouth layer · its blink layer: design exports in `brand/src/exports/`, read by the scene kit's sprite slot; `<sprite>` and `<pose>` are kebab slugs, `<shape>` is `a`–`h` or `x` |
| `<piece>.chNN.pNN.txt` / `<piece>.chNN.pNN.tN.mp3` / `<piece>.chNN.mp3` | 012-….ch03.p02.t1.mp3 | an audiobook text chunk / its take / a mastered chapter |
| `<piece>.chNN.chunks.toml` | 012-….ch03.chunks.toml | a chapter's chunk sidecar, beside its chunks: each chunk in order and the pause after it |
| `<piece>.ch00.md` / `<piece>.ch99.md` | 012-….ch00.md | an audiobook's opening / closing credits, beside its chapter register (`ch00` and `ch99` are the credit rows) |
| `<piece>.sNN.scratch.wav` / `<piece>.chNN.pNN.scratch.wav` | 003-….s04.scratch.wav | an espeak-ng scratch track (approximate; never a take, never in a register): a voiceover's in `production/src/voiceover/generated/<piece>/`, never among its takes; a chapter's in its generated folder |
| `<stem>[.<in>-<out>].wav` | talk-cam-a.wav | audio extracted for speech-to-text or alignment: by default in `production/src/renders/<piece>/`, or at the folder's top for a stem with no piece key, such as a footage file's; `production/workflows/08-bring-in-a-recording/` passes `-o` into the recorded piece's folder |
| `<stem>.<platform>-<format>.<ext>` | 003-….blog-featured-image.avif | an image `media.py image` encoded or framed (`jpg`, `png`, `webp`, `avif`), in `publishing/src/renders/<piece>/` (a stem with no piece key, such as a show cover's export, at the folder's top); `<stem>` is the source's name up to its first `.` |
| `<piece>[--cNN].newsletter-preview-gif.gif` | 003-…--c03.newsletter-preview-gif.gif | a GIF preview, made by `cut` from its thumbnail brief, in `publishing/src/renders/<piece>/` |
| `<piece>[--cNN].transcript.en-GB.md` | 003-…--c01.transcript.en-GB.md | a published transcript of the whole piece or one cut, in `publishing/src/captions/` |
| `<show>` / `<show>.toml` / `<show>.feed.xml` | harbour-lane-talks.feed.xml | a podcast show's frozen slug / its register / its feed as last published, both tracked in the podcast folder of `publishing/src/`; the same `<show>.feed.xml` at the top of `publishing/src/renders/`, which no piece owns, is the upload copy |
| `<piece>.podcast-feed-audio.mp3` / `<piece>.chapters.json` | 003-….chapters.json | a feed episode's audio (encoded at M5, tagged at M7) / its JSON chapters, in `publishing/src/renders/<piece>/` |
| `<platform>:<slug>` | website:studio | a placement on the brand's own channels: the schedule's and the log's Platform cell, and a package H2's qualifier; a slug is frozen once a row uses it |
| `transcript.md` | — | a recorded piece's transcript, in its piece folder |
| `F0001` · `RR0001` · `cNN` · `sNN` · `chNN` · `pNN` | — | footage, rights, cut, segment, chapter and part IDs: permanent |
| `workflows/NN-verb-first-name/`, `workflows/local/NN-verb-first-name/` | 02-make-a-voiceover/ | a template procedure (numbers frozen) / the author's own |
| `kebab-case.md` in `docs/`; `SCREAMING-SNAKE-CASE.md` | writing-for-the-ear.md; STEPS.md | a guide, named for its question; structural files and sub-documents |

**Folders.** In an output folder, a name that begins with a piece's key lands in that piece's
folder: a take in its takes folder, a card PNG in its cards folder, the working copy of a timing
or scene file in its timing folder, a scene's page in its scene folder and its stills in its
stills folder, and anything else in `<piece>/` itself. A name with no piece key stays at the
folder's top, and the audiobook folder's generated and renders folders stay flat. A tracked file
never sits in a per-piece folder: it stays flat in its tracked folder under its `<piece>.` name.

Dates in filenames are DD-MM-YYYY. A name other files cite (a piece, a skill, a workflow number,
an ID, a show's slug) is never changed without a migration; a corrected episode file is published
under a new name (`-v2` before its extension) while its render name stays. No tracked media file ends in `.log`, `.out`, `.aux`,
`.toc`, `.tmp`, `.bak` or `.orig`: syntek-author's root ignore rules, where present, would hide it.

---

## 2. What goes in `MEMORY.md`, and what goes elsewhere

`.claude/MEMORY.md` holds what a later session needs and cannot read off the files, and project
state lives only there; write there, not to any global or automatic memory. Its headings are the
template's; where syntek-author's 00-project.md is present, its Memory headings map each one to
this project's heading, and media reads and writes under that heading.

| What you learned | Where it goes |
|---|---|
| A fact not visible in the files (release cadence, the next publish date) | `MEMORY.md` Facts |
| A decision that passed the gate; the author's feedback; where the work stands | `MEMORY.md` Decisions; Feedback; Status |
| A question only the author can settle; a risk to people or privacy | `MEMORY.md` Open questions; Sensitivities |
| A piece's status and gates | its brief: `status` and `verified` |
| A narrator, a voice or model ID, a pronunciation | `brand/src/voice/voice.md` |
| Credits spent; a right, a licence or a consent | `production/src/credits-log.md`; `production/src/rights-register.md` |
| A design and its Claude Design link | `brand/src/design-register.md` |
| A planned post; what was posted, with what disclosure | `publishing/src/schedule.md`; `publishing/src/publish-log.md` |
| A platform limit that has changed | an `[[override]]` in `brand/src/platforms/overrides.toml` |
| The brand's name, kind, platforms or media kinds | the Copier answers (`.claude/rules/syntek-media/06-global-rules.md` Section 11) |

---

## 3. The memory gate

Write to `MEMORY.md` only when all three hold:

1. **It will be needed again**: a later session would otherwise ask the author the same question.
2. **It cannot be read off the files**: if a `CONTEXT.md`, a brief or a register already says it,
   update that instead.
3. **Getting it wrong would cost real work**: a re-render, credits spent twice, a wrong claim in
   public, a missed date.

A **decision** must also pass the decision gate kept by the grill-with-docs skill (syntek-author),
where present, and kept here otherwise: it is hard to reverse, it would surprise someone without
the context, and it settled a genuine trade-off. Record only what the author has confirmed.

---

## 4. Entries: dated, and superseded, never deleted

- One bullet under the right heading:
  `- **DD/MM/YYYY** — **Headline.** Body, including why, and what was rejected.`
- Dates are absolute: 'next week' becomes a date before it is written down.
- **Supersede; never delete.** Append `*(Superseded DD/MM/YYYY — see below.)*` to the old bullet
  and add the new one. The history of a decision is part of the decision.
- Past 300 lines, split by topic into `.claude/memory/<topic>.md` and leave `MEMORY.md` as the
  index, unless the Overrides of syntek-author's 00-project.md, where present, keep it whole.

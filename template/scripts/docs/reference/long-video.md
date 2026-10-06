---
type: guide
skills: [write-script]
model: opus
---

# Long video — an explainer or a talk that holds attention to the end

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A long video is an explainer or a talk watched in landscape, usually with the
sound on, by someone who chose to spend minutes on it. It earns those minutes beat by beat: a
promise made at the start, kept in steps the viewer can follow, and a close that sends them
somewhere. It is either scripted and then filmed or voiced, or recorded first, as a talk is, and
shaped from its transcript.

## The shape of the piece

| Beat | Does |
|---|---|
| Hook | One line that names the problem or the question, before any welcome. |
| Promise | What the viewer will know or be able to do by the end. |
| Steps | One point per beat, in the order the viewer needs them; each opens by saying where it is going. |
| Recap | The steps again, in a sentence each. |
| Call to action | One thing to do next, said and shown. |

Record this order under the brief's `## Shape`; each beat is an H2 in the script with its target time, so `python3 toolkit/media.py script time`
can show which beat runs long.

## Keeping the picture moving

A face talking to camera for minutes loses viewers, however good the words. The storyboard
changes the picture at every beat and often within one: a cut to a screen, a still, a card that
names the step, a `TEXT:` cue for a figure or a term. A card or a still can carry a slow push-in;
anything more elaborate is beyond this template's toolkit for now.

## Scripted or recorded

- A **scripted** explainer is written first, approved, then filmed or voiced against the script.
- A **recorded** talk (`origin: recorded`) is not re-scripted: its transcript is made from the
  recording, its beats anchored at their start times, and the master is cut from it. A talk
  that ran long is shortened in the edit decision list, never by rewriting what was said.

## Lines that stand alone

A long video is the parent of most shorts. While writing, mark in `NOTE:` cues the lines that
would make sense to a stranger with no context: a claim, a story, a turn of phrase. The cut-down
plan starts from them, and a line that needs the previous minute to be understood is a poor
cut-down however good it is.

## How we apply it here

A scene explainer animates the author's art as `ai_visuals: assisted`, with native masters per aspect.

- The promise is kept in the same piece; a long video that ends on 'more next time' has not.
- Every figure and quotation is checked before approval, or cut.
- Chapters, descriptions and timestamps belong to the post package, not the script.

## Who implements it

- **Workflow:** `scripts/workflows/02-write-a-script/` writes, times and approves the script.
- **Skills:** `write-script` writes the script; a recorded talk's transcript comes through the
  production layer's procedure for bringing in a recording.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 makes M2 (briefed → scripted)
binding, and Section 7 forbids a fabricated figure or quotation. The rules own the requirements;
this guide owns how a long video is shaped to be watched to the end.

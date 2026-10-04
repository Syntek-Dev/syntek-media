# 05-model-allocation.md — which model does which media work

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

The two model tiers for media work are defined here and nowhere else in syntek-media. Every other
media file names a tier, never a rule of its own, so a change of policy is one edit. Where
syntek-author is applied, its own table governs writing work; both name the tiers the same way.

---

## 1. The two tiers

No Haiku on this project.

| Work | Model |
|---|---|
| Mechanical only: renders and encodes, probes, file moves and renames, `take add` and `footage add`, register and log rows already agreed, checklist ticks | **<%MODEL_MECHANICAL%>** |
| Everything substantive: anything a viewer or listener will read or hear (scripts, transcripts, caption text, titles, descriptions, thumbnail words, voice direction), edit decisions, rights and disclosure judgements, grilling, reviewing, any decision about meaning | **opus** |

If Opus usage is exhausted, substantive work falls back to **sonnet** until it returns, never
lower. **When in doubt, the work is substantive.** A caption break that changes what a line seems
to say, or a cut that drops a qualification, is a judgement, not a chore.

---

## 2. How the tiers are named in files

- **Checklist tags** are the literal `· _opus_` (the substantive tier) and `· _sonnet_` (the
  mechanical tier). They name the tier, not a model: the mechanical tier runs on the model in the
  table above.
- **Routing frontmatter** on guides, `STEPS.md` and `CHECKLIST.md` carries `model: opus` for
  substantive work and `model: sonnet` for mechanical work. As with the tags, `sonnet` there names
  the mechanical tier, which this project runs on **<%MODEL_MECHANICAL%>**.
- **Briefs, scripts, transcripts and registers carry no `model:` key.** The tier belongs to the
  task, not to the file being worked on.
- **Never write a version string.** Use the alias, `opus` or `sonnet`, so the project follows the
  current model without an edit.
- **Never put a template token inside an emphasised checklist tag.** A formatter that rewrites
  emphasis can corrupt it.

---

## 3. Why

Substantive work is where an error costs the author: a fabricated figure on screen, a flattened
argument in a clip, a voice directed out of character, a disclosure missed. The cheaper tier is
safe only where the result can be checked at a glance, which is why the line sits at mechanical
work and never higher, and why the fallback never drops below the tier the work needs.

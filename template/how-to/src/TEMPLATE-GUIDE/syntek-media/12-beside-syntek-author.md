# Beside syntek-author — sharing the project with syntek-author

syntek-media is built to share a project with syntek-author, the template for written work, and most projects that carry it carry both.
Each template keeps its own files, the two share some files byte for byte, and each is updated on its own.
This chapter explains how the two live together, and how to keep both in step.

## What each template keeps

- Each template records its answers in its own file: this one's is `.copier-answers.syntek-media.yml`, and syntek-author's is `.copier-answers.syntek-author.yml`.
- Media keeps its rules in `.claude/rules/syntek-media/`, beside syntek-author's rules folder, and both sets load at launch.
- Media ships its own bridge for the other coding agents, `.claude/syntek-media-agents.md`, beside syntek-author's.
- Media's skills, layers and workflows have names of their own, and none of them collides with syntek-author's.
- syntek-author's project settings file, 00-project.md, outranks media's rules, as it outranks syntek-author's own.
- Claude reads that file at run time, so its Paths, Memory headings, Workflow aliases and Overrides apply to media work too.
- No template ever updates `.claude/CLAUDE.md`, which stays yours.

## Who wrote the shared files

- Some files belong to the project as a whole: `README.md`, `CONTEXT.md`, `.gitignore`, `.mcp.json`, the shared files in `.claude/` and the coding agents' files.
- Whichever template was applied first wrote them, and the second template's copy printed each as 'conflict' then 'skip', or as 'identical'.
- So in a project where syntek-author came first, those files are syntek-author's, and they may not mention media at all.
- For media's layers, skills and rules, `.claude/rules/syntek-media/01-layout-and-routing.md` is the authority, whatever the shared files say.
- The family-shared files are the same in both templates, byte for byte, so the project holds one copy of each.
- They are the working-practice skills, the session hooks, the manual of `handoffs/`, the coding agents' settings files and the shared files of the guide.
- Each template's update refreshes the skills, the hooks, the manual of `handoffs/` and the guide's shared files from its own record, and only while you have not changed them.
- An update never refreshes the coding agents' settings files: it only offers their MCP servers, once each.
- A shared file holding the other template's newer version waits for that template's own update, and is never put back to an older one.
- A shared file you have edited is kept as it is, and the update's report says so.
- Media's mode files beside a shared skill are named for media and the brand kind, so they never meet syntek-author's.
- Where media came first, its shared files leave out what syntek-author needs, and you add those entries by hand.
- The template's own README lists them under 'Living beside syntek-author', at the source `_src_path` records in `.copier-answers.syntek-media.yml`.
- `.claude/MEMORY.md` is one file for both templates, written by whichever came first.
- Where syntek-author's project settings file maps the memory headings to names of your own, media reads them under those names.
- The handoff skill and its two session hooks ship with both templates, byte for byte, so the project holds one copy of each.
- A session hands off instead of compacting, and the handoff goes in the folder the Paths of syntek-author's project settings file give.
- In a project without syntek-author, it goes in `handoffs/`.

## Applying the second template

- Apply syntek-author first where you can, and then media, from a clean, committed branch.
- The other order works too, but whichever template comes first writes the shared files, and media's leave out what syntek-author needs.
- Never pass `--overwrite` to either copy: the second copy leaves every shared file as it stands.
- Media's first copy takes the data root, the coding agents and their models from syntek-author's recorded answers as its defaults, so the two agree from the start.
- `how-to/src/TEMPLATE-GUIDE/syntek-media/03-applying-over-syntek-author.md` walks the copy, and `how-to/workflows/syntek-media/01-finish-a-copy/` finishes it.

## Two routers

- `run-media-workflow` routes media work: video, audio, captions, thumbnails and posting.
- syntek-author's router routes writing work, and never sees media's layers.
- Neither router runs the other template's work, and neither routes the other template's procedures in the guide.
- `run-media-workflow` never routes media's own procedures in the guide either: a session runs one as `how-to/workflows/syntek-media/` says, step by step with its checklist open.
- syntek-author's writing skills are companions to media, named in the form 'the spelling skill (syntek-author), where present'.
- Media runs them on scripts, transcripts and post copy as reports, and applies a fix only when you accept it.
- In a business project, syntek-author's social-media documents own the written social plan, and media's profiles, schedule and posts cite them.

## syntek-author's lint

- syntek-author's `make lint` and `make flags` read media's `src/` Markdown as well as its own.
- That is why media's pieces, registers and plans are written one sentence per line.
- The rule applies to a paragraph you are already editing: never reflow a whole file to meet it.
- Neither check reads `how-to/src/` unless you name it, as in `make lint SCOPE=how-to/src`.
- Media's chapters are written so that such a run reports nothing in them.

## Updating both

- Update one template at a time, syntek-author first, and commit between them.
- Copier refuses to update a project with uncommitted changes, so each update starts from a clean, committed tree.
- Media's update, with its full command and its report, is in `how-to/workflows/syntek-media/04-update-the-template/`.
- syntek-author's update follows its own procedure, in its own folder of the guide's procedures.
- Never run one template's command against the other's answers file.
- Never follow one template's steps to update the other.
- The two MCP servers are added to an existing project once, by whichever template's update runs first.
- The data-root answers must agree in both answers files, as `how-to/src/TEMPLATE-GUIDE/the-data-root.md` explains.
- The coding agents and their models should match too, as `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` explains.

## The guide with two templates

- syntek-author's own guide sits in folders named for it, beside media's folders named `syntek-media/`, and the shared chapters sit outside both.
- Each template's update puts back its own guide files and the shared ones wherever they differ, and never touches the other template's folders.
- The guide is read-only in every template's folders alike: read it, and never edit it.
- Only a template's update, its recovery and the commands its report prints change a file there.
- To work differently from media's guide, record the difference in syntek-author's project settings file, 00-project.md, under Overrides or Workflow aliases.
- `how-to/src/TEMPLATE-GUIDE/syntek-media/10-customising.md` explains how.

## The version you need

- A project that carries media's guide needs syntek-author v0.6.0 or later.
- Update syntek-author to it before you take this template's release that adds its guide, and update it before media from then on.
- An older syntek-author treats every `src/` folder as your work, so its checks would read the guide's chapters as if they were your text.
- It also puts nothing back in `how-to/`, so a change made there would stand until a newer update.
- Media's copy warns where syntek-author's answers file stands without syntek-author's guide, because that means its release is too old.

## Where the rules live

- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 10: syntek-author's project settings file, precedence, and living beside syntek-author.
- `.claude/rules/syntek-media/02-skills.md` Section 4: the family-shared skills and the companions from syntek-author.
- `.claude/rules/syntek-media/06-global-rules.md` Section 5: one sentence per line, and syntek-author's lint.
- `.claude/syntek-media-agents.md`: how the other coding agents read every template's rules and bridge, and which outranks which.
- `how-to/workflows/syntek-media/04-update-the-template/`: every step and command for updating this template.

## Next

- Updating this template, step by step → `how-to/workflows/syntek-media/04-update-the-template/`
- What an update does, and how it treats another template's files → `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`
- When something goes wrong → `how-to/src/TEMPLATE-GUIDE/syntek-media/13-troubleshooting.md`

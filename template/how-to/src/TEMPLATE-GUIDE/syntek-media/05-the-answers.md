# The answers — every answer the template keeps, and changing one later

When syntek-media was applied, Copier asked a series of questions, and your answers decided what it wrote.
This chapter explains each answer in plain words, what it changes in the project, and how to change one later.
The questions themselves, with their help text, are in the template's `copier.yml` at its source, which the `_src_path` line of your answers file names.

## Where the answers live

Your answers are recorded in `.copier-answers.syntek-media.yml`, the answers file at the top of the project.
Copier wrote it, and every later update reads it to know how the project was made.
Never edit it by hand: a hand edit and the files rendered from the old answer drift apart without warning.
An answer changes only through an update that is given the new answer, which renders the template's files again with it.
`how-to/workflows/syntek-media/02-change-the-answers/` gives every step of that, from the first commit to the last.
The brand section of `.claude/rules/syntek-media/01-layout-and-routing.md` is rendered from these answers, so a changed answer reaches it on its own.

## The brand

These answers say who the brand is and who it speaks to.

- `BRAND_NAME` is the brand's name exactly as a viewer meets it: on screen, in captions, in credits and in the metadata the toolkit writes.
- Every skill's title carries it, so write it in the one form you always use, without double quotation marks or backslashes.
- `BRAND_SLUG` is the brand's machine name, in lower-case words joined by hyphens, made from the name by default.
- `BRAND_DESCRIPTION` is the brief: what the channel is for and for whom, in at least one full sentence.
- Every skill reads it before anything else, so write it as a brief, never as a tagline.
- `AUDIENCE_TEST` names the one viewer or listener every piece must work for, in a real moment, such as someone watching on a phone with the sound off.
- Every script is written for that person, and the comprehension skill (syntek-author), where present, reads as them.
- `OWNER_NAME` is the person or business who keeps the project, exactly as written: it is 'Maintained By' in every metadata header.
- It defaults to the brand's name, which suits a business, or an author whose pen name is the brand.
- `OWNER_FIRST_NAME` is what the skills call you in chat, and defaults to the first word of the owner's name.
- Change it where that first word is a business name, an initial or a title.

## The brand kind never changes

`BRAND_KIND` says what kind of brand this is: `business`, `author-fiction` or `author-nonfiction`.
It has no default, on purpose, so a copy never chooses one for you.
It decides the mode file that sits beside each skill with one, the worked example and the brand seeds.
In this project that is `BUSINESS.md`, `FICTION.md` or `NONFICTION.md` beside a media skill, and the file of the same name with a `MEDIA-` prefix beside a shared one.
`how-to/src/TEMPLATE-GUIDE/syntek-media/08-skills-and-the-router.md` explains what a mode file does.
An update that is given a different brand kind stops before it touches a single file.
A different brand kind is a new project: make one, and copy your work across.

## Platforms and media kinds

`PLATFORMS` names where the brand publishes, and `MEDIA_KINDS` names what it makes.
Each is a list, so you may choose several values, and each value adds its own files.
A platform adds its profile in `brand/src/platforms/`, which you fill in, and its guide in `publishing/docs/reference/`.
A media kind adds its guide in `scripts/docs/reference/`, and the podcast and audiobook kinds add their workflows too.
Each brand kind starts from its own sensible list, which you can change when you answer.
A list is always given whole, and the new list replaces the old one.
So `--data 'PLATFORMS=[youtube, podcast]'` keeps the platforms it names and removes every other.
Removing a value on an update deletes every file it generated, profiles you have filled in included.
`how-to/src/TEMPLATE-GUIDE/syntek-media/11-platforms-and-media-kinds.md` says what each removal deletes, and how to keep what you need.

## The example, the model, the time zone and the date

`SEED_EXAMPLES` decides whether a copy writes one worked example to learn from: a short piece carried from its brief to its post package.
It is written once, by the copy, and the worked example, where it was kept, is yours to delete when you are done.
Once deleted it stays deleted, and no update writes it again.
Answer it off when you apply the template to a project already in use.
`MODEL_MECHANICAL` names the model for mechanical work only, such as renders, encodes, file moves and checklist ticks.
It is `opus` or `sonnet`, and defaults to `opus` for a business and `sonnet` otherwise.
Anything a viewer or listener will read or hear always uses Opus, whatever you answer.
`TIMEZONE` is your time zone, as a name such as Europe/London.
The skills use it for the dates in filenames and headers and for the times in the posting schedule.
`DATE` is the date in every metadata header, written DD/MM/YYYY.
It is answered once and kept, so an update never changes the headers across the project.

## The family's questions

The questions about coding agents and about the data root are shared by every template of the family, word for word.
So a project that carries syntek-author as well answers them the same way in each.
Each default reads this project's own record first, then syntek-author's record, where it stands.
So a copy over a syntek-author project takes its coding agents, their models and its data-root answers, and writes no client file it left out.
`AGENT_CLIENTS` names the coding agents you use besides Claude Code, and the model answers after it name each one's model.
`how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` explains the clients, their files and their models.
Ticking a client on an update records it and adds its row to the model table, but writes none of its files.
`how-to/workflows/syntek-media/06-enable-a-coding-agent-client/` then adds its files.
`DATA_STORE` and the answers after it say where binary files are kept, and with what layout.
`how-to/src/TEMPLATE-GUIDE/the-data-root.md` explains the data root, and `how-to/src/TEMPLATE-GUIDE/syntek-media/07-a-tour-of-the-project.md` says what it means for media.

## Answering without prompts

Copier normally asks each question in turn, but a command can give the answers instead.
`--data` gives one answer, written `KEY=value`, and can be repeated for each answer you give.
`--defaults` accepts the default of every question that has one, and on an update it keeps every answer already recorded.
`BRAND_KIND` has no default, so a copy given `--defaults` alone stops with an error that names it, rather than quietly choosing a kind.
In a script, give `--defaults` with every update, so that a question new to the project takes its default instead of waiting for you.
Run the update by hand when you are unsure, so that you see each question and its help.

## Changing an answer later

Run the change the way `how-to/workflows/syntek-media/02-change-the-answers/` says: on a branch, with everything committed first.
This example changes the audience test; put your own question and answer after `--data`:

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx --python '>=3.14' copier update --trust -a .copier-answers.syntek-media.yml --data AUDIENCE_TEST='A reader who has never heard of the book, scrolling with the sound off.'
```

The five settings in front turn Git's background housekeeping off for that one run, so the update does not stop part way.
`-a` names the answers file, which Copier finds only when you name it.
The update records the new answer, and the brand section of the media rules follows it.
Some files quote your answers but are never rewritten, because a copy writes them once.
In a project made by syntek-media alone, edit by hand `README.md`, `CONTEXT.md` and the 'Project' section of `.claude/CLAUDE.md` to match.
Over syntek-author those files are syntek-author's, so leave them to it.
After a platform is removed, also delete its rows in `brand/src/platforms/overrides.toml` by hand.

## Where the rules live

- `.claude/rules/syntek-media/06-global-rules.md` Section 11: answers change through Copier, and what a removal deletes.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1: the brand brief, rendered from your answers.
- `.claude/rules/syntek-media/05-model-allocation.md` Section 4: the models of the other coding agents, where the project uses one.
- `how-to/docs/syntek-media/changing-the-answers.md`: why an answer changes only through an update.
- `how-to/workflows/syntek-media/02-change-the-answers/`: the change, with every command.

## Next

- Changing an answer, step by step → `how-to/workflows/syntek-media/02-change-the-answers/`
- Adding or removing a platform or a media kind → `how-to/src/TEMPLATE-GUIDE/syntek-media/11-platforms-and-media-kinds.md`
- The coding agents and their models → `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md`
- Keeping binary files outside the repository → `how-to/src/TEMPLATE-GUIDE/the-data-root.md`

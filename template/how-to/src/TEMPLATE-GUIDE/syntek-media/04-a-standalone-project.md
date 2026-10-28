# A standalone project — a project made by syntek-media alone

syntek-media can also make a project on its own, in a new, empty folder, with no syntek-author beside it.
This chapter gives the copy command, says what the copy writes, and explains what a project without syntek-author lacks.

## A copy into an empty folder

Run the copy from the folder that will hold the new project, with the template's source in place of SOURCE and the new folder's name at the end:

```bash
uvx --python '>=3.14' copier copy --trust SOURCE my-channel
```

The source is the template's address, which its README gives, and which the `_src_path` line of `.copier-answers.syntek-media.yml` records in every project made from it.
To copy from a local clone of the template instead, give the clone's absolute path and add `--vcs-ref=HEAD`, so that Copier renders the checkout you have:

```bash
uvx --python '>=3.14' copier copy --trust --vcs-ref=HEAD "$(realpath ../syntek-media)" my-channel
```

Never give a relative path: Copier records the source in the answers file, and every later update would fail.
A project made from `HEAD` is updated with `--vcs-ref=HEAD` too, until a newer release of the template exists.
Copier asks each question in turn, and `BRAND_KIND` has no default, so that a brand kind is always chosen on purpose.

## What the copy writes

- Every media folder, rule, skill, workflow and guide the answers call for.
- The shared files, such as `README.md`, `CONTEXT.md`, `.claude/CLAUDE.md` and `.claude/settings.json`, from media's own copies.
- The family-shared files, such as the working-practice skills, the session hooks and the guide's shared files, in syntek-author's bytes, the same in every template of the family.
- The coding agents' files: a fresh copy ticks all four clients by default, and you can untick any you will not use.
- The data-root answers: a fresh copy records `DATA_STORE` as external by default, so that binary files would live outside the repository.

syntek-media itself files nothing under a data root, whatever `DATA_STORE` records.
After writing the files, the copy runs its tasks.
It makes the folder a Git repository, makes the session hooks executable, and sets a Git LFS safeguard, so that a large design export cannot be committed whole by mistake.
Its last task records the version just copied, on Python 3.14 or later, as `how-to/src/TEMPLATE-GUIDE/syntek-media/03-applying-over-syntek-author.md` explains.
A `MissingFileWarning` about `.copier-answers.syntek-media.yml`, and another about syntek-author's answers file, are both expected and harmless.
Copier commits nothing for you: `how-to/workflows/syntek-media/01-finish-a-copy/` takes a fresh copy to its first commit.

## Without syntek-author

A standalone project works, with less.
The writing companions are absent, so a skill that would use one names it, such as the spelling skill (syntek-author), where present, and carries on without it.
There is no writing router, and no project settings file to change how the rules apply.
Your own project rules go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.
The working-practice skills still ship, such as `handoff`, `grilling` and `grill-with-docs`, with the session hooks and the `handoffs/` folder.
They are byte for byte the ones syntek-author ships, so nothing changes when it arrives.

## Adding syntek-author later

syntek-author can be applied to a standalone project afterwards, with its own copy command, from its own source.
The shared files are already here, so its copy skips them, and its answers take this template's recorded ones where the two share a question.
`how-to/src/TEMPLATE-GUIDE/syntek-media/12-beside-syntek-author.md` explains what changes when it arrives, and which template updates first.

## Where the rules live

- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 8: who owns which files, and which are written only once.
- `.claude/rules/syntek-media/02-skills.md` Section 4: the family-shared skills, and the companions from syntek-author.
- `how-to/workflows/syntek-media/01-finish-a-copy/`: every step from a fresh copy to its first commit.

## Next

- Finding your way round the folders → `how-to/src/TEMPLATE-GUIDE/syntek-media/07-a-tour-of-the-project.md`
- Taking a first piece from a brief to a publication → `how-to/src/TEMPLATE-GUIDE/syntek-media/09-your-first-piece.md`
- Adding syntek-author beside it later → `how-to/src/TEMPLATE-GUIDE/syntek-media/12-beside-syntek-author.md`

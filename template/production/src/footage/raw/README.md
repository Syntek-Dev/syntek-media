# Local mirror of source media

This folder holds this machine's copies of the files listed in `production/src/footage/manifest.toml`, at the paths the manifest gives.
`python3 toolkit/media.py footage add` copies a file here and never moves the original; `footage verify` checks every copy against its checksum.
Everything here except this file is ignored by `production/src/.gitignore`: the master copy of each file lives in external storage, at its row's `location`, and never in Git.
Where the project keeps its files on a data root, the resolver's `add` also files a copy there, and `footage verify` warns of a file not yet filed.
Never edit, trim or re-encode a file here, because a changed byte fails `footage verify`.

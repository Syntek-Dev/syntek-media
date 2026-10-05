# Generated voiceover

Each piece's takes land in `<piece>/takes/`, one ElevenLabs call at a time, and `python3 toolkit/media.py take add` renames each at once to `<piece>.sNN.tN.mp3` (`.pcm` for a raw format) and logs it in the piece's segment register and the credits log.
That folder is the call's absolute `output_directory`, and `python3 toolkit/media.py speak plan <piece>` makes it before the first call: the server refuses a folder whose parent is missing, so nobody makes it with `mkdir`.
A piece's espeak-ng scratch tracks, `<piece>.sNN.scratch.wav`, sit in `<piece>/` itself, never among its takes: approximate, never a take, never entered in a register.
Voice trials, which no piece owns, go to `voice-trials/<name>/`, made by `python3 toolkit/media.py speak plan --trial <name>` before the first call; a trial is never a take, keeps the server's name, enters no register and takes its credits-log row with `—` for the piece.
A take an earlier release left at this folder's top stays where it is: its register row's `file` names that path, and every reader opens the path the row names.
Everything here except this file is ignored by `production/src/.gitignore`, every folder inside it included; never force a take into Git, and never put a tracked file in a folder here.
A folder inside this one carries no README and no pair.
A take cannot be made again: regenerating spends credits and gives a different take.
Archive every approved take with `python3 toolkit/media.py footage add FILE --kind generated --location LABEL` before a master depends on it, and record its footage ID in the register's `archived`.

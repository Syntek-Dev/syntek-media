# Masters, cards and working copies

Each piece's renders land in a folder named for it, `<piece>/`, which the toolkit makes when it first writes there.
The master from `python3 toolkit/media.py assemble` sits in it as `<piece>.master.mp4`, or `<piece>.master.wav` for an audio master, beside the piece's joined voice, `<piece>.voice.wav`, and any audio extracted from the piece's own files.
`<piece>/cards/` holds the card PNGs `assemble` renders before compositing, as `<piece>.<card>.<W>x<H>.png`, and `<piece>.<card>.<W>x<H>.transparent.png` for a card laid over the picture.
`<piece>/timing/` holds the working copy of every timing and scene file a toolkit command writes, before `-o` writes the tracked one in `production/src/timing/` or `production/src/scenes/`; a scene piece's page and its stills sit in `<piece>/scene/` and `<piece>/stills/`.
At this folder's top sits only what no piece owns: audio extracted from a file whose name carries no piece key, such as a footage file's, and brand-kit proofs, each set in `proofs/<what>-DD-MM-YYYY/`.
A master or card render an earlier release left at this folder's top stays where it is, ignored, until you delete it; the toolkit makes each again in the piece's folder when it needs one.
Everything here except this file is ignored by `production/src/.gitignore`, a piece's folder and everything in it included: a render is regenerable from the tracked edit decision list, cards, footage manifest, voiceover register and timing files, so never force one into Git, and never put a tracked file in a folder here.
A folder inside this one carries no README and no pair.
Never hand-edit a render; change what it is made from and render again.

# Masters and cards

Masters land here from `python3 toolkit/media.py assemble`, as `<piece>.master.mp4`, or `<piece>.master.wav` for an audio master.
So do the card PNGs it renders before compositing, as `<piece>.<card>.<W>x<H>.png`.
Everything here except this file is ignored by `production/src/.gitignore`: a render is regenerable from the tracked edit decision list, cards, footage manifest and voiceover register, so never force one into Git.
Never hand-edit a render; change what it is made from and assemble again.

# Rendered deliverables

The toolkit writes every publishing render here: each platform deliverable as
`<piece>[--cNN].<platform>-<format>[.burned].<ext>`, and each thumbnail or cover as
`<html-stem>.<platform>-<format>.png`. Everything in this folder except this file is ignored by
`publishing/src/.gitignore`, and all of it is regenerable from the master, the captions and the
thumbnail layouts. Never edit a render by hand, and never force one into Git.

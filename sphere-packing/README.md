# Stacking Balls, from Zero

A visual guide to the sphere packing linear program and to the 2026 result that
determined its exact strength, written for a reader with no mathematical
background.

- **[Read it on one page](ARTICLE.md)**, or on the web at
  [muchmirul.github.io/conjectures/sphere-packing/](https://muchmirul.github.io/conjectures/sphere-packing/)
- **[Read it chapter by chapter](guide/00-start-here/README.md)**, thirteen
  chapters of about five minutes each

## What it covers

How densely equal balls can fill space; why high dimensions are strange; the
Cohn-Elkies certificate method and why counting the same total twice proves
anything at all; and then the two halves of the 2026 theorem, which show that no
certificate can beat a certain rate and that one certificate reaches it. The
result replaces the general packing exponent that had stood since 1978.

The source is chapter 1 of *Ten Advances in Mathematics and Theoretical
Computer Science* (OpenAI). It is kept with its reasoning walkthrough in
`docs/ten-proofs/01-sphere-packing-linear-program/`.

## Running the code

```bash
make venv        # create the shared ../.venv and install this package
make test        # re-verify every number the guide quotes
make figures     # re-render every figure into guide/
make guide       # rebuild the chapter READMEs from ARTICLE.md
make play        # rebuild the playable pages in ../docs/sphere-packing/play/
make docs        # rebuild ../docs/sphere-packing/index.html from ARTICLE.md
```

## Play with it

Every chapter has a page where the numbers in it are controls you can move:
[docs/sphere-packing/play/](../docs/sphere-packing/play/index.html). Turn the
stack by dragging it, break a certificate by moving a slider, push the radius
into the wall and watch the demand become impossible. The pages carry no
libraries and make no network requests, so they work offline and straight from
a file. Their arithmetic is checked against the Python library in
`tests/test_interactive.py`, so the two cannot drift apart.

## Layout

```
ARTICLE.md  the whole guide on one page, and the single source for the prose
guide/NN-slug/README.md   one chapter per folder, generated, figures alongside
src/sphere_packing_guide/ core.py (ball volumes, certificates, the Mellin
                          ingredients), examples.py (the named numbers),
                          plotting.py (palette, GIFs, rotating 3D camera)
  viz/            one figure script per chapter
tests/      re-checks every computed number in the guide
notes/      research notes: every claim, marked computed, classical or recent
build_docs.py        turns ARTICLE.md into ../docs/sphere-packing/index.html
build_guide.py       turns ARTICLE.md into the chapter READMEs
build_interactive.py writes the playable page for each chapter
```

## What this repository proves, and what it only describes

The tests recompute the known densities, the ball volumes, the certificate
machinery, and each ingredient of the 2026 argument that can be evaluated
directly. They also re-check the certificates found here against both sign
rules on a grid far finer than the search used.

They do not prove the theorem. The main argument is described in words and
pictures and is not implemented. `notes/research-content.md` marks every claim
in the article as computed here, quoted from the literature, or part of the 2026
result.

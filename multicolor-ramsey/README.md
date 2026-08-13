# The Triangle Game, from Zero

A visual guide to the multicolor Ramsey problem for triangles and to the 2026
result that settled its growth rate, written for a reader with no mathematical
background.

- **[Read it on one page](ARTICLE.md)**, or on the web at
  [muchmirul.github.io/conjectures/multicolor-ramsey/](https://muchmirul.github.io/conjectures/multicolor-ramsey/)
- **[Read it chapter by chapter](guide/00-start-here/README.md)**, thirteen
  chapters of about five minutes each

## What it covers

The guide starts with the game of coloring every connection in a group so
that no three people are joined in a single color, and gives the exact small
answers and the point where they stop. It then states the question Erdős put
money on, which is whether the safe group size per color climbs forever, and
explains why products and shortcuts could never answer it. The last chapters
cover the three moving parts of the 2026 construction, which are palettes,
teams and a fixed saturated table, and show how they make the rate climb like
the cube root of the color count.

The source is chapter 9 of *Ten Advances in Mathematics and Theoretical
Computer Science* (OpenAI). It is kept with its reasoning walkthrough in
`docs/ten-proofs/09-multicolor-ramsey/`.

## Running the code

```bash
make venv        # create the shared ../.venv and install this package
make test        # re-verify every number the guide quotes
make figures     # re-render every figure into guide/
make guide       # rebuild the chapter READMEs from ARTICLE.md
make play        # rebuild the playable pages in ../docs/multicolor-ramsey/play/
make docs        # rebuild ../docs/multicolor-ramsey/index.html from ARTICLE.md
```

## Play with it

Every chapter has a page where the numbers in it are controls you can move:
[docs/multicolor-ramsey/play/](../docs/multicolor-ramsey/play/index.html).
Click strings to recolor the pentagon, try in vain to keep six people safe,
interrogate the referee's card column by column, and find the crossover
where the 2026 bound overtakes the old recipes. The pages carry no libraries
and make no network requests, so they work offline and straight from a file.
Their arithmetic is checked against the Python library in
`tests/test_interactive.py`, so the two cannot drift apart.

## Layout

```
ARTICLE.md  the whole guide on one page, and the single source for the prose
guide/NN-slug/README.md   one chapter per folder, generated, figures alongside
src/ramsey_guide/  core.py (colorings, the triangle check, the saturated
                   matrix, the answer maps, the staircases), examples.py (the
                   named numbers), plotting.py (palette, graph drawing, GIFs)
  viz/            one figure script per chapter
tests/      re-checks every computed number in the guide
notes/      research notes: every claim, marked computed, classical or recent
build_docs.py        turns ARTICLE.md into ../docs/multicolor-ramsey/index.html
build_guide.py       turns ARTICLE.md into the chapter READMEs
build_interactive.py writes the playable page for each chapter
```

## What this repository proves, and what it only describes

The tests rebuild the pentagon and the sixteen-person coloring and re-check
every triangle. They also sweep all 32768 two-colorings of six people, verify
two product colorings cold, find the saturated matrix at alphabet size two and
verify its promise over all seventy column choices and the meeting guarantee
over every pair of words; check all eight cases of the palette parity rule
and both endings of the two-room trap; and recompute the paper's own
parameters, including the 342 colors of its smallest full-scale stage.

They do not prove the theorem. The full tower is described in words and
pictures and is not implemented, because its smallest honest floor is wider
than any computer. `notes/research-content.md` marks every claim in the
article as computed here, quoted from the literature, or part of the 2026
result.

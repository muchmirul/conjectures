# Condensed Mathematics

A beginner's visual guide to condensed mathematics, in three parts, with
something to move in every chapter.

It retells Peter Scholze's *Lectures on Condensed Mathematics*
([arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026), which record
a course taught in Bonn in 2019, joint work with Dustin Clausen. No
mathematical background is assumed: the guide starts from a set with a
distance on it and builds everything else.

**Read it on the web:** [muchmirul.github.io/conjectures/condensed-math](https://muchmirul.github.io/conjectures/condensed-math/)

## The three parts

| part | lectures | what it adds |
|---|---|---|
| [one, Shapes You Can Only See By Probing Them](parts/condensed-math01/ARTICLE.md) | I to III | a space is what it says to probes, and that makes subtraction work |
| [two, Infinite Sums That Finally Land](parts/condensed-math02/ARTICLE.md) | IV to VI | an endless sum gets exactly one answer, and the objects where it does are rows of dials |
| [three, Rings That Know How To Integrate](parts/condensed-math03/ARTICLE.md) | VII to XI | carry the rule to rings, and geometry with a duality theorem falls out |

Each part is nine chapters, and each chapter carries a simulation embedded in
the article. Twenty-seven in all. The topic is deliberately simulation-heavy:
the definitions here look forbidding and the objects underneath them are
concrete, so every chapter comes with a control that pokes at its own claim.

## Layout

```
parts/condensed-mathNN/
    ARTICLE.md          the source of truth for that part's prose
    guide/NN-.../       one folder per chapter: generated README plus figures
src/condensed_guide/    the computable core, plus the drawing helpers
src/viz/partN_figures.py  every figure of part N
build_guide.py          ARTICLE.md  ->  guide/NN-.../README.md
build_docs.py           ARTICLE.md  ->  ../docs/condensed-math/
build_interactive.py    the 27 playable pages
notes/                  the curriculum, and what is computed versus quoted
tests/                  every claim above, recomputed
```

`ARTICLE.md` is the only file to edit by hand. The chapter READMEs, the web
pages and the playable pages are all generated; run `make all` after editing.

Figures are grouped one script per part rather than one per chapter, because
the figures inside a part share their layout helpers heavily and share almost
nothing across parts. `make part2` re-renders one part.

## Commands

```
cd condensed-math
make venv        # prepare the software once
make test        # recompute every number the articles quote
make figures     # rebuild all 45 figures
make all         # regenerate the chapter files, the pages and the simulations
```

## What is checked, and what is not

Condensed mathematics is foundational, so nearly every theorem in the lectures
is a statement about a whole category, and no program checks those. What this
repository computes is the finite machinery underneath:

- probes as honest inverse systems of finite sets, with their transition maps
- weightings as compatible families of integer weights, and the fact that
  integrating against one does not depend on the level you read it at
- Bergman's basis construction, at finite stages
- the doubling sum, in exact fractions, under both the ordinary size and the
  base-p size
- homology of five shapes by Smith normal form over the integers, torsion
  included
- the measure sizes of part three, and the exponent ceiling in closed form
- the tails on the line and on the coordinate cross, by truncation

`notes/research-content.md` lists every claim the three articles make and
marks it computed, a finite shadow of an infinite statement, or quoted. The
articles say which is which where it matters.

The simulations are checked twice over: `tests/test_interactive.py` runs their
JavaScript and compares it against the Python library at sample points, and
runs every page against a small DOM stub through every position of every
control, so a page that throws fails here rather than in front of a reader.

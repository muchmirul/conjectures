# Condensed Mathematics

This folder contains a three-part visual introduction to condensed mathematics. It is written for readers with no background in the subject. Every chapter explains one idea and includes an activity that lets the reader change a finite example.

The guide follows Peter Scholze's *Lectures on Condensed Mathematics* ([arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026). The lectures record a course taught in Bonn in 2019 and present joint work with Dustin Clausen.

**Read the guide online:** [muchmirul.github.io/conjectures/condensed-math](https://muchmirul.github.io/conjectures/condensed-math/)

**Learn by playing:** [the game](game/README.md) teaches the same subject through eight worlds and assumes no previous mathematics. Each idea begins with a plain explanation. The game then asks the player to make a prediction, try an experiment, and finally learn the standard name and notation. [Play it online](https://muchmirul.github.io/conjectures/condensed-math/game/).

## The three parts

| part | lectures | main idea |
|---|---|---|
| [1. Understanding Spaces Through Probes](parts/condensed-math01/ARTICLE.md) | I to III | Probes record closeness that individual points cannot see, making kernels and cokernels reliable. |
| [2. Giving Infinite Sums a Meaning](parts/condensed-math02/ARTICLE.md) | IV to VI | Compatible weights lead to solid groups and connect infinite sums with ordinary homology. |
| [3. Measure Rules for Rings and Geometry](parts/condensed-math03/ARTICLE.md) | VII to XI | Different rings receive suitable measure rules, leading to compact support, the six operations, and duality. |

Read the parts in order. Each part has an opening activity and eight numbered chapters, for a total of 27 playable pages.

## Files and folders

```text
parts/condensed-mathNN/
    ARTICLE.md            source text for one part
    guide/NN-.../         generated chapter README files and figures
game/
    worlds/               source text and structure for the eight game worlds
    build_game.py         builds the published game pages
src/condensed_guide/      finite mathematical models and drawing helpers
src/viz/partN_figures.py  figure generator for one part
build_guide.py            builds chapter README files from the articles
build_docs.py             builds the published guide
build_interactive.py      builds the 27 playable pages
notes/                    curriculum and claim-by-claim source notes
tests/                    checks for calculations, pages, activities, and game worlds
```

Edit the three `ARTICLE.md` files when changing the written guide. Edit `game/worlds/` when changing the game. The chapter README files, published guide, activities, and game pages are generated. Run `make all` after an edit.

The figure code is grouped by part because the figures within one part share layout helpers. For example, `make part2` rebuilds only the figures for part two.

## Commands

```text
cd condensed-math
make venv        # create the Python environment once
make test        # rerun all calculations and page tests
make figures     # rebuild all figures
make game        # rebuild the eight game worlds
make all         # rebuild the guide, activities, and game
```

## What the tests can verify

Most major results in condensed mathematics concern entire categories, so a finite program cannot prove them. The repository instead checks the concrete calculations used by the explanations:

- probes represented as inverse systems of finite sets, including their transition maps
- compatible integer measures and stage-independent integration
- finite stages of Bergman's basis construction
- geometric sums under ordinary and $p$-adic distance, calculated with exact fractions
- homology of five spaces using Smith normal form over the integers, including torsion
- the effect of merging weights under different exponents
- finite boundary-tail counts for a line and a coordinate cross

The file `notes/research-content.md` records every mathematical claim. It marks each one as computed, a finite illustration of an infinite statement, or quoted from the lectures.

The game tests play every world from beginning to end in a small browser-like environment. They also check the teaching order: explain the concept, state what it assumes, ask for a prediction, provide an experiment, and only then introduce the standard name and symbols.

The activity tests compare the JavaScript calculations with the Python implementation. They also move every control through all its positions, so a page that throws an error fails during testing rather than in front of a reader.

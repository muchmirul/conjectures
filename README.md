# Conjectures

*Famous math problems, explained from zero, with pictures that move.*

Every topic in this repo is one self-contained folder: its own chapters, its own
animations, its own code, and its own tests. Pick one and start reading.

## Topics

| Topic | What it is about | Read it |
|---|---|---|
| [jacobian-conjecture](jacobian-conjecture/) | A question from 1939 about polynomial machines that can be undone. It stayed open for 87 years and then fell in July 2026. | [chapters](jacobian-conjecture/guide/00-start-here/README.md) · [one page](https://muchmirul.github.io/conjectures/jacobian-conjecture/) |
| [kakeya-conjecture](kakeya-conjecture/) | A question from 1917 about the smallest room you can turn a needle around in. There is no smallest room, and the sequel question fell in three dimensions in February 2025. | [chapters](kakeya-conjecture/guide/00-start-here/README.md) · [one page](https://muchmirul.github.io/conjectures/kakeya-conjecture/) |
| [sphere-packing](sphere-packing/) | How densely equal balls can fill space, and the one method that bounds every packing at once. In 2026 the exact strength of that method was determined. | [chapters](sphere-packing/guide/00-start-here/README.md) · [one page](https://muchmirul.github.io/conjectures/sphere-packing/) |
| [multicolor-ramsey](multicolor-ramsey/) | A coloring game about avoiding one-color triangles, and a growth question Erdős put money on. In 2026 the answer arrived: the rate climbs forever. | [chapters](multicolor-ramsey/guide/00-start-here/README.md) · [one page](https://muchmirul.github.io/conjectures/multicolor-ramsey/) |
| [zeta-critical-line](zeta-critical-line/) | The Riemann hypothesis, open since 1859, asks whether every zeta zero sits on one line. In 2026 an AI-authored paper proved two thirds of them do, simple and on the line, unconditionally. | [chapters](zeta-critical-line/guide/00-start-here/README.md) · [one page](https://muchmirul.github.io/conjectures/zeta-critical-line/) |
| [condensed-math](condensed-math/) | A set with a distance on it is two structures badly glued, and the glue fails in a way that breaks ordinary algebra. Scholze and Clausen's repair, in three parts, with a simulation in every chapter, plus a game that makes you discover it from nothing. | [three parts](condensed-math/README.md) · [read it](https://muchmirul.github.io/conjectures/condensed-math/) · [play it](https://muchmirul.github.io/conjectures/condensed-math/game/) |

## How a topic is laid out

```
<topic>/
  README.md   the topic's front page and chapter list
  ARTICLE.md  the whole topic as one continuous page
  guide/      the chapters (each folder: README.md + its images and GIFs)
  src/        the code that generates every figure
  tests/      checks for every mathematical claim the topic makes
  notes/      research notes and sources
```

A topic may also carry a `build_docs.py`, which rebuilds its page under `docs/`
from its `ARTICLE.md`. The one-page version therefore never has to be edited
by hand.

A wide topic may be split into parts, in which case `ARTICLE.md` and `guide/`
sit one level down, inside `parts/<topic>NN/`, and the topic's `docs/` folder
gains one subfolder per part plus a landing page. `condensed-math` is the
first topic laid out that way.

A topic may also carry a `game/`: the same mathematics with the explaining
taken out, as a route a reader walks rather than a text they read. Each idea
arrives as a brick running concept, then intuition ending in a guess, then an
experiment the reader performs, and only then the name and the symbols.
`condensed-math` is the first topic to have one.

Two things live at the repository root instead, because they have to:

- `docs/` is what GitHub Pages serves. It holds one subfolder per topic, plus the
  landing page at [docs/index.html](docs/index.html). GitHub Pages can only publish
  from the root or from `/docs`, so the web versions cannot move into their topic folder.
- `.venv/` is one shared virtualenv for all topics.

## Run the code

```bash
make venv    # create the shared .venv and install every topic
make test    # run every topic's tests
make topics  # list the topics
```

Or work inside a single topic:

```bash
cd jacobian-conjecture
make test
make figures
```

## Adding a topic

1. Create the folder, following the layout above.
2. Create `docs/<topic>/` for its web version.
3. Add the topic to `TOPICS` in the root [Makefile](Makefile), to the table above,
   and to the landing page in [docs/index.html](docs/index.html).

## Why this repo exists

**To pull the essence of a piece of mathematics out to a wider audience.** The
point is intuition first: a reader should be able to see what a problem is
about before meeting any of its machinery. The more people who engage with an
idea, the more people there are who can play with it, and the further the
mathematics itself can travel. Some of it looks impossibly hard and some of it
looks trivially small, but either kind can find a use in the real world once it
reaches the one person who can internalise it and recognise where it fits.

**Why the hardest problems.** A hard problem tends to reach
the parts of a person's imagination that nothing else asks for. A question that
has stayed open for a century is a question that has already resisted every
obvious way of thinking, so meeting it means going somewhere new.

**Abductive thinking, human and machine together.** A human guesses at the
explanation that would make the picture make sense, and works backwards from
there. Pairing that habit with what an AI can do, holding a whole codebase at
once, checking every claim, drawing every figure, makes a collaboration that is
hard to beat.

## The ethos

Distrust, and verify. The writing is friendly, but the claims are not hand-waved.
Every topic re-checks its own mathematics from scratch, in exact arithmetic, on your
machine, not on anyone's authority.

## Donation

USDT (Solana)

```
7adm4hMtxxBSjcztEewVqFV7cXvktceFMfdgMopAXVeC
```

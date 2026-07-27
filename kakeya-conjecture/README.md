# Zero to the Kakeya Conjecture

*A visual, step-by-step journey from "what is a needle?" to one of the most famous problems in modern mathematics, no math background required.*

One topic inside [conjectures](../README.md). Read it online: [muchmirul.github.io/conjectures/kakeya-conjecture](https://muchmirul.github.io/conjectures/kakeya-conjecture/)

<img src="guide/00-start-here/hero.gif" width="620" alt="A needle turning through every direction inside a thin spiky shape of area 0.244">

In 1917 Soichi Kakeya asked how small a room can be if you have to turn a needle right around inside it. Two years later the answer came back: **there is no smallest room.** A needle can be turned inside a set of any size you name, and a close cousin of that set has area exactly zero while still pointing in every direction.

That answer replaced the question with a harder one, which stood for another century, quietly holding up large parts of Fourier analysis. In **February 2025** it fell in three dimensions. Four dimensions and up are still open.

This repo teaches the whole story from absolute zero: pictures first, simple sentences second, symbols last. At the end you will run a complete proof of the grid version **with your own hands**.

## The guide

| | Chapter | The one idea |
|---|---|---|
| 0 | [Start here](guide/00-start-here/README.md) | The promise, and the map of the journey |
| 1 | [The needle](guide/01-the-needle/README.md) | Only direction matters, and all directions fit in a half circle |
| 2 | [Turning around](guide/02-turning-around/README.md) | Disc, triangle, deltoid: the rooms people tried first |
| 3 | [How much space](guide/03-how-much-space/README.md) | Overlap is charged once, and sliding keeps every direction |
| 4 | [The free slide](guide/04-the-free-slide/README.md) | Sliding along your own line is free: Pal's trick |
| 5 | [The Perron tree](guide/05-the-perron-tree/README.md) | Cut and slide; one fixed squeeze stalls forever at a sixth |
| 6 | [Area zero](guide/06-area-zero/README.md) | Besicovitch: there is no smallest room, and zero is reachable |
| 7 | [Zero, but big](guide/07-zero-but-big/README.md) | Dimension: the ruler that survives area being zero |
| 8 | [The conjecture](guide/08-the-conjecture/README.md) | Zero volume yes, small dimension no |
| 9 | [Why it matters](guide/09-why-it-matters/README.md) | Needles become tubes become wave packets |
| 10 | [On a grid](guide/10-on-a-grid/README.md) | The finite field version, and Dvir's half page proof, runnable |
| 11 | [Why it was hard](guide/11-why-it-was-hard/README.md) | Tubes hug without being lines; a century of inches |
| 12 | [The proof](guide/12-the-proof/README.md) | February 2025: dimension 3 in 3D, and what is still open |

**Start reading: [chapter 0 →](guide/00-start-here/README.md)**

Prefer one continuous page? The whole guide is also assembled as a single article, in two formats:

- **[docs/kakeya-conjecture/index.html](../docs/kakeya-conjecture/index.html)**, the polished web version: real LaTeX math (MathJax), playing animations, article typography. Published at [muchmirul.github.io/conjectures/kakeya-conjecture](https://muchmirul.github.io/conjectures/kakeya-conjecture/).
- **[ARTICLE.md](ARTICLE.md)**, plain GitHub-flavored Markdown.

The web version lives at the repository root under `docs/`, not in this folder, because GitHub Pages can only publish from the root or from `/docs`. `make docs` rebuilds it from `ARTICLE.md`, which stays the single source of truth.

## Run the code

Every figure in the guide is produced by a script in this repo, and **every mathematical claim about a computable object is enforced by a test**:

```bash
cd kakeya-conjecture
make venv       # create the shared ../.venv and install (numpy, matplotlib, sympy, pillow)
make test       # re-verify every claim: areas, trees, dimensions, Dvir's proof
make figures    # re-render every figure in guide/
```

The virtualenv sits at the repository root and is shared by every topic, so `make venv` from the root works too.

Play: open any `src/viz/chNN_*.py`, change a construction, re-run, and watch your own monster.

## Layout

```
guide/      the 13 chapters (each folder: README.md + its figures)
src/
  kakeya_guide/   core.py (exact sliver geometry, Perron trees)  finite.py (grids,
                  Dvir's polynomial method)  shapes.py (disc, triangle, deltoid)
                  dimension.py (box counting)  examples.py  plotting.py
  viz/            one figure script per chapter
tests/      exact verification of everything the guide asserts
manim/      optional Manim CE scenes (fancier renders; not required)
notes/      research notes: content and sources, the Perron scan, delivery
build_docs.py   turns ARTICLE.md into ../docs/kakeya-conjecture/index.html
```

## The ethos

Distrust, and verify. The tone is friendly, the claims are not hand-waved. The areas of the Perron trees, the closed form that makes a fixed squeeze stall at exactly 1/6, the deltoid's unit chord, Pal's three-point turn, the box dimension of the Cantor set, the smallest Kakeya sets on grids up to 7 by 7, and **every step of Dvir's 2008 proof** are re-computed from scratch by `tests/`, in exact arithmetic, on your machine, not on anyone's authority.

And where a claim cannot be checked by a computer, the guide says so out loud. Nothing here verifies Davies 1971 or Wang-Zahl 2025; those are quoted, with sources, in [notes/research-content.md](notes/research-content.md).

The conjecture is proved in dimensions 1, 2 and 3. **In four dimensions and up it is still open.** Maybe it is waiting for you.

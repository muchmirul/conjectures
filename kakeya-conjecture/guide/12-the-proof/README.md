# 12 · The proof

*February 2025. After a hundred and eight years, three dimensional space gave up its answer. This page tells you what was proved, by whom, and exactly what is left.*

## The news

On 24 February 2025, Hong Wang and Joshua Zahl posted a paper called *Volume estimates for unions of convex sets, and the Kakeya set conjecture in three dimensions* (arXiv:2502.17655, 127 pages). Its main theorem:

> **Every Kakeya set in $\mathbb{R}^3$ has Hausdorff and Minkowski dimension 3.**

Both rulers. The strong version. The conjecture of chapter 8, in dimension three, is a theorem.

<img src="volume.gif" width="560" alt="Ninety thin tubes pointing in every direction of three dimensional space, with the camera turning right round them">

The engine of the proof is a statement about tubes rather than needles: take a family of thin tubes in space, with a limit on how many of them can be crammed into any one convex region, and their union has to have almost the largest volume it could. Everything else, including the needle statement, follows from that.

The camera turns because it has to. This is a statement about three dimensions, and a still picture of space hides the one thing that matters: the tubes above run over a whole sphere of directions, not a circle of them, and the third axis is where all the difficulty lives.

Terence Tao wrote it up on his blog within a day; the result was reported widely as one of the results of the decade in geometric measure theory. As this guide is written, in July 2026, the paper is on arXiv and has been read closely by the community, and the argument builds on work the same authors had already published on **sticky** Kakeya sets. Treat it the way mathematics treats any result: believed because people have checked it, not because it was announced.

## A Kakeya set of space, in your hand

You can build one from the flat tree of chapter 5, without any new ideas. Push the tree sideways, out of its plane, into a slab.

<img src="kakeya3d.gif" width="560" alt="The flat Perron tree extruded into a translucent green slab in three dimensions, rotating, with a blue needle inside it leaning out of the original plane">

Why that works: a unit needle of space pointing along $(a, b, c)$ casts a shadow on the plane of length $\sqrt{a^2+b^2}$, which is **less** than one. A shorter shadow fits inside the unit segment the flat tree already holds in that direction, and the height the needle needs is $|c| \le 1$, which the slab covers. So the slab holds every direction of space whose shadow lies in the tree's fan, and four rotated copies hold the rest.

The blue needle in the picture is checked rather than drawn by hand. The file `tests/test_core.py` walks along it point by point and checks that every point is inside a sliver and inside the slab.

## What you can check, and what you cannot

This repo's ethos is distrust and verify. So, plainly:

- **A 127 page proof cannot be checked by running a script.** Nothing here verifies Wang and Zahl, and nothing could.
- **What you can run** is everything the theorem sits on top of: that Kakeya sets of tiny area exist at all (chapters 5 and 6), that area zero does not imply small (chapter 7), and the entire finite grid version with Dvir's proof executed step by step (chapter 10).

That is the honest split between what is checked here and what is quoted. Any statement in this guide falls on one side of it or the other, and the text says which.

## A hundred and eight years

| year | who | what |
|---|---|---|
| 1917 | Kakeya | asks for the smallest room a needle can turn in |
| 1919 | **Besicovitch** | **builds a set of area zero holding every direction** |
| 1921 | Pal | smallest convex room: the triangle of height 1 |
| 1928 | Besicovitch | turns the needle in a room of any size you name |
| 1928 | Perron | the tree: a short proof anyone can draw |
| 1971 | Davies | in the plane, area zero still means dimension 2 |
| 1971 | Cunningham | arbitrarily small rooms with no holes, inside a disc |
| 1991 | Bourgain | dimension beats (n+1)/2, the modern assault begins |
| 1995 | Wolff | the hairbrush: dimension at least (n+2)/2, so 5/2 in 3D |
| 1999 | Wolff | poses the finite field version |
| 2000 | Katz, Laba, Tao | 3D nudged past 5/2, by a ten-billionth |
| 2008 | **Dvir** | **finite fields fall to the polynomial method, in half a page** |
| 2019 | Katz, Zahl | the same nudge for the finer ruler, Hausdorff dimension |
| 2025 | **Wang, Zahl** | **every Kakeya set in 3D has dimension 3** |

Kakeya asked in 1917 for the smallest room. Besicovitch answered in 1919 that there is none, and the question turned into a different one. That second question outlived everyone who first asked it.

## What survives

| dimension | status |
|---|---|
| 1 | trivial: a segment is one dimensional |
| 2 | proved by Davies, 1971 |
| 3 | proved by Wang and Zahl, February 2025 |
| 4 | **open** |
| 5 and up | **open** |

The result is specifically three dimensional. It uses the geometry of lines in space, where two directions span a plane and the third dimension is the only room left over. In four dimensions there is more room, the possible configurations multiply, and the known bounds fall well short of 4.

So the conjecture is not finished. It is settled in exactly the dimensions where you can draw a picture.

## Why this ending is a good one

For a century the story was about shrinking: how small, how much smaller, is there a floor. Besicovitch answered that in the strongest way possible, by removing the floor. Everyone then agreed on the replacement question and could not answer it for another century, while it quietly became a load bearing wall under Fourier analysis.

The answer, when it came, was not a clever construction or a slick trick. It was the accumulated ability to talk about structure at many scales at once, built over thirty years by many people, finally sharp enough to close the gap. That is what most hard mathematics actually looks like from the inside.

And the needle, the actual physical needle from 1917, turns in a room of any size you name. That part was true the whole time.

## Where to go next

- **This repo's notes**: [notes/research-content.md](../../notes/research-content.md), for sources, exact statements, and what is verified where.
- H. Wang and J. Zahl, *Volume estimates for unions of convex sets, and the Kakeya set conjecture in three dimensions*, arXiv:2502.17655.
- T. Tao's blog post, *The three-dimensional Kakeya conjecture, after Wang and Zahl*, a readable account of the strategy.
- Z. Dvir, *On the size of Kakeya sets in finite fields* (2008), the half page proof of chapter 10.
- K. Falconer, *The Geometry of Fractal Sets*, for Besicovitch sets and dimension from the ground up.
- J. Zahl, *A survey of the Kakeya conjecture, 2000 to 2025* (arXiv:2512.09397), for where the field stands and what is still open.
- Quanta Magazine, *'Once in a Century' Proof Settles Math's Kakeya Conjecture* (March 2025), for the story with no equations.
- The Wikipedia article *Kakeya set*, for current status and further references.

## Try it

```bash
python src/viz/ch12_the_proof.py
python -m pytest tests/ -q      # re-verify EVERYTHING this guide claims to check
```

---

> **The one thing to remember:** in February 2025 Wang and Zahl proved that every Kakeya set in three dimensional space has dimension 3, the plane was settled in 1971, and four dimensions and up are still open.

[← Why it was hard](../11-why-it-was-hard/README.md) · [Back to the start](../00-start-here/README.md)

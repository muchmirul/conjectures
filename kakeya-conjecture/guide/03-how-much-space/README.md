# 3 · How much space

*By the end of this page you will know how area is counted here, and you will have seen the loophole that the whole story walks through.*

## Overlap is only counted once

Two shapes cover a region, and the area they cover together is not the sum of their two areas. The part they share is one patch of ground, and ground does not get counted twice because two shapes claim it. That sounds like a technicality, and it is what every shrinking construction in this guide runs on.

<img src="overlap.gif" width="820" alt="A triangle split down the middle; the right half slides left onto the left half while a graph shows the total area dropping from 1 to two thirds">

Split a triangle down the middle, then slide the right half onto the left half. The two pieces never shrink. Nothing is thrown away. Every direction the original triangle held is still held, because sliding a piece sideways does not turn it. And yet the ink on the page **drops**, because the halves now share ground.

Slide by exactly the right amount and you land on the best deal available:

```math
\text{area after sliding by } t = 1 - t + \tfrac34 t^2 ,
```

which is smallest at $t = 2/3$, where the two halves together cover exactly **two thirds** of what the whole triangle covered. The repo checks this closed form at every $t$ it can, exactly, in fractions (`tests/test_core.py`).

That is two thirds from a single cut. Chapter 5 cuts again, and then keeps cutting.

## How the area is actually measured here

Every figure in this guide is made of **slivers**: triangles standing on the same ground line, all the same height. That one restriction makes area easy to compute exactly.

<img src="slices.gif" width="820" alt="A horizontal line sweeping up through two overlapping triangles, with a graph on the right building the profile of covered width against height">

At each height, a sliver covers one interval. A pile of slivers covers a union of intervals, and a union of intervals has an obvious length, with the overlaps counted once. Sweep the height from bottom to top, add up the widths, and you have the area.

The code does this in exact rational arithmetic, not floating point, so an area quoted in this guide is not a rounded estimate: it is the number. To be sure the fast sweep is right, the repo also computes every area a second, slower, obviously correct way, and the tests demand that the two agree.

## Why this matters for a needle

A needle only cares about direction. Two slivers that overlap still hold all the directions they held apart. So overlap is free storage: you can pile up the directions and pay only once for the ground.

That is the loophole. The rest of the guide is people learning how far it goes.

## Try it

```bash
python src/viz/ch03_how_much_space.py
python -m pytest tests/test_core.py -q
```

```python
from fractions import Fraction
from kakeya_guide.core import merged_pair_area

merged_pair_area(Fraction(2, 3))     # -> Fraction(2, 3)
```

---

> **The one thing to remember:** overlapping shapes are charged for shared ground once, and pieces that slide keep every direction they had, so directions can be stacked cheaply.

[← Turning around](../02-turning-around/README.md) · [Next: the free slide →](../04-the-free-slide/README.md)

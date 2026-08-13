# 7 · Zero, but big

*By the end of this page you will have a second ruler for "how big is this set", one that does not collapse to zero when the area does.*

## Area was the wrong question

Chapter 6 broke area as a measure of these sets. A Besicovitch set has area 0. So does a single dot. So does a line segment. Area cannot tell them apart, and clearly they are not the same kind of nothing.

Mathematicians needed a sharper ruler, and the one they use is **dimension**. Not "the space it lives in", but "how the set fills space as you zoom in".

## Counting boxes

Cover the set with a grid of boxes of side $\varepsilon$ and count how many boxes it touches. Then shrink $\varepsilon$ and count again. What matters is how the count **grows**.

- A dot: 1 box, always. The count does not grow.
- A unit segment: about $1/\varepsilon$ boxes. Halve the box, double the count.
- A solid square: about $1/\varepsilon^2$ boxes. Halve the box, quadruple the count.

The exponent is the **dimension**: $N(\varepsilon) \approx \varepsilon^{-d}$. Segment 1, square 2. So far so boring. Now a set that is neither.

## The Cantor set: no length, and yet

Start with the interval from 0 to 1 and remove the middle third. Remove the middle third of what is left. Repeat forever.

<img src="cantor.png" width="780" alt="Rows showing the middle thirds Cantor set: 1 piece of length 1, 2 pieces of length 0.667, 4 of 0.444, down to 128 pieces of length 0.0585">

The length after $m$ rounds is exactly $(2/3)^m$, which marches to zero. The finished set has length **0**. It is also uncountably infinite and contains no interval at all. Now count boxes.

<img src="boxcount.png" width="840" alt="Boxes of three sizes covering the Cantor set, with a log-log plot whose slope is 0.6309">

At box size $3^{-m}$ the count is exactly $2^m$. So

```math
d = \frac{\log 2}{\log 3} = 0.6309\ldots
```

Length zero, dimension 0.63. The set is bigger than a dot and smaller than a line, and the two rulers give completely different answers. This is not a trick of definitions; it is the correct description of a set that is genuinely spread out at every scale while occupying no room.

## The zoo

<img src="zoo.png" width="780" alt="A bar chart of dimensions: a dot 0, Cantor set 0.63, Cantor set with ratio a quarter 0.5, Cantor set times a line 1.63, a Besicovitch set 2, a solid square 2">

The Cantor set crossed with a line segment has area 0 and dimension $1.63$. Two Cantor sets crossed with each other have area 0 and dimension $1.26$. Each of these is computed by counting boxes in this repo, and each measured slope matches its theoretical value to more decimals than are shown (`tests/test_dimension.py`).

A Besicovitch set in the plane has area 0, like all of these, and dimension **2**, the same as a solid square. That is a theorem, proved by Roy Davies in 1971, and it is the last piece of setup before the conjecture.

That is exactly the shape of the question. Area zero these sets can manage, and what remains to ask is whether they can be thin in the sharper sense as well.

## Try it

```bash
python src/viz/ch07_zero_but_big.py
python -m pytest tests/test_dimension.py -q
```

```python
from fractions import Fraction
from kakeya_guide.dimension import cantor_length, cantor_box_dimension

cantor_length(20)                          # -> Fraction(1048576, 3486784401)
cantor_box_dimension(2, Fraction(1, 3))    # -> 0.6309297535714574
```

---

> **The one thing to remember:** dimension counts how fast the covering boxes multiply as they shrink, it can be a fraction, and a set of zero area can have any dimension it likes, right up to full.

[← Area zero](../06-area-zero/README.md) · [Next: the conjecture →](../08-the-conjecture/README.md)

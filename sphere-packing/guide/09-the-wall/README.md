# 9 · The wall

Making the radius smaller makes the requirement harder to meet. The negative amount remains exactly half of the total, but it has less space in which to fit.

![A radius shrinking until there is not enough room for the required negative half](wall.gif)

The animation uses a simple shrinking speed chosen to make the idea visible. It shows why the fixed half eventually cannot fit, rather than exact values for individual dimensions.

The 2026 proof shows that there is a long-term limit. As dimensions grow, a radius below one over pi times the square root of the dimension cannot hold enough of the balanced function. The greatest amount that could fit there becomes exponentially small, meaning that it repeatedly shrinks by a fixed factor as dimensions are added. One half does not shrink at all, so no certificate can keep its radius below that limit.

Finite dimensions can differ slightly from this simple description. The statement is about the rate as the dimension becomes large: after the radius is divided by the square root of the dimension, those smaller differences disappear. This is the part of the proof that places a ceiling on the certificate method.

The appearance of pi comes from a specific step in the proof. The argument first changes to a view in which the Fourier transform acts like a reflection. It then studies a strip-shaped region. A standard result says that values along the two edges control what can happen between them; this result is called the maximum principle. It gives a weight to each wave. At the decisive edge of the strip, those weights approach one particular bell-shaped curve.

![The proof’s changing weights settling into the bell-shaped curve that fixes the limit](ingredients.png)

That final curve produces the factor one over pi. This repository does not reproduce the proof, but it does recalculate several of its ingredients. The tests confirm that the reflection step changes direction without changing size along the required line. They also confirm that the limiting curve has total area one and the stated Fourier view. A separate check recovers the exact average used by the proof.

One small-looking detail affects the final number. At an earlier stage, the edge weights do not add up to one. Turning them into percentages too soon would change the result, so the proof must keep their original total until the correct step.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/09.html)** to reduce the radius and compare its capacity with the fixed negative half.

---

[← The balancing trick](../08-balancing/README.md)  ·  [Building the witness →](../10-the-witness/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

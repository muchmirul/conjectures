# 9 · The wall

Sections 8 and 9 form the first half of the proof, and they show that no certificate, including one nobody has discovered yet, can have a better long-term radius. Making the radius smaller makes the requirement harder to meet, because the negative amount remains exactly half of the total while having less space in which to fit.

![A radius shrinking until there is not enough room for the required negative half](wall.gif)

The animation uses a simple shrinking speed chosen to make the idea visible. It shows why the fixed half eventually cannot fit, rather than exact values for individual dimensions.

The 2026 proof shows that there is a long-term limit. As dimensions grow, a radius below one over pi times the square root of the dimension cannot hold enough of the balanced function. The greatest amount that could fit there becomes exponentially small, meaning that it repeatedly shrinks by a fixed factor as dimensions are added. One half does not shrink at all, so no certificate can keep its radius below that limit.

Finite dimensions can differ slightly from this simple description. The statement is about the rate as the dimension becomes large: after the radius is divided by the square root of the dimension, those smaller differences disappear. This is the part of the proof that places a ceiling on the certificate method.

The number pi comes from one particular step. The proof changes how the function is viewed until the Fourier transform acts like a mirror, and it then looks at a strip, meaning the region between two parallel edges. A standard rule called the maximum principle says that values on those edges limit what can happen between them. This rule gives a weight to each wave, and near the important edge the weights settle into one bell-shaped curve.

![The proof’s changing weights settling into the bell-shaped curve that fixes the limit](ingredients.png)

That final curve produces the factor one over pi. This repository does not reproduce the proof, but it does recalculate several of its ingredients. The tests confirm that the reflection step changes direction without changing size along the required line, and they also confirm that the limiting curve has total area one and the stated Fourier view. A separate check recovers the exact average used by the proof.

At an earlier stage of the proof, the edge weights do not add up to one, and this small-looking detail affects the final number. Turning them into percentages too soon would change the result, so the proof must keep their original total until the correct step.

The behind-the-scenes document describes an earlier idea that failed. It compared only two totals: all the negative weight and all the room available inside the ball. This does give a limit, but not the correct one, because a total records how much weight exists without recording where that weight sits. Two functions can have similar totals while placing their negative parts in very different places. The successful proof had to keep track of location as well as amount, which is what the strip method above does.

The sources also give a second way to express the same wall, using one fixed object, built from nonnegative weights, that can check every certificate at once. Mathematicians call this a dual witness. The rest of the guide does not use it, but it is useful confirmation, because this different viewpoint reaches the same limit.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/09.html)** to reduce the radius and compare its capacity with the fixed negative half.

---

[← The balancing trick](../08-balancing/README.md)  ·  [Building the witness →](../10-the-witness/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

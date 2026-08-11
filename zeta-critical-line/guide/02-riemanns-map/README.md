# 2 · Riemann's map

In 1859 Bernhard Riemann sent the Berlin Academy an eight-page memoir on how many primes lie below a given bound. Its central object is a single function, now written with the Greek letter zeta. The recipe behind it starts simply: pick a strength, take every whole number, raise each to that strength, flip each into one-over-it, and add them all up. Riemann's step was to feed this recipe not a single number but a point in the plane: one coordinate for the strength, a second coordinate that makes the terms rotate as well as shrink. He then extended the map, in the one standard way such maps extend, so that it covers essentially the whole plane. The result assigns a value to every point, and it helps to see the size of that value as a landscape.

![A rotating three-dimensional view of the zeta landscape over the critical strip, with the floor touched only along the critical line](landscape.gif)

The camera circles so that the shape is genuinely three-dimensional: two directions of the floor are the two coordinates of the input point, and the height is the size of zeta there. What matters is where the landscape touches the floor, because floor level means the value is exactly zero. There are some easy touchdowns far to the left of the picture, at a neat row of evenly spaced points on the real axis; they are called the trivial zeros, they are completely understood, and this guide sets them aside now and does not mention them again. Every other touchdown lies inside a vertical band called **the strip**: the band of points whose first coordinate is between zero and one. These are the zeros that control the prime wobble of chapter 1, and in the picture every one of them sits at first coordinate exactly one half, on the vertical line down the middle of the strip. That middle line is what this guide calls **the line**: the critical line, the place the paper's two thirds refers to.

![A flat map of the strip with the first thirty zeros marked on the critical line, and the mirror symmetry indicated](strip.png)

The flat map shows the same region from above, with the first thirty zeros marked as pins. Two symmetries are worth carrying forward. The zeros come in top-bottom pairs, so it is enough to look above the horizontal axis, and everyone measures a zero by its **height**: the first sits at height 14.13, the second at 21.02, and so on, forever upward. Less obviously, the landscape obeys a left-right mirror rule across the line: if a zero ever sat off the line, its mirror image through the line would also be a zero. Off-line zeros could only appear as symmetric pairs, one on each side at the same height. We will call such a hypothetical couple a **mirror pair**, and no such pair has ever been found.

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/02.html)** to slide a slice across the strip and watch the valley touch zero only at one half.

---

[← The primes](../01-the-primes/README.md)  ·  [The music of the primes →](../03-the-music/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

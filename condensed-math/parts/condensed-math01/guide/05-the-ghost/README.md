# 5 · The quotient with no points

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Now the repair pays off.

Go back to the map from the dust to the ruler. As answer sheets, these are genuinely different objects, so the map between them is genuinely not a sameness, and algebra is now allowed to ask what the difference is. Subtract the dust from the ruler. The result is a perfectly good condensed group, and this guide calls it **the ghost**.

The ghost has no points. Ask it what a single point can say, and the answer is: nothing, the entry is empty. By the old way of counting, the ghost is zero.

Ask it what the halving probe can say, and the answer is not empty.

![A staircase-like function being built on the branching probe, level by level, ending as a landing that is continuous but not flat on any box](ghost.gif)

The animation builds one entry of the ghost. On the halving probe, choose a value on each box, refine, choose again, and keep the choices consistent. In the limit you get a landing which is perfectly continuous but is not constant on any box, no matter how far you refine. A landing like that is precisely something the ruler can do and the dust cannot, so it is a nonzero entry of the ghost's answer sheet ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)).

So the ghost is an object with no points which is not zero. That sounds like a paradox and it is the opposite: it is the missing piece that makes the recipe work. The map from the dust to the ruler kills nothing and misses nothing *at the level of points*, and the reason it is still not a sameness is a difference which only shows up on probes, and which the ghost now names.

With that, the thing algebra needs is finally true.

> Condensed groups form a setting where every map has a genuine kill-list and a genuine miss-list, and a map with both of them empty really is a sameness.

That is the opening theorem of the lectures ([Theorem 1.10, page 9](https://arxiv.org/pdf/2605.03658v1#page=9), restated with the size bound fixed as [Theorem 2.2, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)). In the standard vocabulary: condensed abelian groups form an abelian category, and it satisfies the strongest of the usual good behaviour axioms, including some that sheaves almost never satisfy. Topological groups form no such thing, which is where this guide began.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/05.html)** to build a ghost entry yourself and watch the point count stay at zero while the probe entry stays nonzero.

---

[← Cut, and glue](../04-cut-and-glue/README.md)  ·  [Probes that never need folding →](../06-unfoldable-probes/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

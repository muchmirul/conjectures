# 8 · Solidification recovers homology

*Part 2 of three: Giving Infinite Sums a Meaning. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We can now return from infinite sums to topology. Begin with a circle, sphere, torus, or another space built from cells. Form the free condensed abelian group on its points, then apply derived solidification.

![A torus rotates in three dimensions beside bars for homology in degrees zero, one, and two](solidify.gif)

The homology groups of the result are the classical integral homology groups of the original space ([Example 6.5, page 44](https://arxiv.org/pdf/2605.03658v1#page=44)). Degree zero records connected components, degree one records loop classes, and degree two can record enclosed surfaces. Higher degrees describe higher-dimensional versions. The result also keeps torsion, which is information about classes killed by multiplication by an integer.

![Free and torsion homology classes are compared for a circle, figure eight, sphere, torus, and Klein bottle](homology_bars.png)

The chart is computed from cellular boundary maps using Smith normal form over the integers. A circle has one degree-one class, and a figure eight has two. A sphere has one degree-two class and no degree-one class. A torus has two degree-one classes and one degree-two class. A Klein bottle has one free degree-one class and one torsion class of order two. Doubling that torsion class gives zero.

The theorem connects the ideas from both parts. Part one showed that translating a compact space into condensed mathematics preserves integral cohomology. This part described solidification through maps from products of integers. The lectures combine these facts to identify derived solidification of the free group on a space with singular homology.

The definition of solidity mentions compatible sums rather than loops or surfaces. Even so, its universal completion recovers a standard topological invariant. Completion and topology therefore fit inside the same framework.

### The mathematics

For a CW complex $X$, [Example 6.5, page 44 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=44) identifies derived solidification with singular homology:

```math
\mathbb Z[X]^{L\blacksquare}\cong H_\bullet(X;\mathbb Z).
```

We can apply the theorem to several familiar spaces. For the circle, sphere, and torus, it gives

```math
H_\bullet(S^1;\mathbb Z)=(\mathbb Z,\mathbb Z),
\quad
H_\bullet(S^2;\mathbb Z)=(\mathbb Z,0,\mathbb Z),
\quad
H_\bullet(T^2;\mathbb Z)=(\mathbb Z,\mathbb Z^2,\mathbb Z).
```

**Reading the symbols.** The space $X$ is a CW complex, meaning that it is built from cells. The object $\mathbb Z[X]$ is the free condensed abelian group on its points. The superscript $L\blacksquare$ means derived solidification. The notation $H_\bullet(X;\mathbb Z)$ means all singular homology groups of $X$ with integer coefficients, arranged by degree. The symbols $S^1$ and $S^2$ are the circle and sphere, while $T^2$ is the torus. Each list begins with degree zero and then gives the higher degrees in order. The expression $\mathbb Z^2$ means two independent copies of the integers.

**Why it matters.** A completion defined by compatible infinite sums recovers integral homology. Because the construction is derived, groups can appear in several degrees, and it keeps integer torsion such as the order-two class of the Klein bottle.

**In the simulation.** The shape control chooses $X$. Bars display the homology groups by degree, and the camera rotates the three-dimensional examples. A brown bar labelled two represents a $\mathbb Z/2\mathbb Z$ torsion class, not two free copies of $\mathbb Z$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/08.html)** to compare the homology of five spaces and rotate the three-dimensional models.

---

[← Completed tensor products](../07-the-multiplication-table/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

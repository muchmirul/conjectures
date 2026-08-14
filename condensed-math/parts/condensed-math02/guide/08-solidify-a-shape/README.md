# 8 · Solidify a shape, get its holes

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We can now connect the summation rule back to topology. Begin with an ordinary space, such as a circle, sphere, or torus. Form the free condensed abelian group on its points, which allows finite formal integer combinations of those points, and then apply derived solidification.

![A torus rotates in three dimensions beside bars for its homology in degrees zero, one, and two](solidify.gif)

The homology groups of the resulting object are the classical integral homology groups of the original space ([Example 6.5, page 44](https://arxiv.org/pdf/2605.03658v1#page=44)). Thus, the degrees record connected pieces, loops, enclosed surfaces, and higher-dimensional analogues. Torsion information is retained as well, so the result contains more than numerical hole counts.

![Free and torsion homology groups are compared for a circle, figure eight, sphere, torus, and Klein bottle](homology_bars.png)

The chart is computed from cellular boundary maps using Smith normal form over the integers. A circle has one free class in degree one, and a figure eight has two. A sphere has one class in degree two and none in degree one. A torus has two degree-one classes and one degree-two class. The Klein bottle has one free degree-one class together with a torsion class of order two, which disappears when doubled.

The connection follows the ideas already developed. Part one showed that integral cohomology agrees before and after translating a compact space into condensed mathematics. In this part, solidification is characterized through maps from products of integer groups, while maps out of the free group on a space correspond to integer-valued data on that space. The lectures turn this correspondence into the precise identification with singular homology.

This result explains why solidity matters beyond the original convergence problem. The definition mentions compatible infinite sums, not loops or surfaces. Nevertheless, applying its universal completion to the free group of a space recovers established topological invariants. The same framework can therefore handle completion and topology without treating them as unrelated constructions.

### The mathematics

For a CW complex $X$, [Example 6.5, page 44 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=44) identifies derived solidification with singular homology:

```math
\mathbb Z[X]^{L\blacksquare}\cong H_\bullet(X;\mathbb Z).
```

The figure uses three familiar spaces. For these examples, the theorem gives

```math
H_\bullet(S^1;\mathbb Z)=(\mathbb Z,\mathbb Z),
\quad
H_\bullet(S^2;\mathbb Z)=(\mathbb Z,0,\mathbb Z),
\quad
H_\bullet(T^2;\mathbb Z)=(\mathbb Z,\mathbb Z^2,\mathbb Z).
```

**Reading the symbols.** The space $X$ is built from cells. The object $\mathbb Z[X]$ is the free condensed abelian group on its points. The superscript $L\blacksquare$ means derived solidification. The notation $H_\bullet(X;\mathbb Z)$ means all singular homology groups of $X$ with integer coefficients, arranged by degree. The circle and sphere are $S^1$ and $S^2$, and $T^2$ is the two-dimensional torus. Each parenthesized list gives degree zero first, then degree one, then degree two when present. The expression $\mathbb Z^2$ means two independent copies of the integers.

**Why it matters.** A completion defined through compatible infinite sums recovers a classical topological invariant. Because the statement is derived, nonzero homology may appear in several degrees, and integer torsion such as the Klein bottle's order-two class is retained.

**In the simulation.** The shape selector chooses $X$. The bars display the groups on the right side degree by degree, and the camera control rotates the three-dimensional models. A brown bar labelled by two represents a $\mathbb Z/2\mathbb Z$ torsion class rather than a free copy of $\mathbb Z$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/08.html)** to select a space, rotate the three-dimensional examples, and compare their free and torsion homology classes.

---

[← The multiplication table](../07-the-multiplication-table/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

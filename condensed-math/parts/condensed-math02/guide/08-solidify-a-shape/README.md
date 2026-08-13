# 8 · Solidify a shape, get its holes

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We can now connect the summation rule back to topology. Begin with an ordinary space, such as a circle, sphere, or torus. Form the free condensed abelian group on its points, which allows finite formal integer combinations of those points, and then apply derived solidification.

![A rotating three-dimensional doughnut surface with its holes counted off as bars beneath it](solidify.gif)

The homology groups of the resulting object are the classical integral homology groups of the original space ([Example 6.5, page 44](https://arxiv.org/pdf/2605.03658v1#page=44)). Thus, the degrees record connected pieces, loops, enclosed surfaces, and higher-dimensional analogues. Torsion information is retained as well, so the result contains more than numerical hole counts.

![The computed hole counts of five shapes, including the two-torsion of the Klein bottle](homology_bars.png)

The chart is computed from cellular boundary maps using Smith normal form over the integers. A circle has one free class in degree one, and a figure eight has two. A sphere has one class in degree two and none in degree one. A torus has two degree-one classes and one degree-two class. The Klein bottle has one free degree-one class together with a torsion class of order two, which disappears when doubled.

The connection follows the ideas already developed. Part one showed that integral cohomology agrees before and after translating a compact space into condensed mathematics. In this part, solidification is characterized through maps from products of integer groups, while maps out of the free group on a space correspond to integer-valued data on that space. The lectures turn this correspondence into the precise identification with singular homology.

This result explains why solidity matters beyond the original convergence problem. The definition mentions compatible infinite sums, not loops or surfaces. Nevertheless, applying its universal completion to the free group of a space recovers established topological invariants. The same framework can therefore handle completion and topology without treating them as unrelated constructions.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/08.html)** to select a space, rotate the three-dimensional examples, and compare their free and torsion homology classes.

---

[← The multiplication table](../07-the-multiplication-table/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

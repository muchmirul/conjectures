# 8 · Solidify a shape, get its holes

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The last section of this part is the payoff, and it is a magic trick with a short explanation.

Take an ordinary shape: a circle, a doughnut surface, a sphere. Turn it into a group the cheapest possible way, by taking formal combinations of its points, with no relations imposed. Then solidify.

![A rotating three-dimensional doughnut surface with its holes counted off as bars beneath it](solidify.gif)

Out comes the shape's holes.

Not a shadow of them, not something related to them: the hole counts exactly, in every degree, torsion included. Solidification, an operation defined purely to make infinite sums behave, hands back the classical topology of the shape ([Example 6.5, page 44](https://arxiv.org/pdf/2605.03658v1#page=44)).

![The computed hole counts of five shapes, including the two-torsion of the Klein bottle](homology_bars.png)

The bars are computed in this repository from cell-by-cell boundary data, over the whole numbers, using Smith normal form, so the torsion is genuine and not rounded away. A circle has one hole in degree one. A figure eight has two. A sphere has none in degree one and one in degree two. A doughnut has two and one. A Klein bottle has one hole in degree one plus a piece of order two, which is a hole you have to go round twice to close, and the computation finds it.

Why this happens is short. Part one, section 8 showed that counting holes with whole numbers is the same whether you count classically or inside the world of answer sheets. Solidification is defined by how it answers questions from rows of dials, and questions asked of a shape's formal combinations are exactly whole-number measurements on the shape, which is hole counting. The two descriptions meet, and the lectures make the identification precise in half a page.

The consequence worth keeping is the direction the information travels. Nobody put topology into the definition of solidity. Solidity was defined by a rule about infinite sums, section 5, and the topology came out anyway. That is the sense in which the subject is not a repackaging: it is one notion that turns out to be several.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/08.html)** to pick a shape, turn it in three dimensions, and read the holes that fall out.

---

[← The multiplication table](../07-the-multiplication-table/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

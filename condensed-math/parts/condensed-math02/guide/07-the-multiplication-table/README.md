# 7 · The multiplication table

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Solid groups can be multiplied together, in the sense that two of them combine into a third that handles pairs. The combination is called the completed tensor product, and its table is the most quotable thing in the lectures.

![The completed tensor products of the sample groups, arranged as a grid, with the vanishing entries marked](tensor_table.png)

The grid reads as follows. The base-two numbers combined with the base-three numbers give zero, while the base-two numbers combined with themselves give the base-two numbers back. The base-two numbers combined with the real numbers give zero, which section 6 already explains. Power series in one variable combined with power series in another give power series in both.

![Two rulers marked in powers of two and powers of three sliding against each other, with no scale ever lining up](rulers.gif)

The two-and-three entry is the surprising one, and the animation above draws the two nestings side by side, one shrinking its boxes by twos and the other by threes. The base-two numbers are built by a nesting whose boxes shrink by twos, and the base-three numbers by a nesting whose boxes shrink by threes. Neither nesting reaches the other's boxes, because three is a unit in the base-two world, so dividing by three is harmless there, and two is a unit in the base-three world. Nothing can carry both nestings at once, so the product is zero.

The lectures summarise the pattern in a sentence worth quoting, that the completed tensor product asks both sides which nesting they carry, and then keeps all of them ([Example 6.4, page 44](https://arxiv.org/pdf/2605.03658v1#page=44)). Two compatible nestings combine, and two incompatible ones annihilate.

The one entry in the grid that this repository derives rather than transcribes is the power series row. Section 4 said a collection of weightings is a row of dials, and the lectures show that combining two such rows gives the row indexed by all pairs ([Proposition 6.3, page 43](https://arxiv.org/pdf/2605.03658v1#page=43)). A power series in one variable has one dial per power of that variable, so pairs of dials are pairs of powers, which is exactly a power series in two variables. The tests check that pairing, and mark the rest of the grid as quoted from the lectures.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/07.html)** to pick any two entries and see the product, with the nesting that explains it.

---

[← Where the real line goes](../06-where-the-real-line-goes/README.md)  ·  [Solidify a shape, get its holes →](../08-solidify-a-shape/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

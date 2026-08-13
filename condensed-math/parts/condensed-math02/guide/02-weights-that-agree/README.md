# 2 · Weights that agree

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

A weighting turns the opening animation into a definition. Begin with one integer on the coarsest box of a probe. When that box is refined, assign integers to its smaller boxes whose sum equals the original integer. Continue at every level. The resulting family is compatible because the weight of any box always equals the sum of all weights immediately below it.

![The same function read at a coarse level and at a fine one, with the two totals coming out equal](integral.png)

This compatibility makes integration independent of the chosen level. A continuous integer-valued function on a probe is constant on the boxes of some finite stage. Multiply each of those values by its box's weight and add the finite list. If the stage is refined, the function value is repeated on the smaller boxes and their weights add back to the old weight, so the answer stays the same. The figure compares these two calculations, and the tests verify their agreement for both the halving and base-p probes.

The lectures call the group of all such weightings the free solid group on the probe. They define it as an inverse limit of finite groups, with one copy of the integers for every box and with refinement maps that add weights back together ([Definition 5.1, page 33](https://arxiv.org/pdf/2605.03658v1#page=33)). An element of this inverse limit is also called a measure because it assigns a compatible integer size to every box.

The simplest example concentrates one unit at a single point. Follow the branch leading to that point, place weight one on its box at every stage, and place zero on all other boxes. This is a Dirac measure. The code constructs these point measures, checks their compatibility, and uses them as the point-level data that more general weightings must extend.

The important simplification is that each stage contains only finite data. A weighting may involve infinitely many levels, but each level is just a finite list of integers, and compatibility is checked by finite addition. The next two sections study the functions being integrated and use their algebraic structure to classify all weightings.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/02.html)** to split weights across finer boxes and see which assignments satisfy the compatibility rule.

---

[← Sums with nowhere to land](../01-sums-with-nowhere-to-land/README.md)  ·  [Every function is a stack of steps →](../03-stacks-of-steps/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

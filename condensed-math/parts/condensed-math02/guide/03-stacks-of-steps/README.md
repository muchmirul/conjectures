# 3 · Every function is a stack of steps

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

To understand weightings, it helps to look at what they are weighing. A continuous whole-number-valued measurement on a probe is a simple thing. Because the values are whole numbers they cannot drift smoothly, so continuity forces the measurement to be constant on small enough boxes. This means that every such measurement is decided at some finite stage, and is a plain function on a finite list of boxes.

![A whole-number measurement on the branching probe being taken apart into step functions, one basis element at a time](steps.gif)

The animation takes such a measurement apart. Each step function is one box switched on and everything else switched off, or a product of a few such switches, and the original is rebuilt by stacking them with whole-number coefficients. The rebuild uses each step exactly once and needs no fractions.

That is a stronger statement than it looks, and it is a genuine theorem. The measurements on a probe form a group under addition, and the claim is that this group has a basis, meaning a list of measurements such that everything is a whole-number combination of finitely many of them, in exactly one way. Groups with a basis are called free, and most groups are not.

![The number of basis elements produced by the construction, level by level, matching the number of boxes at that level](basis_size.png)

The theorem that this always works is due to Nöbeling, building on Specker, and the lectures give Bergman's proof of it ([Theorem 5.4, page 34](https://arxiv.org/pdf/2605.03658v1#page=34)). This repository runs that construction: it orders the products of switch functions, keeps each one that is not already a combination of earlier ones, and checks the result is a basis. The chart shows the count coming out equal to the number of boxes at every level, which is what a basis must give.

One honesty note belongs here. At any single finite stage, freeness is automatic and the computation checks only that the *construction* behaves. The theorem's content is entirely in the infinite limit, where it is not automatic and where nothing in this repository can reach. The tests say what they check and no more.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/03.html)** to draw a measurement on the probe and watch it get taken apart into steps.

---

[← Weights that agree](../02-weights-that-agree/README.md)  ·  [Products in, sums out →](../04-products-in-sums-out/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

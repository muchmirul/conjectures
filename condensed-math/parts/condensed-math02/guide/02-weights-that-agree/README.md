# 2 · Weights that agree

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Here is the answer, and it is the animation from the top of this page.

Take a probe. At the coarsest stage there is one box; give it a number. Split the box; split the number between the two new boxes, however you like, as long as the two add back to the original. Keep going forever. The result is a **weighting**: one number per box at every stage, with the rule that a box's number is always the total of the boxes inside it.

![The same function read at a coarse level and at a fine one, with the two totals coming out equal](integral.png)

A weighting is exactly what you need to add things up. Suppose someone hands you a value for each box, and you want a single total. Multiply each box's value by the box's weight, and add. The picture shows the one property that makes this well posed: if you refine, and read the same values on the smaller boxes, the total does not change. This repository computes both readings and the tests check they agree, on the halving probe and on the base-p probe.

That is genuinely an infinite sum. The probe has infinitely many points, the weighting spreads a finite total across all of them, and the answer is a single number.

The lectures write the collection of all weightings on a probe as the free solid group on that probe, and build it as exactly this: the limit of the finite pictures, one copy of the whole numbers per box at each stage, fitting together down the levels ([Definition 5.1, page 33](https://arxiv.org/pdf/2605.03658v1#page=33)). Its elements are called measures on the probe, which is the ordinary word for a rule that assigns a size to every region.

Two things about weightings are worth carrying forward.

First, the simplest weighting is one unit sitting on a single point of the dust, and it is what you get by following one branch all the way down and putting every unit there. This repository builds those, checks the agreement rule holds, and uses them as the starting point of every picture that follows.

Second, and this is the move the whole part turns on: **a weighting is built entirely out of finite data**. At each stage it is a finite list of whole numbers. Nothing about it requires limits, completeness, convergence, or any of the apparatus that made the original problem hard. The infinite sum has been rebuilt out of finite bookkeeping.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/02.html)** to place weights, refine, and watch the agreement rule refuse an inconsistent split.

---

[← Sums with nowhere to land](../01-sums-with-nowhere-to-land/README.md)  ·  [Every function is a stack of steps →](../03-stacks-of-steps/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

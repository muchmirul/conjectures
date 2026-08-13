# 1 · Sums with nowhere to land

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Part one repaired kernels and cokernels, but it did not define infinite addition. Consider the series obtained by adding 1, then 2, then 4, then 8, and continuing to double. Its partial sums are 1, 3, 7, 15, 31, and so on. With ordinary distance, these values move farther and farther away, so the series does not converge.

Now use a different measure of size. Fix the number two and declare an integer to be smaller when it is divisible by a larger power of two. Under this rule, 16 is smaller than 4, and 1024 is smaller than 16. This is the 2-adic absolute value, the notion of size carried by the base-two probe from part one.

![The running totals of the doubling sum, drawn twice: running away on the ordinary ruler, and closing in on a single point in the base-two probe](padic_walk.gif)

The same partial sums now have a different behaviour. Consecutive gaps are 2, 4, 8, and 16, which become progressively smaller in 2-adic size. The partial sums therefore settle into finer and finer boxes of the base-two probe. The animation places this convergence beside their divergence on the ordinary real line.

![The distance from each running total to the limit, measured the ordinary way and the base-two way, one climbing and one halving](distance.png)

The chart uses exact arithmetic from this repository. The ordinary distance from the partial sum to minus one doubles at each step, while its 2-adic distance halves. Thus, in the 2-adic number system, the series converges to minus one. There is no contradiction: convergence depends on the chosen notion of distance, and the ordinary and 2-adic distances are different.

This example identifies what an infinite sum needs in addition to its terms. It needs a rule that says when partial sums are close and what their limit should be. In other words, infinite addition depends on topology or an equivalent completion rule. Condensed sets already carry topological information inside their responses to probes, so the next task is to express summation through those responses rather than by adding an external topology again.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/01.html)** to change the base and compare the ordinary and base-p distances of the same partial sums.

---

[← Start here](../00-start-here/README.md)  ·  [Weights that agree →](../02-weights-that-agree/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

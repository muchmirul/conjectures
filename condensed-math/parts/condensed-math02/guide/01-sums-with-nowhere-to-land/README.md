# 1 · Sums with nowhere to land

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Part one repaired kernels and cokernels, but it did not define infinite addition. Consider the series obtained by adding 1, then 2, then 4, then 8, and continuing to double. Its partial sums are 1, 3, 7, 15, 31, and so on. With ordinary distance, these values move farther and farther away, so the series does not converge.

Now use a different measure of size. Fix the number two and declare an integer to be smaller when it is divisible by a larger power of two. Under this rule, 16 is smaller than 4, and 1024 is smaller than 16. This is the 2-adic absolute value, the notion of size carried by the base-two probe from part one.

![Partial sums grow without bound in ordinary distance but enter successively smaller nested regions in 2-adic distance](padic_walk.gif)

The same partial sums now have a different behaviour. Consecutive gaps are 2, 4, 8, and 16, which become progressively smaller in 2-adic size. The partial sums therefore settle into finer and finer boxes of the base-two probe. The animation places this convergence beside their divergence on the ordinary real line.

![A logarithmic chart shows ordinary error doubling and 2-adic error halving with each added term](distance.png)

The chart uses exact arithmetic from this repository. The ordinary distance from the partial sum to minus one doubles at each step, while its 2-adic distance halves. Thus, in the 2-adic number system, the series converges to minus one. There is no contradiction: convergence depends on the chosen notion of distance, and the ordinary and 2-adic distances are different.

This example identifies what an infinite sum needs in addition to its terms. It needs a rule that says when partial sums are close and what their limit should be. In other words, infinite addition depends on topology or an equivalent completion rule. Condensed sets already carry topological information inside their responses to probes, so the next task is to express summation through those responses rather than by adding an external topology again.

### The mathematics

The convergence problem that opens [Lecture V, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) can be seen in a geometric series. For an integer base $p\ge2$, the first $n$ terms form a finite sum, and the same algebraic identity gives its limit in the $p$-adic numbers:

```math
s_n=\sum_{k=0}^{n-1}p^k=\frac{p^n-1}{p-1},
\qquad
s_n-\frac{1}{1-p}=\frac{p^n}{p-1},
\qquad
s_n\xrightarrow[n\to\infty]{\,p\text{-adic}\,}\frac{1}{1-p}.
```

The base-two case gives the example used in the pictures. Its limit is

```math
1+2+4+8+\cdots=-1\quad\text{in }\mathbb Z_2.
```

**Reading the symbols.** The integer $p$ is the chosen base and is at least two. The symbol $s_n$ names the running total after $n$ terms. The summation sign adds $p^k$ as the exponent $k$ runs from zero to $n-1$. The fractions are ordinary algebraic rearrangements of that finite sum. The long arrow says that $s_n$ converges as $n$ tends to infinity when distance is measured $p$-adically. The dots mean that the powers continue forever. The symbol $\mathbb Z_2$ means the 2-adic integers, not the ordinary integers.

**Why it matters.** The error is a multiple of $p^n$, so its $p$-adic size is $p^{-n}$ and tends to zero. Its ordinary size grows instead. The terms alone therefore do not determine convergence; the chosen completion does.

**In the simulation.** The base control chooses $p$, and the terms control chooses $n$. The ordinary panel shows $s_n$ growing. The nested panel shows the $p$-adic error shrinking toward $1/(1-p)$, which equals minus one when $p=2$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/01.html)** to change the base and compare the ordinary and base-p distances of the same partial sums.

---

[← Start here](../00-start-here/README.md)  ·  [Weights that agree →](../02-weights-that-agree/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

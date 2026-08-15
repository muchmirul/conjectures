# 1 · One series, two ideas of distance

*Part 2 of three: Giving Infinite Sums a Meaning. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Consider the series that begins with 1 and then keeps doubling: 1, 2, 4, 8, and so on. Its partial sums are 1, 3, 7, 15, and 31. Under the usual distance, these totals grow without bound, so the series does not converge.

Now choose an integer $p$ and use a different measure of size. A number is small when it is divisible by a high power of $p$. For $p=2$, this makes 1024 smaller than 16, and 16 smaller than 4. This rule is the **2-adic absolute value**.

![The same partial sums move away on the usual number line but enter smaller nested regions in 2-adic distance](padic_walk.gif)

Under 2-adic distance, the gaps between successive partial sums are 2, 4, 8, 16, and so on. Each new gap is smaller than the previous one because it has another factor of two. The partial sums settle into smaller and smaller regions of the base-two probe even while they grow on the usual real line.

![A logarithmic chart shows the usual error increasing and the 2-adic error decreasing](distance.png)

The calculation uses exact arithmetic. The usual distance from a partial sum to minus one doubles after each term. Its 2-adic distance to minus one is cut in half. The series therefore converges to minus one in the 2-adic integers. It still diverges under the usual distance, and there is no contradiction because the two distances define different notions of convergence.

This example shows that a list of terms does not determine the value of an infinite sum. We also need a completion rule that says when the partial sums become close and what their limit is. Condensed sets already carry topological information through probes, so we will express this rule using probe data rather than adding a separate topology afterward.

### The mathematics

The motivation at the start of [Lecture V, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) can be illustrated by a geometric series. Let $p\ge2$. The sum of the first $n$ terms and its $p$-adic limit satisfy

```math
s_n=\sum_{k=0}^{n-1}p^k=\frac{p^n-1}{p-1},
\qquad
s_n-\frac{1}{1-p}=\frac{p^n}{p-1},
\qquad
s_n\xrightarrow[n\to\infty]{\,p\text{-adic}\,}\frac{1}{1-p}.
```

For $p=2$, this becomes

```math
1+2+4+8+\cdots=-1\quad\text{in }\mathbb Z_2.
```

**Reading the symbols.** The integer $p$ is the chosen base and is at least two. The symbol $s_n$ means the total after $n$ terms. The summation sign adds $p^k$ while $k$ runs from zero to $n-1$. The fractions are algebraic forms of the same finite sum and its error. The long arrow says that $s_n$ converges as $n$ tends to infinity when distance is measured $p$-adically. The dots mean that the powers continue forever. The symbol $\mathbb Z_2$ means the 2-adic integers.

**Why it matters.** The error contains a factor $p^n$, so its $p$-adic size is $p^{-n}$ and approaches zero. Its usual size increases instead. The chosen completion, not just the terms, determines whether the series converges.

**In the simulation.** The base control chooses $p$, and the term control chooses $n$. One panel shows $s_n$ growing under ordinary distance. The nested panel shows its $p$-adic error shrinking toward $1/(1-p)$, which is minus one when $p=2$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/01.html)** to change the base and compare both distances for the same partial sums.

---

[← Start here](../00-start-here/README.md)  ·  [Compatible weights on a probe →](../02-weights-that-agree/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

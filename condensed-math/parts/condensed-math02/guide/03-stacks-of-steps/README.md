# 3 · A basis for integer-valued functions

*Part 2 of three: Giving Infinite Sums a Meaning. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We next study continuous functions from a probe to the integers. Different integers are separated from one another. Because the probe is compact, a continuous integer-valued function must become constant on every box at some finite stage. We can then read it as a finite list of integers.

![Indicator functions are added one box at a time until they reproduce the chosen integer-valued function](steps.gif)

At one finite stage, define one **indicator function** for each box. It equals one on that box and zero on all the others. Multiplying these functions by integers and adding them reproduces any integer-valued function on the stage. The animation builds the chosen function in this way.

The stronger statement covers all stages at once. The continuous integer-valued functions on a complete profinite probe form an abelian group under addition. Nöbeling's theorem says that this group is free. In other words, it has a basis such that every function has one unique expression using finitely many basis functions and integer coefficients.

![For each tested finite stage, the number of constructed basis elements equals the number of boxes](basis_size.png)

Nöbeling extended earlier work by Specker, and the lectures present a proof due to Bergman ([Theorem 5.4, page 34](https://arxiv.org/pdf/2605.03658v1#page=34)). The code follows the construction at finite stages. It keeps a new indicator product only when the functions already selected cannot generate it. The tests then verify that the selected functions form a basis.

This finite calculation is only an illustration. Every group of functions on one finite set is automatically free. Nöbeling's theorem says something deeper: the full group of continuous functions on the infinite probe is also free. We quote that theorem from the lectures rather than claiming that a finite test proves it.

### The mathematics

[Nöbeling's theorem, Theorem 5.4 on page 34 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=34), states

```math
C(S,\mathbb Z)\cong\bigoplus_{e\in E}\mathbb Z e.
```

Thus every $f\in C(S,\mathbb Z)$ has one finite expression. The display below records the basis elements and coefficients used for that function:

```math
f=\sum_{e\in F}n_e e,
\qquad F\subset E\text{ finite},
\qquad n_e\in\mathbb Z.
```

**Reading the symbols.** The group $C(S,\mathbb Z)$ contains the continuous integer-valued functions on $S$. The set $E$ is a basis. The direct sum $\bigoplus$ means that each function uses only finitely many basis elements. The expression $\mathbb Z e$ means all integer multiples of $e$. The letter $f$ names one function. The finite subset $F$ lists the basis functions used to build it, and $n_e$ is the integer coefficient of $e$. The symbol $\in$ means “belongs to,” and $\subset$ means “is a subset of.”

**Why it matters.** A measure can be viewed as an additive map from $C(S,\mathbb Z)$ to $\mathbb Z$. Once this function group has a basis, such a map is determined by an independent integer value on each basis element. This gives the product description in the next chapter.

**In the simulation.** The target control chooses a function $f$ on one finite stage. Adding basis functions enlarges $F$. Each filled bar shows a term $n_e e$. The reconstruction is complete when their sum equals $f$ on every box. This demonstrates the finite case only.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/03.html)** to rebuild an integer-valued function from indicator functions.

---

[← Compatible weights on a probe](../02-weights-that-agree/README.md)  ·  [Products and direct sums →](../04-products-in-sums-out/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

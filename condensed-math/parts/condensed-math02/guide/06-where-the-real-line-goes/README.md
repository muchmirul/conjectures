# 6 · Why the usual real line disappears

*Part 2 of three: Giving Infinite Sums a Meaning. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Derived solidification sends the usual additive real line to zero ([Corollary 6.1 (iii), page 42](https://arxiv.org/pdf/2605.03658v1#page=42)). A divisibility argument explains the main obstruction, although the full proof needs an additional derived calculation.

![Repeated division stays inside the real numbers but eventually leaves the integers](divisible.gif)

Every real number can be divided by any positive integer and remain a real number. A group with this property is called **divisible**. The integers are not divisible because, for example, one divided by two is not an integer.

Consider an additive map from the real numbers to the integers. A real number is divisible by every positive integer, and an additive map preserves those divisibility relations. Its image would have to be an integer divisible by every positive integer. Only zero has that property, so every such map is zero. The same argument works one coordinate at a time for a product of integer groups.

![Every coordinate of a map from the divisible real group into an integer product is forced to be zero](no_map.png)

This argument proves that the real line maps trivially into the projective building blocks of the solid category. It does not by itself prove that derived solidification sends the real line to zero. The complete result also uses the universal-resolution calculation in [Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25).

The result does not say that real analysis is unimportant. The solid rule in this part is based on integer-valued measures and suits nonarchimedean sizes such as the $p$-adic absolute value. The usual real absolute value behaves differently, as the lectures note when introducing solidity ([page 33](https://arxiv.org/pdf/2605.03658v1#page=33)). Part three introduces a separate real-valued theory of measures.

The vanishing also has a use. Real-valued correction terms disappear in some condensed calculations instead of creating additional obstructions. Lecture IV uses this fact in the calculation that supports the structure theorem for solid groups.

### The mathematics

An abelian group $D$ is divisible if every element can be divided by every positive integer. In symbols, this means

```math
\forall x\in D,\ \forall n\ge1,\ \exists y\in D\text{ such that }ny=x.
```

Every homomorphism from a divisible group to a product of integer groups is zero:

```math
\operatorname{Hom}\!\left(D,\prod_{i\in I}\mathbb Z\right)=0.
```

The usual additive real line is divisible, but the lectures prove a stronger result than the homomorphism calculation alone. [Corollary 6.1 (iii), page 42 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=42) gives

```math
\mathbb R^{L\blacksquare}=0.
```

**Reading the symbols.** The letter $D$ names an abelian group. The symbols $\forall$ and $\exists$ mean “for every” and “there exists.” The relation $x\in D$ says that $x$ belongs to $D$, while $n\ge1$ chooses any positive integer. The equation $ny=x$ means that adding $y$ to itself $n$ times gives $x$. The product has one integer group for each label in $I$. The equation $\operatorname{Hom}=0$ means that every additive map to this product is the zero map. The superscript $L\blacksquare$ means derived solidification, and the final $0$ is the zero object.

**Why it matters.** Divisibility explains why the reals have no nonzero map to the compact projective generators of solid groups. The stronger equation $\mathbb R^{L\blacksquare}=0$ also relies on [Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25), so the arithmetic argument explains the obstruction without claiming to prove the corollary.

**In the simulation.** Choose a group $D$ and increase the divisor $n$. The real line always contains $y=x/n$, while the integers eventually do not. The final readout shows what this implies for a map into one integer coordinate.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/06.html)** to compare repeated division in the reals, integers, and $p$-adic examples.

---

[← The unique-extension rule](../05-the-solid-rule/README.md)  ·  [Completed tensor products →](../07-the-multiplication-table/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

# 5 · The unique-extension rule

*Part 2 of three: Giving Infinite Sums a Meaning. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We can now define a **solid abelian group**. Start with a map from the points of a probe into a condensed group. Each point gives a Dirac measure, but the probe also has general compatible integer measures. The group is solid when every point map extends in exactly one way to all these measures.

![Values assigned to probe points extend to one map on every compatible measure](extension.gif)

Existence means that every compatible measure can be integrated in the group. Uniqueness means that the values on points cannot lead to two different results. Together, these requirements make summation part of the group's structure rather than an extra choice for each infinite expression.

The lectures give the definition in [Definition 5.1, page 33](https://arxiv.org/pdf/2605.03658v1#page=33). They then prove that solid groups form an abelian category closed under limits, colimits, and extensions. Products of copies of $\mathbb Z$ are compact projective generators. In addition, every condensed abelian group has a **solidification**, which is the universal map from that group into the solid setting. These facts come from [Theorem 5.8, page 35](https://arxiv.org/pdf/2605.03658v1#page=35) and [Corollary 6.1, page 42](https://arxiv.org/pdf/2605.03658v1#page=42).

![Sample groups are marked according to whether point maps extend uniquely to compatible measures](solid_or_not.png)

The integers are solid, as is every product of copies of the integers. The $p$-adic integers and formal power-series groups are also solid. A direct sum of infinitely many integer groups is not solid because it does not contain every needed infinite coordinate family. The usual real numbers also fail this integer-based rule, for a different reason explained next.

### The mathematics

[Definition 5.1, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) says that a condensed abelian group $A$ is solid when every point map extends uniquely:

```math
\forall S,\quad
\operatorname{Hom}(\mathbb Z[S]^{\blacksquare},A)
\xrightarrow{\sim}
\operatorname{Hom}(\mathbb Z[S],A).
```

[Theorem 5.8, page 35](https://arxiv.org/pdf/2605.03658v1#page=35) provides universal solidification:

```math
(-)^{\blacksquare}:\operatorname{Cond}(\mathrm{Ab})\longrightarrow\operatorname{Solid},
\qquad
\operatorname{Hom}_{\operatorname{Solid}}(M^{\blacksquare},A)
\cong
\operatorname{Hom}_{\operatorname{Cond}(\mathrm{Ab})}(M,A).
```

**Reading the symbols.** The phrase $\forall S$ means “for every profinite probe $S$.” The group $\mathbb Z[S]$ is the free condensed group on the points of $S$, and the black square gives its free solid completion. The arrow marked $\sim$ is a bijection. It says that restricting a map from all compatible measures to the point measures loses no information and introduces no choice. The functor $(-)^{\blacksquare}$ sends a condensed abelian group $M$ to its solidification $M^{\blacksquare}$. The notation $\operatorname{Solid}$ names the category of solid groups, and $\operatorname{Cond}(\mathrm{Ab})$ names condensed abelian groups. The second line is the universal property: maps from $M^{\blacksquare}$ to a solid group $A$ are the same as maps from $M$ to $A$.

**Why it matters.** The first bijection combines the existence and uniqueness of integration. The theorem creates a universal way to turn any condensed group into a solid one and gives the solid category the algebraic closure properties needed later.

**In the simulation.** Selecting a group chooses $A$. A green result means that every point map in the listed example has one extension. A red result reports a failure of existence or uniqueness. The examples use the cited theorems; the finite activity does not prove those theorems.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/05.html)** to compare familiar groups and read why each one passes or fails the solid rule.

---

[← Products and direct sums](../04-products-in-sums-out/README.md)  ·  [Why the usual real line disappears →](../06-where-the-real-line-goes/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

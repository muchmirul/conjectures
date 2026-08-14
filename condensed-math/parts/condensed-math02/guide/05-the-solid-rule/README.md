# 5 · The solid rule

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We can now define the property that gives this part its name. The definition uses the compatible weightings from section 2 and asks whether point-level data determine how every such weighting should be integrated.

A condensed abelian group is **solid** when any map from the points of a probe into the group extends uniquely to the free solid group of weightings on that probe. Informally, once the values of individual points are known, there must be exactly one compatible way to assign a value to every integer weighting.

![A map from probe points into a group extends to a single map defined on all compatible weightings](extension.gif)

The two parts of "extends uniquely" serve different purposes. Existence ensures that every weighting described by the probe can be integrated in the group. Uniqueness ensures that the point values do not lead to two conflicting answers. Together, they make the summation rule part of the group's structure rather than an extra choice made for each series.

The lectures give this definition in one line ([Definition 5.1, page 33](https://arxiv.org/pdf/2605.03658v1#page=33)) and then establish the structure of the resulting category. The main conclusions needed here can be summarized as follows:

> Solid groups form an abelian category closed under limits, colimits, and extensions. Products of copies of the integers are compact projective generators, and every condensed group has a universal solidification.

This statement combines Theorem 5.8 ([page 35](https://arxiv.org/pdf/2605.03658v1#page=35)) with Corollary 6.1 ([page 42](https://arxiv.org/pdf/2605.03658v1#page=42)). The word **universal** means that the map to the solidification factors uniquely through every other map from the original group to a solid group. Compact projective generators are equally practical: maps from the products in section 4 detect objects and help build the rest of the solid category.

![Six sample groups are shown with a pass or fail result for the unique-extension condition](solid_or_not.png)

The figure classifies several recurring examples. The integers are solid, as is every product of copies of the integers. The p-adic integers and formal power-series groups are also solid. The usual real numbers are not solid under this integer-based rule, and understanding that failure will prepare us for the different rule introduced in part three.

### The mathematics

[Definition 5.1, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) says that a condensed abelian group $A$ is solid exactly when every map from a probe extends uniquely:

```math
\forall S,\quad
\operatorname{Hom}(\mathbb Z[S]^{\blacksquare},A)
\xrightarrow{\sim}
\operatorname{Hom}(\mathbb Z[S],A).
```

[Theorem 5.8, page 35](https://arxiv.org/pdf/2605.03658v1#page=35) supplies the universal solidification

```math
(-)^{\blacksquare}:\operatorname{Cond}(\mathrm{Ab})\longrightarrow\operatorname{Solid},
\qquad
\operatorname{Hom}_{\operatorname{Solid}}(M^{\blacksquare},A)
\cong
\operatorname{Hom}_{\operatorname{Cond}(\mathrm{Ab})}(M,A).
```

**Reading the symbols.** The phrase $\forall S$ means “for every profinite probe $S$.” The group $\mathbb Z[S]$ is the free condensed group on its points, and the black square gives its free solid completion. The arrow marked $\sim$ is a bijection: restricting a map from all weightings to the point weights loses no choices and creates none. The functor $(-)^{\blacksquare}$ sends any condensed abelian group $M$ to its solidification $M^{\blacksquare}$. The notation $\operatorname{Solid}$ names the category of solid groups, while $\operatorname{Cond}(\mathrm{Ab})$ names condensed abelian groups. The second line is the universal property: maps from the solidification to a solid group $A$ are the same as maps from $M$ itself.

**Why it matters.** The first bijection combines existence and uniqueness of integration. The theorem says that solid groups form an abelian category closed under limits, colimits, and extensions, with products of copies of $\mathbb Z$ as compact projective generators.

**In the simulation.** Selecting a group chooses $A$. A green result means the point map on the right has one extension on the left. A red result marks a failure of existence or uniqueness. The activity illustrates listed examples; the categorical theorem is quoted from the lectures.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/05.html)** to compare sample groups and see which requirement supports each solidity verdict.

---

[← Products in, sums out](../04-products-in-sums-out/README.md)  ·  [Where the real line goes →](../06-where-the-real-line-goes/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

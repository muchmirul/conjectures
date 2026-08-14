# 4 · Products in, sums out

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Nöbeling's theorem lets us describe weightings by comparing two ways to store an infinite family of integers. A **product** is an unlimited row of integer dials. Every dial can be set independently, and infinitely many of them may be nonzero. A **direct sum** uses the same row but allows only finitely many nonzero dials in any one element. This finite-support condition creates an important duality between the two constructions.

![A product allows nonzero entries across an unlimited row, while a direct sum has only finitely many nonzero entries](product_sum.png)

A homomorphism from a product to the integers cannot depend on infinitely many dials. Although one might try to assign a coefficient to every position, Specker's theorem says that every additive map reads only finitely many coordinates. Therefore, the collection of homomorphisms from a product is a direct sum of copies of the integers.

![A homomorphism reads a finite initial group of coordinates and ignores all later coordinates in the product](finite_reach.gif)

The underlying obstruction comes from divisibility. Data placed sufficiently far along the row can be arranged to be divisible by arbitrarily high powers of an integer. Any output that respects all those divisions would have to be divisible by every such power, and the only integer with that property is zero. Specker's proof makes this argument precise; the theorem is quoted here rather than reproduced.

A homomorphism from a direct sum behaves in the opposite way. Because each input has finite support, one may choose an independent integer coefficient for every dial without creating an infinite numerical sum. The collection of homomorphisms from a direct sum is therefore a product.

This applies directly to measures. By Nöbeling's theorem, the continuous integer-valued functions on a probe form a free group, so they are a direct sum of copies of the integers indexed by a basis. A weighting is exactly an integer-valued homomorphism on this function group, obtained by integration. Taking the homomorphisms turns that direct sum into a product:

> Every collection of weightings on a probe is an endless product of copies of the whole numbers.

This is Corollary 5.5 of the lectures ([page 34](https://arxiv.org/pdf/2605.03658v1#page=34)). The branching pattern of the probe determines the indexing set, but once a basis is chosen, every weighting is represented by an unrestricted row of integer coordinates. These products will become the basic projective building blocks of solid groups.

### The mathematics

Products and direct sums exchange roles under integer duality. Specker's theorem and [Corollary 5.5, page 34 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=34) give the two descriptions

```math
\operatorname{Hom}_{\mathrm{Ab}}\!\left(
\prod_{n\in\mathbb N}\mathbb Z,\mathbb Z\right)
\cong\bigoplus_{n\in\mathbb N}\mathbb Z,
\qquad
\operatorname{Hom}_{\mathrm{Ab}}\!\left(
\bigoplus_{i\in I}\mathbb Z,\mathbb Z\right)
\cong\prod_{i\in I}\mathbb Z.
```

The index set depends on the probe $S$. Consequently, for some such set $I$,

```math
\mathbb Z[S]^{\blacksquare}\cong\prod_{i\in I}\mathbb Z.
```

**Reading the symbols.** The notation $\operatorname{Hom}_{\mathrm{Ab}}$ means additive maps of ordinary abelian groups. The first product has one coordinate for each natural number $n\in\mathbb N$. The more general index set in the second formula is $I$. A product $\prod$ allows an integer in every coordinate, including infinitely many nonzero entries. A direct sum $\bigoplus$ allows only finitely many nonzero entries. Specker's theorem is the first isomorphism: an integer-valued homomorphism on a countable product reads only finitely many coordinates. The second isomorphism says that a homomorphism on a direct sum may choose one coefficient for every coordinate. The black square on $\mathbb Z[S]^{\blacksquare}$ marks the free solid group on $S$. The next displayed isomorphism follows by applying the second duality to Nöbeling's basis of $C(S,\mathbb Z)$.

**Why it matters.** Nöbeling makes $C(S,\mathbb Z)$ a direct sum of copies of $\mathbb Z$. Taking its integer dual changes that direct sum into the product displayed above. Products of integer groups are therefore the basic free objects of solid mathematics.

**In the simulation.** The reach control chooses the finite set of coordinates used by one homomorphism in Specker's formula. Moving a coordinate outside that set leaves the output unchanged. The endless row represents the countable product, while the finite reach represents its direct-sum dual.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/04.html)** to compare products with direct sums and test how many coordinates an integer-valued homomorphism can use.

---

[← Every function is a stack of steps](../03-stacks-of-steps/README.md)  ·  [The solid rule →](../05-the-solid-rule/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

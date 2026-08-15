# 4 · Products and direct sums

*Part 2 of three: Giving Infinite Sums a Meaning. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

There are two common ways to store a family of integers. A **product** allows an integer in every coordinate, with no limit on how many are nonzero. A **direct sum** uses the same coordinates but requires each element to have only finitely many nonzero entries.

![An infinite product allows nonzero values everywhere, while a direct sum allows only finitely many nonzero values](product_sum.png)

Specker's theorem says that an additive map from a countable product of integers to the integers can depend on only finitely many coordinates. Therefore, all such maps form a direct sum of copies of the integers.

![A homomorphism reads only a finite group of coordinates and ignores the rest of the product](finite_reach.gif)

The proof uses divisibility. Far enough along the product, one can arrange data divisible by increasingly high powers of an integer. Any output that respected all those divisibility relations would have to be divisible by every power. The only integer with that property is zero. The full proof is quoted rather than reproduced here.

Maps from a direct sum behave in the opposite way. Each input has finite support, so we may choose one coefficient for every coordinate without ever evaluating an infinite numerical sum. The group of maps from a direct sum to the integers is therefore a product.

Nöbeling's theorem says that $C(S,\mathbb Z)$ is a direct sum indexed by a basis. A measure is an integer-valued homomorphism on this group. Taking all such homomorphisms changes the direct sum into a product. This is [Corollary 5.5, page 34](https://arxiv.org/pdf/2605.03658v1#page=34): the free solid group on a probe is a product of copies of the integers. These products will serve as the basic projective objects in the category of solid groups.

### The mathematics

Specker's theorem describes maps from a product to the integers. Together with [Corollary 5.5, page 34 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=34), it gives

```math
\operatorname{Hom}_{\mathrm{Ab}}\!\left(
\prod_{n\in\mathbb N}\mathbb Z,\mathbb Z\right)
\cong\bigoplus_{n\in\mathbb N}\mathbb Z,
\qquad
\operatorname{Hom}_{\mathrm{Ab}}\!\left(
\bigoplus_{i\in I}\mathbb Z,\mathbb Z\right)
\cong\prod_{i\in I}\mathbb Z.
```

The basis, and therefore its index set, depends on the probe. For the resulting index set $I$, we obtain

```math
\mathbb Z[S]^{\blacksquare}\cong\prod_{i\in I}\mathbb Z.
```

**Reading the symbols.** The notation $\operatorname{Hom}_{\mathrm{Ab}}$ means additive maps of abelian groups. The first product has one coordinate for each natural number $n\in\mathbb N$. The letter $I$ is a general index set. A product $\prod$ permits infinitely many nonzero coordinates. A direct sum $\bigoplus$ permits only finitely many. The first isomorphism says that a homomorphism from a countable product to $\mathbb Z$ reads only finitely many coordinates. The second says that a homomorphism from a direct sum may choose one coefficient for every coordinate. The black square on $\mathbb Z[S]^{\blacksquare}$ marks the free solid group on $S$.

**Why it matters.** Nöbeling's theorem writes the function group as a direct sum. Taking its integer dual turns that direct sum into the product shown above. Products of integer groups are therefore the basic free objects for solid mathematics.

**In the simulation.** The reach control chooses the finite set of coordinates read by one homomorphism. Changing a coordinate inside that set can change the output. Changing one outside it cannot. The finite model illustrates Specker's conclusion but does not prove the infinite theorem.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/04.html)** to change coordinates inside and outside a homomorphism's finite range.

---

[← A basis for integer-valued functions](../03-stacks-of-steps/README.md)  ·  [The unique-extension rule →](../05-the-solid-rule/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

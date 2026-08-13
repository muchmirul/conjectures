# 4 · Products in, sums out

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Nöbeling's theorem lets us describe weightings by comparing two ways to store an infinite family of integers. A **product** is an unlimited row of integer dials. Every dial can be set independently, and infinitely many of them may be nonzero. A **direct sum** uses the same row but allows only finitely many nonzero dials in any one element. This finite-support condition creates an important duality between the two constructions.

![An endless row of dials with every dial set, beside the same row where all but a few dials are blank](product_sum.png)

A homomorphism from a product to the integers cannot depend on infinitely many dials. Although one might try to assign a coefficient to every position, Specker's theorem says that every additive map reads only finitely many coordinates. Therefore, the collection of homomorphisms from a product is a direct sum of copies of the integers.

![A reader scanning along an endless row of dials and coming to a halt after finitely many, because no legal question can reach further](finite_reach.gif)

The underlying obstruction comes from divisibility. Data placed sufficiently far along the row can be arranged to be divisible by arbitrarily high powers of an integer. Any output that respects all those divisions would have to be divisible by every such power, and the only integer with that property is zero. Specker's proof makes this argument precise; the theorem is quoted here rather than reproduced.

A homomorphism from a direct sum behaves in the opposite way. Because each input has finite support, one may choose an independent integer coefficient for every dial without creating an infinite numerical sum. The collection of homomorphisms from a direct sum is therefore a product.

This applies directly to measures. By Nöbeling's theorem, the continuous integer-valued functions on a probe form a free group, so they are a direct sum of copies of the integers indexed by a basis. A weighting is exactly an integer-valued homomorphism on this function group, obtained by integration. Taking the homomorphisms turns that direct sum into a product:

> Every collection of weightings on a probe is an endless product of copies of the whole numbers.

This is Corollary 5.5 of the lectures ([page 34](https://arxiv.org/pdf/2605.03658v1#page=34)). The branching pattern of the probe determines the indexing set, but once a basis is chosen, every weighting is represented by an unrestricted row of integer coordinates. These products will become the basic projective building blocks of solid groups.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/04.html)** to compare products with direct sums and test how many coordinates an integer-valued homomorphism can use.

---

[← Every function is a stack of steps](../03-stacks-of-steps/README.md)  ·  [The solid rule →](../05-the-solid-rule/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

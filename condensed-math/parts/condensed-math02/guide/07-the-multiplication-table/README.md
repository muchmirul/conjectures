# 7 · The multiplication table

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The category of solid groups has a product operation called the **completed tensor product**. It combines two solid groups into a third group that represents additive operations depending on one input from each side. The examples below show that this product remembers which completion, or adic topology, each group carries.

![A table lists completed tensor products for p-adic groups, power-series groups, integers, and reals](tensor_table.png)

Read the grid by choosing one label from its row and one from its column. The 2-adic integers tensored with the 3-adic integers give zero, while the 2-adic integers tensored with themselves return the 2-adic integers. Combining the 2-adic integers with the real numbers also gives zero, consistent with section 6. Combining power series in one variable with power series in another produces power series in both variables.

![Nested scales based on powers of two and powers of three are compared without a common completion direction](rulers.gif)

The animation gives an intuition for the mixed 2-adic and 3-adic entry. The 2-adic completion is organized by divisibility by powers of two, while the 3-adic completion is organized by powers of three. In the 2-adic setting, three is invertible and does not produce a finer scale; in the 3-adic setting, the same is true of two. The two scales are therefore incompatible. The picture illustrates the exact vanishing stated in the table, but does not prove it.

The lectures describe the general pattern by saying that the completed tensor product asks which adic topologies the two factors carry and retains the compatible ones ([Example 6.4, page 44](https://arxiv.org/pdf/2605.03658v1#page=44)). Matching completions reinforce one another, while incompatible completions can give zero. The table is a set of precise instances of that rule.

The power-series entry can also be understood through the coordinates from section 4. A one-variable power series has one coefficient for each nonnegative power of its variable. Combining two such products gives coordinates indexed by pairs of powers ([Proposition 6.3, page 43](https://arxiv.org/pdf/2605.03658v1#page=43)). A pair of powers is exactly a monomial in two variables, so the resulting coordinate system is the group of two-variable power series. The repository tests this indexing argument; the remaining table entries are quoted from the lectures.

### The mathematics

[Proposition 6.3, page 43 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=43) states that completed tensor product multiplies the coordinate sets of integer products:

```math
\left(\prod_{i\in I}\mathbb Z\right)\otimes^{L}_{\blacksquare}
\left(\prod_{j\in J}\mathbb Z\right)
\cong
\prod_{(i,j)\in I\times J}\mathbb Z.
```

[Example 6.4, page 44](https://arxiv.org/pdf/2605.03658v1#page=44) lists the concrete identities for distinct primes $p\neq\ell$:

```math
\mathbb Z_p\otimes^{L}_{\blacksquare}\mathbb R=0,
\quad
\mathbb Z_p\otimes^{L}_{\blacksquare}\mathbb Z_\ell=0,
\quad
\mathbb Z_p\otimes^{L}_{\blacksquare}\mathbb Z_p\cong\mathbb Z_p,
```

```math
\mathbb Z_p\otimes^{L}_{\blacksquare}\mathbb Z[[T]]\cong\mathbb Z_p[[T]],
\qquad
\mathbb Z[[U]]\otimes^{L}_{\blacksquare}\mathbb Z[[T]]
\cong\mathbb Z[[U,T]].
```

**Reading the symbols.** The sets $I$ and $J$ index the two rows of integer coordinates, and $I\times J$ is the set of ordered pairs of indices. The product signs allow unrestricted coordinates. The symbol $\otimes^{L}_{\blacksquare}$ is the derived solid tensor product from [Theorem 6.2, page 43](https://arxiv.org/pdf/2605.03658v1#page=43). The groups $\mathbb Z_p$ and $\mathbb Z_\ell$ are the $p$-adic and $\ell$-adic integers for distinct primes. The notation $\mathbb Z[[T]]$ means formal power series in $T$, and $\mathbb Z[[U,T]]$ means formal power series in both variables. The symbol $0$ is the zero object, and $\cong$ means isomorphic.

**Why it matters.** Compatible completion directions survive together, while incompatible prime directions produce zero. Pairing the coefficient indices of a series in $U$ with those of a series in $T$ gives exactly the monomials of a two-variable series.

**In the simulation.** The row and column selectors choose the two tensor factors. The highlighted cell reports the corresponding identity. The nested rulers visualize the completion directions, while the readout marks whether an entry is stated directly in Example 6.4 or obtained by the same coordinate rule.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/07.html)** to select two solid groups and inspect the completion rule behind their tensor product.

---

[← Where the real line goes](../06-where-the-real-line-goes/README.md)  ·  [Solidify a shape, get its holes →](../08-solidify-a-shape/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

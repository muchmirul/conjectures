# 7 · Completed tensor products

*Part 2 of three: Giving Infinite Sums a Meaning. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Solid groups have a product operation called the **completed tensor product**. It combines two solid groups while keeping track of the completion carried by each one. The resulting group represents additive operations that depend on one input from each side.

![A table gives completed tensor products of integer, p-adic, power-series, and real groups](tensor_table.png)

Choose one group from a row and another from a column. The 2-adic integers tensored with the 3-adic integers give zero. The 2-adic integers tensored with themselves give the 2-adic integers again. Tensoring the 2-adic integers with the real numbers also gives zero, in agreement with chapter 6. Two one-variable power-series groups combine into a two-variable power-series group.

![Scales formed from powers of two and powers of three do not share a common direction of completion](rulers.gif)

The mixed 2-adic and 3-adic case can be understood through their scales. The 2-adic completion uses divisibility by powers of two. In that setting, three is invertible and does not define a finer scale. The 3-adic completion reverses these roles. The two completion directions are incompatible. The picture illustrates the vanishing in [Example 6.4, page 44](https://arxiv.org/pdf/2605.03658v1#page=44), but it is not a proof.

For power series, a series in $U$ has one coordinate for every nonnegative power of $U$, and a series in $T$ has one for every nonnegative power of $T$. Pairing the coordinate sets gives one coordinate for every pair of powers. Such a pair is a monomial in $U$ and $T$, so the result is a two-variable power series ([Proposition 6.3, page 43](https://arxiv.org/pdf/2605.03658v1#page=43)). The repository tests this indexing calculation. The other displayed identities are quoted from the lectures.

### The mathematics

[Proposition 6.3, page 43 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=43) states that the completed tensor product multiplies the coordinate sets of integer products:

```math
\left(\prod_{i\in I}\mathbb Z\right)\otimes^{L}_{\blacksquare}
\left(\prod_{j\in J}\mathbb Z\right)
\cong
\prod_{(i,j)\in I\times J}\mathbb Z.
```

The result depends on whether the completion directions agree. For distinct primes $p\neq\ell$, [Example 6.4, page 44](https://arxiv.org/pdf/2605.03658v1#page=44) gives

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

**Reading the symbols.** The sets $I$ and $J$ label two families of integer coordinates, and $I\times J$ is the set of ordered pairs of labels. The product signs permit unrestricted coordinates. The symbol $\otimes^{L}_{\blacksquare}$ is the derived solid tensor product from [Theorem 6.2, page 43](https://arxiv.org/pdf/2605.03658v1#page=43). The groups $\mathbb Z_p$ and $\mathbb Z_\ell$ are the $p$-adic and $\ell$-adic integers for different primes. The notation $\mathbb Z[[T]]$ means formal power series in $T$, and $\mathbb Z[[U,T]]$ means formal power series in both variables. The symbol $0$ is the zero object, and $\cong$ means isomorphic.

**Why it matters.** Compatible completion directions remain together, while incompatible prime directions give zero. For products of integer coordinates, the tensor product pairs every coordinate on one side with every coordinate on the other.

**In the simulation.** Row and column controls choose the tensor factors. The selected cell displays the corresponding identity. The readout also says whether the lectures state the entry directly or whether it follows by relabelling the coordinate rule.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/07.html)** to choose two solid groups and inspect their completed tensor product.

---

[← Why the usual real line disappears](../06-where-the-real-line-goes/README.md)  ·  [Solidification recovers homology →](../08-solidify-a-shape/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

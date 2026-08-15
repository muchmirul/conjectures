# 3 · A measure rule for the real numbers

*Part 3 of three: Measure Rules for Rings and Geometry. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The integer-based solidification from part two sends the usual real line to zero. Real analysis therefore needs a different theory of measures. A natural place to begin is with finite lists of signed real weights and a rule that bounds their size.

Choose a positive exponent $p$. At $p=1$, add the absolute values of the weights. At $p=2$, square the absolute values, add them, and take a square root. Other positive exponents use the same pattern. This is the familiar $\ell^p$ size of a finite list.

A measure on a probe must agree across stages. Passing from a fine stage to a coarse one merges boxes and adds their weights. If a fine list is within a chosen size limit, the merged list must stay within the same limit. Otherwise, the allowed regions at different stages do not form an inverse system.

![Curves for merging two, four, and nine equal boxes meet the no-growth level at exponent one](merge.png)

For equal weights, the effect can be calculated exactly. Merging does not increase size precisely when $p\le1$. Above one, the growth becomes larger as more boxes are merged. For example, joining four equal weights at $p=2$ doubles the size ([Example 7.10, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)).

![Five unit regions are convex at exponents at least one and bend inward below one](lp_balls.png)

The same boundary causes a second difficulty. At and above one, the unit region is convex. Below one, it bends inward and is not convex. Classical functional analysis is largely based on locally convex spaces, but compatibility under merging forces us to use exponents at most one.

The fixed rule at $p=1$ gives the usual bounded signed measures, but it is not an analytic ring. Ribe found an extension of complete locally convex spaces whose middle term is not locally convex, so these spaces are not stable under the extensions required by the analytic condition ([Example 7.10, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)). Choosing one fixed exponent below one does not remove the related obstruction.

The successful construction does not fix a single smaller exponent. For a target $p\le1$, it combines the measure modules for every exponent $q<p$ into a directed union, or colimit. [Theorem 7.11, page 50](https://arxiv.org/pdf/2605.03658v1#page=50) proves that this varying-exponent construction is analytic. Its complete modules are called **liquid modules**.

The restriction $p\le1$ came from a finite operation: merging child boxes adds their weights. This is a recurring feature of condensed mathematics. Compatibility between finite stages places a strong condition on the infinite analytic theory.

### The mathematics

Choose $0<p\le1$. [Example 7.10, page 49 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=49) defines the finite-stage size and measure module by

```math
\|(x_i)\|_{\ell^p}=\left(\sum_i|x_i|^p\right)^{1/p},
\qquad
\mathcal M_p[S]=\bigcup_{r>0}\varprojlim_i
\{x\in\mathbb R[S_i]\mid\|x\|_{\ell^p}\le r\}.
```

Equal weights make the effect of merging easy to calculate. For $n$ equal positive weights, the size changes by

```math
\frac{\|\text{after}\|_{\ell^p}}{\|\text{before}\|_{\ell^p}}
=n^{1-1/p}\le1\quad\Longleftrightarrow\quad p\le1.
```

No fixed $p$ gives an analytic ring. [Theorem 7.11, page 50](https://arxiv.org/pdf/2605.03658v1#page=50) instead uses all smaller exponents:

```math
\mathcal M_{<p}[S]:=\varinjlim_{q<p}\mathcal M_q[S],
\qquad
(\mathbb R,\mathcal M_{<p})\text{ is an analytic ring.}
```

**Reading the symbols.** The exponent $p$ is positive and at most one. The list $(x_i)$ contains the weights on one finite stage. The absolute-value bars measure each real weight. The summation sign adds their $p$th powers, and the outside exponent $1/p$ defines the $\ell^p$ size. The union over $r>0$ allows any finite bound. The inverse limit $\varprojlim$ requires compatibility among the stages $S_i$. The fraction compares the size after merging with the size before merging. The double arrow $\Longleftrightarrow$ means “if and only if.” The direct limit $\varinjlim_{q<p}$ combines all positive exponents $q$ below $p$. The pair $(\mathbb R,\mathcal M_{<p})$ is the real ring with this combined measure rule.

**Why it matters.** Compatibility under refinement forces $p\le1$, exactly where local convexity is no longer available below the endpoint. Combining all smaller exponents gives the liquid theory that passes the analytic-ring test.

**In the simulation.** One control changes $p$, and another changes the number $n$ of merged boxes. The chart calculates $n^{1-1/p}$. A second picture shows whether the unit region is convex. These are separate conditions that meet at $p=1$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/03.html)** to find the exponent at which merging stops increasing the size.

---

[← Two analytic examples](../02-two-that-work/README.md)  ·  [Global functions and boundary tails →](../04-functions-near-the-edge/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

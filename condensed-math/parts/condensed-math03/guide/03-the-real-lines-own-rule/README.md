# 3 · The real line's own rule

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Part two's integer-based solidification sends the usual real line to zero, so real analysis needs its own theory of measures. The natural candidates are signed real-valued measures with a bound on their size. We will see that the way a probe refines places a strict limit on how that size may be defined.

For a finite list of weights, choose a positive exponent. At exponent one, size is the sum of the absolute values. At exponent two, square the absolute values, add them, and take a square root. Other exponents follow the same pattern. These are the familiar ell-p sizes, applied here to the weights on each finite stage of a probe.

A measure must be compatible between stages. Moving from a fine stage to a coarse stage merges boxes and adds their weights. If a fine-stage list has size at most a fixed bound, its merged list must satisfy the same bound. Otherwise, the bounded regions at different stages do not form an inverse system, and there is no well-defined space of measures on the full probe.

![Curves for merging two, four, and nine equal boxes cross the no-growth threshold when the exponent is one](merge.png)

The chart computes the worst effect of merging equal weights. The size after merging is no greater than the size before merging exactly when the exponent is at most one. Above one, the ratio grows with the number of merged boxes. For example, merging four equal weights at exponent two doubles the size. This forces the real theory into exponents no larger than one ([Example 7.10, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)).

![Five unit regions show convex boundaries for exponents at least one and nonconvex boundaries below one](lp_balls.png)

The same boundary creates a second problem. At exponent one and above, the unit ball is convex, so the straight segment between any two allowed points remains allowed. Below one, the unit ball caves inward and loses convexity. Classical functional analysis is largely organized around locally convex spaces, while compatibility under merging requires us to work at or below the edge of that setting.

Choosing exponent one gives the standard bounded signed measures, but the resulting pair is not an analytic ring ([Example 7.10, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)). Ribe constructed an extension of complete locally convex spaces whose middle space is not locally convex, showing that this class is not stable under the extensions required by the analytic-ring test. Fixing any one exponent below one does not solve the problem because a related obstruction persists there as well.

The successful construction avoids fixing a single lower exponent. For a target exponent p no greater than one, it collects the measures bounded for some exponent q strictly below p and identifies them compatibly as q varies. The standard name for this directed construction is a colimit.

> With the exponents swept rather than fixed, the real numbers do get a rule that works, for every target exponent up to one.

This is Theorem 7.11 ([page 50](https://arxiv.org/pdf/2605.03658v1#page=50)), whose proof belongs to the companion work cited by the lectures. Modules built from this varying-exponent real theory are called **liquid** modules. The name distinguishes this construction from the fixed integer-based solid theory of part two.

The restriction on the exponent came directly from finite refinement maps: merging boxes adds their weights. This is an important pattern in condensed mathematics. A concrete compatibility condition on finite stages determines which infinite analytic structures can exist.

### The mathematics

Choose an exponent with $0<p\le1$. [Example 7.10, page 49 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=49) defines the finite-stage size and its measure module by

```math
\|(x_i)\|_{\ell^p}=\left(\sum_i|x_i|^p\right)^{1/p},
\qquad
\mathcal M_p[S]=\bigcup_{r>0}\varprojlim_i
\{x\in\mathbb R[S_i]\mid\|x\|_{\ell^p}\le r\}.
```

The effect of merging can be calculated exactly for equal weights. Merging $n$ equal positive weights changes the size by

```math
\frac{\|\text{after}\|_{\ell^p}}{\|\text{before}\|_{\ell^p}}
=n^{1-1/p}\le1\quad\Longleftrightarrow\quad p\le1.
```

No fixed $p$ gives an analytic ring. [Theorem 7.11, page 50](https://arxiv.org/pdf/2605.03658v1#page=50) uses all smaller exponents:

```math
\mathcal M_{<p}[S]:=\varinjlim_{q<p}\mathcal M_q[S],
\qquad
(\mathbb R,\mathcal M_{<p})\text{ is an analytic ring.}
```

**Reading the symbols.** The exponent $p$ is positive and at most one. The list $(x_i)$ contains the weights on one finite stage. Absolute-value bars measure each real weight, $\sum$ adds their $p$th powers, and the outer exponent $1/p$ defines the $\ell^p$ size. The union over $r>0$ allows any finite bound, while $\varprojlim$ imposes compatibility between the stages $S_i$. The ratio compares the size after and before merging $n$ equal boxes. The double arrow $\Longleftrightarrow$ means “if and only if.” The direct-limit symbol $\varinjlim_{q<p}$ combines the theories for all positive $q$ smaller than $p$. The pair $(\mathbb R,\mathcal M_{<p})$ is the real ring with this combined rule.

**Why it matters.** Refinement forces $p\le1$, exactly the range where ordinary local convexity stops being available. Sweeping through all smaller exponents produces the liquid theory that passes the analytic-ring test.

**In the simulation.** The exponent control changes $p$, and the box control changes $n$. The chart computes $n^{1-1/p}$ live. The unit-ball picture shows convexity, while the verdict checks the separate requirement that merging must not increase size.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/03.html)** to change the exponent, merge equal weights, and locate the boundary where the size begins to increase.

---

[← Two rules that work](../02-two-that-work/README.md)  ·  [Functions near the edge →](../04-functions-near-the-edge/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

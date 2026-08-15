# 4 · The cut and glue rules

*Part 1 of three: Understanding Spaces Through Probes. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The answers for different probes must agree with one another. A condensed set follows two rules, called **cut** and **glue**. These are the two sheaf conditions in its definition.

**Cut.** Suppose a probe has two disjoint pieces. Giving one map from the whole probe is the same as giving one map from each piece. Because the pieces do not meet, we may choose their maps independently and then combine them.

![Two separate pieces each provide one independent value for the value on their union](cut.png)

**Glue.** Now suppose a larger probe covers a smaller probe. A map on the cover can come from the smaller probe only if repeated copies of the same point receive the same value. When they agree, exactly one map on the smaller probe must produce the map on the cover.

![Values on two covering pieces agree where the pieces represent the same point, then descend to one value below](glue.gif)

The glue rule requires both existence and uniqueness. Compatible local answers must produce a global answer, and the same local data cannot produce two different global answers. Together with the cut rule, this gives the definition of a condensed set ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)).

The definition also has a size detail ([Remark 1.4, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)). There are too many profinite sets to place all of them inside one ordinary set. The theory first chooses a sufficiently large size limit, works within it, and then proves that using a larger limit does not change the result. We will leave this set-theoretic bookkeeping in the background.

### The mathematics

[Definition 1.2, page 6 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=6) writes the cut rule for disjoint probes as

```math
T(S_1\sqcup S_2)\xrightarrow{\sim}T(S_1)\times T(S_2).
```

For the glue rule, begin with a surjection $q:S'\twoheadrightarrow S$ and the projections $p_1,p_2:S'\times_S S'\to S'$. Then

```math
T(S)\xrightarrow{\sim}
\{x\in T(S')\mid p_1^*x=p_2^*x\text{ in }T(S'\times_S S')\}.
```

**Reading the symbols.** The letter $T$ names a condensed set, and $T(S)$ is its set of answers on $S$. The symbol $\sqcup$ means disjoint union, and $\times$ means Cartesian product. An arrow marked $\sim$ means a bijection. The double-headed map $q$ is a cover. The fibre product $S'\times_S S'$ contains pairs of points in the cover that represent the same point below. The maps $p_1$ and $p_2$ choose the first and second point in such a pair. A star in $p_i^*$ means pullback. The braces mean “the set of,” $\in$ means “belongs to,” and the vertical bar means “such that.” The equality requires both representatives of each point to receive the same answer.

**Why it matters.** The first bijection lets us work independently on separate pieces. The second says that compatible data on a cover come from exactly one answer below. Together with $T(\varnothing)=*$, these statements define a condensed set.

**In the simulation.** In cut mode, two controls choose the independent entries of $T(S_1)\times T(S_2)$. In glue mode, they choose the two pullbacks $p_1^*x$ and $p_2^*x$. An answer appears below only when the pullbacks agree.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/04.html)** to compare independent values on separate pieces with values that must agree on a cover.

---

[← Mapping a probe into a space](../03-what-a-shape-says/README.md)  ·  [A quotient that points cannot detect →](../05-the-ghost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

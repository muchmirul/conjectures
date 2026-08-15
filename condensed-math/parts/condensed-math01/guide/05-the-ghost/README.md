# 5 · A quotient that points cannot detect

*Part 1 of three: Understanding Spaces Through Probes. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We can now return to the two real lines. Their probe data differ because a probe can vary continuously in the usual real line in ways that are impossible in the discrete line. In condensed abelian groups, we can take a cokernel of the identity map between them. Call this cokernel $Q$.

On the one-point probe, $Q$ is zero. Both real lines have the same individual values, so nothing remains after the pointwise quotient. A larger probe can give a nonzero result. It can map continuously into the usual line without being locally constant, so that map does not come from the discrete line.

![A real-valued map keeps varying as the halving probe is refined and never becomes locally constant](ghost.gif)

The animation builds a finite approximation to such a map on the halving probe. At each new stage, the values vary on smaller boxes. In the completed probe, a continuous map of this kind never becomes constant on a finite collection of boxes. Every continuous map from a compact probe to a discrete space is locally constant, so this map cannot come from the discrete real line. It represents a nonzero element of $Q$ ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)).

This example explains the earlier failure. Individual points could not see the quotient, but a family of nearby points could. Condensed mathematics keeps that missing information as an ordinary algebraic object.

The general theorem says that condensed abelian groups form an abelian category ([Theorem 1.10, page 9](https://arxiv.org/pdf/2605.03658v1#page=9), with the size limit fixed in [Theorem 2.2, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)). Kernels, cokernels, and exact sequences therefore work together in the expected way.

### The mathematics

[Example 1.9, page 9 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=9) identifies the condensed cokernel $Q$ by

```math
Q(S)=C(S,\mathbb{R})/C_{\mathrm{lc}}(S,\mathbb{R}),
\qquad Q(*)=0,
\qquad Q\neq0.
```

The surrounding theorem gives the category in which this cokernel behaves correctly. [Theorem 1.10, page 9](https://arxiv.org/pdf/2605.03658v1#page=9) states, in particular, that

```math
\operatorname{Cond}(\mathrm{Ab})\text{ is an abelian category.}
```

**Reading the symbols.** The letter $Q$ names the cokernel, and $Q(S)$ is what the probe $S$ detects. The notation $C(S,\mathbb{R})$ means continuous real-valued maps. The subscript $\mathrm{lc}$ restricts the denominator to locally constant maps. The slash forms the quotient. The star is the one-point probe. Thus $Q(*)=0$ says that one point detects nothing, while $Q\neq0$ says that the condensed group itself is not zero. The notation $\operatorname{Cond}(\mathrm{Ab})$ means condensed abelian groups. An abelian category is a setting in which kernels, cokernels, and exact sequences obey the usual algebraic rules.

**Why it matters.** A continuous map that is not locally constant gives a nonzero class in $Q(S)$ even though every class vanishes on the one-point probe. The formula shows exactly which information pointwise algebra had discarded.

**In the simulation.** The variation control changes a map in $C(S,\mathbb{R})$. At zero variation, the map is locally constant and gives the zero class. With nonzero variation, it changes through every visible refinement and represents the kind of class that survives in $Q(S)$. The activity shows finite stages of the construction rather than proving its infinite continuation.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/05.html)** to compare a locally constant map with one that continues to vary as the probe is refined.

---

[← The cut and glue rules](../04-cut-and-glue/README.md)  ·  [Probes on which every cover splits →](../06-unfoldable-probes/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

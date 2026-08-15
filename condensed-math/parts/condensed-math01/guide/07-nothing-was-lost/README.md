# 7 · Recovering familiar spaces

*Part 1 of three: Understanding Spaces Through Probes. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Replacing a space by all its probe maps would not help if we could no longer recover ordinary spaces and their continuous maps. A comparison theorem shows that the new description preserves them for a broad and familiar class of spaces.

![Nested regions show compact Hausdorff spaces inside compactly generated spaces, which map into condensed sets](nesting.png)

Compact Hausdorff spaces correspond exactly to condensed sets with the matching compactness properties ([Theorem 2.16, page 17](https://arxiv.org/pdf/2605.03658v1#page=17)). Closed and bounded shapes in Euclidean space are standard examples. A larger class, called the compactly generated spaces, includes all metric spaces and spaces built from cells. On this class, the translation is **fully faithful**: the maps between the condensed descriptions are exactly the original continuous maps ([Proposition 1.7, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)).

![A familiar space is changed into its probe data and then rebuilt with the same topology](roundtrip.gif)

There is also a way back. Start with the point values of a condensed set. Declare a subset closed when every probe detects it as closed. If we begin with a compactly generated space, turn it into probe data, and then apply this rule, we recover the original topology.

The theorem has limits. A topological space with a point that is not closed does not produce a condensed set of the required kind ([Warning 2.14, page 16](https://arxiv.org/pdf/2605.03658v1#page=16)). In the opposite direction, converting a condensed set back into a topological space can lose some information. The lectures give an example involving uncountable increasing unions of compact objects. This does not happen for countable colimits.

### The mathematics

[Proposition 1.7, page 9 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=9) says that $X\mapsto\underline X$ is fully faithful on compactly generated spaces:

```math
\operatorname{Hom}_{\mathrm{Top}}(X,Y)
\xrightarrow{\sim}
\operatorname{Hom}_{\operatorname{Cond}(\mathrm{Set})}(\underline X,\underline Y).
```

It also gives the return map. [Theorem 2.16, page 17](https://arxiv.org/pdf/2605.03658v1#page=17) identifies the compact case:

```math
(\underline X(*))_{\mathrm{top}}\cong X,
\qquad
\{\text{compact Hausdorff spaces}\}\simeq
\{\text{qcqs condensed sets}\}.
```

**Reading the symbols.** The notation $\operatorname{Hom}$ means the set of maps. The subscript $\mathrm{Top}$ means continuous maps of topological spaces. The expression $\operatorname{Cond}(\mathrm{Set})$ refers to condensed sets. An underline sends a space to its probe data. An arrow marked $\sim$ is a bijection, so each map of condensed sets comes from exactly one continuous map. The expression $\underline X(*)$ reads the value on the one-point probe, and the subscript $\mathrm{top}$ gives it the topology detected by all probes. The symbol $\cong$ means isomorphic. The symbol $\simeq$ means an equivalence of categories. The abbreviation qcqs means quasicompact and quasiseparated.

**Why it matters.** On the familiar class used here, the translation preserves spaces and all maps between them. Condensed sets enlarge topology instead of replacing it with a description that forgets ordinary spaces.

**In the simulation.** Choose a circle, interval, or finite set to follow $X\mapsto\underline X\mapsto(\underline X(*))_{\mathrm{top}}$. Each returns with the same topology. The example with a nonclosed point stops at the first step because it does not meet the theorem's assumptions.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/07.html)** to translate several spaces into probe data and recover their topologies.

---

[← Probes on which every cover splits](../06-unfoldable-probes/README.md)  ·  [Keeping track of holes →](../08-counting-holes/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

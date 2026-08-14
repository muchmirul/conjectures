# 4 · Cut, and glue

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The entries of an answer sheet cannot be chosen independently. They must respect two basic ways of relating probes, called **cut** and **glue**. Together, these are the sheaf conditions in the definition of a condensed set.

**Cut.** If a probe is a disjoint union of two pieces, then a landing of the whole probe contains exactly the same information as one landing for each piece. Since the pieces do not meet, the two landings can be chosen independently and then combined.

![Two disjoint pieces of a probe contribute one independent answer each to the answer for the whole probe](cut.png)

**Glue.** Suppose a larger probe covers a smaller probe. A landing on the covering probe descends to the smaller one when it assigns the same result wherever the cover represents the same point more than once. If that agreement holds, there must be one and only one landing downstairs that produces the given landing upstairs.

![Two answers on overlapping covering pieces agree in the shared region and combine into one answer below](glue.gif)

The glue rule prevents two kinds of failure. Compatible local answers must assemble into a global answer, so information cannot agree everywhere locally but fail to exist globally. The global answer must also be unique, so the same local data cannot produce two different results. The lectures place these two requirements directly after the definition ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). Thus, a condensed set is precisely an answer sheet on profinite probes that respects disjoint pieces and compatible covers.

A size issue also appears in the definition, and the lectures address it immediately ([Remark 1.4, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)). There are too many profinite sets to collect into one ordinary set, so the phrase "every probe" must be handled carefully. One first chooses a sufficiently large size bound, develops the theory within that bound, and proves that enlarging it does not change the resulting mathematics. This guide will treat that step as background bookkeeping.

### The mathematics

[Definition 1.2, page 6 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=6) gives the two sheaf conditions explicitly. For disjoint probes,

```math
T(S_1\sqcup S_2)\xrightarrow{\sim}T(S_1)\times T(S_2).
```

The second condition begins with a surjection $q:S'\twoheadrightarrow S$ and the projections $p_1,p_2:S'\times_S S'\to S'$. The glue condition is

```math
T(S)\xrightarrow{\sim}
\{x\in T(S')\mid p_1^*x=p_2^*x\text{ in }T(S'\times_S S')\}.
```

**Reading the symbols.** The letter $T$ is an answer sheet, and $T(S)$ is its set of answers on the probe $S$. The symbol $\sqcup$ means disjoint union, $\times$ means Cartesian product, and an arrow marked $\sim$ means a bijection. The map $q$ is a cover, shown by the double-headed arrow. The fibre product $S'\times_S S'$ contains pairs of covering points that represent the same point below. The maps $p_1$ and $p_2$ select the first and second member of such a pair. The star in $p_i^*$ means pullback. Braces mean “the set of,” $\in$ means “belongs to,” and the vertical bar means “such that.” The equality says that an answer upstairs gives the same value on both representatives of every point downstairs.

**Why it matters.** The first bijection says that separate pieces can be answered independently. The second says that compatible answers on a cover come from exactly one answer below. These are not optional properties; together with $T(\varnothing)=*$, they are the definition of a condensed set.

**In the simulation.** In cut mode, the two controls choose the independent entries in $T(S_1)\times T(S_2)$. In glue mode, they choose the two pullbacks $p_1^*x$ and $p_2^*x$. An answer below appears only when those values agree.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/04.html)** to assign local answers and see how the cut and glue rules decide whether they form one valid answer.

---

[← What a shape says to a probe](../03-what-a-shape-says/README.md)  ·  [The quotient with no points →](../05-the-ghost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

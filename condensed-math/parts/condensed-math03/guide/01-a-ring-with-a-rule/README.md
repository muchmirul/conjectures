# 1 · A ring and its legal measures

*Part 3 of three: Measure Rules for Rings and Geometry. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Part two used one fixed summation rule based on integer-valued measures. That rule does not suit every ring. The real numbers and the $p$-adic numbers have different ideas of convergence, so they should not be forced to use the same completion.

A **ring** has addition, subtraction, and multiplication. A **module** is an additive group whose elements can also be multiplied by elements of the ring. For each probe, we want to specify which weighted combinations of its points are allowed in a module and how those combinations behave.

The general definition has two pieces ([Definition 7.1, page 45](https://arxiv.org/pdf/2605.03658v1#page=45)). First, we choose a condensed ring $A$. As in part one, its probe values contain topological information together with algebraic operations. Second, for every extremally disconnected probe $S$, we choose an $A$-module $\mathcal M[S]$ of allowed measures.

The measure modules must include all **Dirac measures**, which place unit weight at one point. They must also respect finite disjoint unions. Measures on two separate probes should be the same as one independent measure on each probe.

![A probe maps to its module of allowed measures, and every point enters as a Dirac measure](measures.png)

These visible rules are necessary but not sufficient. The proposed measure theory must remain stable when its modules are used in exact sequences and chain complexes. [Definition 7.4, page 46](https://arxiv.org/pdf/2605.03658v1#page=46) gives the derived compatibility test. A pair that passes it is called an **analytic ring**.

This distinction matters because a rule can look sensible on each individual probe and still fail after modules are combined. Chapter 3 shows this for several natural real-valued measure rules.

### The mathematics

[Definition 7.1, page 45 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=45) defines a theory of measures on a condensed ring $A$ as a functor

```math
\mathcal M:\{\text{extremally disconnected }S\}
\longrightarrow A\text{-}\operatorname{Mod},
\qquad
S\longmapsto\mathcal M[S],
```

The definition also includes a natural Dirac map $S\to\mathcal M[S]$, which sends each point to its unit measure. For disjoint probes, the measure modules must satisfy

```math
\mathcal M[S_1\sqcup S_2]\cong\mathcal M[S_1]\times\mathcal M[S_2].
```

[Definition 7.4, page 46](https://arxiv.org/pdf/2605.03658v1#page=46) calls the pair analytic when, for the specified complexes $C$,

```math
R\!\operatorname{Hom}_A(\mathcal M[S],C)
\xrightarrow{\sim}
R\!\operatorname{Hom}_A(A[S],C).
```

**Reading the symbols.** The ring is $A$, and $A$-$\operatorname{Mod}$ is the category of condensed $A$-modules. The functor $\mathcal M$ assigns a module of legal measures $\mathcal M[S]$ to each extremally disconnected probe $S$. The map $S\to\mathcal M[S]$ sends each point to its Dirac measure. The symbol $\sqcup$ means disjoint union, $\times$ means product, and $\cong$ means isomorphic. The notation $A[S]$ is the free $A$-module on the points of $S$. The letter $C$ names a chain complex made from free measure modules. The expression $R\!\operatorname{Hom}_A$ is the derived object of $A$-linear maps. An arrow marked $\sim$ is an isomorphism.

**Why it matters.** The first two displays describe a proposed summation rule. The final isomorphism tests whether that rule survives the homological constructions used later. Passing the finite rules alone does not prove that a pair is analytic.

**In the simulation.** Choose a ring $A$ and a proposed module $\mathcal M[S]$. Two controls check whether point masses are included and whether disjoint pieces give a product. The final result represents the additional analytic condition as a quoted fact rather than treating the finite checks as a proof.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/01.html)** to assemble the data of a measure rule and check each basic requirement.

---

[← Start here](../00-start-here/README.md)  ·  [Two analytic examples →](../02-two-that-work/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

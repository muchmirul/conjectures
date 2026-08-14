# 1 · A ring with a rule for sums

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Part two attached one particular theory of infinite summation to the integers. Other rings need different theories, so we begin by separating the underlying ring from the measures it permits. This allows p-adic numbers, ordinary discrete rings, and the real numbers to use the same framework without pretending that they share one notion of convergence.

A ring supports addition, subtraction, and multiplication. A module is an additive group whose elements can also be multiplied by elements of the ring. For every probe and every placement of its points in a module, we want a rule that says which weighted combinations are legal and how those combinations act on the module.

The general definition contains two pieces of data ([Definition 7.1, page 45](https://arxiv.org/pdf/2605.03658v1#page=45)):

**The ring** is treated as a condensed ring, meaning an answer sheet of the kind introduced in part one, with compatible addition and multiplication. This description allows topological information to live inside the algebra rather than beside it.

**The theory of measures** assigns an A-module of legal measures to every unfoldable probe. It respects finite disjoint unions, and it includes every Dirac measure, the unit weight concentrated at one point. Thus, ordinary points remain available inside the larger space of measures.

![A diagram sends a probe to its module of allowed measures and includes each probe point as a Dirac measure](measures.png)

A ring and a proposed theory of measures must also pass a compatibility test. The test ensures that modules built from the proposed free complete modules form a stable algebraic world, with the expected maps from point data agreeing with maps from measures. A pair that passes is called an **analytic ring** ([Definition 7.4, page 46](https://arxiv.org/pdf/2605.03658v1#page=46)). This guide uses the plainer phrase *a ring with a rule*.

The distinction between proposing a rule and proving it analytic is important. Many assignments look reasonable on each individual probe but fail when modules are combined into exact sequences or complexes. Section 3 examines this problem for real-valued measures and shows why the first natural choices do not pass.

### The mathematics

[Definition 7.1, page 45 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=45) defines a theory of measures on a condensed ring $A$ as a functor

```math
\mathcal M:\{\text{extremally disconnected }S\}
\longrightarrow A\text{-}\operatorname{Mod},
\qquad
S\longmapsto\mathcal M[S],
```

The definition also includes natural Dirac maps $S\to\mathcal M[S]$. Its disjoint-union rule is

```math
\mathcal M[S_1\sqcup S_2]\cong\mathcal M[S_1]\times\mathcal M[S_2].
```

[Definition 7.4, page 46](https://arxiv.org/pdf/2605.03658v1#page=46) calls the pair analytic when, for the complexes $C$ specified there,

```math
R\!\operatorname{Hom}_A(\mathcal M[S],C)
\xrightarrow{\sim}
R\!\operatorname{Hom}_A(A[S],C).
```

**Reading the symbols.** The ring is $A$, and $A$-$\operatorname{Mod}$ is the category of condensed $A$-modules. The functor $\mathcal M$ assigns the module of legal measures $\mathcal M[S]$ to each unfoldable probe $S$. The arrow $S\to\mathcal M[S]$ sends a point to its Dirac measure. The symbol $\sqcup$ means disjoint union, $\times$ means product, and $\cong$ means isomorphic. The notation $A[S]$ is the free $A$-module on the points of $S$. The letter $C$ names a chain complex assembled from free measure modules. The expression $R\!\operatorname{Hom}_A$ is the derived object of $A$-linear maps, and an arrow marked $\sim$ is an isomorphism.

**Why it matters.** The first two lines propose a summation rule. The final isomorphism is the test that makes the proposal stable under the homological operations used later. A pair may satisfy the visible finite rules and still fail this analytic test.

**In the simulation.** The controls first select the ring $A$, then a candidate module $\mathcal M[S]$, and finally check that points enter as Dirac measures and disjoint pieces produce a product. The final verdict represents the extra analytic condition rather than pretending that the finite checks prove it.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/01.html)** to assemble the two pieces of a proposed rule and check its basic requirements in order.

---

[← Start here](../00-start-here/README.md)  ·  [Two rules that work →](../02-two-that-work/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

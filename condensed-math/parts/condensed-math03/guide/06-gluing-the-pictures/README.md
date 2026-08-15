# 6 · Gluing affine patches

*Part 3 of three: Measure Rules for Rings and Geometry. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

So far, we have worked with one ring, which describes one affine patch. A general geometric space is built from several patches that overlap. To glue the module theories, each patch must remember both its ring of functions and which functions count as bounded.

A **Huber pair** consists of a ring $A$ and an integrally closed subring $A^+$. Elements of $A^+$ are declared to have size at most one. A point of the corresponding valuation space assigns multiplicative sizes to all elements of $A$ while keeping every element of $A^+$ within that bound ([Proposition 9.2, page 63](https://arxiv.org/pdf/2605.03658v1#page=63)).

![Three regions of possible valuations become smaller as more functions are required to have size at most one](spa.png)

Choosing $A^+$ selects the valuations that regard all its elements as bounded. In the setting of the proposition, the selected region also recovers $A^+$: it consists exactly of the functions whose size is at most one at every point in the region. The algebraic choice and the geometric region determine each other.

![Compatible module data on two overlapping affine patches combine into one object on their union](gluing.gif)

[Theorem 9.8, page 65](https://arxiv.org/pdf/2605.03658v1#page=65) says that the derived categories of complete modules form a sheaf over these patches. Local module objects that agree on every overlap determine one global object, including all required higher compatibility data. This theorem lets us extend the affine construction of compactly supported cohomology to spaces made from many affine pieces.

The statement uses infinity-categories because gluing derived objects needs more than maps up to homotopy. It must also retain compatible homotopies between homotopies and all further levels. Earlier finite examples did not need this language, but the global gluing step does.

The proof follows the usual pattern of Zariski descent. Cover a space by patches where selected functions become invertible, verify the statement on each localized patch, and show that an object vanishing on every patch was already zero globally. Lecture X proves the localization facts needed for this argument.

### The mathematics

For a ring $A$, [Proposition 9.2, page 63 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=63) relates an integrally closed subring $A^+$ to its valuation region:

```math
\operatorname{Spa}(A,A^+)
=\{x\in\operatorname{Spv}(A)\mid |f(x)|\le1\text{ for every }f\in A^+\},
```

```math
A^+=\{f\in A\mid |f(x)|\le1\text{ for every }x\in\operatorname{Spa}(A,A^+)\}.
```

[Theorem 9.8, page 65](https://arxiv.org/pdf/2605.03658v1#page=65) states the gluing result:

```math
U=\operatorname{Spa}(A,A^+)
\longmapsto
D((A,A^+)^{\blacksquare})
\quad\text{is a sheaf of }\infty\text{-categories on }X.
```

**Reading the symbols.** The subring $A^+$ contains the functions declared to have size at most one. The space $\operatorname{Spv}(A)$ contains equivalence classes of valuations on $A$. The region $\operatorname{Spa}(A,A^+)$ keeps the valuations that bound every element of $A^+$ by one. The braces mean “the set of,” $\in$ means “belongs to,” and the vertical bar means “such that.” The expression $|f(x)|$ is the size that the valuation $x$ assigns to $f$. The open patch is $U$, and $D((A,A^+)^{\blacksquare})$ is its derived category of complete modules. Saying that these categories form a sheaf means that compatible local objects glue uniquely. The infinity symbol records all higher homotopies needed for that compatibility.

**Why it matters.** The first two displays say that the bounded subring and its valuation region determine one another. The theorem then lets the module categories on local regions assemble into one global category.

**In the simulation.** Selecting bounded functions changes $A^+$. Highlighted points are the valuations that satisfy the corresponding bounds. The plotted points are a schematic model, so they show how extra conditions shrink a region rather than representing the valuation space of one specific ring.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/06.html)** to add boundedness conditions and see which valuations remain.

---

[← Compactly supported cohomology](../05-compact-support/README.md)  ·  [The six operations →](../07-six-operations/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

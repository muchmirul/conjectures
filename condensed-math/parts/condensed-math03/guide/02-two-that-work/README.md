# 2 · Two analytic examples

*Part 3 of three: Measure Rules for Rings and Geometry. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The first examples extend the solid measures from part two. They use the same general definition with two different coefficient rings.

For the **$p$-adic rule**, use the $p$-adic integers as the ring. On every probe, take compatible measures with values in the $p$-adic integers. [Proposition 7.8, page 48](https://arxiv.org/pdf/2605.03658v1#page=48) proves that this pair is analytic, so $p$-adic summation fits the general framework.

For the **solid rule over a discrete ring**, let $A$ be any ring with the discrete topology. Begin with compatible integer measures and extend their coefficients from $\mathbb Z$ to $A$. Proposition 7.8 also proves that this pair is analytic.

![The p-adic measure rule and the solid rule over a discrete ring are shown with one example for each](two_rules.png)

A discrete ring has no nontrivial limits inside the ring itself, but the second example is still meaningful. The measure rule governs condensed modules over the ring, not only individual elements of the ring. Those modules can carry topological information in their probe values. The rule selects modules in which solid measures can be integrated consistently.

This separation is useful. The ring controls multiplication, while its measure theory controls infinite additive behavior in modules. We can change the completion rule without changing the algebraic formulas for multiplication.

A wider construction starts with a ring $A$ and a subring $A^+$ whose elements are declared to have size at most one ([Remark 7.9, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)). The pair $(A,A^+)$ is called a **Huber pair**. For the field of $p$-adic numbers, it gives bounded $p$-adic-valued measures. We will return to Huber pairs when we build geometric patches in chapter 6.

### The mathematics

[Proposition 7.8, page 48 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=48) says that the following two measure theories are analytic:

```math
\mathbb Z_{p,\blacksquare}[S]
:=\varprojlim_i\mathbb Z_p[S_i]
=M(S,\mathbb Z_p),
```

```math
(A,\mathbb Z)^{\blacksquare}[S]
:=\mathbb Z[S]^{\blacksquare}\otimes_{\mathbb Z}A
\qquad\text{for a discrete ring }A.
```

[Remark 7.9, page 49](https://arxiv.org/pdf/2605.03658v1#page=49) extends the pattern to a Huber pair $(A,A^+)$ and gives

```math
(\mathbb Q_p,\mathbb Z_p)^{\blacksquare}[S]
=M_b(S,\mathbb Q_p)
=M(S,\mathbb Z_p)[1/p].
```

**Reading the symbols.** The probe $S$ has finite stages $S_i$. The inverse limit $\varprojlim$ keeps compatible $p$-adic weights at every stage. The group $\mathbb Z_p$ is the $p$-adic integers, and $M(S,\mathbb Z_p)$ is the module of $\mathbb Z_p$-valued measures. In the second display, $A$ is a discrete ring. The tensor product $\otimes_{\mathbb Z}$ changes integer coefficients to coefficients in $A$. The black square marks the solid measure rule. A Huber pair consists of a ring $A$ and a chosen bounded subring $A^+$. The field $\mathbb Q_p$ is the $p$-adic numbers. The subscript $b$ means bounded, and $[1/p]$ permits division by powers of $p$.

**Why it matters.** These examples keep multiplication and summation separate. One framework handles a topological $p$-adic ring and a discrete ring without pretending that they have the same completion.

**In the simulation.** The selector switches between the two constructions. Nested boxes represent compatible $\mathbb Z_p$-valued weights. A row of coefficients represents the extension of $\mathbb Z[S]^{\blacksquare}$ from integer coefficients to a discrete ring $A$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/02.html)** to compare the two rules and the infinite operations each one allows.

---

[← A ring and its legal measures](../01-a-ring-with-a-rule/README.md)  ·  [A measure rule for the real numbers →](../03-the-real-lines-own-rule/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

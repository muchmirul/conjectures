# 2 · Two rules that work

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The first examples require no new construction because they come from the solid measures of part two. They show how the general definition packages familiar completion rules.

**The base-p rule.** Use the p-adic integers as the ring and compatible p-adic-valued measures on each probe as its free complete modules. This pair passes the analytic-ring test ([Proposition 7.8, page 48](https://arxiv.org/pdf/2605.03658v1#page=48)), so p-adic summation fits the new framework.

**The solid rule over a plain ring.** Let A be any discrete ring and extend the integer-valued solid measures by coefficients in A. This pair also passes. It supplies a theory of complete A-modules even though the underlying ring itself has no nontrivial topology.

![The p-adic measure rule and the solid rule over a discrete ring are compared with one infinite sum handled by each](two_rules.png)

The second example may initially seem empty because a discrete ring has no limits to complete inside the ring itself. However, the rule governs condensed modules over that ring, not merely its individual elements. Those modules can carry rich topological information through their probe values. The theory selects the modules in which solid measures can be integrated consistently, while keeping the coefficient ring algebraically simple.

This separation is useful in geometry. The ring describes multiplication of functions, while the theory of measures controls infinite additive behaviour in its modules. Since these roles are independent, one can alter the completion rule without changing the underlying algebraic formulas.

A broader construction begins with a ring A and a chosen subring of elements regarded as having size at most one ([Remark 7.9, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)). Such a pair is called a Huber pair. For the field of p-adic numbers, it produces the bounded p-adic-valued measures. Section 6 will use Huber pairs to turn local rings into geometric patches.

### The mathematics

[Proposition 7.8, page 48 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=48) states that the following two theories are analytic:

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

[Remark 7.9, page 49](https://arxiv.org/pdf/2605.03658v1#page=49) extends this pattern to a Huber pair $(A,A^+)$ and, in particular, identifies

```math
(\mathbb Q_p,\mathbb Z_p)^{\blacksquare}[S]
=M_b(S,\mathbb Q_p)
=M(S,\mathbb Z_p)[1/p].
```

**Reading the symbols.** The probe $S$ has finite stages $S_i$. The inverse-limit symbol $\varprojlim$ keeps compatible $p$-adic weights on all stages. The group $\mathbb Z_p$ is the $p$-adic integers, and $M(S,\mathbb Z_p)$ is the module of $\mathbb Z_p$-valued measures. In the second line, $A$ is any discrete ring, $\otimes_{\mathbb Z}$ extends integer coefficients to $A$, and the black square marks the solid measure rule. A Huber pair consists of a ring $A$ and a subring $A^+$ of elements regarded as bounded. The field $\mathbb Q_p$ is the $p$-adic numbers. The subscript $b$ means bounded, and $[1/p]$ allows division by powers of $p$.

**Why it matters.** These examples separate multiplication, supplied by the ring, from summation, supplied by its measure modules. The same framework handles a topological $p$-adic ring and an algebraically discrete ring without assigning them the same completion.

**In the simulation.** The rule selector switches between the two displayed constructions. The nested boxes represent the inverse limit for $\mathbb Z_p$, while the row of coefficients represents extension from $\mathbb Z[S]^{\blacksquare}$ to a discrete ring $A$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/02.html)** to compare the p-adic and discrete-ring rules and see which measures each one permits.

---

[← A ring with a rule for sums](../01-a-ring-with-a-rule/README.md)  ·  [The real line's own rule →](../03-the-real-lines-own-rule/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

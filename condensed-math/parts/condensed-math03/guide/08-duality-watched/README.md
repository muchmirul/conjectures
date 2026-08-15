# 8 · Coherent duality

*Part 3 of three: Measure Rules for Rings and Geometry. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Duality pairs two kinds of cohomological information and produces a scalar on the base. A **perfect pairing** loses no information: knowing how one input pairs with every input on the other side determines it completely. For a smooth space, the partner uses differential forms and a shift by the dimension.

![A torus rotates while classes in complementary degrees pair and pass through a trace map](duality.gif)

The animation models this on a surface. One class has a chosen degree, and its partner has the complementary degree. Their product reaches the top degree. Compactly supported pushforward carries that class to the base, where a trace map turns it into one scalar.

[Theorem 11.1, page 71](https://arxiv.org/pdf/2605.03658v1#page=71) applies to a separated smooth map of finite type with a fixed relative dimension. It constructs compactly supported pushforward, proves that it agrees with ordinary cohomology for a proper map, and gives a canonical trace from top-degree differential forms to the base. Pairing with that trace identifies the two dual objects. This is coherent duality in the setting of solid modules.

![Matching spaces of degree-zero and degree-one classes pair into a top-degree class and then into the base ring](pairing.png)

The earlier chapters provide three parts of the construction. First, $f^!$ is defined as the right adjoint of compactly supported pushforward, so $f^!$ of the unit is the dualizing complex. In the smooth case, the theorem identifies this object with the expected differential forms and proves that the pairing is perfect.

Second, compactly supported pushforward preserves compact objects. For a proper map, it agrees with ordinary pushforward, which also preserves discreteness. This recovers the classical finite-generation statement for coherent cohomology ([Remark 8.3, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)).

Third, the construction may pass through nondiscrete modules because boundary functions have infinite tails. The right adjoint can return the dualizing complex to the discrete setting. Condensed mathematics provides the larger category needed for the middle of the construction.

### The mathematics

[Theorem 11.1, page 71 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=71) considers a separated smooth map $f:X\to\operatorname{Spec}R$ of finite type and relative dimension $d$. Define

```math
\omega_{X/R}:=\bigwedge^d\Omega^1_{X/R},
```

The theorem gives a trace and a perfect duality:

```math
\operatorname{tr}:f_!\omega_{X/R}[d]\longrightarrow R,
```

```math
R\!\operatorname{Hom}_{X}(C,\omega_{X/R})[d]
\xrightarrow{\sim}
R\!\operatorname{Hom}_{R}(f_!C,R).
```

Properness removes the difference between compactly supported and ordinary cohomology. When $f$ is proper, the theorem also gives

```math
f_!C\cong R\Gamma(X,C).
```

**Reading the symbols.** The space is $X$, the base ring is $R$, and $\operatorname{Spec}R$ is its affine base space. The integer $d$ is the relative dimension. The module $\Omega^1_{X/R}$ contains relative differential one-forms. Its top exterior power $\bigwedge^d$ is written $\omega_{X/R}$. The functor $f_!$ is compactly supported pushforward. Square brackets $[d]$ shift the cohomological degree by $d$. The trace $\operatorname{tr}$ sends a top-degree compactly supported class to a scalar in $R$. The letter $C$ names a suitable complex on $X$. The two derived Hom expressions are dual objects, and the arrow marked $\sim$ says that the trace pairing identifies them. The notation $R\Gamma(X,C)$ means derived global cohomology.

**Why it matters.** The theorem identifies the right adjoint of compactly supported cohomology with the expected object of differential forms and proves that the pairing loses no information. If the space is proper, compactly supported and ordinary cohomology agree, which recovers classical coherent duality.

**In the simulation.** Degree controls choose a class and a possible partner. Their product reaches the top degree only when the degrees add to the displayed dimension $d$. The trace then sends the result to one scalar. Matching finite dimensions illustrate a perfect pairing but do not prove the theorem.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/08.html)** to pair complementary degrees and follow their product through the trace.

---

[← The six operations](../07-six-operations/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

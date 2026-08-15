# 5 · Compactly supported cohomology

*Part 3 of three: Measure Rules for Rings and Geometry. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

A map from a space to a point gives two ways to collect information. Ordinary pushforward collects global sections across the whole space. Pushforward with compact support keeps the part whose support does not continue out toward the boundary.

For the second operation, we must compare functions defined everywhere with functions that exist near the boundary. The quotient from chapter 4 provides exactly this comparison.

![Global function blocks are removed from boundary function blocks, leaving the negative-power tails](compact_support.gif)

For a finitely generated algebra over the integers, the global module theory and the boundary module theory are connected by three adjoint functors. The new left adjoint is built from the boundary quotient. This construction works because the relevant measure theories are analytic, so limits, products, and derived operations stay in the appropriate complete categories ([Theorem 8.1, page 53](https://arxiv.org/pdf/2605.03658v1#page=53)).

The resulting compactly supported pushforward has a right adjoint ([Theorem 8.2, page 53](https://arxiv.org/pdf/2605.03658v1#page=53)). In standard notation, they are lower shriek $f_!$ and upper shriek $f^!$. Applying $f^!$ to the unit object gives the **dualizing complex**. This adjunction defines the object by a universal property instead of requiring a separate guess in every example.

![A chart compares finite truncations of the boundary quotient for a line and a coordinate cross](dualizing.png)

For the coordinate cross, the lectures describe the dualizing complex as the integer dual of the quotient of boundary functions by global functions ([Remark 8.5, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)). The code only reproduces the rank pattern in finite truncations. It does not verify the categorical theorem.

Condensed modules are needed because boundary tails involve infinite products. Compactly supported pushforward can therefore send a discrete module to a genuinely nondiscrete object ([the discussion after Theorem 8.2, page 53](https://arxiv.org/pdf/2605.03658v1#page=53)). Its right adjoint does preserve discrete objects, so the final dualizing complex can still be classical even though its construction passes through a larger category.

Compactly supported pushforward also preserves compact objects. After gluing the local construction, proper pushforward agrees with compactly supported pushforward. This turns formal compactness into the usual finiteness result for coherent cohomology ([Remark 8.3, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)).

### The mathematics

Let $A$ be a finitely generated integer algebra. [Theorem 8.1, page 53 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=53) constructs

```math
j_!\dashv j^*\dashv j_*:
D(A^{\blacksquare})\longleftrightarrow D((A,\mathbb Z)^{\blacksquare}).
```

Let $f:\operatorname{Spec}A\to\operatorname{Spec}\mathbb Z$ be the projection. [Theorem 8.2, page 53](https://arxiv.org/pdf/2605.03658v1#page=53) defines compactly supported pushforward and its right adjoint:

```math
f_!:D(A^{\blacksquare})\longrightarrow D(\mathbb Z^{\blacksquare}),
\qquad
f_!\dashv f^!,
```

The same theorem identifies the dualizing complex:

```math
\omega_A:=f^!\mathbb Z
\cong R\!\operatorname{Hom}_{\mathbb Z}(f_!A,\mathbb Z).
```

**Reading the symbols.** The ring $A$ is finitely generated over the integers. The notation $D$ means a derived category of modules with the measure rule shown in parentheses. The symbols $j_!$, $j^*$, and $j_*$ are functors. The symbol $\dashv$ means “is left adjoint to.” The map $f$ sends the affine space $\operatorname{Spec}A$ to the base $\operatorname{Spec}\mathbb Z$. The functor $f_!$ is pushforward with compact support, and $f^!$ is its right adjoint. The object $\omega_A$ is the dualizing complex. The expression $R\!\operatorname{Hom}_{\mathbb Z}$ is the derived integer dual. The symbol $\cong$ means a canonical isomorphism.

**Why it matters.** The boundary quotient provides the new left adjoint $j_!$. It is used to construct $f_!$, and the right adjoint $f^!$ then defines the dualizing complex. The theorem also says that $f_!$ preserves compact objects, although it generally does not preserve discrete objects.

**In the simulation.** Choose the line or the cross. The top row represents boundary functions, the middle row represents global functions, and the bottom row represents their quotient. The displayed number is a finite truncation of the construction, not a proof of the adjunction.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/05.html)** to compare the boundary quotients of a line and a coordinate cross.

---

[← Global functions and boundary tails](../04-functions-near-the-edge/README.md)  ·  [Gluing affine patches →](../06-gluing-the-pictures/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

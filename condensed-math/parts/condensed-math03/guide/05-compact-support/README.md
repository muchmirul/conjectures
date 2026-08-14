# 5 · Cohomology with compact support

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

A map from a space to a point gives two natural ways to collect information. Ordinary pushforward records all global sections. Pushforward with compact support records the part that does not persist out toward the boundary. The second operation is harder because it must distinguish global behaviour from the infinite tails introduced in section 4.

**Everything.** Ordinary cohomology collects functions or sheaf data across the entire space. Algebraic geometry already has this pushforward, and it behaves well for the usual derived categories.

**Only what vanishes near the edge.** Compactly supported cohomology keeps data whose support stays away from the boundary. In the present construction, it is obtained by comparing global modules with the modules of functions near that boundary.

![Blocks for global functions are removed from the larger set of boundary functions, leaving the negative-power tails](compact_support.gif)

For a finitely generated algebra over the integers, the two relevant module theories are connected by a sequence of adjoints. The edge quotient provides the additional left adjoint needed to define compactly supported pushforward. This construction works because the theories are analytic rings, so products, limits, and derived operations retain the required completeness ([Theorem 8.1, page 53](https://arxiv.org/pdf/2605.03658v1#page=53)).

The resulting operation has a right adjoint, which means that maps out of a compactly supported pushforward correspond naturally and uniquely to maps into a partner object:

> Compactly supported pushforward has a right adjoint. Applying this right adjoint to the unit object produces the classical dualizing complex.

This is Theorem 8.2 ([page 53](https://arxiv.org/pdf/2605.03658v1#page=53)). In standard notation the operations are called lower shriek and upper shriek. Applying upper shriek to the unit object gives the dualizing complex. The adjunction characterizes this object canonically, replacing a separate case-by-case choice of a candidate.

![A chart compares the truncated boundary quotient for the affine line and the coordinate cross](dualizing.png)

For the coordinate cross, the lectures express the dualizing complex as the integer dual of the quotient of boundary functions by global functions ([Remark 8.5, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)). The truncation calculation in this repository reproduces the finite-dimensional counting pattern behind that quotient, not the categorical theorem itself.

Two consequences clarify why condensed modules are needed. First, compactly supported pushforward generally takes a discrete module to a genuinely nondiscrete object because boundary tails involve infinite products. The operation therefore has no naive construction within ordinary discrete modules. Its right adjoint does preserve discrete objects, so the final dualizing complex can be classical even though the route used to define it passes through condensed mathematics ([the discussion under Theorem 8.2, page 53](https://arxiv.org/pdf/2605.03658v1#page=53)).

Second, compactly supported pushforward preserves compact objects. This formal compactness condition becomes the local form of the familiar finiteness theorem for coherent cohomology ([Remark 8.3, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)). Once the construction is globalized and proper pushforward agrees with compactly supported pushforward, it recovers the usual finiteness statement.

### The mathematics

Let $A$ be a finitely generated integer algebra. [Theorem 8.1, page 53 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=53) constructs a chain of adjoints

```math
j_!\dashv j^*\dashv j_*:
D(A^{\blacksquare})\longleftrightarrow D((A,\mathbb Z)^{\blacksquare}).
```

Now let $f:\operatorname{Spec}A\to\operatorname{Spec}\mathbb Z$ be the projection. [Theorem 8.2, page 53](https://arxiv.org/pdf/2605.03658v1#page=53) defines compactly supported pushforward and its right adjoint

```math
f_!:D(A^{\blacksquare})\longrightarrow D(\mathbb Z^{\blacksquare}),
\qquad
f_!\dashv f^!,
```

The same theorem identifies the dualizing complex. Its formula is

```math
\omega_A:=f^!\mathbb Z
\cong R\!\operatorname{Hom}_{\mathbb Z}(f_!A,\mathbb Z).
```

**Reading the symbols.** The ring $A$ is finitely generated over the integers. The notation $D$ means the derived category of modules for the rule shown in parentheses. The symbols $j_!$, $j^*$, and $j_*$ are three functors, and $\dashv$ means “is left adjoint to.” The map $f$ sends the affine space $\operatorname{Spec}A$ to the integer base $\operatorname{Spec}\mathbb Z$. The functor $f_!$ is pushforward with compact support, and $f^!$ is its right adjoint. The object $\omega_A$ names the dualizing complex. The expression $R\!\operatorname{Hom}_{\mathbb Z}$ is the derived integer dual, and $\cong$ means a canonical isomorphism.

**Why it matters.** The left adjoint $j_!$ is the new operation supplied by the boundary quotient. Composing it with the ordinary map to the base produces $f_!$. Its right adjoint then defines the dualizing complex without choosing one separately. The theorem also states that $f_!$ preserves compact objects but generally not discrete ones.

**In the simulation.** The shape selector chooses the line or cross. The upper row represents boundary functions, the middle row represents global functions, and the lower row is the quotient used by $j_!$. The readout counts the finite truncation of $f_!A$; it illustrates the construction and does not prove the adjunction.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/05.html)** to form the boundary quotient for a line and a coordinate cross and compare the surviving tails.

---

[← Functions near the edge](../04-functions-near-the-edge/README.md)  ·  [Gluing the local pictures →](../06-gluing-the-pictures/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

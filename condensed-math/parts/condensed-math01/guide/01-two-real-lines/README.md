# 1 · The same numbers, but different ideas of closeness

*Part 1 of three: Understanding Spaces Through Probes. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Take two copies of the real numbers. The copies contain exactly the same values, but we give them different rules for closeness.

In the first copy, different numbers are never close. Every number stands alone. This is the real line with the **discrete topology**, which we will sometimes call the discrete real line. In the second copy, we keep the usual distance. Here 0.999 is close to 1, a sequence can approach a limit, and continuous motion is possible. This is the usual real line.

![Two rows contain the same real values, but one row has isolated dots and the other is a continuous line](bijection.gif)

Map each number in the discrete copy to the same number in the usual copy. Every input has one output, no two inputs have the same output, and every output is reached. The map is therefore a bijection of sets.

The map is not an isomorphism of topological spaces. It is continuous from the discrete line to the usual line, but its inverse is not continuous. A single point is an open set in the discrete line. A single point is not open in the usual line. The inverse therefore fails the definition of continuity.

This creates a problem for algebra. For a map of abelian groups, the **kernel** consists of the elements sent to zero. The **cokernel** measures what remains in the target after we account for the image. In an abelian category, a map with zero kernel and zero cokernel must be an isomorphism. Our map has zero kernel and zero cokernel when treated as a map of topological abelian groups, but it is not an isomorphism. The usual category of topological abelian groups does not support this basic algebraic test.

The lectures begin with this failure ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). Both real lines have the same individual points, so checking one point at a time cannot distinguish them. A useful replacement must also record how whole compact families of points move.

### The mathematics

[Example 1.9, page 9 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=9) writes the identity map and its condensed cokernel explicitly. In topological abelian groups, the map has zero kernel and cokernel even though it is not an isomorphism:

```math
\mathbb{R}_{\mathrm{disc}} \xrightarrow{\;\mathrm{id}\;} \mathbb{R},
\qquad \ker(\mathrm{id})=0, \qquad \operatorname{coker}(\mathrm{id})=0,
\qquad \mathbb{R}_{\mathrm{disc}}\not\cong\mathbb{R}.
```

After we pass to condensed abelian groups, the cokernel $Q$ is not zero. On a profinite probe $S$, it has the value

```math
Q(*)=0,
\qquad
Q(S)=\frac{C(S,\mathbb{R})}{C_{\mathrm{lc}}(S,\mathbb{R})}\neq 0
\quad\text{for suitable }S.
```

**Reading the symbols.** The symbol $\mathbb{R}$ means the real numbers. The subscript $\mathrm{disc}$ gives them the discrete topology. The label $\mathrm{id}$ means that every number maps to itself. The expressions $\ker$ and $\operatorname{coker}$ mean kernel and cokernel. The symbol $0$ is the zero group, and $\not\cong$ means “is not isomorphic to.” The letter $Q$ names the condensed cokernel. The symbol $*$ is the probe with one point. The notation $C(S,\mathbb{R})$ means all continuous maps from $S$ to the usual real line. The subscript $\mathrm{lc}$ keeps only the locally constant maps, which are exactly the continuous maps into the discrete real line. The fraction bar forms a quotient group. Finally, $\neq0$ says that this quotient contains a nonzero element for some probe.

**Why it matters.** A one-point probe sees $Q(*)=0$, while a larger probe can see $Q(S)\neq0$. The condensed cokernel keeps the topological information that pointwise algebra lost. [Theorem 1.10, page 9](https://arxiv.org/pdf/2605.03658v1#page=9) says that condensed abelian groups form an abelian category, so zero kernel and zero cokernel once again imply that a map is an isomorphism.

**In the simulation.** The upper row represents $\mathbb{R}_{\mathrm{disc}}$, and the lower row represents $\mathbb{R}$. Each vertical line connects one real value to itself under $\mathrm{id}$. The point-level kernel and cokernel remain zero even though the two rows use different rules for closeness.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/01.html)** to compare the two topologies and see why a pointwise bijection is not enough.

---

[← Start here](../00-start-here/README.md)  ·  [Building a probe from finite stages →](../02-branching-probes/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

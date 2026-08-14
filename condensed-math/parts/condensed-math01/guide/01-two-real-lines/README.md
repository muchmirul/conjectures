# 1 · Two real lines

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Start with the set of all real numbers and give it two different rules about nearness. In the first copy, forget nearness completely. Two numbers are either equal or different, and no distinct numbers count as close. We will call this copy **the dust**, which is the real line with the discrete topology.

In the second copy, keep the usual notion of distance. In this copy, 0.999 is close to 1, sequences can approach limits, and continuous motion makes sense. We will call this copy **the ruler**, which is the ordinary topological real line.

![Two copies of the real numbers, one shown as separate dots and one as a continuous line, with equal values joined](bijection.gif)

Send each number in the dust to the same number on the ruler. The animation shows this matching. Every input has one output, different inputs remain different, and every point on the ruler is reached. As a map of underlying sets, it is a perfect one-to-one correspondence.

However, the two topological groups are not the same. The map from the dust to the ruler is continuous, but its inverse is not. A single point is open in the dust, while a single point is not open on the ruler, so the inverse fails the basic test for continuity. A bijection of points therefore does not guarantee an isomorphism of topological objects.

This causes a precise algebraic problem. In an abelian setting, one studies a map by finding its kernel, the elements it sends to zero, and its cokernel, the part of the target it fails to account for. If both are zero, the map should be an isomorphism. For the map above, both are zero even though the map is not an isomorphism, so topological abelian groups do not support this standard algebraic test.

The lectures begin with this example ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)) and give two related failures. These examples identify the problem that condensed mathematics is designed to solve. The point sets of the dust and ruler agree, so a successful repair must record how whole compact families of points move, not merely which individual points exist.

### The mathematics

[Example 1.9, page 9 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=9) writes the identity map and its condensed cokernel explicitly. In topological abelian groups the same map has zero kernel and cokernel, although it is not an isomorphism:

```math
\mathbb{R}_{\mathrm{disc}} \xrightarrow{\;\mathrm{id}\;} \mathbb{R},
\qquad \ker(\mathrm{id})=0, \qquad \operatorname{coker}(\mathrm{id})=0,
\qquad \mathbb{R}_{\mathrm{disc}}\not\cong\mathbb{R}.
```

After passing to condensed abelian groups, the cokernel $Q$ is no longer zero. Its value on a profinite probe $S$ is

```math
Q(*)=0,
\qquad
Q(S)=\frac{C(S,\mathbb{R})}{C_{\mathrm{lc}}(S,\mathbb{R})}\neq 0
\quad\text{for suitable }S.
```

**Reading the symbols.** The symbol $\mathbb{R}$ means the real numbers, and $\mathrm{disc}$ gives them the discrete topology. The label $\mathrm{id}$ means that each number is sent to itself. The symbols $\ker$ and $\operatorname{coker}$ mean kernel and cokernel. The symbol $0$ is the zero group, while $\not\cong$ means “is not isomorphic to.” The letter $Q$ names the condensed cokernel, and $*$ is the one-point probe. The notation $C(S,\mathbb{R})$ means all continuous maps from $S$ to the usual real line. The subscript $\mathrm{lc}$ restricts this to locally constant maps, which are exactly the continuous maps into the discrete real line. The fraction bar means quotient group, and $\neq 0$ says that this quotient has a nonzero element for some probe.

**Why it matters.** Points see $Q(*)=0$, but a larger probe can see $Q(S)\neq0$. Condensed groups therefore retain the missing topological quotient. [Theorem 1.10, page 9](https://arxiv.org/pdf/2605.03658v1#page=9) then states that condensed abelian groups form an abelian category, so zero kernel and zero cokernel once again force a map to be an isomorphism.

**In the simulation.** The two rows represent $\mathbb{R}_{\mathrm{disc}}$ and $\mathbb{R}$. Each vertical line is one value of $\mathrm{id}$. The point-level kernel and cokernel stay at zero, even though the two rows still have different rules for nearness.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/01.html)** to inspect the matching and see why its empty kernel and cokernel do not make it an isomorphism.

---

[← Start here](../00-start-here/README.md)  ·  [Probes that branch →](../02-branching-probes/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

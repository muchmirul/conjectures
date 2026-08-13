# 1 · Two real lines

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Start with the set of all real numbers and give it two different rules about nearness. In the first copy, forget nearness completely. Two numbers are either equal or different, and no distinct numbers count as close. We will call this copy **the dust**, which is the real line with the discrete topology.

In the second copy, keep the usual notion of distance. In this copy, 0.999 is close to 1, sequences can approach limits, and continuous motion makes sense. We will call this copy **the ruler**, which is the ordinary topological real line.

![The same numbers drawn twice, as separated grains and as a continuous ruler, with every grain matched to its point](bijection.gif)

Send each number in the dust to the same number on the ruler. The animation shows this matching. Every input has one output, different inputs remain different, and every point on the ruler is reached. As a map of underlying sets, it is a perfect one-to-one correspondence.

However, the two topological groups are not the same. The map from the dust to the ruler is continuous, but its inverse is not. A single point is open in the dust, while a single point is not open on the ruler, so the inverse fails the basic test for continuity. A bijection of points therefore does not guarantee an isomorphism of topological objects.

This causes a precise algebraic problem. In an abelian setting, one studies a map by finding its kernel, the elements it sends to zero, and its cokernel, the part of the target it fails to account for. If both are zero, the map should be an isomorphism. For the map above, both are zero even though the map is not an isomorphism, so topological abelian groups do not support this standard algebraic test.

The lectures begin with this example ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)) and give two related failures. These examples identify the problem that condensed mathematics is designed to solve. The point sets of the dust and ruler agree, so a successful repair must record how whole compact families of points move, not merely which individual points exist.

### The mathematics

Write $\mathbb{R}_{\mathrm{disc}}$ for the dust and $\mathbb{R}$ for the ruler, both taken as topological abelian groups. Sending each number to itself is a continuous homomorphism between them, and in the category of topological abelian groups it has no kernel and no cokernel:

```math
\mathbb{R}_{\mathrm{disc}} \xrightarrow{\;\mathrm{id}\;} \mathbb{R},
\qquad \ker = 0, \qquad \mathrm{coker} = 0,
\qquad \text{yet } \mathbb{R}_{\mathrm{disc}} \not\cong \mathbb{R}.
```

**Reading the symbols.** The symbol $\mathbb{R}$ means the real numbers, and the subscript $\mathrm{disc}$ says that distinct numbers are treated as separate, with no usual notion of nearness. The arrow labelled $\mathrm{id}$ sends every number to itself. The symbol $\ker$ names the kernel, or everything sent to zero, while $\mathrm{coker}$ names the cokernel, or what remains unaccounted for in the target. Both are $0$, meaning that neither detects a difference. The symbol $\not\cong$ says that the two topological groups are nevertheless not isomorphic.

**Why it matters.** In an abelian category, a map whose kernel and cokernel are both zero must be an isomorphism. This example violates that implication, so the category of topological abelian groups is not abelian. As a result, the usual tools of homological algebra cannot simply be applied there.

**In the simulation.** The slider controls how closely you inspect the two copies of the real line. The two rows represent $\mathbb{R}_{\mathrm{disc}}$ and $\mathbb{R}$, and the vertical lines show the identity map matching equal numbers. The readout displays the kernel and cokernel, which remain zero even while the pictures retain different notions of nearness.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/01.html)** to inspect the matching and see why its empty kernel and cokernel do not make it an isomorphism.

---

[← Start here](../00-start-here/README.md)  ·  [Probes that branch →](../02-branching-probes/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

# 1 · Two real lines

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Take the real numbers, the whole endless ruler of them, and write them down twice. In the first copy, forget every idea of nearness. Two numbers are either the same number or different numbers, and that is all you may ask. The numbers sit apart like grains of sand, and no grain is nearer any other. Call this copy **the dust**.

In the second copy, keep nearness. Now 0.999 is close to 1, a sequence can approach a limit, and a function can be continuous. Call this copy **the ruler**.

![The same numbers drawn twice, as separated grains and as a continuous ruler, with every grain matched to its point](bijection.gif)

There is an obvious way to go from the dust to the ruler, which is to send each number to itself. The animation matches them up, and nothing is left over on either side. Every number of the dust arrives somewhere, no two arrive at the same place, and every point of the ruler is arrived at, so the map loses nothing and adds nothing.

Even so, the dust and the ruler are not the same object, because on the ruler you may speak of limits and on the dust you may not. This gives a map which is not a genuine sameness, even though it has nothing missing at the front and nothing missing at the back.

The distinction matters, because it makes ordinary algebra impossible. In algebra the whole method is this: given a map, look at what it kills, look at what it misses, and if both are nothing, the map was a sameness. This is how one solves equations, chains up long calculations, and defines almost everything. Here both questions are answered with nothing, so the recipe declares the map a sameness, which is the wrong answer.

The lectures open on exactly this example ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)), and list two more failures of the same kind. That list sits on the first page of the course because the whole course is the repair for it. Rather than patching the recipe, the repair starts from the observation that the dust and the ruler differ in something the points cannot see, and then changes what an object *is*, so that the difference becomes visible.

### The mathematics

Write $\mathbb{R}_{\mathrm{disc}}$ for the dust and $\mathbb{R}$ for the ruler, both taken as topological abelian groups. Sending each number to itself is a continuous homomorphism between them, and in the category of topological abelian groups it has no kernel and no cokernel:

```math
\mathbb{R}_{\mathrm{disc}} \xrightarrow{\;\mathrm{id}\;} \mathbb{R},
\qquad \ker = 0, \qquad \mathrm{coker} = 0,
\qquad \text{yet } \mathbb{R}_{\mathrm{disc}} \not\cong \mathbb{R}.
```

**Reading the symbols.** The subscript "disc" records the choice to forget nearness, so $\mathbb{R}_{\mathrm{disc}}$ and $\mathbb{R}$ hold the same numbers under different rules about which of them count as close. The arrow labelled $\mathrm{id}$ is the map that sends each number to itself. The word $\ker$ names everything the map sends to zero, which is the kill-list, and $\mathrm{coker}$ names what the map fails to reach, which is the miss-list. The last symbol, $\not\cong$, says the two groups are still not the same object.

**Why it matters.** In an abelian category, a map with $\ker = 0$ and $\mathrm{coker} = 0$ is an isomorphism. Here both vanish and the map is not one, so topological abelian groups do not form an abelian category, and the standard machinery of homological algebra cannot be used on them.

**In the simulation.** The slider is how closely you look. The two rows are $\mathbb{R}_{\mathrm{disc}}$ and $\mathbb{R}$, the vertical lines are $\mathrm{id}$ matching them up one to one, and the readout prints $\ker$ and $\mathrm{coker}$ so you can watch both stay empty while the two rows behave differently.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/01.html)** to match the two lines yourself and watch both the kill-list and the miss-list come out empty.

---

[← Start here](../00-start-here/README.md)  ·  [Probes that branch →](../02-branching-probes/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

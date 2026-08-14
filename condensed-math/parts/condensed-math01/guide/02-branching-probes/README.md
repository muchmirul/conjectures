# 2 · Probes that branch

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

To detect nearness, we need an object that carries nearness of its own. Build one by starting with a box and repeatedly dividing it into smaller boxes. At each stage there are only finitely many pieces, together with a map telling us which new piece came from which old one. The infinite object is completely described by these finite stages and their connecting maps.

![Finite stages of three probes shown side by side: binary branching, an approaching sequence, and branching in base p](probes.png)

A **probe** consists of such a compatible sequence of finite divisions and the points obtained by following branches through every stage. The lectures call this a profinite set. Three examples will be used repeatedly in this guide.

The **halving probe** divides every box into two at each stage. After ten rounds it has 1024 boxes. Its limiting points form the classical Cantor set, which can also be made by repeatedly removing the middle third of every remaining interval.

The **approaching probe** records one convergent sequence and its limit. At stage five, the first five points have been separated into their own boxes, while all later points and the limit still occupy one final box. Further stages separate one more point at a time.

The **counting-in-base-p probe** divides each box into p pieces. Its limiting points form the p-adic integers, an important number system in which divisibility by powers of p determines nearness. Part two will use this probe to explain an infinite sum that converges in one notion of size but not another.

The formal name *profinite set* means an inverse limit of finite sets ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). Two parts of that description are important. Every individual stage is finite, and all information about the probe lies in the stages and the maps between them. The code follows this definition literally by storing finite sets and their transition maps. Its tests check the expected growth of all three probes and verify that compatible data can be read consistently through their levels.

### The mathematics

The definition used in [Definition 1.2, page 6 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=6) is that a profinite set is an inverse limit of finite sets:

```math
S \cong \varprojlim_i S_i,
\qquad
\pi_{ji}:S_j\twoheadrightarrow S_i \quad (j\ge i),
\qquad
\pi_{ki}=\pi_{ji}\circ\pi_{kj} \quad (k\ge j\ge i).
```

**Reading the symbols.** The letter $S$ names the whole probe, while each $S_i$ is its finite stage numbered $i$. The symbol $\cong$ means “is isomorphic to,” and $\varprojlim$ means inverse limit: a point of $S$ is a compatible choice of one box at every stage. The map $\pi_{ji}$ sends a box at the finer stage $j$ back to its parent at stage $i$. The double-headed arrow says that every coarse box has at least one finer box above it. The inequalities order the stages. The symbol $\circ$ means “followed by,” and the final equality says that going back two stages at once gives the same answer as going back one stage at a time.

**Why it matters.** This formula replaces one infinite object by finite stages joined by exact compatibility maps. The halving, approaching, and base-$p$ probes differ only in the finite sets $S_i$ and the maps $\pi_{ji}$.

**In the simulation.** The depth control chooses the largest index $i$ shown. Each row is one finite set $S_i$, and every connecting branch displays a transition map $\pi_{i+1,i}$. Selecting a box shows the finer boxes that map back to it.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/02.html)** to compare the three probes, change their depth, and inspect the points contained in any box.

---

[← Two real lines](../01-two-real-lines/README.md)  ·  [What a shape says to a probe →](../03-what-a-shape-says/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

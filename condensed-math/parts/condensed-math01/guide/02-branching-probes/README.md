# 2 · Building a probe from finite stages

*Part 1 of three: Understanding Spaces Through Probes. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We need probes that carry their own notion of closeness. To build one, start with a finite set of boxes and repeatedly divide each box into smaller boxes. At every stage, a map tells us which new box came from which box in the previous stage. The full probe consists of all the stages together with these maps.

![Three probes are shown through finite stages: binary branches, an approaching sequence, and base-p branches](probes.png)

A point of the completed probe is a choice of one box at every stage, where each chosen box lies inside the one chosen before it. The lectures call this an **inverse limit of finite sets**, or a **profinite set**. We will use three examples throughout the guide.

The **halving probe** divides each box into two. After ten divisions, it has 1024 boxes. Its completed set of points is the Cantor set. The **approaching-sequence probe** contains a sequence and its limit. At stage five, the first five sequence points have separate boxes, while all later points and the limit remain together in one box. Each new stage separates one more point.

The **base-$p$ probe** divides each box into $p$ pieces. Its points form the $p$-adic integers. In that number system, divisibility by powers of $p$ determines which numbers are close. Part two uses this probe to show why one infinite sum can diverge under the usual distance and converge under the $p$-adic distance.

The code follows [Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6) directly. It stores each finite set and each map to the earlier stage. The tests check the size of every stage and verify that moving back through several stages gives a consistent answer.

### The mathematics

[Definition 1.2, page 6 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=6) defines a profinite set as an inverse limit of finite sets:

```math
S \cong \varprojlim_i S_i,
\qquad
\pi_{ji}:S_j\twoheadrightarrow S_i \quad (j\ge i),
\qquad
\pi_{ki}=\pi_{ji}\circ\pi_{kj} \quad (k\ge j\ge i).
```

**Reading the symbols.** The letter $S$ names the complete probe, and $S_i$ is its finite stage numbered $i$. The symbol $\cong$ means “is isomorphic to.” The symbol $\varprojlim$ means inverse limit, so a point of $S$ is one compatible choice of a box at every stage. The map $\pi_{ji}$ sends a box at the finer stage $j$ back to its parent at stage $i$. The double-headed arrow says that every coarse box has a finer box above it. The inequalities put the stages in order. The symbol $\circ$ means composition. The last equality says that returning two stages at once gives the same result as returning one stage at a time.

**Why it matters.** The formula describes one infinite object using finite pieces and exact rules between them. The three examples differ only in their finite sets $S_i$ and their maps $\pi_{ji}$.

**In the simulation.** The depth control chooses the largest stage $i$ on the screen. Each row is a finite set $S_i$, and each branch shows part of the transition map $\pi_{i+1,i}$. Selecting one box highlights the finer boxes that map back to it.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/02.html)** to compare the three probes and inspect what lies above any chosen box.

---

[← The same numbers, but different ideas of closeness](../01-two-real-lines/README.md)  ·  [Mapping a probe into a space →](../03-what-a-shape-says/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

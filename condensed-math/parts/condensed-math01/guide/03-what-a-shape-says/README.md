# 3 · Mapping a probe into a space

*Part 1 of three: Understanding Spaces Through Probes. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

A probe **lands in** a space when we map all its points into the space continuously. Continuity requires the map to preserve closeness. For example, if points of the probe approach a limit, their images must approach the image of that limit.

![A sequence and its limit map into a target, first continuously and then with the limit sent elsewhere](landing.gif)

The animation compares two maps from the approaching-sequence probe. In the first map, the images of the sequence approach the chosen image of the limit, so the map is continuous. In the second map, the sequence approaches one value while the limit is sent to another. That map is not continuous.

We can now describe a space by recording every continuous map into it from every probe. For each probe, the record gives a set of allowed maps. This record is a **condensed set** once it satisfies the cut and glue rules in the next chapter ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). It remembers more than a list of points because it also tells us which compact families of points fit together continuously.

If the space supports addition, we can add two probe maps point by point and obtain a condensed group. If it also supports multiplication, we obtain a condensed ring ([Example 1.3, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)).

This description distinguishes the two real lines from chapter 1. The approaching probe has many continuous maps into the usual real line. A convergent sequence of real values and its limit give one. A map into the discrete real line can converge only if the sequence is eventually constant. The two lines therefore give different answers to the same probe.

For spaces whose topology comes from a distance, convergent sequences determine the topology. The approaching probe is enough to test those sequences ([Remark 1.6, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). More general spaces need all profinite probes, but this example shows how a probe detects information that isolated points miss.

![Points in a flat region move toward a boundary point that is not included in the region](sequence_test.png)

### The mathematics

[Example 1.3, page 7 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=7) sends a topological space $X$ to the condensed set represented by it:

```math
\underline{X}(S)=C(S,X)=\{f:S\to X\mid f\text{ is continuous}\}.
```

For the approaching probe $S=\mathbb{N}\cup\{\infty\}$, continuity has the following direct test:

```math
f(n)\longrightarrow f(\infty) \quad\text{as } n\to\infty.
```

**Reading the symbols.** The underline in $\underline{X}$ marks the condensed set associated with the space $X$. The expression $\underline{X}(S)$ is its answer to the probe $S$. The letter $C$ denotes continuous maps. The braces contain all maps $f$ from $S$ to $X$, and the vertical bar means “such that.” The symbol $\mathbb{N}$ means the natural numbers, and $\infty$ is the added limit point. The long arrow says that the images $f(n)$ approach $f(\infty)$ as $n$ grows without bound. [Remark 1.6, page 9](https://arxiv.org/pdf/2605.03658v1#page=9) explains why this test determines a metrizable space.

**Why it matters.** The one-point probe records only the points of $X$. Larger probes also record which families of points vary continuously. That is why they can distinguish the discrete and usual real lines.

**In the simulation.** One slider chooses the value approached by $f(n)$. The other chooses $f(\infty)$. The map passes the continuity test exactly when these values agree.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/03.html)** to change both values and watch the continuity test respond.

---

[← Building a probe from finite stages](../02-branching-probes/README.md)  ·  [The cut and glue rules →](../04-cut-and-glue/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

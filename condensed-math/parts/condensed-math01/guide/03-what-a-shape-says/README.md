# 3 · What a shape says to a probe

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We can now use a probe to examine a space. A probe **lands** in a space when its points are mapped there continuously. Continuity means that the map respects the nearness already carried by the probe. In particular, if probe points approach a limit, their images must approach the image of that limit.

![Points from an approaching sequence map to a target, first with the correct limit and then with a different limit](landing.gif)

The animation tests two attempted landings of the approaching probe. In the first, the sequence of images approaches the image of the limit point, so the landing is continuous. In the second, the sequence approaches one place while the limit point is sent elsewhere. That break in continuity causes the landing to be rejected.

This suggests a new way to describe a space. For every possible probe, record every continuous way that probe can land in the space. The resulting record is like an answer sheet: each probe poses a test, and the space answers with its set of legal landings. This answer sheet remembers not only which points exist but also which compact families of points fit together continuously.

An answer sheet satisfying the two compatibility rules in the next section is called a **condensed set** ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). If the original space has addition, its landings can be added point by point, producing a condensed group. If it also has multiplication, the same construction produces a condensed ring ([Example 1.3, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)).

This description immediately distinguishes the two real lines. The approaching probe has many continuous landings in the ruler, because any convergent sequence of real numbers and its limit gives one. In the dust, a convergent sequence must eventually remain at one value, so nearly all of those landings disappear. Although the dust and ruler have the same individual points, their answer sheets are different.

For spaces with a distance, the approaching probe already contains enough information to detect the topology. Such a space is determined by its convergent sequences, and this probe tests exactly those sequences ([Remark 1.6, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). More general spaces require all profinite probes, but this small example explains why probes can see information that points alone miss.

![Points inside a planar set approach a boundary point that the set does not contain](sequence_test.png)

### The mathematics

[Example 1.3, page 7 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=7) sends a topological space $X$ to the condensed set represented by it:

```math
\underline{X}(S)=C(S,X)=\{f:S\to X\mid f\text{ is continuous}\}.
```

For the approaching probe $S=\mathbb{N}\cup\{\infty\}$, continuity has a direct sequence test. It says

```math
f(n)\longrightarrow f(\infty) \quad\text{as } n\to\infty.
```

**Reading the symbols.** The underline in $\underline{X}$ means the condensed set associated with the space $X$. The expression $\underline{X}(S)$ is its answer to the probe $S$. The letter $C$ denotes continuous maps. Braces describe a set of maps $f$ from $S$ to $X$, the vertical bar means “such that,” and the words after it impose continuity. The symbol $\mathbb{N}$ means the natural numbers, while $\infty$ is the added limit point. The long arrow means that the sequence of images $f(n)$ converges to the image $f(\infty)$ as $n$ grows without bound. [Remark 1.6, page 9](https://arxiv.org/pdf/2605.03658v1#page=9) explains why this sequence test determines every metrizable space.

**Why it matters.** The value on the one-point probe records only the points of $X$. The values $\underline{X}(S)$ for larger probes also record which families of points fit together continuously, so they distinguish the dust from the ruler.

**In the simulation.** One slider chooses the value approached by the points $f(n)$, and the other chooses $f(\infty)$. The landing is accepted exactly when these two values agree, which is the displayed convergence condition.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/03.html)** to move the images of a convergent sequence and see exactly when the proposed landing stops being continuous.

---

[← Probes that branch](../02-branching-probes/README.md)  ·  [Cut, and glue →](../04-cut-and-glue/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

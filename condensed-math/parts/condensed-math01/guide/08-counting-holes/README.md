# 8 · Keeping track of holes

*Part 1 of three: Understanding Spaces Through Probes. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We should also check that probe data preserve topological features such as holes. For a circle, draw a closed path and count how many times it travels around the centre. This integer is the **winding number**. A continuous deformation can change the path's shape, but it cannot change the winding number unless the path breaks.

![A closed path changes shape around a circle while its integer winding number stays fixed](winding.gif)

The first cohomology group of a circle is one copy of the integers, and its generator measures this winding number. A product of two circles is a torus. It has two independent loop directions: one passes around the central opening, and one passes around the tube.

![A torus rotates in three dimensions and displays its two independent loop directions](torus.gif)

Products of more circles have higher-degree holes. We obtain one class by choosing several different circle directions at once. The lectures describe this for any number of circle factors, including infinitely many ([Proposition 3.1, page 20](https://arxiv.org/pdf/2605.03658v1#page=20)).

![Rows of bars show cohomology ranks for products of one to six circles, following Pascal's triangle](ranks.png)

The chart recomputes the finite cases. Each row follows Pascal's triangle because the rank in degree $i$ counts the ways to choose $i$ directions from the available circle directions.

Two results connect this calculation to condensed mathematics. For every compact space, classical sheaf cohomology agrees with cohomology after translation into condensed sets ([Theorem 3.2, page 21](https://arxiv.org/pdf/2605.03658v1#page=21)). With the usual real numbers as coefficients, all positive-degree condensed cohomology vanishes, while degree zero contains the continuous real-valued functions ([Theorem 3.3, page 22](https://arxiv.org/pdf/2605.03658v1#page=22)). This difference between integer and real coefficients will matter in part two.

### The mathematics

Let $\mathbb T=\mathbb R/\mathbb Z$ be the circle. [Proposition 3.1, page 20 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=20) computes the cohomology of a product of circles:

```math
H^i\!\left(\prod_{j\in I}\mathbb T,\mathbb Z\right)
\cong
\bigwedge^i\!\left(\bigoplus_{j\in I}\mathbb Z\right).
```

[Theorems 3.2 and 3.3, pages 21 and 22](https://arxiv.org/pdf/2605.03658v1#page=21) compare this with condensed cohomology and describe real coefficients:

```math
H^i_{\mathrm{sheaf}}(S,\mathbb Z)\cong H^i_{\mathrm{cond}}(S,\mathbb Z),
\qquad
H^i_{\mathrm{cond}}(S,\mathbb R)=0\ (i>0),
\qquad
H^0_{\mathrm{cond}}(S,\mathbb R)=C(S,\mathbb R).
```

**Reading the symbols.** The circle $\mathbb T$ is the real line $\mathbb R$ with numbers that differ by an integer identified. The product contains one circle for each label $j$ in the index set $I$. The group $H^i$ is cohomology in degree $i$, with integer coefficients $\mathbb Z$. The direct sum $\bigoplus$ contains finite integer combinations of directions. The exterior power $\bigwedge^i$ chooses $i$ distinct directions at a time. The subscripts $\mathrm{sheaf}$ and $\mathrm{cond}$ name classical sheaf cohomology and condensed cohomology. The condition $i>0$ means every positive degree. The notation $C(S,\mathbb R)$ means continuous real-valued functions on $S$.

**Why it matters.** For $n$ circles, the rank in degree $i$ is $\binom ni$, the number of ways to choose $i$ directions from $n$. The comparison theorem says that the condensed description preserves these hole counts for compact spaces. Real coefficients behave differently because every positive-degree group is zero.

**In the simulation.** The first control chooses a class in $H^1(\mathbb T,\mathbb Z)$ by setting its winding number. In torus mode, two controls choose the two generators of $H^1(\mathbb T^2,\mathbb Z)$. The displayed ranks $1,2,1$ come from the exterior-power formula.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/08.html)** to deform loops while keeping their winding numbers fixed, then compare the two loop directions on a torus.

---

[← Recovering familiar spaces](../07-nothing-was-lost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

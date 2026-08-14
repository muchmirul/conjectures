# 8 · Counting holes

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The final check is whether the translation preserves topological features such as holes. A basic way to detect a hole in a circle is to draw a closed path and count how many times it travels around the centre. This count is the winding number, and it remains unchanged when the path is continuously deformed without being broken.

![A closed path deforms around a circle while its integer winding number remains unchanged](winding.gif)

The animation computes the winding number of a closed path around the circle. This number is always an integer and records both the number of turns and their direction. A generator of the circle's first cohomology measures this winding, so the first cohomology group is one copy of the integers.

Products of circles create more independent directions for loops. The product of two circles is the surface of a torus, which has one loop around its central opening and another around the body of the tube.

![A torus rotates in three dimensions with one loop around the central opening and another around the tube](torus.gif)

The rotating view makes the three-dimensional surface and its two independent loops visible. Products of more circles have higher-degree holes formed by choosing several circle directions at once. The lectures compute this pattern for any number of factors, including infinitely many ([Proposition 3.1, page 20](https://arxiv.org/pdf/2605.03658v1#page=20)).

![Rows of bars give the cohomology ranks for products of one through six circles and follow Pascal's triangle](ranks.png)

The chart shows the finite cases recomputed in this repository. Each row is a row of Pascal's triangle. For a product of several circles, the count in a given degree equals the number of ways to choose that many circle directions, exactly as the formula in the lectures predicts.

Two theorems connect this calculation to condensed mathematics. First, for every compact space, cohomology computed after translation to condensed sets agrees with classical cohomology ([Theorem 3.2, page 21](https://arxiv.org/pdf/2605.03658v1#page=21)). Second, when the coefficients are the usual real numbers rather than the integers, all positive-degree cohomology vanishes ([Theorem 3.3, page 22](https://arxiv.org/pdf/2605.03658v1#page=22)); degree zero records the continuous real-valued functions. This vanishing result is important later because it shows that the usual real line behaves very differently from the integer-based objects used in part two.

### The mathematics

Let $\mathbb T=\mathbb R/\mathbb Z$ be the circle. [Proposition 3.1, page 20 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=20) computes the cohomology of any product of circles:

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

**Reading the symbols.** The circle $\mathbb T$ is the real line $\mathbb R$ with numbers differing by an integer identified. The product sign combines one circle for each label $j$ in the index set $I$. The group $H^i$ is cohomology in degree $i$, with integer coefficients $\mathbb Z$. The symbol $\bigoplus$ is a direct sum, and $\bigwedge^i$ is the $i$th exterior power, which selects $i$ different circle directions at a time. The subscripts “sheaf” and “cond” name classical sheaf and condensed cohomology. The condition $i>0$ means every positive degree, while $H^0$ is degree zero. The notation $C(S,\mathbb R)$ means continuous real-valued functions on $S$.

**Why it matters.** For $n$ circles, the rank in degree $i$ is $\binom ni$, the number of ways to choose $i$ directions from $n$. The comparison theorem says that translating a compact space into condensed mathematics keeps these hole counts. Real coefficients behave differently because all positive-degree groups vanish.

**In the simulation.** The first control chooses the winding class in $H^1(\mathbb T,\mathbb Z)$. In torus mode, the two controls choose the two generators of $H^1(\mathbb T^2,\mathbb Z)$, and the readout lists the ranks $1,2,1$ predicted by the exterior-power formula.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/08.html)** to change a loop's winding number and then compare the two independent loop directions on a torus.

---

[← Nothing was lost](../07-nothing-was-lost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

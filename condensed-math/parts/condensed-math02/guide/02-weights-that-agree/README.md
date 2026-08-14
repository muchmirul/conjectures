# 2 · Weights that agree

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

A weighting turns the opening animation into a definition. Begin with one integer on the coarsest box of a probe. When that box is refined, assign integers to its smaller boxes whose sum equals the original integer. Continue at every level. The resulting family is compatible because the weight of any box always equals the sum of all weights immediately below it.

![Coarse and fine bar charts represent the same function and display an equal weighted total](integral.png)

This compatibility makes integration independent of the chosen level. A continuous integer-valued function on a probe is constant on the boxes of some finite stage. Multiply each of those values by its box's weight and add the finite list. If the stage is refined, the function value is repeated on the smaller boxes and their weights add back to the old weight, so the answer stays the same. The figure compares these two calculations, and the tests verify their agreement for both the halving and base-p probes.

The lectures call the group of all such weightings the free solid group on the probe. They define it as an inverse limit of finite groups, with one copy of the integers for every box and with refinement maps that add weights back together ([Definition 5.1, page 33](https://arxiv.org/pdf/2605.03658v1#page=33)). An element of this inverse limit is also called a measure because it assigns a compatible integer size to every box.

The simplest example concentrates one unit at a single point. Follow the branch leading to that point, place weight one on its box at every stage, and place zero on all other boxes. This is a Dirac measure. The code constructs these point measures, checks their compatibility, and uses them as the point-level data that more general weightings must extend.

The important simplification is that each stage contains only finite data. A weighting may involve infinitely many levels, but each level is just a finite list of integers, and compatibility is checked by finite addition. The next two sections study the functions being integrated and use their algebraic structure to classify all weightings.

### The mathematics

Let the profinite probe be $S=\varprojlim_i S_i$. [Definition 5.1, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) defines its free solid abelian group by

```math
\mathbb Z[S]^{\blacksquare}:=\varprojlim_i\mathbb Z[S_i]
\cong \operatorname{Hom}(C(S,\mathbb Z),\mathbb Z).
```

A compatible weighting is a family $\mu=(\mu_i)_i$. For every coarse box $a\in S_i$, it obeys

```math
\mu_i(a)=\sum_{b\in S_{i+1}:\,\pi_{i+1,i}(b)=a}\mu_{i+1}(b).
```

**Reading the symbols.** The probe $S$ is the inverse limit of finite stages $S_i$. The group $\mathbb Z[S_i]$ consists of finite integer weights on the boxes at stage $i$. The black square marks solid completion, and $\varprojlim$ keeps exactly the families that agree between stages. The notation $\operatorname{Hom}$ means additive maps, while $C(S,\mathbb Z)$ means continuous integer-valued functions on $S$. The weighting $\mu$ has one finite-stage list $\mu_i$ at each level. The symbol $a\in S_i$ means that $a$ is a coarse box. The sum runs over every finer box $b$ whose parent under $\pi_{i+1,i}$ is $a$.

**Why it matters.** The compatibility equation is what makes integration independent of the stage. Refining a box repeats the function value, while the weights below add back to the old weight.

**In the simulation.** Each slider changes the entries $\mu_{i+1}(b)$. The number shown on the parent is their sum. The assignment is accepted exactly when this equals $\mu_i(a)$ for every visible box.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/02.html)** to split weights across finer boxes and see which assignments satisfy the compatibility rule.

---

[← Sums with nowhere to land](../01-sums-with-nowhere-to-land/README.md)  ·  [Every function is a stack of steps →](../03-stacks-of-steps/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

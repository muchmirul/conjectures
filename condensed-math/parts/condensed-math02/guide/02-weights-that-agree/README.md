# 2 · Compatible weights on a probe

*Part 2 of three: Giving Infinite Sums a Meaning. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

A measure on a probe is built from finite lists of integer weights. Begin with one weight on the first stage. Whenever a box is divided, give integer weights to its children whose sum is the parent's weight. Continue through every stage. The weight on any box must always equal the total weight of the finer boxes inside it.

![Coarse and fine bars show the same function and produce the same weighted total](integral.png)

This rule makes integration independent of the stage. A continuous integer-valued function on a compact probe is constant on the boxes of some finite stage. To integrate it, multiply each value by the weight of its box and add the finite list. At a finer stage, the function value repeats on the child boxes and their weights add back to the parent weight. The total therefore stays unchanged.

The lectures define the **free solid abelian group** on a probe as the group of all these compatible weightings ([Definition 5.1, page 33](https://arxiv.org/pdf/2605.03658v1#page=33)). It is an inverse limit of finite groups, one integer coordinate for every box at every stage. The word *measure* is appropriate because each element gives a compatible integer size to every box.

A simple example puts one unit of weight at one point. Follow the branch leading to that point. Put weight one on its box at each stage and zero on every other box. This is a **Dirac measure**. More general measures spread positive and negative integer weights across many branches.

Each visible stage still contains only finite data. The infinite part is the requirement that all these finite lists agree. The next two chapters study the functions we integrate and describe the full group of compatible measures.

### The mathematics

Let $S=\varprojlim_i S_i$ be a profinite probe. [Definition 5.1, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) defines its free solid abelian group by

```math
\mathbb Z[S]^{\blacksquare}:=\varprojlim_i\mathbb Z[S_i]
\cong \operatorname{Hom}(C(S,\mathbb Z),\mathbb Z).
```

A compatible weighting is a family $\mu=(\mu_i)_i$. For every box $a\in S_i$, it satisfies

```math
\mu_i(a)=\sum_{b\in S_{i+1}:\,\pi_{i+1,i}(b)=a}\mu_{i+1}(b).
```

**Reading the symbols.** The probe $S$ is the inverse limit of its finite stages $S_i$. The group $\mathbb Z[S_i]$ contains finite integer weights on the boxes at stage $i$. The black square marks solid completion. The inverse limit $\varprojlim$ keeps the families that agree at every stage. The notation $\operatorname{Hom}$ means additive maps, and $C(S,\mathbb Z)$ means continuous integer-valued functions on $S$. The measure $\mu$ has one list $\mu_i$ at each stage. The expression $a\in S_i$ says that $a$ is a box at stage $i$. The sum includes every child box $b$ whose parent under $\pi_{i+1,i}$ is $a$.

**Why it matters.** The compatibility equation guarantees that refining a stage does not change an integral. The function value repeats on the children, and their weights add up to the old weight.

**In the simulation.** Each slider changes one child weight $\mu_{i+1}(b)$. The number on the parent is their sum. A weighting is accepted only when that sum equals $\mu_i(a)$ for every displayed parent.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/02.html)** to split weights among child boxes and test the compatibility rule.

---

[← One series, two ideas of distance](../01-sums-with-nowhere-to-land/README.md)  ·  [A basis for integer-valued functions →](../03-stacks-of-steps/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

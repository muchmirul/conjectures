# Giving Infinite Sums a Meaning

*This is the second of three parts on condensed mathematics. Part one replaced a space by the continuous maps from probes into it, which made kernels and cokernels reliable. We now use those probes to understand infinite sums. Compatible weights on their finite stages lead to solid groups and also recover the holes of familiar spaces. Only part one is assumed.*

![A number on one box is divided among finer branches while every stage keeps the same total](guide/00-start-here/hero.gif)

Place an integer weight on the first box of a probe. When the box splits, distribute its weight among the new boxes so that their weights add up to the old one. Repeat this at every stage. The result is a **compatible weighting**, or an integer-valued measure. Every stage contains only finitely many weights, and compatibility makes the total independent of the stage where we calculate it.

This part covers Lectures IV to VI of Peter Scholze's *Lectures on Condensed Mathematics* ([arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026), which present joint work with Dustin Clausen. [Part one](../condensed-math01/ARTICLE.md) introduced profinite probes and condensed sets. Part three will give different rings their own theories of measures. Each chapter below includes an activity that turns its main definition into a finite example. The [part-two activity list](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/index.html) links to all nine pages.

```
    understand the problem      1  one series and two ideas of distance
    build the ingredients       2  compatible weights on a probe
                               3  integer-valued functions have a basis
                               4  products and direct sums exchange roles
    state the rule              5  unique extension from points to measures
    follow two consequences     6  why the usual real line disappears
                               7  completed tensor products
    return to topology          8  solidification recovers homology
```

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/00.html)** by distributing weights through several stages and checking that every stage has the same total.

## 1 · One series, two ideas of distance

Consider the series that begins with 1 and then keeps doubling: 1, 2, 4, 8, and so on. Its partial sums are 1, 3, 7, 15, and 31. Under the usual distance, these totals grow without bound, so the series does not converge.

Now choose an integer $p$ and use a different measure of size. A number is small when it is divisible by a high power of $p$. For $p=2$, this makes 1024 smaller than 16, and 16 smaller than 4. This rule is the **2-adic absolute value**.

![The same partial sums move away on the usual number line but enter smaller nested regions in 2-adic distance](guide/01-sums-with-nowhere-to-land/padic_walk.gif)

Under 2-adic distance, the gaps between successive partial sums are 2, 4, 8, 16, and so on. Each new gap is smaller than the previous one because it has another factor of two. The partial sums settle into smaller and smaller regions of the base-two probe even while they grow on the usual real line.

![A logarithmic chart shows the usual error increasing and the 2-adic error decreasing](guide/01-sums-with-nowhere-to-land/distance.png)

The calculation uses exact arithmetic. The usual distance from a partial sum to minus one doubles after each term. Its 2-adic distance to minus one is cut in half. The series therefore converges to minus one in the 2-adic integers. It still diverges under the usual distance, and there is no contradiction because the two distances define different notions of convergence.

This example shows that a list of terms does not determine the value of an infinite sum. We also need a completion rule that says when the partial sums become close and what their limit is. Condensed sets already carry topological information through probes, so we will express this rule using probe data rather than adding a separate topology afterward.

### The mathematics

The motivation at the start of [Lecture V, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) can be illustrated by a geometric series. Let $p\ge2$. The sum of the first $n$ terms and its $p$-adic limit satisfy

```math
s_n=\sum_{k=0}^{n-1}p^k=\frac{p^n-1}{p-1},
\qquad
s_n-\frac{1}{1-p}=\frac{p^n}{p-1},
\qquad
s_n\xrightarrow[n\to\infty]{\,p\text{-adic}\,}\frac{1}{1-p}.
```

For $p=2$, this becomes

```math
1+2+4+8+\cdots=-1\quad\text{in }\mathbb Z_2.
```

**Reading the symbols.** The integer $p$ is the chosen base and is at least two. The symbol $s_n$ means the total after $n$ terms. The summation sign adds $p^k$ while $k$ runs from zero to $n-1$. The fractions are algebraic forms of the same finite sum and its error. The long arrow says that $s_n$ converges as $n$ tends to infinity when distance is measured $p$-adically. The dots mean that the powers continue forever. The symbol $\mathbb Z_2$ means the 2-adic integers.

**Why it matters.** The error contains a factor $p^n$, so its $p$-adic size is $p^{-n}$ and approaches zero. Its usual size increases instead. The chosen completion, not just the terms, determines whether the series converges.

**In the simulation.** The base control chooses $p$, and the term control chooses $n$. One panel shows $s_n$ growing under ordinary distance. The nested panel shows its $p$-adic error shrinking toward $1/(1-p)$, which is minus one when $p=2$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/01.html)** to change the base and compare both distances for the same partial sums.

## 2 · Compatible weights on a probe

A measure on a probe is built from finite lists of integer weights. Begin with one weight on the first stage. Whenever a box is divided, give integer weights to its children whose sum is the parent's weight. Continue through every stage. The weight on any box must always equal the total weight of the finer boxes inside it.

![Coarse and fine bars show the same function and produce the same weighted total](guide/02-weights-that-agree/integral.png)

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

## 3 · A basis for integer-valued functions

We next study continuous functions from a probe to the integers. Different integers are separated from one another. Because the probe is compact, a continuous integer-valued function must become constant on every box at some finite stage. We can then read it as a finite list of integers.

![Indicator functions are added one box at a time until they reproduce the chosen integer-valued function](guide/03-stacks-of-steps/steps.gif)

At one finite stage, define one **indicator function** for each box. It equals one on that box and zero on all the others. Multiplying these functions by integers and adding them reproduces any integer-valued function on the stage. The animation builds the chosen function in this way.

The stronger statement covers all stages at once. The continuous integer-valued functions on a complete profinite probe form an abelian group under addition. Nöbeling's theorem says that this group is free. In other words, it has a basis such that every function has one unique expression using finitely many basis functions and integer coefficients.

![For each tested finite stage, the number of constructed basis elements equals the number of boxes](guide/03-stacks-of-steps/basis_size.png)

Nöbeling extended earlier work by Specker, and the lectures present a proof due to Bergman ([Theorem 5.4, page 34](https://arxiv.org/pdf/2605.03658v1#page=34)). The code follows the construction at finite stages. It keeps a new indicator product only when the functions already selected cannot generate it. The tests then verify that the selected functions form a basis.

This finite calculation is only an illustration. Every group of functions on one finite set is automatically free. Nöbeling's theorem says something deeper: the full group of continuous functions on the infinite probe is also free. We quote that theorem from the lectures rather than claiming that a finite test proves it.

### The mathematics

[Nöbeling's theorem, Theorem 5.4 on page 34 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=34), states

```math
C(S,\mathbb Z)\cong\bigoplus_{e\in E}\mathbb Z e.
```

Thus every $f\in C(S,\mathbb Z)$ has one finite expression. The display below records the basis elements and coefficients used for that function:

```math
f=\sum_{e\in F}n_e e,
\qquad F\subset E\text{ finite},
\qquad n_e\in\mathbb Z.
```

**Reading the symbols.** The group $C(S,\mathbb Z)$ contains the continuous integer-valued functions on $S$. The set $E$ is a basis. The direct sum $\bigoplus$ means that each function uses only finitely many basis elements. The expression $\mathbb Z e$ means all integer multiples of $e$. The letter $f$ names one function. The finite subset $F$ lists the basis functions used to build it, and $n_e$ is the integer coefficient of $e$. The symbol $\in$ means “belongs to,” and $\subset$ means “is a subset of.”

**Why it matters.** A measure can be viewed as an additive map from $C(S,\mathbb Z)$ to $\mathbb Z$. Once this function group has a basis, such a map is determined by an independent integer value on each basis element. This gives the product description in the next chapter.

**In the simulation.** The target control chooses a function $f$ on one finite stage. Adding basis functions enlarges $F$. Each filled bar shows a term $n_e e$. The reconstruction is complete when their sum equals $f$ on every box. This demonstrates the finite case only.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/03.html)** to rebuild an integer-valued function from indicator functions.

## 4 · Products and direct sums

There are two common ways to store a family of integers. A **product** allows an integer in every coordinate, with no limit on how many are nonzero. A **direct sum** uses the same coordinates but requires each element to have only finitely many nonzero entries.

![An infinite product allows nonzero values everywhere, while a direct sum allows only finitely many nonzero values](guide/04-products-in-sums-out/product_sum.png)

Specker's theorem says that an additive map from a countable product of integers to the integers can depend on only finitely many coordinates. Therefore, all such maps form a direct sum of copies of the integers.

![A homomorphism reads only a finite group of coordinates and ignores the rest of the product](guide/04-products-in-sums-out/finite_reach.gif)

The proof uses divisibility. Far enough along the product, one can arrange data divisible by increasingly high powers of an integer. Any output that respected all those divisibility relations would have to be divisible by every power. The only integer with that property is zero. The full proof is quoted rather than reproduced here.

Maps from a direct sum behave in the opposite way. Each input has finite support, so we may choose one coefficient for every coordinate without ever evaluating an infinite numerical sum. The group of maps from a direct sum to the integers is therefore a product.

Nöbeling's theorem says that $C(S,\mathbb Z)$ is a direct sum indexed by a basis. A measure is an integer-valued homomorphism on this group. Taking all such homomorphisms changes the direct sum into a product. This is [Corollary 5.5, page 34](https://arxiv.org/pdf/2605.03658v1#page=34): the free solid group on a probe is a product of copies of the integers. These products will serve as the basic projective objects in the category of solid groups.

### The mathematics

Specker's theorem describes maps from a product to the integers. Together with [Corollary 5.5, page 34 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=34), it gives

```math
\operatorname{Hom}_{\mathrm{Ab}}\!\left(
\prod_{n\in\mathbb N}\mathbb Z,\mathbb Z\right)
\cong\bigoplus_{n\in\mathbb N}\mathbb Z,
\qquad
\operatorname{Hom}_{\mathrm{Ab}}\!\left(
\bigoplus_{i\in I}\mathbb Z,\mathbb Z\right)
\cong\prod_{i\in I}\mathbb Z.
```

The basis, and therefore its index set, depends on the probe. For the resulting index set $I$, we obtain

```math
\mathbb Z[S]^{\blacksquare}\cong\prod_{i\in I}\mathbb Z.
```

**Reading the symbols.** The notation $\operatorname{Hom}_{\mathrm{Ab}}$ means additive maps of abelian groups. The first product has one coordinate for each natural number $n\in\mathbb N$. The letter $I$ is a general index set. A product $\prod$ permits infinitely many nonzero coordinates. A direct sum $\bigoplus$ permits only finitely many. The first isomorphism says that a homomorphism from a countable product to $\mathbb Z$ reads only finitely many coordinates. The second says that a homomorphism from a direct sum may choose one coefficient for every coordinate. The black square on $\mathbb Z[S]^{\blacksquare}$ marks the free solid group on $S$.

**Why it matters.** Nöbeling's theorem writes the function group as a direct sum. Taking its integer dual turns that direct sum into the product shown above. Products of integer groups are therefore the basic free objects for solid mathematics.

**In the simulation.** The reach control chooses the finite set of coordinates read by one homomorphism. Changing a coordinate inside that set can change the output. Changing one outside it cannot. The finite model illustrates Specker's conclusion but does not prove the infinite theorem.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/04.html)** to change coordinates inside and outside a homomorphism's finite range.

## 5 · The unique-extension rule

We can now define a **solid abelian group**. Start with a map from the points of a probe into a condensed group. Each point gives a Dirac measure, but the probe also has general compatible integer measures. The group is solid when every point map extends in exactly one way to all these measures.

![Values assigned to probe points extend to one map on every compatible measure](guide/05-the-solid-rule/extension.gif)

Existence means that every compatible measure can be integrated in the group. Uniqueness means that the values on points cannot lead to two different results. Together, these requirements make summation part of the group's structure rather than an extra choice for each infinite expression.

The lectures give the definition in [Definition 5.1, page 33](https://arxiv.org/pdf/2605.03658v1#page=33). They then prove that solid groups form an abelian category closed under limits, colimits, and extensions. Products of copies of $\mathbb Z$ are compact projective generators. In addition, every condensed abelian group has a **solidification**, which is the universal map from that group into the solid setting. These facts come from [Theorem 5.8, page 35](https://arxiv.org/pdf/2605.03658v1#page=35) and [Corollary 6.1, page 42](https://arxiv.org/pdf/2605.03658v1#page=42).

![Sample groups are marked according to whether point maps extend uniquely to compatible measures](guide/05-the-solid-rule/solid_or_not.png)

The integers are solid, as is every product of copies of the integers. The $p$-adic integers and formal power-series groups are also solid. A direct sum of infinitely many integer groups is not solid because it does not contain every needed infinite coordinate family. The usual real numbers also fail this integer-based rule, for a different reason explained next.

### The mathematics

[Definition 5.1, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) says that a condensed abelian group $A$ is solid when every point map extends uniquely:

```math
\forall S,\quad
\operatorname{Hom}(\mathbb Z[S]^{\blacksquare},A)
\xrightarrow{\sim}
\operatorname{Hom}(\mathbb Z[S],A).
```

[Theorem 5.8, page 35](https://arxiv.org/pdf/2605.03658v1#page=35) provides universal solidification:

```math
(-)^{\blacksquare}:\operatorname{Cond}(\mathrm{Ab})\longrightarrow\operatorname{Solid},
\qquad
\operatorname{Hom}_{\operatorname{Solid}}(M^{\blacksquare},A)
\cong
\operatorname{Hom}_{\operatorname{Cond}(\mathrm{Ab})}(M,A).
```

**Reading the symbols.** The phrase $\forall S$ means “for every profinite probe $S$.” The group $\mathbb Z[S]$ is the free condensed group on the points of $S$, and the black square gives its free solid completion. The arrow marked $\sim$ is a bijection. It says that restricting a map from all compatible measures to the point measures loses no information and introduces no choice. The functor $(-)^{\blacksquare}$ sends a condensed abelian group $M$ to its solidification $M^{\blacksquare}$. The notation $\operatorname{Solid}$ names the category of solid groups, and $\operatorname{Cond}(\mathrm{Ab})$ names condensed abelian groups. The second line is the universal property: maps from $M^{\blacksquare}$ to a solid group $A$ are the same as maps from $M$ to $A$.

**Why it matters.** The first bijection combines the existence and uniqueness of integration. The theorem creates a universal way to turn any condensed group into a solid one and gives the solid category the algebraic closure properties needed later.

**In the simulation.** Selecting a group chooses $A$. A green result means that every point map in the listed example has one extension. A red result reports a failure of existence or uniqueness. The examples use the cited theorems; the finite activity does not prove those theorems.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/05.html)** to compare familiar groups and read why each one passes or fails the solid rule.

## 6 · Why the usual real line disappears

Derived solidification sends the usual additive real line to zero ([Corollary 6.1 (iii), page 42](https://arxiv.org/pdf/2605.03658v1#page=42)). A divisibility argument explains the main obstruction, although the full proof needs an additional derived calculation.

![Repeated division stays inside the real numbers but eventually leaves the integers](guide/06-where-the-real-line-goes/divisible.gif)

Every real number can be divided by any positive integer and remain a real number. A group with this property is called **divisible**. The integers are not divisible because, for example, one divided by two is not an integer.

Consider an additive map from the real numbers to the integers. A real number is divisible by every positive integer, and an additive map preserves those divisibility relations. Its image would have to be an integer divisible by every positive integer. Only zero has that property, so every such map is zero. The same argument works one coordinate at a time for a product of integer groups.

![Every coordinate of a map from the divisible real group into an integer product is forced to be zero](guide/06-where-the-real-line-goes/no_map.png)

This argument proves that the real line maps trivially into the projective building blocks of the solid category. It does not by itself prove that derived solidification sends the real line to zero. The complete result also uses the universal-resolution calculation in [Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25).

The result does not say that real analysis is unimportant. The solid rule in this part is based on integer-valued measures and suits nonarchimedean sizes such as the $p$-adic absolute value. The usual real absolute value behaves differently, as the lectures note when introducing solidity ([page 33](https://arxiv.org/pdf/2605.03658v1#page=33)). Part three introduces a separate real-valued theory of measures.

The vanishing also has a use. Real-valued correction terms disappear in some condensed calculations instead of creating additional obstructions. Lecture IV uses this fact in the calculation that supports the structure theorem for solid groups.

### The mathematics

An abelian group $D$ is divisible if every element can be divided by every positive integer. In symbols, this means

```math
\forall x\in D,\ \forall n\ge1,\ \exists y\in D\text{ such that }ny=x.
```

Every homomorphism from a divisible group to a product of integer groups is zero:

```math
\operatorname{Hom}\!\left(D,\prod_{i\in I}\mathbb Z\right)=0.
```

The usual additive real line is divisible, but the lectures prove a stronger result than the homomorphism calculation alone. [Corollary 6.1 (iii), page 42 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=42) gives

```math
\mathbb R^{L\blacksquare}=0.
```

**Reading the symbols.** The letter $D$ names an abelian group. The symbols $\forall$ and $\exists$ mean “for every” and “there exists.” The relation $x\in D$ says that $x$ belongs to $D$, while $n\ge1$ chooses any positive integer. The equation $ny=x$ means that adding $y$ to itself $n$ times gives $x$. The product has one integer group for each label in $I$. The equation $\operatorname{Hom}=0$ means that every additive map to this product is the zero map. The superscript $L\blacksquare$ means derived solidification, and the final $0$ is the zero object.

**Why it matters.** Divisibility explains why the reals have no nonzero map to the compact projective generators of solid groups. The stronger equation $\mathbb R^{L\blacksquare}=0$ also relies on [Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25), so the arithmetic argument explains the obstruction without claiming to prove the corollary.

**In the simulation.** Choose a group $D$ and increase the divisor $n$. The real line always contains $y=x/n$, while the integers eventually do not. The final readout shows what this implies for a map into one integer coordinate.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/06.html)** to compare repeated division in the reals, integers, and $p$-adic examples.

## 7 · Completed tensor products

Solid groups have a product operation called the **completed tensor product**. It combines two solid groups while keeping track of the completion carried by each one. The resulting group represents additive operations that depend on one input from each side.

![A table gives completed tensor products of integer, p-adic, power-series, and real groups](guide/07-the-multiplication-table/tensor_table.png)

Choose one group from a row and another from a column. The 2-adic integers tensored with the 3-adic integers give zero. The 2-adic integers tensored with themselves give the 2-adic integers again. Tensoring the 2-adic integers with the real numbers also gives zero, in agreement with chapter 6. Two one-variable power-series groups combine into a two-variable power-series group.

![Scales formed from powers of two and powers of three do not share a common direction of completion](guide/07-the-multiplication-table/rulers.gif)

The mixed 2-adic and 3-adic case can be understood through their scales. The 2-adic completion uses divisibility by powers of two. In that setting, three is invertible and does not define a finer scale. The 3-adic completion reverses these roles. The two completion directions are incompatible. The picture illustrates the vanishing in [Example 6.4, page 44](https://arxiv.org/pdf/2605.03658v1#page=44), but it is not a proof.

For power series, a series in $U$ has one coordinate for every nonnegative power of $U$, and a series in $T$ has one for every nonnegative power of $T$. Pairing the coordinate sets gives one coordinate for every pair of powers. Such a pair is a monomial in $U$ and $T$, so the result is a two-variable power series ([Proposition 6.3, page 43](https://arxiv.org/pdf/2605.03658v1#page=43)). The repository tests this indexing calculation. The other displayed identities are quoted from the lectures.

### The mathematics

[Proposition 6.3, page 43 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=43) states that the completed tensor product multiplies the coordinate sets of integer products:

```math
\left(\prod_{i\in I}\mathbb Z\right)\otimes^{L}_{\blacksquare}
\left(\prod_{j\in J}\mathbb Z\right)
\cong
\prod_{(i,j)\in I\times J}\mathbb Z.
```

The result depends on whether the completion directions agree. For distinct primes $p\neq\ell$, [Example 6.4, page 44](https://arxiv.org/pdf/2605.03658v1#page=44) gives

```math
\mathbb Z_p\otimes^{L}_{\blacksquare}\mathbb R=0,
\quad
\mathbb Z_p\otimes^{L}_{\blacksquare}\mathbb Z_\ell=0,
\quad
\mathbb Z_p\otimes^{L}_{\blacksquare}\mathbb Z_p\cong\mathbb Z_p,
```

```math
\mathbb Z_p\otimes^{L}_{\blacksquare}\mathbb Z[[T]]\cong\mathbb Z_p[[T]],
\qquad
\mathbb Z[[U]]\otimes^{L}_{\blacksquare}\mathbb Z[[T]]
\cong\mathbb Z[[U,T]].
```

**Reading the symbols.** The sets $I$ and $J$ label two families of integer coordinates, and $I\times J$ is the set of ordered pairs of labels. The product signs permit unrestricted coordinates. The symbol $\otimes^{L}_{\blacksquare}$ is the derived solid tensor product from [Theorem 6.2, page 43](https://arxiv.org/pdf/2605.03658v1#page=43). The groups $\mathbb Z_p$ and $\mathbb Z_\ell$ are the $p$-adic and $\ell$-adic integers for different primes. The notation $\mathbb Z[[T]]$ means formal power series in $T$, and $\mathbb Z[[U,T]]$ means formal power series in both variables. The symbol $0$ is the zero object, and $\cong$ means isomorphic.

**Why it matters.** Compatible completion directions remain together, while incompatible prime directions give zero. For products of integer coordinates, the tensor product pairs every coordinate on one side with every coordinate on the other.

**In the simulation.** Row and column controls choose the tensor factors. The selected cell displays the corresponding identity. The readout also says whether the lectures state the entry directly or whether it follows by relabelling the coordinate rule.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/07.html)** to choose two solid groups and inspect their completed tensor product.

## 8 · Solidification recovers homology

We can now return from infinite sums to topology. Begin with a circle, sphere, torus, or another space built from cells. Form the free condensed abelian group on its points, then apply derived solidification.

![A torus rotates in three dimensions beside bars for homology in degrees zero, one, and two](guide/08-solidify-a-shape/solidify.gif)

The homology groups of the result are the classical integral homology groups of the original space ([Example 6.5, page 44](https://arxiv.org/pdf/2605.03658v1#page=44)). Degree zero records connected components, degree one records loop classes, and degree two can record enclosed surfaces. Higher degrees describe higher-dimensional versions. The result also keeps torsion, which is information about classes killed by multiplication by an integer.

![Free and torsion homology classes are compared for a circle, figure eight, sphere, torus, and Klein bottle](guide/08-solidify-a-shape/homology_bars.png)

The chart is computed from cellular boundary maps using Smith normal form over the integers. A circle has one degree-one class, and a figure eight has two. A sphere has one degree-two class and no degree-one class. A torus has two degree-one classes and one degree-two class. A Klein bottle has one free degree-one class and one torsion class of order two. Doubling that torsion class gives zero.

The theorem connects the ideas from both parts. Part one showed that translating a compact space into condensed mathematics preserves integral cohomology. This part described solidification through maps from products of integers. The lectures combine these facts to identify derived solidification of the free group on a space with singular homology.

The definition of solidity mentions compatible sums rather than loops or surfaces. Even so, its universal completion recovers a standard topological invariant. Completion and topology therefore fit inside the same framework.

### The mathematics

For a CW complex $X$, [Example 6.5, page 44 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=44) identifies derived solidification with singular homology:

```math
\mathbb Z[X]^{L\blacksquare}\cong H_\bullet(X;\mathbb Z).
```

We can apply the theorem to several familiar spaces. For the circle, sphere, and torus, it gives

```math
H_\bullet(S^1;\mathbb Z)=(\mathbb Z,\mathbb Z),
\quad
H_\bullet(S^2;\mathbb Z)=(\mathbb Z,0,\mathbb Z),
\quad
H_\bullet(T^2;\mathbb Z)=(\mathbb Z,\mathbb Z^2,\mathbb Z).
```

**Reading the symbols.** The space $X$ is a CW complex, meaning that it is built from cells. The object $\mathbb Z[X]$ is the free condensed abelian group on its points. The superscript $L\blacksquare$ means derived solidification. The notation $H_\bullet(X;\mathbb Z)$ means all singular homology groups of $X$ with integer coefficients, arranged by degree. The symbols $S^1$ and $S^2$ are the circle and sphere, while $T^2$ is the torus. Each list begins with degree zero and then gives the higher degrees in order. The expression $\mathbb Z^2$ means two independent copies of the integers.

**Why it matters.** A completion defined by compatible infinite sums recovers integral homology. Because the construction is derived, groups can appear in several degrees, and it keeps integer torsion such as the order-two class of the Klein bottle.

**In the simulation.** The shape control chooses $X$. Bars display the homology groups by degree, and the camera rotates the three-dimensional examples. A brown bar labelled two represents a $\mathbb Z/2\mathbb Z$ torsion class, not two free copies of $\mathbb Z$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/08.html)** to compare the homology of five spaces and rotate the three-dimensional models.

## What part two established

A measure on a profinite probe is a compatible family of finite integer weightings. A solid group is a condensed group in which values on points extend uniquely to all such measures. Nöbeling's theorem and integer duality describe the free solid groups as products of copies of the integers. Universal solidification places any condensed group in this setting, and derived solidification of a space recovers its integral homology.

This integer-based rule is nonarchimedean. It sends the usual real line to zero, so it cannot be the measure theory for real analysis. Part three allows a ring to carry its own theory of measures. That change brings back the real numbers, adds multiplication, and opens the way to geometry.

**[Part three: Measure Rules for Rings and Geometry](../condensed-math03/ARTICLE.md)**

## How this part lines up with the lectures

| this guide | in the lectures |
|---|---|
| chapter 1, two distances | the motivation opening Lecture V, page 33 |
| chapter 2, compatible weights | Definition 5.1, page 33, the free solid group |
| chapter 3, integer-valued functions | Theorem 5.4, page 34, Nöbeling's theorem and Bergman's proof |
| chapter 4, products and direct sums | Corollary 5.5, page 34, and the biduality in Proposition 5.7, page 35 |
| chapter 5, the solid rule | Definition 5.1, page 33; Theorem 5.8, page 35; Corollary 6.1, page 42 |
| chapter 6, the real line | Corollary 6.1 (iii), page 42; Theorem 4.3, page 25; the footnote on page 33 |
| chapter 7, completed tensor products | Theorem 6.2 and Proposition 6.3, page 43; Example 6.4, page 44 |
| chapter 8, homology | Example 6.5, page 44 |

## Checking it yourself

You can regenerate the figures and rerun the finite calculations used in this part. Run the following commands from a terminal:

```
cd condensed-math
make venv
make test
make figures
```

For this part, the tests:

- calculate the doubling series exactly and compare its usual and 2-adic errors
- build compatible measures on halving and base-$p$ probes
- verify that integration gives the same result at coarse and fine stages
- run Bergman's finite-stage basis construction and compare basis size with box count
- pair the coordinate sets of one-variable power series and recover the coordinates of a two-variable series
- check that the recorded tensor-product table is symmetric and follows the stated completion rule
- compute homology from cellular boundary maps using Smith normal form, including the Klein bottle's order-two class

The tests do not prove the infinite and categorical theorems. Nöbeling's theorem, the structure theorem for solid groups, the vanishing of the solidified real line, and the identification with homology are quoted from the lectures. The file `notes/research-content.md` labels each claim as computed, a finite illustration, derived, or quoted.

## Glossary

| phrase used in this guide | standard mathematical term |
|---|---|
| a compatible weighting | a measure on a profinite set |
| the rule that child weights add to the parent | compatibility in an inverse limit |
| small when divisible by a high power of $p$ | the $p$-adic absolute value |
| the base-$p$ integers | the $p$-adic integers |
| weight one at one point | a Dirac measure |
| an unrestricted family of coordinates | a product |
| a family with finite support | a direct sum |
| an additive map | a group homomorphism |
| a group with unique integration of compatible measures | a solid abelian group |
| the universal passage to a solid group | solidification |
| the product that keeps completion data | the solid tensor product |
| a direction of completion | an adic topology |
| divisible by every positive integer | a divisible group |
| the topological invariants recovered after solidification | singular homology groups |
| a class killed by a nonzero integer | a torsion class |
| the basic product objects | compact projective generators |

## Further reading

- Peter Scholze, *Lectures on Condensed Mathematics*, [arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026, joint work with Dustin Clausen. Lectures IV to VI are the source for this part.
- E. Specker, “Additive Gruppen von Folgen ganzer Zahlen” (1950), and G. Nöbeling, “Verallgemeinerung eines Satzes von Herrn E. Specker” (1968), cited by the lectures for Theorem 5.4.
- `notes/research-content.md`, for a claim-by-claim record of what is computed and what is quoted.

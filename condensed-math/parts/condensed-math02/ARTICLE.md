# Infinite Sums That Finally Land

*Part two of three on condensed mathematics. Part one made subtraction reliable by replacing spaces with their answers to probes. We now ask when an infinite sum has one well-defined value. Compatible weights on the finite stages of a probe lead to the solid rule, reveal the basic structure of solid groups, and recover the holes of familiar spaces. Only part one is assumed.*

![An initial weight is divided among finer branches while every level keeps the same total](guide/00-start-here/hero.gif)

The animation shows the main construction of this part. Place an integer weight on the first box of a probe. Whenever a box splits, divide its weight among the new boxes so that their weights add back to the old one. Repeating this at every level produces a compatible family called a **weighting**, or, in standard language, an integer-valued measure. Because every level is finite and the totals agree between levels, a weighting gives a controlled way to interpret sums over all the points of a probe.

This is part two of three, covering Lectures IV to VI of Peter Scholze's *Lectures on Condensed Mathematics* ([arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026), joint work with Dustin Clausen. [Part one](../condensed-math01/ARTICLE.md) introduced probes and condensed sets, and those ideas will be used here. Part three extends the resulting theory from groups to rings and geometry. Most sections include a [page you can play with](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/index.html), so each new definition can be tested on a finite example.

```
    the problem again           1  sums with nowhere to land
    the answer                  2  weights that agree
                                3  every function is a stack of steps
                                4  products in, sums out
    the rule                    5  the solid rule
    two consequences            6  where the real line goes
                                7  the multiplication table
    the payoff                  8  solidify a shape, get its holes
```

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/00.html)** to distribute weights through a probe and check that every refinement preserves the total above it.

## 1 · Sums with nowhere to land

Part one repaired kernels and cokernels, but it did not define infinite addition. Consider the series obtained by adding 1, then 2, then 4, then 8, and continuing to double. Its partial sums are 1, 3, 7, 15, 31, and so on. With ordinary distance, these values move farther and farther away, so the series does not converge.

Now use a different measure of size. Fix the number two and declare an integer to be smaller when it is divisible by a larger power of two. Under this rule, 16 is smaller than 4, and 1024 is smaller than 16. This is the 2-adic absolute value, the notion of size carried by the base-two probe from part one.

![Partial sums grow without bound in ordinary distance but enter successively smaller nested regions in 2-adic distance](guide/01-sums-with-nowhere-to-land/padic_walk.gif)

The same partial sums now have a different behaviour. Consecutive gaps are 2, 4, 8, and 16, which become progressively smaller in 2-adic size. The partial sums therefore settle into finer and finer boxes of the base-two probe. The animation places this convergence beside their divergence on the ordinary real line.

![A logarithmic chart shows ordinary error doubling and 2-adic error halving with each added term](guide/01-sums-with-nowhere-to-land/distance.png)

The chart uses exact arithmetic from this repository. The ordinary distance from the partial sum to minus one doubles at each step, while its 2-adic distance halves. Thus, in the 2-adic number system, the series converges to minus one. There is no contradiction: convergence depends on the chosen notion of distance, and the ordinary and 2-adic distances are different.

This example identifies what an infinite sum needs in addition to its terms. It needs a rule that says when partial sums are close and what their limit should be. In other words, infinite addition depends on topology or an equivalent completion rule. Condensed sets already carry topological information inside their responses to probes, so the next task is to express summation through those responses rather than by adding an external topology again.

### The mathematics

The convergence problem that opens [Lecture V, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) can be seen in a geometric series. For an integer base $p\ge2$, the first $n$ terms form a finite sum, and the same algebraic identity gives its limit in the $p$-adic numbers:

```math
s_n=\sum_{k=0}^{n-1}p^k=\frac{p^n-1}{p-1},
\qquad
s_n-\frac{1}{1-p}=\frac{p^n}{p-1},
\qquad
s_n\xrightarrow[n\to\infty]{\,p\text{-adic}\,}\frac{1}{1-p}.
```

The base-two case gives the example used in the pictures. Its limit is

```math
1+2+4+8+\cdots=-1\quad\text{in }\mathbb Z_2.
```

**Reading the symbols.** The integer $p$ is the chosen base and is at least two. The symbol $s_n$ names the running total after $n$ terms. The summation sign adds $p^k$ as the exponent $k$ runs from zero to $n-1$. The fractions are ordinary algebraic rearrangements of that finite sum. The long arrow says that $s_n$ converges as $n$ tends to infinity when distance is measured $p$-adically. The dots mean that the powers continue forever. The symbol $\mathbb Z_2$ means the 2-adic integers, not the ordinary integers.

**Why it matters.** The error is a multiple of $p^n$, so its $p$-adic size is $p^{-n}$ and tends to zero. Its ordinary size grows instead. The terms alone therefore do not determine convergence; the chosen completion does.

**In the simulation.** The base control chooses $p$, and the terms control chooses $n$. The ordinary panel shows $s_n$ growing. The nested panel shows the $p$-adic error shrinking toward $1/(1-p)$, which equals minus one when $p=2$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/01.html)** to change the base and compare the ordinary and base-p distances of the same partial sums.

## 2 · Weights that agree

A weighting turns the opening animation into a definition. Begin with one integer on the coarsest box of a probe. When that box is refined, assign integers to its smaller boxes whose sum equals the original integer. Continue at every level. The resulting family is compatible because the weight of any box always equals the sum of all weights immediately below it.

![Coarse and fine bar charts represent the same function and display an equal weighted total](guide/02-weights-that-agree/integral.png)

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

## 3 · Every function is a stack of steps

We first examine continuous functions from a probe to the integers. Since distinct integers are separated from one another, continuity prevents such a function from changing indefinitely inside smaller and smaller nearby regions. On a compact probe, it becomes constant on every box of some finite stage. The function can therefore be read as a finite list of integer values.

![Indicator functions fill one box at a time until their integer combination matches the target function](guide/03-stacks-of-steps/steps.gif)

At one finite stage, the basic step functions are easy to see. For each box, use the function that equals one on that box and zero elsewhere. Multiplying these indicators by integers and adding them reconstructs any function on the stage. The animation performs this reconstruction one basis element at a time, without introducing fractions.

The deeper statement concerns all stages at once. Under addition, the continuous integer-valued functions on a probe form an abelian group. Nöbeling's theorem says that this group is free: there is a collection of basis functions such that every continuous integer-valued function has one unique expression as a finite integer combination of them. Freeness is special because a general abelian group need not have any basis of this kind.

![Paired bars show equal counts for finite-stage boxes and the basis elements constructed from them](guide/03-stacks-of-steps/basis_size.png)

The theorem is due to Nöbeling, extending work of Specker, and the lectures present Bergman's proof ([Theorem 5.4, page 34](https://arxiv.org/pdf/2605.03658v1#page=34)). The implementation in this repository follows the finite stages of that construction. It orders products of indicator functions, retains a function when earlier choices do not already generate it, and checks that the retained functions form a basis. The chart confirms that the basis size matches the number of boxes at each tested stage.

This finite calculation does not prove Nöbeling's theorem. At a fixed finite stage, the group is automatically free, while the theorem's real content is that a compatible basis exists for the full infinite object. The repository therefore labels its calculation as a finite shadow and quotes the infinite theorem from the lectures.

### The mathematics

[Nöbeling's theorem, Theorem 5.4 on page 34 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=34), states

```math
C(S,\mathbb Z)\cong\bigoplus_{e\in E}\mathbb Z e.
```

This freeness gives every $f\in C(S,\mathbb Z)$ one finite expression. Explicitly,

```math
f=\sum_{e\in F}n_e e,
\qquad F\subset E\text{ finite},
\qquad n_e\in\mathbb Z.
```

**Reading the symbols.** The group $C(S,\mathbb Z)$ contains the continuous integer-valued functions on the probe $S$. The set $E$ is a basis of step functions. The direct-sum symbol $\bigoplus$ says that each function uses only finitely many basis elements. The expression $\mathbb Z e$ means all integer multiples of the basis element $e$. The letter $f$ names one continuous function, $F$ is the finite subset of basis elements used for it, and $n_e$ is the integer coefficient attached to $e$. The membership sign $\in$ means “belongs to,” and $\subset$ means “is a subset of.”

**Why it matters.** Freeness for the full infinite probe is the theorem's content. It lets an integer-valued measure be described by choosing its value independently on every basis function, which leads to the product description in the next chapter.

**In the simulation.** The target control chooses $f$ at one finite stage. The switches used control enlarges $F$. Each filled bar is one coefficient $n_e e$, and the reconstruction is complete when their finite sum equals $f$ on every box. This finite activity illustrates the construction but does not prove the infinite theorem.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/03.html)** to choose an integer-valued function and watch the basis functions rebuild it.

## 4 · Products in, sums out

Nöbeling's theorem lets us describe weightings by comparing two ways to store an infinite family of integers. A **product** is an unlimited row of integer dials. Every dial can be set independently, and infinitely many of them may be nonzero. A **direct sum** uses the same row but allows only finitely many nonzero dials in any one element. This finite-support condition creates an important duality between the two constructions.

![A product allows nonzero entries across an unlimited row, while a direct sum has only finitely many nonzero entries](guide/04-products-in-sums-out/product_sum.png)

A homomorphism from a product to the integers cannot depend on infinitely many dials. Although one might try to assign a coefficient to every position, Specker's theorem says that every additive map reads only finitely many coordinates. Therefore, the collection of homomorphisms from a product is a direct sum of copies of the integers.

![A homomorphism reads a finite initial group of coordinates and ignores all later coordinates in the product](guide/04-products-in-sums-out/finite_reach.gif)

The underlying obstruction comes from divisibility. Data placed sufficiently far along the row can be arranged to be divisible by arbitrarily high powers of an integer. Any output that respects all those divisions would have to be divisible by every such power, and the only integer with that property is zero. Specker's proof makes this argument precise; the theorem is quoted here rather than reproduced.

A homomorphism from a direct sum behaves in the opposite way. Because each input has finite support, one may choose an independent integer coefficient for every dial without creating an infinite numerical sum. The collection of homomorphisms from a direct sum is therefore a product.

This applies directly to measures. By Nöbeling's theorem, the continuous integer-valued functions on a probe form a free group, so they are a direct sum of copies of the integers indexed by a basis. A weighting is exactly an integer-valued homomorphism on this function group, obtained by integration. Taking the homomorphisms turns that direct sum into a product:

> Every collection of weightings on a probe is an endless product of copies of the whole numbers.

This is Corollary 5.5 of the lectures ([page 34](https://arxiv.org/pdf/2605.03658v1#page=34)). The branching pattern of the probe determines the indexing set, but once a basis is chosen, every weighting is represented by an unrestricted row of integer coordinates. These products will become the basic projective building blocks of solid groups.

### The mathematics

Products and direct sums exchange roles under integer duality. Specker's theorem and [Corollary 5.5, page 34 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=34) give the two descriptions

```math
\operatorname{Hom}_{\mathrm{Ab}}\!\left(
\prod_{n\in\mathbb N}\mathbb Z,\mathbb Z\right)
\cong\bigoplus_{n\in\mathbb N}\mathbb Z,
\qquad
\operatorname{Hom}_{\mathrm{Ab}}\!\left(
\bigoplus_{i\in I}\mathbb Z,\mathbb Z\right)
\cong\prod_{i\in I}\mathbb Z.
```

The index set depends on the probe $S$. Consequently, for some such set $I$,

```math
\mathbb Z[S]^{\blacksquare}\cong\prod_{i\in I}\mathbb Z.
```

**Reading the symbols.** The notation $\operatorname{Hom}_{\mathrm{Ab}}$ means additive maps of ordinary abelian groups. The first product has one coordinate for each natural number $n\in\mathbb N$. The more general index set in the second formula is $I$. A product $\prod$ allows an integer in every coordinate, including infinitely many nonzero entries. A direct sum $\bigoplus$ allows only finitely many nonzero entries. Specker's theorem is the first isomorphism: an integer-valued homomorphism on a countable product reads only finitely many coordinates. The second isomorphism says that a homomorphism on a direct sum may choose one coefficient for every coordinate. The black square on $\mathbb Z[S]^{\blacksquare}$ marks the free solid group on $S$. The next displayed isomorphism follows by applying the second duality to Nöbeling's basis of $C(S,\mathbb Z)$.

**Why it matters.** Nöbeling makes $C(S,\mathbb Z)$ a direct sum of copies of $\mathbb Z$. Taking its integer dual changes that direct sum into the product displayed above. Products of integer groups are therefore the basic free objects of solid mathematics.

**In the simulation.** The reach control chooses the finite set of coordinates used by one homomorphism in Specker's formula. Moving a coordinate outside that set leaves the output unchanged. The endless row represents the countable product, while the finite reach represents its direct-sum dual.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/04.html)** to compare products with direct sums and test how many coordinates an integer-valued homomorphism can use.

## 5 · The solid rule

We can now define the property that gives this part its name. The definition uses the compatible weightings from section 2 and asks whether point-level data determine how every such weighting should be integrated.

A condensed abelian group is **solid** when any map from the points of a probe into the group extends uniquely to the free solid group of weightings on that probe. Informally, once the values of individual points are known, there must be exactly one compatible way to assign a value to every integer weighting.

![A map from probe points into a group extends to a single map defined on all compatible weightings](guide/05-the-solid-rule/extension.gif)

The two parts of "extends uniquely" serve different purposes. Existence ensures that every weighting described by the probe can be integrated in the group. Uniqueness ensures that the point values do not lead to two conflicting answers. Together, they make the summation rule part of the group's structure rather than an extra choice made for each series.

The lectures give this definition in one line ([Definition 5.1, page 33](https://arxiv.org/pdf/2605.03658v1#page=33)) and then establish the structure of the resulting category. The main conclusions needed here can be summarized as follows:

> Solid groups form an abelian category closed under limits, colimits, and extensions. Products of copies of the integers are compact projective generators, and every condensed group has a universal solidification.

This statement combines Theorem 5.8 ([page 35](https://arxiv.org/pdf/2605.03658v1#page=35)) with Corollary 6.1 ([page 42](https://arxiv.org/pdf/2605.03658v1#page=42)). The word **universal** means that the map to the solidification factors uniquely through every other map from the original group to a solid group. Compact projective generators are equally practical: maps from the products in section 4 detect objects and help build the rest of the solid category.

![Six sample groups are shown with a pass or fail result for the unique-extension condition](guide/05-the-solid-rule/solid_or_not.png)

The figure classifies several recurring examples. The integers are solid, as is every product of copies of the integers. The p-adic integers and formal power-series groups are also solid. The usual real numbers are not solid under this integer-based rule, and understanding that failure will prepare us for the different rule introduced in part three.

### The mathematics

[Definition 5.1, page 33 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=33) says that a condensed abelian group $A$ is solid exactly when every map from a probe extends uniquely:

```math
\forall S,\quad
\operatorname{Hom}(\mathbb Z[S]^{\blacksquare},A)
\xrightarrow{\sim}
\operatorname{Hom}(\mathbb Z[S],A).
```

[Theorem 5.8, page 35](https://arxiv.org/pdf/2605.03658v1#page=35) supplies the universal solidification

```math
(-)^{\blacksquare}:\operatorname{Cond}(\mathrm{Ab})\longrightarrow\operatorname{Solid},
\qquad
\operatorname{Hom}_{\operatorname{Solid}}(M^{\blacksquare},A)
\cong
\operatorname{Hom}_{\operatorname{Cond}(\mathrm{Ab})}(M,A).
```

**Reading the symbols.** The phrase $\forall S$ means “for every profinite probe $S$.” The group $\mathbb Z[S]$ is the free condensed group on its points, and the black square gives its free solid completion. The arrow marked $\sim$ is a bijection: restricting a map from all weightings to the point weights loses no choices and creates none. The functor $(-)^{\blacksquare}$ sends any condensed abelian group $M$ to its solidification $M^{\blacksquare}$. The notation $\operatorname{Solid}$ names the category of solid groups, while $\operatorname{Cond}(\mathrm{Ab})$ names condensed abelian groups. The second line is the universal property: maps from the solidification to a solid group $A$ are the same as maps from $M$ itself.

**Why it matters.** The first bijection combines existence and uniqueness of integration. The theorem says that solid groups form an abelian category closed under limits, colimits, and extensions, with products of copies of $\mathbb Z$ as compact projective generators.

**In the simulation.** Selecting a group chooses $A$. A green result means the point map on the right has one extension on the left. A red result marks a failure of existence or uniqueness. The activity illustrates listed examples; the categorical theorem is quoted from the lectures.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/05.html)** to compare sample groups and see which requirement supports each solidity verdict.

## 6 · Where the real line goes

The solidification of the usual real numbers is zero. This is Corollary 6.1 (iii) of the lectures ([Corollary 6.1 (iii), page 42](https://arxiv.org/pdf/2605.03658v1#page=42)). A simple divisibility argument explains why zero is the expected result, although the full theorem requires more than that argument alone.

![Repeated division remains inside the real numbers but eventually leaves the integers](guide/06-where-the-real-line-goes/divisible.gif)

Every real number can be divided by any positive integer and remain a real number. An abelian group with this property is called **divisible**. The integers do not have it, because an integer such as one cannot be divided by two while staying inside the integers. The animation contrasts these two behaviours.

Now consider a homomorphism from the additive real numbers to one copy of the integers. If a real number is divisible by every positive integer, its image must have the same property because homomorphisms respect addition and division relations. The only integer divisible by every positive integer is zero. Every such homomorphism is therefore zero, and the same coordinate-by-coordinate argument applies to a product of integer groups.

![A map from the divisible real group to each integer coordinate is forced to have value zero](guide/06-where-the-real-line-goes/no_map.png)

This argument shows that the real line maps trivially into the projective building blocks of the solid category. It does not by itself prove that solidification sends the real line to zero. That stronger conclusion also uses the universal-resolution calculation from Lecture IV ([Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25)), after which the stated vanishing follows.

**This does not make the real numbers unimportant.** The solid rule in this part is designed for nonarchimedean notions of size, such as the p-adic size from section 1, where high divisibility means smallness. The ordinary real absolute value behaves differently and requires a different theory of measures. The lectures note this when solidity is introduced ([page 33](https://arxiv.org/pdf/2605.03658v1#page=33)), and part three explains the real-valued replacement.

**The vanishing also has a mathematical use.** Real-valued correction terms disappear from certain condensed calculations instead of creating obstructions. Part one encountered a related result when higher cohomology with real coefficients vanished. The computation in Lecture IV uses this behaviour ([Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25)), and that computation supports the structure theorem for solid groups.

### The mathematics

Divisibility is the property used in this chapter. An abelian group $D$ is divisible when

```math
\forall x\in D,\ \forall n\ge1,\ \exists y\in D\text{ such that }ny=x.
```

Every homomorphism from a divisible group to an integer product is zero:

```math
\operatorname{Hom}\!\left(D,\prod_{i\in I}\mathbb Z\right)=0.
```

The usual additive real line is divisible. For this group, [Corollary 6.1 (iii), page 42 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=42) gives the stronger derived statement

```math
\mathbb R^{L\blacksquare}=0.
```

**Reading the symbols.** The letter $D$ names an abelian group. The symbols $\forall$ and $\exists$ mean “for every” and “there exists.” The relation $x\in D$ says that $x$ belongs to $D$, and $n\ge1$ chooses any positive integer. The equation $ny=x$ means that adding $y$ to itself $n$ times gives $x$. The product sign denotes an arbitrary row of integer groups indexed by $I$. The equation $\operatorname{Hom}=0$ says that every additive map to that product is the zero map. The superscript $L\blacksquare$ means derived solidification, and its value $0$ is the zero object.

**Why it matters.** The divisibility argument proves that the reals map trivially to every compact projective building block of the solid category. The full vanishing $\mathbb R^{L\blacksquare}=0$ also uses [Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25), so the simulation is an explanation of the obstruction rather than a proof of the corollary.

**In the simulation.** The group selector chooses $D$, and the divisions control chooses values of $n$. The real line always supplies a $y=x/n$, while the integers eventually cannot. The final readout shows the consequence for maps into one product coordinate.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/06.html)** to divide elements repeatedly and compare divisible groups with the integers.

## 7 · The multiplication table

The category of solid groups has a product operation called the **completed tensor product**. It combines two solid groups into a third group that represents additive operations depending on one input from each side. The examples below show that this product remembers which completion, or adic topology, each group carries.

![A table lists completed tensor products for p-adic groups, power-series groups, integers, and reals](guide/07-the-multiplication-table/tensor_table.png)

Read the grid by choosing one label from its row and one from its column. The 2-adic integers tensored with the 3-adic integers give zero, while the 2-adic integers tensored with themselves return the 2-adic integers. Combining the 2-adic integers with the real numbers also gives zero, consistent with section 6. Combining power series in one variable with power series in another produces power series in both variables.

![Nested scales based on powers of two and powers of three are compared without a common completion direction](guide/07-the-multiplication-table/rulers.gif)

The animation gives an intuition for the mixed 2-adic and 3-adic entry. The 2-adic completion is organized by divisibility by powers of two, while the 3-adic completion is organized by powers of three. In the 2-adic setting, three is invertible and does not produce a finer scale; in the 3-adic setting, the same is true of two. The two scales are therefore incompatible. The picture illustrates the exact vanishing stated in the table, but does not prove it.

The lectures describe the general pattern by saying that the completed tensor product asks which adic topologies the two factors carry and retains the compatible ones ([Example 6.4, page 44](https://arxiv.org/pdf/2605.03658v1#page=44)). Matching completions reinforce one another, while incompatible completions can give zero. The table is a set of precise instances of that rule.

The power-series entry can also be understood through the coordinates from section 4. A one-variable power series has one coefficient for each nonnegative power of its variable. Combining two such products gives coordinates indexed by pairs of powers ([Proposition 6.3, page 43](https://arxiv.org/pdf/2605.03658v1#page=43)). A pair of powers is exactly a monomial in two variables, so the resulting coordinate system is the group of two-variable power series. The repository tests this indexing argument; the remaining table entries are quoted from the lectures.

### The mathematics

[Proposition 6.3, page 43 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=43) states that completed tensor product multiplies the coordinate sets of integer products:

```math
\left(\prod_{i\in I}\mathbb Z\right)\otimes^{L}_{\blacksquare}
\left(\prod_{j\in J}\mathbb Z\right)
\cong
\prod_{(i,j)\in I\times J}\mathbb Z.
```

[Example 6.4, page 44](https://arxiv.org/pdf/2605.03658v1#page=44) lists the concrete identities for distinct primes $p\neq\ell$:

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

**Reading the symbols.** The sets $I$ and $J$ index the two rows of integer coordinates, and $I\times J$ is the set of ordered pairs of indices. The product signs allow unrestricted coordinates. The symbol $\otimes^{L}_{\blacksquare}$ is the derived solid tensor product from [Theorem 6.2, page 43](https://arxiv.org/pdf/2605.03658v1#page=43). The groups $\mathbb Z_p$ and $\mathbb Z_\ell$ are the $p$-adic and $\ell$-adic integers for distinct primes. The notation $\mathbb Z[[T]]$ means formal power series in $T$, and $\mathbb Z[[U,T]]$ means formal power series in both variables. The symbol $0$ is the zero object, and $\cong$ means isomorphic.

**Why it matters.** Compatible completion directions survive together, while incompatible prime directions produce zero. Pairing the coefficient indices of a series in $U$ with those of a series in $T$ gives exactly the monomials of a two-variable series.

**In the simulation.** The row and column selectors choose the two tensor factors. The highlighted cell reports the corresponding identity. The nested rulers visualize the completion directions, while the readout marks whether an entry is stated directly in Example 6.4 or obtained by the same coordinate rule.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/07.html)** to select two solid groups and inspect the completion rule behind their tensor product.

## 8 · Solidify a shape, get its holes

We can now connect the summation rule back to topology. Begin with an ordinary space, such as a circle, sphere, or torus. Form the free condensed abelian group on its points, which allows finite formal integer combinations of those points, and then apply derived solidification.

![A torus rotates in three dimensions beside bars for its homology in degrees zero, one, and two](guide/08-solidify-a-shape/solidify.gif)

The homology groups of the resulting object are the classical integral homology groups of the original space ([Example 6.5, page 44](https://arxiv.org/pdf/2605.03658v1#page=44)). Thus, the degrees record connected pieces, loops, enclosed surfaces, and higher-dimensional analogues. Torsion information is retained as well, so the result contains more than numerical hole counts.

![Free and torsion homology groups are compared for a circle, figure eight, sphere, torus, and Klein bottle](guide/08-solidify-a-shape/homology_bars.png)

The chart is computed from cellular boundary maps using Smith normal form over the integers. A circle has one free class in degree one, and a figure eight has two. A sphere has one class in degree two and none in degree one. A torus has two degree-one classes and one degree-two class. The Klein bottle has one free degree-one class together with a torsion class of order two, which disappears when doubled.

The connection follows the ideas already developed. Part one showed that integral cohomology agrees before and after translating a compact space into condensed mathematics. In this part, solidification is characterized through maps from products of integer groups, while maps out of the free group on a space correspond to integer-valued data on that space. The lectures turn this correspondence into the precise identification with singular homology.

This result explains why solidity matters beyond the original convergence problem. The definition mentions compatible infinite sums, not loops or surfaces. Nevertheless, applying its universal completion to the free group of a space recovers established topological invariants. The same framework can therefore handle completion and topology without treating them as unrelated constructions.

### The mathematics

For a CW complex $X$, [Example 6.5, page 44 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=44) identifies derived solidification with singular homology:

```math
\mathbb Z[X]^{L\blacksquare}\cong H_\bullet(X;\mathbb Z).
```

The figure uses three familiar spaces. For these examples, the theorem gives

```math
H_\bullet(S^1;\mathbb Z)=(\mathbb Z,\mathbb Z),
\quad
H_\bullet(S^2;\mathbb Z)=(\mathbb Z,0,\mathbb Z),
\quad
H_\bullet(T^2;\mathbb Z)=(\mathbb Z,\mathbb Z^2,\mathbb Z).
```

**Reading the symbols.** The space $X$ is built from cells. The object $\mathbb Z[X]$ is the free condensed abelian group on its points. The superscript $L\blacksquare$ means derived solidification. The notation $H_\bullet(X;\mathbb Z)$ means all singular homology groups of $X$ with integer coefficients, arranged by degree. The circle and sphere are $S^1$ and $S^2$, and $T^2$ is the two-dimensional torus. Each parenthesized list gives degree zero first, then degree one, then degree two when present. The expression $\mathbb Z^2$ means two independent copies of the integers.

**Why it matters.** A completion defined through compatible infinite sums recovers a classical topological invariant. Because the statement is derived, nonzero homology may appear in several degrees, and integer torsion such as the Klein bottle's order-two class is retained.

**In the simulation.** The shape selector chooses $X$. The bars display the groups on the right side degree by degree, and the camera control rotates the three-dimensional models. A brown bar labelled by two represents a $\mathbb Z/2\mathbb Z$ torsion class rather than a free copy of $\mathbb Z$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/08.html)** to select a space, rotate the three-dimensional examples, and compare their free and torsion homology classes.

## Where part two leaves you

A weighting is a compatible family of finite integer assignments on a probe. A solid group is one in which point-level data extend uniquely to all such weightings, giving a consistent form of infinite summation. Nöbeling's theorem identifies the weightings as products of copies of the integers, and solidification provides a universal way to enter the solid category. Applied to a space, its derived form recovers integral homology.

This rule is deliberately nonarchimedean, so it sends the usual real line to zero rather than modelling real analysis. Part three replaces the fixed integer-valued theory with the more general idea of a ring together with its own theory of measures. That extension brings back the real numbers and adds multiplication, which is the step needed to move from groups into geometry.

**[Part three: Rings That Know How To Integrate](../condensed-math03/ARTICLE.md)**

## How this part lines up with the lectures

| this guide | in the lectures |
|---|---|
| section 1, sums with nowhere to land | the motivation opening Lecture V, page 33 |
| section 2, weights that agree | Definition 5.1, page 33, the free solid group |
| section 3, every function is a stack of steps | Theorem 5.4, page 34, Nöbeling's theorem with Bergman's proof |
| section 4, products in, sums out | Corollary 5.5, page 34, and the biduality inside Proposition 5.7, page 35 |
| section 5, the solid rule | Definition 5.1, page 33; Theorem 5.8, page 35; Corollary 6.1, page 42 |
| section 6, where the real line goes | Corollary 6.1 (iii), page 42; Theorem 4.3, page 25; the footnote on page 33 |
| section 7, the multiplication table | Theorem 6.2 and Proposition 6.3, page 43; Example 6.4, page 44 |
| section 8, solidify a shape | Example 6.5, page 44 |

## Checking it yourself

The following commands rebuild the figures used in this part. They also rerun the finite examples that support the visual explanations.

```
cd condensed-math
make venv
make test
make figures
```

For this part, the tests:

- recompute the running totals of the doubling sum in exact arithmetic and confirm the ordinary distance doubles while the base-two distance halves, converging to minus one
- build weightings on the halving probe and the base-p probe and confirm the agreement rule at every level
- confirm that integrating a measurement read at a coarse level and at a refined one gives the same total
- run Bergman's basis construction and confirm the basis size equals the box count at each level
- check the pairing behind the power series row of the multiplication table: the dials of a two-variable series correspond exactly to pairs of dials of one-variable series
- confirm the transcribed multiplication table is symmetric and consistent with the nesting rule the lectures describe
- compute the holes of five shapes from boundary data by Smith normal form over the whole numbers, torsion included, and confirm the Klein bottle's piece of order two

The infinite and categorical results are quoted rather than established by these tests. They include Nöbeling's theorem, the structural theorem for solid groups, the vanishing of the solidified real line, and the identification of derived solidification with homology. The file `notes/research-content.md` marks each claim as computed, a finite shadow, derived, or quoted.

## Glossary

| this guide's plain phrase | the standard mathematical term |
|---|---|
| a weighting | a measure on a profinite set, an element of the free solid abelian group |
| the agreement rule | compatibility in the inverse limit |
| small when divisible by a high power | the p-adic absolute value |
| the base-p numbers | the p-adic integers |
| a row of dials, a product | a product of copies of the integers |
| a sum | a direct sum of copies of the integers |
| a question | a group homomorphism to the integers |
| solid | solid, in the lectures' sense |
| solidification | the left adjoint to the inclusion of solid groups |
| the completed tensor product | the solid tensor product |
| a nesting | an adic topology |
| divisible | divisible |
| the holes of a shape | the singular homology groups |
| a hole you go round twice | a torsion class of order two |
| the building blocks | the compact projective generators |

## Further reading

- The lectures: Peter Scholze, "Lectures on Condensed Mathematics", [arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026, joint work with Dustin Clausen. Lectures IV to VI are this part.
- For section 4: E. Specker, "Additive Gruppen von Folgen ganzer Zahlen" (1950), and G. Nöbeling, "Verallgemeinerung eines Satzes von Herrn E. Specker" (1968), both cited in the lectures for Theorem 5.4.
- `notes/research-content.md` marks every claim above as computed here or quoted.

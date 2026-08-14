# Rings That Know How To Integrate

*Part three of three on condensed mathematics. Part two gave abelian groups a rule for integrating integer-valued measures. This final part lets each ring carry an appropriate theory of measures, including one suited to the real numbers. With multiplication and integration available together, the same framework builds functions near a boundary, compactly supported cohomology, the six operations, and coherent duality. Parts one and two are assumed.*

![The unit region changes from a rounded convex shape to a diamond and then to a nonconvex inward-curving shape as the exponent falls](guide/00-start-here/hero.gif)

The animation previews the central example. Each shape contains the pairs of weights whose size is at most one, and the exponent determines how that size is measured. For exponents above one, the region is convex and rounded. At one it becomes a diamond, while below one it bends inward and is no longer convex. At the same time, merging several boxes preserves the size bound only when the exponent is at most one. The real theory must therefore work in the nonconvex range, which explains why ordinary functional analysis is not sufficient.

This is part three of three, covering Lectures VII to XI of Peter Scholze's *Lectures on Condensed Mathematics* ([arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026), joint work with Dustin Clausen. [Part one](../condensed-math01/ARTICLE.md) introduced probes and condensed sets, while [part two](../condensed-math02/ARTICLE.md) developed integer-valued measures and solid groups. Both parts are used here, but no other background is assumed. Most sections include a [page you can play with](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/index.html) that turns the main abstract choice into a finite activity.

```
    the general notion          1  a ring with a rule for sums
                                2  two rules that work
                                3  the real line's own rule
    geometry appears            4  functions near the edge
                                5  cohomology with compact support
                                6  gluing the local pictures
    what it was all for         7  the six operations
                                8  duality, watched
```

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/00.html)** to vary the exponent and compare convexity with the effect of merging boxes.

## 1 · A ring with a rule for sums

Part two attached one particular theory of infinite summation to the integers. Other rings need different theories, so we begin by separating the underlying ring from the measures it permits. This allows p-adic numbers, ordinary discrete rings, and the real numbers to use the same framework without pretending that they share one notion of convergence.

A ring supports addition, subtraction, and multiplication. A module is an additive group whose elements can also be multiplied by elements of the ring. For every probe and every placement of its points in a module, we want a rule that says which weighted combinations are legal and how those combinations act on the module.

The general definition contains two pieces of data ([Definition 7.1, page 45](https://arxiv.org/pdf/2605.03658v1#page=45)):

**The ring** is treated as a condensed ring, meaning an answer sheet of the kind introduced in part one, with compatible addition and multiplication. This description allows topological information to live inside the algebra rather than beside it.

**The theory of measures** assigns an A-module of legal measures to every unfoldable probe. It respects finite disjoint unions, and it includes every Dirac measure, the unit weight concentrated at one point. Thus, ordinary points remain available inside the larger space of measures.

![A diagram sends a probe to its module of allowed measures and includes each probe point as a Dirac measure](guide/01-a-ring-with-a-rule/measures.png)

A ring and a proposed theory of measures must also pass a compatibility test. The test ensures that modules built from the proposed free complete modules form a stable algebraic world, with the expected maps from point data agreeing with maps from measures. A pair that passes is called an **analytic ring** ([Definition 7.4, page 46](https://arxiv.org/pdf/2605.03658v1#page=46)). This guide uses the plainer phrase *a ring with a rule*.

The distinction between proposing a rule and proving it analytic is important. Many assignments look reasonable on each individual probe but fail when modules are combined into exact sequences or complexes. Section 3 examines this problem for real-valued measures and shows why the first natural choices do not pass.

### The mathematics

[Definition 7.1, page 45 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=45) defines a theory of measures on a condensed ring $A$ as a functor

```math
\mathcal M:\{\text{extremally disconnected }S\}
\longrightarrow A\text{-}\operatorname{Mod},
\qquad
S\longmapsto\mathcal M[S],
```

The definition also includes natural Dirac maps $S\to\mathcal M[S]$. Its disjoint-union rule is

```math
\mathcal M[S_1\sqcup S_2]\cong\mathcal M[S_1]\times\mathcal M[S_2].
```

[Definition 7.4, page 46](https://arxiv.org/pdf/2605.03658v1#page=46) calls the pair analytic when, for the complexes $C$ specified there,

```math
R\!\operatorname{Hom}_A(\mathcal M[S],C)
\xrightarrow{\sim}
R\!\operatorname{Hom}_A(A[S],C).
```

**Reading the symbols.** The ring is $A$, and $A$-$\operatorname{Mod}$ is the category of condensed $A$-modules. The functor $\mathcal M$ assigns the module of legal measures $\mathcal M[S]$ to each unfoldable probe $S$. The arrow $S\to\mathcal M[S]$ sends a point to its Dirac measure. The symbol $\sqcup$ means disjoint union, $\times$ means product, and $\cong$ means isomorphic. The notation $A[S]$ is the free $A$-module on the points of $S$. The letter $C$ names a chain complex assembled from free measure modules. The expression $R\!\operatorname{Hom}_A$ is the derived object of $A$-linear maps, and an arrow marked $\sim$ is an isomorphism.

**Why it matters.** The first two lines propose a summation rule. The final isomorphism is the test that makes the proposal stable under the homological operations used later. A pair may satisfy the visible finite rules and still fail this analytic test.

**In the simulation.** The controls first select the ring $A$, then a candidate module $\mathcal M[S]$, and finally check that points enter as Dirac measures and disjoint pieces produce a product. The final verdict represents the extra analytic condition rather than pretending that the finite checks prove it.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/01.html)** to assemble the two pieces of a proposed rule and check its basic requirements in order.

## 2 · Two rules that work

The first examples require no new construction because they come from the solid measures of part two. They show how the general definition packages familiar completion rules.

**The base-p rule.** Use the p-adic integers as the ring and compatible p-adic-valued measures on each probe as its free complete modules. This pair passes the analytic-ring test ([Proposition 7.8, page 48](https://arxiv.org/pdf/2605.03658v1#page=48)), so p-adic summation fits the new framework.

**The solid rule over a plain ring.** Let A be any discrete ring and extend the integer-valued solid measures by coefficients in A. This pair also passes. It supplies a theory of complete A-modules even though the underlying ring itself has no nontrivial topology.

![The p-adic measure rule and the solid rule over a discrete ring are compared with one infinite sum handled by each](guide/02-two-that-work/two_rules.png)

The second example may initially seem empty because a discrete ring has no limits to complete inside the ring itself. However, the rule governs condensed modules over that ring, not merely its individual elements. Those modules can carry rich topological information through their probe values. The theory selects the modules in which solid measures can be integrated consistently, while keeping the coefficient ring algebraically simple.

This separation is useful in geometry. The ring describes multiplication of functions, while the theory of measures controls infinite additive behaviour in its modules. Since these roles are independent, one can alter the completion rule without changing the underlying algebraic formulas.

A broader construction begins with a ring A and a chosen subring of elements regarded as having size at most one ([Remark 7.9, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)). Such a pair is called a Huber pair. For the field of p-adic numbers, it produces the bounded p-adic-valued measures. Section 6 will use Huber pairs to turn local rings into geometric patches.

### The mathematics

[Proposition 7.8, page 48 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=48) states that the following two theories are analytic:

```math
\mathbb Z_{p,\blacksquare}[S]
:=\varprojlim_i\mathbb Z_p[S_i]
=M(S,\mathbb Z_p),
```

```math
(A,\mathbb Z)^{\blacksquare}[S]
:=\mathbb Z[S]^{\blacksquare}\otimes_{\mathbb Z}A
\qquad\text{for a discrete ring }A.
```

[Remark 7.9, page 49](https://arxiv.org/pdf/2605.03658v1#page=49) extends this pattern to a Huber pair $(A,A^+)$ and, in particular, identifies

```math
(\mathbb Q_p,\mathbb Z_p)^{\blacksquare}[S]
=M_b(S,\mathbb Q_p)
=M(S,\mathbb Z_p)[1/p].
```

**Reading the symbols.** The probe $S$ has finite stages $S_i$. The inverse-limit symbol $\varprojlim$ keeps compatible $p$-adic weights on all stages. The group $\mathbb Z_p$ is the $p$-adic integers, and $M(S,\mathbb Z_p)$ is the module of $\mathbb Z_p$-valued measures. In the second line, $A$ is any discrete ring, $\otimes_{\mathbb Z}$ extends integer coefficients to $A$, and the black square marks the solid measure rule. A Huber pair consists of a ring $A$ and a subring $A^+$ of elements regarded as bounded. The field $\mathbb Q_p$ is the $p$-adic numbers. The subscript $b$ means bounded, and $[1/p]$ allows division by powers of $p$.

**Why it matters.** These examples separate multiplication, supplied by the ring, from summation, supplied by its measure modules. The same framework handles a topological $p$-adic ring and an algebraically discrete ring without assigning them the same completion.

**In the simulation.** The rule selector switches between the two displayed constructions. The nested boxes represent the inverse limit for $\mathbb Z_p$, while the row of coefficients represents extension from $\mathbb Z[S]^{\blacksquare}$ to a discrete ring $A$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/02.html)** to compare the p-adic and discrete-ring rules and see which measures each one permits.

## 3 · The real line's own rule

Part two's integer-based solidification sends the usual real line to zero, so real analysis needs its own theory of measures. The natural candidates are signed real-valued measures with a bound on their size. We will see that the way a probe refines places a strict limit on how that size may be defined.

For a finite list of weights, choose a positive exponent. At exponent one, size is the sum of the absolute values. At exponent two, square the absolute values, add them, and take a square root. Other exponents follow the same pattern. These are the familiar ell-p sizes, applied here to the weights on each finite stage of a probe.

A measure must be compatible between stages. Moving from a fine stage to a coarse stage merges boxes and adds their weights. If a fine-stage list has size at most a fixed bound, its merged list must satisfy the same bound. Otherwise, the bounded regions at different stages do not form an inverse system, and there is no well-defined space of measures on the full probe.

![Curves for merging two, four, and nine equal boxes cross the no-growth threshold when the exponent is one](guide/03-the-real-lines-own-rule/merge.png)

The chart computes the worst effect of merging equal weights. The size after merging is no greater than the size before merging exactly when the exponent is at most one. Above one, the ratio grows with the number of merged boxes. For example, merging four equal weights at exponent two doubles the size. This forces the real theory into exponents no larger than one ([Example 7.10, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)).

![Five unit regions show convex boundaries for exponents at least one and nonconvex boundaries below one](guide/03-the-real-lines-own-rule/lp_balls.png)

The same boundary creates a second problem. At exponent one and above, the unit ball is convex, so the straight segment between any two allowed points remains allowed. Below one, the unit ball caves inward and loses convexity. Classical functional analysis is largely organized around locally convex spaces, while compatibility under merging requires us to work at or below the edge of that setting.

Choosing exponent one gives the standard bounded signed measures, but the resulting pair is not an analytic ring ([Example 7.10, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)). Ribe constructed an extension of complete locally convex spaces whose middle space is not locally convex, showing that this class is not stable under the extensions required by the analytic-ring test. Fixing any one exponent below one does not solve the problem because a related obstruction persists there as well.

The successful construction avoids fixing a single lower exponent. For a target exponent p no greater than one, it collects the measures bounded for some exponent q strictly below p and identifies them compatibly as q varies. The standard name for this directed construction is a colimit.

> With the exponents swept rather than fixed, the real numbers do get a rule that works, for every target exponent up to one.

This is Theorem 7.11 ([page 50](https://arxiv.org/pdf/2605.03658v1#page=50)), whose proof belongs to the companion work cited by the lectures. Modules built from this varying-exponent real theory are called **liquid** modules. The name distinguishes this construction from the fixed integer-based solid theory of part two.

The restriction on the exponent came directly from finite refinement maps: merging boxes adds their weights. This is an important pattern in condensed mathematics. A concrete compatibility condition on finite stages determines which infinite analytic structures can exist.

### The mathematics

Choose an exponent with $0<p\le1$. [Example 7.10, page 49 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=49) defines the finite-stage size and its measure module by

```math
\|(x_i)\|_{\ell^p}=\left(\sum_i|x_i|^p\right)^{1/p},
\qquad
\mathcal M_p[S]=\bigcup_{r>0}\varprojlim_i
\{x\in\mathbb R[S_i]\mid\|x\|_{\ell^p}\le r\}.
```

The effect of merging can be calculated exactly for equal weights. Merging $n$ equal positive weights changes the size by

```math
\frac{\|\text{after}\|_{\ell^p}}{\|\text{before}\|_{\ell^p}}
=n^{1-1/p}\le1\quad\Longleftrightarrow\quad p\le1.
```

No fixed $p$ gives an analytic ring. [Theorem 7.11, page 50](https://arxiv.org/pdf/2605.03658v1#page=50) uses all smaller exponents:

```math
\mathcal M_{<p}[S]:=\varinjlim_{q<p}\mathcal M_q[S],
\qquad
(\mathbb R,\mathcal M_{<p})\text{ is an analytic ring.}
```

**Reading the symbols.** The exponent $p$ is positive and at most one. The list $(x_i)$ contains the weights on one finite stage. Absolute-value bars measure each real weight, $\sum$ adds their $p$th powers, and the outer exponent $1/p$ defines the $\ell^p$ size. The union over $r>0$ allows any finite bound, while $\varprojlim$ imposes compatibility between the stages $S_i$. The ratio compares the size after and before merging $n$ equal boxes. The double arrow $\Longleftrightarrow$ means “if and only if.” The direct-limit symbol $\varinjlim_{q<p}$ combines the theories for all positive $q$ smaller than $p$. The pair $(\mathbb R,\mathcal M_{<p})$ is the real ring with this combined rule.

**Why it matters.** Refinement forces $p\le1$, exactly the range where ordinary local convexity stops being available. Sweeping through all smaller exponents produces the liquid theory that passes the analytic-ring test.

**In the simulation.** The exponent control changes $p$, and the box control changes $n$. The chart computes $n^{1-1/p}$ live. The unit-ball picture shows convexity, while the verdict checks the separate requirement that merging must not increase size.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/03.html)** to change the exponent, merge equal weights, and locate the boundary where the size begins to increase.

## 4 · Functions near the edge

We now turn from analysis to geometry. Begin with the affine line, whose global functions are polynomials in one coordinate. To study what happens far from its finite part, introduce the reciprocal coordinate. When the original coordinate is large, its reciprocal is small, so series in the reciprocal describe functions in a formal neighbourhood of infinity.

![A point moves toward infinity while bars compare positive coordinate powers with powers of the inverse coordinate](guide/04-functions-near-the-edge/tail.gif)

Such a series may contain finitely many positive powers of the original coordinate and infinitely many negative powers. The lectures call the resulting ring of formal Laurent series the functions near the boundary. This guide calls it the **edge ring**. The animation moves toward the boundary while assembling the terms that remain meaningful there.

Every polynomial has an expansion near infinity, so the polynomial ring maps into the edge ring. The edge ring also contains infinite negative-power tails that no polynomial can have. Comparing the two rings separates information defined everywhere from information that exists only near the boundary.

The quotient of the edge ring by the polynomial ring discards every global polynomial contribution. What remains consists of the boundary tails. This quotient is the concrete object used in the next section to build compactly supported cohomology.

![The two axes form a coordinate cross with one shared central point and four directions toward the boundary](guide/04-functions-near-the-edge/cross.png)

The lectures work out the coordinate cross, defined by two coordinate axes meeting at one point ([Remark 8.5, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)). Each branch contributes its own Laurent tails, while the shared value at the crossing imposes one relation between the global functions. The finite truncation in this repository counts the quotient as the tails from both branches plus one additional piece associated with that shared point. The count stabilizes as the truncation is extended.

### The mathematics

Begin with the affine line and its coordinate $T$. Lecture VIII uses the boundary ring

```math
A=\mathbb Z[T],
\qquad
A_\infty=\mathbb Z((T^{-1})),
\qquad
A_\infty/A=\mathbb Z((T^{-1}))/\mathbb Z[T].
```

The coordinate cross has two branches and one shared origin. [Remark 8.5, page 54 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=54) writes

```math
A=\mathbb Z[X,Y]/(XY),
\qquad
A_\infty=\mathbb Z((X^{-1}))\times\mathbb Z((Y^{-1})),
```

```math
A_\infty/A=
\frac{\mathbb Z((X^{-1}))\times\mathbb Z((Y^{-1}))}
{\mathbb Z[X,Y]/(XY)}.
```

**Reading the symbols.** The ring $A=\mathbb Z[T]$ contains polynomials in the coordinate $T$. The double parentheses in $\mathbb Z((T^{-1}))$ mean formal Laurent series in the inverse coordinate: infinitely many negative powers of $T$ are allowed, but only finitely many positive powers. The subscript $\infty$ marks functions near the boundary. The quotient $A_\infty/A$ identifies two boundary series when they differ by a global polynomial. For the cross, $X$ and $Y$ are its two coordinates, and the relation $XY=0$ forces points to lie on one axis or the other. The product sign $\times$ keeps one Laurent tail for each branch.

**Why it matters.** The quotient removes every function already defined globally and retains only boundary information. On the cross, the relation at the shared point couples the two branches and accounts for the extra piece in the finite truncation.

**In the simulation.** Moving toward the edge increases $T$ and decreases the inverse coordinate $T^{-1}$. The term controls separate polynomial powers, which lie in $A$ and vanish in the quotient, from inverse-power tails, which remain in $A_\infty/A$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/04.html)** to move toward the boundary and see which polynomial and tail terms survive in the quotient.

## 5 · Cohomology with compact support

A map from a space to a point gives two natural ways to collect information. Ordinary pushforward records all global sections. Pushforward with compact support records the part that does not persist out toward the boundary. The second operation is harder because it must distinguish global behaviour from the infinite tails introduced in section 4.

**Everything.** Ordinary cohomology collects functions or sheaf data across the entire space. Algebraic geometry already has this pushforward, and it behaves well for the usual derived categories.

**Only what vanishes near the edge.** Compactly supported cohomology keeps data whose support stays away from the boundary. In the present construction, it is obtained by comparing global modules with the modules of functions near that boundary.

![Blocks for global functions are removed from the larger set of boundary functions, leaving the negative-power tails](guide/05-compact-support/compact_support.gif)

For a finitely generated algebra over the integers, the two relevant module theories are connected by a sequence of adjoints. The edge quotient provides the additional left adjoint needed to define compactly supported pushforward. This construction works because the theories are analytic rings, so products, limits, and derived operations retain the required completeness ([Theorem 8.1, page 53](https://arxiv.org/pdf/2605.03658v1#page=53)).

The resulting operation has a right adjoint, which means that maps out of a compactly supported pushforward correspond naturally and uniquely to maps into a partner object:

> Compactly supported pushforward has a right adjoint. Applying this right adjoint to the unit object produces the classical dualizing complex.

This is Theorem 8.2 ([page 53](https://arxiv.org/pdf/2605.03658v1#page=53)). In standard notation the operations are called lower shriek and upper shriek. Applying upper shriek to the unit object gives the dualizing complex. The adjunction characterizes this object canonically, replacing a separate case-by-case choice of a candidate.

![A chart compares the truncated boundary quotient for the affine line and the coordinate cross](guide/05-compact-support/dualizing.png)

For the coordinate cross, the lectures express the dualizing complex as the integer dual of the quotient of boundary functions by global functions ([Remark 8.5, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)). The truncation calculation in this repository reproduces the finite-dimensional counting pattern behind that quotient, not the categorical theorem itself.

Two consequences clarify why condensed modules are needed. First, compactly supported pushforward generally takes a discrete module to a genuinely nondiscrete object because boundary tails involve infinite products. The operation therefore has no naive construction within ordinary discrete modules. Its right adjoint does preserve discrete objects, so the final dualizing complex can be classical even though the route used to define it passes through condensed mathematics ([the discussion under Theorem 8.2, page 53](https://arxiv.org/pdf/2605.03658v1#page=53)).

Second, compactly supported pushforward preserves compact objects. This formal compactness condition becomes the local form of the familiar finiteness theorem for coherent cohomology ([Remark 8.3, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)). Once the construction is globalized and proper pushforward agrees with compactly supported pushforward, it recovers the usual finiteness statement.

### The mathematics

Let $A$ be a finitely generated integer algebra. [Theorem 8.1, page 53 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=53) constructs a chain of adjoints

```math
j_!\dashv j^*\dashv j_*:
D(A^{\blacksquare})\longleftrightarrow D((A,\mathbb Z)^{\blacksquare}).
```

Now let $f:\operatorname{Spec}A\to\operatorname{Spec}\mathbb Z$ be the projection. [Theorem 8.2, page 53](https://arxiv.org/pdf/2605.03658v1#page=53) defines compactly supported pushforward and its right adjoint

```math
f_!:D(A^{\blacksquare})\longrightarrow D(\mathbb Z^{\blacksquare}),
\qquad
f_!\dashv f^!,
```

The same theorem identifies the dualizing complex. Its formula is

```math
\omega_A:=f^!\mathbb Z
\cong R\!\operatorname{Hom}_{\mathbb Z}(f_!A,\mathbb Z).
```

**Reading the symbols.** The ring $A$ is finitely generated over the integers. The notation $D$ means the derived category of modules for the rule shown in parentheses. The symbols $j_!$, $j^*$, and $j_*$ are three functors, and $\dashv$ means “is left adjoint to.” The map $f$ sends the affine space $\operatorname{Spec}A$ to the integer base $\operatorname{Spec}\mathbb Z$. The functor $f_!$ is pushforward with compact support, and $f^!$ is its right adjoint. The object $\omega_A$ names the dualizing complex. The expression $R\!\operatorname{Hom}_{\mathbb Z}$ is the derived integer dual, and $\cong$ means a canonical isomorphism.

**Why it matters.** The left adjoint $j_!$ is the new operation supplied by the boundary quotient. Composing it with the ordinary map to the base produces $f_!$. Its right adjoint then defines the dualizing complex without choosing one separately. The theorem also states that $f_!$ preserves compact objects but generally not discrete ones.

**In the simulation.** The shape selector chooses the line or cross. The upper row represents boundary functions, the middle row represents global functions, and the lower row is the quotient used by $j_!$. The readout counts the finite truncation of $f_!A$; it illustrates the construction and does not prove the adjunction.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/05.html)** to form the boundary quotient for a line and a coordinate cross and compare the surviving tails.

## 6 · Gluing the local pictures

The preceding construction used one ring, so geometrically it described one affine patch. A general space requires many such patches joined along overlaps. To glue them, each patch must remember both its ring of functions and the local rule that decides which functions are bounded.

The local data form a Huber pair: a ring A together with an integrally closed subring A-plus whose elements are declared to have size at most one. From this pair one forms a valuation space. A point of that space is a consistent multiplicative way to assign sizes to all elements of A, subject to the requirement that every element of A-plus has size at most one ([Proposition 9.2, page 63](https://arxiv.org/pdf/2605.03658v1#page=63)).

![Three schematic valuation regions shrink as additional ring elements are required to have size at most one](guide/06-gluing-the-pictures/spa.png)

Choosing A-plus cuts out the region of valuations that treat its elements as small. Conversely, the allowed region recovers A-plus as exactly the functions whose size is at most one at every point in that region. Within the class stated in the proposition, the algebraic choice and geometric region therefore determine one another.

![Compatible module data on two overlapping patches combine into one object on their union](guide/06-gluing-the-pictures/gluing.gif)

The gluing theorem says that the derived category of complete modules varies as a sheaf over these patches ([Theorem 9.8, page 65](https://arxiv.org/pdf/2605.03658v1#page=65)). If local module objects and all their comparison data agree on overlaps, they determine one global object, uniquely up to the appropriate equivalence. This result allows the affine construction of compactly supported cohomology to be used on spaces assembled from many affines.

The theorem requires a higher-categorical version of the derived category. Ordinary derived categories record maps only up to homotopy, but gluing also needs coherent homotopies between those homotopies and further levels of compatibility. An infinity-category retains that information. The need for this language appears at the gluing step rather than in the earlier finite pictures.

Despite that technical language, the proof follows the familiar pattern of Zariski descent. Cover a space by patches where chosen functions become invertible, check the statement after localizing to each patch, and use the fact that the localized cover splits. Lecture X establishes the two required facts in this setting: localizations commute with one another, and a module that vanishes on every patch is globally zero.

### The mathematics

For a ring $A$, [Proposition 9.2, page 63 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=63) gives the correspondence between an integrally closed subring $A^+$ and its valuation region:

```math
\operatorname{Spa}(A,A^+)
=\{x\in\operatorname{Spv}(A)\mid |f(x)|\le1\text{ for every }f\in A^+\},
```

```math
A^+=\{f\in A\mid |f(x)|\le1\text{ for every }x\in\operatorname{Spa}(A,A^+)\}.
```

[Theorem 9.8, page 65](https://arxiv.org/pdf/2605.03658v1#page=65) states the gluing result:

```math
U=\operatorname{Spa}(A,A^+)
\longmapsto
D((A,A^+)^{\blacksquare})
\quad\text{is a sheaf of }\infty\text{-categories on }X.
```

**Reading the symbols.** The ring $A^+$ contains the elements declared to have size at most one. The space $\operatorname{Spv}(A)$ contains equivalence classes of valuations on $A$, and $\operatorname{Spa}(A,A^+)$ is the region where every element of $A^+$ is bounded by one. Braces mean “the set of,” $\in$ means “belongs to,” and the vertical bar means “such that.” The absolute-value notation $|f(x)|$ is the size assigned to $f$ by the valuation $x$. The open patch is $U$, and $D((A,A^+)^{\blacksquare})$ is its derived category of complete modules. A sheaf means that compatible local objects glue uniquely, including all their higher compatibility data. The infinity symbol indicates that these higher homotopies are retained.

**Why it matters.** The first two formulas say that the algebraic bounded subring and the geometric valuation region determine each other. The theorem then allows the local module categories attached to those regions to assemble into one global category.

**In the simulation.** Selecting bounded functions changes $A^+$. The highlighted dots are the valuations satisfying the first formula. In the overlap view, the two patches display local categories that glue only when their restrictions agree.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/06.html)** to change the chosen bounded functions and watch the corresponding region of valuations change.

## 7 · The six operations

The local and global constructions now fit into the **six-operations formalism**, the standard organizational structure for modern cohomology theories. To each space it assigns a category of sheaf-like objects. A map of spaces then gives operations that move or compare those objects in controlled ways.

![Tensor and internal Hom, pullback and pushforward, and the two shriek operations are arranged as three adjoint pairs](guide/07-six-operations/six.png)

The six operations come in three related pairs. In each pair, one operation is adjoint to the other, meaning that maps after applying the first correspond naturally to maps after applying its partner.

**Combine and separate.** Tensor product combines two sheaves on the same space. Internal Hom is its partner and records the maps from one sheaf into another.

**Pull back and push forward.** For a map of spaces, pullback transfers a sheaf from the target to the source. Ordinary pushforward transfers information from the source back to the target and is the right adjoint of pullback.

**Push forward with compact support, and its counterweight.** Lower shriek pushes forward while controlling behaviour at the boundary. Upper shriek is its right adjoint and produces the dualizing object when applied to the unit.

The lectures explain that the first four operations can be constructed without condensed mathematics. The difficult step is lower shriek, the compactly supported pushforward built from the boundary theory in section 5. Constructing this third pair is the reason condensed modules enter the six-operation story ([the discussion after Theorem 11.1, page 72](https://arxiv.org/pdf/2605.03658v1#page=72)).

Two familiar cases determine how lower shriek must behave. For a proper map, nothing can escape through a boundary, so compactly supported pushforward equals ordinary pushforward. For an open inclusion, upper shriek equals pullback, which makes lower shriek the left adjoint of pullback. Nagata compactification factors a separated finite-type map into an open inclusion followed by a proper map. These rules therefore determine the candidate operation, while the theorem must still show that it is independent of the chosen factorization and behaves coherently under composition.

### The mathematics

The discussion after [Theorem 11.1, page 72 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=72) arranges the six operations into three adjoint pairs:

```math
-\otimes_X B\dashv R\!\operatorname{Hom}_X(B,-),
\qquad
f^*\dashv f_*,
\qquad
f_!\dashv f^!.
```

Two required identities are

```math
f_!\cong f_*\quad\text{when }f\text{ is proper},
\qquad
f^!\cong f^*\quad\text{when }f\text{ is étale}.
```

The projection formula is

```math
f_!(A\otimes_X f^*B)\cong f_!A\otimes_Y B.
```

**Reading the symbols.** The tensor product $\otimes_X$ combines objects on the same space $X$. The derived internal Hom $R\!\operatorname{Hom}_X$ records maps from $B$. The map of spaces is $f:X\to Y$. Its pullback is $f^*$, ordinary pushforward is $f_*$, compactly supported pushforward is $f_!$, and the right adjoint of the latter is $f^!$. The symbol $\dashv$ says that the operation on the left is left adjoint to the one on the right. The symbol $\cong$ means naturally isomorphic. Proper means that nothing escapes at the boundary, and étale is the local condition under which upper shriek agrees with pullback. In the final line, $A$ is an object on $X$ and $B$ is an object on $Y$.

**Why it matters.** The first four operations exist in ordinary derived algebraic geometry. Constructing $f_!$ and therefore $f^!$ is the difficult part. The boundary theory from chapter 5 supplies this missing pair and makes the required identities coherent under composition.

**In the simulation.** The operation selector chooses one of the six symbols. The arrows show its source and target, and switching to the paired operation reverses the adjunction. Proper and open examples display the two special rules that determine compactly supported pushforward.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/07.html)** to apply each operation to a sheaf and compare the directions of the three adjoint pairs.

## 8 · Duality, watched

Duality relates two kinds of cohomological information through a pairing that produces a scalar on the base. A perfect pairing loses no information: either input can be recovered from how it pairs with every possible input on the other side. For a smooth space, the complementary object involves differential forms and a shift by the dimension.

![A torus rotates in three dimensions while complementary cohomological degrees are paired and sent through the trace](guide/08-duality-watched/duality.gif)

The animation represents this complementary pairing on a surface. One class lies in a lower degree, its partner lies in the corresponding complementary degree, and compactly supported pushforward carries their product to the base. A trace map then turns the top-degree result into one scalar.

The precise theorem assumes a separated smooth map of finite type from a space X to a base ring, with a fixed relative dimension ([Theorem 11.1, page 71](https://arxiv.org/pdf/2605.03658v1#page=71)). It constructs compactly supported pushforward, proves that it agrees with ordinary cohomology when the map is proper, and supplies a canonical trace from top-degree differential forms to the base. For every suitable complex on X, pairing with the trace identifies its dual with the corresponding differential-form complex. This is coherent duality in the solid-module setting.

![Equal-dimensional degree-zero and degree-one spaces pair into a top-degree class whose trace lies in the base ring](guide/08-duality-watched/pairing.png)

Three features explain how the previous sections contribute to this result. Together, they connect the abstract framework to the classical theorem.

**The dualizing object is characterized by an adjunction.** Upper shriek is defined as the right adjoint of compactly supported pushforward, and its value on the unit is the dualizing complex. The theorem then identifies this canonical object with the expected differential forms in the smooth case and proves that the trace pairing is perfect.

**Finiteness follows from preservation of compactness.** Compactly supported pushforward preserves compact objects. For a proper map it agrees with ordinary pushforward, which also preserves discreteness, so this formal statement recovers the classical finite-generation result for coherent cohomology ([Remark 8.3, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)).

**The construction passes through nondiscrete modules.** Boundary functions contain infinite tails, so compactly supported pushforward generally leaves the category of ordinary modules. Its right adjoint returns the dualizing complex to the discrete setting. Condensed mathematics supplies the larger middle category in which the full construction can be carried out.

### The mathematics

[Theorem 11.1, page 71 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=71) applies to a separated smooth map $f:X\to\operatorname{Spec}R$ of finite type and relative dimension $d$. With

```math
\omega_{X/R}:=\bigwedge^d\Omega^1_{X/R},
```

The theorem first constructs compactly supported pushforward. It then gives a trace and a perfect duality:

```math
\operatorname{tr}:f_!\omega_{X/R}[d]\longrightarrow R,
```

```math
R\!\operatorname{Hom}_{X}(C,\omega_{X/R})[d]
\xrightarrow{\sim}
R\!\operatorname{Hom}_{R}(f_!C,R).
```

Properness removes the boundary distinction. When $f$ is proper, the theorem also gives

```math
f_!C\cong R\Gamma(X,C).
```

**Reading the symbols.** The space is $X$, the base ring is $R$, and $\operatorname{Spec}R$ is its affine base space. The integer $d$ is the relative dimension. The module $\Omega^1_{X/R}$ contains relative differential one-forms, and $\bigwedge^d$ takes their top exterior power, denoted $\omega_{X/R}$. The functor $f_!$ is compactly supported pushforward. Square brackets $[d]$ shift cohomological degree by $d$. The trace $\operatorname{tr}$ sends the top-degree compactly supported class to a scalar in $R$. The letter $C$ names any suitable complex on $X$. The derived Hom expressions are the two dual objects, and the arrow marked $\sim$ says that the trace pairing identifies them. The notation $R\Gamma(X,C)$ is derived global cohomology.

**Why it matters.** The theorem identifies the right adjoint of compactly supported cohomology with the expected differential-form object and proves that its pairing loses no information. Proper spaces recover classical coherent duality because compactly supported and ordinary cohomology then agree.

**In the simulation.** The degree controls choose a class and its complementary partner. Their product enters the top degree, and the final trace control sends it to one scalar. The pairing is marked complete only when the degrees add to the displayed dimension $d$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/08.html)** to pair complementary classes and follow their product through the trace to a scalar.

## Where this leaves you

The three parts form one progression. Probes first place topology inside algebra by recording continuous families rather than isolated points. Compatible measures then give solid groups a unique rule for infinite integer-weighted sums. Finally, an analytic ring combines multiplication with its own theory of measures, allowing local algebraic constructions to be glued into geometry. In that setting, compactly supported cohomology and its right adjoint produce coherent duality.

The lectures describe a 2019 course and were published in this form in May 2026. Their preface points to later developments by Clausen and Scholze, including broader theories of analytic rings, real and complex variants, light condensed mathematics, and analytic stacks. The notes also identify results whose proofs were not previously available in the literature. In particular, they include an appendix proving the universal resolution used in Lecture IV ([Remark 4.6, page 25](https://arxiv.org/pdf/2605.03658v1#page=25)). This guide remains an introduction to the lectures rather than a replacement for their full statements and proofs.

## How this part lines up with the lectures

| this guide | in the lectures |
|---|---|
| section 1, a ring with a rule | Definition 7.1, page 45; Definition 7.4, page 46 |
| section 2, two rules that work | Proposition 7.8, page 48; Remark 7.9, page 49 |
| section 3, the real line's own rule | Example 7.10, page 49; Theorem 7.11, page 50 |
| section 4, functions near the edge | Lecture VIII from page 53; Remark 8.5, page 54 |
| section 5, cohomology with compact support | Theorem 8.1 and Theorem 8.2, page 53; Remarks 8.3 to 8.5, page 54 |
| section 6, gluing the local pictures | Proposition 9.2, page 63; Theorem 9.8, page 65; Lecture X from page 66 |
| section 7, the six operations | the discussion after Theorem 11.1, page 72 |
| section 8, duality, watched | Theorem 11.1, page 71; Remark 8.4, page 54 |

## Checking it yourself

The commands below rerun the finite calculations and regenerate their figures. They do not attempt to prove the categorical theorems quoted from the lectures.

```
cd condensed-math
make venv
make test
make figures
```

For this part, the tests:

- compute how a measure's size changes when boxes are merged, and confirm the ratio is at most one exactly when the exponent is at most one
- confirm the closed form for the worst case: merging a number of equal boxes changes the size by that number raised to one minus the reciprocal of the exponent
- confirm the unit ball is convex at and above exponent one and not convex below it
- count the tails on the line and on the coordinate cross by truncation, and confirm the cross keeps one extra piece beyond the two branches' tails
- confirm the counts are stable as the truncation is pushed further out

The analytic-ring results, gluing theorem, six-operations formalism, and duality theorem are all categorical statements quoted from the lectures. No finite test establishes them. The file `notes/research-content.md` distinguishes these quotations from the explicit computations and finite models used in the figures.

## Glossary

| this guide's plain phrase | the standard mathematical term |
|---|---|
| a ring with a rule | an analytic ring |
| the rule | the theory of measures |
| the exponent | the p of the ell-p norm on measures |
| swept exponents | the colimit over exponents below the target, the liquid theory |
| the edge ring | the formal Laurent series in the inverse coordinate |
| functions near the edge | sections over the complement of the compact part |
| tails | the strictly negative part of a Laurent expansion |
| compactly supported collection | cohomology with compact support, the lower-shriek pushforward |
| the counterweight | the right adjoint, upper-shriek |
| the dualizing object | the dualizing complex |
| size at most one | a chosen integrally closed subring, the plus part of a Huber pair |
| valuation space | the space of equivalence classes of valuations |
| the trace | the trace map of coherent duality |
| the six operations | tensor, internal hom, pullback, pushforward, and the compactly supported pair |
| nothing escapes to the edge | properness |

## Further reading

- The lectures: Peter Scholze, "Lectures on Condensed Mathematics", [arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026, joint work with Dustin Clausen. Lectures VII to XI are this part. The preface lists the later work where each thread continues.
- For section 3: M. Ribe, "Examples for the nonlocally convex three space problem" (1979), and N. Kalton's follow-up, both cited in the lectures at Example 7.10.
- For section 6: R. Huber's work on adic spaces, cited in the lectures for the local structure results of Lecture X.
- `notes/research-content.md` marks every claim above as computed here or quoted.

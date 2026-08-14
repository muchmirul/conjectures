# Shapes You Can Only See By Probing Them

*Part one of three on condensed mathematics. We begin with a familiar problem: the same set of numbers can carry different ideas of nearness, but ordinary algebra does not record that difference well. Step by step, this part introduces probes, explains how a space answers them, and shows how this new description makes subtraction work without losing familiar spaces or their holes. No previous mathematics is assumed.*

![A tree adds one level of branches at a time as the intervals below become smaller and more numerous](guide/00-start-here/hero.gif)

The animation introduces the basic object used throughout this guide. Begin with one box, split it into two, and then split each new box again. Every stage is finite, so you can see the whole stage at once. If the process continues forever, each path through the boxes approaches a point, while the full branching pattern remembers how those points were separated. We will call the resulting object a **probe**. Condensed mathematics describes a space through all the continuous ways probes can enter it, rather than through its points alone.

This is part one of three. It covers the first three lectures of Peter Scholze's *Lectures on Condensed Mathematics* ([arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026), which record a course taught in Bonn in 2019 and present joint work with Dustin Clausen. Part two develops infinite sums, and part three moves from addition to rings and geometry. The text, figures, and code for every computed example are available in the open source repository at [github.com/muchmirul/conjectures](https://github.com/muchmirul/conjectures). Most sections also include a [page you can play with](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/index.html), where changing one choice updates the corresponding picture.

```
    the problem                 1  two real lines, and the broken bridge
    the new object              2  probes that branch
                                3  what a shape says to a probe
                                4  cut, and glue
    what it repairs             5  the quotient with no points
                                6  probes that never need folding
    what it costs               7  nothing was lost
                                8  counting holes
```

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/00.html)** to build a probe one split at a time and see how its finite stages fit together.

## 1 · Two real lines

Start with the set of all real numbers and give it two different rules about nearness. In the first copy, forget nearness completely. Two numbers are either equal or different, and no distinct numbers count as close. We will call this copy **the dust**, which is the real line with the discrete topology.

In the second copy, keep the usual notion of distance. In this copy, 0.999 is close to 1, sequences can approach limits, and continuous motion makes sense. We will call this copy **the ruler**, which is the ordinary topological real line.

![Two copies of the real numbers, one shown as separate dots and one as a continuous line, with equal values joined](guide/01-two-real-lines/bijection.gif)

Send each number in the dust to the same number on the ruler. The animation shows this matching. Every input has one output, different inputs remain different, and every point on the ruler is reached. As a map of underlying sets, it is a perfect one-to-one correspondence.

However, the two topological groups are not the same. The map from the dust to the ruler is continuous, but its inverse is not. A single point is open in the dust, while a single point is not open on the ruler, so the inverse fails the basic test for continuity. A bijection of points therefore does not guarantee an isomorphism of topological objects.

This causes a precise algebraic problem. In an abelian setting, one studies a map by finding its kernel, the elements it sends to zero, and its cokernel, the part of the target it fails to account for. If both are zero, the map should be an isomorphism. For the map above, both are zero even though the map is not an isomorphism, so topological abelian groups do not support this standard algebraic test.

The lectures begin with this example ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)) and give two related failures. These examples identify the problem that condensed mathematics is designed to solve. The point sets of the dust and ruler agree, so a successful repair must record how whole compact families of points move, not merely which individual points exist.

### The mathematics

[Example 1.9, page 9 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=9) writes the identity map and its condensed cokernel explicitly. In topological abelian groups the same map has zero kernel and cokernel, although it is not an isomorphism:

```math
\mathbb{R}_{\mathrm{disc}} \xrightarrow{\;\mathrm{id}\;} \mathbb{R},
\qquad \ker(\mathrm{id})=0, \qquad \operatorname{coker}(\mathrm{id})=0,
\qquad \mathbb{R}_{\mathrm{disc}}\not\cong\mathbb{R}.
```

After passing to condensed abelian groups, the cokernel $Q$ is no longer zero. Its value on a profinite probe $S$ is

```math
Q(*)=0,
\qquad
Q(S)=\frac{C(S,\mathbb{R})}{C_{\mathrm{lc}}(S,\mathbb{R})}\neq 0
\quad\text{for suitable }S.
```

**Reading the symbols.** The symbol $\mathbb{R}$ means the real numbers, and $\mathrm{disc}$ gives them the discrete topology. The label $\mathrm{id}$ means that each number is sent to itself. The symbols $\ker$ and $\operatorname{coker}$ mean kernel and cokernel. The symbol $0$ is the zero group, while $\not\cong$ means “is not isomorphic to.” The letter $Q$ names the condensed cokernel, and $*$ is the one-point probe. The notation $C(S,\mathbb{R})$ means all continuous maps from $S$ to the usual real line. The subscript $\mathrm{lc}$ restricts this to locally constant maps, which are exactly the continuous maps into the discrete real line. The fraction bar means quotient group, and $\neq 0$ says that this quotient has a nonzero element for some probe.

**Why it matters.** Points see $Q(*)=0$, but a larger probe can see $Q(S)\neq0$. Condensed groups therefore retain the missing topological quotient. [Theorem 1.10, page 9](https://arxiv.org/pdf/2605.03658v1#page=9) then states that condensed abelian groups form an abelian category, so zero kernel and zero cokernel once again force a map to be an isomorphism.

**In the simulation.** The two rows represent $\mathbb{R}_{\mathrm{disc}}$ and $\mathbb{R}$. Each vertical line is one value of $\mathrm{id}$. The point-level kernel and cokernel stay at zero, even though the two rows still have different rules for nearness.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/01.html)** to inspect the matching and see why its empty kernel and cokernel do not make it an isomorphism.

## 2 · Probes that branch

To detect nearness, we need an object that carries nearness of its own. Build one by starting with a box and repeatedly dividing it into smaller boxes. At each stage there are only finitely many pieces, together with a map telling us which new piece came from which old one. The infinite object is completely described by these finite stages and their connecting maps.

![Finite stages of three probes shown side by side: binary branching, an approaching sequence, and branching in base p](guide/02-branching-probes/probes.png)

A **probe** consists of such a compatible sequence of finite divisions and the points obtained by following branches through every stage. The lectures call this a profinite set. Three examples will be used repeatedly in this guide.

The **halving probe** divides every box into two at each stage. After ten rounds it has 1024 boxes. Its limiting points form the classical Cantor set, which can also be made by repeatedly removing the middle third of every remaining interval.

The **approaching probe** records one convergent sequence and its limit. At stage five, the first five points have been separated into their own boxes, while all later points and the limit still occupy one final box. Further stages separate one more point at a time.

The **counting-in-base-p probe** divides each box into p pieces. Its limiting points form the p-adic integers, an important number system in which divisibility by powers of p determines nearness. Part two will use this probe to explain an infinite sum that converges in one notion of size but not another.

The formal name *profinite set* means an inverse limit of finite sets ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). Two parts of that description are important. Every individual stage is finite, and all information about the probe lies in the stages and the maps between them. The code follows this definition literally by storing finite sets and their transition maps. Its tests check the expected growth of all three probes and verify that compatible data can be read consistently through their levels.

### The mathematics

The definition used in [Definition 1.2, page 6 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=6) is that a profinite set is an inverse limit of finite sets:

```math
S \cong \varprojlim_i S_i,
\qquad
\pi_{ji}:S_j\twoheadrightarrow S_i \quad (j\ge i),
\qquad
\pi_{ki}=\pi_{ji}\circ\pi_{kj} \quad (k\ge j\ge i).
```

**Reading the symbols.** The letter $S$ names the whole probe, while each $S_i$ is its finite stage numbered $i$. The symbol $\cong$ means “is isomorphic to,” and $\varprojlim$ means inverse limit: a point of $S$ is a compatible choice of one box at every stage. The map $\pi_{ji}$ sends a box at the finer stage $j$ back to its parent at stage $i$. The double-headed arrow says that every coarse box has at least one finer box above it. The inequalities order the stages. The symbol $\circ$ means “followed by,” and the final equality says that going back two stages at once gives the same answer as going back one stage at a time.

**Why it matters.** This formula replaces one infinite object by finite stages joined by exact compatibility maps. The halving, approaching, and base-$p$ probes differ only in the finite sets $S_i$ and the maps $\pi_{ji}$.

**In the simulation.** The depth control chooses the largest index $i$ shown. Each row is one finite set $S_i$, and every connecting branch displays a transition map $\pi_{i+1,i}$. Selecting a box shows the finer boxes that map back to it.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/02.html)** to compare the three probes, change their depth, and inspect the points contained in any box.

## 3 · What a shape says to a probe

We can now use a probe to examine a space. A probe **lands** in a space when its points are mapped there continuously. Continuity means that the map respects the nearness already carried by the probe. In particular, if probe points approach a limit, their images must approach the image of that limit.

![Points from an approaching sequence map to a target, first with the correct limit and then with a different limit](guide/03-what-a-shape-says/landing.gif)

The animation tests two attempted landings of the approaching probe. In the first, the sequence of images approaches the image of the limit point, so the landing is continuous. In the second, the sequence approaches one place while the limit point is sent elsewhere. That break in continuity causes the landing to be rejected.

This suggests a new way to describe a space. For every possible probe, record every continuous way that probe can land in the space. The resulting record is like an answer sheet: each probe poses a test, and the space answers with its set of legal landings. This answer sheet remembers not only which points exist but also which compact families of points fit together continuously.

An answer sheet satisfying the two compatibility rules in the next section is called a **condensed set** ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). If the original space has addition, its landings can be added point by point, producing a condensed group. If it also has multiplication, the same construction produces a condensed ring ([Example 1.3, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)).

This description immediately distinguishes the two real lines. The approaching probe has many continuous landings in the ruler, because any convergent sequence of real numbers and its limit gives one. In the dust, a convergent sequence must eventually remain at one value, so nearly all of those landings disappear. Although the dust and ruler have the same individual points, their answer sheets are different.

For spaces with a distance, the approaching probe already contains enough information to detect the topology. Such a space is determined by its convergent sequences, and this probe tests exactly those sequences ([Remark 1.6, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). More general spaces require all profinite probes, but this small example explains why probes can see information that points alone miss.

![Points inside a planar set approach a boundary point that the set does not contain](guide/03-what-a-shape-says/sequence_test.png)

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

## 4 · Cut, and glue

The entries of an answer sheet cannot be chosen independently. They must respect two basic ways of relating probes, called **cut** and **glue**. Together, these are the sheaf conditions in the definition of a condensed set.

**Cut.** If a probe is a disjoint union of two pieces, then a landing of the whole probe contains exactly the same information as one landing for each piece. Since the pieces do not meet, the two landings can be chosen independently and then combined.

![Two disjoint pieces of a probe contribute one independent answer each to the answer for the whole probe](guide/04-cut-and-glue/cut.png)

**Glue.** Suppose a larger probe covers a smaller probe. A landing on the covering probe descends to the smaller one when it assigns the same result wherever the cover represents the same point more than once. If that agreement holds, there must be one and only one landing downstairs that produces the given landing upstairs.

![Two answers on overlapping covering pieces agree in the shared region and combine into one answer below](guide/04-cut-and-glue/glue.gif)

The glue rule prevents two kinds of failure. Compatible local answers must assemble into a global answer, so information cannot agree everywhere locally but fail to exist globally. The global answer must also be unique, so the same local data cannot produce two different results. The lectures place these two requirements directly after the definition ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). Thus, a condensed set is precisely an answer sheet on profinite probes that respects disjoint pieces and compatible covers.

A size issue also appears in the definition, and the lectures address it immediately ([Remark 1.4, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)). There are too many profinite sets to collect into one ordinary set, so the phrase "every probe" must be handled carefully. One first chooses a sufficiently large size bound, develops the theory within that bound, and proves that enlarging it does not change the resulting mathematics. This guide will treat that step as background bookkeeping.

### The mathematics

[Definition 1.2, page 6 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=6) gives the two sheaf conditions explicitly. For disjoint probes,

```math
T(S_1\sqcup S_2)\xrightarrow{\sim}T(S_1)\times T(S_2).
```

The second condition begins with a surjection $q:S'\twoheadrightarrow S$ and the projections $p_1,p_2:S'\times_S S'\to S'$. The glue condition is

```math
T(S)\xrightarrow{\sim}
\{x\in T(S')\mid p_1^*x=p_2^*x\text{ in }T(S'\times_S S')\}.
```

**Reading the symbols.** The letter $T$ is an answer sheet, and $T(S)$ is its set of answers on the probe $S$. The symbol $\sqcup$ means disjoint union, $\times$ means Cartesian product, and an arrow marked $\sim$ means a bijection. The map $q$ is a cover, shown by the double-headed arrow. The fibre product $S'\times_S S'$ contains pairs of covering points that represent the same point below. The maps $p_1$ and $p_2$ select the first and second member of such a pair. The star in $p_i^*$ means pullback. Braces mean “the set of,” $\in$ means “belongs to,” and the vertical bar means “such that.” The equality says that an answer upstairs gives the same value on both representatives of every point downstairs.

**Why it matters.** The first bijection says that separate pieces can be answered independently. The second says that compatible answers on a cover come from exactly one answer below. These are not optional properties; together with $T(\varnothing)=*$, they are the definition of a condensed set.

**In the simulation.** In cut mode, the two controls choose the independent entries in $T(S_1)\times T(S_2)$. In glue mode, they choose the two pullbacks $p_1^*x$ and $p_2^*x$. An answer below appears only when those values agree.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/04.html)** to assign local answers and see how the cut and glue rules decide whether they form one valid answer.

## 5 · The quotient with no points

We can now revisit the map from the dust to the ruler. Their answer sheets are different because probes detect continuous families on the ruler that do not exist in the dust. Condensed groups therefore allow us to form a meaningful cokernel of the map. This guide calls that cokernel **the ghost**.

At a single point, the ghost looks like zero: the dust and ruler contain exactly the same real numbers, so their point-level quotient has nothing left. A branching probe gives a different result. It can move continuously through the ruler in ways that are not locally constant and therefore cannot come from the discrete real line.

![Successive refinements build a continuous real-valued function that never becomes locally constant on the probe](guide/05-the-ghost/ghost.gif)

The animation constructs such a landing on the halving probe. Values are assigned on increasingly fine boxes in a compatible way. In the limit, the resulting map to the ruler is continuous but never becomes constant on a finite collection of boxes. Maps from a compact probe to the dust must be locally constant, so this landing cannot come from the dust. It therefore gives a nonzero element of the ghost ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)).

The ghost is consequently nonzero even though its value on the one-point probe is zero. This explains why the original kernel-and-cokernel test failed: it examined individual points and missed a quotient visible only to larger probes. In the condensed setting, that missing quotient becomes an ordinary algebraic object instead of disappearing.

The general result can now be stated in the form needed for algebra:

> Condensed abelian groups form an abelian category. In this category, a map with zero kernel and zero cokernel is an isomorphism.

This is the opening theorem of the lectures ([Theorem 1.10, page 9](https://arxiv.org/pdf/2605.03658v1#page=9), restated with the size bound fixed as [Theorem 2.2, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)). In standard language, condensed abelian groups form an abelian category with especially strong closure properties. The usual machinery of kernels, cokernels, and exact sequences therefore works here, including for topological information that ordinary topological groups fail to record algebraically.

### The mathematics

The map from the discrete to the usual real line has a condensed cokernel $Q$. [Example 1.9, page 9 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=9) identifies it by

```math
Q(S)=C(S,\mathbb{R})/C_{\mathrm{lc}}(S,\mathbb{R}),
\qquad Q(*)=0,
\qquad Q\neq0.
```

The surrounding theorem places this example in a reliable algebraic category. [Theorem 1.10, page 9](https://arxiv.org/pdf/2605.03658v1#page=9) states in particular that

```math
\operatorname{Cond}(\mathrm{Ab})\text{ is an abelian category.}
```

**Reading the symbols.** The letter $Q$ names the ghost, and $Q(S)$ is what the probe $S$ sees. The notation $C(S,\mathbb{R})$ means continuous real-valued maps. The subscript $\mathrm{lc}$ means locally constant, so the denominator contains the maps that already come from the discrete reals. The slash forms the quotient. The star is the one-point probe. Thus $Q(*)=0$ says that points see nothing, while $Q\neq0$ says that the condensed group itself is not zero. The notation $\operatorname{Cond}(\mathrm{Ab})$ means condensed objects in the category of abelian groups, and “abelian category” is the standard setting where kernels, cokernels, and exact sequences work together.

**Why it matters.** The formula displays the information that pointwise algebra lost. A continuous map that is not locally constant represents a nonzero class in $Q(S)$, even though every class vanishes on the one-point probe.

**In the simulation.** The wobble control builds an element of $C(S,\mathbb{R})$. At zero wobble the map is locally constant and its quotient class is zero. A nonzero wobble makes the displayed map vary through every refinement, so it survives in $Q(S)$ while the point count $Q(*)$ stays zero.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/05.html)** to build a probe-level element of the ghost while its value on individual points remains zero.

## 6 · Probes that never need folding

This section uses only the ideas already introduced and asks which probes are easiest to work with. Suppose one probe maps onto another, so every point downstairs has at least one point above it. Choosing one point above each point downstairs gives a **lift**. For the lift to be useful, that choice must also be continuous.

![Alternating choices between two points above each sequence term leave no continuous choice above the limit](guide/06-unfoldable-probes/folding.gif)

A continuous lift does not always exist. In the animation, the possible choices alternate as points approach the limit. Following either set of choices forces a jump at the end, so no continuous selection can be made. The covering folds over the target in a way that cannot be continuously undone.

A probe is called **unfoldable** in this guide when every covering onto it has a continuous lift. The standard term is *extremally disconnected* ([Definition 2.4, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)). Important examples come from the Stone-Čech compactification of a discrete set. Start with separate points and add exactly the limiting information needed so that every map from those points to a compact space extends uniquely. To lift a cover, choose a point above each original discrete point; the extension property then turns those choices into one continuous lift on the completion ([Example 2.5, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)).

![Alternating terms of a sequence lie in two separate open-and-closed regions and therefore cannot converge](guide/06-unfoldable-probes/no_convergence.png)

Unfoldable probes behave very differently from familiar geometric spaces. Any convergent sequence in one must eventually be constant ([Warning 2.6, page 12](https://arxiv.org/pdf/2605.03658v1#page=12)). To see the obstruction, colour alternating terms of a nonconstant sequence with two colours. In an unfoldable probe, that colouring extends to two separated regions, leaving infinitely many terms on each side. Such a sequence cannot converge. The same warning notes another unusual fact: the product of two infinite unfoldable probes is never unfoldable.

Their usefulness comes from the glue rule. Since every cover of an unfoldable probe admits a lift, compatible data over the cover descend automatically. An answer sheet is therefore determined by its values on unfoldable probes, and only the cut rule remains to be checked there ([Proposition 2.8, page 12](https://arxiv.org/pdf/2605.03658v1#page=12)). This simpler description is one reason condensed groups have unusually strong algebraic properties, and the next two parts will repeatedly use these probes as convenient building blocks.

### The mathematics

[Definition 2.4, page 11 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=11) calls a compact Hausdorff space $S$ extremally disconnected when every surjection onto it splits:

```math
\forall\,q:S'\twoheadrightarrow S,\quad
\exists\,s:S\to S'\quad\text{such that}\quad q\circ s=\operatorname{id}_S.
```

[Proposition 2.8, page 12](https://arxiv.org/pdf/2605.03658v1#page=12) then reduces a condensed set on such probes to the cut rule

```math
T(\varnothing)=*,
\qquad
T(S_1\sqcup S_2)\xrightarrow{\sim}T(S_1)\times T(S_2),
```

The second line is the remaining condition on these probes. The glue condition follows automatically from the splitting.

**Reading the symbols.** The symbol $\forall$ means “for every,” and $q$ is any surjective map from $S'$ onto $S$. The symbol $\exists$ means “there exists,” and $s$ is a section, or continuous choice of one point above each point of $S$. The composition $q\circ s$ goes up by $s$ and back down by $q$. The expression $\operatorname{id}_S$ is the identity map of $S$, so the equality says that the lift returns every point to itself. The empty-set symbol $\varnothing$ names the empty probe, and $*$ is the single possible answer there. The symbols $\sqcup$, $\times$, and $\sim$ mean disjoint union, product, and bijection.

**Why it matters.** A split cover can always be unfolded by its section. Because of this, checking answer sheets on extremally disconnected probes requires only finite disjoint unions, not a separate descent calculation for every cover. [Warning 2.6, page 12](https://arxiv.org/pdf/2605.03658v1#page=12) adds that convergent sequences in such a probe are eventually constant and that products of two infinite such probes are not extremally disconnected.

**In the simulation.** The selected points define a proposed section $s$. The lift succeeds only when the choices remain continuous at the limit and satisfy $q\circ s=\operatorname{id}_S$. Switching to the unfoldable probe represents the case in which every cover has some continuous section.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/06.html)** to attempt a lift and identify the discontinuity that prevents one from existing.

## 7 · Nothing was lost

Changing from spaces to answer sheets is useful only if familiar spaces and continuous maps can still be recovered. The concern is natural because an answer sheet contains far more entries than a point set. The relevant comparison theorem says that, for a broad class of ordinary spaces, the new description preserves exactly the original maps and keeps distinct spaces distinct.

![Nested classes compare compact Hausdorff spaces, compactly generated spaces, and condensed sets](guide/07-nothing-was-lost/nesting.png)

Read the picture from the centre outward. Compact Hausdorff spaces correspond exactly to condensed sets that satisfy the matching compactness condition ([Theorem 2.16, page 17](https://arxiv.org/pdf/2605.03658v1#page=17)). In familiar Euclidean examples, these are the closed and bounded shapes. A larger surrounding class contains all metric spaces and spaces built from cells. On this larger class, the translation is fully faithful: different spaces have different answer sheets, and maps of answer sheets are exactly the continuous maps of spaces ([Proposition 1.7, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). Condensed sets extend beyond this image, as the ghost from section 5 demonstrates.

![A familiar space is converted to its probe data and reconstructed with the same topology](guide/07-nothing-was-lost/roundtrip.gif)

There is also a return construction. Begin with the point entries of an answer sheet, and declare a subset closed when every probe detects it as closed. For the broad class just described, translating a space into an answer sheet and then applying this construction returns the original topology. The animation follows that round trip.

The comparison has limits, and the lectures state them explicitly. If a topological space has a point that is not closed, its probe data do not define a condensed set of the required kind ([Warning 2.14, page 16](https://arxiv.org/pdf/2605.03658v1#page=16)). In the other direction, the return to ordinary topology can identify condensed information that topology cannot retain. One example involves compact objects built as increasing unions of strictly smaller closed pieces. The lectures interpret this as a limitation of ordinary topology, and note that the issue does not occur for countable colimits.

### The mathematics

[Proposition 1.7, page 9 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=9) says that the translation $X\mapsto\underline X$ is fully faithful on compactly generated spaces:

```math
\operatorname{Hom}_{\mathrm{Top}}(X,Y)
\xrightarrow{\sim}
\operatorname{Hom}_{\operatorname{Cond}(\mathrm{Set})}(\underline X,\underline Y).
```

It also gives the return map, and [Theorem 2.16, page 17](https://arxiv.org/pdf/2605.03658v1#page=17) identifies the compact case:

```math
(\underline X(*))_{\mathrm{top}}\cong X,
\qquad
\{\text{compact Hausdorff spaces}\}\simeq
\{\text{qcqs condensed sets}\}.
```

**Reading the symbols.** The notation $\operatorname{Hom}$ means the set of maps. The subscript $\mathrm{Top}$ restricts to continuous maps of topological spaces, while $\operatorname{Cond}(\mathrm{Set})$ means condensed sets. The underline sends a space to its probe answers. An arrow marked $\sim$ is a bijection, so every map of answer sheets comes from one continuous map. The expression $\underline X(*)$ reads the point entry, and the subscript $\mathrm{top}$ equips it with the topology detected by all probes. The symbol $\cong$ means isomorphic. The double arrow $\simeq$ means an equivalence of categories. The abbreviation qcqs means quasicompact and quasiseparated.

**Why it matters.** The translation preserves both objects and maps on the familiar class used in the guide. It is an enlargement of topology, not a replacement that forgets ordinary spaces. [Warning 2.14, page 16](https://arxiv.org/pdf/2605.03658v1#page=16) gives the stated boundary: a space with a nonclosed point does not define a condensed set of this kind.

**In the simulation.** Choosing a familiar space runs $X\mapsto\underline X\mapsto(\underline X(*))_{\mathrm{top}}$ and returns the same picture. Choosing the space with a nonclosed point stops at the first arrow, showing the warning rather than claiming the theorem there.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/07.html)** to follow a space through the translation and compare the recovered result with the starting space.

## 8 · Counting holes

The final check is whether the translation preserves topological features such as holes. A basic way to detect a hole in a circle is to draw a closed path and count how many times it travels around the centre. This count is the winding number, and it remains unchanged when the path is continuously deformed without being broken.

![A closed path deforms around a circle while its integer winding number remains unchanged](guide/08-counting-holes/winding.gif)

The animation computes the winding number of a closed path around the circle. This number is always an integer and records both the number of turns and their direction. A generator of the circle's first cohomology measures this winding, so the first cohomology group is one copy of the integers.

Products of circles create more independent directions for loops. The product of two circles is the surface of a torus, which has one loop around its central opening and another around the body of the tube.

![A torus rotates in three dimensions with one loop around the central opening and another around the tube](guide/08-counting-holes/torus.gif)

The rotating view makes the three-dimensional surface and its two independent loops visible. Products of more circles have higher-degree holes formed by choosing several circle directions at once. The lectures compute this pattern for any number of factors, including infinitely many ([Proposition 3.1, page 20](https://arxiv.org/pdf/2605.03658v1#page=20)).

![Rows of bars give the cohomology ranks for products of one through six circles and follow Pascal's triangle](guide/08-counting-holes/ranks.png)

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

## Where part one leaves you

Part one has changed the basic description of a space. A probe is an inverse system of finite sets, and a condensed set records how every probe can land in it while respecting cut and glue. For familiar spaces, this translation preserves the topology, continuous maps, and cohomology. At the same time, it reveals objects such as the ghost, which have no nonzero point-level value but are visible to larger probes. This extra information restores the algebra of kernels and cokernels.

We have not yet defined how to add an infinite family of elements. That requires a rule for convergence or completion, and different rules can give different answers to the same formal series. Part two develops such a rule from compatible weights on the finite stages of a probe. The resulting notion is called solidity.

**[Part two: Infinite Sums That Finally Land](../condensed-math02/ARTICLE.md)**

## How this part lines up with the lectures

The lectures are kept in this repository at `docs/condensed-math/paper/lectures-on-condensed-mathematics.pdf` and published at [arXiv:2605.03658](https://arxiv.org/abs/2605.03658). The following table shows where each section's definitions and quoted results appear in the source.

| this guide | in the lectures |
|---|---|
| section 1, two real lines | Question 1.1 and the problem list, page 6; Example 1.9, page 9 |
| section 2, probes that branch | Definition 1.2, page 6, the profinite sets |
| section 3, what a shape says | Example 1.3, page 7; Remark 1.6, page 9 |
| section 4, cut and glue | the two sheaf conditions under Definition 1.2, page 6 |
| section 5, the quotient with no points | Example 1.9, page 9; Theorem 1.10, page 9; Theorem 2.2, page 11 |
| section 6, probes that never fold | Definition 2.4 and Example 2.5, page 11; Warning 2.6 and Proposition 2.8, page 12 |
| section 7, nothing was lost | Proposition 1.7, page 9; Warning 2.14, page 16; Theorem 2.16, page 17 |
| section 8, counting holes | Proposition 3.1, page 20; Theorem 3.2, page 21; Theorem 3.3, page 22 |

## Checking it yourself

You can rebuild the figures and rerun every finite computation from the repository. These commands require Python and a command line, but no additional mathematics.

```
cd condensed-math
make venv        # prepare the software once
make test        # recompute every number this guide quotes
make figures     # rebuild every picture
```

For this part, the tests:

- build the three probes as honest inverse systems and check the level sizes double, grow by one, and multiply by p
- check every stored probe really is an inverse system, with surjective transition maps
- check that reading a function at a coarser level and at a finer one gives the same integral
- run Bergman's basis construction on the halving probe and confirm it produces exactly as many basis elements as the level has boxes
- recompute the hole counts of a stack of circles and confirm the binomial pattern of Proposition 3.1
- compute the winding number of sample loops and confirm it is a whole number that survives deformation

The categorical results are quoted rather than computed. These include the claims that condensed groups form an abelian category and that familiar spaces embed fully faithfully. A finite program cannot verify a theorem about every object in an entire category. The file `notes/research-content.md` labels each claim as computed, a finite shadow of an infinite result, or quoted, and gives its source.

## Glossary

| this guide's plain phrase | the standard mathematical term |
|---|---|
| a probe | a profinite set |
| the dust of a probe | the underlying set of the profinite set, its inverse limit |
| a stage of a probe | one finite set in the inverse system |
| the halving probe | the Cantor set, the limit of the powers of a two-point set |
| the approaching probe | the one-point compactification of the natural numbers |
| the counting-in-base-p probe | the p-adic integers |
| a landing | a continuous map from the probe to the target |
| an answer sheet | a sheaf on the site of profinite sets |
| a condensed set | the same thing, the subject's own name for it |
| the dust (of the real line) | the real numbers with the discrete topology |
| the ruler | the real numbers with their usual topology |
| the ghost | the cokernel of the map from the discrete reals to the usual reals |
| kill-list, miss-list | kernel, cokernel |
| cut and glue | the sheaf conditions for finite disjoint unions and for surjections |
| unfoldable | extremally disconnected |
| completing separate points so every map out of them survives | the Stone-Čech compactification of a discrete set |
| a lift | a section of a surjection |
| a hole count | a cohomology group |
| the first hole count of a circle | the first cohomology of the circle, generated by the winding number |

## Further reading

- The lectures themselves: Peter Scholze, "Lectures on Condensed Mathematics", [arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026, and in `docs/condensed-math/paper/`. The material is joint work with Dustin Clausen. Lectures I to III are the ones this part retells.
- For the folding-free probes: A. M. Gleason, "Projective topological spaces", *Illinois Journal of Mathematics* 2 (1958), which the lectures cite for both the definition and the fact that nothing converges in one.
- The file `notes/research-content.md` lists each claim above and marks it as computed here or quoted.

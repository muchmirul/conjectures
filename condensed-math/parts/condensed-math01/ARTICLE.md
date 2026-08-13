# Shapes You Can Only See By Probing Them

*Part one of three on condensed mathematics. A set with a distance on it carries two structures that do not fit together properly, and the mismatch breaks ordinary algebra. This part builds the repair from the beginning: what a probe is, what a shape says to one, and why describing a shape that way makes subtraction work again. You do not need a maths background, and every idea arrives as a picture you can move.*

![A branching probe growing level by level while the boxes it cuts a line into get finer and finer](guide/00-start-here/hero.gif)

The animation shows the only kind of object this whole subject is built on. You start with one box, split it in two, split each half in two, and keep going. At every stage you have a plain finite list of boxes, and the picture records nothing except which box sits inside which. If you follow the splitting forever, the boxes shrink onto a dust of points, and that dust, together with the memory of how it was cut, is called a **probe** in this guide. Everything that follows is about what happens when you stop describing a shape by its points and start describing it by what it says to probes like this one.

This is part one of three. It covers the first three lectures of Peter Scholze's *Lectures on Condensed Mathematics* ([arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026), which record a course taught in Bonn in 2019, joint work with Dustin Clausen. Part two is about infinite sums, part three about geometry. Everything here comes from the open source repository at [github.com/muchmirul/conjectures](https://github.com/muchmirul/conjectures): the text, every figure, and the code behind each computed claim. Most sections also have a [page you can play with](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/index.html), where you change the main choice and see how the picture changes.

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

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/00.html)** to build the probe yourself, one split at a time.

## 1 · Two real lines

Take the real numbers, the whole endless ruler of them, and write them down twice. In the first copy, forget every idea of nearness. Two numbers are either the same number or different numbers, and that is all you may ask. The numbers sit apart like grains of sand, and no grain is nearer any other. Call this copy **the dust**.

In the second copy, keep nearness. Now 0.999 is close to 1, a sequence can approach a limit, and a function can be continuous. Call this copy **the ruler**.

![The same numbers drawn twice, as separated grains and as a continuous ruler, with every grain matched to its point](guide/01-two-real-lines/bijection.gif)

There is an obvious way to go from the dust to the ruler, which is to send each number to itself. The animation matches them up, and nothing is left over on either side. Every number of the dust arrives somewhere, no two arrive at the same place, and every point of the ruler is arrived at, so the map loses nothing and adds nothing.

Even so, the dust and the ruler are not the same object, because on the ruler you may speak of limits and on the dust you may not. This gives a map which is not a genuine sameness, even though it has nothing missing at the front and nothing missing at the back.

The distinction matters, because it makes ordinary algebra impossible. In algebra the whole method is this: given a map, look at what it kills, look at what it misses, and if both are nothing, the map was a sameness. This is how one solves equations, chains up long calculations, and defines almost everything. Here both questions are answered with nothing, so the recipe declares the map a sameness, which is the wrong answer.

The lectures open on exactly this example ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)), and list two more failures of the same kind. That list sits on the first page of the course because the whole course is the repair for it. Rather than patching the recipe, the repair starts from the observation that the dust and the ruler differ in something the points cannot see, and then changes what an object *is*, so that the difference becomes visible.

### The mathematics

Write $\mathbb{R}_{\mathrm{disc}}$ for the dust and $\mathbb{R}$ for the ruler, both taken as topological abelian groups. Sending each number to itself is a continuous homomorphism between them, and in the category of topological abelian groups it has no kernel and no cokernel:

```math
\mathbb{R}_{\mathrm{disc}} \xrightarrow{\;\mathrm{id}\;} \mathbb{R},
\qquad \ker = 0, \qquad \mathrm{coker} = 0,
\qquad \text{yet } \mathbb{R}_{\mathrm{disc}} \not\cong \mathbb{R}.
```

**Reading the symbols.** The subscript "disc" records the choice to forget nearness, so $\mathbb{R}_{\mathrm{disc}}$ and $\mathbb{R}$ hold the same numbers under different rules about which of them count as close. The arrow labelled $\mathrm{id}$ is the map that sends each number to itself. The word $\ker$ names everything the map sends to zero, which is the kill-list, and $\mathrm{coker}$ names what the map fails to reach, which is the miss-list. The last symbol, $\not\cong$, says the two groups are still not the same object.

**Why it matters.** In an abelian category, a map with $\ker = 0$ and $\mathrm{coker} = 0$ is an isomorphism. Here both vanish and the map is not one, so topological abelian groups do not form an abelian category, and the standard machinery of homological algebra cannot be used on them.

**In the simulation.** The slider is how closely you look. The two rows are $\mathbb{R}_{\mathrm{disc}}$ and $\mathbb{R}$, the vertical lines are $\mathrm{id}$ matching them up one to one, and the readout prints $\ker$ and $\mathrm{coker}$ so you can watch both stay empty while the two rows behave differently.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/01.html)** to match the two lines yourself and watch both the kill-list and the miss-list come out empty.

## 2 · Probes that branch

The object that will do the seeing is made by splitting. Start with a single box, split it into two boxes, split each of those into two, and keep splitting forever. At every stage you have a finite list of boxes and a record of which box came from which, so nothing infinite has happened at any single stage, and each stage is a finite picture a child could draw.

![Three probes side by side: the endlessly halving one, the one that is a single approaching sequence, and the one whose boxes split five ways](guide/02-branching-probes/probes.png)

A **probe** is a splitting scheme like this, together with the dust of points you reach by following the splits forever. Three of them carry this whole guide, and the picture shows all three:

The **halving probe** splits every box in two, every time. After ten rounds it has 1024 boxes, and its dust is the classical Cantor set: take a line, remove the middle third, remove the middle third of what is left, and repeat.

The **approaching probe** is thinner. Its dust is a single sequence of points marching towards one limit point, together with that limit point. At stage five it has separated the first five points and is still holding everything beyond them in one box.

The **counting-in-base-p probe** splits every box into p boxes. Its dust is what number theorists call the p-adic integers, and part two of this guide will work inside it.

The lectures call these objects profinite sets, and the word says what they are, namely things made out of finite things ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). Two features of the definition matter later, and both are visible in the picture. The first is that every stage is finite, so nothing at any stage is hard. The second is that the whole probe is nothing but the stages plus the memory of which box sits in which, so a probe carries no extra information brought in from outside. The code in this repository stores probes exactly this way, as a list of finite stages plus the map from each stage to the one before, and the tests check that the halving probe really doubles, that the approaching probe really adds one separated point per stage, and that following the splits down and reading a weight back up is consistent.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/02.html)** to switch between the three probes, set the depth, and click a box to see everything inside it.

## 3 · What a shape says to a probe

Now point a probe at a shape. Pointing a probe at a shape means laying the probe's dust into the shape without tearing it, so that nearby dust lands nearby. If two points of the dust are close, their images have to be close as well, and if a sequence of dust points marches towards a limit, the images must march towards the image of the limit.

![A probe's points being laid into a curve, first a landing that keeps limits and then one that tears, with the verdict shown](guide/03-what-a-shape-says/landing.gif)

The animation lays an approaching probe into a curve twice. The first landing takes the marching points to marching points and the limit point to their limit, and it is accepted. The second sends the limit point somewhere else, which breaks the chain, so it is refused.

The whole subject turns on a change of description: instead of describing a shape by listing its points, you describe it by listing, for every probe, all the ways that probe can land in it. A shape becomes a giant answer sheet, with one entry per probe, and the entry is the collection of legal landings.

An object of that kind, an answer sheet obeying two rules we will meet next section, is called a **condensed set** ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). If the shape you started from carried a notion of adding, so does its answer sheet, and it is then called a condensed group; if it carried multiplication too, a condensed ring ([Example 1.3, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)).

Now return to the two real lines. Point the approaching probe at the ruler and there are enormous numbers of legal landings, since any marching sequence with a limit will do. Point it at the dust and almost all of those landings are refused, because in the dust a sequence marching towards a limit is a sequence of unrelated grains, and the only landings that survive are the ones that are eventually stuck on a single grain. The two answer sheets are therefore different, so the difference that the points could not see is visible to the probes straight away.

The approaching probe alone is already enough to catch this, for a reason worth stating. Any space where you can measure distance is completely determined by which sequences converge in it, so the probe that is one converging sequence can already read the whole of such a space ([Remark 1.6, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). Everything with a distance on it, which is nearly everything anyone draws, is covered by that one probe.

![A set in the plane with a sequence inside it approaching a point outside, so the probe reports that the set is missing a limit](guide/03-what-a-shape-says/sequence_test.png)

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/03.html)** to drag the landing points yourself and watch the verdict flip when the chain snaps.

## 4 · Cut, and glue

An answer sheet cannot be filled in at random. Two rules tie the entries together, and both say something obvious about probes.

**Cut.** If a probe falls into two separate pieces, then landing the whole probe is exactly the same as landing each piece, independently. Nothing connects the pieces, so there is nothing more to say.

![A probe separated into two pieces, with the landings of the pieces recombining into landings of the whole](guide/04-cut-and-glue/cut.png)

**Glue.** Suppose a bigger probe covers a smaller one, and you have a landing of the bigger probe which gives the same answer everywhere the covering doubles back on itself. That landing then came from exactly one landing of the smaller one.

![Two overlapping covering pieces carrying landings that agree on their overlap, merging into a single landing of the whole](guide/04-cut-and-glue/glue.gif)

Of the two rules, the second is the one that constrains an answer sheet most. Under it, an answer sheet cannot hold local information that fails to assemble globally, and cannot assemble the same local information in two different ways. In the lectures these are the two conditions listed directly under the definition ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)); together they are what mathematicians call a sheaf condition. A condensed set is an answer sheet for probes obeying cut and glue, and the definition asks for nothing more.

One honest caution belongs here, because the lectures raise it immediately ([Remark 1.4, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)). There are too many probes to form a list in the usual sense, and a definition quantifying over all of them needs care. The fix is to bound the size of the probes considered, check that nothing depends on where the bound is put, and then let the bound grow. It is bookkeeping rather than mathematics, it occupies an appendix of the lectures, and this guide will not return to it.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/04.html)** to cut a probe, fill in the pieces, and watch the two rules accept or refuse your answers.

## 5 · The quotient with no points

The repair pays off as soon as you return to the map from the dust to the ruler. As answer sheets, these are genuinely different objects, so the map between them is genuinely not a sameness, and algebra is now allowed to ask what the difference is. Subtracting the dust from the ruler leaves a perfectly good condensed group, and this guide calls it **the ghost**.

The ghost has no points. When you ask what a single point can say to it, the entry is empty, so by the old way of counting the ghost is zero. When you ask what the halving probe can say, however, the answer is not empty.

![A staircase-like function being built on the branching probe, level by level, ending as a landing that is continuous but not flat on any box](guide/05-the-ghost/ghost.gif)

The animation builds one entry of the ghost. On the halving probe, choose a value on each box, refine, choose again, and keep the choices consistent. In the limit you get a landing which is perfectly continuous but is not constant on any box, no matter how far you refine. A landing like that is precisely something the ruler can do and the dust cannot, so it is a nonzero entry of the ghost's answer sheet ([Example 1.9, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)).

So the ghost is an object with no points which is not zero, and it is the missing piece that makes the recipe work. The map from the dust to the ruler kills nothing and misses nothing *at the level of points*, and the reason it is still not a sameness is a difference which only shows up on probes, and which the ghost now names.

With that, the statement algebra needs is finally true:

> Condensed groups form a setting where every map has a genuine kill-list and a genuine miss-list, and a map with both of them empty really is a sameness.

That is the opening theorem of the lectures ([Theorem 1.10, page 9](https://arxiv.org/pdf/2605.03658v1#page=9), restated with the size bound fixed as [Theorem 2.2, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)). In the standard vocabulary: condensed abelian groups form an abelian category, and it satisfies the strongest of the usual good behaviour axioms, including some that sheaves almost never satisfy. Topological groups form no such thing, which is where this guide began.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/05.html)** to build a ghost entry yourself and watch the point count stay at zero while the probe entry stays nonzero.

## 6 · Probes that never need folding

Nothing new is needed for this section. It is about which probes are the convenient ones to work with. Suppose one probe covers another, meaning that every box downstairs is hit from upstairs. It is often useful to choose, for each point downstairs, one point upstairs sitting above it, and to make that choice continuously. Call such a choice **a lift**.

![A covering of the approaching probe where the choice of lift must jump at the limit point, so no continuous lift exists](guide/06-unfoldable-probes/folding.gif)

Sometimes lifting is impossible. The animation shows a covering of the approaching probe where the two candidate lifts alternate down the sequence. Follow either one and you are forced to jump at the limit, so no continuous choice exists. The probe has a place where it *folds*, and the fold blocks the lift.

Some probes have no such place. A probe where every covering can be lifted is called **unfoldable** here; the lectures call it extremally disconnected ([Definition 2.4, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)). Probes of this kind exist in quantity. Take any plain set of separate points, and complete it in the one way that keeps every map out of it working: every map from the separate points into a compact shape must still be defined, and defined in only one way, after the completion. That completion is unfoldable ([Example 2.5, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)), and the reason is short: to lift a covering you may choose lifts for the separate points however you like, and the completion's own rule then extends the choice, exactly once. Unfoldable probes are strange to look at, in a way that is worth one picture, because it explains why nobody draws them.

![A sequence inside an unfoldable probe being split apart by a two-colouring, so it cannot settle on any limit](guide/06-unfoldable-probes/no_convergence.png)

In an unfoldable probe, a sequence of points converges only if it is eventually stuck on one point ([Warning 2.6, page 12](https://arxiv.org/pdf/2605.03658v1#page=12)). The picture shows why. Colour the points of the sequence alternately, and in an unfoldable probe that colouring can be extended so the two colours sit in genuinely separated regions. The sequence is torn in half and both halves are infinite, so it cannot be settling anywhere, and any colouring you like does the same thing. No shape anyone normally sketches behaves in this way. The same warning also notes that the product of two infinite unfoldable probes is never unfoldable.

Because coverings of an unfoldable probe always lift, the glue rule of section 4 becomes automatic there, and an answer sheet is determined by its entries on unfoldable probes alone, with only the cut rule to check ([Proposition 2.8, page 12](https://arxiv.org/pdf/2605.03658v1#page=12)), so half the definition no longer has to be checked at all. This is the technical reason the whole theory is so much better behaved than sheaf theories usually are, and it is what the next parts of this guide will lean on constantly.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/06.html)** to try lifting a covering yourself, and see where a foldable probe stops you.

## 7 · Nothing was lost

A repair is only worth having if it keeps what was already good, and this section checks that it does. The worry is reasonable, since answer sheets are stranger and larger than spaces, and swapping every space for its answer sheet might smear distinct spaces together, or might lose track of which maps between spaces were the continuous ones. Neither happens, on a class of spaces broad enough to contain everything anyone draws.

![Nested regions showing which topological spaces sit inside condensed sets, and which condensed sets come from spaces](guide/07-nothing-was-lost/nesting.png)

The picture is read from the inside out. The compact shapes, meaning the ones that are closed, bounded and separated, correspond exactly to the answer sheets that are compact in the matching sense, with nothing on either side left over ([Theorem 2.16, page 17](https://arxiv.org/pdf/2605.03658v1#page=17)). Around them sits a much wider class, containing every space with a distance and every shape built out of cells, and on that class the translation is still faithful: two different spaces give two different answer sheets, and the continuous maps between two spaces are exactly the maps between their answer sheets ([Proposition 1.7, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). Outside that, condensed sets keep going, and the ghost of section 5 sits out there.

![A space being translated into its answer sheet and read back out, returning to the same space](guide/07-nothing-was-lost/roundtrip.gif)

There is a way back, too. From an answer sheet you can recover a space by taking its points and declaring a set closed when every probe says so. On the wide class above, the round trip returns the space you started with, which is what the animation traces.

Two honest limits are worth recording, and the lectures flag both. The translation genuinely fails for spaces where a point need not be closed, and such a space never gives an answer sheet at all ([Warning 2.14, page 16](https://arxiv.org/pdf/2605.03658v1#page=16)). In the other direction, the return trip can merge things, because there are compact shapes which are an increasing union of strictly smaller closed pieces, in a way ordinary topology cannot record but an answer sheet can. The lectures regard that as topology losing information rather than condensed sets gaining it, and note it cannot happen for unions taken one step at a time.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/07.html)** to send a space around the round trip and watch what comes back.

## 8 · Counting holes

The last section of part one checks the other thing that must survive, which is the holes. Counting holes is the oldest way to tell shapes apart: a disc has none, a ring has one, and the count is visible by hand, since you can walk a loop around the ring and count your turns.

![A loop being dragged around a ring while a counter records how many whole turns it has made](guide/08-counting-holes/winding.gif)

The animation is the whole of the first hole-count of a circle. Drag a closed path around and the number of complete turns is a whole number, it cannot change by a little, and it is the only thing about the path that matters. That whole number is the circle's first cohomology, and it is a copy of the integers.

The next step is to stack circles. Two circles at right angles make the surface of a doughnut, and it has two independent loops.

![A rotating three-dimensional view of a doughnut surface carrying its two independent loops](guide/08-counting-holes/torus.gif)

The camera goes round so the surface is genuinely three-dimensional, and the two loops are drawn on it: one going the long way round, one going through the hole. Combine them and you get the doughnut's higher holes. Stack more circles and the counts follow one fixed pattern, worked out in the lectures for any number of circles at once, including infinitely many ([Proposition 3.1, page 20](https://arxiv.org/pdf/2605.03658v1#page=20)).

![Bar charts of the hole counts of a stack of circles, for stacks of one up to six, each row the binomial pattern](guide/08-counting-holes/ranks.png)

The bars are the hole counts by degree, recomputed in this repository. Every row is a row of Pascal's triangle, which is what the lectures' formula says: the holes of a stack of circles are exactly the ways of choosing some of the circles.

Two results then say the translation to answer sheets keeps all of this. First, counting holes inside the world of answer sheets gives the same numbers as counting them the classical way, for every compact shape ([Theorem 3.2, page 21](https://arxiv.org/pdf/2605.03658v1#page=21)). Second, if you count with smooth real-valued measurements instead of whole numbers, every hole count above the zeroth is zero ([Theorem 3.3, page 22](https://arxiv.org/pdf/2605.03658v1#page=22)); real-valued measurements are too flexible to notice a hole, and they simply report the continuous functions on the shape. That second result is one of the most used facts in the subject. It says the real numbers are invisible to this kind of counting, and part two will spend a section on where they went.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/08.html)** to drag a loop around and count turns, then switch to the doughnut and count both.

## Where part one leaves you

Four things have been established, and part two uses all of them. A shape can be described by what it says to probes, and probes are nothing but endlessly refined finite pictures. That description keeps every space anyone draws, and keeps their holes. It also sees differences that points cannot, so subtraction finally works, and objects like the ghost, invisible to points, are legitimate.

What has *not* been done is any analysis. Nothing so far can add up an infinite series, complete anything, or say what an infinite sum of group elements should mean. That is the entire content of part two, and the tool built there, called solidity, is where the subject starts to show what it is good for.

**[Part two: Infinite Sums That Finally Land](../condensed-math02/ARTICLE.md)**

## How this part lines up with the lectures

The lectures are kept in this repository at `docs/condensed-math/paper/lectures-on-condensed-mathematics.pdf` and published at [arXiv:2605.03658](https://arxiv.org/abs/2605.03658). This table points each section at what it retells.

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

The figures and computed claims can be rebuilt from this repository. The commands need Python and a command line, and no mathematics.

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

The categorical statements, that condensed groups form a good setting for algebra and that spaces embed faithfully, are quoted, not computed: no finite program can check a statement about a whole category. `notes/research-content.md` marks every claim in this guide as computed here or quoted, and from where.

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

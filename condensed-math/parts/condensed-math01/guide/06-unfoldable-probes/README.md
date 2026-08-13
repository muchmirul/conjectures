# 6 · Probes that never need folding

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

This section uses only the ideas already introduced and asks which probes are easiest to work with. Suppose one probe maps onto another, so every point downstairs has at least one point above it. Choosing one point above each point downstairs gives a **lift**. For the lift to be useful, that choice must also be continuous.

![A covering of the approaching probe where the choice of lift must jump at the limit point, so no continuous lift exists](folding.gif)

A continuous lift does not always exist. In the animation, the possible choices alternate as points approach the limit. Following either set of choices forces a jump at the end, so no continuous selection can be made. The covering folds over the target in a way that cannot be continuously undone.

A probe is called **unfoldable** in this guide when every covering onto it has a continuous lift. The standard term is *extremally disconnected* ([Definition 2.4, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)). Important examples come from the Stone-Čech compactification of a discrete set. Start with separate points and add exactly the limiting information needed so that every map from those points to a compact space extends uniquely. To lift a cover, choose a point above each original discrete point; the extension property then turns those choices into one continuous lift on the completion ([Example 2.5, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)).

![A sequence inside an unfoldable probe being split apart by a two-colouring, so it cannot settle on any limit](no_convergence.png)

Unfoldable probes behave very differently from familiar geometric spaces. Any convergent sequence in one must eventually be constant ([Warning 2.6, page 12](https://arxiv.org/pdf/2605.03658v1#page=12)). To see the obstruction, colour alternating terms of a nonconstant sequence with two colours. In an unfoldable probe, that colouring extends to two separated regions, leaving infinitely many terms on each side. Such a sequence cannot converge. The same warning notes another unusual fact: the product of two infinite unfoldable probes is never unfoldable.

Their usefulness comes from the glue rule. Since every cover of an unfoldable probe admits a lift, compatible data over the cover descend automatically. An answer sheet is therefore determined by its values on unfoldable probes, and only the cut rule remains to be checked there ([Proposition 2.8, page 12](https://arxiv.org/pdf/2605.03658v1#page=12)). This simpler description is one reason condensed groups have unusually strong algebraic properties, and the next two parts will repeatedly use these probes as convenient building blocks.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/06.html)** to attempt a lift and identify the discontinuity that prevents one from existing.

---

[← The quotient with no points](../05-the-ghost/README.md)  ·  [Nothing was lost →](../07-nothing-was-lost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

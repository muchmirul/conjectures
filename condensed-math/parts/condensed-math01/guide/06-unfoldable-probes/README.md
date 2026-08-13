# 6 · Probes that never need folding

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Nothing new is needed for this section. It is about which probes are the convenient ones to work with. Suppose one probe covers another, meaning that every box downstairs is hit from upstairs. It is often useful to choose, for each point downstairs, one point upstairs sitting above it, and to make that choice continuously. Call such a choice **a lift**.

![A covering of the approaching probe where the choice of lift must jump at the limit point, so no continuous lift exists](folding.gif)

Sometimes lifting is impossible. The animation shows a covering of the approaching probe where the two candidate lifts alternate down the sequence. Follow either one and you are forced to jump at the limit, so no continuous choice exists. The probe has a place where it *folds*, and the fold blocks the lift.

Some probes have no such place. A probe where every covering can be lifted is called **unfoldable** here; the lectures call it extremally disconnected ([Definition 2.4, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)). Probes of this kind exist in quantity. Take any plain set of separate points, and complete it in the one way that keeps every map out of it working: every map from the separate points into a compact shape must still be defined, and defined in only one way, after the completion. That completion is unfoldable ([Example 2.5, page 11](https://arxiv.org/pdf/2605.03658v1#page=11)), and the reason is short: to lift a covering you may choose lifts for the separate points however you like, and the completion's own rule then extends the choice, exactly once. Unfoldable probes are strange to look at, in a way that is worth one picture, because it explains why nobody draws them.

![A sequence inside an unfoldable probe being split apart by a two-colouring, so it cannot settle on any limit](no_convergence.png)

In an unfoldable probe, a sequence of points converges only if it is eventually stuck on one point ([Warning 2.6, page 12](https://arxiv.org/pdf/2605.03658v1#page=12)). The picture shows why. Colour the points of the sequence alternately, and in an unfoldable probe that colouring can be extended so the two colours sit in genuinely separated regions. The sequence is torn in half and both halves are infinite, so it cannot be settling anywhere, and any colouring you like does the same thing. No shape anyone normally sketches behaves in this way. The same warning also notes that the product of two infinite unfoldable probes is never unfoldable.

Because coverings of an unfoldable probe always lift, the glue rule of section 4 becomes automatic there, and an answer sheet is determined by its entries on unfoldable probes alone, with only the cut rule to check ([Proposition 2.8, page 12](https://arxiv.org/pdf/2605.03658v1#page=12)), so half the definition no longer has to be checked at all. This is the technical reason the whole theory is so much better behaved than sheaf theories usually are, and it is what the next parts of this guide will lean on constantly.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/06.html)** to try lifting a covering yourself, and see where a foldable probe stops you.

---

[← The quotient with no points](../05-the-ghost/README.md)  ·  [Nothing was lost →](../07-nothing-was-lost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

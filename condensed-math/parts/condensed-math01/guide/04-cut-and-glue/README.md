# 4 · Cut, and glue

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The entries of an answer sheet cannot be chosen independently. They must respect two basic ways of relating probes, called **cut** and **glue**. Together, these are the sheaf conditions in the definition of a condensed set.

**Cut.** If a probe is a disjoint union of two pieces, then a landing of the whole probe contains exactly the same information as one landing for each piece. Since the pieces do not meet, the two landings can be chosen independently and then combined.

![A probe separated into two pieces, with the landings of the pieces recombining into landings of the whole](cut.png)

**Glue.** Suppose a larger probe covers a smaller probe. A landing on the covering probe descends to the smaller one when it assigns the same result wherever the cover represents the same point more than once. If that agreement holds, there must be one and only one landing downstairs that produces the given landing upstairs.

![Two overlapping covering pieces carrying landings that agree on their overlap, merging into a single landing of the whole](glue.gif)

The glue rule prevents two kinds of failure. Compatible local answers must assemble into a global answer, so information cannot agree everywhere locally but fail to exist globally. The global answer must also be unique, so the same local data cannot produce two different results. The lectures place these two requirements directly after the definition ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). Thus, a condensed set is precisely an answer sheet on profinite probes that respects disjoint pieces and compatible covers.

A size issue also appears in the definition, and the lectures address it immediately ([Remark 1.4, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)). There are too many profinite sets to collect into one ordinary set, so the phrase "every probe" must be handled carefully. One first chooses a sufficiently large size bound, develops the theory within that bound, and proves that enlarging it does not change the resulting mathematics. This guide will treat that step as background bookkeeping.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/04.html)** to assign local answers and see how the cut and glue rules decide whether they form one valid answer.

---

[← What a shape says to a probe](../03-what-a-shape-says/README.md)  ·  [The quotient with no points →](../05-the-ghost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

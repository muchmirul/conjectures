# 4 · Cut, and glue

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

An answer sheet cannot be filled in at random. Two rules tie the entries together, and both say something obvious about probes.

**Cut.** If a probe falls into two separate pieces, then landing the whole probe is exactly the same as landing each piece, independently. Nothing connects the pieces, so there is nothing more to say.

![A probe separated into two pieces, with the landings of the pieces recombining into landings of the whole](cut.png)

**Glue.** Suppose a bigger probe covers a smaller one, and you have a landing of the bigger probe which gives the same answer everywhere the covering doubles back on itself. That landing then came from exactly one landing of the smaller one.

![Two overlapping covering pieces carrying landings that agree on their overlap, merging into a single landing of the whole](glue.gif)

Of the two rules, the second is the one that constrains an answer sheet most. Under it, an answer sheet cannot hold local information that fails to assemble globally, and cannot assemble the same local information in two different ways. In the lectures these are the two conditions listed directly under the definition ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)); together they are what mathematicians call a sheaf condition. A condensed set is an answer sheet for probes obeying cut and glue, and the definition asks for nothing more.

One honest caution belongs here, because the lectures raise it immediately ([Remark 1.4, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)). There are too many probes to form a list in the usual sense, and a definition quantifying over all of them needs care. The fix is to bound the size of the probes considered, check that nothing depends on where the bound is put, and then let the bound grow. It is bookkeeping rather than mathematics, it occupies an appendix of the lectures, and this guide will not return to it.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/04.html)** to cut a probe, fill in the pieces, and watch the two rules accept or refuse your answers.

---

[← What a shape says to a probe](../03-what-a-shape-says/README.md)  ·  [The quotient with no points →](../05-the-ghost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

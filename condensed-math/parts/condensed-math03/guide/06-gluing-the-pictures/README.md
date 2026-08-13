# 6 · Gluing the local pictures

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

So far the spaces have been affine: one ring, one coordinate patch. Real geometry is patches glued together, so the machinery has to survive gluing.

The patches used here are slightly richer than a plain ring. Along with the ring of functions you carry a chosen subring: the functions you have decided to call **size at most one**. The pair determines a space of valuations, meaning a space whose points are the consistent ways of measuring how big each function is ([Proposition 9.2, page 63](https://arxiv.org/pdf/2605.03658v1#page=63)).

![A ring's valuation space, with the region cut out by choosing which functions count as size at most one](spa.png)

The picture shows the effect of the choice. Every choice of subring cuts out a region of the valuation space, and the lectures prove the correspondence runs exactly both ways: the subring determines the region and the region determines the subring, with nothing lost either way. Choosing a subring is choosing how much of the space you are looking at.

![Two overlapping patches carrying their own module theories, agreeing on the overlap and merging into one theory on the union](gluing.gif)

Then the gluing theorem ([Theorem 9.8, page 65](https://arxiv.org/pdf/2605.03658v1#page=65)): the assignment sending each patch to its theory of modules is a sheaf, so local theories that agree on overlaps determine exactly one theory on the union. That is what licenses everything global.

Two honest notes.

Gluing derived categories in the old-fashioned sense does not work: one has to track homotopies between homotopies, without end, and the classical derived category has thrown that information away. The lectures pass to the higher-categorical version at precisely this point and say so plainly. The statement is unchanged; the technology underneath it is not.

And the proof is the same proof as classical Zariski descent: cover the space by the places where one function is invertible, and check exactness there, where the cover splits. Nothing exotic enters. The whole of Lecture X is spent making the two supporting lemmas, that localisations commute and that a module which is locally zero is zero, hold in this setting.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/06.html)** to choose which functions count as small and watch the region move.

---

[← Cohomology with compact support](../05-compact-support/README.md)  ·  [The six operations →](../07-six-operations/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

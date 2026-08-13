# 3 · What a shape says to a probe

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Now point a probe at a shape. Pointing a probe at a shape means laying the probe's dust into the shape without tearing it, so that nearby dust lands nearby. If two points of the dust are close, their images have to be close as well, and if a sequence of dust points marches towards a limit, the images must march towards the image of the limit.

![A probe's points being laid into a curve, first a landing that keeps limits and then one that tears, with the verdict shown](landing.gif)

The animation lays an approaching probe into a curve twice. The first landing takes the marching points to marching points and the limit point to their limit, and it is accepted. The second sends the limit point somewhere else, which breaks the chain, so it is refused.

The whole subject turns on a change of description: instead of describing a shape by listing its points, you describe it by listing, for every probe, all the ways that probe can land in it. A shape becomes a giant answer sheet, with one entry per probe, and the entry is the collection of legal landings.

An object of that kind, an answer sheet obeying two rules we will meet next section, is called a **condensed set** ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). If the shape you started from carried a notion of adding, so does its answer sheet, and it is then called a condensed group; if it carried multiplication too, a condensed ring ([Example 1.3, page 7](https://arxiv.org/pdf/2605.03658v1#page=7)).

Now return to the two real lines. Point the approaching probe at the ruler and there are enormous numbers of legal landings, since any marching sequence with a limit will do. Point it at the dust and almost all of those landings are refused, because in the dust a sequence marching towards a limit is a sequence of unrelated grains, and the only landings that survive are the ones that are eventually stuck on a single grain. The two answer sheets are therefore different, so the difference that the points could not see is visible to the probes straight away.

The approaching probe alone is already enough to catch this, for a reason worth stating. Any space where you can measure distance is completely determined by which sequences converge in it, so the probe that is one converging sequence can already read the whole of such a space ([Remark 1.6, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). Everything with a distance on it, which is nearly everything anyone draws, is covered by that one probe.

![A set in the plane with a sequence inside it approaching a point outside, so the probe reports that the set is missing a limit](sequence_test.png)

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/03.html)** to drag the landing points yourself and watch the verdict flip when the chain snaps.

---

[← Probes that branch](../02-branching-probes/README.md)  ·  [Cut, and glue →](../04-cut-and-glue/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

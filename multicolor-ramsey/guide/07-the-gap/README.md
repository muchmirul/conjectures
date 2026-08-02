# 7 · The gap

Put the two guardrails on one chart and the problem stares back.

![The exponential floor and the factorial ceiling, with the widening unknown band shaded](gap.png)

The floor in the chart is what multiplying the record tables honestly proves at each color count. It grows like a fixed number raised to the color count. The ceiling grows like the factorial of the color count, which is what you get when the multiplying factor itself keeps growing. These are different kinds of growth, and the band between them widens without end. Fifty years of work lived inside that band, moving the floor's fixed rate from 2.24 toward 3.28 without ever changing its character.

Shortcuts were tried. Here is the most tempting one, sunk by a computation you can watch.

There are lots of orderings of a handful of items, factorially many, and any two orderings first disagree at some position. Color each pair of orderings by that position. Factorially many tables from a handful of colors would smash the question. With three items there are six orderings and only two possible colors, and if the trick worked it would beat the pentagon.

![Six orderings colored by first disagreement, with a one-color triangle found and flashed](orderings.gif)

It does not work. The orderings ABC, BAC and CAB pairwise first-disagree at the very same position, the first letter, so their triangle is one-colored. Nothing about three items is special; the same collision happens at every size, and the tests exhibit it. Patching the color to record more information avoids the collision only by spending far more colors, which puts you back where you started.

Other routes fail for their own reasons. Building tables from addition on a number circle turns out to be the same problem wearing different clothes, not an easier one. What every failure has in common is this: each color's net must stay triangle-free, and the cheap ways to guarantee that all quarantine every color inside its own private region. The winning idea has to let many rooms *reuse* the same color, while some global mechanism guarantees the reused pieces can never assemble a triangle. Finding that mechanism took until 2026, and it is the next three chapters.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/07.html)** and turn the idea over yourself.

---

[← The ceiling](../06-the-ceiling/README.md)  ·  [Palettes →](../08-palettes/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

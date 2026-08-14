# Start here

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

*Part one of three on condensed mathematics. We begin with a familiar problem: the same set of numbers can carry different ideas of nearness, but ordinary algebra does not record that difference well. Step by step, this part introduces probes, explains how a space answers them, and shows how this new description makes subtraction work without losing familiar spaces or their holes. No previous mathematics is assumed.*

![A tree adds one level of branches at a time as the intervals below become smaller and more numerous](hero.gif)

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

---

[Two real lines →](../01-two-real-lines/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

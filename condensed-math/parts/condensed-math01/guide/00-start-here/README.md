# Start here

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

*Part one of three on condensed mathematics. A set with a distance on it carries two structures that do not fit together properly, and the mismatch breaks ordinary algebra. This part builds the repair from the beginning: what a probe is, what a shape says to one, and why describing a shape that way makes subtraction work again. You do not need a maths background, and every idea arrives as a picture you can move.*

![A branching probe growing level by level while the boxes it cuts a line into get finer and finer](hero.gif)

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

---

[Two real lines →](../01-two-real-lines/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

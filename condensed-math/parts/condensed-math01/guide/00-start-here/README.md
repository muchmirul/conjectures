# Start here

*Part 1 of three: Understanding Spaces Through Probes. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

*This is the first of three parts on condensed mathematics. We begin with a simple problem: the same set of numbers can have different rules for which numbers are close. Ordinary algebra does not handle that difference well. We will build a new description of a space, one step at a time, and use it to repair the problem. You do not need any previous mathematics.*

![A branching tree gains one finite level at a time, while the intervals below it become smaller](hero.gif)

The animation shows the basic object used in this guide. Start with one box. Divide it into smaller boxes, then divide those boxes again. Each stage has only finitely many boxes, so we can view and study it completely. If the process continues without end, a path through all the stages picks out a point. The whole branching pattern also records how the points are separated from one another.

We will call this object a **probe**. Its standard name is a *profinite set*. Instead of describing a space only by listing its points, condensed mathematics records every continuous way that every probe can map into the space. This extra information remembers which families of points are close.

This part covers Lectures I to III of Peter Scholze's *Lectures on Condensed Mathematics* ([arXiv:2605.03658](https://arxiv.org/abs/2605.03658), May 2026). The lectures describe joint work with Dustin Clausen from a course taught in Bonn in 2019. Part two introduces infinite sums, and part three adds rings and geometry. You can find the text, figures, and code in the [open source repository](https://github.com/muchmirul/conjectures). Each chapter also has an activity in which changing a control updates the picture. You can open the [full list of part-one activities](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/index.html) at any time.

```
    first see the problem       1  the same numbers with different notions of closeness
    build the new description  2  finite stages that form a probe
                               3  continuous maps from a probe into a space
                               4  the cut and glue rules
    use the description         5  a quotient that points cannot detect
                               6  probes on which every cover splits
    compare with topology       7  recovering familiar spaces
                               8  keeping track of holes
```

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/00.html)** by adding one stage at a time and seeing how the finite stages fit together.

---

[The same numbers, but different ideas of closeness →](../01-two-real-lines/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

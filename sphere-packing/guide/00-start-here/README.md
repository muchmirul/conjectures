# Start here

*A step-by-step visual guide to packing equal balls, a question first asked in 1611, and to a major result proved in 2026. You do not need a maths background. Each new idea begins with a picture.*

![Equal balls in a tightly packed fruit-shop stack, rotating so you can see its depth](hero.gif)

Every ball in this stack is the same size, and none of them overlap. This familiar fruit-shop arrangement fills a little under 75 percent of the surrounding space. The remaining space is made of gaps between the balls. Everything in this guide comes from the open source repository at [github.com/muchmirul/conjectures](https://github.com/muchmirul/conjectures): the text, every figure, and the tests behind each number.

For circles on a flat surface, the best arrangement is known. For balls in ordinary three-dimensional space, finding the answer took almost four hundred years. In most higher dimensions, the exact answer is still unknown and is expected to remain difficult. Researchers therefore also ask a more manageable question: how dense could any packing possibly be? In 2026, they found the exact long-term limit of the main method used to answer that question. The result improved a general limit that had stood since 1978.

This guide develops that story one small step at a time. Most numbered sections also have a [page you can play with](https://muchmirul.github.io/conjectures/sphere-packing/play/index.html), where you can change the main quantities and watch the picture respond.

The 2026 result is presented in two documents. The first gives the finished proof. The second is a behind-the-scenes guide that explains how the main ideas were found, including earlier attempts that did not work. Sections 8 to 11 explain the finished proof. The other sections provide the surrounding story. A table near the end shows where each idea appears in the two source documents.

The code that makes each figure is included in this repository. The tests recalculate the numbers used in the guide. When a statement comes from an existing theorem rather than from those calculations, the text says so.

```
    first, the problem       1  what are we trying to find?
                             2  why balls lose space
                             3  why examples are not enough
    next, the method         4  one useful function
                             5  one total counted two ways
                             6  what the method can show
                             7  can the method be improved forever?
    finally, the 2026 proof  8  balancing the two views
                             9  the limit no function can cross
                            10  building a function that reaches it
                            11  why the two parts give an exact answer
                            12  what is settled and what remains open
```

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/00.html)** to rotate the opening stack and see why its depth matters.

---

[The question →](../01-the-question/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

# 2 · Probes that branch

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

To detect nearness, we need an object that carries nearness of its own. Build one by starting with a box and repeatedly dividing it into smaller boxes. At each stage there are only finitely many pieces, together with a map telling us which new piece came from which old one. The infinite object is completely described by these finite stages and their connecting maps.

![Three probes side by side: the endlessly halving one, the one that is a single approaching sequence, and the one whose boxes split five ways](probes.png)

A **probe** consists of such a compatible sequence of finite divisions and the points obtained by following branches through every stage. The lectures call this a profinite set. Three examples will be used repeatedly in this guide.

The **halving probe** divides every box into two at each stage. After ten rounds it has 1024 boxes. Its limiting points form the classical Cantor set, which can also be made by repeatedly removing the middle third of every remaining interval.

The **approaching probe** records one convergent sequence and its limit. At stage five, the first five points have been separated into their own boxes, while all later points and the limit still occupy one final box. Further stages separate one more point at a time.

The **counting-in-base-p probe** divides each box into p pieces. Its limiting points form the p-adic integers, an important number system in which divisibility by powers of p determines nearness. Part two will use this probe to explain an infinite sum that converges in one notion of size but not another.

The formal name *profinite set* means an inverse limit of finite sets ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). Two parts of that description are important. Every individual stage is finite, and all information about the probe lies in the stages and the maps between them. The code follows this definition literally by storing finite sets and their transition maps. Its tests check the expected growth of all three probes and verify that compatible data can be read consistently through their levels.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/02.html)** to compare the three probes, change their depth, and inspect the points contained in any box.

---

[← Two real lines](../01-two-real-lines/README.md)  ·  [What a shape says to a probe →](../03-what-a-shape-says/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

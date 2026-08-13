# 4 · Functions near the edge

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Geometry starts here, with a question about edges. Take the simplest space with an edge, an endless line, with coordinates running out forever in one direction. The polynomials are the functions defined on all of it. The question is what functions look like far out, near the edge, ignoring everything in the middle.

![The camera pulling back along an endless line towards its far edge, with a function's expansion in the reciprocal coordinate assembling term by term](tail.gif)

Far out, the coordinate is huge, so its reciprocal is tiny, and the natural thing to expand in is that reciprocal. A function near the edge is a series in one-over-the-coordinate, allowed finitely many positive powers and endlessly many negative ones. Call this the **edge ring**. The lectures write it as the formal Laurent series in the inverse coordinate and it is the central object of Lecture VIII.

Two features matter here. Every polynomial is also a function near the edge, by just reading it out there, so the polynomials sit inside the edge ring. The edge ring is also much bigger, because of all the endless negative tails.

The quotient, functions near the edge modulo functions everywhere, is the object that does the work. Its elements are exactly the endless tails, with the polynomial part discarded as irrelevant.

![The coordinate cross, two lines meeting at a point, with an edge at each of its four ends](cross.png)

The picture shows the example the lectures compute in full ([Remark 8.5, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)): the coordinate cross, two lines glued at a single point. It has an edge at each end, each end contributes its own tails, and the shared point ties the two branches together in exactly one place. This repository computes the quotient's size for that shape by truncation, and the count comes out as the tails from each branch plus a single extra piece left over from the shared point, which is where the crossing enters the count. The next section says why any of this is worth doing.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/04.html)** to slide out to the edge and watch which terms of a function survive.

---

[← The real line's own rule](../03-the-real-lines-own-rule/README.md)  ·  [Cohomology with compact support →](../05-compact-support/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

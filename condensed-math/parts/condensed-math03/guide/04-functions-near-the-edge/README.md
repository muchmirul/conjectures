# 4 · Functions near the edge

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We now turn from analysis to geometry. Begin with the affine line, whose global functions are polynomials in one coordinate. To study what happens far from its finite part, introduce the reciprocal coordinate. When the original coordinate is large, its reciprocal is small, so series in the reciprocal describe functions in a formal neighbourhood of infinity.

![The camera pulling back along an endless line towards its far edge, with a function's expansion in the reciprocal coordinate assembling term by term](tail.gif)

Such a series may contain finitely many positive powers of the original coordinate and infinitely many negative powers. The lectures call the resulting ring of formal Laurent series the functions near the boundary. This guide calls it the **edge ring**. The animation moves toward the boundary while assembling the terms that remain meaningful there.

Every polynomial has an expansion near infinity, so the polynomial ring maps into the edge ring. The edge ring also contains infinite negative-power tails that no polynomial can have. Comparing the two rings separates information defined everywhere from information that exists only near the boundary.

The quotient of the edge ring by the polynomial ring discards every global polynomial contribution. What remains consists of the boundary tails. This quotient is the concrete object used in the next section to build compactly supported cohomology.

![The coordinate cross, two lines meeting at a point, with an edge at each of its four ends](cross.png)

The lectures work out the coordinate cross, defined by two coordinate axes meeting at one point ([Remark 8.5, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)). Each branch contributes its own Laurent tails, while the shared value at the crossing imposes one relation between the global functions. The finite truncation in this repository counts the quotient as the tails from both branches plus one additional piece associated with that shared point. The count stabilizes as the truncation is extended.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/04.html)** to move toward the boundary and see which polynomial and tail terms survive in the quotient.

---

[← The real line's own rule](../03-the-real-lines-own-rule/README.md)  ·  [Cohomology with compact support →](../05-compact-support/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

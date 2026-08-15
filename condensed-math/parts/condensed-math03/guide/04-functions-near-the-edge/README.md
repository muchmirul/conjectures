# 4 · Global functions and boundary tails

*Part 3 of three: Measure Rules for Rings and Geometry. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We now move from analysis to geometry. Begin with the affine line, whose global functions are polynomials in one coordinate $T$. To describe behavior near infinity, use the reciprocal coordinate $T^{-1}$. When $T$ becomes large, $T^{-1}$ becomes small, so series in $T^{-1}$ describe a formal neighborhood of the boundary.

![As a point moves toward infinity, bars compare powers of the coordinate with powers of its reciprocal](tail.gif)

A formal Laurent series near infinity can have finitely many positive powers of $T$ and infinitely many negative powers. We will call this the **boundary ring**. Every polynomial has an expansion in this ring, but the boundary ring also contains infinite negative-power tails that no polynomial can contain.

Taking the quotient of the boundary ring by the polynomial ring removes all functions already defined globally. What remains records information that exists only near the boundary. This quotient becomes the basic ingredient for compactly supported cohomology in the next chapter.

![Two coordinate axes meet at one point and create four directions toward the boundary](cross.png)

The lectures also calculate the coordinate cross, which consists of two axes meeting at the origin ([Remark 8.5, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)). Each axis contributes its own Laurent tail. The two global polynomial descriptions must agree at the shared point. In the finite truncation used here, the quotient contains the tails from both branches plus one extra contribution from that shared relation. The count remains stable when the truncation is extended.

### The mathematics

The affine line has global polynomial functions and formal functions near infinity. With coordinate $T$, Lecture VIII writes these rings as

```math
A=\mathbb Z[T],
\qquad
A_\infty=\mathbb Z((T^{-1})),
\qquad
A_\infty/A=\mathbb Z((T^{-1}))/\mathbb Z[T].
```

The coordinate cross needs one copy of the boundary ring for each branch. [Remark 8.5, page 54 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=54) gives

```math
A=\mathbb Z[X,Y]/(XY),
\qquad
A_\infty=\mathbb Z((X^{-1}))\times\mathbb Z((Y^{-1})),
```

```math
A_\infty/A=
\frac{\mathbb Z((X^{-1}))\times\mathbb Z((Y^{-1}))}
{\mathbb Z[X,Y]/(XY)}.
```

**Reading the symbols.** The ring $A=\mathbb Z[T]$ contains polynomials in $T$ with integer coefficients. The double parentheses in $\mathbb Z((T^{-1}))$ mean formal Laurent series in the inverse coordinate. These series may have infinitely many negative powers of $T$ but only finitely many positive powers. The subscript $\infty$ marks functions near the boundary. The quotient $A_\infty/A$ identifies two boundary series when they differ by a global polynomial. For the cross, $X$ and $Y$ are its two coordinates. The relation $XY=0$ restricts points to one axis or the other. The product $\times$ keeps one Laurent series for each branch.

**Why it matters.** The quotient removes every function that already extends over the whole affine space. It keeps only boundary information. On the cross, the relation at the shared origin links the two branches and creates the additional contribution seen in the finite model.

**In the simulation.** Moving toward the boundary increases $T$ and decreases $T^{-1}$. Polynomial terms belong to $A$ and disappear in the quotient. Negative-power tails remain in $A_\infty/A$.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/04.html)** to separate global polynomial terms from terms that remain only near infinity.

---

[← A measure rule for the real numbers](../03-the-real-lines-own-rule/README.md)  ·  [Compactly supported cohomology →](../05-compact-support/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

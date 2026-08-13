# 6 · Where the real line goes

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Solidifying the real numbers gives zero, meaning the whole group disappears rather than shrinking to something small. That result is a precise statement in the lectures ([Corollary 6.1 (iii), page 42](https://arxiv.org/pdf/2605.03658v1#page=42)), not a defect being confessed, and the reason for it is visible in one picture.

![A real number being halved, thirded, and divided by every whole number in turn, always landing on another real number, while a whole number falls off its lattice immediately](divisible.gif)

Every real number can be divided by two, and by three, and by every whole number, and the answer is again a real number. The animation shows a real number surviving division forever while a whole number falls off the lattice at the first step. A group where every element can always be divided like this is called divisible.

Section 5 said the building blocks of solid groups are rows of dials, and each dial holds a whole number, so consider what a divisible group can send into a single dial. Whatever a real number is sent to must itself be divisible by two, and by three, and by everything, because the sending respects division. The only whole number divisible by everything is zero, so every dial receives zero, and the whole row receives zero.

![Every homomorphism from the real line into a row of dials collapsing to zero, because the image would have to be divisible](no_map.png)

That settles the building blocks, and it is as far as this argument reaches on its own, since it shows only that the real line sends nothing but zero into any of the pieces solid groups are assembled from. Going from there to the full statement, that the solidification is zero and not merely small, is the lectures' step and it needs one more input, the computation of Lecture IV ([Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25)). With that in hand the conclusion is exactly what the picture suggests: the real numbers solidify to nothing.

Two things must be said plainly here, because this is where a reader is most likely to conclude the theory is broken:

**The theory is not claiming the real numbers are unimportant.** It is saying that this particular notion of completion is a nonarchimedean one, tuned to sizes like the base-p size of section 1, where near means divisible by a high power. The real line's notion of near is a different kind, and it needs a different completion. The lectures flag this in a footnote at the very moment solidity is defined ([page 33](https://arxiv.org/pdf/2605.03658v1#page=33)), and part three of this guide builds the real version.

**The collapse is useful, not merely tolerated.** Because real-valued measurements vanish, they cannot obstruct anything, and calculations that would otherwise carry an unbounded real-valued correction term simply lose it. Section 8 of part one already met this, where real-valued hole counting returns nothing above the zeroth. That vanishing is what makes the key computation of Lecture IV go through ([Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25)), and that computation is what everything in this part rests on.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/06.html)** to divide numbers repeatedly and watch which groups survive it.

---

[← The solid rule](../05-the-solid-rule/README.md)  ·  [The multiplication table →](../07-the-multiplication-table/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

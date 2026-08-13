# 3 · Every function is a stack of steps

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

We first examine continuous functions from a probe to the integers. Since distinct integers are separated from one another, continuity prevents such a function from changing indefinitely inside smaller and smaller nearby regions. On a compact probe, it becomes constant on every box of some finite stage. The function can therefore be read as a finite list of integer values.

![A whole-number measurement on the branching probe being taken apart into step functions, one basis element at a time](steps.gif)

At one finite stage, the basic step functions are easy to see. For each box, use the function that equals one on that box and zero elsewhere. Multiplying these indicators by integers and adding them reconstructs any function on the stage. The animation performs this reconstruction one basis element at a time, without introducing fractions.

The deeper statement concerns all stages at once. Under addition, the continuous integer-valued functions on a probe form an abelian group. Nöbeling's theorem says that this group is free: there is a collection of basis functions such that every continuous integer-valued function has one unique expression as a finite integer combination of them. Freeness is special because a general abelian group need not have any basis of this kind.

![The number of basis elements produced by the construction, level by level, matching the number of boxes at that level](basis_size.png)

The theorem is due to Nöbeling, extending work of Specker, and the lectures present Bergman's proof ([Theorem 5.4, page 34](https://arxiv.org/pdf/2605.03658v1#page=34)). The implementation in this repository follows the finite stages of that construction. It orders products of indicator functions, retains a function when earlier choices do not already generate it, and checks that the retained functions form a basis. The chart confirms that the basis size matches the number of boxes at each tested stage.

This finite calculation does not prove Nöbeling's theorem. At a fixed finite stage, the group is automatically free, while the theorem's real content is that a compatible basis exists for the full infinite object. The repository therefore labels its calculation as a finite shadow and quotes the infinite theorem from the lectures.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/03.html)** to choose an integer-valued function and watch the basis functions rebuild it.

---

[← Weights that agree](../02-weights-that-agree/README.md)  ·  [Products in, sums out →](../04-products-in-sums-out/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

# 5 · The solid rule

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Everything is now in place to state the rule this part is named for. Nothing new is needed, only the weightings from section 2.

A group is **solid** when weightings can be summed against it, and can be summed in exactly one way. More precisely, take any probe, and any way of placing the probe's points into the group. Then there must be exactly one way to extend that placement so that weightings can be integrated against it, agreeing with the placement on single points.

![A placement of a probe's points into a group, and the unique extension that lets weightings be integrated against it](extension.gif)

The animation shows what "exactly one way" gives you. Once the extension exists, every weighting has a value, so every infinite sum the probe describes has an answer, and there is no ambiguity about which answer. Existence gives you the sums, and uniqueness stops you inventing two different theories of the same sum.

The lectures state the rule in one line ([Definition 5.1, page 33](https://arxiv.org/pdf/2605.03658v1#page=33)) and spend a lecture and a half establishing that it behaves. What comes out is a full toolkit, and this is the central result of this part:

> The solid groups form a self-contained setting for algebra, closed under everything one wants to do. Its building blocks are exactly the endless products of copies of the whole numbers. Any group at all can be pushed into a solid one, in a best-possible way, and pushing is compatible with everything else.

That is Theorem 5.8 ([page 35](https://arxiv.org/pdf/2605.03658v1#page=35)) together with Corollary 6.1 ([page 42](https://arxiv.org/pdf/2605.03658v1#page=42)). The operation of pushing a group into a solid one is called solidification here; the lectures write it with a small square.

![Which of the sample groups obey the solid rule and which do not, each with the reason](solid_or_not.png)

The picture sorts the guide's stock examples. The whole numbers are solid, and so is any endless product of copies of them, which by the previous section means every collection of weightings. The base-p numbers are solid, which keeps the promise of section 1. Power series in a variable are solid. The real numbers are not, and the next section is about what happens to them.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/05.html)** to test candidate groups against the rule and see each verdict's reason.

---

[← Products in, sums out](../04-products-in-sums-out/README.md)  ·  [Where the real line goes →](../06-where-the-real-line-goes/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

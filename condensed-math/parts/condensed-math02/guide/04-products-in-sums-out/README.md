# 4 · Products in, sums out

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Now the shape of a weighting becomes visible, and it is startling.

Two different ways of having infinitely many whole numbers at once:

A **product** is an endless row of dials, each set independently, with no restriction at all. Every dial may be nonzero, forever.

A **sum** is the same endless row, but with a rule: only finitely many dials may be off zero. Everything past some point must be blank.

![An endless row of dials with every dial set, beside the same row where all but a few dials are blank](product_sum.png)

These are wildly different objects. Now the striking part: they are each other's mirror image, and the mirror is the operation of asking for a number.

Ask an endless product for a single whole number, in a way that respects addition. You might expect that such a question could sample all the dials at once, weighting them somehow. It cannot. Any such question reads only finitely many dials and ignores the rest.

![A reader scanning along an endless row of dials and coming to a halt after finitely many, because no legal question can reach further](finite_reach.gif)

That is Specker's theorem from 1950, and the lectures use it constantly. The shape of the reason is worth a sentence, because it is the shape of section 6 below as well: a legal question is destroyed by divisibility. Settings that live only in the far tail of the row can be made divisible by as high a power of a number as you like, so the answer they force would have to be divisible by every such power, and the only whole number like that is zero. Making that precise is more work than one sentence, and this guide leaves it to the sources.

Ask an endless sum for a number, and the opposite happens: you may choose an answer for every dial independently, since only finitely many are ever on, so nothing diverges. The questions on a sum form a product.

Put these together with the previous section and the shape of a weighting falls out. The measurements on a probe form a free group, so they are a sum of copies of the whole numbers. The weightings are exactly the questions one can ask of the measurements. Therefore:

> Every collection of weightings on a probe is an endless product of copies of the whole numbers.

That is the lectures' Corollary 5.5 ([page 34](https://arxiv.org/pdf/2605.03658v1#page=34)). It is worth pausing on how blunt it is. Whatever probe you started with, however intricately it branched, the weightings on it are just a row of dials. All the structure has been pushed into how many dials there are.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/04.html)** to set dials in a product and a sum, and try to build a question that reaches past the end.

---

[← Every function is a stack of steps](../03-stacks-of-steps/README.md)  ·  [The solid rule →](../05-the-solid-rule/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

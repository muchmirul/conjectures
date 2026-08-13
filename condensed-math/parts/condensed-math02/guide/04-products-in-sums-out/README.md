# 4 · Products in, sums out

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

With the previous section in hand, the shape of a weighting becomes visible, and it comes out of comparing two different ways of having infinitely many whole numbers at once. A **product** is an endless row of dials, each set independently, with no restriction at all, so a dial may hold a number other than zero however far along the row you look. A **sum** is the same endless row with one restriction added, that only finitely many dials may be off zero, so every dial past some point is blank. The difference between the two matters because they behave in opposite ways when you ask them for a number, and that is what the rest of this section works out.

![An endless row of dials with every dial set, beside the same row where all but a few dials are blank](product_sum.png)

Although the two rows are built differently, a single operation turns each one into the other, and that operation is asking for a number. Ask an endless product for a single whole number, in a way that respects addition. You might expect that such a question could sample all the dials at once, weighting them somehow, but it cannot, because any such question reads only finitely many dials and ignores the rest.

![A reader scanning along an endless row of dials and coming to a halt after finitely many, because no legal question can reach further](finite_reach.gif)

That is Specker's theorem from 1950, and the lectures use it constantly. The shape of the reason is worth a sentence, because it is the shape of section 6 below as well, and it is that a legal question is defeated by divisibility. Settings that live only in the far tail of the row can be made divisible by as high a power of a number as you like, so the answer they force would have to be divisible by every such power, and the only whole number like that is zero. Making that precise is more work than one sentence, and this guide leaves it to the sources.

Ask an endless sum for a number and the opposite happens, since you may choose an answer for every dial independently. Only finitely many dials are ever on, so nothing diverges, and the questions on a sum form a product.

Put these together with the previous section and the shape of a weighting falls out. The measurements on a probe form a free group, so they are a sum of copies of the whole numbers. The weightings are exactly the questions one can ask of the measurements. Therefore:

> Every collection of weightings on a probe is an endless product of copies of the whole numbers.

That is the lectures' Corollary 5.5 ([page 34](https://arxiv.org/pdf/2605.03658v1#page=34)), and the statement is a blunt one. Whatever probe you started with, however intricately it branched, the weightings on it are just a row of dials, so all the structure has been pushed into how many dials there are.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/04.html)** to set dials in a product and a sum, and try to build a question that reaches past the end.

---

[← Every function is a stack of steps](../03-stacks-of-steps/README.md)  ·  [The solid rule →](../05-the-solid-rule/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

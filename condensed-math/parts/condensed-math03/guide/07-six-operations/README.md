# 7 · The six operations

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Everything now assembles into the standard shape that modern geometry organises itself around. Nothing new is required: the six operations are the ones already built.

![The six operations arranged as three adjoint pairs, with the pullback, the two pushforwards, and their partners](six.png)

Reading the diagram. To each space one attaches a category of sheaves. Then there are three pairs, each pair being an operation and its exact counterweight:

**Combine and separate.** A way of multiplying two sheaves together, and its partner that asks what one sheaf does to another.

**Pull back and push forward.** Given a map of spaces, a way of dragging a sheaf backwards along it, and its partner pushing forwards.

**Push forward with compact support, and its counterweight.** Section 5's operation, and the one that produced the dualizing object.

The lectures state plainly which of these is the difficulty. The first four are easy; constructing the third pair is where the work is, and it is the only reason condensed mathematics was needed at all in this story ([the discussion after Theorem 11.1, page 72](https://arxiv.org/pdf/2605.03658v1#page=72)).

Two rules pin the third pair down. When the map is proper, meaning nothing escapes to the edge, pushing forward with compact support is just pushing forward. When the map is an open inclusion, the counterweight is just the pullback. Between them these force the definition everywhere, by factoring any reasonable map into an open inclusion followed by a proper map. The lectures note the standard consequence: since the definition is forced, the real content is checking it does not depend on how you factored.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/07.html)** to move a sheaf around a map with each operation and see where it lands.

---

[← Gluing the local pictures](../06-gluing-the-pictures/README.md)  ·  [Duality, watched →](../08-duality-watched/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

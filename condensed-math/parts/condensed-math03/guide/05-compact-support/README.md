# 5 · Cohomology with compact support

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

There are two natural ways to collect up the functions on a space:

**Everything.** Take all the functions, on the whole space, and record them. This is the ordinary one and it always works.

**Only what vanishes near the edge.** Take the functions that vanish near the edge, or more precisely the ones that can be pushed off the edge, and record those. This is the compactly supported one, and classically it is much harder to define for the kind of functions algebraic geometry uses.

![The functions near the edge, the functions everywhere, and the quotient between them being formed](compact_support.gif)

In this setting it is nearly free. Section 4 built the functions near the edge, with the functions everywhere sitting inside them. The compactly supported collection is assembled from exactly that comparison, and the construction goes through because both sides are modules over a ring with a rule, so infinite sums behave in every step ([Theorem 8.1, page 53](https://arxiv.org/pdf/2605.03658v1#page=53)).

What comes out is stronger than the construction:

> The compactly supported collection has a partner: a second operation that is its exact counterweight, meaning that maps out of anything the first operation produces correspond exactly, and in only one way, to maps into what the second produces. Applying that partner to the simplest possible input returns one specific object, and that object is the classical dualizing complex.

That is Theorem 8.2 ([page 53](https://arxiv.org/pdf/2605.03658v1#page=53)). The dualizing complex is the object classical duality theory needs, and classically it has to be constructed by hand, with cases and choices. Here it is whatever the counterweight produces, with no choices at all.

![The dualizing object of the line and of the cross, read off from the tails at each edge](dualizing.png)

The lectures make this concrete on the cross of section 4 and get a formula for its dualizing complex directly out of the tails ([Remark 8.5, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)). This repository reproduces the counting side of that formula by truncation.

Two remarks in the lectures are worth carrying, because they say what was gained. The first is that the compactly supported operation does not preserve ordinary discrete objects, and it *cannot*, since the tails are genuinely infinite. This means that it does not exist, even naively, in the classical setting, and the operation is only available because the modules are allowed to be answer sheets. Its counterweight does land back among ordinary objects, so the classical theory could reach the answer without being able to follow the construction that produces it ([the discussion under Theorem 8.2, page 53](https://arxiv.org/pdf/2605.03658v1#page=53)).

The second remark is about finiteness. The finiteness statements of classical coherent cohomology, that certain collections of functions are finitely generated, become the statement that the compactly supported operation preserves a purely formal notion of smallness ([Remark 8.3, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)).

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/05.html)** to form the quotient yourself on the line and on the cross.

---

[← Functions near the edge](../04-functions-near-the-edge/README.md)  ·  [Gluing the local pictures →](../06-gluing-the-pictures/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

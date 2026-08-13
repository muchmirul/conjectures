# 8 · Duality, watched

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Duality relates two kinds of cohomological information through a pairing that produces a scalar on the base. A perfect pairing loses no information: either input can be recovered from how it pairs with every possible input on the other side. For a smooth space, the complementary object involves differential forms and a shift by the dimension.

![A rotating three-dimensional view of a surface, with a class in one degree and its partner in the complementary degree pairing to a single number](duality.gif)

The animation represents this complementary pairing on a surface. One class lies in a lower degree, its partner lies in the corresponding complementary degree, and compactly supported pushforward carries their product to the base. A trace map then turns the top-degree result into one scalar.

The precise theorem assumes a separated smooth map of finite type from a space X to a base ring, with a fixed relative dimension ([Theorem 11.1, page 71](https://arxiv.org/pdf/2605.03658v1#page=71)). It constructs compactly supported pushforward, proves that it agrees with ordinary cohomology when the map is proper, and supplies a canonical trace from top-degree differential forms to the base. For every suitable complex on X, pairing with the trace identifies its dual with the corresponding differential-form complex. This is coherent duality in the solid-module setting.

![The pairing on a curve, degree zero against degree one, with the trace collapsing the result to a single number](pairing.png)

Three features explain how the previous sections contribute to this result. Together, they connect the abstract framework to the classical theorem.

**The dualizing object is characterized by an adjunction.** Upper shriek is defined as the right adjoint of compactly supported pushforward, and its value on the unit is the dualizing complex. The theorem then identifies this canonical object with the expected differential forms in the smooth case and proves that the trace pairing is perfect.

**Finiteness follows from preservation of compactness.** Compactly supported pushforward preserves compact objects. For a proper map it agrees with ordinary pushforward, which also preserves discreteness, so this formal statement recovers the classical finite-generation result for coherent cohomology ([Remark 8.3, page 54](https://arxiv.org/pdf/2605.03658v1#page=54)).

**The construction passes through nondiscrete modules.** Boundary functions contain infinite tails, so compactly supported pushforward generally leaves the category of ordinary modules. Its right adjoint returns the dualizing complex to the discrete setting. Condensed mathematics supplies the larger middle category in which the full construction can be carried out.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/08.html)** to pair complementary classes and follow their product through the trace to a scalar.

---

[← The six operations](../07-six-operations/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

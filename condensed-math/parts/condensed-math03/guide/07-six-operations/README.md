# 7 · The six operations

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The local and global constructions now fit into the **six-operations formalism**, the standard organizational structure for modern cohomology theories. To each space it assigns a category of sheaf-like objects. A map of spaces then gives operations that move or compare those objects in controlled ways.

![The six operations arranged as three adjoint pairs, with the pullback, the two pushforwards, and their partners](six.png)

The six operations come in three related pairs. In each pair, one operation is adjoint to the other, meaning that maps after applying the first correspond naturally to maps after applying its partner.

**Combine and separate.** Tensor product combines two sheaves on the same space. Internal Hom is its partner and records the maps from one sheaf into another.

**Pull back and push forward.** For a map of spaces, pullback transfers a sheaf from the target to the source. Ordinary pushforward transfers information from the source back to the target and is the right adjoint of pullback.

**Push forward with compact support, and its counterweight.** Lower shriek pushes forward while controlling behaviour at the boundary. Upper shriek is its right adjoint and produces the dualizing object when applied to the unit.

The lectures explain that the first four operations can be constructed without condensed mathematics. The difficult step is lower shriek, the compactly supported pushforward built from the boundary theory in section 5. Constructing this third pair is the reason condensed modules enter the six-operation story ([the discussion after Theorem 11.1, page 72](https://arxiv.org/pdf/2605.03658v1#page=72)).

Two familiar cases determine how lower shriek must behave. For a proper map, nothing can escape through a boundary, so compactly supported pushforward equals ordinary pushforward. For an open inclusion, upper shriek equals pullback, which makes lower shriek the left adjoint of pullback. Nagata compactification factors a separated finite-type map into an open inclusion followed by a proper map. These rules therefore determine the candidate operation, while the theorem must still show that it is independent of the chosen factorization and behaves coherently under composition.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/07.html)** to apply each operation to a sheaf and compare the directions of the three adjoint pairs.

---

[← Gluing the local pictures](../06-gluing-the-pictures/README.md)  ·  [Duality, watched →](../08-duality-watched/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

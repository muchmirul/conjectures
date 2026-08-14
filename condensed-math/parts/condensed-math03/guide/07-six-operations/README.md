# 7 · The six operations

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The local and global constructions now fit into the **six-operations formalism**, the standard organizational structure for modern cohomology theories. To each space it assigns a category of sheaf-like objects. A map of spaces then gives operations that move or compare those objects in controlled ways.

![Tensor and internal Hom, pullback and pushforward, and the two shriek operations are arranged as three adjoint pairs](six.png)

The six operations come in three related pairs. In each pair, one operation is adjoint to the other, meaning that maps after applying the first correspond naturally to maps after applying its partner.

**Combine and separate.** Tensor product combines two sheaves on the same space. Internal Hom is its partner and records the maps from one sheaf into another.

**Pull back and push forward.** For a map of spaces, pullback transfers a sheaf from the target to the source. Ordinary pushforward transfers information from the source back to the target and is the right adjoint of pullback.

**Push forward with compact support, and its counterweight.** Lower shriek pushes forward while controlling behaviour at the boundary. Upper shriek is its right adjoint and produces the dualizing object when applied to the unit.

The lectures explain that the first four operations can be constructed without condensed mathematics. The difficult step is lower shriek, the compactly supported pushforward built from the boundary theory in section 5. Constructing this third pair is the reason condensed modules enter the six-operation story ([the discussion after Theorem 11.1, page 72](https://arxiv.org/pdf/2605.03658v1#page=72)).

Two familiar cases determine how lower shriek must behave. For a proper map, nothing can escape through a boundary, so compactly supported pushforward equals ordinary pushforward. For an open inclusion, upper shriek equals pullback, which makes lower shriek the left adjoint of pullback. Nagata compactification factors a separated finite-type map into an open inclusion followed by a proper map. These rules therefore determine the candidate operation, while the theorem must still show that it is independent of the chosen factorization and behaves coherently under composition.

### The mathematics

The discussion after [Theorem 11.1, page 72 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=72) arranges the six operations into three adjoint pairs:

```math
-\otimes_X B\dashv R\!\operatorname{Hom}_X(B,-),
\qquad
f^*\dashv f_*,
\qquad
f_!\dashv f^!.
```

Two required identities are

```math
f_!\cong f_*\quad\text{when }f\text{ is proper},
\qquad
f^!\cong f^*\quad\text{when }f\text{ is étale}.
```

The projection formula is

```math
f_!(A\otimes_X f^*B)\cong f_!A\otimes_Y B.
```

**Reading the symbols.** The tensor product $\otimes_X$ combines objects on the same space $X$. The derived internal Hom $R\!\operatorname{Hom}_X$ records maps from $B$. The map of spaces is $f:X\to Y$. Its pullback is $f^*$, ordinary pushforward is $f_*$, compactly supported pushforward is $f_!$, and the right adjoint of the latter is $f^!$. The symbol $\dashv$ says that the operation on the left is left adjoint to the one on the right. The symbol $\cong$ means naturally isomorphic. Proper means that nothing escapes at the boundary, and étale is the local condition under which upper shriek agrees with pullback. In the final line, $A$ is an object on $X$ and $B$ is an object on $Y$.

**Why it matters.** The first four operations exist in ordinary derived algebraic geometry. Constructing $f_!$ and therefore $f^!$ is the difficult part. The boundary theory from chapter 5 supplies this missing pair and makes the required identities coherent under composition.

**In the simulation.** The operation selector chooses one of the six symbols. The arrows show its source and target, and switching to the paired operation reverses the adjunction. Proper and open examples display the two special rules that determine compactly supported pushforward.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/07.html)** to apply each operation to a sheaf and compare the directions of the three adjoint pairs.

---

[← Gluing the local pictures](../06-gluing-the-pictures/README.md)  ·  [Duality, watched →](../08-duality-watched/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

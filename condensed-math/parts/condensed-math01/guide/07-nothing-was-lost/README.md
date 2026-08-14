# 7 · Nothing was lost

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Changing from spaces to answer sheets is useful only if familiar spaces and continuous maps can still be recovered. The concern is natural because an answer sheet contains far more entries than a point set. The relevant comparison theorem says that, for a broad class of ordinary spaces, the new description preserves exactly the original maps and keeps distinct spaces distinct.

![Nested classes compare compact Hausdorff spaces, compactly generated spaces, and condensed sets](nesting.png)

Read the picture from the centre outward. Compact Hausdorff spaces correspond exactly to condensed sets that satisfy the matching compactness condition ([Theorem 2.16, page 17](https://arxiv.org/pdf/2605.03658v1#page=17)). In familiar Euclidean examples, these are the closed and bounded shapes. A larger surrounding class contains all metric spaces and spaces built from cells. On this larger class, the translation is fully faithful: different spaces have different answer sheets, and maps of answer sheets are exactly the continuous maps of spaces ([Proposition 1.7, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). Condensed sets extend beyond this image, as the ghost from section 5 demonstrates.

![A familiar space is converted to its probe data and reconstructed with the same topology](roundtrip.gif)

There is also a return construction. Begin with the point entries of an answer sheet, and declare a subset closed when every probe detects it as closed. For the broad class just described, translating a space into an answer sheet and then applying this construction returns the original topology. The animation follows that round trip.

The comparison has limits, and the lectures state them explicitly. If a topological space has a point that is not closed, its probe data do not define a condensed set of the required kind ([Warning 2.14, page 16](https://arxiv.org/pdf/2605.03658v1#page=16)). In the other direction, the return to ordinary topology can identify condensed information that topology cannot retain. One example involves compact objects built as increasing unions of strictly smaller closed pieces. The lectures interpret this as a limitation of ordinary topology, and note that the issue does not occur for countable colimits.

### The mathematics

[Proposition 1.7, page 9 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=9) says that the translation $X\mapsto\underline X$ is fully faithful on compactly generated spaces:

```math
\operatorname{Hom}_{\mathrm{Top}}(X,Y)
\xrightarrow{\sim}
\operatorname{Hom}_{\operatorname{Cond}(\mathrm{Set})}(\underline X,\underline Y).
```

It also gives the return map, and [Theorem 2.16, page 17](https://arxiv.org/pdf/2605.03658v1#page=17) identifies the compact case:

```math
(\underline X(*))_{\mathrm{top}}\cong X,
\qquad
\{\text{compact Hausdorff spaces}\}\simeq
\{\text{qcqs condensed sets}\}.
```

**Reading the symbols.** The notation $\operatorname{Hom}$ means the set of maps. The subscript $\mathrm{Top}$ restricts to continuous maps of topological spaces, while $\operatorname{Cond}(\mathrm{Set})$ means condensed sets. The underline sends a space to its probe answers. An arrow marked $\sim$ is a bijection, so every map of answer sheets comes from one continuous map. The expression $\underline X(*)$ reads the point entry, and the subscript $\mathrm{top}$ equips it with the topology detected by all probes. The symbol $\cong$ means isomorphic. The double arrow $\simeq$ means an equivalence of categories. The abbreviation qcqs means quasicompact and quasiseparated.

**Why it matters.** The translation preserves both objects and maps on the familiar class used in the guide. It is an enlargement of topology, not a replacement that forgets ordinary spaces. [Warning 2.14, page 16](https://arxiv.org/pdf/2605.03658v1#page=16) gives the stated boundary: a space with a nonclosed point does not define a condensed set of this kind.

**In the simulation.** Choosing a familiar space runs $X\mapsto\underline X\mapsto(\underline X(*))_{\mathrm{top}}$ and returns the same picture. Choosing the space with a nonclosed point stops at the first arrow, showing the warning rather than claiming the theorem there.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/07.html)** to follow a space through the translation and compare the recovered result with the starting space.

---

[← Probes that never need folding](../06-unfoldable-probes/README.md)  ·  [Counting holes →](../08-counting-holes/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

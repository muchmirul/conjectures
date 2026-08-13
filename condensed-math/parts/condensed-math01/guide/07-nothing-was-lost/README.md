# 7 · Nothing was lost

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

A repair is only worth having if it keeps what was already good. This section is the receipt.

The worry is reasonable. Answer sheets are stranger and larger than spaces, and swapping every space for its answer sheet might smear distinct spaces together, or might quietly forget which maps between spaces were the continuous ones.

Neither happens, on a class of spaces broad enough to contain everything anyone draws.

![Nested regions showing which topological spaces sit inside condensed sets, and which condensed sets come from spaces](nesting.png)

Reading the picture from the inside out. The compact shapes, meaning the ones that are closed, bounded and separated, correspond exactly to the answer sheets that are compact in the matching sense, with nothing on either side left over ([Theorem 2.16, page 17](https://arxiv.org/pdf/2605.03658v1#page=17)). Around them sits a much wider class, containing every space with a distance and every shape built out of cells, and on that class the translation is still faithful: two different spaces give two different answer sheets, and the continuous maps between two spaces are exactly the maps between their answer sheets ([Proposition 1.7, page 9](https://arxiv.org/pdf/2605.03658v1#page=9)). Outside that, condensed sets keep going, and the ghost of section 5 lives out there.

![A space being translated into its answer sheet and read back out, returning to the same space](roundtrip.gif)

There is a way back, too. From an answer sheet you can recover a space by taking its points and declaring a set closed when every probe says so. On the wide class above, the round trip returns the space you started with, which is what the animation traces.

Two honest limits, both flagged in the lectures. The translation genuinely fails for spaces where a point need not be closed, and such a space never gives an answer sheet at all ([Warning 2.14, page 16](https://arxiv.org/pdf/2605.03658v1#page=16)). And in the other direction, the return trip can merge things: there are compact shapes which are an increasing union of strictly smaller closed pieces, in a way ordinary topology cannot record but an answer sheet can. The lectures regard that as topology losing information rather than condensed sets gaining it, and note it cannot happen for unions taken one step at a time.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/07.html)** to send a space around the round trip and watch what comes back.

---

[← Probes that never need folding](../06-unfoldable-probes/README.md)  ·  [Counting holes →](../08-counting-holes/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

# 2 · Six is forced

Five people can stay safe with two colours. Six people cannot. This is the one theorem proved completely in this guide, and every step can be seen in the animation.

Choose one of the six people and look at the five connections leading from that person. There are only two colours available. At least three of those five connections must have the same colour, because two connections of each colour would account for only four. Suppose three of them are red.

![Three same-coloured connections from one person forcing a red or blue triangle](pigeonhole.gif)

Now focus on the three people at the other ends of those red connections. If any pair among them is joined in red, that connection and the two red connections back to the first person make a red triangle. To avoid that outcome, all three connections among those people would have to be blue. But those three blue connections make a blue triangle instead.

A one-colour triangle appears in either case. The first counting step is often called the **pigeonhole principle**: when more objects are placed into fewer groups, one group must receive several objects.

The argument did not depend on how the connections were coloured, so it covers every possible two-colouring of six people. The computer tests check the same claim another way. Six people have fifteen connections, with two choices for each connection, giving 32768 complete colourings. The tests inspect all of them and find that none is safe.

![All 32768 two-colourings of six people grouped by their number of one-colour triangles](census.png)

The empty bar at zero confirms that every colouring contains a one-colour triangle. The bar at one is empty too. Even the best six-person colourings contain exactly two one-colour triangles, never only one. Goodman recorded this stronger observation in 1959, and the exhaustive test finds it again.

The two-colour story is now complete: five people can stay safe, while six force a loss. We will call six **the forcing size** for two colours, meaning the first group size at which a one-colour triangle is unavoidable.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/02.html)** to try colouring six people and see which triangle becomes unavoidable.

---

[← The game](../01-the-game/README.md)  ·  [More crayons →](../03-more-crayons/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

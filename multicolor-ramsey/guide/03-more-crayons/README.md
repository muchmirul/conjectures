# 3 · More crayons

Adding a third colour makes a much larger safe group possible, raising the best safe size from five people to sixteen. The opening animation showed the full colouring, and the next picture separates its three colours so that each can be checked on its own.

![The sixteen-person colouring separated into three colour layers, none of which contains a triangle](layers.png)

Each panel contains the connections of one colour. Every person has five connections in each panel, but no panel contains a triangle. A one-colour triangle would have to appear entirely inside one of these panels, so the full three-colour pattern is safe. Greenwood and Gleason created this pattern in 1955. This repository rebuilds it from their instructions and checks all 560 groups of three.

They also proved that seventeen people cannot stay safe with three colours. A direct computer sweep would require considering three choices on each of 136 connections, which is far beyond the case-by-case checks in this project. The guide therefore quotes their theorem rather than claiming to verify it. After three colours, no exact forcing size is known.

![The exact answers for one, two and three colours, followed by the open range for four colours](records.png)

For four colours, the forcing size is known to be somewhere between 51 and 62. In other words, a safe colouring of fifty people is known, and every colouring of sixty-two people is known to fail, but the exact point between them remains open. The uncertainty is even wider for five colours, and no exact answer is known for any colour count above three. The number of possible colourings grows too quickly for a simple search, so progress depends on general arguments and constructions.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/03.html)** to compare the known small cases and the first open range.

---

[← Six is forced](../02-six-is-forced/README.md)  ·  [The question →](../04-the-question/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

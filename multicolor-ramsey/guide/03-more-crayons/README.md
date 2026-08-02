# 3 · More crayons

A third color changes the scale of the game. The record safe group jumps from five to sixteen, and the sixteen-person coloring is the one the opening animation drew. Here it is taken apart, one color at a time.

![The record three-color table split into its three one-color nets, each triangle-free](layers.png)

Each panel is one color's net. Every person is joined to exactly five others in each color, and each net, seen on its own, contains no triangle at all. A net with no triangle can never hold a one-color one, so the whole table is safe. The construction comes from Greenwood and Gleason in 1955; this repository rebuilds it from their recipe and re-checks all 560 triangles.

Greenwood and Gleason also proved the matching failure: seventeen people cannot be kept safe with three colors. That direction is far beyond checking case by case, since the colorings of seventeen people outnumber atoms, so this article quotes it rather than verifying it.

Then the exact answers stop.

![What is known for one, two, three and four colors, with the four-color range still open](records.png)

For four colors the forcing size is known to be somewhere between 51 and 62, a range that has stood for decades. For five colors the uncertainty is wider still. Nobody knows the answer for any color count past three, and it is not for lack of computers: the case-by-case approach dies immediately, and everything since has been about finding arguments instead.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/03.html)** and turn the idea over yourself.

---

[← Six is forced](../02-six-is-forced/README.md)  ·  [The question →](../04-the-question/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

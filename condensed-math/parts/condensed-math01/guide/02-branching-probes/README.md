# 2 · Probes that branch

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Here is what will do the seeing.

Start with a single box. Split it into two boxes. Split each of those into two, and keep splitting forever. At every stage you have a finite list of boxes and a record of which box came from which. Nothing infinite has happened yet at any single stage: each stage is a finite picture a child could draw.

![Three probes side by side: the endlessly halving one, the one that is a single approaching sequence, and the one whose boxes split five ways](probes.png)

A **probe** is a splitting scheme like this, together with the dust of points you reach by following the splits forever. Three of them carry this whole guide, and the picture shows all three:

The **halving probe** splits every box in two, every time. After ten rounds it has 1024 boxes. Its dust is the classical Cantor set: take a line, remove the middle third, remove the middle third of what is left, and repeat.

The **approaching probe** is thinner. Its dust is a single sequence of points marching towards one limit point, together with that limit point. At stage five it has separated the first five points and is still holding everything beyond them in one box.

The **counting-in-base-p probe** splits every box into p boxes. Its dust is what number theorists call the p-adic integers, and part two of this guide will live inside it.

The lectures call these objects profinite sets, and the word says what they are: made out of finite things ([Definition 1.2, page 6](https://arxiv.org/pdf/2605.03658v1#page=6)). Two features of the definition matter later, and both are visible in the picture. Every stage is finite, so nothing at any stage is hard. And the whole probe is nothing but the stages plus the memory of which box sits in which, so a probe carries no extra information smuggled in from outside.

The code in this repository stores probes exactly this way, as a list of finite stages plus the map from each stage to the one before, and the tests check that the halving probe really doubles, that the approaching probe really adds one separated point per stage, and that following the splits down and reading a weight back up is consistent.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/02.html)** to switch between the three probes, set the depth, and click a box to see everything inside it.

---

[← Two real lines](../01-two-real-lines/README.md)  ·  [What a shape says to a probe →](../03-what-a-shape-says/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

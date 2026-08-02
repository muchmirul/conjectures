# 1 · The game

Take a group of people and connect every pair with a string. Now color every string. You lose the moment three people are joined to each other by three strings of the same color. Call such a threesome a **one-color triangle**, and call a finished coloring with no one-color triangle **safe**.

![A four-person group colored two ways, one with a one-color triangle and one safe](rules.png)

The left group is lost: the thick triangle has all three of its strings in the first color. The right group is safe: every one of its four possible triangles wears two colors.

With two colors, five people can be kept safe, and there is essentially one way to do it. Put the five in a circle. Color the ring of neighbouring pairs with the first color and the star of skipping pairs with the second.

![The five-person table being colored, then all ten triangles checked one by one](pentagon.gif)

The sweep at the end is the point. A safe coloring is not a vague impression, it is a finite list of checks: this table has ten possible triangles, and all ten mix their colors. The test suite of this repository performs exactly that sweep.

Why it works is worth one sentence. Each color's strings form a ring of five on their own, and a ring has no triangle of any kind, so it certainly has no one-color one.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/01.html)** and turn the idea over yourself.

---

[← Start here](../00-start-here/README.md)  ·  [Six is forced →](../02-six-is-forced/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

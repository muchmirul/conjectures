# 6 · The ceiling

The other guardrail comes from the six-person argument of chapter 2, which generalizes to any number of colors. Pick one person at a big table and sort everyone else by the color of their string to her.

![One person's fifteen connections in the sixteen-person table, sliding into three color groups](sort.gif)

With three colors and fifteen strings, some group holds at least five people. Inside that group, its own color is now poison: any string of that color between two members would close a triangle with the person at the center. So the group is a smaller table effectively playing with one color fewer, and the same move can be made again inside it, and again, until the colors run out and a bare triangle is forced.

Run the argument in reverse and it says: a table safe for one color holds at most 2 people, so a table safe for two colors holds at most a group small enough that sorting works out, and so on. The forcing sizes it proves are 3, 6, 17, 66, 327, and onward, each step multiplying by roughly the number of colors.

![The staircase of forcing sizes next to plain factorials on a growth chart](staircase.png)

Multiplying by the color count at every step is exactly what a factorial does, so the ceiling grows like a factorial. The staircase happens to be exactly right at two colors and at three, where 6 and 17 are the true answers. At four colors it says 66 while the truth is at most 62; the best refinement in the literature trims such constants, reaching about e minus one sixth times the factorial, but no refinement has ever changed the factorial shape.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/06.html)** and turn the idea over yourself.

---

[← Multiply](../05-multiply/README.md)  ·  [The gap →](../07-the-gap/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

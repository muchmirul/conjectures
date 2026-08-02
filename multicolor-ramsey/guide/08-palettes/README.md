# 8 · Palettes

Nothing in the next three chapters is harder than what you have already read. The construction has three moving parts, each of which is a rule simple enough to draw, and this chapter is the first: who is allowed to use which color.

The people are divided into rooms, as in chapter 5. The new ingredient is that every room is issued a **palette**: a list of colors that room deliberately refuses to use inside itself. Every other color is fair game internally. And a string between two different rooms must use a color that exactly one of the two rooms holds.

![A string between two rooms auditioning colors until one is held on exactly one side](rooms.gif)

That little rule already kills every triangle that touches three different rooms. Fix any single color and any three rooms, and ask whether that color is held or missing in each room. A triangle across the three rooms would need its color on all three walls, held on exactly one side of each. Try to arrange it: around the triangle, held must alternate with missing at every wall, and a cycle of three cannot alternate. Some wall always has the color held on both sides or on neither.

![All eight hold-or-miss patterns for one color across three rooms, each with an unusable wall](parity.png)

All eight patterns fail, and the tests enumerate them rather than trusting the story. So triangles across three rooms are ruled out, and the rule costs nothing. What it does not rule out is a triangle with two corners in the same room, and that is the trap of the next chapter.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/08.html)** and turn the idea over yourself.

---

[← The gap](../07-the-gap/README.md)  ·  [The trap →](../09-the-trap/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

# 5 · Multiply

The classical tool takes two safe tables and multiplies them. Watch it act on two copies of the pentagon.

![Each of five people becoming a room of five, keeping outer colors between rooms and fresh colors inside](blowup.gif)

Each of the original five people becomes a **room** holding a full copy of the other table. A string between two rooms keeps the color the two original people used. A string inside a room uses the inner table's coloring, in fresh colors that nothing else touches.

The result is safe, and the reason splits cleanly in two. A triangle with all three corners in one room is a triangle of the inner table, and the inner table was safe. A triangle touching more than one room cannot use any inside color, so all its strings run between rooms; but two corners in one room lead outward in strings that copy the *same* original person's colors, so the triangle's colors trace a triangle of the outer table, and the outer table was safe. The tests do not take this on faith: they verify the 25-person, four-color product cold, all 2300 triangles, and an 80-person, five-color product as well.

So safe tables multiply: sizes multiply, color counts add. Repeat forever and five people at two colors become 25 at four, 125 at six, and so on without end.

![Repeated products of the pentagon and of the sixteen table, straight lines on a growth chart](tower.png)

Both lines are straight on this chart, and straight means stuck. Multiplying the pentagon forever earns exactly 2.24 people per color at every step, and the sixteen-person table earns exactly 2.52, because each round adds the same colors and multiplies by the same factor. A fixed recipe, repeated, can never make the rate climb. Whatever answers the question of chapter 4 has to spend its colors in a genuinely new way.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/05.html)** and turn the idea over yourself.

---

[← The question](../04-the-question/README.md)  ·  [The ceiling →](../06-the-ceiling/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

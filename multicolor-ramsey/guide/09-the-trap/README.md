# 9 · The trap

The dangerous triangle has two corners inside one room and one corner outside. The color on its strings is one the room actively uses, so the room contains strings of that color, and an outsider connected in by two same-colored strings might land exactly on two people the room has already joined in that color.

The defense starts by looking at one color's net inside the room. Here is the red net of the pentagon room, with its people badged into **teams**.

![The red net inside the pentagon room, with three teams and no red string inside any team](teams.png)

The teams are chosen so that no red string stays inside one team; every red string crosses between teams. Three teams suffice for the pentagon's red net. Now the rule that disarms the trap: all red strings arriving from any one outsider must land inside a single team.

![The trap springing when the rule is broken, and failing to spring when it is obeyed](trap.gif)

Watch both halves. Rule ignored, the outsider's two red strings land on two people who are red-connected, and the triangle snaps shut. Rule obeyed, the outsider's red strings land on teammates only, teammates are never red-connected, and no red triangle can involve that outsider. Strings that the rule turns away are colored instead with a color the room's palette forbids inside, which is harmless for the room automatically: a triangle needs an inside string of its color, and there are none. The tests verify both endings on exactly the colorings drawn here.

This is the point of palettes beyond the parity trick of chapter 8. A palette does not just say which colors a room avoids. It splits every arriving color into two safety cases: colors the room misses are safe by emptiness, and colors the room holds are safe by teams, provided the landing rule is enforced. Enforcing it for every pair of rooms at once, without spending new colors, is the job of the referee.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/09.html)** and turn the idea over yourself.

---

[← Palettes](../08-palettes/README.md)  ·  [The referee →](../10-the-referee/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

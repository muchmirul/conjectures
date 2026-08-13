# 9 · The trap

The second part of the construction handles the remaining danger, a triangle that uses two rooms. Consider two people in one room and a third person outside it. Suppose both incoming connections use red. A red triangle appears if the two people inside the room are also connected in red. The construction must prevent the two incoming connections from landing on such a pair.

Look at the red connections already inside the room. Split the people into **teams** so that no red connection has both ends in one team. In the five-person room, the red connections form a ring, and the next picture shows a split into three teams.

![The red ring inside a five-person room split into three teams, with no red connection within a team](teams.png)

Now impose the landing rule: all red connections coming from the same outside person must end within one team. Since no two teammates are joined in red, those arrivals cannot complete a red triangle.

![An outside person's arrivals making a triangle when the team rule is ignored and staying safe when it is followed](trap.gif)

The first half of the animation breaks the rule. The two red arrivals land on people who are connected in red, so the triangle closes. In the second half, both arrivals land in one team, where no red connection exists, and the triangle cannot close.

There is a second safe case. If red appears on the room's palette, then red is not used anywhere inside that room. Incoming red connections are automatically harmless because the triangle would need a red internal connection too. Thus every incoming colour is protected in one of two ways: it is absent inside the room, or its arrivals are confined to one safe team.

It would be convenient to use only two teams for every colour, but that rule is too strict. Keeping the same two sides lined up across every room and every floor would cost almost as much as giving each room fresh colours. The new construction lets the number of teams grow slowly instead. When a floor is added, rooms that use a colour keep their existing teams. All rooms that omit that colour form one extra team together. The number of teams therefore rises by only one on each floor. This keeps the referee's set of symbols small enough to manage.

The animation is a small demonstration of why the team rule matters. The real construction does not choose each arrival by hand, so it needs one fixed procedure that enforces the rule for every pair of rooms without adding new colours. That procedure is the referee in the next section.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/09.html)** to compare a broken landing rule with a safe one.

---

[← Palettes](../08-palettes/README.md)  ·  [The referee →](../10-the-referee/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

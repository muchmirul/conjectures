# 8 · Palettes

**The proof begins here.** Sections 8 to 11 follow the proof document itself, one moving part per section, with the walkthrough's account of how each part was found told alongside.

The next three sections reuse ideas already introduced: rooms, colours, and the need to prevent one-colour triangles. Each section adds one simple rule. The first rule decides which colours may be used in each room.

As in section 5, divide the people into rooms. Give every room a **palette**, meaning a list of colours that are not allowed on connections inside that room. All colours outside the list may be used internally. In the pictures, a room is said to “hold” a colour when that colour is on its palette, even though holding it means keeping it out of the room.

A connection between two different rooms may use a colour only when that colour appears on exactly one of their palettes.

![A connection between two rooms trying colours until it finds one listed by exactly one room](rooms.gif)

This rule immediately prevents a one-colour triangle spread across three rooms. Fix one colour and look at any three room palettes. For each room, the colour is either listed or not listed. Among three rooms, at least two must have the same answer. The connection between those two rooms cannot use that colour, because a cross-room colour must be listed by exactly one side. The chosen colour therefore cannot appear on all three sides of the triangle.

![All eight listed-or-unlisted patterns for one colour across three rooms, each blocking at least one side](parity.png)

The figure shows all eight possible patterns, and the tests check every one. No extra colour was needed to rule out triangles across three rooms. A different danger remains: two corners of a triangle may lie in the same room while the third lies outside. The next section handles that case.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/08.html)** to change the palettes and see which cross-room colours are allowed.

---

[← The gap](../07-the-gap/README.md)  ·  [The trap →](../09-the-trap/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

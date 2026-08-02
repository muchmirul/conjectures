# 11 · The tower

**The proof, part four of four.** The assembly, the count, and the final rate.

The palette rule protects triangles across three rooms. The team rule protects triangles that use two rooms. The referee enforces the team rule everywhere at once. The construction now repeats these parts over several floors.

The ground floor contains one person. On each new floor, many rooms are created. Every room contains a complete copy of the floor below, with its internal colours renamed to match the colours allowed by that room's palette. Different rooms receive palettes that differ in many places, ensuring that the referee always has enough cross-room colours from which to choose. The same fixed referee rule colours every connection between rooms. Every kind of triangle is now covered: a triangle inside a single room is a triangle of the floor below, already ruled out one floor down, and the palette and team rules dispose of the triangles that touch two or three rooms.

![Several floors of rooms inside larger rooms, with the multiplying gain increasing on later floors](tower.gif)

The animation shows the nesting pattern, not the true number of rooms. Even the first full-scale floors are far too wide to draw. The important change is that the available colour pool grows from one floor to the next. A larger pool provides many more sufficiently different palettes, so a later floor can contain more rooms than an earlier floor. Each floor multiplies the group size by a larger amount than the floor before it.

Why must many sufficiently different palettes exist at all? The proof chooses them greedily: keep any new palette that differs enough from every palette already kept, and stop only when nothing more can be added. At that point, every possible palette sits close to one of the kept ones. Palettes close to any single kept palette are rare compared with the vastness of all palettes, so covering everything requires an enormous number of kept ones. Counting that cover is the entire existence argument, and it is where each floor's room count comes from.

This is exactly what fixed products could not do. In section 5, every round used the same number of rooms and kept the score flat. Here, the number of rooms rises with the floor, so the people-per-colour score rises too.

There is a trade-off. Palettes must differ in many colours so that the referee has enough choices, which makes each palette large and spends more colours. Making the tower taller creates more multiplying gains, but also increases that cost. After balancing the two, first multiply the tower height by a slowly growing logarithmic factor and then cube the result. That is roughly how many colours the tower uses. Its people-per-colour score grows roughly like the height.

Turning that relationship around gives the final rate: for a given colour count, the score is about the cube root of the colour count, divided by its logarithm. A logarithm is a slow-growing way to record repeated multiplication. It grows much more slowly than a cube root, so the score eventually keeps increasing.

![The fixed scores of older recipes compared with the rising shape of the 2026 score](base.png)

The rising curve shows the long-term shape without the theorem's tiny fixed multiplier. It is not a plot of useful values at small colour counts. For the smallest full-scale stage, the referee's card has 57 rows. Each floor uses palettes containing 114 colors, and three floors use 342 colours altogether. This repository recalculates those parameters from the paper's instructions.

One further step deserves a mention, because without it the theorem would be weaker than it sounds. Towers exist only at special colour counts: 342, then the next full height, and so on. For a colour count that falls between two towers, the proof uses the tallest tower below it and simply never touches the leftover colours. Neighbouring tower sizes are close enough that this wastes only a fixed fraction of the score. The final statement therefore holds at every colour count from two upward, not only at the special ones.

---

[← The referee](../10-the-referee/README.md)  ·  [What it means, and what it does not →](../12-what-it-means/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

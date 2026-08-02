# 11 · The tower

The fourth part assembles the rooms, counts how quickly they grow, and turns that count into the final rate.

The palette rule protects triangles across three rooms. The team rule protects triangles that use two rooms. The referee enforces the team rule everywhere at once. The construction now repeats these parts over several floors.

The ground floor contains one person. On each new floor, many rooms are created. Every room contains a complete copy of the floor below, with its internal colours renamed to match the colours allowed by that room's palette. Different rooms receive palettes that differ in many places, so the referee always has enough cross-room colours to choose from. The same fixed referee rule colours every connection between rooms.

Every possible triangle is now covered. A triangle inside one room was already ruled out on the floor below. The team rule handles a triangle that touches two rooms, and the palette rule handles one that touches three.

![Several floors of rooms inside larger rooms, with the multiplying gain increasing on later floors](tower.gif)

The animation shows the nesting pattern, not the true number of rooms. Even the first full-scale floors are far too wide to draw. The important change is that the available colour pool grows from one floor to the next. A larger pool provides many more sufficiently different palettes, so a later floor can contain more rooms than an earlier floor. Each floor multiplies the group size by a larger amount than the floor before it.

The proof also has to show that enough different palettes exist. It builds a list in a simple way. Keep a new palette only when it differs enough from every palette already on the list. Stop when no more can be added. At that point, every unused palette must be close to one that was kept. Only a small share of all palettes can be close to any one kept palette. Since every possible palette must be covered this way, the kept list has to be enormous. Each kept palette becomes one room.

This is exactly what fixed products could not do. In section 5, every round used the same number of rooms and kept the score flat. Here, the number of rooms rises with the floor, so the people-per-colour score rises too.

There is a trade-off. Palettes must differ in many colours so that the referee has enough choices, which makes each palette large and spends more colours. Making the tower taller creates more multiplying gains, but also increases that cost. After balancing the two, first multiply the tower height by a slowly growing logarithmic factor and then cube the result. That is roughly how many colours the tower uses. Its people-per-colour score grows roughly like the height.

Turning that relationship around gives the final rate: for a given colour count, the score is about the cube root of the colour count, divided by its logarithm. A logarithm is a slow-growing way to record repeated multiplication. It grows much more slowly than a cube root, so the score eventually keeps increasing.

![The fixed scores of older recipes compared with the rising shape of the 2026 score](base.png)

The rising curve shows the long-term shape without the theorem's tiny fixed multiplier. It is not a plot of useful values at small colour counts. For the smallest full-scale stage, the referee's card has 57 rows. Each floor uses palettes containing 114 colors, and three floors use 342 colours altogether. This repository recalculates those parameters from the paper's instructions.

Complete towers naturally use only certain colour totals, beginning with 342 and then larger special values. The theorem must also cover colour counts between them. For such a count, the proof uses the tallest smaller tower and leaves the extra colours unused. Consecutive tower sizes are close enough that this reduces the score by only a fixed factor. The final result therefore applies to every colour count from two upward, not just the special totals.

---

[← The referee](../10-the-referee/README.md)  ·  [What it means, and what it does not →](../12-what-it-means/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

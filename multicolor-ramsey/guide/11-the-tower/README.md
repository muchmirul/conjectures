# 11 · The tower

All three parts are on the table. What remains is assembly, and one piece of bookkeeping that turns the assembly into a growing rate.

The construction is a tower of floors. The ground floor is one person. Each new floor takes a batch of fresh colors and builds many rooms, each room holding a complete copy of the floor below with its colors relabeled. Every room's palette is chosen from the enlarged pool, sized so that the colors a room holds are exactly as many as the floor below needs. Strings between rooms are colored by the referee, whose single fixed table serves every floor and every pair of rooms.

![Floors of rooms of rooms, with later floors multiplying by more than earlier ones](tower.gif)

The diagram is a cartoon of the shape, not a portrait of the size; the real floors are astronomically wide. The bookkeeping that matters is this. Palettes on floor after floor are drawn from a growing pool of colors, and the number of usably different palettes grows with the pool. So the number of rooms a floor can support grows as the tower rises. Each floor multiplies the table size by more than the floor before, and that is precisely the behaviour no fixed product could ever have.

Two constraints fight over the tower's height. Any two rooms on one floor must have palettes different enough that each room holds plenty of colors the other one is missing, or the referee has too few candidate colors to pick from; that forces palettes to be large, which spends colors. Colors, in turn, are what the final score divides by. Balancing the two, a tower of some height spends about the cube of that height in colors (times smaller logarithmic factors) and pays out about that height in people per color. Undo the cube: a table built with some number of colors earns a rate of about the *cube root* of its color count, divided by a logarithm.

![Flat rates of the fixed recipes against the climbing rate shape of the 2026 construction](base.png)

The flat lines are the whole world before 2026. The curve climbs past every one of them and keeps going. At the smallest full-scale size, the numbers are: a referee's card of 57 rows, palettes of 114 colors per floor, three floors, 342 colors in all. This repository computes those parameters from the paper's recipe and the tests pin them.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/11.html)** and turn the idea over yourself.

---

[← The referee](../10-the-referee/README.md)  ·  [What it means, and what it does not →](../12-what-it-means/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

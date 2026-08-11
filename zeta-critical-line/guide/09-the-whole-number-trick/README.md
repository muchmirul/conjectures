# 9 · The whole-number trick

The last ingredient is the oldest kind of mathematics in the paper: a fact about whole numbers, upgraded to tables. Nothing new is needed beyond chapter 8's two totals.

Here is the fact. Multiplicities are whole numbers: a pin counts once, or twice, or three times, never one and a half. Now compare a whole number's square with three times the number minus two. At one: one against one, even. At two: four against four, even again. At three and beyond: nine against seven, sixteen against ten, the square wins, and the gap only grows.

![The square of each whole number compared with the line three-times-minus-two, touching at one and two and above it afterwards](parabola.png)

So for every whole number, the square is at least three times the number minus two. Why care? Because in the table's energy, a pin of multiplicity m contributes like m squared, while in the count it contributes m. A doubled pin is energy-expensive: it pays four in energy for its two of count. Clean pins are the most energy-efficient inhabitants a table can have. Since chapter 8 *measured* the energy and found it modest, four thirds per zero, there simply is not enough energy in the table for many pins to be doubled or worse. Montgomery's original argument was exactly this, run under RH: modest energy forces most pins to be clean.

The paper's upgrade is to make the same trick work on the table itself, where off-line saddles and the microphones' finite reach muddy any pin-by-pin reading. The upgraded statement, the **rank-trace inequality** ([Lemma 3.2, equation 3.1, page 9](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=9)), says: for a sum of bowls and saddles, the number of independent directions the bowls span is at least twice the bowls' diagonal total, plus four times the saddles' diagonal total, minus four per saddle, minus the energy of the whole table. Every quantity on the right is either measured by the primes (chapter 8) or counted by the see-saw law (chapter 7). The proof of the upgrade is half a page of linear algebra resting on one classical inequality of von Neumann about how two tables can share their strength, and its whole-number soul is visible: setting every direction back to the scalar case collapses it to the square-versus-three-m-minus-two fact above.

This repository cannot prove the lemma any more than reading it can, but it can do what the paper's own referees did: attack it. The tests throw thousands of random bowl-and-saddle tables at the inequality, including adversarial near-equality shapes, and count how often the guaranteed floor exceeds the true direction count. The answer must be, and is, never.

![Random bowl-and-saddle tables plotted by guaranteed floor against true count, every point on the safe side of the diagonal](floor.png)

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/09.html)** to choose multiplicities and watch the energy budget expose doubled pins.

---

[← What the primes reveal](../08-the-prime-side/README.md)  ·  [Two thirds →](../10-two-thirds/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

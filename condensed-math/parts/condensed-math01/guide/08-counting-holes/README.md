# 8 · Counting holes

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The last section of part one checks the other thing that must survive: the holes.

Counting holes is the oldest way to tell shapes apart. A disc has none. A ring has one, and the count is visible by hand: walk a loop around it and count your turns.

![A loop being dragged around a ring while a counter records how many whole turns it has made](winding.gif)

The animation is the whole of the first hole-count of a circle. Drag a closed path around and the number of complete turns is a whole number, it cannot change by a little, and it is the only thing about the path that matters. That whole number is the circle's first cohomology, and it is a copy of the integers.

Now stack circles. Two circles at right angles make the surface of a doughnut, and it has two independent loops.

![A rotating three-dimensional view of a doughnut surface carrying its two independent loops](torus.gif)

The camera goes round so the surface is genuinely three-dimensional, and the two loops are drawn on it: one going the long way round, one going through the hole. Combine them and you get the doughnut's higher holes. Stack more circles and the counts follow one fixed pattern, worked out in the lectures for any number of circles at once, including infinitely many ([Proposition 3.1, page 20](https://arxiv.org/pdf/2605.03658v1#page=20)).

![Bar charts of the hole counts of a stack of circles, for stacks of one up to six, each row the binomial pattern](ranks.png)

The bars are the hole counts by degree, recomputed in this repository. Every row is a row of Pascal's triangle, which is what the lectures' formula says: the holes of a stack of circles are exactly the ways of choosing some of the circles.

Two results then say the translation to answer sheets keeps all of this. First, counting holes inside the world of answer sheets gives the same numbers as counting them the classical way, for every compact shape ([Theorem 3.2, page 21](https://arxiv.org/pdf/2605.03658v1#page=21)). Second, if you count with smooth real-valued measurements instead of whole numbers, every hole count above the zeroth is zero ([Theorem 3.3, page 22](https://arxiv.org/pdf/2605.03658v1#page=22)); real-valued measurements are too flexible to notice a hole, and they simply report the continuous functions on the shape.

That second result sounds like a disappointment and is one of the most used facts in the subject. It says the real numbers are invisible to this kind of counting, and part two will spend a section on where they went.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/08.html)** to drag a loop around and count turns, then switch to the doughnut and count both.

---

[← Nothing was lost](../07-nothing-was-lost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

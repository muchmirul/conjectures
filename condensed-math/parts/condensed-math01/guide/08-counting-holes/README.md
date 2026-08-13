# 8 · Counting holes

*Part 1 of three: Shapes You Can Only See By Probing Them. Retells Lectures I to III of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The final check is whether the translation preserves topological features such as holes. A basic way to detect a hole in a circle is to draw a closed path and count how many times it travels around the centre. This count is the winding number, and it remains unchanged when the path is continuously deformed without being broken.

![A loop being dragged around a ring while a counter records how many whole turns it has made](winding.gif)

The animation computes the winding number of a closed path around the circle. This number is always an integer and records both the number of turns and their direction. A generator of the circle's first cohomology measures this winding, so the first cohomology group is one copy of the integers.

Products of circles create more independent directions for loops. The product of two circles is the surface of a torus, which has one loop around its central opening and another around the body of the tube.

![A rotating three-dimensional view of a doughnut surface carrying its two independent loops](torus.gif)

The rotating view makes the three-dimensional surface and its two independent loops visible. Products of more circles have higher-degree holes formed by choosing several circle directions at once. The lectures compute this pattern for any number of factors, including infinitely many ([Proposition 3.1, page 20](https://arxiv.org/pdf/2605.03658v1#page=20)).

![Bar charts of the hole counts of a stack of circles, for stacks of one up to six, each row the binomial pattern](ranks.png)

The chart shows the finite cases recomputed in this repository. Each row is a row of Pascal's triangle. For a product of several circles, the count in a given degree equals the number of ways to choose that many circle directions, exactly as the formula in the lectures predicts.

Two theorems connect this calculation to condensed mathematics. First, for every compact space, cohomology computed after translation to condensed sets agrees with classical cohomology ([Theorem 3.2, page 21](https://arxiv.org/pdf/2605.03658v1#page=21)). Second, when the coefficients are the usual real numbers rather than the integers, all positive-degree cohomology vanishes ([Theorem 3.3, page 22](https://arxiv.org/pdf/2605.03658v1#page=22)); degree zero records the continuous real-valued functions. This vanishing result is important later because it shows that the usual real line behaves very differently from the integer-based objects used in part two.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math01/play/08.html)** to change a loop's winding number and then compare the two independent loop directions on a torus.

---

[← Nothing was lost](../07-nothing-was-lost/README.md)  ·  [all of part 1 on one page](../../ARTICLE.md)

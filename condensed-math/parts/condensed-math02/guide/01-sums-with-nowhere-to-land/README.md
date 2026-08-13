# 1 · Sums with nowhere to land

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Part one repaired subtraction, but it did not add anything up. Consider adding one, then two, then four, then eight, doubling forever. In ordinary arithmetic the running totals are 1, 3, 7, 15, 31, and they run away, so the sum has no value.

Now measure size differently. Say a whole number is **small when it is divisible by a high power of two**, so 16 is smaller than 4, and 1024 is smaller still. This is a real and consistent notion of size, used constantly in number theory, and it is exactly the size the counting-in-base-two probe from part one carries.

![The running totals of the doubling sum, drawn twice: running away on the ordinary ruler, and closing in on a single point in the base-two probe](padic_walk.gif)

Under that size the running totals behave differently. The gaps between them are 2, 4, 8, 16, each one smaller than the last, and the totals close in on a single point. The animation shows both readings side by side: on the ordinary ruler the totals fly apart, and in the probe they nest into one box after another and converge.

![The distance from each running total to the limit, measured the ordinary way and the base-two way, one climbing and one halving](distance.png)

The chart is computed in this repository, in exact arithmetic. The ordinary distance doubles at every step, while the base-two distance halves at every step, and the point the totals close in on is minus one. Adding an endless string of positive numbers and getting minus one is not a trick, because the doubling sum genuinely converges to minus one under this size, and the tests here recompute both columns.

So the same endless sum has no answer under one notion of size and exactly one answer under another, and that is where the difficulty lies. An infinite sum is not a property of the numbers being added on their own, but a property of those numbers together with a decision about what near means, and that decision is precisely the topology that part one had to swallow into the answer sheet. The question of this part follows from that, since having swallowed the topology, we now need a way to get the infinite sums back out.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/01.html)** to change the base and the number of terms, and watch the two size readings disagree.

---

[← Start here](../00-start-here/README.md)  ·  [Weights that agree →](../02-weights-that-agree/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

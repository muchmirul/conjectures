# 5 · Four ways to count

The theorems ahead distinguish counts that sound alike, and most of the care in their statements sits in these distinctions. This chapter fixes the counts with one picture, and nothing in it is difficult.

Think of each zero as a pin stuck in the strip at its height. Four counters then move up the strip together through the same stretch of heights.

![A stretch of the strip with pins on and off the line, one doubled, and the four counters tallying them differently](pins.png)

**The full count** tallies every pin, and it counts a doubled pin twice. A doubled pin is a subtle possibility the theory must allow for: the landscape of chapter 2 could, in principle, touch the floor at one point in an extra-flat way, and such a point legitimately counts twice (or more). We will call an ordinary once-counting pin **a clean pin**, and the technical word for it is a *simple* zero. For the record, no doubled pin has ever been found either: every zero anyone has computed is clean and on the line.

**The distinct count** tallies pins as locations, so a doubled pin counts once. **The on-line count** tallies only pins on the line, again as locations. **The clean-line count** tallies only pins that are both on the line and clean.

By their definitions, the clean-line count can never exceed the on-line count, which can never exceed the distinct count, which can never exceed the full count. The full count is the one with a known formula: a stretch of heights contains a predictable number of pins (the counting formula of [equation 1.2, page 3 of the paper](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=3)), and the tests here verify that prediction against this repository's own table of computed zeros.

The 2026 paper's three headline theorems can now be said exactly, in this guide's words. Take an ever-higher stretch of heights, from any large height up to its double, and compare each counter with the full count. Then, in the limit:

> The on-line count is at least two thirds of the full count. So is the clean-line count. The distinct count is at least five sixths of the full count.

These are [Theorems A, B and C on pages 3 and 4 of the paper](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=3). "Unconditional" means: assuming nothing unproven, in particular not assuming the Riemann hypothesis.

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/05.html)** to place pins yourself and watch the four counters disagree.

---

[← The question](../04-the-question/README.md)  ·  [The microphones →](../06-the-microphones/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

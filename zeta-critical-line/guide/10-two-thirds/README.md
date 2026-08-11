# 10 · Two thirds

All the parts are now available, and nothing new is needed, because this chapter only adds them up, the way [section 6 of the paper](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=19) does.

Write the budget in units where the full count of zeros in the stretch is one. The rank-trace inequality of chapter 9 promises: clean on-line pins are at least twice the count, plus a term for the saddle bookkeeping that the see-saw law caps at twice the count again, minus the energy. Chapter 8 measured the count's total (one, in these units, times a factor of two from how the table's slots pair up) and the energy (four thirds). The assembly is three subtractions long:

![A waterfall chart: four, minus two, minus four thirds, leaving two thirds](budget.png)

Four, minus two, minus four thirds, leaves two thirds. That is the whole final step, and each block of the waterfall is a chapter of this guide: the four is the doubled count reading of the table (chapters 6 and 8), the minus two is the see-saw law's price for allowing saddles at all (chapter 7), and the minus four thirds is the measured energy (chapter 8) entering through the whole-number trick (chapter 9). The conclusion: in the limit, clean on-line pins are at least two thirds of the full count. This proves the guide's version of Theorems A and B at the natural dial setting. For Theorem C, the same inequality re-run with the count of *distinct* pins gives five sixths: each mirror pair, remember, still contains two genuinely distinct points, so distinctness is cheaper to certify than being on the line.

Two refinements complete the paper's headline numbers.

**The dial matters.** Run the whole argument at a different dial setting and each block of the budget changes: the shape of the result as a function of the dial is the paper's [equation 1.3, page 3](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=3). The chart below plots it: the certified proportion peaks exactly at the natural setting, dial equal to one, where it reads two thirds.

![The certified proportion as the dial turns, for on-line, distinct and the weaker certificate, peaking at dial one](dial.png)

**The window matters, a little.** The bump shape of chapter 6 was flat-topped for simplicity. Optimising the shape instead ([section 7.1, page 20](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=20)) leads to a gently curved cosine profile, and the constants improve to 0.6725 on the line and simple, and 0.83625 distinct. The optimal shape was already known: Montgomery and Taylor found the same test function in 1975 for the conditional version of this problem, and the paper proves that the 2026 machine reaches their constant without their hypothesis. This repository recomputes the optimising shape's score numerically and checks that nearby shapes do worse.

![The flat window and the optimised cosine window, with the constants each one certifies](window_race.png)

Finally, the same machine runs verbatim for close cousins of zeta: for the L-function of any fixed Dirichlet character, the paper's [Theorem E, page 22](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=22) gives the same constants, and for the derivative of the completed zeta function it certifies 0.85838 simple-and-on-the-line and 0.92919 distinct ([Remark 7.3, page 23](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=23)).

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/10.html)** to turn the dial and switch windows, and watch every constant respond.

---

[← The whole-number trick](../09-the-whole-number-trick/README.md)  ·  [The checks →](../11-the-checks/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

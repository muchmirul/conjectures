# 12 · Where things stand

The paper spends a full section, [1.5, page 5](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=5), stating what its results are not, and any honest account must lead with the same.

**It has no bearing on the Riemann hypothesis, in either direction.** The argument produces lower bounds only: it certifies that at least two thirds of the zeros are clean and on the line, and it says nothing about the remaining third. Those zeros are simply beyond this certificate's reach, and nothing in the result suggests they are off the line. The paper also notes that its inputs are too coarse to ever decide RH, because there exist other functions, long known, that satisfy every input the proof uses while their version of the hypothesis is false. This means a proof of RH must use more about zeta than this proof does.

**The method has a proven ceiling.** The paper proves its own limit ([Remark 1.1, page 4](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=4)): no certificate built from this data, the table's two totals at the natural dial, can ever certify more than 0.68185 of the zeros. The two thirds already sits within 0.016 of that ceiling, and the optimised 0.6725 within a hundredth, so the machine has been driven essentially as far as it goes. Reaching 0.70, 0.80 or 0.90 by this route would need pair-correlation knowledge at bandwidths around 1.04, 1.26 and 1.70, beyond what anyone can currently prove, and the full hypothesis would correspond to unlimited bandwidth.

![The proportion line from zero to one, with the old record, the new unconditional constants, the method's ceiling, and the untouched hypothesis marked](map.png)

```
    now known, unconditionally             still open
    ----------------------------           ----------
    at least 2/3 of the zeros are          whether all zeros are on the
    on the line, and clean                 line (the Riemann hypothesis)
    at least 5/6 are distinct              whether all zeros are clean
    with the best window: 0.6725           anything between 0.68185 and 1
    and 0.83625                            by this method: provably nothing
    the same for every Dirichlet
    L-function
```

Three conclusions are worth keeping. The first is that the state of knowledge moved: the best unconditional statement about where zeta's zeros live improved from five twelfths to two thirds, the largest single step since Levinson in 1974, and the companion counts (five sixths distinct, and the derivative's 0.929) moved with it. The second is that a fifty-year-old conditional theorem became unconditional: what Montgomery could prove in 1973 only by assuming RH, the see-saw law now delivers with no assumption, and the paper is candid that this, rather than any new arithmetic, is its real contribution. The third concerns how the result was produced: a mathematical result of record strength was found by a machine, doubted by the machine, attacked by the machine, formalised down to axioms, and only then handed to people. The paper took unusual care that the question of whether the result is true would not depend on the question of who wrote it.

The question itself remains where Riemann left it. Two thirds of the wobble's frequencies are now proved to sit on the line. The remaining third lie somewhere in the strip, all of them on the line as far as any computer has looked and none of them proven to be, and the oldest question in analytic number theory is exactly as open as it was in 1859.

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/12.html)** to walk the proportion line and see what each mark would take to move.

---

[← The checks](../11-the-checks/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

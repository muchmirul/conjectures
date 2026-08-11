# 12 · What it means, and what it does not

The paper spends a full section, [1.5, page 5](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=5), stating what its results are not, and any honest account must lead with the same.

**It has no bearing on the Riemann hypothesis, in either direction.** The argument produces floors, never ceilings: it certifies that at least two thirds of the zeros are clean and on the line, and about the remaining third it says nothing at all. Those zeros are not shown to be off the line; they are simply beyond this certificate's reach. More pointedly, the paper notes that its inputs are too coarse to ever decide RH: there exist other functions, long known, that satisfy every input the proof uses while their version of the hypothesis is false. A proof of RH must use more about zeta than this proof does.

**The method has a hard ceiling, and knows it.** The paper proves its own limit ([Remark 1.1, page 4](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=4)): no certificate built from this data, the table's two totals at the natural dial, can ever certify more than 0.68185 of the zeros. The two thirds already sits within 0.016 of that ceiling, and the optimised 0.6725 within a hundredth, so the machine has been driven essentially as far as it goes. Reaching 0.70, 0.80 or 0.90 by this route would need pair-correlation knowledge at bandwidths around 1.04, 1.26 and 1.70, beyond what anyone can currently prove; the full hypothesis would correspond to bandwidth infinity.

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

What should a reader take from it? Three things, roughly. First, the state of knowledge moved: the best unconditional statement about where zeta's zeros live improved from five twelfths to two thirds, the largest single step since Levinson in 1974, and the companion counts (five sixths distinct; the derivative's 0.929) moved with it. Second, a fifty-year-old conditional theorem became unconditional: what Montgomery could see in 1973 only through the lens of RH, the see-saw law now delivers with no lens. The paper is candid that this is its real contribution: not new arithmetic, but a new, assumption-free way of reading arithmetic that was already there. Third, the sociology: a mathematical result of record strength was produced by a machine, disbelieved by the machine, attacked by the machine, formalised down to axioms, and only then handed to people. Whatever one thinks that means, the paper took unusual care that the question "is it true?" would not depend on the answer to "who wrote it?".

The wobble of the primes, meanwhile, keeps its secret. Two thirds of its frequencies are now pinned to the line forever. The rest still hum somewhere in the strip, all of them on the line as far as any computer has ever looked, none of them proven to be, and the oldest question in analytic number theory is exactly as open as it was in 1859.

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/12.html)** to walk the proportion line and see what each mark would take to move.

---

[← The checks](../11-the-checks/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

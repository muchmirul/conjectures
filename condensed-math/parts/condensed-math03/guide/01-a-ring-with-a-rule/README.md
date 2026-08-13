# 1 · A ring with a rule for sums

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

Part two attached a rule for infinite sums to the whole numbers. This section says what that rule is in general, so it can be attached to anything.

A ring is a place where you can add, subtract and multiply, while part two's rule was about adding only. The question now is what the same service looks like over a ring: given a probe, and a placement of the probe's points into a module over the ring, we want to integrate weightings against the placement.

The general notion needs two pieces of data ([Definition 7.1, page 45](https://arxiv.org/pdf/2605.03658v1#page=45)):

**The ring**, taken as an answer sheet in the sense of part one. Being an answer sheet is what lets it carry a topology without that topology sitting outside the algebra.

**A rule**, which for each probe hands back the module of legal weightings on it. The rule also has to meet one requirement, that every point of the probe already counts as a weighting, namely the unit sitting on that point alone.

![A ring beside its rule: for each probe the module of weightings the ring allows, with each point of the probe entering as a unit weight](measures.png)

Those two pieces of data are not yet enough on their own. The pair must be well behaved, meaning roughly that the modules it produces really do form a self-contained world of their own, the way solid groups did in part two. A pair passing that test is called an **analytic ring** ([Definition 7.4, page 46](https://arxiv.org/pdf/2605.03658v1#page=46)), and this guide will simply say *a ring with a rule*.

The definition is short, and all of its content sits in which pairs pass. It is genuinely possible to write down a ring and a plausible-looking rule that fails, and section 3 is about the most important such failure.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/01.html)** to assemble a rule and watch the requirements be checked one at a time.

---

[← Start here](../00-start-here/README.md)  ·  [Two rules that work →](../02-two-that-work/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

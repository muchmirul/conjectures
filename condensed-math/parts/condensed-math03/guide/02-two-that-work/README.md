# 2 · Two rules that work

*Part 3 of three: Rings That Know How To Integrate. Retells Lectures VII to XI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The first examples require no new construction because they come from the solid measures of part two. They show how the general definition packages familiar completion rules.

**The base-p rule.** Use the p-adic integers as the ring and compatible p-adic-valued measures on each probe as its free complete modules. This pair passes the analytic-ring test ([Proposition 7.8, page 48](https://arxiv.org/pdf/2605.03658v1#page=48)), so p-adic summation fits the new framework.

**The solid rule over a plain ring.** Let A be any discrete ring and extend the integer-valued solid measures by coefficients in A. This pair also passes. It supplies a theory of complete A-modules even though the underlying ring itself has no nontrivial topology.

![The two working rules side by side, the base-p one and the solid one over a plain ring, with what each allows you to sum](two_rules.png)

The second example may initially seem empty because a discrete ring has no limits to complete inside the ring itself. However, the rule governs condensed modules over that ring, not merely its individual elements. Those modules can carry rich topological information through their probe values. The theory selects the modules in which solid measures can be integrated consistently, while keeping the coefficient ring algebraically simple.

This separation is useful in geometry. The ring describes multiplication of functions, while the theory of measures controls infinite additive behaviour in its modules. Since these roles are independent, one can alter the completion rule without changing the underlying algebraic formulas.

A broader construction begins with a ring A and a chosen subring of elements regarded as having size at most one ([Remark 7.9, page 49](https://arxiv.org/pdf/2605.03658v1#page=49)). Such a pair is called a Huber pair. For the field of p-adic numbers, it produces the bounded p-adic-valued measures. Section 6 will use Huber pairs to turn local rings into geometric patches.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math03/play/02.html)** to compare the p-adic and discrete-ring rules and see which measures each one permits.

---

[← A ring with a rule for sums](../01-a-ring-with-a-rule/README.md)  ·  [The real line's own rule →](../03-the-real-lines-own-rule/README.md)  ·  [all of part 3 on one page](../../ARTICLE.md)

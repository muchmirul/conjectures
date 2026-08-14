# 6 · Where the real line goes

*Part 2 of three: Infinite Sums That Finally Land. Retells Lectures IV to VI of Scholze's [Lectures on Condensed Mathematics](https://arxiv.org/abs/2605.03658).*

The solidification of the usual real numbers is zero. This is Corollary 6.1 (iii) of the lectures ([Corollary 6.1 (iii), page 42](https://arxiv.org/pdf/2605.03658v1#page=42)). A simple divisibility argument explains why zero is the expected result, although the full theorem requires more than that argument alone.

![Repeated division remains inside the real numbers but eventually leaves the integers](divisible.gif)

Every real number can be divided by any positive integer and remain a real number. An abelian group with this property is called **divisible**. The integers do not have it, because an integer such as one cannot be divided by two while staying inside the integers. The animation contrasts these two behaviours.

Now consider a homomorphism from the additive real numbers to one copy of the integers. If a real number is divisible by every positive integer, its image must have the same property because homomorphisms respect addition and division relations. The only integer divisible by every positive integer is zero. Every such homomorphism is therefore zero, and the same coordinate-by-coordinate argument applies to a product of integer groups.

![A map from the divisible real group to each integer coordinate is forced to have value zero](no_map.png)

This argument shows that the real line maps trivially into the projective building blocks of the solid category. It does not by itself prove that solidification sends the real line to zero. That stronger conclusion also uses the universal-resolution calculation from Lecture IV ([Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25)), after which the stated vanishing follows.

**This does not make the real numbers unimportant.** The solid rule in this part is designed for nonarchimedean notions of size, such as the p-adic size from section 1, where high divisibility means smallness. The ordinary real absolute value behaves differently and requires a different theory of measures. The lectures note this when solidity is introduced ([page 33](https://arxiv.org/pdf/2605.03658v1#page=33)), and part three explains the real-valued replacement.

**The vanishing also has a mathematical use.** Real-valued correction terms disappear from certain condensed calculations instead of creating obstructions. Part one encountered a related result when higher cohomology with real coefficients vanished. The computation in Lecture IV uses this behaviour ([Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25)), and that computation supports the structure theorem for solid groups.

### The mathematics

Divisibility is the property used in this chapter. An abelian group $D$ is divisible when

```math
\forall x\in D,\ \forall n\ge1,\ \exists y\in D\text{ such that }ny=x.
```

Every homomorphism from a divisible group to an integer product is zero:

```math
\operatorname{Hom}\!\left(D,\prod_{i\in I}\mathbb Z\right)=0.
```

The usual additive real line is divisible. For this group, [Corollary 6.1 (iii), page 42 of the lectures](https://arxiv.org/pdf/2605.03658v1#page=42) gives the stronger derived statement

```math
\mathbb R^{L\blacksquare}=0.
```

**Reading the symbols.** The letter $D$ names an abelian group. The symbols $\forall$ and $\exists$ mean “for every” and “there exists.” The relation $x\in D$ says that $x$ belongs to $D$, and $n\ge1$ chooses any positive integer. The equation $ny=x$ means that adding $y$ to itself $n$ times gives $x$. The product sign denotes an arbitrary row of integer groups indexed by $I$. The equation $\operatorname{Hom}=0$ says that every additive map to that product is the zero map. The superscript $L\blacksquare$ means derived solidification, and its value $0$ is the zero object.

**Why it matters.** The divisibility argument proves that the reals map trivially to every compact projective building block of the solid category. The full vanishing $\mathbb R^{L\blacksquare}=0$ also uses [Theorem 4.3, page 25](https://arxiv.org/pdf/2605.03658v1#page=25), so the simulation is an explanation of the obstruction rather than a proof of the corollary.

**In the simulation.** The group selector chooses $D$, and the divisions control chooses values of $n$. The real line always supplies a $y=x/n$, while the integers eventually cannot. The final readout shows the consequence for maps into one product coordinate.

**[Play with this](https://muchmirul.github.io/conjectures/condensed-math/condensed-math02/play/06.html)** to divide elements repeatedly and compare divisible groups with the integers.

---

[← The solid rule](../05-the-solid-rule/README.md)  ·  [The multiplication table →](../07-the-multiplication-table/README.md)  ·  [all of part 2 on one page](../../ARTICLE.md)

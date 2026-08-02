# 4 · The certificate

Before defining a certificate, choose the unit of distance so that every ball has diameter one. Resizing the whole packing does not change the fraction of space it fills. With that choice made, a certificate is a function: give it the distance between two ball centres, and it returns a number.

The function must pass two rules.

**Rule one.** At distance one and beyond, its value must always be zero or negative.

**Rule two.** A second view of the function, called its **Fourier transform**, must always be zero or positive.

The name “Fourier transform” can sound more difficult than the picture. A changing curve can be described as a mixture of simple waves. The Fourier transform tells us how much of each wave is present. The original curve and this list of waves are two views of the same information, just as a musical chord and the notes inside it describe the same sound.

![A certificate shown as its original curve on the left and its Fourier view on the right](rules.png)

The left panel shows the original function. In the shaded region, which begins at distance one, the curve stays on or below the zero line. That is rule one. The right panel shows its Fourier transform staying on or above the zero line. That is rule two.

Either rule is easy to satisfy by itself. It is easy to draw a curve that stays negative after distance one, and it is easy to draw a curve whose Fourier view stays positive. Satisfying both at the same time is difficult. A sharp change in one view usually spreads out and produces ripples in the other, so improving one side can break the other.

The next picture shows a basic function that passes both rules.

![A basic certificate made from a simple curve that fades away like a bell](simple.png)

This function qualifies as a certificate in dimensions one through six, but it gives useful information only in dimensions four and five. In the plane, for example, its density limit is greater than 100 percent. We already know that no packing can fill more than 100 percent, so that limit tells us nothing new. In dimension seven, its Fourier view becomes negative and the function no longer qualifies as a certificate.

The next animation changes one part of a working certificate. Watch the Fourier view as the control moves.

![A control changing the function until its Fourier view crosses below zero](tuning.gif)

Once any part of the Fourier view falls below zero, rule two fails. Even a small failure means the function can no longer prove a density limit.

A function that passes both rules produces a number that no packing in that dimension can exceed. The next section explains where that number comes from.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/04.html)** to adjust a certificate and see exactly when one of its rules breaks.

---

[← Why you cannot just check](../03-cannot-check/README.md)  ·  [Counting twice →](../05-count-twice/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

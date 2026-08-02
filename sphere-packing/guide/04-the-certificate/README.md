# 4 · The certificate

A certificate is one function. Feed it a distance and it hands back a number, and it has to obey two rules.

**Rule one.** From distance one outward, the number it hands back is never above zero.

**Rule two.** Its **Fourier transform** is never below zero, anywhere.

The Fourier transform is the second character in this story, so here is what it is. Any function can be built by adding up waves of different frequencies. The Fourier transform is the recipe: it tells you how much of each frequency you need. A function and its transform are two views of one object, the way a chord and its list of notes are two views of one sound.

![A certificate: the function on the left, its transform on the right, with both rules drawn](rules.png)

The left panel is the function. The shaded band is where rule one applies, and the curve dips below zero exactly where it must. The right panel is the transform, which stays at or above zero the whole way.

Both rules are easy on their own. A function that is negative from distance one out is easy to write. A function whose transform is never negative is easy to write. The difficulty is that the Fourier transform pushes back: making a function drop sharply in one view makes it spread out and wobble in the other. Getting both at once is the entire game.

Here is the simplest thing that obeys both.

![The simplest certificate: one minus the distance squared, times a bell curve](simple.png)

It obeys both rules, and it is nearly worthless. In the plane the number it hands back is above one, and every density is below one anyway, so it says nothing. It only starts saying something true in dimensions four and five, and it stops existing entirely at dimension seven, where its transform can no longer be kept positive.

Turn one dial on a working certificate and watch what happens.

![Turning a dial until the transform dips below zero and the certificate stops proving anything](tuning.gif)

Past a point the transform goes negative, rule two breaks, and the certificate proves nothing at all.

Once you have a function obeying both rules, it hands you a number, and no packing in that dimension can be denser than that number. The next section says why.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/04.html)** and turn the idea over yourself.

---

[← Why you cannot just check](../03-cannot-check/README.md)  ·  [Counting twice →](../05-count-twice/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

# 5 · Counting twice

Take any packing and any certificate. Add up the certificate's value over every pair of ball centres.

![Adding over pairs of centres, then over frequencies instead](two_counts.gif)

Do the sum in the ordinary way, over pairs of centres, and rule one takes over. Two different centres are always at least distance one apart, because the balls do not overlap. Out there the certificate is at or below zero. So every pair except a centre with itself can only drag the total down.

Now do the same sum in the other view, over frequencies. This is where the Fourier transform earns its place: there is an identity, Poisson summation, that says the sum over centres and the sum over frequencies are the same number. In that view rule two takes over, every term is at or above zero, and the total can only be pushed up.

```
    pairs of centres  --->   one total   <---  frequencies
    push it down                              push it up

    the packing is caught between them,
    and that trap is the density bound
```

One number, squeezed from both sides. Rearranging the squeeze gives a ceiling on the density, and that ceiling depends only on the certificate, never on the packing. That is the Gorbachev and Cohn-Elkies bound, from 2000 and 2003.

The word "linear program" in the title of the source paper is the name for this kind of setup: a best value being hunted subject to a list of constraints that are all of this simple sign type.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/05.html)** and turn the idea over yourself.

---

[← The certificate](../04-the-certificate/README.md)  ·  [What certificates actually prove →](../06-best-so-far/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

# 12 · What it means, and what it does not

Be careful about what was settled. The method now has a known ceiling. The packing problem does not.

```
    settled                                still open
    -------                                ----------
    the exact rate of the method           the true densest packing in
    the best exponent since 1978 replaced  most dimensions
    both sign uncertainty constants        whether any method beats this
                                           exponent
                                           the gap between what is built
                                           and what is proved
```

Nobody has found a packing in high dimensions that comes anywhere near the new bound, and the gap between the best construction and the best bound is still exponentially wide. What changed is that one particular route is now fully mapped: we know exactly how far it goes, so improving on it requires a different idea.

```
    1611  Kepler guesses the greengrocer's stack cannot be beaten
    1978  Kabatianskii and Levenshtein prove the exponent 0.59905576
    2000  Gorbachev, and independently Cohn, write down the method
    2003  Cohn and Elkies publish it and compute with it
    2005  Hales's proof of the Kepler conjecture appears in print
    2014  Cohn and Zhao: the method is at least as strong as the 1978 bound
    2017  Viazovska settles dimension 8; with Cohn, Kumar, Miller and
          Radchenko, dimension 24
    2020  Afkhami-Jeddi, Cohn, Hartman, de Laat and Tajdini conjecture the rate
    2026  the rate is proved, and 0.6044005442916777 replaces the 1978 exponent
```

The same proof settles two other questions, about how early a Fourier eigenfunction can settle down to a fixed sign. There are two versions, one for functions that transform into themselves and one for functions that transform into minus themselves. Both were conjectured to have the same limit, and the proof confirms it: both are one over pi, times the square root of the dimension.

![The two radii drawn as circles closing on the shared dashed limit circle, the plus one always inside; the spacing sketches the trend rather than exact values](two_radii.png)

The source also observes something the limit hides. In every single dimension the two radii are different, and the plus version is always the smaller. Their limits agree; the quantities themselves never do.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/12.html)** and turn the idea over yourself.

---

[← The two halves meet](../11-they-meet/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

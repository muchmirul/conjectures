# 12 · What it means, and what it does not

The 2026 result settles the limit of one method. It does not settle the sphere-packing problem in most dimensions.

```
    now known                              still unknown
    ---------                              -------------
    the exact long-term rate of this       the densest packing in most
    certificate method                     dimensions
    the improved general upper-limit rate  whether a different method can give
    that replaces the 1978 rate            a better long-term upper limit
    the two related Fourier sign limits    how to close the gap between packings
                                           we can build and limits we can prove
```

No known high-dimensional packing comes close to the new upper limit. The gap between the best construction and the best proven limit is still exponentially wide, which means their ratio grows by repeated factors as dimensions are added. The advance maps one route completely: we now know exactly how far this certificate method can go, so a better long-term rate will need a different idea.

```
    1611  Kepler proposes that the fruit-shop stack cannot be beaten
    1978  Kabatianskii and Levenshtein obtain the rate 0.59905576
    2000  Gorbachev publishes the Fourier certificate method
    2002  Cohn independently develops the same method
    2003  Cohn and Elkies publish it together and calculate new limits
    2005  Hales’s proof of Kepler’s three-dimensional claim appears in print
    2014  Cohn and Zhao show the method is at least as strong as the 1978 rate
    2017  Viazovska settles dimension 8; with Cohn, Kumar, Miller and
          Radchenko, she also helps settle dimension 24
    2020  Afkhami-Jeddi, Cohn, Hartman, de Laat and Tajdini predict the exact rate
    2026  a proof establishes the rate, and 0.6044005442916777 replaces the
          1978 exponent
```

The proof also answers two closely related questions about functions and their Fourier transforms. Some special functions turn into themselves under the Fourier transform; others turn into their own negative. These are the plus and minus versions of a **Fourier eigenfunction**. For each version, ask how far from the centre we must go before the function settles to one fixed sign and never changes sign again.

Both versions were expected to approach the same radius in high dimensions. The proof confirms this. For each one, the limiting radius is one over pi times the square root of the dimension.

![The plus and minus radii approaching the same dashed limit, with the plus radius always smaller; the spacing shows the trend rather than exact values](two_radii.png)

The shared limit does not mean the two radii are equal in any particular dimension. The source shows that the plus radius is smaller in every finite dimension. Their difference becomes small compared with the square root of the dimension, so only their long-term limits agree.

---

[← The two halves meet](../11-they-meet/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

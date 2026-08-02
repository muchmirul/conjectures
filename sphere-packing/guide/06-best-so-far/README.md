# 6 · What certificates actually prove

This repository contains a small search that hunts for good certificates. Starting from an easy one and nudging it at random, it finds these. In the picture, space is a tube being filled from the floor: blue is how full the best known packing really makes it, and everything above the certificate's ceiling is proved unreachable.

![Space drawn as a tube being filled, with the thin unknown sliver between what is reached and what is impossible magnified beside it](gap.png)

In the plane it proves that no packing of circles beats 91.16 percent. The staggered rows reach 90.69 percent. Those two numbers are less than half a percentage point apart, a sliver too thin to see at true scale, which is why the picture magnifies it. Everything that is still unknown about circle packing lives inside that sliver.

Two honest notes about that. The sign rules here are checked by sampling a fine grid, not proved symbolically, so this is a numerical certificate rather than a formal proof. And it is much weaker than what specialists get: they use semidefinite programming and force the function to have roots in chosen places, and none of that is implemented here.

The search also fails in an instructive way. Its starting family of functions stops existing before dimension six, so in dimension eight it cannot even begin. Dimension eight is exactly where Viazovska's function lives, and building it took the mathematics of modular forms.

```
    dimensions 8 and 24     the certificate is known exactly, and it is sharp
    dimensions 1, 2, 3      the best packing is known, the certificate is not sharp
    every other dimension   neither the best packing nor the best certificate is known
    as the dimension grows  the best certificate is now known: the 2026 result
```

In dimensions eight and twenty four the best certificate is known and it is exactly right, which is why those two dimensions are settled. Everywhere else there is a gap between what can be built and what can be proved impossible.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/06.html)** and turn the idea over yourself.

---

[← Counting twice](../05-count-twice/README.md)  ·  [Is there a ceiling on the method? →](../07-the-ceiling/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

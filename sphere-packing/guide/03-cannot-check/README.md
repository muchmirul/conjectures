# 3 · Why you cannot just check

Trying many arrangements can help us find a good packing, but it can never confirm that we have found the best one. The next picture shows several different ways of arranging equal circles.

![Six possible circle arrangements that show how many different choices there are](many_packings.png)

There are endlessly many ways to place the balls, and there is no checklist that contains them all. One arrangement can show that a particular density can be reached, which is called a lower bound, but it cannot show that every other arrangement is worse. For that we need an upper bound, meaning one statement that applies to all possible packings at once.

The rest of the guide explains how a single number-making rule can provide such a statement. The two ways of working compare like this:

```
    trying arrangements one by one      using one certificate
    --------------------------------    ---------------------
    test one arrangement                choose one function
    test another                        make it pass two rules
    keep testing
    there is no final test              get a limit for every packing at once
```

We will call this function a **certificate**, because passing its two rules certifies a density limit. The usual mathematical name appears in the glossary near the end.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/03.html)** to compare what examples can show with what a certificate can show.

---

[← The room runs out](../02-room-runs-out/README.md)  ·  [The certificate →](../04-the-certificate/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

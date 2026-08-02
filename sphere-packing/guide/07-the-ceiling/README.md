# 7 · Is there a ceiling on the method?

In high dimensions, these density limits are compared by how quickly they shrink as the dimension grows. Once the dimension is very large, the main part of each limit behaves like multiplying by the same fraction whenever another dimension is added. The next picture represents that repeated shrinking with squares. Each square has a fixed fraction of the area of the previous one.

![Two models of repeatedly shrinking limits, using the rates from 1978 and 2026](exponents.png)

At first glance, the two rows look the same. A useful way to compare them is to ask how much of a halving happens per added dimension. A larger number is better because it means the upper limit becomes smaller more quickly. Kabatianskii and Levenshtein obtained 0.59906 halvings per dimension in 1978. That rate remained the best general result for forty-eight years.

The difference made in 2026 begins only in the fourth decimal place, but it is repeated across every dimension. The animation lets that repeated difference build up. The grey disc keeps the 1978 value at a fixed display size. The green disc shows the 2026 value at the same scale as the dimension rises.

![The 2026 rate becoming smaller than the 1978 rate as the dimension rises to one thousand](advantage.gif)

If we use only these long-term rates to compare dimension one thousand, the 2026 value is about 40.6 times smaller than the 1978 value.

This leads to the main question behind the 2026 work. Researchers had found increasingly good certificates for about twenty years, but could the method keep improving forever? Answering that requires two separate results.

```
    build one certificate near a rate   shows the method can reach that rate
    rule out all better certificates    shows the method cannot pass that rate

    the exact limit is known only when both statements meet
```

A good example proves what the method can achieve. A limit that applies to every possible certificate proves what the method cannot achieve. The second task is especially difficult because it must cover functions that nobody has found or written down.

In 2020, Afkhami-Jeddi, Cohn, Hartman, de Laat and Tajdini calculated the rate they expected and stated it as a conjecture. In 2026, both required statements were proved.

---

[← What certificates actually prove](../06-best-so-far/README.md)  ·  [The balancing trick →](../08-balancing/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

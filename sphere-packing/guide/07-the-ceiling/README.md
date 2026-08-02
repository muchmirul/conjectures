# 7 · Is there a ceiling on the method?

Every bound of this kind shrinks by a fixed factor for each dimension you add. The honest picture of such a bound is a row of squares, each square a fixed fraction of the area of the one before. The next figure draws one row for the 1978 rule and one for the 2026 rule.

![Two rows of shrinking squares, one for the 1978 rule and one for the 2026 rule, too alike for the eye to separate](exponents.png)

The two rows look identical, and that is the honest first impression. Because the factor is fixed, the natural way to compare two bounds is to ask how many halvings each is worth per dimension, and bigger is better, because it means the bound shrinks faster. The 1978 figure was 0.59906 halvings per dimension, from Kabatianskii and Levenshtein. It stood for forty eight years.

A difference in the fourth decimal place sounds like nothing. It is a difference in a rate, so it compounds, and the next animation lets it. The gray disc is the 1978 ceiling held at a fixed size for comparison; the green disc is the 2026 ceiling drawn to scale beside it, area for area, as the dimension climbs.

![The 2026 ceiling shrinking against the fixed 1978 one as the dimension counter climbs to one thousand](advantage.gif)

By dimension one thousand the new bound is about 40.6 times smaller than the old one.

Now the question this article has been building towards. Certificates can be improved, and people had been improving them for twenty years. Is there a best one? And if there is, what does it prove?

```
    find one certificate         shows the method can reach the rate
    rule out every certificate   shows the method can do no better

    only both together say what the method is worth
    the second is the hard half, and it is what 2026 added
```

Finding one good certificate shows the method can reach some rate. Ruling out every certificate shows it can do no better. The second half is where all the difficulty is, because it has to say something about functions nobody has written down.

In 2020 Afkhami-Jeddi, Cohn, Hartman, de Laat and Tajdini worked out what they believed the answer was and conjectured it. In 2026 both halves were proved.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/07.html)** and turn the idea over yourself.

---

[← What certificates actually prove](../06-best-so-far/README.md)  ·  [The balancing trick →](../08-balancing/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

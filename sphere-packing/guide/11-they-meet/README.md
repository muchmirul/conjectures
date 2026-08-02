# 11 · The two halves meet

**The proof, completed.** The two halves are combined, and the exact rate falls out.

One part of the proof says that no certificate can have a better long-term radius than the limit. The other part builds certificates whose radii approach that same limit. Either statement alone leaves room for a gap. Together, they show that the limit is exact.

![The impossible side and the constructed side closing on the same limiting number](closing.gif)

The speed of the two moving sides is chosen only to make their meeting easy to see. It does not represent the proof’s exact step-by-step error.

One standard estimate is still needed to turn a radius into a density. It is called Stirling’s formula, and here it gives a reliable description of the volume of a ball when the dimension is very large. Applying it to the ball volumes from section 2 makes the parts that still change with the dimension cancel, leaving one fixed rate.

```
    multiplying factor per dimension    0.6577446234794570
    the same rate in halvings            0.6044005442916777
    radius per square root of dimension  0.3183098861837907

    these are three descriptions of the same long-term result
```

The middle number is the easiest one to compare with earlier work: **0.6044005442916777** halvings per dimension. In the long run, each added dimension contributes about that much of a halving to the density limit. The 1978 value was 0.59905576.

This is the first improvement to the general sphere-packing exponent since 1978. “Exponent” is the standard name for this long-term shrinking rate. Because the other half of the proof rules out every better certificate, no certificate using these two sign rules can improve that rate again.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/11.html)** to bring the constructed and impossible sides together at one value.

---

[← Building the witness](../10-the-witness/README.md)  ·  [What it means, and what it does not →](../12-what-it-means/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

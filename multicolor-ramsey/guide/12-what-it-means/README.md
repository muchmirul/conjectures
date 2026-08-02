# 12 · What it means, and what it does not

The 2026 theorem can now be stated in the guide's plain language. For every colour count from two upward, there is a safe table whose people-per-colour score is at least one fixed positive constant times the cube root of the colour count, divided by its logarithm. The same constant works for every colour count.

That score grows without bound. Erdős's 100-dollar question asked whether the long-term score was finite, and the answer is no. His 250-dollar question asked what it approaches, and the answer is infinity.

Combine this construction with the factorial upper limit from section 6. The forcing size now has the same broad shape from both sides: the colour count is raised to a power proportional to the colour count. The lower result gives roughly one third of the colour count in that power, apart from slowly growing corrections. The upper result gives roughly the full colour count.

![The 2026 lower growth shape and the factorial upper growth shape, with the space between them still open](sandwich.png)

This chart compares the shapes of the two limits rather than exact values at a particular colour count. The result settles the type of growth, but not every detail.

```
    now known                              still open
    ---------                              ----------
    the people-per-colour score has        where the true power lies between
    no fixed ceiling                       the lower result's one third and the
    the forcing size has the colour        upper result's one
    count raised to a multiple of the      the four-colour forcing size remains
    colour count                           between 51 and 62
```

The scale of the theorem also matters. Its printed constant is extremely small because its denominator is enormous. The authors focused on proving the long-term shape rather than improving that number. With the printed constant, the new construction does not beat the old 3.28 score until around ten to the sixtieth colours. Below 342 colours, its numerical bound says nothing beyond the trivial fact that a safe group exists. At every size anyone could draw or compute directly, the older constructions give bigger tables. The advance is about what eventually becomes possible, not a new small-colour record.

The result also answers a question about sending messages through noise. The next picture begins with five symbols arranged in a ring. Neighbouring symbols can be confused with each other.

![Five noisy symbols and five two-letter codewords that carry more safe messages than single symbols](channel.png)

With one use of this channel, at most two symbols can be chosen so that every pair is clearly distinguishable. With two uses, five two-letter words can be chosen so that every pair differs safely in at least one position. Five messages over two uses is a better rate per use than two messages over one use.

The **capacity** of a noisy channel asks for the best message rate when words can be very long. Safe colourings and these channel codes are two forms of the same structure: people correspond to messages, and colours provide positions where pairs can be told apart. The 2026 result therefore creates channels in which every three symbols include a pair that may be confused, while the long-word capacity can still be as large as desired. Before this result, nobody knew whether such channels existed.

```
    1955  Greenwood and Gleason settle the two- and three-colour cases
    1971  Erdős, McEliece and Taylor connect the game with channel capacity
    1973  Chung proves that four colours can keep at least fifty people safe
    1983  Chung and Grinstead's survey records Erdős's prizes
    1990  Graham, Rothschild and Spencer record the growth question
    1995  Alon and Orlitsky make the channel connection explicit
    2021  addition-based recipes reach the best fixed score, about 3.28
    2026  the people-per-colour score is proved to grow without bound
```

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/12.html)** to compare the old and new rates and explore the noisy-channel example.

---

[← The tower](../11-the-tower/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

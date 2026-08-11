# 1 · The primes

A prime is a whole number bigger than one that only breaks into pieces the trivial way: 7 is prime, 6 is not, because 6 is 2 times 3. Primes are the atoms of multiplication. Every whole number is a product of primes in exactly one way, so whatever the primes do, all numbers inherit.

What the primes do is thin out, irregularly. There are 25 of them below 100, but only 21 in the next hundred, and 16 in the hundred after that. The picture below counts them: each step up is one new prime.

![The prime-counting staircase up to one hundred, climbing by one at every prime](staircase.png)

The steps come at uneven moments. Sometimes two primes arrive almost together, like 71 and 73; sometimes there is a long silence, like the eight-number gap after 89. Nobody has ever found a simple rule for the next step, and it is known there is no simple rule to find.

Zoom out, though, and the staircase smooths into a gentle curve. In 1792, aged fifteen, Gauss guessed a formula for that curve, and his guess is astonishingly good. The next picture subtracts the guess from the true count, leaving only the difference.

![The difference between the true prime count and Gauss's smooth guess, wobbling around zero up to ten thousand](wobble.png)

What is left is a wobble: the gap between truth and guess wavers irregularly, in waves with no obvious period. (In this whole range the true count runs slightly under the guess; Littlewood proved in 1914 that the gap nevertheless flips sign infinitely often, the first flip lying unimaginably far out. The quoted theorems in this paragraph and the last are classical, and the chart itself is recomputed by this repository.) This wobble is the whole subject of this guide. The zeta function's zeros turn out to be, quite literally, the frequencies of these waves, and every question about how far the primes can stray from the smooth curve becomes a question about where the zeros sit.

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/01.html)** to walk the staircase and compare it with the smooth guess.

---

[← Start here](../00-start-here/README.md)  ·  [Riemann's map →](../02-riemanns-map/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

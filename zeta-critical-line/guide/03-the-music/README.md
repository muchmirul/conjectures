# 3 · The music of the primes

Riemann's discovery is that the zeros and the primes are two descriptions of one thing, the way a chord and its notes are. There is an exact formula, called the explicit formula, that turns the list of zeros into the prime staircase and back. This guide will not write the formula; it will show it working.

Each zero contributes one wave. The zero's height sets the wave's frequency: a zero at height 14.13 contributes a wave that oscillates 14.13 fast on a logarithmic ruler. Here is the first zero's wave on its own.

![The single wave contributed by the first zero, oscillating with slowly growing amplitude](one_wave.png)

One wave explains nothing by itself. But add the waves of the first zero, the first two, the first five, twenty, one hundred, and watch what the sum converges to.

![Waves from more and more zeros being added to a smooth ramp until the sum reproduces the prime staircase](waves.gif)

The sum walks itself into the staircase, corners and all. (The staircase in this figure is a standard weighted variant of the prime count, chosen because its formula is the cleanest; its steps land on primes and their powers, and its wobble is the same wobble.) This is not an approximation trick invented for the picture; it is the mathematical identity at the centre of the whole subject, and the tests in this repository check that adding more waves really does shrink the error. The zeros are the music the primes dance to.

The duet also plays in the other direction: summing a wave for every prime points back at the zeros. That reverse direction is how the 2026 paper listens to zeros it cannot see, and chapter 8 plays it.

One more thing matters here. How loud each zero's wave sounds depends on where the zero sits sideways. A zero on the line contributes the quietest possible wave, one whose loudness stays balanced forever. A mirror pair off the line would contribute a wave that grows louder, and the further off the line, the faster the growth. The Riemann hypothesis is therefore exactly the statement that the prime wobble stays as quiet as it can possibly be.

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/03.html)** to add the zero-waves one at a time yourself.

---

[← Riemann's map](../02-riemanns-map/README.md)  ·  [The question →](../04-the-question/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

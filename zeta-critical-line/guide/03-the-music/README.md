# 3 · The music of the primes

Riemann's discovery is that the zeros and the primes are two descriptions of one thing, the way a chord and its notes are. There is an exact formula, called the explicit formula, that turns the list of zeros into the prime staircase and back. Instead of writing the formula, this guide shows it working.

Each zero contributes one wave, and the zero's height sets the wave's frequency: a zero at height 14.13 contributes a wave that oscillates 14.13 fast on a logarithmic ruler. The picture below shows the first zero's wave on its own.

![The single wave contributed by the first zero, oscillating with slowly growing amplitude](one_wave.png)

One wave on its own explains very little. The animation therefore adds the waves of the first zero, then the first two, the first five, twenty, and one hundred, and shows what the sum converges to.

![Waves from more and more zeros being added to a smooth ramp until the sum reproduces the prime staircase](waves.gif)

As more waves are added, the sum reproduces the staircase, corners and all. (The staircase in this figure is a standard weighted variant of the prime count, chosen because its formula is the cleanest; its steps land on primes and their powers, and its wobble is the same wobble.) The convergence is an exact mathematical identity rather than an approximation invented for the picture, and the tests in this repository check that adding more waves really does shrink the error.

The same identity also works in the other direction: a sum with one wave for every prime points back at the zeros. This reverse direction is what the 2026 paper relies on, because it gives information about zeros nobody can see, and chapter 8 shows it in action.

One further fact will matter later. How loud each zero's wave sounds depends on where the zero sits sideways. A zero on the line contributes the quietest possible wave, one whose loudness stays balanced forever. A mirror pair off the line would contribute a wave that grows louder, and the further off the line, the faster the growth. The Riemann hypothesis is therefore exactly the statement that the prime wobble stays as quiet as it can possibly be.

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/03.html)** to add the zero-waves one at a time yourself.

---

[← Riemann's map](../02-riemanns-map/README.md)  ·  [The question →](../04-the-question/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

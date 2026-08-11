# Design notes: how this guide is built

## The reader

Assumed to know no mathematics. Not assumed to be stupid. The test of every
paragraph is whether someone who last did algebra at school can follow it
without pausing, and whether an analytic number theorist reading over their
shoulder would call it correct.

## The order, and why

The 2026 paper certifies that two thirds of the zeta zeros sit on Riemann's
line. A reader who has never met the zeta function needs four chapters before
that sentence can even be parsed, so the guide spends them building the
objects: the primes, the zeta landscape, the zero-wave duet, and the question
itself. One chapter then fixes the four ways of counting zeros that the
theorems distinguish. The proof takes four chapters, one per moving part, in
the paper's own order: the listening family, the zero side, the prime side,
and the whole-number step. One chapter assembles the constants, one covers
the paper's own checking (numerics, Lean, and the discovery account), and the
last says honestly what is and is not settled.

1. **The primes** (1) starts from counting primes and shows the wobble in
   their staircase. The wobble is the whole subject.
2. **Riemann's map** (2) introduces the zeta landscape over the plane of
   exponents, the strip, the line, and the zeros, with a rotating
   three-dimensional shot because the landscape genuinely has height.
3. **The music** (3) is the explicit formula seen, not stated: each zero is
   a wave, and adding waves rebuilds the prime staircase.
4. **The question** (4) states the Riemann hypothesis and the record race
   for the proportion on the line: Hardy, Selberg, Levinson's third,
   Conrey's two fifths, the 5/12 of 2020, and the 2026 jump to two thirds.
5. **Three ways to count** (5) fixes the four counters (all zeros, distinct,
   on-line, simple-on-line) that the theorems tell apart. Without this
   chapter the main theorem cannot even be stated honestly.
6. **The microphones** (6) is the test family: windowed waves at equally
   spaced frequencies, and the grid of overlaps they produce. The matrix is
   introduced as a table of numbers a laptop can actually print.
7. **Bowls and saddles** (7) is the zero side: an on-line zero shapes the
   table like a bowl, an off-line pair like a saddle, and the see-saw law
   (inertia) counts positive directions. Rotating three-dimensional shots,
   because bowls and saddles are surfaces.
8. **What the primes reveal** (8) is the prime side: two totals of the same
   table (the count and the energy) computable from primes alone, with no
   unproven assumption. This is Montgomery's calculation made visible.
9. **The whole-number trick** (9) is the integrality step m squared at least
   3m minus 2 and its matrix upgrade, the rank-trace inequality, tested on
   random matrices in front of the reader.
10. **Two thirds** (10) assembles the budget: four, minus two, minus four
    thirds, leaves two thirds; the dial (bandwidth) and the window
    optimisation give 0.6725 and 0.83625; Theorems A to E each get a plain
    sentence.
11. **The checks** (11) covers the paper's section 8 numerics re-run here at
    toy height, the synthetic adversarial configurations, the Lean
    formalisation, and the Appendix C account of how the argument was found.
12. **What it means** (12) carries section 1.5 and Remark 1.1: no bearing on
    RH, lower bounds only, a hard ceiling of 0.68185 for this kind of
    certificate, the slow convergence, and the extensions (Dirichlet
    L-functions, the derivative of the completed zeta).

## Rules followed here

- **No equations in the prose.** Every relation is a picture or a sentence.
  Where the paper's equation matters, the article links to it by number and
  page in the source PDF instead of typesetting it.
- **The difficulty must not spike.** Chapters 7 to 10 open by naming what is
  reused and stating that nothing new is needed. The linear algebra is done
  with bowls, saddles and budgets, never with symbols.
- **Plain words carry their real names.** Every invented term (the line, the
  strip, a pin, a double pin, a mirror pair, the microphones, the window, the
  dial, the table of overlaps, the count, the energy, the see-saw law, the
  whole-number trick) has a glossary line at the end giving the standard
  term.
- **One word, one meaning.** "Table" is only ever the grid of numbers (the
  matrix); the people-free word "staircase" is only the prime count;
  "window" is only the taper; "dial" is only the bandwidth. "Zero" always
  means a nontrivial zero of zeta; the trivial zeros are dismissed once, by
  name, in chapter 2.
- **Animation only where the motion is the mathematics.** The figures that
  move are: the zeta path spiralling through the origin as the height climbs
  (hero), the camera circling the zeta landscape (3D), waves accumulating
  into the prime staircase, a zero's height sliding across two microphones'
  response curves, the camera circling the bowl and the saddle (3D), and
  prime waves accumulating into the spiky density. Everything else is a
  static chart. Non-looping GIFs hold their last frame about 2.5 seconds via
  `end_pad`; the two camera orbits loop seamlessly with no pause.
- **Three-dimensional things are shown as three-dimensional.** The zeta
  landscape and the bowl/saddle pair are surfaces, so they are drawn as
  surfaces and the camera moves around them. Nothing else in the topic is
  three-dimensional, so nothing else pretends to be.
- **A picture made only of words is not a picture.** Word-only comparisons
  (the record table, the now-known/still-open box) are plain quoted blocks.
- **Playable pages.** Chapters 0, 1, 3, 5, 7, 8, 9, 10 and 12 each get a
  self-contained page under `docs/zeta-critical-line/play/`, built by
  `build_interactive.py`, no libraries, no network. The flagship is chapter
  3, where the reader adds zero-waves one at a time and watches the prime
  staircase assemble itself. The JavaScript re-implements parts of
  `zeta_guide`, and `tests/test_interactive.py` compares the two at sample
  points so they cannot drift apart.
- **Do not oversell.** The article says plainly: the theorem is a statement
  about the limit of large heights; at any height a computer can reach, the
  certificate is smaller; the full proof is described, not implemented; the
  tests check toy models and the article's numbers, not the theorem. And it
  states, early and again at the end, that the result has no bearing on the
  Riemann hypothesis in either direction.

## Toolchain decisions

- **matplotlib and Pillow GIFs** for everything, as in the other topics.
  Animations are snapped to an even pixel size first, because an odd width
  comes out of the GIF writer sheared.
- **mpmath** computes zeta and its zeros. The first 300 zero heights are
  shipped in `src/zeta_guide/data/zeros300.txt` so figure scripts and tests
  do not pay the root-finding cost on every run; a test recomputes a sample
  live and compares, and another checks zeta really vanishes at every
  shipped height.
- **The toy matrix experiments run at the window 100 to 300** (44
  microphones), where the shipped zeros cover everything including the tail,
  and a full prime-side integration takes seconds. The paper's own tables
  use 600 to 1200 and up; ours are smaller and say so.
- **The playable pages compute zeta in JavaScript** by the same
  Euler-Maclaurin recipe as `zeta_guide.core.zeta_em`, and embed the first
  fifty shipped zero heights as a constant; tests compare both to the
  library.

## Correctness guardrails

- Chapter 4's record race chart carries years and names, and the tests pin
  every number in it against `examples.py`.
- The four counters of chapter 5 are drawn in one figure with a worked tally,
  and the article never says "zeros on the line" where it means "distinct
  zeros on the line".
- The prime-side/zero-side agreement is computed here at toy height and the
  article quotes our own discrepancy (a few parts in a hundred thousand), not
  the paper's 10^-8, for our sizes.
- The certificate tables of chapter 11 come from our own synthetic runs; the
  paper's corresponding numbers are quoted as the paper's.
- The article states the authorship and verification exactly as the paper
  does: the mathematics is the model's, reviewed and communicated by the
  named humans, formalised in Lean; and it links the Lean repository the
  paper names.

# 8 · What the primes reveal

The see-saw law turns the table into a counting device, but only if we know something about the finished table. Here is the miracle that powers the whole paper: two properties of the table can be computed without looking at the zeros at all. The primes alone reveal them.

The reason is chapter 3's duet. The zeros' side of the duet built the table; the primes' side of the duet can rebuild it. Riemann's explicit formula converts the sum over zeros into a sum over primes, exactly, so every entry of the table equals a sum of prime contributions plus smooth, fully-understood terms ([Proposition 2.1, page 7](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=7)). And the prime rebuild needs surprisingly little: with the dial at its natural setting, only the primes and prime powers below a small reach enter. For our toy stretch, heights 100 to 200, the reach is sixteen: the primes up to 13, and nothing else, know the toy table.

![Prime waves being added one prime at a time until a spiky density stands up, its spikes at the true zero heights](density.gif)

The animation is the duet running in the prime-to-zero direction: start from the smooth average, add one wave per prime power, and watch spikes stand up at the heights of the true zeros, marked along the base. (With so few primes playing, the profile is low-resolution: where two zeros crowd together it shows one broad spike between them, and the tests state the alignment exactly.) This spiky profile is the density the paper integrates against ([equation 2.6, page 7](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=7)). The tests confirm the alignment quantitatively at toy scale: this repository computes the table twice, once from its zeros and once from its primes, and the two agree to about two parts in a hundred million. (The paper's own numerical section reports the same experiment at greater heights, with the same order of agreement.)

Two properties of the table are what the proof extracts, and this guide gives them plain names.

**The count.** Add up the table's diagonal. The prime-side calculation shows this total is, up to small errors, exactly the full count of zeros in the stretch: the microphones, collectively, tally every pin once per multiplicity. In the paper's units our toy table's diagonal adds to 50.4, against 50 zeros really in the stretch.

**The energy.** Square every entry of the table and add them all up. The prime side computes this too, and at the natural dial setting the answer is, per zero counted, four thirds in the limit ([the summary is Theorem 5.8, page 18](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=18)); our small toy still reads about ten percent above it, and closes in slowly as the stretch rises. This single number is the deep arithmetic input of the whole paper. It is Montgomery's 1973 pair-correlation calculation, and the fact that it holds *without assuming the Riemann hypothesis* was made fully explicit by Baluyot, Goldston, Suriajaya and Turnage-Butterbaugh in 2024. The paper leans on their work by name, re-deriving it with the explicit error terms its finite table needs, and adds no new arithmetic of its own: every input beyond this is bookkeeping or linear algebra.

![The toy table with its diagonal highlighted and totals displayed: the count matching the zero tally, the energy near four thirds per zero](totals.png)

Pause on how strange this is. The count and the energy are facts about an object built from the zeros, whose positions are the greatest mystery in mathematics. Yet both facts are certain, because the primes, which we can list, dictate them through an exact identity. The proof now holds a table it cannot see inside, but whose diagonal total and whose energy it knows.

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/08.html)** to add prime waves yourself and watch the spikes find the zeros.

---

[← Bowls and saddles](../07-bowls-and-saddles/README.md)  ·  [The whole-number trick →](../09-the-whole-number-trick/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

# 6 · The microphones

Everything in the proof happens inside one man-made object: a square table of numbers built by listening to the zeros. This chapter builds the table; the toy version on this page was really computed and is really drawn.

A **microphone**, in this guide, is a probe tuned to one frequency: point it at the zeros and it rings according to how close each zero's height is to the microphone's tuned frequency. Its sensitivity curve has a bump shape: a zero at the tuned frequency rings it hard, a zero a little away rings it less, a zero far away barely at all. The shape of that bump is set by a **window**, a taper the paper chooses once ([section 2.2, page 7](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=7)); the window also has a width knob, called **the dial** in this guide, which trades sharpness for reach and whose best setting turns out to be the natural one.

![The window shape, and the row of overlapping microphone sensitivity bumps spread evenly across the stretch of heights](window.png)

Now spread microphones evenly across the stretch of heights being studied, packed at the natural density: about one microphone per zero expected in the stretch. Our toy uses the stretch from height 100 to height 200, which holds 44 microphones. For every pair of microphones, ask: how much do the two hear in common? Each zero rings both, so each zero contributes to the pair jointly; adding the contributions of all zeros gives one number per pair. Written into a grid, one row and one column per microphone, these numbers form **the table** ([equation 2.20, page 8](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=8)).

![A zero sliding between two microphones while both sensitivity bumps respond, and the pair's table entry updates](listen.gif)

The animation shows the principle on two microphones: as a zero slides across, each microphone's response follows its bump, and the product of the two responses is what lands in the table. Here is the real table for our toy stretch, computed from the actual 196 zeros this repository holds near the stretch:

![The forty-four by forty-four table computed from real zeros, bright along the diagonal band and quiet away from it](table.png)

The table is big along its diagonal, where a microphone is paired with itself or a close neighbour, and fades away from it, because distant microphones share almost nothing. It is also perfectly symmetric, thanks to the mirror symmetries of chapter 2. This unassuming grid is the paper's whole arena: the zeros made it, and the next three chapters extract from it everything the theorems need. A reader who likes standard names can know it as a Gram matrix of Weil's Hermitian form; the glossary at the end collects such names.

---

[← Four ways to count](../05-four-counts/README.md)  ·  [Bowls and saddles →](../07-bowls-and-saddles/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

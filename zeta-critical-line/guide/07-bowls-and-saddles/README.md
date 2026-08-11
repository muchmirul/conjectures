# 7 · Bowls and saddles

Nothing new is needed in this chapter: only the table of chapter 6 and one idea about shapes. The question is what a zero's position does to the table's character.

The table is symmetric, and every symmetric table describes a landscape of its own: feed it any mixing recipe for the microphones (so much of microphone one, so much of microphone two, and so on) and the table returns one number, the strength of that mix. Varying the recipe and plotting the strength gives a surface. What kind of surface depends on the zeros, and there are exactly two characters, corresponding to the two kinds of pin.

![A rotating three-dimensional view of a bowl surface next to a saddle surface](bowl_saddle.gif)

**A zero on the line contributes a bowl.** Whatever mix you feed it, its contribution to the strength is never negative: the surface curves up, in at most one direction, and is flat in all the others. This is visible in the arithmetic of the table (each on-line zero enters as a product of a response with itself, and a times a is never negative) and the tests here verify it on real zeros: the toy table of chapter 6, built entirely from on-line zeros, has all 44 of its principal directions curving up or flat, none down.

**A mirror pair contributes a saddle.** The two off-line partners enter the table as a product of *different* responses, and such a contribution curves up in exactly one direction and down in exactly one other ([the paper's Proposition 4.1, page 11](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=11)). The tests build a synthetic mirror pair and confirm: one up-direction, one down-direction.

So the table is a sum: one bowl per distinct on-line pin, one saddle per mirror pair. Now comes the counting law that makes this useful, known since the 1850s as Sylvester's law of inertia, and pictured here as **the see-saw law**: however you add surfaces together, and however you then restrict attention to fewer mixing directions, *the number of independent up-curving directions can never exceed the number of up-contributions you added*. Bowls give at most one up-direction each; saddles give exactly one each. Nothing can conjure more.

![Eigenvalue bars of the toy table, every one positive or flat, next to the bars of one synthetic mirror pair's own contribution, one up and one down](seesaw.png)

Read the law in the useful direction: **count the up-curving directions of the finished table, and you have a floor on how many pins built it.** If the table shows many up-directions, there must be many distinct on-line pins and mirror pairs behind them; and a second, finer accounting in the paper (same proposition) separates the two, because a mirror pair always spends one of its two table slots on a down-direction, while clean on-line pins never do. Counting directions is something a computer, or a theorem, can do to the table without ever being told where the pins are. That is the entire role of the zero side: the paper's [section 4](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf#page=10) does this bookkeeping carefully, including the pins just outside the stretch, whose leakage into the table it bounds once and for all.

Why this replaces the Riemann hypothesis is worth saying plainly. The older route to these counts read the table's entries zero by zero and needed every reading to be positive, which is only guaranteed when all zeros are on the line: that is where RH used to enter. The see-saw law asks for no such thing. It works whatever the zeros are doing, because saddles are allowed for and priced in.

**[Play with this](https://muchmirul.github.io/conjectures/zeta-critical-line/play/07.html)** to mix bowls and saddles and count the up-directions yourself.

---

[← The microphones](../06-the-microphones/README.md)  ·  [What the primes reveal →](../08-the-prime-side/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

# Stacking Balls, from Zero

*A step by step guide to a question about stacking balls that has been open since 1611, and to what was proved about it in 2026. No mathematical background is assumed. Every idea arrives as a picture first.*

![Balls packed in the greengrocer's stack, turning so the depth is visible](guide/00-start-here/hero.gif)

Those are equal balls, packed as tightly as anyone knows how. They fill a little under 75 percent of the space they sit in. The rest is gaps.

In two dimensions the same question has a clean answer, and in three dimensions it took nearly four hundred years to settle. In high dimensions nobody knows the answer, and nobody expects to know it soon. What people do instead is prove that no packing can beat a certain figure. In 2026 the exact limit of the main method for doing that was worked out, and the best general figure since 1978 was replaced.

This article explains the whole story from zero. Each section is one small idea with a picture, and each one has a [page you can play with](https://muchmirul.github.io/conjectures/sphere-packing/play/index.html) where every number in it is a control you can move.

The code for every figure is in this repository, along with a test suite that recomputes each number. Where a claim is somebody else's theorem rather than something computed here, the text says so.

```
    the setting        1  the question        2  the room runs out
                       3  why you cannot just check
    the method         4  the certificate     5  counting twice
                       6  what certificates prove
                       7  is there a ceiling
    the 2026 answer    8  the balancing trick 9  the wall
                      10  building the witness
                      11  the two halves meet
                      12  what it means, and what it does not
```

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/00.html)** and turn the idea over yourself.

## 1 · The question

Take equal balls and pack them without overlapping. The **density** is the fraction of space they fill. Higher is better.

In the plane, "balls" are circles. Line them up in rows and columns and they fill a little over 78 percent. Then push alternate rows sideways so each circle nestles into the dip between two others, and pull the rows closer.

![Circles sliding from square rows into staggered rows while the covered fraction rises](guide/01-the-question/rearrange.gif)

Nothing was added and nothing shrank. The same circles now cover 90.69 percent. That staggered arrangement is the best possible in the plane, which Thue argued in 1910 and Fejes Toth proved completely in 1943.

![The gaps left by square rows and by staggered rows](guide/01-the-question/waste.png)

There are exactly five dimensions where the best packing is known. The next picture cuts space into one hundred equal pieces for each of them and colours the pieces the best known packing fills.

![The five known best packings, each drawn as one hundred equal pieces of space with the filled pieces coloured](guide/01-the-question/known.png)

One dimension is trivial: segments on a line leave no gaps. Two is the staggered rows. Three is the greengrocer's stack, guessed by Kepler in 1611 and proved by Hales in 1998. Eight and twenty four were settled in 2017, by Viazovska for dimension eight and by Cohn, Kumar, Miller, Radchenko and Viazovska for dimension twenty four.

Look at the last two panels. Dimension eight keeps twenty five pieces out of the hundred. Dimension twenty four keeps less than a fifth of a single piece. The density does not drift down as dimensions are added; it falls off a cliff.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/01.html)** and turn the idea over yourself.

## 2 · The room runs out

A ball in a box seems to fill most of it. Turn the box and count the corners.

![A ball inside the box that just holds it, turning so all eight corners are visible](guide/02-room-runs-out/ball_in_box.gif)

In the plane a square has four corners the circle cannot reach. In space a cube has eight. The number of corners doubles with every dimension you add, and the ball never grows to meet them.

The next animation replays that, one dimension at a time, on a single flat box. Each red mark stands for one corner of the higher dimensional box, so the marks double at every step, and the blue disc is drawn with exactly the share of the box the ball still holds.

![The corner marks doubling while the ball's share of the box collapses, one dimension at a time](guide/02-room-runs-out/corners.gif)

By dimension ten a ball fills a quarter of one percent of its box. By dimension thirty it is about two parts in a hundred trillion. Almost all of a high dimensional box is corner.

A stranger fact hides in the same collapse. Keep the radius fixed at one and ask how big the ball itself is. In the next picture every ball is drawn at its true relative size, so nothing needs to be read off an axis: the balls swell for a while, and then they stop.

![Balls of radius one drawn at their true relative sizes, swelling to dimension five and then shrinking away](guide/02-room-runs-out/volume_peak.png)

The biggest ball of radius one lives in dimension five. After that, adding a dimension makes the ball smaller.

The fourth dimension cannot be drawn honestly, so the next picture draws a shadow of it instead, and turns the object in a direction that involves the fourth axis. Watch the corners swing out and back.

![A four dimensional cube turning in four dimensions, shown as its three dimensional shadow](guide/02-room-runs-out/four_d.gif)

The swelling is the fourth direction making itself felt. Every dimension you add gives the corners somewhere further to go.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/02.html)** and turn the idea over yourself.

## 3 · Why you cannot just check

You might hope to settle the question by trying arrangements. You cannot.

![Six different arrangements of circles, none of them settling anything](guide/03-cannot-check/many_packings.png)

There is no end to the arrangements, and they are not even a list you could work through one at a time. Worse, an arrangement can only ever show that some density **is** reachable. To prove no arrangement does better you need a statement about all of them at once.

That is what the rest of this article is about: a single object that says something true about every packing there is.

```
    checking arrangements            one certificate
    ---------------------            ---------------
    one arrangement                  a single function
    another one                      obeying two sign rules
    another one
    and so on                        bounds every arrangement
    never finishes                   at once
```

We will call that object a **certificate**. The name is ours; the standard term is in the glossary at the end.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/03.html)** and turn the idea over yourself.

## 4 · The certificate

A certificate is one function. Feed it a distance and it hands back a number, and it has to obey two rules.

**Rule one.** From distance one outward, the number it hands back is never above zero.

**Rule two.** Its **Fourier transform** is never below zero, anywhere.

The Fourier transform is the second character in this story, so here is what it is. Any function can be built by adding up waves of different frequencies. The Fourier transform is the recipe: it tells you how much of each frequency you need. A function and its transform are two views of one object, the way a chord and its list of notes are two views of one sound.

![A certificate: the function on the left, its transform on the right, with both rules drawn](guide/04-the-certificate/rules.png)

The left panel is the function. The shaded band is where rule one applies, and the curve dips below zero exactly where it must. The right panel is the transform, which stays at or above zero the whole way.

Both rules are easy on their own. A function that is negative from distance one out is easy to write. A function whose transform is never negative is easy to write. The difficulty is that the Fourier transform pushes back: making a function drop sharply in one view makes it spread out and wobble in the other. Getting both at once is the entire game.

Here is the simplest thing that obeys both.

![The simplest certificate: one minus the distance squared, times a bell curve](guide/04-the-certificate/simple.png)

It obeys both rules, and it is nearly worthless. In the plane the number it hands back is above one, and every density is below one anyway, so it says nothing. It only starts saying something true in dimensions four and five, and it stops existing entirely at dimension seven, where its transform can no longer be kept positive.

Turn one dial on a working certificate and watch what happens.

![Turning a dial until the transform dips below zero and the certificate stops proving anything](guide/04-the-certificate/tuning.gif)

Past a point the transform goes negative, rule two breaks, and the certificate proves nothing at all.

Once you have a function obeying both rules, it hands you a number, and no packing in that dimension can be denser than that number. The next section says why.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/04.html)** and turn the idea over yourself.

## 5 · Counting twice

Take any packing and any certificate. Add up the certificate's value over every pair of ball centres.

![Adding over pairs of centres, then over frequencies instead](guide/05-count-twice/two_counts.gif)

Do the sum in the ordinary way, over pairs of centres, and rule one takes over. Two different centres are always at least distance one apart, because the balls do not overlap. Out there the certificate is at or below zero. So every pair except a centre with itself can only drag the total down.

Now do the same sum in the other view, over frequencies. This is where the Fourier transform earns its place: there is an identity, Poisson summation, that says the sum over centres and the sum over frequencies are the same number. In that view rule two takes over, every term is at or above zero, and the total can only be pushed up.

```
    pairs of centres  --->   one total   <---  frequencies
    push it down                              push it up

    the packing is caught between them,
    and that trap is the density bound
```

One number, squeezed from both sides. Rearranging the squeeze gives a ceiling on the density, and that ceiling depends only on the certificate, never on the packing. That is the Gorbachev and Cohn-Elkies bound, from 2000 and 2003.

The word "linear program" in the title of the source paper is the name for this kind of setup: a best value being hunted subject to a list of constraints that are all of this simple sign type.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/05.html)** and turn the idea over yourself.

## 6 · What certificates actually prove

This repository contains a small search that hunts for good certificates. Starting from an easy one and nudging it at random, it finds these. In the picture, space is a tube being filled from the floor: blue is how full the best known packing really makes it, and everything above the certificate's ceiling is proved unreachable.

![Space drawn as a tube being filled, with the thin unknown sliver between what is reached and what is impossible magnified beside it](guide/06-best-so-far/gap.png)

In the plane it proves that no packing of circles beats 91.16 percent. The staggered rows reach 90.69 percent. Those two numbers are less than half a percentage point apart, a sliver too thin to see at true scale, which is why the picture magnifies it. Everything that is still unknown about circle packing lives inside that sliver.

Two honest notes about that. The sign rules here are checked by sampling a fine grid, not proved symbolically, so this is a numerical certificate rather than a formal proof. And it is much weaker than what specialists get: they use semidefinite programming and force the function to have roots in chosen places, and none of that is implemented here.

The search also fails in an instructive way. Its starting family of functions stops existing before dimension six, so in dimension eight it cannot even begin. Dimension eight is exactly where Viazovska's function lives, and building it took the mathematics of modular forms.

```
    dimensions 8 and 24     the certificate is known exactly, and it is sharp
    dimensions 1, 2, 3      the best packing is known, the certificate is not sharp
    every other dimension   neither the best packing nor the best certificate is known
    as the dimension grows  the best certificate is now known: the 2026 result
```

In dimensions eight and twenty four the best certificate is known and it is exactly right, which is why those two dimensions are settled. Everywhere else there is a gap between what can be built and what can be proved impossible.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/06.html)** and turn the idea over yourself.

## 7 · Is there a ceiling on the method?

Every bound of this kind shrinks by a fixed factor for each dimension you add. The honest picture of such a bound is a row of squares, each square a fixed fraction of the area of the one before. The next figure draws one row for the 1978 rule and one for the 2026 rule.

![Two rows of shrinking squares, one for the 1978 rule and one for the 2026 rule, too alike for the eye to separate](guide/07-the-ceiling/exponents.png)

The two rows look identical, and that is the honest first impression. Because the factor is fixed, the natural way to compare two bounds is to ask how many halvings each is worth per dimension, and bigger is better, because it means the bound shrinks faster. The 1978 figure was 0.59906 halvings per dimension, from Kabatianskii and Levenshtein. It stood for forty eight years.

A difference in the fourth decimal place sounds like nothing. It is a difference in a rate, so it compounds, and the next animation lets it. The gray disc is the 1978 ceiling held at a fixed size for comparison; the green disc is the 2026 ceiling drawn to scale beside it, area for area, as the dimension climbs.

![The 2026 ceiling shrinking against the fixed 1978 one as the dimension counter climbs to one thousand](guide/07-the-ceiling/advantage.gif)

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

## 8 · The balancing trick

Nothing new is needed from here on. The rest of this article uses the two sign rules from section 4, the Fourier transform from the same section, and the idea of a radius. What changes is that we stop asking what a particular certificate proves and start asking what any certificate must look like.

Start with a certificate. Stretch it, like adjusting the zoom on a photograph. Stretching a function makes its transform shrink by the same factor and grow taller, so there is exactly one amount of stretch that makes the function and its transform agree at the centre. Apply that stretch, then subtract one from the other.

![Subtracting the stretched certificate from its own transform](guide/08-balancing/balancing.gif)

Call the result the **balanced function**. Two things are now true about it, and both come for free.

It is zero at the centre, because that is what the stretch was for.

And it turns into minus itself under the Fourier transform. Subtracting swapped the two roles, so taking the transform swaps them back and flips the sign. A function that transforms into minus itself is a rare thing, and it is rigid enough to be attacked.

Here is why that matters. A function that transforms into minus itself has total zero, so exactly half of its weight is negative. And rule one, translated through the subtraction, says the balanced function is never negative beyond a certain radius.

![Half the weight is negative, and all of it is trapped inside one radius](guide/08-balancing/trapped.png)

So the entire negative half is trapped inside one ball. The radius of that ball is the number that decides how good the certificate was: the smaller the radius, the better the certificate. The packing question has turned into a question about how far in you can push a radius.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/08.html)** and turn the idea over yourself.

## 9 · The wall

Push the radius in and the demand gets harder. The negative half of the weight does not shrink; it is always exactly half. It just has less room to sit in.

![Shrinking the radius until the demand cannot be met](guide/09-the-wall/wall.gif)

The 2026 proof shows there is a wall. Once the radius drops below one over pi, times the square root of the dimension, the amount of weight that can possibly sit inside that ball is exponentially small. Half is not exponentially small. So the radius cannot go there, for any certificate at all.

That is the hard half of the theorem, and it is the half that says the method has a ceiling.

The number pi appears because of the shape of the machinery, not by coincidence. Roughly, the argument moves the problem into a coordinate system where taking the Fourier transform becomes a reflection, works inside a strip, and uses a classical principle that bounds a function inside a region by its values on the edges. That principle assigns each frequency a weight. As the argument is pushed to the decisive edge of the strip, those weights settle into one specific bell shaped curve.

![The weighting used by the argument, and the shape it becomes at the edge](guide/09-the-wall/ingredients.png)

That curve is where one over pi comes from. This repository does not implement the argument, but it does check the ingredients: the reflection has size exactly one along the relevant line, the limiting curve is a genuine probability density with the stated frequency profile, and its logarithmic average has the closed form the proof uses.

One detail is worth repeating because it is the kind of thing that decides a constant. The weights do not add up to one. It is tempting to normalise them into a probability, and doing it too early changes the answer.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/09.html)** and turn the idea over yourself.

## 10 · Building the witness

Ruling everything out is only half. Someone still has to produce a certificate that actually reaches the wall.

The natural place to start is a Gaussian, the bell curve, because it is its own Fourier transform. The symmetry the argument needs is free. The trouble is that its radius sits at one over the square root of two pi, which is about 0.399, and the wall is at one over pi, about 0.318. The Gaussian is in the wrong place.

So the construction multiplies it by a carefully chosen even deformation, which moves the radius without disturbing the symmetry.

![The radius sliding from the Gaussian's value down onto the wall](guide/10-the-witness/moving_radius.gif)

How far it moves is given by a single integral. An **integral** is an area being gathered up piece by piece, and this one can be watched doing it: the region under the curve fills in from the left, and the jar on the right fills with the total gathered so far. The jar settles on an exact closed value, the logarithm of pi over two. It is an old identity of Wallis.

![The area under the curve being gathered up from the left, and a jar filling to exactly the log of pi over two](guide/10-the-witness/wallis.gif)

Put the two together and the Gaussian's 0.399 becomes exactly 0.318. The construction lands on the wall, not near it. That is the second half of the theorem.

Two more pieces are needed to make it work, and both are repairs rather than ideas.

```
    a Gaussian                   already its own Fourier transform,
                                 so the symmetry is free
    an even deformation          slides the radius onto the wall
                                 without breaking that symmetry
    a tiny bump far away         restores the damping the deformation
                                 destroys at huge radii
    a pair of polynomial factors fixes the signs near the origin, where
                                 the estimates say nothing
```

The deformation, left alone, destroys the damping that keeps the function well behaved at enormous radii, so a tiny positive bump is added far away to restore it. And the estimates that control the signs are useless near the origin, so a pair of polynomial factors is included to handle that stretch separately.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/10.html)** and turn the idea over yourself.

## 11 · The two halves meet

One direction says no certificate has a radius below the wall. The other exhibits a certificate whose radius reaches it. Neither alone is an answer. Together they say the wall is the exact answer.

![The two directions closing on one number](guide/11-they-meet/closing.gif)

Converting a statement about radii into a statement about densities takes one more standard fact, Stirling's formula, which is what turns the ball volume from section 2 into something explicit. The dimension cancels, and one number is left.

```
    as a rate per dimension        0.6577446234794570
    as halvings per dimension      0.6044005442916777
    as a radius per square root    0.3183098861837907

    three ways of writing one fact
```

The middle number is the one to remember: **0.6044005442916777** halvings per dimension. The 1978 figure was 0.59905576.

This is the first improvement to the general sphere packing exponent since 1978, and the matching half means no certificate of this kind can ever improve it again.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/11.html)** and turn the idea over yourself.

## 12 · What it means, and what it does not

Be careful about what was settled. The method now has a known ceiling. The packing problem does not.

```
    settled                                still open
    -------                                ----------
    the exact rate of the method           the true densest packing in
    the best exponent since 1978 replaced  most dimensions
    both sign uncertainty constants        whether any method beats this
                                           exponent
                                           the gap between what is built
                                           and what is proved
```

Nobody has found a packing in high dimensions that comes anywhere near the new bound, and the gap between the best construction and the best bound is still exponentially wide. What changed is that one particular route is now fully mapped: we know exactly how far it goes, so improving on it requires a different idea.

```
    1611  Kepler guesses the greengrocer's stack cannot be beaten
    1978  Kabatianskii and Levenshtein prove the exponent 0.59905576
    2000  Gorbachev, and independently Cohn, write down the method
    2003  Cohn and Elkies publish it and compute with it
    2005  Hales's proof of the Kepler conjecture appears in print
    2014  Cohn and Zhao: the method is at least as strong as the 1978 bound
    2017  Viazovska settles dimension 8; with Cohn, Kumar, Miller and
          Radchenko, dimension 24
    2020  Afkhami-Jeddi, Cohn, Hartman, de Laat and Tajdini conjecture the rate
    2026  the rate is proved, and 0.6044005442916777 replaces the 1978 exponent
```

The same proof settles two other questions, about how early a Fourier eigenfunction can settle down to a fixed sign. There are two versions, one for functions that transform into themselves and one for functions that transform into minus themselves. Both were conjectured to have the same limit, and the proof confirms it: both are one over pi, times the square root of the dimension.

![The two radii drawn as circles closing on the shared dashed limit circle, the plus one always inside; the spacing sketches the trend rather than exact values](guide/12-what-it-means/two_radii.png)

The source also observes something the limit hides. In every single dimension the two radii are different, and the plus version is always the smaller. Their limits agree; the quantities themselves never do.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/12.html)** and turn the idea over yourself.

## What you can check yourself

Everything below runs from this repository, with no mathematical background needed.

```
cd sphere-packing
make venv        # once
make test        # re-checks every number in this article
make figures     # re-renders every picture
```

The tests do these things, among others:

- rebuild the five known densities from their lattices and confirm they match the quoted values
- confirm the ball volume peaks in dimension five and then falls
- verify, by direct integration in dimensions one and three, that the building blocks used for certificates really do transform into themselves up to a sign
- take the certificates this repository found and re-check both sign rules on a grid thirty times finer than the search used
- confirm that Wallis's integral is the logarithm of pi over two, and that the Gaussian's radius times that displacement is one over pi
- confirm that the three pieces multiply to the rate the theorem states

The one thing you cannot check here is the theorem. The argument in section 9 is described, not implemented.

## The plain words, and the real ones

| this article says | the standard term |
|---|---|
| certificate | admissible function for the Cohn-Elkies linear program |
| the two sign rules | the sign conditions defining the admissible set |
| the balanced function | an anti-self-Fourier function, one satisfying the transform equals minus itself |
| the wall | the sign uncertainty radius lower bound |
| halvings per dimension | the exponent, in base two, of the density bound |
| the recipe of frequencies | the Fourier transform |
| counting twice | Poisson summation |
| the deformation | the Mellin envelope multiplier |
| stretching a function | dilation |

The source calls the density bound LP, for linear program, and writes the new exponent as one half of the logarithm to base two of two pi over e.

## Where to go next

- The source: chapter 1 of *Ten Advances in Mathematics and Theoretical Computer Science*, with its reasoning walkthrough. Both are in `docs/ten-proofs/01-sphere-packing-linear-program/`.
- The published collection of reasoning walkthroughs the source belongs to: [cdn.openai.com/pdf/reasoning-walkthroughs.pdf](https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf).
- Cohn and Elkies, "New upper bounds on sphere packings I", Annals of Mathematics 157 (2003), for the method itself.
- Viazovska, "The sphere packing problem in dimension 8", Annals of Mathematics 185 (2017).
- `notes/research-content.md` in this folder, which lists every claim above and marks it as computed here, quoted from the literature, or part of the 2026 result.

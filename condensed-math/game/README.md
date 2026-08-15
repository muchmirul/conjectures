# The game

*An interactive introduction to condensed mathematics in eight worlds, from
three objects on a table to the duality theorem developed in the lectures.*

**Play it:**
[muchmirul.github.io/conjectures/condensed-math/game](https://muchmirul.github.io/conjectures/condensed-math/game/)

The written guide beside this folder explains the subject. The game makes a
reader find it. Nothing is presented as a finished definition before the reader
has watched the thing the definition is about, and no name is given before the
thing has been run.

It assumes no mathematics whatsoever. World 1 begins by putting a coin, a key
and a stone on a table.

## The shape of a brick

Every idea arrives as a **brick**, and every brick runs in three stages, in the
same order, always:

| stage | what it does |
|---|---|
| **Concept** | the idea, stated plainly in one sentence, before any story, so the reader is never guessing what is being talked about |
| **Intuition** | what it feels like, in everyday terms, ending in a question the reader answers *before* the answer exists on the page |
| **Experiment** | something the reader runs, then the name the literature uses, then the mathematics with every symbol read out |

Each brick also declares its **preliminary**: what a reader must already hold
to follow it, in plain words. Nothing may appear in a preliminary that an
earlier brick did not build, and the tests check the order.

The experiment is either a simulation on the page, computing its numbers as the
reader moves it, or a short thing to do by hand whose result is withheld until
the reader says they have done it.

## The route

| world | what the reader ends up holding |
|---|---|
| 1 · Four familiar ideas | collections, maps, equivalence, and addition |
| 2 · Nearness and a one-way bridge | topology, continuity, and spaces with the same points but different nearness |
| 3 · The algebraic test that fails | kernels, cokernels, and their incorrect verdict on the bridge |
| 4 · Study spaces with probes | probes built from finite stages |
| 5 · The answer table becomes the object | restriction, gluing, and condensed sets |
| 6 · Verify the repair | the missing object, the restored test, preserved spaces, and homology |
| 7 · Infinite sums with well-defined values | p-adic nearness, measures, and solidity |
| 8 · From multiplication to duality | analytic rings, the exponent bound, compact support, and duality |

Worlds 1 to 3 are not condensed mathematics. They exist because the crack the
subject repairs is a crack in exactly those ordinary ideas, and a reader who
has not watched it open has no reason to accept the repair. Worlds 4 to 6 are
Lectures I to III, world 7 is Lectures IV to VI, and world 8 is Lectures VII to
XI at the level of intuition this format can carry honestly.

## Layout

```
model.py       the shape of a beat, a brick and a world
worlds/        the content, one module per world
widgets.py     the twelve things a reader can move, as JavaScript
build_game.py  worlds -> ../../docs/condensed-math/game/
```

`worlds/` is the only place to edit prose. Run `make game` from the
`condensed-math` folder afterwards.

## The mathematics in the widgets

None of it is written in this folder. `build_interactive.MATHS` already carries
probes, measures, the p-adic size, the merge ratio and Smith normal form in
JavaScript, and `tests/test_interactive.py` already compares that block against
the Python library point by point. The game pages include the same block, so a
widget and a chapter simulation cannot quietly disagree about a number, and
`tests/test_game.py` fails if the game ever starts carrying its own copy.

What the game does add is small and separately checked: the count of fractions
inside a shrinking window, the wobble of the base-two value function inside a
box, and the finite window used to display a kernel and a cokernel.

## What the tests check

```
cd condensed-math
make test
```

- every brick runs the three stages, in order, with a preliminary, a guess
  before the answer, something to run, a name and the mathematics
- every guess has at least two options and answers each one properly
- every widget named by a world exists, and every widget that exists is used
- each world is played from the first press to the last in `node`, through a
  DOM stub, with every control of every widget moved afterwards; a page that
  throws fails there rather than in front of a reader
- the numbers the widgets add on top of the library agree with exact
  arithmetic in Python

## The reading interface

One column, one button, one thing on screen at a time. No scoring, no
branching, nothing to lose: a guess that misses gets a reply explaining which
instinct misled, and the route carries on. Progress is remembered in the
browser, so a world can be left half-finished and resumed.

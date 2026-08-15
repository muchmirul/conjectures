# The order the ideas arrive in

Condensed mathematics is one subject and a wide one, so this topic is three
articles rather than one. Each part is readable given the one before it and
nothing else. This file records why the split falls where it does, and what
each chapter is allowed to assume.

## The split

| part | lectures | the one thing it adds |
|---|---|---|
| one, *Shapes You Can Only See By Probing Them* | I to III | a space is what it says to probes, and that makes subtraction work |
| two, *Infinite Sums That Finally Land* | IV to VI | an endless sum has exactly one answer, and the objects where it does are built from products of copies of the whole numbers |
| three, *Rings That Know How To Integrate* | VII to XI | carry the rule to rings, and geometry with a duality theorem falls out |

The seam between one and two is where analysis starts: nothing before it can
add up an infinite series. The seam between two and three is where
multiplication starts: everything before it is about adding only.

## Part one, chapter by chapter

Each row lists what the chapter may assume. A chapter may never assume
anything below it.

| chapter | assumes | introduces |
|---|---|---|
| 1 two real lines | nothing | the failure: a map with nothing missing at either end which is still not a sameness |
| 2 probes that branch | 1 | a probe: one box split forever, every stage finite |
| 3 what a shape says | 2 | a landing, and the move to describing a shape by all its landings |
| 4 cut, and glue | 3 | the two rules an answer sheet obeys |
| 5 the quotient with no points | 1, 4 | the ghost, and that subtraction now works |
| 6 probes that never fold | 2, 4 | unfoldable probes, and that the glue rule is free on them |
| 7 nothing was lost | 3, 5 | the receipt: which spaces survive the translation |
| 8 counting holes | 7 | winding, the doughnut's two loops, and that the holes survive |

The difficulty must not spike anywhere in this list. Chapters 6 and 8 are the
two that could, and both open by saying nothing new is needed.

## Part two, chapter by chapter

| chapter | assumes | introduces |
|---|---|---|
| 1 sums with nowhere to land | part one | that an infinite sum depends on a choice of what near means |
| 2 weights that agree | 1, part one chapter 2 | a weighting, and integrating against one |
| 3 every function is a stack of steps | 2 | that the things being weighed form a free group |
| 4 products in, sums out | 3 | the duality that turns weightings into a row of dials |
| 5 the solid rule | 2, 4 | solidity, and the building blocks |
| 6 where the real line goes | 5 | divisibility, and the ruler's disappearance |
| 7 the multiplication table | 5 | the completed tensor product |
| 8 solidify a shape | 5, part one chapter 8 | the payoff: topology falls out of an algebra rule |

Chapter 6 is the one a reader is most likely to read as the theory breaking.
It therefore says plainly, twice, that the vanishing is a feature of this
particular notion of completion rather than a defect.

## Part three, chapter by chapter

| chapter | assumes | introduces |
|---|---|---|
| 1 a ring with a rule | part two | the general notion, ring plus theory of measures |
| 2 two rules that work | 1 | the two examples everything else is built on |
| 3 the real line's own rule | 1, part two chapter 6 | the exponent, and why it cannot pass one |
| 4 functions near the edge | 2 | the edge ring and its tails |
| 5 cohomology with compact support | 4 | the compactly supported operation and its counterweight |
| 6 gluing the local pictures | 5 | patches, and the choice of what counts as small |
| 7 the six operations | 5, 6 | the standard shape modern geometry uses |
| 8 duality, watched | 7 | the theorem the course was pointing at |

## Rules this topic follows

**Every chapter carries something to move.** Twenty-seven chapters, twenty-seven
simulations, embedded in the article rather than linked beside it. The topic
is deliberately simulation-heavy, because the definitions here look forbidding
and the objects underneath them are concrete.

**Motion is reserved for mathematics.** A figure that only redraws itself is a
static png. The animations are: a probe refining, a matching being made, a
landing being torn, a staircase assembling, weights being handed down, a scan
running out of reach, a ball changing shape, and two cameras going round a
surface. Everything else is still.

**Every animation that builds to a point holds that point for two and a half
seconds.** The two rotating camera shots are the exception and loop seamlessly.

**No formula appears in the prose.** Where the lectures use one, this guide
either draws it or links to the numbered result by page. Every invented plain
word has a glossary line giving its standard name, in each part.

**Nothing claims more than it has.** `research-content.md` marks every claim as
computed here, a finite shadow of an infinite statement, or quoted, and the
prose says which where it matters.

## The game, and why its order is different

The three articles explain the subject. `game/` makes a reader find it, and
that changes what the ordering constraint is. An article may introduce an idea
because the next section needs it. The game may not: nothing is allowed to be
named before the reader has watched the thing the name is for.

So the game carries its own route, eight worlds rather than three parts, and
the first three of them are not condensed mathematics at all.

| world | lectures | why it is there |
|---|---|---|
| 1 four words you already use | none | the crack is a crack in *collection*, *map*, *same* and *adding*; a reader who has not held those four cannot see it open |
| 2 nearness, and the one-way bridge | none | builds the dust and the ruler by hand, so Example 1.9 is something the reader made |
| 3 the test that should have caught it | none | kernel and cokernel from nothing, then the confident wrong verdict |
| 4 stop asking what is inside | I to II | probes, split by hand, and what a shape says to one |
| 5 the answer table becomes the object | I to II | restriction, gluing, condensed sets, extremally disconnected probes |
| 6 verify the repair | I to III | the missing object, the restored test, preserved spaces, and homology |
| 7 sums that finally land | IV to VI | p-adic nearness, measures, solidity, the vanishing of the line |
| 8 multiplying, and what it was all for | VII to XI | analytic rings, the exponent ceiling, the six operations, duality |

Worlds 1 to 3 exist because of a rule the articles do not have to obey: the
reader must want the repair before it arrives. World 3 ends with the reader
writing down a three-line specification, and world 6 ticks it off line by line
in the same order.

### Rules the game follows

**Concept, then intuition, then experiment.** Every brick, always, in that
order. The concept is stated in one sentence before any story, so the reader is
never inferring what is being talked about. The intuition is everyday and ends
in a guess made before the answer exists on the page. The experiment is
something the reader runs, and only after it comes the name and the symbols.
`tests/test_game.py` fails a brick that breaks the order.

**Every brick declares what it assumes.** In plain words, shown before the
brick starts, and nothing may appear there that an earlier brick did not build.

**No option is wrong.** Each answer to a guess gets a reply of its own, naming
which instinct produced it and where that instinct is sound. A reader who
guesses badly learns more than one who guesses well, and the writing has to
reward that rather than punish it.

**Nothing is named before it is run.** Twelve widgets and twenty-two hands-on
experiments, one in every brick. A hands-on experiment withholds its result
until the reader says they have done it.

**The symbols always arrive.** Every brick ends with the notation and a
symbol-by-symbol reading, plus the numbered result in the lectures where there
is one. The game is a route into the literature, not a substitute for it, and
the last brick asks the reader to open the lectures at page 9 and read.

**No new mathematics in the game's own JavaScript.** The widgets include the
same `MATHS` block the playable pages use, which is already compared against
the Python library; the tests fail if the game starts carrying its own copy of
a probe or a measure.

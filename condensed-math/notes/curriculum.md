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

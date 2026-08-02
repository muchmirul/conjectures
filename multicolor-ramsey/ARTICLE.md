# The Triangle Game, from Zero

*A step by step guide to a coloring game that has been studied since 1955, to a question about it that Erdős put money on, and to the 2026 result that answered it. No mathematical background is assumed. Every idea arrives as a picture first.*

![All 120 connections among sixteen people being colored with three colors, ending safe](guide/00-start-here/hero.gif)

Sixteen people, every pair connected, every connection given one of three colors. Watch to the end: no three people have all three of their mutual connections in a single color. That is the whole game, and sixteen is the largest group that can win it with three colors. It has been since 1955, and nobody has beaten it.

The question this article builds toward is what happens when you have many colors. With more colors you can protect a bigger group. How much bigger, per color? Erdős offered cash for the answer in the 1980s, the standard reference book recorded the question in 1990, and until recently the honest summary was that the two known guardrails were absurdly far apart. In 2026 the question was answered.

This article explains the whole story from zero. Each section is one small idea with a picture, and each one has a [page you can play with](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/index.html) where the numbers in it are controls you can move.

The code for every figure is in this repository, along with a test suite that recomputes each number. Where a claim is somebody else's theorem rather than something computed here, the text says so.

```
    the game           1  the game            2  six is forced
                       3  more crayons
    the question       4  the question
    the old tools      5  multiply            6  the ceiling
                       7  the gap
    the 2026 answer    8  palettes            9  the trap
                      10  the referee        11  the tower
                      12  what it means, and what it does not
```

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/00.html)** and turn the idea over yourself.

## 1 · The game

Take a group of people and connect every pair with a string. Now color every string. You lose the moment three people are joined to each other by three strings of the same color. Call such a threesome a **one-color triangle**, and call a finished coloring with no one-color triangle **safe**.

![A four-person group colored two ways, one with a one-color triangle and one safe](guide/01-the-game/rules.png)

The left group is lost: the thick triangle has all three of its strings in the first color. The right group is safe: every one of its four possible triangles wears two colors.

With two colors, five people can be kept safe, and there is essentially one way to do it. Put the five in a circle. Color the ring of neighbouring pairs with the first color and the star of skipping pairs with the second.

![The five-person table being colored, then all ten triangles checked one by one](guide/01-the-game/pentagon.gif)

The sweep at the end is the point. A safe coloring is not a vague impression, it is a finite list of checks: this table has ten possible triangles, and all ten mix their colors. The test suite of this repository performs exactly that sweep.

Why it works is worth one sentence. Each color's strings form a ring of five on their own, and a ring has no triangle of any kind, so it certainly has no one-color one.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/01.html)** and turn the idea over yourself.

## 2 · Six is forced

Five people can be kept safe with two colors. Six cannot. This is the one theorem this article proves completely, and the proof fits in a picture.

Sit six people down, pick one of them, and look at her five strings. Five strings, two colors: some color appears on at least three of them. Say it is red, going to three particular people.

![The pigeonhole proof playing out: three same-colored strings force a triangle either way](guide/02-six-is-forced/pigeonhole.gif)

Now watch those three people. If any two of them are joined by a red string, that string plus their two red strings back to the first person close a red triangle. So all three of their mutual strings must avoid red, which means all three are blue, and that is a blue triangle. A one-color triangle appears in either case.

Nothing about the argument used which coloring was chosen, so every coloring of six people fails. Machines agree: this repository's tests walk through all 32768 ways to two-color the fifteen strings of a six-person group, and not one is safe. The sweep finds a little more than the proof promised.

![The census of all 32768 colorings of six people, counted by how many one-color triangles each contains](guide/02-six-is-forced/census.png)

The bar at zero is empty, which is the theorem. The bar at one is also empty: the luckiest colorings of six contain exactly two one-color triangles, never just one. That refinement is a 1959 observation of Goodman, rediscovered here by brute force.

So the story of two colors is complete: five people can be kept safe and six cannot. Call six the **forcing size** for two colors: the group size at which a one-color triangle becomes unavoidable.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/02.html)** and turn the idea over yourself.

## 3 · More crayons

A third color changes the scale of the game. The record safe group jumps from five to sixteen, and the sixteen-person coloring is the one the opening animation drew. Here it is taken apart, one color at a time.

![The record three-color table split into its three one-color nets, each triangle-free](guide/03-more-crayons/layers.png)

Each panel is one color's net. Every person is joined to exactly five others in each color, and each net, seen on its own, contains no triangle at all. A net with no triangle can never hold a one-color one, so the whole table is safe. The construction comes from Greenwood and Gleason in 1955; this repository rebuilds it from their recipe and re-checks all 560 triangles.

Greenwood and Gleason also proved the matching failure: seventeen people cannot be kept safe with three colors. That direction is far beyond checking case by case, since the colorings of seventeen people outnumber atoms, so this article quotes it rather than verifying it.

Then the exact answers stop.

![What is known for one, two, three and four colors, with the four-color range still open](guide/03-more-crayons/records.png)

For four colors the forcing size is known to be somewhere between 51 and 62, a range that has stood for decades. For five colors the uncertainty is wider still. Nobody knows the answer for any color count past three, and it is not for lack of computers: the case-by-case approach dies immediately, and everything since has been about finding arguments instead.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/03.html)** and turn the idea over yourself.

## 4 · The question

Line up what the records so far actually cost. Two colors bought a table of five. Three colors bought a table of sixteen. The natural currency is not the table size itself but the table size *per color spent*, measured so that the arithmetic comes out fair: a recipe that turns each color into the same multiplying factor should score that factor.

Two colors for five people scores about 2.24, because 2.24 times itself is five. Three colors for sixteen scores about 2.52, because 2.52 times itself, twice over, is sixteen. The best recipe known before 2026, built from addition tricks on number circles, approaches a score of about 3.28 as the color count grows. It only approaches it: the recipe loses a fixed slice at every round, so no single small table actually reaches that rate, and at five colors, for example, a table big enough to score 3.28 outright is already impossible.

![The people-per-color rate of the known constructions, climbing slowly toward an open question](guide/04-the-question/rate.png)

The bars creep upward. The question the rest of this article answers is the obvious one about that creep.

> As the number of colors grows without limit, does the people-per-color rate climb without limit too, or does it level off at some fixed ceiling?

Erdős offered 250 dollars for determining what the rate approaches and 100 dollars for merely deciding whether it is finite. The question was recorded in the standard Ramsey theory reference in 1990, and it stayed open, in both directions, until the result this article describes.

It is worth feeling why both answers were plausible. Each new color is a whole extra dimension of freedom, so perhaps tables can grow faster and faster per color forever. On the other hand every construction anyone had ever written down got a fixed rate and no more, as the next chapter shows.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/04.html)** and turn the idea over yourself.

## 5 · Multiply

The classical tool takes two safe tables and multiplies them. Watch it act on two copies of the pentagon.

![Each of five people becoming a room of five, keeping outer colors between rooms and fresh colors inside](guide/05-multiply/blowup.gif)

Each of the original five people becomes a **room** holding a full copy of the other table. A string between two rooms keeps the color the two original people used. A string inside a room uses the inner table's coloring, in fresh colors that nothing else touches.

The result is safe, and the reason splits cleanly in two. A triangle with all three corners in one room is a triangle of the inner table, and the inner table was safe. A triangle touching more than one room cannot use any inside color, so all its strings run between rooms; but two corners in one room lead outward in strings that copy the *same* original person's colors, so the triangle's colors trace a triangle of the outer table, and the outer table was safe. The tests do not take this on faith: they verify the 25-person, four-color product cold, all 2300 triangles, and an 80-person, five-color product as well.

So safe tables multiply: sizes multiply, color counts add. Repeat forever and five people at two colors become 25 at four, 125 at six, and so on without end.

![Repeated products of the pentagon and of the sixteen table, straight lines on a growth chart](guide/05-multiply/tower.png)

Both lines are straight on this chart, and straight means stuck. Multiplying the pentagon forever earns exactly 2.24 people per color at every step, and the sixteen-person table earns exactly 2.52, because each round adds the same colors and multiplies by the same factor. A fixed recipe, repeated, can never make the rate climb. Whatever answers the question of chapter 4 has to spend its colors in a genuinely new way.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/05.html)** and turn the idea over yourself.

## 6 · The ceiling

The other guardrail comes from the six-person argument of chapter 2, which generalizes to any number of colors. Pick one person at a big table and sort everyone else by the color of their string to her.

![One person's fifteen connections in the sixteen-person table, sliding into three color groups](guide/06-the-ceiling/sort.gif)

With three colors and fifteen strings, some group holds at least five people. Inside that group, its own color is now poison: any string of that color between two members would close a triangle with the person at the center. So the group is a smaller table effectively playing with one color fewer, and the same move can be made again inside it, and again, until the colors run out and a bare triangle is forced.

Run the argument in reverse and it says: a table safe for one color holds at most 2 people, so a table safe for two colors holds at most a group small enough that sorting works out, and so on. The forcing sizes it proves are 3, 6, 17, 66, 327, and onward, each step multiplying by roughly the number of colors.

![The staircase of forcing sizes next to plain factorials on a growth chart](guide/06-the-ceiling/staircase.png)

Multiplying by the color count at every step is exactly what a factorial does, so the ceiling grows like a factorial. The staircase happens to be exactly right at two colors and at three, where 6 and 17 are the true answers. At four colors it says 66 while the truth is at most 62; the best refinement in the literature trims such constants, reaching about e minus one sixth times the factorial, but no refinement has ever changed the factorial shape.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/06.html)** and turn the idea over yourself.

## 7 · The gap

Put the two guardrails on one chart and the problem stares back.

![The exponential floor and the factorial ceiling, with the widening unknown band shaded](guide/07-the-gap/gap.png)

The floor in the chart is what multiplying the record tables honestly proves at each color count. It grows like a fixed number raised to the color count. The ceiling grows like the factorial of the color count, which is what you get when the multiplying factor itself keeps growing. These are different kinds of growth, and the band between them widens without end. Fifty years of work lived inside that band, moving the floor's fixed rate from 2.24 toward 3.28 without ever changing its character.

Shortcuts were tried. Here is the most tempting one, sunk by a computation you can watch.

There are lots of orderings of a handful of items, factorially many, and any two orderings first disagree at some position. Color each pair of orderings by that position. Factorially many tables from a handful of colors would smash the question. With three items there are six orderings and only two possible colors, and if the trick worked it would beat the pentagon.

![Six orderings colored by first disagreement, with a one-color triangle found and flashed](guide/07-the-gap/orderings.gif)

It does not work. The orderings ABC, BAC and CAB pairwise first-disagree at the very same position, the first letter, so their triangle is one-colored. Nothing about three items is special; the same collision happens at every size, and the tests exhibit it. Patching the color to record more information avoids the collision only by spending far more colors, which puts you back where you started.

Other routes fail for their own reasons. Building tables from addition on a number circle turns out to be the same problem wearing different clothes, not an easier one. What every failure has in common is this: each color's net must stay triangle-free, and the cheap ways to guarantee that all quarantine every color inside its own private region. The winning idea has to let many rooms *reuse* the same color, while some global mechanism guarantees the reused pieces can never assemble a triangle. Finding that mechanism took until 2026, and it is the next three chapters.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/07.html)** and turn the idea over yourself.

## 8 · Palettes

Nothing in the next three chapters is harder than what you have already read. The construction has three moving parts, each of which is a rule simple enough to draw, and this chapter is the first: who is allowed to use which color.

The people are divided into rooms, as in chapter 5. The new ingredient is that every room is issued a **palette**: a list of colors that room deliberately refuses to use inside itself. Every other color is fair game internally. And a string between two different rooms must use a color that exactly one of the two rooms holds.

![A string between two rooms auditioning colors until one is held on exactly one side](guide/08-palettes/rooms.gif)

That little rule already kills every triangle that touches three different rooms. Fix any single color and any three rooms, and ask whether that color is held or missing in each room. A triangle across the three rooms would need its color on all three walls, held on exactly one side of each. Try to arrange it: around the triangle, held must alternate with missing at every wall, and a cycle of three cannot alternate. Some wall always has the color held on both sides or on neither.

![All eight hold-or-miss patterns for one color across three rooms, each with an unusable wall](guide/08-palettes/parity.png)

All eight patterns fail, and the tests enumerate them rather than trusting the story. So triangles across three rooms are ruled out, and the rule costs nothing. What it does not rule out is a triangle with two corners in the same room, and that is the trap of the next chapter.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/08.html)** and turn the idea over yourself.

## 9 · The trap

The dangerous triangle has two corners inside one room and one corner outside. The color on its strings is one the room actively uses, so the room contains strings of that color, and an outsider connected in by two same-colored strings might land exactly on two people the room has already joined in that color.

The defense starts by looking at one color's net inside the room. Here is the red net of the pentagon room, with its people badged into **teams**.

![The red net inside the pentagon room, with three teams and no red string inside any team](guide/09-the-trap/teams.png)

The teams are chosen so that no red string stays inside one team; every red string crosses between teams. Three teams suffice for the pentagon's red net. Now the rule that disarms the trap: all red strings arriving from any one outsider must land inside a single team.

![The trap springing when the rule is broken, and failing to spring when it is obeyed](guide/09-the-trap/trap.gif)

Watch both halves. Rule ignored, the outsider's two red strings land on two people who are red-connected, and the triangle snaps shut. Rule obeyed, the outsider's red strings land on teammates only, teammates are never red-connected, and no red triangle can involve that outsider. Strings that the rule turns away are colored instead with a color the room's palette forbids inside, which is harmless for the room automatically: a triangle needs an inside string of its color, and there are none. The tests verify both endings on exactly the colorings drawn here.

This is the point of palettes beyond the parity trick of chapter 8. A palette does not just say which colors a room avoids. It splits every arriving color into two safety cases: colors the room misses are safe by emptiness, and colors the room holds are safe by teams, provided the landing rule is enforced. Enforcing it for every pair of rooms at once, without spending new colors, is the job of the referee.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/09.html)** and turn the idea over yourself.

## 10 · The referee

Here is the enforcement problem, stripped down. A string runs from person u in one room to person v in another. The rule of chapter 9 says the team it lands on must be determined by the sender, not chosen freely. But the string's color must also be held on exactly one side, per chapter 8, and there are many candidate colors, and this must work for every pair of rooms in the construction simultaneously, using no information beyond the two endpoints themselves.

The solution is a single fixed card of symbols, written down once, before any rooms or people exist. This article calls it the **referee's card**. Here is a real one, at toy size, found and fully verified by this repository.

![The referee's card at toy size, with every choice of four columns containing a row that shows both symbols](guide/10-the-referee/referee.gif)

The card's one promise: choose any four of its columns, and some row shows every symbol within those four columns. Thirteen rows of coin flips are enough to make that hold for all seventy ways of picking four columns out of eight, and the tests check all seventy. At this toy size the promise is easy and almost any random card passes; at the sizes the real construction needs, nothing could be checked case by case, and the existence of a valid card is guaranteed instead by two counting arguments layered on top of each other. What matters downstream is only this: the card is fixed once and works for every situation at once.

Why insist that the card come first? Because a rule invented after seeing a particular pair of words could always be bent to fit that pair, and an agreement arranged after the fact guarantees nothing about the next pair. The promise has force precisely because one card, written blind, must serve every pair of rooms on every floor, forever.

From the card come two fixed answer lists, one for each direction of the conversation. Each person's teams, across the relevant colors, spell out a word. When two words meet, the promise of the card guarantees a position where one word agrees with the answer list of the other.

![Two words and the two fixed answer lists, scanned until the guaranteed agreement appears](guide/10-the-referee/meeting.gif)

That agreeing position picks the string's color, and it does so in exactly the shape chapter 9 demanded: the landing team at the receiving end is read off from the sender's word. Two red strings from the same outsider therefore land on the same team, always, and the trap never springs. The tests verify the meeting promise exhaustively at toy size: all 8192 possible words on one side, every possible word on the other, no pair escapes.

One honest caveat. The toy is real and fully checked, but its size is chosen for the eye. The real construction's smallest card has 57 rows, and the words are 57 symbols long. Nothing conceptual changes with the size; only the counting arguments do.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/10.html)** and turn the idea over yourself.

## 11 · The tower

All three parts are on the table. What remains is assembly, and one piece of bookkeeping that turns the assembly into a growing rate.

The construction is a tower of floors. The ground floor is one person. Each new floor takes a batch of fresh colors and builds many rooms, each room holding a complete copy of the floor below with its colors relabeled. Every room's palette is chosen from the enlarged pool, sized so that the colors a room holds are exactly as many as the floor below needs. Strings between rooms are colored by the referee, whose single fixed table serves every floor and every pair of rooms.

![Floors of rooms of rooms, with later floors multiplying by more than earlier ones](guide/11-the-tower/tower.gif)

The diagram is a cartoon of the shape, not a portrait of the size; the real floors are astronomically wide. The bookkeeping that matters is this. Palettes on floor after floor are drawn from a growing pool of colors, and the number of usably different palettes grows with the pool. So the number of rooms a floor can support grows as the tower rises. Each floor multiplies the table size by more than the floor before, and that is precisely the behaviour no fixed product could ever have.

Two constraints fight over the tower's height. Any two rooms on one floor must have palettes different enough that each room holds plenty of colors the other one is missing, or the referee has too few candidate colors to pick from; that forces palettes to be large, which spends colors. Colors, in turn, are what the final score divides by. Balancing the two, a tower of some height spends about the cube of that height in colors (times smaller logarithmic factors) and pays out about that height in people per color. Undo the cube: a table built with some number of colors earns a rate of about the *cube root* of its color count, divided by a logarithm.

![Flat rates of the fixed recipes against the climbing rate shape of the 2026 construction](guide/11-the-tower/base.png)

The flat lines are the whole world before 2026. The curve climbs past every one of them and keeps going. At the smallest full-scale size, the numbers are: a referee's card of 57 rows, palettes of 114 colors per floor, three floors, 342 colors in all. This repository computes those parameters from the paper's recipe and the tests pin them.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/11.html)** and turn the idea over yourself.

## 12 · What it means, and what it does not

The theorem, in the words of this article: for every color count from two upward, there is a safe table whose people-per-color rate is at least a fixed constant times the cube root of the color count divided by its logarithm. The rate climbs without bound. Erdős's 100-dollar question, whether the rate approaches something finite, is answered: it does not. His 250-dollar question, what it approaches, is answered the same way: it grows forever.

Combined with the factorial ceiling of chapter 6, the forcing size is now boxed in tightly in shape: it is the color count raised to a power that is itself proportional to the color count.

![After 2026 both the floor and the ceiling grow the same way, with only the multiple open](guide/12-what-it-means/sandwich.png)

Be equally clear about what was not settled.

```
    settled                                  still open
    -------                                  ----------
    the rate climbs without bound            the multiple: the floor gets a third,
    the forcing size is the color count      the ceiling gets one, and the truth
      to the power of about the color count  is somewhere between
    the four-color forcing size is           still somewhere between 51 and 62
```

And be clear about scale. The theorem's explicit constant is enormous, deliberately so, because the authors optimized the argument's shape rather than its constants. With that constant, the new bound does not overtake the old 3.28-per-color recipe until around ten to the sixtieth colors, and below 342 colors it says nothing at all. At every size a person will ever draw, the older constructions give bigger tables. What changed is not any record at small sizes; it is the answer to what kind of growth is possible.

There is a payoff outside the game. A safe table is secretly a code for talking over a noisy channel. Here is the classic small example of the phenomenon, re-checked by this repository's tests.

![The noisy five-symbol channel, and the five two-letter codewords that beat single letters](guide/12-what-it-means/channel.png)

Five symbols, each confusable with its neighbours. Any three symbols include a confusable pair, so single-letter messages stop at two safe words; but there are five two-letter words that pairwise differ safely somewhere, which is more per letter. Capacity is about long words, not single letters. A safe table with many colors performs the same trick at scale: its people become symbols, its colors become letter positions, and the sixteen-fold or larger table gives that many words, all mutually safe. Because the rate now climbs without bound, there are channels in which any three symbols contain a confusable pair and yet whose capacity is as large as you like. Before this result, it was not known whether such channels exist at all.

```
    1955  Greenwood and Gleason: two colors force at six, three at seventeen
    1971  Erdős, McEliece and Taylor connect the game to channel capacity
    1973  Chung: four colors force at fifty one or more
    1983  Chung and Grinstead's survey records Erdős's prizes
    1990  Graham, Rothschild and Spencer record the growth question
    1995  Alon and Orlitsky make the channel connection explicit
    2021  Schur-type recipes reach the best fixed rate, about 3.28
    2026  the rate is proved to climb without bound
```

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/12.html)** and turn the idea over yourself.

## What you can check yourself

Everything below runs from this repository, with no mathematical background needed.

```
cd multicolor-ramsey
make venv        # once
make test        # re-checks every number in this article
make figures     # re-renders every picture
```

The tests do these things, among others:

- rebuild the pentagon and the sixteen-person coloring and re-check every triangle
- walk all 32768 two-colorings of six people and confirm none is safe, and that the luckiest contain exactly two one-color triangles
- multiply the pentagon by itself and verify the 25-person, four-color product, and an 80-person, five-color one
- recompute the staircase 3, 6, 17, 66, 327 and compare the four-color step against the known range of 51 to 62
- find the referee's card at toy size, verify its promise over all seventy column choices, and verify the meeting guarantee over every pair of words
- check all eight hold-or-miss patterns of the parity rule, and both endings of the trap
- confirm the paper's own parameters: 57 rows, 114 colors per floor, 342 colors at the smallest full-scale size
- estimate where the explicit bound first overtakes the old recipes, which is around ten to the sixtieth colors

The one thing you cannot check here is the theorem. The full tower is described, not implemented, because its smallest honest floor is wider than any computer. The moving parts are implemented and verified at toy size, and the notes in this folder say exactly which claim rests on which test.

## The plain words, and the real ones

| this article says | the standard term |
|---|---|
| the triangle game | Ramsey theory for triangles, with k colors |
| a one-color triangle | a monochromatic triangle |
| a safe table | a triangle-free k-edge-coloring of a complete graph |
| the forcing size | the multicolor Ramsey number, written R(3, ..., 3) with k threes |
| people per color | the k-th root of the largest safe table size; Erdős's question asks for its limit |
| a room | a block of the recursive construction |
| a palette | the set of colors a block omits; cross-room colors come from the symmetric difference of two palettes |
| a team | one class of a proper vertex coloring of a single color's graph |
| the referee's card | the saturated matrix |
| the two answer lists | the two-sided coordinate cover, a pair of fixed maps built from the matrix |
| the tower | the recursive palette construction of the 2026 proof |
| the noisy channel payoff | the Shannon capacity of graphs with independence number two is unbounded |

The source writes the forcing size for k colors as a subscripted R, and the people-per-color limit as the limit of its k-th root, which it proves is infinite.

## Where to go next

- The source: chapter 9 of *Ten Advances in Mathematics and Theoretical Computer Science*, with its reasoning walkthrough. Both are in `docs/ten-proofs/09-multicolor-ramsey/`.
- Greenwood and Gleason, "Combinatorial relations and chromatic graphs", Canadian Journal of Mathematics 7 (1955), for the pentagon and the sixteen-person table.
- Radziszowski, "Small Ramsey numbers", the living survey of everything known at small sizes.
- Alon and Orlitsky, "Repeated communication and Ramsey graphs", IEEE Transactions on Information Theory 41 (1995), for the channel connection.
- `notes/research-content.md` in this folder, which lists every claim above and marks it as computed here, quoted from the literature, or part of the 2026 result.

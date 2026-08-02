# Design notes: how this guide is built

## The reader

Assumed to know no mathematics. Not assumed to be stupid. The test of every
paragraph is whether someone who last did algebra at school can follow it
without pausing, and whether a specialist reading over their shoulder would
call it correct.

## The order, and why

The 2026 result answers a question most readers have never heard asked, about
a growth rate most readers have never had reason to care about. So the guide
spends four chapters making the question itself feel inevitable, three
chapters on why the obvious attacks stall, and only then explains the
construction, one moving part per chapter.

1. **The game** (1) and **six is forced** (2) teach the whole subject on five
   and six dots: what a safe coloring is, and what it means for a size to
   force a triangle. Chapter 2 contains the guide's one complete proof.
2. **More crayons** (3) gives the reader the three-color record and the
   four-color embarrassment: past three colors nobody knows the answer.
3. **The question** (4) turns the table of records into the growth question
   and states Erdős's prizes. This is the destination chapter; everything
   after it is about answering it.
4. **Multiply** (5) is the classical tool: safe times safe is safe. It builds
   real intuition and a real limit: the rate per color never climbs.
5. **The ceiling** (6) is the factorial staircase from the other side, so the
   reader sees the gap: fixed base below, factorial above.
6. **The gap** (7) shows two tempting shortcuts failing, one of them by an
   exhibit this repo computes, and names the missing ingredient: reusing
   colors across rooms without ever coordinating a triangle.
7. **Palettes** (8), **the trap** (9), **the referee** (10) are the three
   moving parts of the construction, in the order the walkthrough motivates
   them: the parity rule kills three-room triangles, the label rule kills
   two-room triangles, and the fixed answer maps enforce the label rule
   without spending new colors.
8. **The tower** (11) assembles the parts and does the bookkeeping that turns
   packed palettes into a growing base.
9. **What it means** (12) states the theorem honestly, including that the
   explicit constant makes it a growth statement rather than a new record at
   drawable sizes, and gives the channel-capacity payoff.

## Rules followed here

- **No equations in the prose.** Every relation is a picture or a sentence.
  Where a symbol would appear, words appear instead: "the cube root of the
  color count, divided by its logarithm".
- **The difficulty must not spike.** Chapters 8 to 10 open by saying plainly
  that nothing new is needed and naming what is being reused. Each of the
  construction's three parts gets its own chapter and its own toy, none of
  them longer than the chapters before.
- **Plain words carry their real names.** Every invented term (safe table,
  forcing size, room, palette, team, the referee's card) has a glossary line
  at the end giving the standard term, so the reader can go and read anything
  else afterwards.
- **One word, one meaning.** "Table" is only ever the party of people;
  the referee's grid of colors is always "the referee's card" in full, and
  is introduced by contrast. "Triangle" always means three people whose three
  connections share a color.
- **Animation only where the motion is the mathematics.** The figures that
  move are: coloring the pentagon edge by edge, the pigeonhole proof playing
  out, blowing a pentagon up into a pentagon of pentagons, sorting neighbors
  into color groups, three orderings closing a triangle, cross edges picking
  colors between rooms, the trap springing and then failing to spring, the
  referee's row search, and the tower stacking stages. Everything else is a
  static chart. Every non-looping GIF holds its last frame for about two and
  a half seconds via `end_pad`. No rotating shots: nothing in this topic is
  three dimensional, so no camera pretends otherwise.
- **A picture made only of words is not a picture.** Word-only comparisons
  are plain quoted blocks in the text. Only figures with real graphical
  content are images.
- **Every step of the progression is playable.** Each chapter has a self
  contained page under `docs/multicolor-ramsey/play/`, built by
  `build_interactive.py`, with no libraries and no network. The flagship is
  the chapter 2 page, where the reader tries to two-color six people and the
  page finds the triangle they were forced into. The JavaScript re-implements
  parts of `ramsey_guide`, and `tests/test_interactive.py` compares the two
  at sample points so they cannot drift apart.
- **Do not oversell.** The article says explicitly that the theorem is a
  statement about growth, that at drawable sizes the older records are
  bigger, and that the full construction is described, not implemented. The
  toy parts that are implemented are labeled as toys.

## Toolchain decisions

- **matplotlib and Pillow GIFs** for everything, as in the other topics: they
  render anywhere, embed inline on GitHub, and need no LaTeX. Animations are
  snapped to an even pixel size first, because an odd width comes out of the
  GIF writer sheared.
- **Colorings are small integer matrices** and the triangle check walks every
  triple. Honest and slow beats clever and doubted at the sizes drawn here.
- **The edge palette is fixed across the whole guide**: color 0 is the same
  red in every chapter, color 1 the same blue, so a reader who learns the
  pentagon in chapter 1 recognises it inside the products of chapter 5.
- **The chapter READMEs are generated** from ARTICLE.md by `build_guide.py`,
  exactly as in the sphere packing topic, because hand-kept copies have
  already drifted once in this repository.

## Correctness guardrails

- The six-person forcing is checked over all 32768 colorings, so chapter 2's
  proof is backed by exhaustion, not just by the pigeonhole story.
- The seventeen-person forcing for three colors is *not* checkable this way
  and the article says it is quoting.
- The referee's promises at alphabet two (saturation, few exceptional
  columns, the meeting guarantee) are verified exhaustively, and the article
  still says plainly that the union-bound arithmetic, not the toy search, is
  what carries the real sizes.
- The trap chapter's two colorings differ only in whether the label rule is
  obeyed, and the tests pin both outcomes, so the moral is a computation.
- The growth chapter states the crossover honestly: with the printed
  constant, the new bound passes the old record around ten to the sixtieth
  colors. The tests compute that estimate.

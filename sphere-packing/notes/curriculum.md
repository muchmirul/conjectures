# Design notes: how this guide is built

## The reader

Assumed to know no mathematics. Not assumed to be stupid. The test of every
paragraph is whether someone who last did algebra at school can follow it
without pausing, and whether a specialist reading over their shoulder would
call it correct.

## The order, and why

The hard result is about the *limit of a method*, which is a step further out
than most popular mathematics goes. A reader who does not first understand what
the method is cannot be told that it has a ceiling. So the guide spends six
chapters on the method and only then asks the question the paper answers.

1. **The question** (1) and **high dimensions are strange** (2) set the problem
   up and give the reader the one fact that makes the rest surprising: room
   collapses as dimensions are added.
2. **You cannot check** (3) motivates a certificate before defining one.
3. **The certificate** (4) and **counting twice** (5) are the method.
4. **What certificates prove** (6) grounds it in numbers this repo computed.
5. **Is there a ceiling** (7) poses the actual research question.
6. **Balancing** (8), **the wall** (9), **the witness** (10) are the proof, in
   its two halves.
7. **They meet** (11) and **what it means** (12) state the result and fence off
   what it does not say.

## Rules followed here

- **No equations in the prose.** Every relation is a picture or a sentence.
  Where a symbol is unavoidable (pi, the dimension) it is named in words.
- **The difficulty must not spike.** Chapter 8 opens by saying plainly that
  nothing new is needed and naming what is being reused, because chapters 8 to
  10 are where a guide like this usually loses people.
- **Plain words carry their real names.** Every invented term (certificate, the
  two sign rules, the balanced function, the wall) has a glossary line giving
  the standard term, so the reader can go and read anything else afterwards.
- **One word, one meaning.** "Certificate" is only ever the admissible
  function. The word "bound" is never used for both a density and a radius in
  the same passage.
- **Animation only where the motion is the mathematics.** Ten figures move:
  the rearrangement of circles, the three rotating scenes (the stack, the ball
  in its box, the four dimensional shadow), the dial that breaks a rule, the
  two counts, the subtraction, the shrinking radius, the sliding saddle radius,
  and the closing gap. The other fourteen are static charts. Every non-rotating
  GIF holds its last frame for two and a half seconds via `end_pad`; the three
  rotating ones loop seamlessly and deliberately do not.
- **Dimension is shown, not asserted.** Three dimensional scenes turn the
  camera all the way round. The four dimensional one turns the object in a
  plane involving the fourth axis and draws the shadow.
- **A picture made only of words is not a picture.** Nine figures started life
  as PNGs containing nothing but labelled boxes. They are now plain quoted
  typing in the text, which is searchable, selectable, readable by a screen
  reader, and does not need re-rendering when a word changes. Only figures with
  real graphical content stay as images: 10 animations and 14 charts.
- **Every step of the progression is playable.** Reading that a certificate
  breaks when you turn a dial is weaker than turning the dial. Each chapter has
  a self contained page under `docs/sphere-packing/play/`, built by
  `build_interactive.py`, with no libraries and no network so it works offline.
  The JavaScript re-implements part of `sphere_packing_guide`, so
  `tests/test_interactive.py` runs both and compares them; two copies of a
  formula drift otherwise.
- **Do not oversell.** The article says explicitly that the certificates found
  here are numerical, weaker than the literature's, and that the theorem itself
  is described rather than implemented.

## Toolchain decisions

- **matplotlib and Pillow GIFs** for everything, as in the other two topics:
  they render anywhere, embed inline on GitHub, and need no LaTeX. Animations
  are snapped to an even pixel size first, because an odd width comes out of
  the GIF writer sheared.
- **No sympy.** Nothing here needs symbolic algebra; the quantities are
  gamma functions, Laguerre polynomials and numerical integrals.
- **Logs everywhere for high dimensions.** The unit ball's volume underflows a
  double by dimension 340, so `log_ball_volume` is the primitive and plain
  volumes are derived from it.
- **The chapter READMEs are generated** from ARTICLE.md by `build_guide.py`.
  The other two topics keep the same prose in both places by hand, and the
  Kakeya copies have already drifted 91 lines apart. Generating them removes
  the failure mode.

## Correctness guardrails

- The Cohn-Elkies bound needs *both* sign rules; a function obeying one of them
  proves nothing. The tuning animation exists to make that concrete.
- A certificate proves an upper bound on density. It never says a packing
  achieving it exists, and the article never suggests otherwise.
- The 2026 theorem bounds the *method*, not the packing problem. Chapter 12
  exists to stop the reader concluding that sphere packing is now solved in
  high dimensions.
- The two sign uncertainty constants share a limit but are different in every
  dimension. Saying only the first half would be a real error, so both are
  stated.
- The certificates in `examples.py` were found with a margin and are re-checked
  without one, on a grid thirty times finer. Any search allowed right up to the
  constraint boundary finds a function that passes on its own grid and fails on
  a finer one; this was observed here before it was fixed.

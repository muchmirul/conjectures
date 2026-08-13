# Prime Numbers and Two Thirds of the Zeros

A visual guide to the Riemann zeta function, its zeros, and the 2026 paper
proving that at least two thirds of them are simple and on the critical line,
written for a reader with no mathematical background.

- **[Read it on one page](ARTICLE.md)**, or on the web at
  [muchmirul.github.io/conjectures/zeta-critical-line/](https://muchmirul.github.io/conjectures/zeta-critical-line/)
- **[Read it chapter by chapter](guide/00-start-here/README.md)**, thirteen
  chapters of about five minutes each

## What it covers

The guide begins with the primes and the wobble in their staircase, then
builds the zeta landscape, the strip and the critical line. It presents the
explicit formula as a duet between zeros and primes, and then states the
Riemann hypothesis together with the record race from Hardy to five
twelfths; and the whole of the 2026 paper: the four counting functions, the
microphone family and its Gram table, the zero side read by Sylvester's
inertia (bowls and saddles), the prime side read by Montgomery's two moments,
the rank-trace inequality, the assembly of 2/3 and 5/6, the optimised-window
constants 0.6725 and 0.83625, the method's 0.68185 ceiling, the extensions to
Dirichlet L-functions and the derivative of the completed zeta, the numerical
illustrations, the Lean formalisation, and the Appendix C account of how the
argument was found.

The source is "More than two thirds of the zeros of the Riemann zeta function
lie on the critical line" (Claude, Anthropic, August 2026). A copy is kept in
`docs/zeta-critical-line/paper/`, and it is published on the Anthropic CDN.

## Running the code

```bash
make venv        # create the shared ../.venv and install this package
make test        # re-verify every number the guide quotes
make figures     # re-render every figure into guide/
make guide       # rebuild the chapter READMEs from ARTICLE.md
make play        # rebuild the playable pages in ../docs/zeta-critical-line/play/
make docs        # rebuild ../docs/zeta-critical-line/index.html from ARTICLE.md
```

## Play with it

Nine chapters have a page where the numbers in them are controls you can
move: [docs/zeta-critical-line/play/](../docs/zeta-critical-line/play/index.html).
Steer the zeta path into the origin, add zero-waves until the prime staircase
assembles, let the primes point back at the zeros, mix a bowl with a saddle
and watch the see-saw law hold, and turn the dial that sets every constant in
the paper. The pages carry no libraries and make no network requests, so they
work offline and straight from a file. Their arithmetic is checked against
the Python library in `tests/test_interactive.py`, so the two cannot drift
apart.

## Layout

```
ARTICLE.md  the whole guide on one page, and the single source for the prose
guide/NN-slug/README.md   one chapter per folder, generated, figures alongside
src/zeta_guide/  core.py (zeta, the zeros, the explicit formula, the toy
                 listening family, the paper's constants and inequalities),
                 examples.py (the named numbers), plotting.py (palette, 3D
                 helpers, GIFs), data/zeros300.txt (the shipped zero table)
  viz/          one figure script per chapter
tests/      re-checks every computed number in the guide
notes/      research notes: every claim, marked computed, classical or recent
build_docs.py        turns ARTICLE.md into ../docs/zeta-critical-line/index.html
build_guide.py       turns ARTICLE.md into the chapter READMEs
build_interactive.py writes the playable page for each chapter
```

## What this repository proves, and what it only describes

The tests recompute a sample of the 300 shipped zero heights with independent
software and confirm zeta vanishes at all of them. They also verify the
zero-counting formula against the table, rebuild the prime staircase from
zero-waves and
watch the error fall; build the 44-microphone toy table twice, from zeros and
from primes, and confirm agreement to about two parts in a hundred million;
verify bowls, saddles and the see-saw bound on real and synthetic
configurations; attack the rank-trace inequality with thousands of random
instances; pin every constant of the paper, from 2/3 and 5/6 through 0.6725,
0.83625 and the 0.68185 ceiling; and confirm the certificate never exceeds
the truth on hostile synthetic configurations.

They do not prove the theorem. The 2026 result lives at the limit of
ever-larger heights, where no finite table reaches; the paper's own numerics
section opens by saying no theorem depends on any computation, and the same
holds here. `notes/research-content.md` marks every claim in the article as
computed here, quoted from the literature, or part of the 2026 paper.

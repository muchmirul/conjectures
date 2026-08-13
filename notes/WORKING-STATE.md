# Working state, 2026-08-13

Scratch notes for work in progress. Delete when everything below has landed.

**Goal 1, the style revision, is finished.** Every piece of prose in the
repository now passes `notes/style_check.py`: 8 articles, 26 hand-written
chapter files, 27 generated chapter files, 7 READMEs, the research notes, the
play-page prose in all four `build_interactive.py` files, both landing pages
and the hand-maintained Jacobian page. The only file that still reports
problems is `notes/writing-style.md` itself, which quotes the banned phrasings
as examples of what to avoid.

**Goal 2, the mathematics in condensed-math, is 1 chapter of 24.** The
infrastructure is complete; the writing is not. See below.

## Goal 1: revise all writing to the house style

Done. The rules are stored verbatim at `notes/writing-style.md`, and
`notes/style_check.py` enforces them:

    .venv/bin/python notes/style_check.py compare <before> <after>   # skeleton
    .venv/bin/python notes/style_check.py rules   <file>             # rules

The "skeleton" is every heading, image line, table row, fenced block and link
target. If it is unchanged, a revision moved prose and nothing else. Every
revised file was checked both ways.

### How it was done, and one thing to know before repeating it

The first attempt used subagents to rewrite whole files. That worked for style
and failed badly for accuracy: an adversarial review found 24 changed claims in
the first six articles, and 111 more in Kakeya and Jacobian. Several were
plainly false. One told the reader the test suite "prints its numbers" when the
tests are pytest assertions that print dots. Another promised that editing one
recipe redraws both of a chapter's figures when only one figure reads it. A
third turned "the subject is **not** a repackaging" into "is **more than** a
repackaging", conceding the opposite point.

Kakeya and Jacobian were reverted to their originals and then revised again by
hand, fixing only the specific problems the checker names rather than rewriting
paragraphs wholesale. That produced 0 problems with skeletons intact and no
claim drift at all. **Targeted fixes, not wholesale rewriting, is the method
that works here.**

The findings from the discarded attempt are kept at `notes/pending-fixes/`.
They are a useful independent review of the prose in their own right, and
several of them point at real weaknesses that the targeted pass did not
address. Read them with one caveat: the "after" text each finding quotes comes
from the revision that was reverted, so it is not in the repository any more.
The "before" text, and the reasoning about what the revision broke, are still
accurate.

## Goal 2: condensed-math must include the mathematics

The owner asked for the real mathematics in the condensed-math articles, with
every statement paired with an intuitive explanation and with a simulation.
That reverses the older rule for this topic, which kept formulas out of the
prose entirely.

### Done

The infrastructure is complete and working. `condensed-math/build_docs.py`
loads MathJax, understands `$inline$` and ```math fences, and boxes each
chapter's statement together with its plain reading and its simulation as
`<section class="mathpair">`, opened by the heading `### The mathematics` and
closed at the next `##` so the activity iframe falls inside the box.

`tests/test_guide.py` no longer forbids formulas. It now checks that wherever a
statement exists it is paired with a "Reading the symbols" paragraph, an "In
the simulation" paragraph and a link to that chapter's activity, that the
built page renders one boxed pair per statement with MathJax loaded, and it
reports coverage.

Part one chapter one carries the pattern block the rest are meant to copy. It
runs lead-in, display statement, "Reading the symbols", "Why it matters", "In
the simulation", and then the existing activity link. Copying that shape keeps
the three parts consistent.

### Not done

**1 of 24 chapters.** The workflow written to produce the other 23 lost all 23
agents to the usage limit before any of them wrote anything.

    .venv/bin/python -m pytest condensed-math/tests/test_guide.py \
        -k how_much_of_the_mathematics -q -s

prints the current coverage.

**To resume:** re-run the workflow script at
`workflows/scripts/condensed-math-add-mathematics-*.js`. One thing to fix
before re-running: it puts 23 agents on only three files, eight chapters per
file, so concurrent Edit calls can silently drop a block. Either give each
agent worktree isolation, or serialise the eight chapters within each part and
run the three parts in parallel. After it runs, count the
`### The mathematics` headings per part; each must be 8.

Also reconcile `CLAUDE.md`, which still carries the older rule that equations
must never appear in the prose. That rule now holds for every topic except
condensed-math, where the owner asked for the opposite.

## Rebuilding

    cd condensed-math && make all && make test
    cd sphere-packing && make guide docs play
    cd multicolor-ramsey && make guide docs play
    cd zeta-critical-line && make guide docs play
    cd kakeya-conjecture && make docs
    make test                                  # whole repo, about 3.5 minutes

Kakeya's and Jacobian's chapter READMEs are hand-written, not generated. There
is no `build_guide.py` for either, so those files must be edited directly and
kept in step with their articles by hand.

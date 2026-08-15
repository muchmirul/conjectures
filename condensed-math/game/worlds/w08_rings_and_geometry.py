"""World 8.  Multiplication, the exponent ceiling, and what it was all for.

Part three of the written guide, at the level of intuition the game can carry
honestly: a ring carrying its own rule about which sums land, the reason the
real line's rule cannot have an exponent above one, and the duality theorem
that falls out of an adjoint once the setting is right.
"""

from __future__ import annotations

from ..model import Ask, Brick, Math, Name, Play, Say, Try, World


BRICKS = (

    Brick(
        slug="multiplying-too",
        title="A ring that carries its own rule",
        idea="An analytic ring is a ring together with a rule saying which "
             "sums land &mdash; and the rule must survive multiplication.",
        need=(
            "An abelian group: adding, a zero and opposites.",
            "Solidity: a rule saying which endless sums land.",
        ),
        concept=(
            Say("Everything so far could add. Most objects worth studying can "
                "also multiply: numbers, polynomials, functions on a space. A "
                "collection with both operations, behaving together in the "
                "ordinary way, is called a ring."),
            Say("Now bolt on the rule about which sums land &mdash; and notice "
                "this is a deliberate echo of the mistake from world 2. This "
                "time the rule is not a second layer sitting beside the first. "
                "It is a demand the ring itself has to satisfy, phrased so "
                "that multiplication cannot escape it."),
        ),
        intuition=(
            Say("A bolted-on rule drifts. If sums could land in a way the "
                "multiplication ignored, you could multiply two well-behaved "
                "things and get something whose sums no longer land, and the "
                "completion would stop being compatible with the algebra "
                "&mdash; the world-2 failure in a new costume."),
            Ask(
                "Why insist that the rule interact with the multiplication?",
                (
                    ("Otherwise the two layers drift apart again",
                     "That is the design principle, learned the hard way. The "
                     "demand is written into the definition so the drift "
                     "cannot start: measures on two probes must multiply to a "
                     "measure on the pair."),
                    ("Convenience",
                     "It is anything but convenient to check; the definition "
                     "is more demanding than it looks. The reason is "
                     "structural: without the interaction, the completion and "
                     "the multiplication would disagree."),
                    ("So the sums are shorter",
                     "Nothing gets shorter. What is gained is that a "
                     "completion can be performed without destroying the "
                     "multiplication &mdash; and that is what makes geometry "
                     "possible on top of it."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the whole numbers with the base-2 rule, and the two "
                    "sums 1 + 2 + 4 + &hellip; and 1 + 2 + 4 + &hellip; again.",
                    "You know each lands, at &minus;1. Multiply the two "
                    "answers.",
                    "Now ask what the product of the two sums ought to be, "
                    "term by term, and whether that new sum lands under the "
                    "same rule.",
                ),
                found="The product of the answers is 1. Multiplying the sums "
                      "term by term gives a new endless sum of products of "
                      "powers of two, and every term is still divisible by "
                      "ever higher powers of two, so it lands under the very "
                      "same rule &mdash; at 1, as it must. That agreement is "
                      "not automatic for an arbitrary pairing of a ring with a "
                      "notion of which sums land; it is exactly the condition "
                      "an analytic ring is required to satisfy, and here you "
                      "have watched a case where it holds.",
            ),
            Name(
                plain="a ring that knows which sums land",
                standard="an analytic ring",
                notation="(A, M), &nbsp; A a condensed ring, M its measures",
                why="M records, for each probe, which formal combinations of "
                    "points count as having an answer. The two examples that "
                    "carry everything are the whole numbers with the base-p "
                    "rule, and the real numbers with their own rule.",
            ),
            Math(
                statement="A<sub>&#9632;</sub>[S] &otimes; "
                          "A<sub>&#9632;</sub>[T] &rarr; A<sub>&#9632;</sub>"
                          "[S &times; T]",
                reading="A<sub>&#9632;</sub>[S] is the module of measures on "
                        "the probe S: the formal combinations of its points "
                        "that the ring agrees to sum. The arrow is the "
                        "compatibility demand &mdash; measures on two probes "
                        "multiply to a measure on the pair. That single arrow "
                        "is what stops the completion and the multiplication "
                        "from drifting apart.",
                cite="Lecture VII, analytic rings, page 51 onwards",
                url="https://arxiv.org/pdf/2605.03658v1#page=51",
            ),
        ),
        hold="An analytic ring is a ring together with a rule for which sums "
             "land, and the rule must survive multiplication.",
    ),

    Brick(
        slug="the-exponent-ceiling",
        title="Why one is the ceiling",
        idea="Merging boxes may not increase a measure, and that single demand "
             "forces the exponent in the real line's rule to be at most one.",
        need=(
            "Measures: weights on the boxes of a probe.",
            "That merging boxes adds their weights together.",
        ),
        concept=(
            Say("The real line needs its own rule, and the natural candidates "
                "measure the size of a list of weights by raising each to a "
                "power, adding, and taking the matching root. The power is the "
                "exponent."),
            Say("One demand fixes it. Merging two boxes into one is a "
                "legitimate coarsening of a probe, and a coarser view of a "
                "measure must not weigh more than the measure itself. So "
                "merging may never increase the size."),
        ),
        intuition=(
            Say("A coarse picture is a <em>view</em> of the fine one, not a "
                "different object. If looking at something less carefully "
                "could make it bigger, the two stages of the probe would be "
                "recording incompatible things, and the tower would stop being "
                "one measure."),
            Ask(
                "What exactly goes wrong above one?",
                (
                    ("Coarsening a probe would make the measure grow",
                     "And that is incoherent. Above one the inflation factor "
                     "is the number of merged boxes raised to a positive "
                     "power, so it can be made as large as you like &mdash; "
                     "there is no bound to fall back on."),
                    ("Nothing, it just gives a different theory",
                     "There is no theory to have. The compatibility between "
                     "stages is what makes a measure a single object rather "
                     "than a pile of unrelated weightings, and above one that "
                     "compatibility cannot be bounded."),
                    ("The root is hard to compute",
                     "Computation is not the obstacle &mdash; the page "
                     "computes it as you turn the dial. The obstacle is that "
                     "the size increases under a coarsening, which no measure "
                     "may do."),
                ),
                after="So the real line's rule uses exponents at most one, and "
                      "the ceiling is forced by a fact about merging boxes "
                      "that you can watch happen.",
            ),
        ),
        experiment=(
            Play(
                widget="merge",
                prompt="Turn the exponent and watch what merging four equal "
                       "boxes does to the size.",
                notice="Below one, merging shrinks. At exactly one, merging "
                       "leaves the size alone. Above one it inflates, by a "
                       "factor that grows with the number of boxes merged, so "
                       "no bound survives. The page computes the ratio "
                       "directly from the weights and also from the closed "
                       "form n<sup>1&minus;1/p</sup>; the two agree, which is "
                       "the check that the picture is not a cartoon.",
                params={"boxes": 4},
            ),
            Name(
                plain="the exponent cannot pass one",
                standard="the &#8467;<sup>p</sup> norms, and why p &le; 1",
                notation="&#8214;x&#8214;<sub>p</sub> = "
                         "( &sum; |x<sub>i</sub>|<sup>p</sup> )"
                         "<sup>1/p</sup>",
                why="At p = 1 the size is just the total weight and merging is "
                    "exactly neutral. Below 1 the unit ball stops being convex "
                    "&mdash; visibly so &mdash; and that is the regime the "
                    "real line's analytic structure lives in.",
            ),
            Math(
                statement="worst merge ratio for n boxes = "
                          "n<sup>1 &minus; 1/p</sup> &nbsp;&middot;&nbsp; "
                          "&le; 1 &nbsp;&hArr;&nbsp; p &le; 1",
                reading="The exponent 1 &minus; 1/p is negative below one, zero "
                        "at one, and positive above it. So the worst inflation "
                        "from merging n boxes is less than one, exactly one, "
                        "or unbounded in n, according to where p sits. That "
                        "single line is the whole reason for the ceiling.",
                cite="Lecture VII, the real analytic ring, page 55 onwards",
                url="https://arxiv.org/pdf/2605.03658v1#page=55",
            ),
        ),
        hold="Merging boxes may not increase a measure, and that alone forces "
             "the exponent to be at most one.",
    ),

    Brick(
        slug="near-the-edge",
        title="Functions that fade out at the edge",
        idea="Keeping only the functions that fade out before the edge is what "
             "makes a total over an unbounded space finite.",
        need=(
            "An analytic ring: a ring with a rule for which sums land.",
            "The idea of a space having an edge, or a beyond.",
        ),
        concept=(
            Say("Geometry begins once you can talk about functions on a piece "
                "of a space rather than on all of it. The delicate case is a "
                "piece with an edge: what should a function do as it "
                "approaches the boundary of where it is defined?"),
            Say("Two answers are useful. Keep only the functions that fade out "
                "before the edge, or keep all of them and remember the edge "
                "separately. Both are needed, and the relation between them "
                "carries the information about the edge."),
        ),
        intuition=(
            Say("It is the same instinct as everywhere else in this game: an "
                "operation must be defined without an infinite amount of the "
                "space taking part. Fading out is what makes a total finite, "
                "just as landing was what made an endless sum an answer."),
            Ask(
                "Why insist on the functions that fade out?",
                (
                    ("So they can be totalled without reaching the edge",
                     "That is the reason. Fading out is what makes an integral "
                     "over an unbounded space converge, and the whole of "
                     "compactly supported cohomology is built on it."),
                    ("Because the others are badly behaved",
                     "The others are perfectly respectable; they simply cannot "
                     "be totalled. Both families are kept, and it is the "
                     "comparison between them that carries the information "
                     "about the edge."),
                    ("Tradition",
                     "It predates condensed mathematics by a long way, but it "
                     "is not tradition: fading out is the condition that makes "
                     "the total converge."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the function that is 1 everywhere on the whole real "
                    "line and try to total it.",
                    "Take the function that is 1 on the interval from 0 to 1 "
                    "and 0 elsewhere, and total that.",
                    "Now take a function that decays but never quite reaches "
                    "zero, and ask which of the two it behaves like.",
                ),
                found="The constant function has no finite total; the one that "
                      "switches off does, and the total is 1. The decaying one "
                      "may or may not, and which it is depends on how fast it "
                      "decays &mdash; which is precisely why <em>fading "
                      "out</em> has to be a stated condition rather than a "
                      "hope. Compactly supported means the strong version: the "
                      "function is exactly zero outside some bounded piece, so "
                      "the total is a finite sum and no convergence question "
                      "arises.",
            ),
            Name(
                plain="functions that fade out before the edge",
                standard="compactly supported cohomology",
                notation="R&Gamma;<sub>c</sub>(X, F)",
                why="The subscript c is the fading-out condition. In the "
                    "condensed setting this construction stops being a "
                    "special-purpose definition and becomes one of six "
                    "operations that fit together automatically.",
            ),
            Math(
                statement="j<sub>!</sub> &nbsp;&#8867;&nbsp; j<sup>*</sup> "
                          "&nbsp;&#8867;&nbsp; j<sub>*</sub>",
                reading="j is the inclusion of an open piece. The turnstile "
                        "&#8867; means <em>is left adjoint to</em>: a "
                        "systematic pairing in which one construction is "
                        "determined by another. j<sub>!</sub> extends a "
                        "function by zero beyond the piece, j<sup>*</sup> "
                        "restricts to it, and j<sub>*</sub> pushes forward. "
                        "The fading-out condition is what makes the first of "
                        "these exist.",
                cite="Lectures VIII to X, page 60 onwards",
                url="https://arxiv.org/pdf/2605.03658v1#page=60",
            ),
        ),
        hold="Functions that fade out before the edge are what make totals "
             "over an unbounded space finite, and they are one of six "
             "operations.",
    ),

    Brick(
        slug="duality",
        title="The theorem the course was pointing at",
        idea="In this setting duality is not constructed. It is the existence "
             "of a partner to the extend-by-zero operation, forced by a formal "
             "pairing.",
        need=(
            "Compactly supported functions, and the pairing of constructions "
            "called an adjoint.",
        ),
        concept=(
            Say("Duality says that a shape's information in low degrees and "
                "its information in high degrees are two readings of one "
                "thing. It is old, it is central, and classically it is proved "
                "by hand, case by case, with conditions attached."),
            Say("Here it appears instead: the operation that extends by zero "
                "has a partner determined by general nonsense, and that "
                "partner is the dualising object. The theorem becomes the "
                "existence of an adjoint."),
        ),
        intuition=(
            Say("An adjoint is a partner that is determined, not chosen. When "
                "a construction that used to be assembled by hand under "
                "hypotheses turns out to be one, the hypotheses stop being "
                "needed: the work has moved into the foundations and is done "
                "once."),
            Ask(
                "Why is <em>falls out of an adjoint</em> a strong claim?",
                (
                    ("Because it removes the case-by-case hypotheses",
                     "That is the gain. A statement forced by a formal pairing "
                     "holds wherever the pairing does, so the conditions "
                     "attached to the classical proofs stop being needed. "
                     "Generality is not the point in itself; not having to "
                     "re-prove it in every new situation is."),
                    ("Because adjoints are unique",
                     "True and useful &mdash; the partner is determined, not "
                     "chosen &mdash; but the real gain is that a construction "
                     "which used to be assembled by hand now exists "
                     "automatically."),
                    ("Because it is shorter",
                     "The proof is not short; the setting was expensive to "
                     "build. What changes is that the work is done once, in "
                     "the foundations, instead of once per theorem."),
                ),
                after="That is what the machinery of the first seven worlds "
                      "was for. Not elegance: the ability to prove things once "
                      "and keep them.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Count the ingredients the eight worlds spent on this: the "
                    "change of object, the gluing rule, the abelian setting, "
                    "solidity, the analytic ring.",
                    "For each one, say what would break in the duality "
                    "statement if it were removed.",
                    "Then decide whether you would have accepted the cost, "
                    "knowing the payoff.",
                ),
                found="Remove the change of object and the leftovers have "
                      "nowhere to live, so no construction involving quotients "
                      "is reliable. Remove gluing and local answers cannot be "
                      "assembled, so nothing about pieces of a space can be "
                      "said. Remove the abelian setting and the two "
                      "measurements lie, so every exactness argument is "
                      "unsound. Remove solidity and infinite sums have no "
                      "answers, so there is no analysis. Remove the analytic "
                      "ring and there is no multiplication to do geometry "
                      "with. Every ingredient is load-bearing for the last "
                      "line, which is the honest answer to <em>why so much "
                      "machinery</em>.",
            ),
            Name(
                plain="high and low degrees are two readings of one thing",
                standard="Poincar&eacute;&ndash;Verdier duality, from the six "
                         "operations",
                notation="f<sup>!</sup> right adjoint to f<sub>!</sub>",
                why="The upper-shriek is the exceptional inverse image, and "
                    "the dualising complex is what it produces from a point. "
                    "In the condensed setting it exists by general nonsense "
                    "rather than by construction.",
            ),
            Math(
                statement="R Hom( f<sub>!</sub> A, B ) &#8801; "
                          "R Hom( A, f<sup>!</sup> B )",
                reading="Read: maps out of the extended-by-zero object are the "
                        "same as maps into the exceptionally pulled-back one. "
                        "The R marks a derived construction, meaning the "
                        "bookkeeping is done at the level of complexes so that "
                        "no information is lost when things fail to be exact. "
                        "Duality theorems are read off from this "
                        "correspondence rather than proved separately.",
                cite="Lecture XI, page 78 onwards",
                url="https://arxiv.org/pdf/2605.03658v1#page=78",
            ),
        ),
        hold="Duality stops being a construction and becomes the existence of "
             "an adjoint, which is why the foundations were worth rebuilding.",
    ),

    Brick(
        slug="where-you-stand-now",
        title="Where you stand",
        idea="You now hold the shape of the subject and the vocabulary to read "
             "the lectures. The proofs are what remain.",
        need=(
            "Everything from worlds 1 to 8.",
        ),
        concept=(
            Say("You started by putting three things on a table. You now know "
                "why a set with a distance on it is two structures badly "
                "glued, what replaces it, why the replacement is not a loss, "
                "how an endless sum acquires exactly one answer, and what the "
                "whole apparatus buys."),
            Say("None of it was taken on trust. The failure was one you ran, "
                "the probe was one you split, the ghost was one you watched "
                "refuse to settle, the sum was one you saw land, and the "
                "exponent ceiling was one you pushed past and saw break."),
        ),
        intuition=(
            Say("What a route like this gives is not the ability to prove the "
                "theorems. It is the ability to read a definition and know "
                "what it is <em>for</em> &mdash; which is the part that "
                "re-reading a text does not supply, and the part that makes "
                "the proofs approachable."),
            Ask(
                "What is the honest description of what you now have?",
                (
                    ("The shape of the subject, and the vocabulary to read it",
                     "That is exactly it, and it is worth a great deal. You "
                     "can now open the lectures and recognise what the "
                     "definitions are for. The proofs remain ahead."),
                    ("A working knowledge of condensed mathematics",
                     "Further than the game can honestly claim. What you have "
                     "is the intuition and the vocabulary; working knowledge "
                     "comes from the proofs, and the lectures are where they "
                     "are. The gap is real, and much smaller than it was eight "
                     "worlds ago."),
                    ("A set of stories",
                     "More than that. Every story here was tied to a "
                     "computation you can rerun, and the names you were given "
                     "are the names the literature uses. Stories with the "
                     "right names attached are how a subject becomes "
                     "readable."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Open the lectures at page 9 and read Example 1.9.",
                    "Read Theorem 1.10 immediately after it.",
                    "Ask yourself whether you can say, without help, what "
                    "problem the example poses and what the theorem does about "
                    "it.",
                ),
                found="If you can &mdash; the example is the bridge, both "
                      "measurements read zero and the objects are not the "
                      "same, and the theorem says the repaired world does not "
                      "have that defect &mdash; then you are reading a "
                      "research text in a subject you had never met a few "
                      "hours ago, unaided. That was the aim. The three parts "
                      "of the written guide in this repository take the same "
                      "route again with a simulation in every chapter, and "
                      "every number they quote is recomputed by their own "
                      "tests.",
            ),
            Name(
                plain="what you have been through",
                standard="Lectures I to XI of Scholze's <em>Lectures on "
                         "Condensed Mathematics</em>",
                notation="Cond(Set), Cond(Ab), Solid, analytic rings, six "
                         "operations",
                why="Joint work with Dustin Clausen, recorded from a course "
                    "taught in Bonn. The written guide beside this game covers "
                    "the same ground in three parts, chapter by chapter.",
            ),
            Math(
                statement="Top<sub>cg</sub> &#8674; Cond(Set) "
                          "&#8594; Cond(Ab) &#8594; Solid &#8594; "
                          "(A, M) &#8594; six operations",
                reading="The whole route in one line, read left to right: "
                        "spaces embed into condensed sets; adding gives "
                        "condensed abelian groups; demanding that endless sums "
                        "land gives solid ones; adding multiplication gives "
                        "analytic rings; and geometry over those produces the "
                        "six operations and duality. Each arrow was one or two "
                        "worlds of this game.",
                cite="Lectures on Condensed Mathematics, arXiv:2605.03658",
                url="https://arxiv.org/abs/2605.03658",
            ),
        ),
        hold="You have the shape of the subject and the vocabulary to read the "
             "lectures. That was the whole aim.",
    ),
)


WORLD = World(
    number=8,
    slug="rings-and-geometry",
    title="Multiplying, and what it was all for",
    promise="By the end you will have pushed an exponent past the point where "
            "the arithmetic breaks, and you will know what the eight worlds "
            "were buying.",
    bricks=BRICKS,
)

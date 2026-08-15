"""World 6.  The repair, checked against the specification of world 3.

The ghost quotient exists, the two measurements can be trusted again, the old
spaces are still inside unharmed, and the holes of a shape survive the move.
Four demands, four bricks, in the order they were written down.
"""

from __future__ import annotations

from ..model import Ask, Brick, Math, Name, Play, Say, Try, World


BRICKS = (

    Brick(
        slug="the-ghost",
        title="Make the missing information visible",
        idea="In the condensed world the leftover of the bridge is zero on "
             "points and non-zero on larger probes: the object world 3 said "
             "would be needed.",
        need=(
            "A condensed set: the table of answers obeying cut and glue.",
            "The cokernel: what a map missed, seen by declaring the reached "
            "part to be zero.",
        ),
        concept=(
            Say("Take the bridge again, now living in the new world. The dust "
                "and the ruler are both tables of answers, and the bridge is a "
                "map of tables: row by row, it sends each answer of the dust "
                "to the corresponding answer of the ruler."),
            Say("The leftover is computed row by row. In the row for a single "
                "point, the two collections of answers coincide, so nothing is "
                "left over. In a row for a bigger probe, the ruler admits "
                "walks the dust does not, and those are exactly the leftover."),
        ),
        intuition=(
            Say("A continuous map into the dust must be constant on some box of "
                "some stage &mdash; it has to settle down, because arriving is "
                "forbidden. So to find something in the leftover you want a "
                "continuous function that refuses to be constant on any box, "
                "at any stage. One exists, and it is easy to write down: read "
                "the box's address as a binary number."),
            Ask(
                "How can something have no points and still not be nothing?",
                (
                    ("Because points are just one row of the table",
                     "That is the whole answer. In the old setting the points "
                     "<em>were</em> the object, so empty meant nothing. Here "
                     "the points are one row among many, and a table can be "
                     "empty in that row and full further down. Nothing "
                     "paradoxical survives the change of object."),
                    ("It is a formal trick",
                     "It is as concrete as anything here: the non-zero members "
                     "of that row are genuine continuous functions on a probe "
                     "that fail to be locally constant, and you are about to "
                     "watch one refuse to settle down."),
                    ("Points must be hiding somewhere",
                     "They are not. Ask for the row at the one-point probe and "
                     "the answer really is zero. What is not zero is what the "
                     "object says to larger probes, and that is a different "
                     "question with its own honest answer."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="ghost",
                prompt="Read the leftover on one row after another, and push "
                       "the stage as far as it will go.",
                notice="The row for one point reads zero, as it always did. On "
                       "the halving probe the wobble inside a single box is "
                       "2<sup>&minus;n</sup>: smaller at every stage and never "
                       "zero, so the function is constant on no box at any "
                       "stage. That is a member of the leftover you can watch. "
                       "The object has no points and is not zero.",
                params={},
            ),
            Name(
                plain="the leftover with no points",
                standard="the condensed cokernel of "
                         "&#8477;<sub>disc</sub> &rarr; &#8477;",
                notation="Q(*) = 0, &nbsp; Q(S) &ne; 0",
                why="It is the missing nearness, recorded as an object. In the "
                    "old setting it had nowhere to live, so the cokernel "
                    "reported zero and the algebra went wrong.",
            ),
            Math(
                statement="Q(S) = C(S, &#8477;) / "
                          "C<sub>lc</sub>(S, &#8477;) &nbsp;&ne;&nbsp; 0",
                reading="C(S, &#8477;) is every continuous map from the probe "
                        "into the ruler; the subscript lc restricts to the "
                        "locally constant ones, which are exactly the continuous "
                        "walks into the dust. The slash declares the second "
                        "collection to be zero inside the first. For any probe "
                        "with infinitely many points there is a continuous "
                        "function that is not locally constant &mdash; the one "
                        "you just watched &mdash; so the quotient has a "
                        "non-zero member. At the one-point probe the two "
                        "collections coincide and the quotient is zero.",
                cite="Example 1.9, page 9 of the lectures",
                url="https://arxiv.org/pdf/2605.03658v1#page=9",
            ),
        ),
        hold="The bridge's missing information now forms an object that is "
             "zero on points but nonzero on larger probes.",
    ),

    Brick(
        slug="the-test-restored",
        title="Kernels and cokernels work again",
        idea="Run the test on the bridge in the new world and it returns the "
             "right verdict, because the leftover now has somewhere to live.",
        need=(
            "The ghost: a leftover that is zero on points and not zero.",
            "The test: both measurements zero should force sameness.",
        ),
        concept=(
            Say("Run the test on the bridge one more time, in the new world. "
                "The kernel is still zero: nothing is destroyed. The cokernel "
                "is now the ghost, which is not zero."),
            Say("So the test reports: not a sameness. Which is correct. The "
                "same two computations that lied in world 3 now tell the "
                "truth, because the world they are computed in has room for "
                "the answer."),
        ),
        intuition=(
            Say("Nothing was made cleverer. A measurement that can only report "
                "in whole numbers cannot report a half; give it finer units "
                "and the same measurement becomes accurate. The finer unit "
                "here is the row indexed by a probe."),
            Ask(
                "What actually changed &mdash; the map, or the setting?",
                (
                    ("The setting",
                     "Only the setting. The bridge is the same rule it always "
                     "was, sending every number to itself. What changed is "
                     "what kind of object it is a map between, and therefore "
                     "what kind of leftover is permitted to exist."),
                    ("The map, it means something different now",
                     "The rule is untouched: number to itself. It is now read "
                     "as a map of tables rather than a map of point-sets, and "
                     "the leftover of that map has somewhere to live. Same "
                     "map, larger world."),
                    ("The definition of cokernel",
                     "The definition is the same one: declare what was reached "
                     "to be zero, keep what survives. It is computed row by "
                     "row now, and one of the rows is non-zero."),
                ),
                after="This is the theorem the lectures state immediately "
                      "after the failing example, and it is the reason the "
                      "subject is called a repair rather than a "
                      "generalisation.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Fetch the first line of the specification you wrote in "
                    "world 3.",
                    "State the test's verdict on the bridge in the old "
                    "setting, and in the new one.",
                    "Tick the line off, or say precisely what is still "
                    "missing.",
                ),
                found="Old setting: kernel zero, cokernel zero, verdict "
                      "<em>sameness</em>, which is false. New setting: kernel "
                      "zero, cokernel the ghost, verdict <em>not a "
                      "sameness</em>, which is true. The first demand is met, "
                      "and met by the object you read row by row a moment ago "
                      "rather than by an assurance. Two demands remain: that "
                      "the old spaces survive intact, and that what you could "
                      "already compute still comes out the same. They are the "
                      "next two bricks, in that order.",
            ),
            Name(
                plain="a world where the measurements work",
                standard="Cond(Ab) is an abelian category",
                notation="ker = 0 and coker = 0 &rArr; isomorphism",
                why="Better than the old setting in one further respect: it "
                    "has all limits and colimits, and infinite sums and "
                    "products behave, which is what world 7 leans on.",
            ),
            Math(
                statement="Cond(Ab) abelian, with all limits and colimits; "
                          "kernels and cokernels computed rowwise",
                reading="<em>Rowwise</em> is the practical content: to compute "
                        "the kernel or cokernel of a map of condensed abelian "
                        "groups, compute it separately in each row and, for "
                        "the cokernel, repair the gluing afterwards. This is "
                        "Theorem 1.10 of the lectures, quoted here rather than "
                        "checked, since it is a statement about a whole "
                        "category.",
                cite="Theorem 1.10, page 9 of the lectures",
                url="https://arxiv.org/pdf/2605.03658v1#page=9",
            ),
        ),
        hold="In the condensed setting, kernels and cokernels detect "
             "isomorphisms again and correctly identify the bridge as non-invertible.",
    ),

    Brick(
        slug="nothing-was-lost",
        title="Verify that ordinary spaces are preserved",
        idea="Ordinary spaces sit inside the condensed world with exactly "
             "their old maps between them, and no new ones.",
        need=(
            "That every space produces a table of answers.",
            "Being the same: a map across and a map back.",
        ),
        concept=(
            Say("A repair that discarded the spaces you care about would be no "
                "repair. So check the receipt: does the table remember the "
                "space it came from, and does it remember the maps between "
                "spaces?"),
            Say("For a wide class of spaces &mdash; every metric space, every "
                "manifold, every compact space, everything a working "
                "mathematician normally handles &mdash; the answer is yes to "
                "both. Different spaces give different tables, and every map "
                "of tables comes from a genuine continuous map."),
        ),
        intuition=(
            Say("Translating a text is only trustworthy if it neither loses "
                "distinctions nor invents them. Losing them would make "
                "different originals read the same; inventing them would let "
                "you say things in the translation that the original forbids. "
                "The second failure is the dangerous one."),
            Ask(
                "Why is remembering the <em>maps</em> the harder demand?",
                (
                    ("Because a table could admit maps no space allows",
                     "That is the risk, and it would be fatal: the new world "
                     "would then relate old objects in ways the old world "
                     "denied, and results proved there could not be brought "
                     "back. The proposition says this does not happen."),
                    ("It is not harder",
                     "It is strictly stronger. Distinguishing objects is one "
                     "demand; matching every arrow between them exactly is "
                     "another, and it is the one that makes the new world safe "
                     "to work in and return from."),
                    ("Because there are many maps",
                     "Quantity is not the difficulty. The difficulty is "
                     "whether any <em>new</em> maps appear, and the answer is "
                     "that none do."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the dust and the ruler as tables, and ask whether "
                    "the bridge is a map of tables.",
                    "Ask whether there is a map of tables from the ruler back "
                    "to the dust.",
                    "Compare your two answers with what world 2 said about "
                    "continuous maps in each direction.",
                ),
                found="The bridge is a map of tables: a continuous map into the "
                      "dust is in particular a continuous map into the ruler, "
                      "row by row. Backwards there is nothing, because a "
                      "continuous map into the ruler need not be locally "
                      "constant, so there is no rule sending it anywhere in "
                      "the dust's row. Exactly the situation world 2 "
                      "described, reproduced with no new maps invented and "
                      "none of the old ones lost. That is the receipt, checked "
                      "on the one example where it matters most.",
            ),
            Name(
                plain="the translation loses nothing",
                standard="a fully faithful embedding",
                notation="Top<sub>cg</sub> &#8674; Cond(Set)",
                why="<em>Faithful</em>: no two different maps become equal. "
                    "<em>Full</em>: no new maps appear. Together they say the "
                    "old world sits inside the new one exactly as it was.",
            ),
            Math(
                statement="X &#8614; ( S &#8614; C(S, X) ) &nbsp;&middot;"
                          "&nbsp; C(S, X) &#8801; Hom<sub>Cond</sub>(S, X)",
                reading="Hom means <em>all maps from, to</em>. The line says "
                        "the maps between two spaces, computed in the new "
                        "world, are exactly the continuous maps, computed in "
                        "the old one. The subscript cg means compactly "
                        "generated, the mild condition under which this holds; "
                        "it is satisfied by every space in ordinary use. This "
                        "is Proposition 1.7 of the lectures.",
                cite="Proposition 1.7, page 8 of the lectures",
                url="https://arxiv.org/pdf/2605.03658v1#page=8",
            ),
        ),
        hold="Ordinary spaces embed in the condensed setting without losing or "
             "gaining maps between them.",
    ),

    Brick(
        slug="holes-survive",
        title="Topological holes are preserved",
        idea="The holes of a shape, torsion included, come out of the "
             "condensed setting exactly as they came out of the old one.",
        need=(
            "That ordinary spaces sit inside the condensed world unchanged.",
            "The cokernel: what survives after a part is declared zero.",
        ),
        concept=(
            Say("A shape's holes are computed by algebra: build the shape from "
                "cells, write down which cells bound which, and measure what "
                "is closed but not itself a boundary. A circle has one hole; a "
                "doughnut surface has two independent loops."),
            Say("That measurement is made of kernels and cokernels, so a "
                "change of setting could easily change the answer. It does "
                "not. Computed in the condensed world, the holes come out as "
                "they always did."),
        ),
        intuition=(
            Say("The sensitive part is not the count of loops but the torsion: "
                "a loop that is not zero although twice it is. That is the "
                "kind of information that disappears the moment a construction "
                "quietly starts working over the rationals instead of the "
                "whole numbers, so it is the right thing to watch."),
            Ask(
                "Why check the torsion in particular?",
                (
                    ("Because it is the first thing a sloppy repair loses",
                     "Yes. Free ranks survive almost any mistreatment; a hole "
                     "of order two survives only if the setting really does "
                     "keep track of the whole numbers rather than sliding to "
                     "something more forgiving. It is the sensitive "
                     "instrument."),
                    ("Because it is hardest to compute",
                     "It is no harder here: Smith normal form gives ranks and "
                     "torsion in one go. It is the diagnostic value that "
                     "matters, not the difficulty."),
                    ("It is not important",
                     "It is the most important single check. Torsion is "
                     "exactly the information that vanishes when a "
                     "construction quietly starts working over the rationals "
                     "instead of the whole numbers."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="holes",
                prompt="Pick a shape and read off its holes.",
                notice="These numbers are computed from the cell structure by "
                       "Smith normal form over the whole numbers, on this "
                       "page, not looked up. The Klein bottle carries a hole "
                       "of order two &mdash; a loop that is not zero but whose "
                       "double is &mdash; and it is the one entry a careless "
                       "change of setting would destroy first.",
                params={},
            ),
            Name(
                plain="the holes of a shape",
                standard="homology, and its condensed counterpart",
                notation="H<sub>n</sub>(X) = &#8484;<sup>b</sup> &oplus; "
                         "torsion",
                why="The lectures compute the cohomology of profinite sets, of "
                    "the circle, and of products of circles inside the "
                    "condensed setting, and the answers agree with the "
                    "classical ones.",
            ),
            Math(
                statement="H<sup>*</sup>(T<sup>n</sup>, &#8484;) = "
                          "&Lambda;<sup>*</sup>(&#8484;<sup>n</sup>) "
                          "&nbsp;&middot;&nbsp; rank in degree i = "
                          "n choose i",
                reading="T<sup>n</sup> is a product of n circles, and "
                        "&Lambda;<sup>*</sup> is the exterior algebra: one "
                        "generator per circle, and multiplying two of them in "
                        "the other order flips the sign. The rank in degree i "
                        "is the number of ways to choose i circles out of n. "
                        "For the doughnut surface, n = 2, giving ranks 1, 2, 1 "
                        "&mdash; one piece, two independent loops, one "
                        "enclosed volume. This is Proposition 3.1 of the "
                        "lectures, and the numbers on this page are recomputed "
                        "rather than quoted.",
                cite="Proposition 3.1, page 17 of the lectures",
                url="https://arxiv.org/pdf/2605.03658v1#page=17",
            ),
        ),
        hold="The condensed setting preserves homology, including torsion, so "
             "the familiar holes of a space remain detectable.",
    ),

    Brick(
        slug="where-you-stand",
        title="Review the completed repair",
        idea="The construction now satisfies all three requirements from World "
             "3. The next step is to handle infinite sums and multiplication.",
        need=(
            "Everything from worlds 1 to 6.",
        ),
        concept=(
            Say("Look back at the specification you wrote in world 3. An "
                "object with no points that is not zero: built, and you read "
                "its rows. The two measurements trustworthy again: restored. "
                "The old spaces intact inside: receipted, maps and all."),
            Say("That is the content of the first three lectures. None of it "
                "was taken on trust: the failure was one you ran, the probe "
                "was one you split, and the leftover was one you watched "
                "refuse to settle down."),
        ),
        intuition=(
            Say("It is worth naming what is still missing, because the "
                "machinery so far has a definite limit. Everything built can "
                "add two things at a time. Nothing built can add up an endless "
                "list, and endless lists are what analysis is made of."),
            Ask(
                "What has not yet been addressed?",
                (
                    ("Adding up infinitely many things",
                     "That is the gap, and it is the reason topology was "
                     "dragged into algebra in the first place. Nothing built "
                     "so far can add up an endless list. World 7 is about "
                     "exactly that, and it is where the subject starts paying "
                     "for itself."),
                    ("Multiplication",
                     "Also missing, and it comes in world 8. But there is a "
                     "step before it: everything so far can add two things, "
                     "and nothing so far can add infinitely many."),
                    ("Nothing, this is the whole subject",
                     "This is one third of it. Two more things are needed "
                     "before the machinery does any work: infinite sums that "
                     "land, and then multiplication."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Without looking back, say in one sentence what a probe "
                    "is.",
                    "Say in one sentence what a condensed set is.",
                    "Say what goes wrong with the dust and the ruler, and what "
                    "fixes it.",
                    "Any sentence you could not produce marks a brick worth "
                    "replaying before world 7.",
                ),
                found="Serviceable answers: a probe is a tower of finite "
                      "stages, each remembering the one above it. A condensed "
                      "set is the table of continuous maps from every probe, "
                      "obeying cut and glue. The dust and the ruler have the "
                      "same members and different nearness, so the cokernel "
                      "reads zero and the algebra returns a false verdict; in "
                      "the condensed world the leftover has a row to live in "
                      "and the verdict comes out right. If all three came, you "
                      "are carrying the first three lectures.",
            ),
            Name(
                plain="what you have learned",
                standard="condensed sets and condensed abelian groups, "
                         "Lectures I to III",
                notation="Cond(Set), Cond(Ab)",
                why="This is the content of part one of the written guide. "
                    "Everything ahead is built on top of it and nothing "
                    "revises it.",
            ),
            Math(
                statement="Top<sub>cg</sub> &#8674; Cond(Set) "
                          "&nbsp;&middot;&nbsp; Cond(Ab) abelian "
                          "&nbsp;&middot;&nbsp; H<sup>*</sup> unchanged",
                reading="Three lines, three lectures. Spaces embed without "
                        "distortion; the additive world is one where the "
                        "measurements work; and the classical invariants "
                        "survive the move. Nothing here is a generalisation "
                        "for its own sake &mdash; each line answers a demand "
                        "that was written down before the construction "
                        "existed.",
                cite="Lectures I to III",
                url="https://arxiv.org/pdf/2605.03658v1#page=6",
            ),
        ),
        hold="The repair meets every requirement from World 3. The remaining "
             "challenge is to extend it to infinite sums and multiplication.",
    ),
)


WORLD = World(
    number=6,
    slug="the-repair",
    title="Verify the repair",
    promise="By the end, you will have seen the missing object become visible, "
            "watched the broken algebraic test return the correct result, and "
            "confirmed that familiar topological information survives.",
    bricks=BRICKS,
)

"""World 7.  Infinite sums, weights, and the solid rule.

Part two of the written guide, discovered rather than presented: an endless
sum is meaningless until a notion of nearness is chosen, a weighting on a
probe is the thing that turns a function into a number, and solidity is the
demand that every endless sum have exactly one answer.
"""

from __future__ import annotations

from ..model import Ask, Brick, Math, Name, Play, Say, Try, World


BRICKS = (

    Brick(
        slug="an-endless-sum",
        title="How an infinite sum gets a value",
        idea="An infinite sum is defined as a limit, so its value depends on "
             "the chosen notion of nearness.",
        need=(
            "An abelian group: adding, a zero and opposites.",
            "A rule about nearness, and what it means to close in on "
            "something.",
        ),
        concept=(
            Say("Adding, by itself, only ever combines two things at a time. "
                "No amount of it reaches the end of an endless list, so the "
                "value of an endless sum cannot come from the adding."),
            Say("It comes from the nearness rule: the running totals close in "
                "on something, and that something is called the answer. Change "
                "the nearness and the answer changes with it."),
        ),
        intuition=(
            Say("Add a half, then a quarter, then an eighth, forever. The "
                "running totals are 0.5, 0.75, 0.875, crowding in on 1, and "
                "nobody minds calling the answer 1. Notice that the crowding, "
                "not the adding, is what produced the number."),
            Ask(
                "So where does an infinite sum actually live?",
                (
                    ("In the nearness rule, not in the adding",
                     "That is the diagnosis, and it explains the whole awkward "
                     "history. Algebra provides the adding; topology provides "
                     "the closing in; and the two of them are the badly glued "
                     "layers from world 2. Infinite sums are the operation "
                     "that needs both at once, which is why they are where the "
                     "trouble concentrates."),
                    ("In the adding",
                     "Adding alone reaches only finite totals: given the "
                     "endless list, no amount of adding two at a time arrives "
                     "anywhere. The step from the running totals to the answer "
                     "is made entirely by the nearness rule."),
                    ("It is just notation",
                     "The notation is standing for something specific: the "
                     "thing the running totals close in on. Change what "
                     "<em>close in on</em> means and the same notation names a "
                     "different number, as the next brick shows."),
                ),
                after="This is precisely why topology was dragged into algebra "
                      "in the first place, and why the repair had to happen "
                      "before infinite sums could be handled properly.",
            ),
        ),
        experiment=(
            Play(
                widget="series",
                prompt="Watch the running totals of one and two and four and "
                       "eight, and their distance from &minus;1.",
                notice="With ordinary distance the totals run away: 1, 3, 7, "
                       "15, and the gap to &minus;1 doubles at every step. By "
                       "the usual rule this sum has no answer at all, and "
                       "calling it &minus;1 would be nonsense. Keep the number "
                       "in the readout: the next brick changes nothing except "
                       "how that gap is measured.",
                params={"p": 2, "mode": "ordinary"},
            ),
            Name(
                plain="the answer to an endless sum",
                standard="the limit of the partial sums",
                notation="&sum;<sub>n&ge;0</sub> a<sub>n</sub> = "
                         "lim<sub>N&rarr;&infin;</sub> "
                         "&sum;<sub>n&lt;N</sub> a<sub>n</sub>",
                why="The large &sum; means <em>add up</em>. The right-hand "
                    "side is a limit of finite totals, so the whole meaning of "
                    "the left-hand side is borrowed from the nearness rule.",
            ),
            Math(
                statement="1 + 2 + 4 + &#8943; + 2<sup>N&minus;1</sup> = "
                          "2<sup>N</sup> &minus; 1 &nbsp;&middot;&nbsp; "
                          "| 2<sup>N</sup> &minus; 1 &minus; (&minus;1) | = "
                          "2<sup>N</sup>",
                reading="The vertical bars mean ordinary distance. The first "
                        "line is the exact running total after N terms, "
                        "computed on this page rather than quoted. The second "
                        "says its ordinary distance from &minus;1 is "
                        "2<sup>N</sup>, which grows without bound. Under the "
                        "usual nearness the sum diverges, full stop.",
            ),
        ),
        hold="An infinite sum is a limit rather than an ordinary algebraic "
             "operation, and its value depends on the chosen nearness rule.",
    ),

    Brick(
        slug="another-nearness",
        title="A different notion of nearness",
        idea="Declare two numbers close when their difference is divisible by "
             "a high power of two, and one plus two plus four plus eight adds "
             "to &minus;1.",
        need=(
            "That an infinite sum is decided by the nearness rule.",
            "Divisibility: whether one whole number divides another.",
        ),
        concept=(
            Say("Fix the whole numbers and change the rule. Declare two "
                "numbers close when their difference is divisible by a high "
                "power of two. So 0 and 1024 are very close, and 0 and 3 are "
                "far apart."),
            Say("This is a legitimate notion of nearness. It satisfies every "
                "demand ordinary distance satisfies, including the one about "
                "going round a triangle. It simply groups the numbers "
                "differently."),
        ),
        intuition=(
            Say("Under this rule, being close means agreeing in many binary "
                "digits from the bottom up. The running totals 1, 3, 7, 15 are "
                "1, 11, 111, 1111 in binary &mdash; and &minus;1 is the "
                "endless string of ones. Each total agrees with it in one more "
                "digit than the last."),
            Ask(
                "Two nearness rules, two different answers to the same sum. "
                "Is one of them wrong?",
                (
                    ("Neither: the sum was never well-posed alone",
                     "That is the lesson. <em>One plus two plus four plus "
                     "&hellip;</em> is not a question until a nearness is "
                     "named. Under the ordinary rule it has no answer; under "
                     "this one it has exactly one, and it is &minus;1. Both "
                     "statements are correct, about different questions."),
                    ("The new one, since the totals are growing",
                     "Growing in the ordinary sense, certainly. But under the "
                     "new rule the running totals are getting steadily closer "
                     "to &minus;1, because 2<sup>N</sup> is divisible by ever "
                     "higher powers of two. Growth in one rule is convergence "
                     "in the other, and neither rule is a mistake."),
                    ("The old one, since there is an answer now",
                     "Not that either. Having an answer does not make a rule "
                     "better; the ordinary rule is correct about the ordinary "
                     "question. What is wrong is only the habit of asking for "
                     "a sum without naming a nearness."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="series",
                prompt="The same running totals, now with the gap measured by "
                       "the new rule. Switch between the two rules and watch "
                       "one line invert into the other.",
                notice="The totals are identical in both settings &mdash; "
                       "1, 3, 7, 15 &mdash; and only the measurement of the "
                       "gap changed. Under the base-two rule the gap halves at "
                       "every step, so the sum genuinely equals &minus;1, "
                       "exactly and with no hand-waving. Two rules, one list "
                       "of numbers, opposite verdicts.",
                params={"p": 2, "mode": "padic"},
            ),
            Name(
                plain="close when the difference is very divisible",
                standard="the p-adic absolute value",
                notation="|x|<sub>p</sub> = p<sup>&minus;v</sup>",
                why="v counts how many times the prime p divides x. The more "
                    "it divides, the smaller x counts as. Completing the whole "
                    "numbers under this size gives the p-adic numbers, "
                    "&#8484;<sub>p</sub>, one of the two examples the whole of "
                    "world 8 is built on.",
            ),
            Math(
                statement="&sum;<sub>n&ge;0</sub> 2<sup>n</sup> = "
                          "&minus;1 in &#8484;<sub>2</sub> "
                          "&nbsp;&middot;&nbsp; |2<sup>N</sup>|<sub>2</sub> = "
                          "2<sup>&minus;N</sup> &rarr; 0",
                reading="Read the second line as: the 2-adic size of "
                        "2<sup>N</sup> is 2<sup>&minus;N</sup>, which tends to "
                        "zero. So the gap between the running total and "
                        "&minus;1 vanishes, and the sum genuinely equals "
                        "&minus;1 there. Every number on this page is computed "
                        "in exact arithmetic, both sizes side by side.",
            ),
        ),
        hold="With 2-adic nearness, the series 1 + 2 + 4 + 8 + &hellip; "
             "converges to &minus;1. A nearness rule is what makes the sum meaningful.",
    ),

    Brick(
        slug="weights",
        title="Compatible weights on every stage",
        idea="A measure on a probe is a tower of weights in which every box "
             "weighs exactly what the boxes inside it weigh.",
        need=(
            "A probe: boxes at every stage, each remembering its parent.",
            "Adding, and the idea of a running total.",
        ),
        concept=(
            Say("Go back to the probe and put a weight on each box at some "
                "stage. One rule suggests itself immediately: a box at the "
                "stage above should weigh what the boxes inside it weigh, "
                "added up."),
            Say("Insist on that, and weights at one stage determine weights at "
                "every coarser stage. The tower of weights becomes a single "
                "consistent object rather than a pile of unrelated numbers."),
        ),
        intuition=(
            Say("Every function on a probe is built from steps &mdash; "
                "constant on each box of some stage &mdash; so weights are "
                "exactly what turns a function into a number: value times "
                "weight, added over the boxes. The consistency demand is what "
                "makes that total unambiguous."),
            Ask(
                "Why does the level you compute at not matter?",
                (
                    ("Because splitting a box splits its weight too",
                     "That is the mechanism. A function constant on a coarse "
                     "box contributes value times weight, and splitting the "
                     "box splits the weight into pieces that add back to the "
                     "same total. The bookkeeping is arranged so that "
                     "refinement cannot change an answer."),
                    ("It does matter, finer is more accurate",
                     "Not here. Finer boxes give more freedom for the "
                     "<em>function</em>, but for a function already decided at "
                     "the coarse stage the total is identical, because the "
                     "weights add up exactly. That exactness is what the "
                     "compatibility demand buys."),
                    ("By assumption",
                     "It is a consequence, not an assumption. The only thing "
                     "assumed is that a box weighs the total of the boxes "
                     "inside it; level-independence follows from that by "
                     "adding up."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="weights",
                prompt="Change the weight on one small box and watch the "
                       "coarser stages fill in, then compare the two totals.",
                notice="The coarse weights are forced, never chosen: they are "
                       "read off from the fine ones by adding. And the average "
                       "of a step function comes out identical at stage 1 and "
                       "at the finest stage, for every setting of the dial. "
                       "Both numbers are computed live; if compatibility ever "
                       "failed, they would part company.",
                params={"depth": 3},
            ),
            Name(
                plain="weights that agree between stages",
                standard="a measure on a profinite set",
                notation="&mu; = (&mu;<sub>i</sub>), &nbsp; "
                         "&mu;<sub>i</sub>(box) = &sum; &mu;<sub>i+1</sub>"
                         "(sub-boxes)",
                why="Because every function on a probe is built from steps, a "
                    "compatible family of weights is exactly what is needed to "
                    "integrate any function at all.",
            ),
            Math(
                statement="&int;<sub>S</sub> f d&mu; = &sum;<sub>boxes at "
                          "level i</sub> f(box) &middot; &mu;<sub>i</sub>"
                          "(box), &nbsp; independent of i",
                reading="The long S is an integral, which here is nothing more "
                        "than a finite total: value times weight, added over "
                        "the boxes at whichever stage the function was decided "
                        "at. The clause on the right is the claim you just "
                        "moved: the answer does not depend on the stage. This "
                        "page recomputes it at two stages and compares.",
                cite="Lecture IV, on measures, page 26 onwards",
                url="https://arxiv.org/pdf/2605.03658v1#page=26",
            ),
        ),
        hold="A measure gives compatible weights at every stage of a probe, so "
             "integration produces the same result at any stage.",
    ),

    Brick(
        slug="the-solid-rule",
        title="Give every infinite sum one answer",
        idea="An object is solid when every endless sum in it has exactly one "
             "answer, with no choice of nearness left to make.",
        need=(
            "That an infinite sum needs a nearness to have an answer.",
            "Measures on probes, and the condensed world of world 6.",
        ),
        concept=(
            Say("Make the demand a property of the object rather than of a "
                "chosen rule. An object is <strong>solid</strong> if every "
                "endless sum you can write in it has exactly one answer."),
            Say("Exactly one is the strong part. Not <em>at least one</em>, "
                "which would leave the answer ambiguous; not <em>at most "
                "one</em>, which would leave sums unanswered. The demand is "
                "phrased so that the answer is forced."),
        ),
        intuition=(
            Say("You have met this shape of demand twice already: a map "
                "answers every input exactly once, and local answers glue to "
                "exactly one global answer. Each time, <em>exactly one</em> is "
                "what turns an operation from a hope into a usable tool."),
            Ask(
                "Where have you met <em>exactly one</em> as a demand before?",
                (
                    ("In the gluing rule",
                     "The same shape of demand, and that is not a coincidence. "
                     "Both say: a family of local data determines one global "
                     "answer and no more. Solidity is the gluing idea applied "
                     "to sums instead of to pieces of a probe."),
                    ("In the definition of a map",
                     "Also there &mdash; every input gets exactly one output "
                     "&mdash; and it is the same instinct: an operation is "
                     "well defined when it neither fails to answer nor answers "
                     "twice."),
                    ("Nowhere",
                     "It has appeared twice: a map answers every input exactly "
                     "once, and gluing produces exactly one global answer. The "
                     "pattern is the same, and it is what makes an operation "
                     "usable."),
                ),
                after="The building blocks turn out to be startlingly "
                      "concrete: rows of dials, each a copy of the whole "
                      "numbers, with no constraint at all on how they are "
                      "set.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take an endless row of dials, each showing any whole "
                    "number you like, with no condition tying them together.",
                    "Write the sum whose n-th term changes only the n-th dial.",
                    "Ask whether that sum has an answer, and whether it has "
                    "more than one.",
                    "Now try the same in a collection where only finitely many "
                    "dials may be non-zero.",
                ),
                found="In the row of dials the sum has exactly one answer: "
                      "read off each dial independently, and there is nothing "
                      "left to decide. In the finitely-supported collection it "
                      "has none, because the answer would need infinitely many "
                      "non-zero dials and no such member exists. So the row of "
                      "dials is solid and the other is not &mdash; and you "
                      "have just found by hand the building block the "
                      "structural theorem names: a product of copies of the "
                      "whole numbers.",
            ),
            Name(
                plain="every endless sum has exactly one answer",
                standard="a solid abelian group",
                notation="&#8484;<sup>&#9633;</sup>, the solidification",
                why="The building blocks are products of copies of the whole "
                    "numbers, written &#8719;<sub>I</sub> &#8484;. Every solid "
                    "object is assembled from those, which is the structural "
                    "theorem of part two of the written guide.",
            ),
            Math(
                statement="&#8484;[S] &rarr; &#8484;<sup>&#9633;</sup>[S] = "
                          "&#8719;<sub>I</sub> &#8484; &nbsp;&middot;&nbsp; "
                          "Solid &sub; Cond(Ab) closed under limits, colimits "
                          "and extensions",
                reading="&#8484;[S] means formal finite combinations of points "
                        "of the probe S; the box superscript is the "
                        "solidification, which completes it so that endless "
                        "sums land. The result is a product of copies of "
                        "&#8484;, one for each member of a basis. The second "
                        "line records that the solid objects form a "
                        "well-behaved world of their own. Both are theorems of "
                        "the lectures, quoted here.",
                cite="Lecture V and Theorem 5.8, page 34 onwards",
                url="https://arxiv.org/pdf/2605.03658v1#page=34",
            ),
        ),
        hold="A solid object gives each allowed infinite sum exactly one value "
             "and is built from products of copies of the integers.",
    ),

    Brick(
        slug="where-the-line-goes",
        title="Why the real line becomes zero",
        idea="Solidify the real line with respect to the base-p rule and it "
             "becomes zero &mdash; a true report about divisibility, not a "
             "defect.",
        need=(
            "Solidity: every endless sum has exactly one answer.",
            "The base-p nearness, where high powers of p are small.",
        ),
        concept=(
            Say("Make the solid rule with respect to the base-p nearness and "
                "ask what happens to the real line. The answer is startling on "
                "first meeting: it becomes zero."),
            Say("The reason is short. In the real numbers every number can be "
                "divided by p, again and again, without limit. Under the "
                "base-p rule that says every number is arbitrarily small, and "
                "something arbitrarily small in a world where sums must land "
                "exactly is zero."),
        ),
        intuition=(
            Say("The base-p rule measures how divisible a number is by p. The "
                "real line is infinitely divisible by p. Asking that rule "
                "about that object is asking a question to which the honest "
                "answer is <em>nothing here is far from zero</em>."),
            Ask(
                "Is that a defect in the theory?",
                (
                    ("No, it is the theory reporting a genuine mismatch",
                     "Correct, and it is worth saying twice. The base-p "
                     "completion is a statement about divisibility by p, and "
                     "the real line is infinitely divisible by p. The answer "
                     "zero is the honest report of that mismatch, not a bug. "
                     "The real line has its own rule, and world 8 builds it."),
                    ("Yes, the real line clearly exists",
                     "It certainly does, and it survives everywhere else in "
                     "the subject. What vanishes is its image under one "
                     "particular completion, the p-adic one, and that "
                     "vanishing is forced by divisibility. Under the real "
                     "line's own rule it is entirely present."),
                    ("It means the real line is not solid",
                     "Careful with the wording: the zero object is solid, "
                     "vacuously. The statement is that solidifying the real "
                     "line in the p-adic sense yields zero, which is a "
                     "statement about that completion rather than about "
                     "whether the line is well behaved."),
                ),
                after="So a different rule is needed for the real line, with a "
                      "different notion of which sums count as small. That is "
                      "the first thing world 8 builds.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the number 1 in the real line and halve it "
                    "repeatedly: 1, one half, one quarter, one eighth.",
                    "Measure each one with the base-2 rule, where being "
                    "divisible by a high power of two makes a number small.",
                    "Notice which direction the sizes move.",
                    "Now ask what number in the real line has base-2 size "
                    "larger than every other.",
                ),
                found="Dividing by two makes a number <em>larger</em> in the "
                      "base-2 rule, and you can divide forever, so no number "
                      "has a largest size and nothing is bounded. A completion "
                      "in which the sizes are unbounded in that way collapses: "
                      "every element is arbitrarily close to zero, so the "
                      "result is the zero object. You have just watched the "
                      "mismatch rather than accepted the theorem &mdash; and "
                      "notice it is a fact about how the real line divides, "
                      "not about condensed mathematics.",
            ),
            Name(
                plain="the ruler vanishes under the base-p rule",
                standard="&#8477; is p-adically uniquely divisible, so its "
                         "solidification is zero",
                notation="&#8477;<sup>&#9633;</sup> = 0",
                why="Quoted from the lectures and understood, not swallowed: "
                    "it is the reason world 8 has to introduce analytic rings "
                    "rather than stopping at solid groups.",
            ),
            Math(
                statement="&#8477; uniquely p-divisible &nbsp;&rArr;&nbsp; "
                          "&#8477; &otimes;<sup>&#9633;</sup> "
                          "&#8484;<sub>p</sub> = 0",
                reading="<em>Uniquely p-divisible</em> means dividing by p is "
                        "possible and gives exactly one answer, always. The "
                        "boxed tensor is the completed product of world 8. The "
                        "line says the p-adic completion of the real line is "
                        "the zero object &mdash; not a failure of the "
                        "construction but a computation of it.",
                cite="Lecture VI, page 42 onwards",
                url="https://arxiv.org/pdf/2605.03658v1#page=42",
            ),
        ),
        hold="Under the p-adic rule, the real line completes to zero. This "
             "correctly reflects its unique p-divisibility rather than indicating a defect.",
    ),
)


WORLD = World(
    number=7,
    slug="sums-that-land",
    title="Infinite sums with well-defined values",
    promise="By the end, you will understand why 1 + 2 + 4 + 8 + &hellip; "
            "converges to &minus;1 in the 2-adic setting, how measures encode "
            "compatible sums, and what it means for an object to be solid.",
    bricks=BRICKS,
)

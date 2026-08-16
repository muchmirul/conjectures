"""World 7.  Infinite sums, weights, and the solid rule.

Part two of the written guide, discovered instead of presented: an endless
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
        idea='An infinite sum gets its value from a limit, so the answer depends on what counts as near.',
        need=(
            "An abelian group: adding, a zero and opposites.",
            "A rule about nearness, and what it means to close in on "
            "something.",
        ),
        concept=(
            Say('Ordinary addition combines finitely many things. An endless list has no final step, so addition alone cannot give the sum a value.'),
            Say('Instead, watch the running totals. If they get closer and closer to one value, that value is the sum. Change the nearness rule and the answer may change too.'),
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
                after="This is exactly why topology was dragged into algebra "
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
                        "computed on this page instead of quoted. The second "
                        "says its ordinary distance from &minus;1 is "
                        "2<sup>N</sup>, which grows without bound. Under the "
                        "usual nearness the sum diverges, full stop.",
            ),
        ),
        hold='An infinite sum is a limit, not an ordinary finite addition. Its value depends on the nearness rule.',
    ),

    Brick(
        slug="another-nearness",
        title="A different notion of nearness",
        idea='Call two numbers close when their difference contains a large power of two. Under this rule, 1 + 2 + 4 + 8 + ... approaches &minus;1.',
        need=(
            "That an infinite sum is decided by the nearness rule.",
            "Divisibility: whether one whole number divides another.",
        ),
        concept=(
            Say('Keep the whole numbers but change closeness. Two numbers are close when their difference is divisible by a large power of two. That makes 0 close to 1024 but far from 3.'),
            Say('This is a valid distance rule. It follows the usual distance laws but groups numbers by divisibility instead of ordinary size.'),
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
                     "&hellip;</em> isn't a question until a nearness is "
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
                     "Not that either. Having an answer doesn't make a rule "
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
        hold='With 2-adic nearness, 1 + 2 + 4 + 8 + ... converges to &minus;1. The nearness rule gives the sum its meaning.',
    ),

    Brick(
        slug="weights",
        title="Compatible weights on every stage",
        idea='A measure puts compatible weights on every stage of a probe: each large box weighs the total of the smaller boxes inside it.',
        need=(
            "A probe: boxes at every stage, each remembering its parent.",
            "Adding, and the idea of a running total.",
        ),
        concept=(
            Say('Put a weight on every box at one stage of a probe. At the coarser stage above it, each box should weigh the sum of the smaller boxes inside.'),
            Say('That rule forces all coarser weights. Instead of unrelated lists of numbers, the whole tower becomes one consistent measure.'),
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
                     "refinement can't change an answer."),
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
                        "moved: the answer doesn't depend on the stage. This "
                        "page recomputes it at two stages and compares.",
                cite="Lecture IV, on measures, page 26 onwards",
                url="https://arxiv.org/pdf/2605.03658v1#page=26",
            ),
        ),
        hold='A measure keeps weights compatible across stages, so integration gives the same answer wherever you calculate it.',
    ),

    Brick(
        slug="the-solid-rule",
        title="Give every infinite sum one answer",
        idea='An object is solid when every allowed infinite sum has exactly one built-in answer.',
        need=(
            "That an infinite sum needs a nearness to have an answer.",
            "Measures on probes, and the condensed world of world 6.",
        ),
        concept=(
            Say('Build the convergence rule into the object itself. The object is <strong>solid</strong> when every allowed endless sum gets exactly one answer.'),
            Say('The words <em>exactly one</em> matter. More than one answer would be ambiguous, while no answer would leave the sum unfinished.'),
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
                     "The same shape of demand, and that isn't a coincidence. "
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
                      "dials is solid and the other isn't &mdash; and you "
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
        hold='A solid object gives every allowed infinite sum one value and can be built from products of copies of the integers.',
    ),

    Brick(
        slug="where-the-line-goes",
        title="Why the real line becomes zero",
        idea='Solidify the real line using the base-p rule and it becomes zero. This reflects its divisibility; it is not a bug.',
        need=(
            "Solidity: every endless sum has exactly one answer.",
            "The base-p nearness, where high powers of p are small.",
        ),
        concept=(
            Say('Apply the base-p solid rule to the real line. The surprising result is that the real line becomes zero.'),
            Say('Every real number can be divided by p repeatedly without limit. Under base-p nearness, that makes every number arbitrarily small. In a solid setting, such an element must be zero.'),
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
                    ("It means the real line isn't solid",
                     "Careful with the wording: the zero object is solid, "
                     "vacuously. The statement is that solidifying the real "
                     "line in the p-adic sense yields zero, which is a "
                     "statement about that completion instead of about "
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
                      "mismatch instead of accepted the theorem &mdash; and "
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
                    "instead of stopping at solid groups.",
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
        hold='Under the p-adic rule, the real line completes to zero because it is uniquely p-divisible. The result is meaningful, not a defect.',
    ),
)


WORLD = World(
    number=7,
    slug="sums-that-land",
    title="Infinite sums with well-defined values",
    promise='You will see why 1 + 2 + 4 + 8 + ... equals &minus;1 in 2-adic arithmetic, how measures keep sums compatible, and what makes an object solid.',
    bricks=BRICKS,
)

"""World 3.  Kernel, cokernel, and the test that fails on the bridge.

This world builds the two measurements algebra makes on a map, shows the
reader that the two of them together are supposed to decide sameness, and then
runs them on the one-way bridge from world 2 and watches the verdict come back
wrong.  Everything after this exists to fix the verdict.
"""

from __future__ import annotations

from ..model import Ask, Brick, Math, Name, Play, Say, Try, World


BRICKS = (

    Brick(
        slug="crushed-to-zero",
        title="What the map destroys",
        idea="The kernel of a polite map is everything the map sends to zero: "
             "the measurement of what it destroyed.",
        need=(
            "An abelian group: a collection with adding, a zero and opposites.",
            "A homomorphism: a map that carries the adding across unharmed.",
        ),
        concept=(
            Say("Algebra asks exactly two questions about a polite map. Here "
                "is the first: what did it destroy? Collect every member of "
                "the source that came out as zero on the other side."),
            Say("That collection is itself a collection you can add in, "
                "because if two members are crushed then so is their sum. It "
                "is a measurement, and it lives on the source side."),
        ),
        intuition=(
            Say("Take clock arithmetic: whole numbers sent to the hour they "
                "point at on a twelve-hour clock. The numbers 0, 12, 24, "
                "&minus;12 and so on all land on zero. They are precisely what "
                "this map cannot see."),
            Ask(
                "If the only member sent to zero is zero itself, what does "
                "that tell you about the map?",
                (
                    ("Nothing was destroyed, so it does not double up",
                     "Exactly right, and the reason is subtraction. If two "
                     "different members landed on the same place, their "
                     "difference would land on zero &mdash; and would not be "
                     "zero itself. So nothing but zero being crushed is the "
                     "same statement as no two members colliding."),
                    ("The map hits everything",
                     "That is the other question, and it is genuinely a "
                     "different one: this measurement looks at the source and "
                     "what got destroyed, not at the target and what got "
                     "missed. Both questions are needed, and the second one is "
                     "the next brick."),
                    ("The map is the do-nothing map",
                     "Stronger than what follows. Doubling destroys nothing "
                     "either, and doubling is not the do-nothing map. All you "
                     "learn is that no two members collide."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the clock map and find two different numbers that "
                    "land on the same hour &mdash; say 5 and 17.",
                    "Subtract them: 17 &minus; 5.",
                    "Check where that difference lands.",
                    "Now do the same with any other colliding pair.",
                ),
                found="17 &minus; 5 is 12, and 12 lands on zero. Every "
                      "colliding pair you try does the same: the difference is "
                      "always a multiple of twelve, always in the kernel. That "
                      "is the mechanism in one line &mdash; a collision "
                      "<em>is</em> a non-zero member of the kernel, seen from "
                      "the other end. This is why one measurement covers both "
                      "questions, and why it needed subtraction to work at "
                      "all.",
            ),
            Name(
                plain="what the map crushes to zero",
                standard="the kernel",
                notation="ker(f) = { a &isin; A : f(a) = 0 }",
                why="Read the braces aloud as <em>the collection of those a "
                    "in A for which f(a) is zero</em>. The colon is read "
                    "<em>such that</em>.",
            ),
            Math(
                statement="ker(f) = 0 &nbsp;&hArr;&nbsp; f injective "
                          "&nbsp;&nbsp;(f(a) = f(b) &rArr; a = b)",
                reading="<em>Injective</em> is the word for no two members "
                        "colliding. The equivalence holds because f(a) = f(b) "
                        "can be rewritten f(a &minus; b) = 0 using politeness, "
                        "so a collision and a non-zero member of the kernel "
                        "are the same event seen twice. Writing ker(f) = 0 is "
                        "shorthand for <em>the kernel contains nothing but "
                        "zero</em>.",
            ),
        ),
        hold="The kernel measures what a map destroys. Empty kernel means no "
             "two members collide.",
    ),

    Brick(
        slug="left-over",
        title="What the map failed to reach",
        idea="The cokernel is what survives in the target once everything the "
             "map reached is declared to be zero: the measurement of what it "
             "missed.",
        need=(
            "The kernel: what a map crushes to zero.",
            "That a map may leave members of the target unused.",
        ),
        concept=(
            Say("The second question is asked on the other side: what did the "
                "map miss? The naive answer &mdash; the list of untouched "
                "members &mdash; is useless, because that list cannot be added "
                "in: two odd numbers add to an even one."),
            Say("The useful answer instead declares everything the map reached "
                "to be zero, and asks what can still be told apart. That "
                "survivor is a collection you can add in, and it is the "
                "measurement."),
        ),
        intuition=(
            Say("Doubling, from whole numbers to whole numbers, reaches every "
                "even number and no odd one. Half the target is never touched, "
                "and you would like a way of saying <em>the map missed a "
                "factor of two</em> rather than listing the misses."),
            Ask(
                "Declare every even number to be zero. What is left?",
                (
                    ("Two things: even and odd",
                     "Two, and only two. Every whole number is now "
                     "indistinguishable from either 0 or 1. The leftover is a "
                     "tiny object with exactly two members, and it is a "
                     "genuine measurement: it says the map missed a factor of "
                     "two."),
                    ("Nothing, all the numbers are still there",
                     "The numbers are still there but they have stopped being "
                     "<em>distinguishable</em>. Once every even number counts "
                     "as zero, 4 and 0 are the same and 5 and 1 are the same. "
                     "Count what can still be told apart and you find two "
                     "things, not infinitely many."),
                    ("Endlessly many odd numbers",
                     "They collapse. 3 minus 1 is 2, which is now zero, so 3 "
                     "and 1 have become the same member. Every odd number "
                     "folds onto 1 and every even one onto 0. Two survivors."),
                ),
                after="That collapsing move &mdash; declaring a part to be "
                      "zero and seeing what survives &mdash; is the single "
                      "most useful operation in algebra, and it is the one "
                      "that breaks for spaces.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Write the numbers 0 to 11 in a row.",
                    "Declare every multiple of 3 to be zero, and strike out "
                    "the ones that have become indistinguishable from an "
                    "earlier number.",
                    "Count the survivors.",
                    "Predict the answer for multiples of 5 before doing it, "
                    "then check.",
                ),
                found="Three survivors for the multiples of 3, and five for "
                      "the multiples of 5: the count is the number you "
                      "declared zero by. The leftover of <em>multiply by "
                      "n</em> is a collection with exactly n members, so the "
                      "measurement is not vague &mdash; it returns the precise "
                      "factor the map failed to cover. Notice also that the "
                      "answer stayed finite even though the numbers did not. "
                      "That is what makes it a usable measurement.",
            ),
            Name(
                plain="what is left after the map has been declared zero",
                standard="the cokernel, a quotient",
                notation="coker(f) = B / f(A)",
                why="The slash is read <em>modulo</em>, or <em>with this "
                    "declared zero</em>. The cokernel of doubling on &#8484; "
                    "is &#8484;/2&#8484;, the two-member group.",
            ),
            Math(
                statement="coker(f) = B / im(f) &nbsp;&middot;&nbsp; "
                          "coker(f) = 0 &nbsp;&hArr;&nbsp; f surjective",
                reading="im(f), the image, is everything the map actually "
                        "reached. <em>Surjective</em> means it reached "
                        "everything. So an empty cokernel says nothing was "
                        "missed, just as an empty kernel said nothing was "
                        "destroyed. Two measurements, one on each side of the "
                        "arrow.",
            ),
        ),
        hold="The cokernel measures what a map missed, by declaring what it "
             "reached to be zero and counting the survivors.",
    ),

    Brick(
        slug="the-test",
        title="Two measurements that ought to settle everything",
        idea="If a polite map destroys nothing and misses nothing, it must be "
             "a sameness &mdash; so two computations replace the search for a "
             "map back.",
        need=(
            "The kernel: nothing destroyed when it is zero.",
            "The cokernel: nothing missed when it is zero.",
        ),
        concept=(
            Say("Put the two measurements together. If a polite map destroys "
                "nothing and misses nothing, every member of the target is hit "
                "and hit exactly once. There is an obvious way back, and "
                "politeness carries over to it."),
            Say("So for collections you can add in, two computations decide "
                "the question that used to require a search. That is the whole "
                "value of the setting."),
        ),
        intuition=(
            Say("Hunting for a map back is an open-ended search: you either "
                "find one or you keep looking, and failing to find one proves "
                "nothing. Computing two measurements ends. That difference "
                "between searching and computing is what makes long chains of "
                "reasoning possible at all."),
            Ask(
                "Why is a test like this worth so much?",
                (
                    ("Because you can compute it",
                     "That is why. Hunting for a map back is a search with no "
                     "guarantee of ending. Computing a kernel and a cokernel "
                     "is bookkeeping. A world where the bookkeeping settles "
                     "the question is a world you can actually work in."),
                    ("Because it is short",
                     "Shortness helps, but the real value is that both "
                     "measurements are things you can calculate directly from "
                     "the map, with no cleverness and no searching."),
                    ("Because it always works",
                     "It always works <em>here</em>, and that is the promise "
                     "about to be broken. Hold the doubt: you have already "
                     "seen a bridge where it will not."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="algebra",
                prompt="Run both measurements on each map and read the "
                       "verdict.",
                notice="Doubling destroys nothing but misses the odd numbers, "
                       "so it fails on the cokernel. The clock map misses "
                       "nothing but destroys the multiples of twelve, so it "
                       "fails on the kernel. The do-nothing map passes both, "
                       "and is a sameness. Three maps, three verdicts, all "
                       "correct.",
                params={},
            ),
            Name(
                plain="a world where the two measurements decide sameness",
                standard="an abelian category",
                notation="ker = 0 and coker = 0 &rArr; isomorphism",
                why="Abelian groups form one. So do vector spaces, and modules "
                    "over any ring. It is the setting nearly all of algebra "
                    "assumes without saying so.",
            ),
            Math(
                statement="ker(f) = 0 and coker(f) = 0 &nbsp;&rArr;&nbsp; "
                          "f : A &cong; B",
                reading="Read: if both measurements come back zero then f is "
                        "an isomorphism, a genuine sameness with a polite map "
                        "back. In an abelian category this implication is part "
                        "of the definition of the setting rather than a "
                        "theorem about any particular objects.",
            ),
        ),
        hold="In a well-behaved algebraic world, nothing destroyed plus "
             "nothing missed forces sameness. The verdict is computable.",
    ),

    Brick(
        slug="the-verdict-is-wrong",
        title="Running the test on the bridge",
        idea="On the bridge from the dust to the ruler both measurements read "
             "zero, and the verdict they force is false.",
        need=(
            "The test: both measurements zero forces sameness.",
            "The one-way bridge from the dust to the ruler.",
        ),
        concept=(
            Say("The dust and the ruler can both be added in: numbers add, "
                "whatever the nearness rule says. The bridge is polite, since "
                "sending each number to itself obviously survives addition. So "
                "the test applies, with nothing bent to make it apply."),
            Say("Measure. Nothing is crushed to zero, because different "
                "numbers stay different. Nothing is missed, because every "
                "number on the ruler is reached. Both measurements are zero."),
        ),
        intuition=(
            Say("You already know the answer the test is about to give, and "
                "you already know it is wrong. Watch it happen anyway: the "
                "value of this moment is seeing exactly which measurement "
                "cannot see what is missing, and why nothing in the "
                "measurement can warn you."),
            Ask(
                "Which of the two measurements is lying?",
                (
                    ("The cokernel",
                     "The cokernel. What the bridge misses is not any "
                     "<em>number</em> &mdash; every number is reached. What it "
                     "misses is all the nearness that the ruler has and the "
                     "dust does not. The cokernel counts members, members are "
                     "all present, so it reports zero, and the entire second "
                     "layer goes unrecorded."),
                    ("The kernel",
                     "The kernel is telling the truth: nothing really is "
                     "crushed, since different numbers stay different. The "
                     "false report is on the other side, where something real "
                     "is missing and no member is missing to record it."),
                    ("Both",
                     "Only one. Nothing is destroyed, and the kernel says so "
                     "correctly. Something <em>is</em> missed &mdash; the "
                     "nearness &mdash; and the cokernel cannot see it, because "
                     "it can only count members."),
                ),
                after="So the leftover is real but has no members. Ordinary "
                      "algebra has no room for such a thing: an object with no "
                      "members is zero, by definition, and there the matter "
                      "ends.",
            ),
        ),
        experiment=(
            Play(
                widget="algebra",
                prompt="Run the same two measurements on the bridge.",
                notice="Both come back zero, and the verdict reads "
                       "<em>sameness</em>. You already know that verdict is "
                       "false: the way back tears. The bookkeeping has "
                       "returned a confident wrong answer, and nothing in the "
                       "bookkeeping can detect it.",
                params={"bridge": True},
            ),
            Name(
                plain="a leftover you cannot see by counting members",
                standard="the failure of topological abelian groups to be "
                         "abelian",
                notation="ker = 0, coker = 0, &#8477;<sub>disc</sub> "
                         "&#8802; &#8477;",
                why="This is the precise defect. It is not that the subject is "
                    "hard; it is that the standard tool returns a wrong answer "
                    "on the simplest possible example.",
            ),
            Math(
                statement="ker(id) = 0, &nbsp; coker(id) = 0, &nbsp; "
                          "&#8477;<sub>disc</sub> &#8802; &#8477;",
                reading="Every symbol here you have now built yourself. The "
                        "line is Example 1.9 of Scholze's lectures, and it is "
                        "given there as the reason the subject needs new "
                        "foundations. Two measurements read zero; the objects "
                        "are not the same; the setting is therefore not "
                        "abelian.",
                cite="Example 1.9, page 9 of the lectures",
                url="https://arxiv.org/pdf/2605.03658v1#page=9",
            ),
        ),
        hold="On the bridge the test returns zero twice and the wrong verdict. "
             "The leftover is real and has no members.",
    ),

    Brick(
        slug="what-we-must-build",
        title="The specification for a repair",
        idea="Any repair must allow an object with no points that is not zero, "
             "keep the old spaces intact, and make the two measurements "
             "reliable again.",
        need=(
            "That the leftover on the bridge is real and has no members.",
        ),
        concept=(
            Say("Write down what a repair has to do before looking at how to "
                "do it. Three demands, and they are the most useful thing to "
                "carry into the next three worlds."),
            Say("It must allow an object that has no members and is not zero. "
                "It must keep every space you already care about, unchanged, "
                "somewhere inside it. And it must make the two measurements "
                "reliable again."),
        ),
        intuition=(
            Say("A specification written before the solution is what stops a "
                "repair from being judged on elegance. Every claim in worlds 4 "
                "to 6 can be checked against these three lines, and you will "
                "be asked to check them."),
            Ask(
                "An object with no members but not zero. Does that sound "
                "possible?",
                (
                    ("Only if <em>member</em> stops being the basic question",
                     "That is the move, stated before you have seen it. If the "
                     "basic question about an object stops being <em>which "
                     "points are in it</em> and becomes something else, then "
                     "an object can answer <em>nothing</em> to the old "
                     "question and still answer richly to the new one."),
                    ("No, that is a contradiction",
                     "It is a contradiction in the setting you have. That is "
                     "the argument for changing the setting rather than "
                     "hunting harder within it. Watch what the new basic "
                     "question turns out to be; the contradiction dissolves "
                     "rather than getting resolved."),
                    ("Maybe, with some trick",
                     "No trick, and that is what makes it durable. The repair "
                     "changes the question one asks of an object, and the "
                     "strange object then exists as ordinarily as any other."),
                ),
                after="World 4 asks the new question. It comes from an "
                      "everyday habit, and you will recognise it once it is "
                      "pointed at.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Write the three demands down somewhere you will still "
                    "have them in twenty minutes.",
                    "For each one, write a single sentence saying how you "
                    "would know if it had been met.",
                    "Keep the page. Worlds 4 to 6 will hand you each answer, "
                    "and you should tick them off yourself rather than take "
                    "the claim.",
                ),
                found="If your three tests came out as <em>show me the object "
                      "and let me read its rows</em>, <em>show me that the old "
                      "maps and only the old maps survive</em>, and <em>run "
                      "the failing example again and show me the right "
                      "verdict</em>, then you have written the same "
                      "specification the lectures work to. Worlds 4 and 5 "
                      "build the machine; world 6 does exactly those three "
                      "checks, in that order.",
            ),
            Name(
                plain="the specification",
                standard="the design goals of condensed mathematics",
                notation="abelian &nbsp;+&nbsp; fully faithful on spaces",
                why="Clausen and Scholze's answer meets all three demands at "
                    "once, which is why it replaced the earlier patches "
                    "instead of joining them.",
            ),
            Math(
                statement="Cond(Ab) abelian &nbsp;&middot;&nbsp; "
                          "Top &#8674; Cond(Set) fully faithful on compactly "
                          "generated spaces",
                reading="Cond(Ab) names the repaired world of things that can "
                        "be added; Theorem 1.10 of the lectures says it is "
                        "abelian, so the two measurements can be trusted "
                        "there. The hooked arrow &#8674; means <em>sits inside "
                        "without distortion</em>: Proposition 1.7 says the "
                        "spaces you already use survive the move with all "
                        "their maps intact. Both are proved in the lectures "
                        "and quoted here.",
                cite="Theorem 1.10 and Proposition 1.7, pages 9 and 8",
                url="https://arxiv.org/pdf/2605.03658v1#page=8",
            ),
        ),
        hold="The repair must permit a memberless object that is not zero, "
             "keep old spaces intact, and restore the two measurements.",
    ),
)


WORLD = World(
    number=3,
    slug="the-broken-test",
    title="The test that should have caught it",
    promise="By the end you will have built algebra's two measurements with "
            "your own hands, watched them agree on every honest example, and "
            "watched them return a confident wrong answer on the bridge.",
    bricks=BRICKS,
)

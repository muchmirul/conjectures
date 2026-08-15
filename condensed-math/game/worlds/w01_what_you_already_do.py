"""World 1.  Collections, matchings, undoing, and adding.

The reader is assumed to know nothing, so this world builds the four words
that every later world leans on.  None of it is condensed mathematics.  It is
here because the crack that condensed mathematics repairs is a crack in
exactly these four words, and a reader who has not held them cannot see the
crack open.

Every brick runs concept, then intuition, then experiment.  Most of the
experiments here are done by hand, because the ideas are small enough that a
widget would get in the way of the reader doing the thing themselves.  The
exception is the last brick, where four rules are laid side by side to show
that being undoable and surviving addition are independent properties: that
independence is the reason world 3 needs two separate measurements, and it is
much easier to see than to be told.
"""

from __future__ import annotations

from ..model import Ask, Brick, Math, Name, Play, Say, Try, World


BRICKS = (

    Brick(
        slug="a-collection",
        title="Things you have decided to keep together",
        idea="A collection is settled by which things belong to it, and by "
             "nothing else: not their order, not their distance, not their "
             "size.",
        need=(
            "Nothing at all. If you can point at some things and say which "
            "ones you meant, you already have everything this brick asks for.",
        ),
        concept=(
            Say("The first object in mathematics is also the thinnest one. "
                "You name some things, and the naming is the whole object. "
                "Which things belong: that is all it records."),
            Say("Everything you might also have said about those things "
                "&mdash; which came first, how far apart they are, which is "
                "heavier &mdash; is deliberately left out. The thinness is not "
                "poverty. It is what makes the object usable everywhere."),
        ),
        intuition=(
            Say("Put a coin, a key and a stone on a table. Now say: <em>these "
                "three</em>. You have just made one, and it is worth noticing "
                "how little you made."),
            Ask(
                "Slide the stone to the other end of the table. Are the three "
                "things you meant still the same three?",
                (
                    ("Yes, nothing changed",
                     "Right, and that is the whole point. Moving the stone "
                     "changed something about the table, but it changed "
                     "nothing about which things you meant. Whatever you made "
                     "when you said <em>these three</em> does not notice "
                     "distance."),
                    ("No, the arrangement is different",
                     "The arrangement is certainly different, and your eye is "
                     "right to see that. But hold the two apart: the "
                     "arrangement is one thing, and the answer to <em>which "
                     "things did you mean</em> is another. Only the second one "
                     "is what you made. It has not moved."),
                    ("It depends what I do with them",
                     "A fair instinct, and later it will earn its keep: the "
                     "same three things can carry extra rules laid on top. But "
                     "the bare answer to <em>which things did you mean</em> is "
                     "already fixed, and no sliding changes it."),
                ),
                after="Keep that separation in view. It is the seed of "
                      "everything ahead: <em>which things</em> is one kind of "
                      "information, and <em>how they sit</em> is another kind "
                      "laid on top of it.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Write down the collection of letters in the word "
                    "<b>letter</b>.",
                    "Write down the collection of letters in the word "
                    "<b>trestle</b>.",
                    "Decide whether the two collections are the same, using "
                    "only the rule that a collection is settled by which "
                    "things belong to it.",
                ),
                found="Both come out as l, e, t, r, s? Not quite &mdash; "
                      "<b>letter</b> gives l, e, t, r and <b>trestle</b> gives "
                      "t, r, e, s, l. The second has an s and the first does "
                      "not, so they are different collections. But notice what "
                      "you had to ignore to get there: <b>letter</b> has three "
                      "e's and two t's, and none of that repetition counted. A "
                      "collection does not record how many times, or in what "
                      "order. If you found yourself wanting to count the "
                      "repeats, that instinct is real and it belongs to a "
                      "different object, not to this one.",
            ),
            Name(
                plain="a collection",
                standard="a set",
                notation="{coin, key, stone}",
                why="Two sets are the same exactly when they have the same "
                    "members. No order, no nearness, no repetition. This is "
                    "the thinnest object in mathematics, and it is thin on "
                    "purpose.",
            ),
            Math(
                statement="x &isin; X &nbsp;&nbsp;&middot;&nbsp;&nbsp; "
                          "X = Y &nbsp;&hArr;&nbsp; (x &isin; X &hArr; x &isin; Y)",
                reading="The sign &isin; is read <em>is a member of</em>, so "
                        "<em>x &isin; X</em> says the thing x is one of the "
                        "things in the collection X. The double arrow &hArr; "
                        "is read <em>exactly when</em>. So the second line "
                        "says: two collections count as the same exactly when "
                        "membership in one always agrees with membership in "
                        "the other. Nothing else is allowed to matter.",
            ),
        ),
        hold="A set is settled by which things belong to it, and by nothing "
             "else whatsoever.",
    ),

    Brick(
        slug="a-matching",
        title="A rule that answers every time",
        idea="A map from one collection to another is a rule that gives every "
             "member of the first exactly one member of the second.",
        need=(
            "A collection: some things you have decided to keep together.",
        ),
        concept=(
            Say("With two collections in hand, the next object is a rule that "
                "connects them. It takes any member of the first and returns "
                "one member of the second."),
            Say("Two demands, and only two. Every member of the source must "
                "get an answer. And no member may get two different answers. "
                "Nothing is demanded of the target at all."),
        ),
        intuition=(
            Say("Three coats on the left, four hooks on the right. Hang each "
                "coat on a hook. Whatever you did, you obeyed both demands "
                "without noticing: no coat was left on the floor, and no coat "
                "ended up in two places at once."),
            Ask(
                "One hook has no coat on it. Has something gone wrong?",
                (
                    ("No, hooks are allowed to be empty",
                     "Correct. The rule is about coats, not hooks: each coat "
                     "needs exactly one answer. Spare hooks are fine, and they "
                     "will matter enormously in a few bricks' time."),
                    ("Yes, everything should be used",
                     "It feels untidy, but nothing has broken. The demand is "
                     "one-directional: every coat must get an answer. Nothing "
                     "demands that every hook be used. Hold on to the "
                     "discomfort though, because the unused part of the right "
                     "side is going to become an object in its own right."),
                    ("Only if I meant it to be a perfect pairing",
                     "Exactly the right distinction, and you are one brick "
                     "ahead. A plain rule allows spare hooks. A perfect "
                     "pairing does not, and that stricter thing is next."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the numbers 1, 2, 3 as your source and the words "
                    "<b>red</b>, <b>green</b> as your target.",
                    "Try to invent a rule that breaks the first demand, by "
                    "leaving some number unanswered.",
                    "Try to invent a rule that breaks the second demand, by "
                    "giving some number two answers.",
                    "Now count how many rules obey both.",
                ),
                found="Breaking either demand is easy to write down and easy "
                      "to recognise as broken: <em>1 goes nowhere</em> leaves "
                      "you unable to answer a fair question, and <em>1 goes to "
                      "red and also to green</em> leaves you unable to answer "
                      "it once. The rules that obey both number eight: two "
                      "independent choices for each of three numbers, so 2 "
                      "&times; 2 &times; 2. That count is worth remembering "
                      "&mdash; the same shape of count returns in world 4, "
                      "where it becomes the size of what a shape says to a "
                      "probe.",
            ),
            Name(
                plain="a matching",
                standard="a map, or a function",
                notation="f : A &rarr; B",
                why="A map from A to B is a rule that gives every member of A "
                    "exactly one member of B. That is the entire demand: "
                    "every input answered, one answer each.",
            ),
            Math(
                statement="f : A &rarr; B &nbsp;&nbsp;&middot;&nbsp;&nbsp; "
                          "a &#8614; f(a)",
                reading="The arrow &rarr; between two collections announces a "
                        "map: it goes from A, the source, to B, the target. "
                        "The barred arrow &#8614; is read <em>is sent to</em>, "
                        "and it is used for what happens to one individual "
                        "member: the thing a is sent to the thing named f(a). "
                        "Read f(a) aloud as <em>f of a</em>, meaning the one "
                        "answer the rule f gives when it is handed a.",
            ),
        ),
        hold="A map answers every member of the source with exactly one member "
             "of the target. Unused members of the target are allowed.",
    ),

    Brick(
        slug="undoing",
        title="When two collections are the same collection",
        idea="Two collections count as the same when there is a map across "
             "and a map back that undoes it.",
        need=(
            "A collection: which things you meant.",
            "A map: a rule that answers every member of the source once.",
        ),
        concept=(
            Say("<em>Same</em> has to be defined, not felt. For collections "
                "the definition is: a map across, and a map back, such that "
                "doing both returns everything to where it started."),
            Say("Once such a pair exists, nothing can tell the two collections "
                "apart, because any statement about one can be carried across "
                "and read on the other. The test is a test, not an opinion."),
        ),
        intuition=(
            Say("Three coats, three hooks, one coat per hook, every hook "
                "filled. Point at a hook and name the coat on it: that "
                "backwards rule answers every hook, exactly once, so it is a "
                "map too. Going and coming back leaves every coat where it "
                "started."),
            Ask(
                "Here is a rule from the whole numbers 1, 2, 3, &hellip; to "
                "the even numbers 2, 4, 6, &hellip;: double it. Can you walk "
                "backwards?",
                (
                    ("Yes: halve it",
                     "Yes. Every even number halves to exactly one whole "
                     "number, so the way back is a map as well. Two endless "
                     "collections, one sitting inside the other, and yet they "
                     "match perfectly. Endless collections are strange in "
                     "exactly this way, and it is worth being unsettled by it "
                     "now rather than later."),
                    ("No, there are more whole numbers than even ones",
                     "That is the intuition everybody arrives with, and it is "
                     "the intuition that counting small piles trains into you. "
                     "But the test is not <em>which pile looks bigger</em>, it "
                     "is <em>can you walk backwards</em>. Halving walks "
                     "backwards, every time, without ambiguity. By the only "
                     "test we have, these two collections are the same size."),
                    ("Only for some even numbers",
                     "Try to find one that fails. Take any even number and "
                     "halve it: the result is a whole number, and it is the "
                     "only whole number that doubles back to what you started "
                     "with. There is no exception to hunt down."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Write the whole numbers 1, 2, 3, 4, 5 in a row.",
                    "Underneath each, write the even number you get by "
                    "doubling it.",
                    "Now cover the top row and try to rebuild it from the "
                    "bottom row alone.",
                    "Then try the same with the rule <em>round down to the "
                    "nearest even number</em>, and see where the rebuilding "
                    "goes wrong.",
                ),
                found="Doubling rebuilds perfectly: each bottom entry names "
                      "exactly one top entry, so the covered row is "
                      "recoverable with nothing lost. Rounding down does not: "
                      "both 4 and 5 give 4, so when you uncover a 4 you cannot "
                      "say which number produced it. That failure is not a "
                      "matter of degree. One rule can be undone and the other "
                      "cannot, and undoing is the entire test for sameness.",
            ),
            Name(
                plain="a perfect matching",
                standard="a bijection, or an isomorphism of sets",
                notation="A &cong; B",
                why="The symbol &cong; is read <em>is isomorphic to</em>, and "
                    "for bare collections it means precisely that there is a "
                    "map across with a map back undoing it.",
            ),
            Math(
                statement="g &compfn; f = id<sub>A</sub> &nbsp;&nbsp;and"
                          "&nbsp;&nbsp; f &compfn; g = id<sub>B</sub>",
                reading="The circle &compfn; means <em>do one, then the "
                        "other</em>: g &compfn; f is the rule <em>apply f, "
                        "then apply g</em>. The symbol id<sub>A</sub> names "
                        "the do-nothing rule on A, which sends every member of "
                        "A to itself. So the two equations say: going across "
                        "and coming back is the same as doing nothing, in both "
                        "directions. When such a g exists, f is a bijection.",
            ),
        ),
        hold="Two collections are the same when a map across can be undone by "
             "a map back. Undoing is the test, and there is no other.",
    ),

    Brick(
        slug="adding",
        title="Collections you can add in",
        idea="An abelian group is a collection carrying an addition, a zero, "
             "and an opposite for every member.",
        need=(
            "A collection, and a map between collections.",
            "Ordinary addition of whole numbers, as you already use it.",
        ),
        concept=(
            Say("Most collections met in the wild carry more than membership. "
                "Whole numbers can be added. So can lengths, shifts, "
                "rotations, forces, debts. The pattern underneath all of them "
                "is short enough to state in four lines."),
            Say("Any two members combine to give a third. One member changes "
                "nothing when added, and is called zero. Every member has an "
                "opposite that cancels it back to zero. And the order of "
                "adding never matters."),
        ),
        intuition=(
            Say("Think of steps along a path. Two steps combine into one "
                "longer step. Standing still is the step that changes nothing. "
                "And every step has a step back. The pattern is not an "
                "abstraction of numbers; numbers are one instance of it."),
            Ask(
                "Whole numbers with addition: does every member have an "
                "opposite?",
                (
                    ("Yes, if negatives count as whole numbers",
                     "That is the whole subtlety in one line. With the "
                     "negatives included, 5 has &minus;5 to cancel it and "
                     "everything works. Without them, subtraction runs off the "
                     "edge of the collection. Taking away is the fragile "
                     "operation here, and it stays fragile for the rest of "
                     "the game."),
                    ("Yes, always",
                     "Careful: it depends which collection you meant. Among "
                     "0, 1, 2, 3, &hellip; alone, nothing except 0 has an "
                     "opposite inside the collection. You have to let the "
                     "negatives in before the claim is true. Subtraction is "
                     "the demanding one, and it will keep being the "
                     "demanding one."),
                    ("No",
                     "Then look again at which collection you have in mind. If "
                     "the negatives are allowed in, every number does have an "
                     "opposite. Your instinct is sound for the counting "
                     "numbers alone, and that is exactly the case where "
                     "subtraction breaks."),
                ),
                after="Remember which operation was the awkward one. Nearly "
                      "everything ahead is a story about subtraction failing "
                      "somewhere it should not.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the numbers 0, 1, 2, 3 and add them the way a "
                    "four-hour clock does: after 3 comes 0 again.",
                    "Check the four demands one at a time: does every pair "
                    "combine? is there a member that changes nothing? does "
                    "every member have an opposite? does order matter?",
                    "Now try the same four checks on the numbers 0, 1, 2, 3 "
                    "with ordinary addition, where 3 + 3 = 6 is off the end.",
                ),
                found="The clock passes all four. The opposite of 1 is 3, "
                      "since 1 + 3 comes back to 0; the opposite of 2 is 2. "
                      "Ordinary addition on the same four numbers fails at the "
                      "first demand, because 3 + 3 has nowhere to land. So "
                      "<em>can be added in</em> is not a property of the "
                      "numbers you chose; it is a property of the numbers "
                      "together with the rule. The same four members pass "
                      "under one rule and fail under another.",
            ),
            Name(
                plain="a collection you can add in",
                standard="an abelian group",
                notation="(A, +, 0, &minus;)",
                why="<em>Abelian</em> only records that the order of adding "
                    "does not matter. The whole numbers, positive and "
                    "negative, are the first example, written &#8484;.",
            ),
            Math(
                statement="a + b = b + a &nbsp;&middot;&nbsp; "
                          "(a + b) + c = a + (b + c) &nbsp;&middot;&nbsp; "
                          "a + 0 = a &nbsp;&middot;&nbsp; a + (&minus;a) = 0",
                reading="Four demands, in order: swapping two things being "
                        "added changes nothing; when three are added, where "
                        "you put the brackets changes nothing; adding 0 "
                        "changes nothing; and every a has an opposite "
                        "&minus;a that cancels it. The blackboard letter "
                        "&#8484; is the standard name for the whole numbers "
                        "with addition, from the German <em>Zahlen</em>.",
            ),
        ),
        hold="An abelian group is a collection with addition, a zero, and an "
             "opposite for every member. Subtraction is the demand that has "
             "teeth.",
    ),

    Brick(
        slug="respecting-the-adding",
        title="Maps that do not disturb the adding",
        idea="A map between two collections that can be added in is polite "
             "when adding first and crossing over gives the same answer as "
             "crossing over first and adding.",
        need=(
            "A map: every member of the source answered exactly once.",
            "An abelian group: a collection with adding, a zero and opposites.",
        ),
        concept=(
            Say("When both sides carry an addition, a map can be asked to "
                "respect it. Add two members and cross over, or cross over "
                "both and then add: a polite map gives the same answer either "
                "way."),
            Say("This one demand is what makes a map worth studying here. An "
                "impolite map moves members around without carrying the "
                "structure, and there is nothing algebraic to say about it."),
        ),
        intuition=(
            Say("Doubling is polite. Double 3 and double 4 and add, or add 3 "
                "and 4 and then double: 14 either way. Squaring is not polite: "
                "3 squared plus 4 squared is 25, but 7 squared is 49."),
            Ask(
                "A polite map must send zero to zero. Why?",
                (
                    ("Because 0 + 0 = 0 forces it",
                     "That is the argument. Crossing over 0 + 0 gives f(0) + "
                     "f(0), and it must equal f(0). Subtract f(0) from both "
                     "sides &mdash; and here is subtraction again, doing real "
                     "work &mdash; and f(0) = 0. The zero is not an extra "
                     "condition; the adding already implies it."),
                    ("It does not have to",
                     "It is forced, though the force is easy to miss. Since "
                     "0 + 0 = 0, politeness gives f(0) + f(0) = f(0), and "
                     "cancelling one f(0) leaves f(0) = 0. Try to build an "
                     "exception and the cancelling always catches you."),
                    ("By convention",
                     "No convention is needed, which is the pleasant part. It "
                     "follows: f(0) + f(0) = f(0), so f(0) = 0. Very little in "
                     "this subject is convention; almost everything is forced "
                     "by something smaller."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the rule <em>add seven</em> on the whole numbers.",
                    "Compute the answer for 2 + 3 by crossing over first: "
                    "(2 + 7) + (3 + 7).",
                    "Compute it by adding first: (2 + 3) + 7.",
                    "Compare, and then check what the rule does to 0.",
                ),
                found="Crossing over first gives 19; adding first gives 12. "
                      "The rule <em>add seven</em> is not polite, and its "
                      "failure shows up in the same place as its failure to "
                      "fix zero: it sends 0 to 7. Those two failures are one "
                      "failure. A shift is a perfectly good map of collections "
                      "and a useless map of collections-with-addition, which "
                      "is exactly the distinction this brick draws.",
            ),
            Play(
                widget="undo",
                prompt="Four rules, and the two questions asked of each: can "
                       "it be undone, and does it survive addition?",
                notice="The two questions do not travel together. Adding seven "
                       "can be undone and does not survive addition. Doubling "
                       "survives addition and misses half the target. Rounding "
                       "down to even fails both. Only sending each number to "
                       "itself passes both. That independence is why algebra "
                       "needs two separate measurements, which is the whole of "
                       "world 3.",
                params={},
            ),
            Name(
                plain="a polite map",
                standard="a homomorphism of abelian groups",
                notation="f(a + b) = f(a) + f(b)",
                why="From here on, a map between two collections that can be "
                    "added in always means a polite one. The impolite maps are "
                    "not interesting for this purpose: they do not carry the "
                    "structure across.",
            ),
            Math(
                statement="f : A &rarr; B, &nbsp; f(a + b) = f(a) + f(b) "
                          "&nbsp;&rArr;&nbsp; f(0) = 0, &nbsp; "
                          "f(&minus;a) = &minus;f(a)",
                reading="The single arrow &rArr; is read <em>therefore</em>. "
                        "The line says: from the one demand that f survives "
                        "addition, two more facts follow free of charge. Zero "
                        "goes to zero, and opposites go to opposites. One "
                        "demand, three consequences.",
            ),
        ),
        hold="A homomorphism carries the adding across unharmed. Zero and "
             "opposites then look after themselves.",
    ),
)


WORLD = World(
    number=1,
    slug="what-you-already-do",
    title="Four words you already use",
    promise="By the end you will hold the four ideas the whole subject leans "
            "on: a collection, a map, being the same, and adding. None of it "
            "is new mathematics. All of it is about to break.",
    bricks=BRICKS,
)

"""World 2.  Nearness as a second layer, and the two real lines.

Everything here is standard point-set topology, but it is built from the
reader's own hands instead of from axioms: a rule about which things count as
close, a continuous map, and then the single example that the whole of
condensed mathematics is a response to.
"""

from __future__ import annotations

from ..model import Ask, Brick, Math, Name, Play, Say, Try, World


BRICKS = (

    Brick(
        slug="nearness-is-extra",
        title="Nearness is extra information",
        idea="A collection tells you what is there. A separate nearness rule "
             "tells you which things count as close.",
        need=(
            "A collection: which things you meant, and nothing more.",
        ),
        concept=(
            Say("Start with all the numbers on a line. The collection tells "
                "you which numbers are included. Then add a rule that says "
                "when two numbers are close."),
            Say("That closeness rule is extra information. The list alone "
                "never says that 0.999 is near 1, and another rule could treat "
                "those two numbers differently."),
        ),
        intuition=(
            Say("A crowd in a room is one collection of people whether they "
                "are packed together or spread out. Where they stand is real "
                "information, and it isn't the guest list. The line is the "
                "same: which numbers, and how they sit, are two separate "
                "records."),
            Ask(
                "Draw a window a millionth wide around the number 1. How many "
                "numbers are inside it?",
                (
                    ("Endlessly many",
                     "Yes, and no window is small enough to change that "
                     "answer. Every number on the line is crowded, forever, by "
                     "others. That crowding is the second layer at work."),
                    ("A few",
                     "Try halving the width again, and again. Whatever finite "
                     "answer you have in mind, halve the window enough times "
                     "and the count refuses to drop &mdash; between any two "
                     "numbers there is always another, so the crowd never "
                     "thins."),
                    ("Just the number 1",
                     "That would be a perfectly consistent rule about nearness "
                     "&mdash; and in the very next brick it is the rule we "
                     "will adopt on purpose. But it isn't the usual rule for "
                     "distance, where the window always contains a crowd."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="zoom",
                prompt="Shrink the window around 1, and separately change how "
                       "finely you are willing to look.",
                notice="Two dials, and they fight. Shrinking the window "
                       "reduces the count; looking more finely raises it "
                       "again, without limit, at every width. That is the "
                       "precise sense in which the line is crowded: no window "
                       "is ever empty, because no window is small enough to "
                       "outrun the fractions.",
                params={"target": 1.0},
            ),
            Name(
                plain="a rule about nearness",
                standard="a topology, and the pair is a topological space",
                notation="(X, &tau;)",
                why="The rule is usually recorded by listing the "
                    "<em>open</em> pieces: the regions with no edge included, "
                    "the ones where every member has a little room around it "
                    "still inside. A window without its two endpoints is the "
                    "basic example.",
            ),
            Math(
                statement="U &sube; &#8477; open &nbsp;&hArr;&nbsp; "
                          "&forall; x &isin; U, &exist; &epsilon; &gt; 0 : "
                          "(x &minus; &epsilon;, x + &epsilon;) &sube; U",
                reading="The sign &sube; is read <em>sits inside</em>. The "
                        "upside-down A means <em>for every</em>, the backwards "
                        "E means <em>there is</em>. The Greek letter "
                        "&epsilon; is a width, and a small one by tradition. "
                        "So: a piece U of the line is open exactly when every "
                        "point of it has some width of room around it still "
                        "inside U. &#8477; is the standard name for the line "
                        "of all such numbers, the real numbers.",
            ),
        ),
        hold="A space is a collection plus a nearness rule. The same items can "
             "use many different rules for what counts as close.",
    ),

    Brick(
        slug="the-dust",
        title="A rule where every point stands alone",
        idea="Keep the same numbers but use the opposite rule: every point "
             "stands alone. The result is a different space.",
        need=(
            "A collection, and the idea that nearness is a separate layer laid "
            "on top of it.",
        ),
        concept=(
            Say("A nearness rule can isolate every point. Around each point, "
                "you can draw a tiny region that contains nobody else."),
            Say("Call this version <strong>the dust</strong>. Call the usual "
                "number line <strong>the ruler</strong>. They contain the same "
                "numbers but treat closeness in opposite ways."),
        ),
        intuition=(
            Say("A printed line and a line of full stops carry the same "
                "positions; only one of them is joined up. Nothing has been "
                "removed to get from one to the other, and nothing added. What "
                "changed is which positions count as neighbours."),
            Ask(
                "Dust and ruler: do they have the same members?",
                (
                    ("Yes, exactly the same numbers",
                     "Exactly the same, one for one, with nothing added and "
                     "nothing missing. Everything that distinguishes them "
                     "lives in the second layer. Two objects, identical "
                     "underneath, unrecognisable on top."),
                    ("No, the dust must have fewer",
                     "Nothing was removed. Every number that is on the ruler "
                     "is on the dust; the only change was the answer to "
                     "<em>what is near what</em>. It feels like a loss because "
                     "the picture went from a solid line to a scatter, but the "
                     "membership list is untouched."),
                    ("The dust has more, it is spread out",
                     "The scatter is only the drawing. Nothing was added "
                     "either: same numbers, different second layer. The "
                     "drawing changes because the nearness changed, not "
                     "because the collection did."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="zoom",
                prompt="The same window, now on the dust. Shrink it and count "
                       "again.",
                notice="On the dust the count is one before you start, and "
                       "shrinking can't change it. Each number is its own "
                       "island. The collection is identical to the ruler's "
                       "&mdash; every number is present in both &mdash; and "
                       "yet the two pictures couldn't look less alike.",
                params={"target": 1.0, "discrete": True},
            ),
            Name(
                plain="the dust",
                standard="the discrete topology, written &#8477;<sub>disc</sub>",
                notation="&#8477;<sub>disc</sub> versus &#8477;",
                why="Discrete means every single point counts as a piece with "
                    "room around it. It is the finest possible rule about "
                    "nearness: it separates everything from everything.",
            ),
            Math(
                statement="&#8477;<sub>disc</sub> : every U &sube; &#8477; is "
                          "open &nbsp;&middot;&nbsp; {x} open for all x",
                reading="On the dust, every collection of numbers whatsoever "
                        "counts as open, including the one-member collections "
                        "written {x}. On the ruler that is false: a single "
                        "point has no room around it that contains only "
                        "itself, so {x} isn't open there. That one difference "
                        "is the entire difference between the two.",
            ),
        ),
        hold="The dust and ruler use the same numbers. In the dust every point "
             "is isolated; on the ruler nearby numbers crowd together.",
    ),

    Brick(
        slug="no-tearing",
        title="Maps that preserve nearness",
        idea="A map is continuous when pulling any open target region back "
             "gives an open region in the source.",
        need=(
            "A map: every member of the source answered exactly once.",
            "A rule about nearness on each side.",
        ),
        concept=(
            Say("When both sides have a nearness rule, we can ask whether a map "
                "is continuous. It may stretch or squash things, but it cannot "
                "tear apart points that belong together."),
            Say("Here is the exact check. Pick any open region in the target "
                "and collect every source point that lands there. If that "
                "collection is always open, the map is continuous."),
        ),
        intuition=(
            Say("Squashing is allowed and pulling apart isn't. Think of "
                "pressing a sheet of dough: two points may be pushed together, "
                "but the sheet is never ripped. The backwards test is the "
                "precise version of that asymmetry."),
            Ask(
                "The dust is the source, the ruler the target, and every "
                "number goes to itself. Does this map tear anything?",
                (
                    ("No, it can't",
                     "It can't, and the reason is almost a cheat: on the dust "
                     "<em>every</em> piece is open, so whatever the answer "
                     "looking backwards turns out to be, it was open already. "
                     "The dust makes every map out of it continuous. Nothing is "
                     "near anything, so nothing can be torn apart."),
                    ("Yes, it flattens the dust into a line",
                     "That is what the picture shows, and yet by the backwards "
                     "test nothing tore. Squashing points together is allowed; "
                     "only pulling apart what was joined is forbidden. On the "
                     "dust nothing was ever joined, so there is nothing to "
                     "pull apart."),
                    ("It depends which numbers",
                     "It doesn't: the test passes for every open piece at "
                     "once, uniformly. On the dust every possible answer "
                     "counts as open, so no piece can fail the test."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Run the backwards test on the other direction: source "
                    "the ruler, target the dust, every number to itself.",
                    "Pick the open piece of the dust consisting of the single "
                    "number 1 &mdash; on the dust, that piece is open.",
                    "Ask which numbers on the ruler land in it.",
                    "Ask whether that answer is an open piece of the ruler.",
                ),
                found="The answer is the single number 1, and a single point "
                      "isn't an open piece of the ruler: it has no room "
                      "around it containing only itself. So the test fails, "
                      "and this direction isn't continuous. Notice what you just "
                      "did: the same rule &mdash; every number to itself "
                      "&mdash; passed the test one way and failed it the "
                      "other. Continuity isn't a property of the rule alone. "
                      "It is a property of the rule together with a "
                      "direction.",
            ),
            Name(
                plain="a continuous map",
                standard="a continuous map",
                notation="f<sup>&minus;1</sup>(U) open whenever U is open",
                why="The notation f<sup>&minus;1</sup>(U) means <em>everything "
                    "that lands in U</em>. It isn't an undo rule; it is a "
                    "question asked backwards, and it makes sense even when "
                    "nothing can be undone.",
            ),
            Math(
                statement="id : &#8477;<sub>disc</sub> &rarr; &#8477; "
                          "continuous &nbsp;&middot;&nbsp; "
                          "id : &#8477; &rarr; &#8477;<sub>disc</sub> "
                          "not continuous",
                reading="id is the do-nothing rule: every number is sent to "
                        "itself. Read left to right, the first line says that "
                        "going dust to ruler never tears. The second says that "
                        "the same rule read the other way does tear, because "
                        "one point is open on the dust and isn't open on the "
                        "ruler. The rule is the same rule; only the direction "
                        "changed.",
            ),
        ),
        hold="Check continuity by pulling open regions back to the source. A "
             "map can pass this test one way and fail it on the way back.",
    ),

    Brick(
        slug="the-one-way-bridge",
        title="A perfect matching that isn't an equivalence",
        idea="The dust-to-ruler map matches every point and is continuous, but "
             "it still does not make the spaces equivalent.",
        need=(
            "Being the same, for collections: a map across, and a map back "
            "that undoes it.",
            "Continuity: the backwards test on open pieces.",
        ),
        concept=(
            Say("Map each number in the dust to the same number on the ruler. "
                "As a plain matching, it is perfect: every point is used once, "
                "and the matching clearly runs backward."),
            Say("As a map of spaces, though, it only works one way. Dust to "
                "ruler is continuous; ruler to dust is not. So the spaces are "
                "not equivalent."),
        ),
        intuition=(
            Say("A photocopy that can be made but not unmade isn't the same "
                "document as its original. Here the copying is faultless "
                "member by member, and the unmaking is impossible for reasons "
                "that have nothing to do with the members."),
            Ask(
                "So: are the dust and the ruler the same object?",
                (
                    ("No, because the way back tears",
                     "That is the verdict. Sameness demanded a map across and "
                     "a map back, and here <em>both maps must be continuous</em>. "
                     "One of them isn't. The perfect matching of members is "
                     "not enough, and this is the first time in the game that "
                     "matching the members has failed to settle a question."),
                    ("Yes, they have the same members",
                     "Same members, certainly. But once the objects carry a "
                     "second layer, the test has to respect both layers, and "
                     "the way back fails on the second one. Your instinct is "
                     "the right instinct for bare collections, and this is "
                     "exactly the moment it stops being enough."),
                    ("Half the same",
                     "Closer than it sounds. There is a genuine map one way "
                     "and no map back, so the two sit in an order instead of "
                     "in a sameness: the dust is finer than the ruler. But "
                     "<em>same</em> is a yes-or-no test, and the answer is "
                     "no."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="bridge",
                prompt="Send a crowd closing in on 1 across the bridge, then "
                       "try to send it back.",
                notice="Going across, a crowd that was closing in on 1 stays a "
                       "crowd closing in on 1: the gap keeps shrinking, so the "
                       "ruler still sees it arriving. Coming back, every gap "
                       "reads 1 no matter how far along you go, so on the dust "
                       "the crowd arrives nowhere. The information that it was "
                       "closing in is destroyed in that direction, and you can "
                       "watch the number that carries it.",
                params={},
            ),
            Name(
                plain="a one-way bridge",
                standard="a continuous bijection that isn't a homeomorphism",
                notation="&#8477;<sub>disc</sub> &rarr; &#8477;, "
                         "bijective, not an isomorphism",
                why="A homeomorphism is the real sameness for spaces: continuous "
                    "across and continuous back. Bijective alone no longer buys "
                    "it.",
            ),
            Math(
                statement="&#8477;<sub>disc</sub> &#8594; &#8477; "
                          "bijective and continuous, &nbsp; "
                          "&#8477;<sub>disc</sub> &#8802; &#8477;",
                reading="The crossed symbol &#8802; is read <em>isn't "
                        "isomorphic to</em>. The line records the whole "
                        "problem in one breath: a map that is continuous and "
                        "matches every member perfectly, and is still not a "
                        "sameness. This is Example 1.9 of the lectures.",
                cite="Example 1.9, page 9 of the lectures",
                url="https://arxiv.org/pdf/2605.03658v1#page=9",
            ),
        ),
        hold="A continuous bijection does not always make two spaces equivalent. "
             "Matching the points is not enough; nearness must match too.",
    ),

    Brick(
        slug="badly-glued",
        title="When points and nearness stay disconnected",
        idea="If points and nearness live in separate layers, a calculation "
             "using only the points cannot see the nearness information.",
        need=(
            "The one-way bridge, and why it fails to be a sameness.",
        ),
        concept=(
            Say("Here is the basic problem: an ordinary space stores its points "
                "and its nearness rule as two separate layers. The layers sit "
                "next to each other without being fully connected."),
            Say("A calculation about points can ignore nearness completely. "
                "That becomes dangerous in algebra, because algebra usually "
                "computes with the points and misses the extra layer."),
        ),
        intuition=(
            Say("It is the failure mode of any record kept in two files that "
                "never cross-reference each other. Each file is accurate. Any "
                "question spanning both is unanswerable, and the system will "
                "not tell you it has failed &mdash; it will answer from "
                "whichever file it can read."),
            Ask(
                "Where would you look for a repair?",
                (
                    ("Change what an object <em>is</em>",
                     "That is the road taken, and it is more radical than it "
                     "sounds. Rather than patching the bolt, the object is "
                     "replaced: a space stops being points-plus-a-rule and "
                     "becomes something else entirely, in which the nearness "
                     "isn't a separate layer at all."),
                    ("Add rules until the layers agree",
                     "This was tried for decades, and the patches work in the "
                     "cases they were cut for. But each patch is local to its "
                     "own situation, and none of them makes the basic algebra "
                     "test work in general. Something structural has to give."),
                    ("Give up on algebra for spaces",
                     "An honest response, and for a long time the practical "
                     "one: people simply avoided the operations that break. "
                     "The cost is high, because the operations that break are "
                     "the ones you most want &mdash; taking a quotient, "
                     "measuring what is left over, subtracting."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "List everything you can say about the dust using its "
                    "members alone.",
                    "List everything you can say about the ruler using its "
                    "members alone.",
                    "Compare the two lists.",
                    "Now ask which of the two objects a calculation that only "
                    "reads members is working on.",
                ),
                found="The two lists are identical, word for word, because the "
                      "member layer of the dust and the member layer of the "
                      "ruler are the same object. So a calculation that reads "
                      "only members can't tell you which one it is working "
                      "on &mdash; and it won't report an error, because "
                      "from where it stands nothing is missing. That is the "
                      "exact predicament of the next world: the standard "
                      "algebra test reads members, and it is about to give a "
                      "confident wrong answer.",
            ),
            Name(
                plain="two layers badly glued",
                standard="the failure of topological abelian groups to form an "
                         "abelian category",
                notation="Top. ab. groups: not abelian",
                why="The word abelian here has grown a second meaning: it now "
                    "describes a whole world of objects in which the standard "
                    "algebra tests are guaranteed to work. World 3 shows what "
                    "the guarantee is, and how badly this world fails it.",
            ),
            Math(
                statement="&#8477;<sub>disc</sub> &rarr; &#8477; : "
                          "ker = 0, &nbsp; coker = 0, &nbsp; not an isomorphism",
                reading="Two words you haven't met yet, ker and coker, are "
                        "left standing here on purpose. They are the two "
                        "measurements algebra makes on a map, and the next "
                        "world builds both from nothing. The line says that on "
                        "this bridge both measurements read zero, which "
                        "ordinarily forces a sameness, and yet there is no "
                        "sameness.",
                cite="Example 1.9, page 9 of the lectures",
                url="https://arxiv.org/pdf/2605.03658v1#page=9",
            ),
        ),
        hold="Ordinary algebra sees the points but can miss the separate "
             "nearness layer and the topology stored there.",
    ),
)


WORLD = World(
    number=2,
    slug="nearness",
    title="Nearness and a one-way bridge",
    promise="You will build two spaces from the same numbers. Their points "
            "match perfectly, but the spaces do not. That mismatch sets up "
            "the rest of the course.",
    bricks=BRICKS,
)

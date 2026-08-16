"""World 4.  The change of question, and the objects that ask it.

A probe is the one genuinely new object in the subject, and it is concrete: a
box split in two, and again, forever, with every stage still finite.  The
world builds it by hand before naming it, because the standard name --
profinite set -- carries none of the picture.
"""

from __future__ import annotations

from ..model import Ask, Brick, Math, Name, Play, Say, Try, World


BRICKS = (

    Brick(
        slug="a-different-question",
        title="Describe a space from the outside",
        idea="Instead of listing a space's points, describe the space by seeing how different test spaces can map into it.",
        need=(
            "That the leftover on the bridge is real and has no members.",
            "A map: every member of the source answered exactly once.",
        ),
        concept=(
            Say('The repair starts by asking a different question. Do not only ask which points are inside a space. Ask which test spaces can walk into it continuously, without tearing.'),
            Say('Collect every continuous walk from every test space. Together, those walks describe the space in a way that includes its nearness information.'),
        ),
        intuition=(
            Say("You already know how to find out what a room is like without "
                "listing its contents: you walk into it, along different "
                "paths, at different speeds, and from the way the walks go you "
                "learn the shape of the room."),
            Ask(
                "Would this new description tell the dust and the ruler "
                "apart?",
                (
                    ("Yes, if the walks are allowed to be crowded",
                     "That is exactly the condition. A walk that closes in "
                     "on a destination can enter the ruler, because arriving "
                     "is allowed there. The same walk can't enter the dust "
                     "gently, because on the dust arriving would mean tearing. "
                     "Different answers, so different objects. The description "
                     "sees what counting members couldn't."),
                    ("No, they have the same points",
                     "The points are the same, but the walks aren't: the "
                     "question has changed from <em>who is inside</em> to "
                     "<em>who can get in gently</em>, and the nearness rule "
                     "controls the second one completely. That is why the "
                     "change of question is worth making."),
                    ("Only if I use enough walks",
                     "The right worry, and the answer is to use all of them at "
                     "once. Not a chosen sample: every continuous map from every "
                     "possible walker. Then nothing can hide."),
                ),
                after="Now the question becomes: which walkers? Choose them "
                      "badly and the description is useless. The next three "
                      "bricks build the right ones.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Let the walker be a single point, and count the continuous "
                    "walks from it into the dust.",
                    "Count the continuous maps from a single point into the "
                    "ruler.",
                    "Compare the two counts.",
                    "Now say what walker you would need to get "
                    "different answers.",
                ),
                found="Both counts are the same: one continuous map per number, "
                      "in each case, because a map from a single point is just "
                      "a choice of destination and nothing can tear. So the "
                      "one-point walker sees exactly what counting members "
                      "saw, and no more. To separate the two you need a walker "
                      "with infinitely many points that crowd together "
                      "&mdash; something that can be closing in on a "
                      "destination. Building that walker is the next brick, "
                      "and you now know why it has to be infinite.",
            ),
            Name(
                plain="a continuous map into a space",
                standard="a continuous map into the space",
                notation="S &rarr; X",
                why="The walker S is a space in its own right, and the walk is "
                    "an arrow from it into X. Describing X by all such arrows "
                    "is called describing it by its functor of points.",
            ),
            Math(
                statement="X &nbsp;&#8605;&nbsp; ( S &#8614; C(S, X) )",
                reading="C(S, X) is the standard name for all continuous maps "
                        "from S to X. The squiggly arrow means <em>is replaced "
                        "by</em>. So: instead of the space X itself, keep the "
                        "rule that takes any walker S and returns every continuous "
                        "walk from S into X. The rest of this world decides "
                        "which S are allowed.",
            ),
        ),
        hold='You can describe a space through all continuous maps into it, not just through its individual points.',
    ),

    Brick(
        slug="splitting-forever",
        title="A box that keeps splitting",
        idea='A probe is a tower of finite stages. Each stage splits the earlier boxes, and every new box remembers its parent.',
        need=(
            "A collection, and a map between collections.",
        ),
        concept=(
            Say('Build the test space step by step. Start with one box, split it in two, then split those boxes again. Every stage still has only finitely many boxes.'),
            Say('The important part is the family tree: every small box remembers which larger box it came from. That memory connects all the stages into one probe.'),
        ),
        intuition=(
            Say("It is the shape of any address system. A country, then a "
                "region, then a street, then a door: each level refines the "
                "one above and remembers it. No single level pins down a "
                "house, and the whole endless address does."),
            Ask(
                "Never mind the stages. What does an infinite <em>path</em> "
                "through the boxes pick out?",
                (
                    ("One point, in the limit",
                     "Yes. Left, right, right, left, &hellip; forever narrows "
                     "onto a single position. A choice at every stage is "
                     "exactly a point of the finished object, and it takes "
                     "infinitely many choices to specify one."),
                    ("A small box",
                     "A small box is what you get after finitely many choices, "
                     "and it still contains endlessly many positions inside "
                     "it. Only an endless sequence of choices narrows all the "
                     "way down to one."),
                    ("Nothing, the boxes never end",
                     "They never end, and that is what makes the object "
                     "interesting instead of finite. But an unending sequence "
                     "of choices is a perfectly good thing to name, and it "
                     "names one position."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="split",
                prompt="Add stages and watch the boxes multiply.",
                notice="Two things at once, and they are the whole design. "
                       "Every single stage is finite, so nothing is out of "
                       "reach: the readout can list every box there is. And "
                       "the count doubles at every stage, so the tower as a "
                       "whole is nothing like finite.",
                params={"kind": "halving", "depth": 3},
            ),
            Name(
                plain="a box split forever",
                standard="the Cantor set, as a profinite set",
                notation="{0,1}<sup>&#8469;</sup>",
                why="Each stage is the collection of finite strings of choices, "
                    "each written from 0 and 1; the finished object is the "
                    "collection of endless strings. Profinite means built from "
                    "finite stages: <em>pro</em>, meaning assembled from, plus "
                    "finite.",
            ),
            Math(
                statement="S<sub>0</sub> &larr; S<sub>1</sub> &larr; "
                          "S<sub>2</sub> &larr; &#8943; &nbsp;&middot;&nbsp; "
                          "S = lim<sub>&#8592;</sub> S<sub>n</sub>",
                reading="Each S<sub>n</sub> is a finite collection: the boxes "
                        "at stage n. The arrows point backwards because each "
                        "small box remembers its parent. The symbol "
                        "lim<sub>&#8592;</sub> is the inverse limit: the "
                        "collection of all compatible choices, one at every "
                        "stage, each agreeing with the one before. That "
                        "compatible family is a point of S.",
            ),
        ),
        hold='A probe is a tower of finite stages linked backward. A point is one compatible choice followed through every stage.',
    ),

    Brick(
        slug="other-probes",
        title="Three kinds of probe",
        idea='Any tower of linked finite stages is a probe. Different splitting rules create very different kinds of probes.',
        need=(
            "A tower of finite stages with backwards maps.",
        ),
        concept=(
            Say('You do not have to split boxes in half. Split them into three or ten, or use a completely different finite pattern at each stage.'),
            Say('Only two rules matter: every stage is finite, and it remembers the previous stage. Those simple rules allow many different probe shapes.'),
        ),
        intuition=(
            Say("The third walker is the one that matters most for the bridge: "
                "it is a sequence closing in on a destination, and it is "
                "exactly the shape of walk that the dust refuses to admit. "
                "Keep an eye on it as you build the others."),
            Ask(
                "Why insist that every stage be finite?",
                (
                    ("Because then every question is settled by finitely much",
                     "That is the payoff, and it is worth more than it looks. "
                     "Any continuous map out of such a walker is decided at some "
                     "finite stage. Endless objects usually resist "
                     "computation; these don't, because all the work happens "
                     "in a finite picture."),
                    ("To keep the drawings small",
                     "Convenient, but not the reason. The reason is that a "
                     "finite stage can be checked exhaustively, so anything "
                     "the walker says is decided by a finite amount of data "
                     "even though the walker itself is infinite."),
                    ("So they fit inside the line",
                     "Some do and some don't, and it isn't required either "
                     "way. The condition is only about the stages: each one "
                     "finite, with backwards maps."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="split",
                prompt="Switch between the three walkers and watch how the "
                       "stages grow.",
                notice="Halving doubles each stage, splitting in three "
                       "triples, and the approaching walker grows by exactly "
                       "one point each time. All three satisfy the one "
                       "condition being imposed, and their sizes are as "
                       "different as they could be. Finiteness at each stage "
                       "is a weak demand; it is the endlessness of the tower "
                       "that does the work.",
                params={"kind": "pick", "depth": 3},
            ),
            Name(
                plain="walkers built from finite stages",
                standard="profinite sets, equivalently compact Hausdorff "
                         "totally disconnected spaces",
                notation="S = lim<sub>&#8592;</sub> S<sub>i</sub>, each "
                         "S<sub>i</sub> finite",
                why="<em>Compact</em>: no escaping to infinity. "
                    "<em>Hausdorff</em>: any two points can be separated. "
                    "<em>Totally disconnected</em>: no piece is joined "
                    "together. The three conditions together say exactly "
                    "<em>assembled from finite stages</em>.",
            ),
            Math(
                statement="|S<sub>n</sub>| = 2<sup>n</sup> "
                          "&nbsp;&middot;&nbsp; 3<sup>n</sup> "
                          "&nbsp;&middot;&nbsp; n + 2",
                reading="The bars mean <em>how many members</em>. The three "
                        "growth rates belong to the halving walker, the "
                        "splitting-in-three walker, and the approaching "
                        "walker, whose stage n holds the numbers 0 to n plus "
                        "its destination. Every one of these numbers is "
                        "computed on this page from the tower itself, not "
                        "quoted.",
            ),
        ),
        hold='Probes come in many shapes, but every stage is finite and records how it connects to the previous stage.',
    ),

    Brick(
        slug="what-a-shape-says",
        title="Use a probe to question a space",
        idea='A probe questions a space by mapping into it continuously. The dust and ruler give different answers.',
        need=(
            "A probe: a tower of finite stages.",
            "A continuous map: one that doesn't tear.",
        ),
        concept=(
            Say("Send a probe into a space and collect every continuous map you can make. That collection is the space's answer to the probe."),
            Say('The approaching probe can arrive on the ruler. In the dust, a continuous map must eventually settle on only finitely many values. One probe exposes the difference.'),
        ),
        intuition=(
            Say("A continuous map out of a probe is decided box by box: choose a "
                "value on each box of some stage, and you have described a "
                "walk. So the answers aren't mysterious objects &mdash; they "
                "are choices on a finite picture, and you can count them."),
            Ask(
                "Two spaces, same members, different answers to every probe. "
                "Same object or not?",
                (
                    ("Not the same, and now it is provable",
                     "That is the change. Previously the difference was real "
                     "but invisible to the algebra. Now the difference is "
                     "written into the description itself: one object says "
                     "something to a probe, the other says something else, and "
                     "the two descriptions are plainly unequal."),
                    ("Same, the members still match",
                     "The members do match, but members are no longer what the "
                     "object <em>is</em>. The object is now the whole table of "
                     "answers, and the tables differ. Matching members is a "
                     "statement about one row of the table."),
                    ("Cannot tell without checking every probe",
                     "Strictly true and cheap to satisfy: one probe already "
                     "gives different answers, and one difference is enough to "
                     "settle it."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="landings",
                prompt="Count the continuous maps from a probe into a two-point "
                       "target, stage by stage.",
                notice="The count at stage n is 2 raised to the number of "
                       "boxes at that stage, because a continuous map is exactly "
                       "one choice of value per box. It is the same count you "
                       "made by hand in world 1 with three numbers and two "
                       "colours &mdash; the same shape of answer, now indexing "
                       "an entire description.",
                params={"kind": "halving"},
            ),
            Name(
                plain="how a space responds to a probe",
                standard="the set of continuous maps from the probe",
                notation="X(S) = C(S, X)",
                why="Read X(S) as <em>how X responds to S</em>. The space is "
                    "beginning to be treated as a rule that answers probes, "
                    "which is what it will become in the next world.",
            ),
            Math(
                statement="&#8477;(S) = C(S, &#8477;) &nbsp;&middot;&nbsp; "
                          "&#8477;<sub>disc</sub>(S) = C<sub>lc</sub>(S, "
                          "&#8477;)",
                reading="The subscript lc means locally constant: a map that "
                        "is constant on each box of some finite stage. Those "
                        "are exactly the continuous maps into the dust, since "
                        "anything finer would have to tear. The two answers "
                        "differ for any probe with infinitely many points, and "
                        "that difference is the whole content of Example 1.9 "
                        "made visible.",
                cite="Example 1.9, page 9 of the lectures",
                url="https://arxiv.org/pdf/2605.03658v1#page=9",
            ),
        ),
        hold='Each probe gets a collection of answers from a space. The right probe can tell the dust and ruler apart.',
    ),

    Brick(
        slug="why-this-works",
        title="Why probes use finite stages",
        idea='Finite stages keep each calculation manageable, while the endless tower can still describe crowding and limits.',
        need=(
            "Probes built from finite stages, and what a shape says to one.",
        ),
        concept=(
            Say('The construction balances two needs. Each stage stays finite so you can calculate with it, but the tower keeps going so it can describe points crowding together or approaching a limit.'),
            Say('A completely finite walker misses that behavior. A single infinite stage is too large to calculate with directly. The tower gives us both benefits.'),
        ),
        intuition=(
            Say("The design is the same one behind any good instrument: fine "
                "enough to detect the effect, coarse enough to be read. Here "
                "the effect is crowding and the reading is done stage by "
                "finite stage."),
            Ask(
                "Could you use the ruler itself as the walker instead?",
                (
                    ("You could, but you would be assuming what you are "
                     "describing",
                     "That is the objection. Using the ruler to describe "
                     "spaces means the ruler's own nearness is taken as given "
                     "and never explained. Probes are built out of finite "
                     "collections and nothing else, so the description rests "
                     "on something you can hold entirely in your hand."),
                    ("Yes, that would be simpler",
                     "Simpler to state and much worse to work with: the "
                     "answers stop being computable at any finite stage, and "
                     "the good algebraic behaviour is lost. The finiteness at "
                     "every stage is doing real work, not decoration."),
                    ("No, that isn't allowed",
                     "It is allowed to try &mdash; nothing forbids it &mdash; "
                     "and it is what the older approaches effectively did. The "
                     "objection isn't legality but circularity, and the cost "
                     "in computability."),
                ),
                after="One more demand is needed before the description can be "
                      "an object in its own right: it must survive being cut "
                      "and glued. That is world 5.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the walker with exactly two points and no further "
                    "stages.",
                    "Count the continuous maps from it into the dust, and then "
                    "into the ruler.",
                    "Now take the approaching walker and ask whether the walk "
                    "that arrives at the destination is continuous into the ruler, "
                    "and then into the dust.",
                ),
                found="For the two-point walker the counts agree: any map from "
                      "a finite collection is continuous, whatever the target, so "
                      "a finite walker can't separate dust from ruler at all. "
                      "For the approaching walker they part company: the "
                      "arriving walk is continuous into the ruler and not continuous "
                      "into the dust, because on the dust arriving means "
                      "tearing. That single contrast is the reason the tower "
                      "has to be infinite, and you have just found it "
                      "yourself instead of been told it.",
            ),
            Name(
                plain="a walker made from finite pictures",
                standard="an extremally disconnected, or profinite, test object",
                notation="ProFin, the category of profinite sets",
                why="The lectures use profinite sets as the site, and a "
                    "particularly well-behaved subfamily &mdash; the "
                    "extremally disconnected ones &mdash; when the gluing "
                    "condition needs to become automatic. That family reappears "
                    "in world 5.",
            ),
            Math(
                statement="S = lim<sub>&#8592;</sub> S<sub>i</sub> "
                          "&nbsp;&rArr;&nbsp; C(S, T) = "
                          "colim<sub>&#8594;</sub> C(S<sub>i</sub>, T) "
                          "for finite T",
                reading="colim<sub>&#8594;</sub> is the forwards companion of "
                        "the inverse limit: it collects everything that "
                        "appears at some finite stage. The line says that a "
                        "continuous map from an infinite probe into a finite "
                        "target is always already visible at one finite stage. "
                        "That is the computability the finiteness bought, "
                        "stated exactly.",
            ),
        ),
        hold='Finite stages are manageable, and the endless tower still captures arbitrarily fine crowding.',
    ),
)


WORLD = World(
    number=4,
    slug="probes",
    title="Study spaces with probes",
    promise="You will build the subject's basic test objects from finite stages and use one to separate spaces that point-counting cannot tell apart.",
    bricks=BRICKS,
)

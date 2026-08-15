"""World 5.  The table of answers becomes the object.

Two rules turn a table of answers into something worth calling a space: it
must survive being cut, and separate answers that agree where they meet must
glue back into one.  That is the sheaf condition, built here from a reader
cutting a probe in half.
"""

from __future__ import annotations

from ..model import Ask, Brick, Math, Name, Play, Say, Try, World


BRICKS = (

    Brick(
        slug="the-answer-sheet",
        title="Keep the answers, throw away the space",
        idea="Declare the table of answers to be the object, and tables become "
             "possible that no space could produce.",
        need=(
            "A probe, and what a shape says to it: all the gentle walks in.",
        ),
        concept=(
            Say("You have a table. Down one side, every probe. In each row, "
                "everything that probe can say when it walks into your space. "
                "The table is enormous, and it is completely determined by the "
                "space."),
            Say("Now do the disrespectful thing: throw the space away and keep "
                "the table. Declare that the table <em>is</em> the object. "
                "Nothing is lost that any probe could have detected, and "
                "something is gained, because tables can exist that no space "
                "produced."),
        ),
        intuition=(
            Say("It is the move from <em>what is this thing made of</em> to "
                "<em>how does this thing respond</em>. The second question is "
                "answerable for things the first question cannot even reach, "
                "and the row indexed by the one-point probe is where the old "
                "question survives."),
            Ask(
                "What could a table do that a space cannot?",
                (
                    ("Answer nothing to points and something to bigger probes",
                     "That is the strange object from world 3's specification, "
                     "and here is where it becomes possible. The row for the "
                     "one-point probe can read empty while a row further down "
                     "is full. No space behaves like that. A table can."),
                    ("Nothing, tables come from spaces",
                     "Every space gives a table, but not every table comes "
                     "from a space &mdash; and the extra ones are exactly what "
                     "was needed. The leftover on the bridge is going to be "
                     "one of them."),
                    ("Contradict itself",
                     "Not allowed: two rules are about to be imposed, and they "
                     "are exactly what stops a table from being nonsense. "
                     "Within those rules a table is as legitimate an object as "
                     "any space."),
                ),
                after="The one-point probe is the row that asks <em>which "
                      "points do you have</em>. An object with that row empty "
                      "and other rows full is an object with no points that is "
                      "not zero.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Write down the row of the ruler's table indexed by the "
                    "one-point probe.",
                    "Write down the row of the dust's table indexed by the "
                    "same probe.",
                    "Now write down what you would have to change in one table "
                    "to turn it into the other.",
                ),
                found="Both rows are the same: one gentle walk per number. To "
                      "turn one table into the other you would have to change "
                      "rows further down &mdash; the ones indexed by probes "
                      "with infinitely many points &mdash; and nothing you do "
                      "to the first row will do it. So the table has room to "
                      "record a difference in a place the old point-set had no "
                      "room for. That room is the entire gain, and everything "
                      "in world 6 is spent inside it.",
            ),
            Name(
                plain="the table of answers",
                standard="a presheaf on profinite sets",
                notation="X : ProFin<sup>op</sup> &rarr; Set",
                why="The superscript op records that the arrows run backwards: "
                    "a map between probes makes answers travel the other way. "
                    "That backwards travel is the next brick.",
            ),
            Math(
                statement="X(*) = the points of X &nbsp;&middot;&nbsp; "
                          "X(*) = &empty; and X(S) &ne; &empty; is permitted",
                reading="The star * is the one-point probe, and the row it "
                        "indexes is the ordinary point-set of X. The second "
                        "line is the whole freedom the change of object "
                        "bought: no points, and yet not nothing. In the "
                        "additive version this reads X(*) = 0 with X(S) "
                        "&ne; 0.",
            ),
        ),
        hold="The object is now the table of answers. Tables exist that no "
             "space produces, and those are the ones needed.",
    ),

    Brick(
        slug="cutting",
        title="Every answer can be read on a smaller probe",
        idea="Whenever one probe maps into another, answers travel backwards "
             "along that map, automatically and with no choices made.",
        need=(
            "The table of answers, indexed by probes.",
            "A map: every member of the source answered exactly once.",
        ),
        concept=(
            Say("Probes map to each other. A single point sits inside the "
                "halving probe. A stage-two picture sits above a stage-one "
                "picture. Whenever one probe maps into another, something "
                "automatic happens to the answers."),
            Say("If you know a walk from the big probe, you know one from the "
                "small probe: go in along the map, then walk. Answers travel "
                "backwards along maps of probes, always, with no choices "
                "made."),
        ),
        intuition=(
            Say("It is what any measurement does when you narrow the sample. "
                "A reading taken over a whole region can be read off over any "
                "part of it, and no new work is needed to do so &mdash; the "
                "restriction is already contained in what you have."),
            Ask(
                "You know a walk from the halving probe. Does that tell you "
                "the value at one particular point of it?",
                (
                    ("Yes, just look at that point",
                     "Yes, and that is the backwards travel in its smallest "
                     "case: a point maps into the probe, so any answer on the "
                     "probe can be read at that point. Restriction is nothing "
                     "more mysterious than looking at part of what you already "
                     "have."),
                    ("No, the walk is about the whole probe",
                     "It is about the whole probe, and reading it at one point "
                     "is exactly what the backwards travel does. Nothing extra "
                     "is needed; the map from the point supplies it."),
                    ("Only if the walk is nice",
                     "No niceness required: composing a gentle map with a "
                     "gentle map is gentle, so the reading always exists."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take a gentle walk out of the stage-2 halving probe: "
                    "assign a value to each of its four boxes.",
                    "Restrict it along the map that includes one point of the "
                    "probe, and write what you get.",
                    "Restrict it instead along the map from stage 3 down to "
                    "stage 2, and write what you get.",
                    "Then restrict twice in a row and compare with restricting "
                    "along the combined map.",
                ),
                found="The first restriction gives a single value; the second "
                      "gives each of the eight stage-3 boxes the value of the "
                      "stage-2 box it came out of. And doing two restrictions "
                      "in a row gives exactly what the combined map gives "
                      "&mdash; no discrepancy is possible, because both are "
                      "just <em>go in, then walk</em>. That agreement is the "
                      "second line of the mathematics below, and you have now "
                      "checked it rather than accepted it.",
            ),
            Name(
                plain="reading an answer on a smaller probe",
                standard="restriction, or functoriality",
                notation="f : S&prime; &rarr; S &nbsp;&rArr;&nbsp; "
                         "X(f) : X(S) &rarr; X(S&prime;)",
                why="The name <em>presheaf</em> means exactly this much "
                    "structure: a row for every probe, and a backwards travel "
                    "for every map of probes, compatible with doing two maps "
                    "in a row.",
            ),
            Math(
                statement="X(id) = id &nbsp;&middot;&nbsp; "
                          "X(g &compfn; f) = X(f) &compfn; X(g)",
                reading="Two housekeeping demands. Restricting along the "
                        "do-nothing map changes nothing. And restricting along "
                        "two maps in a row is the same as restricting along "
                        "their composite &mdash; with the order swapped, since "
                        "answers travel backwards. Together they say the "
                        "backwards travel is honest bookkeeping and not an "
                        "extra choice.",
            ),
        ),
        hold="Answers travel backwards along maps of probes, automatically and "
             "compatibly.",
    ),

    Brick(
        slug="gluing",
        title="Answers that agree where they meet must glue",
        idea="Local answers that agree on the overlap must assemble into "
             "exactly one global answer: not none, and not several.",
        need=(
            "Restriction: reading an answer on a smaller probe.",
            "A probe: a tower of finite stages, built from boxes.",
        ),
        concept=(
            Say("Cut a probe in two. The halving probe splits cleanly into the "
                "walks starting left and the walks starting right, and each "
                "half is a probe in its own right."),
            Say("Now suppose someone hands you an answer on each half. If the "
                "two are consistent, there must be exactly one answer on the "
                "whole probe restricting to both. Not none, and not several. "
                "Exactly one."),
        ),
        intuition=(
            Say("It is the condition under which local records can be trusted "
                "as a description of the whole. Survey each district and get "
                "consistent results, and there should be exactly one national "
                "picture they came from &mdash; if there could be two, the "
                "districts were not recording everything."),
            Ask(
                "Why insist on <em>exactly</em> one, rather than at least "
                "one?",
                (
                    ("Because two would mean the probe forgot something",
                     "Right. If two different whole answers restricted to the "
                     "same pair of halves, the table would be recording "
                     "information that no probe can detect &mdash; and the "
                     "whole point of the construction is that the probes see "
                     "everything. Uniqueness is what keeps the table honest."),
                    ("To make it easier to compute",
                     "It does make computation possible, since answers can be "
                     "assembled from local ones without ambiguity. But the "
                     "deeper reason is honesty: two answers agreeing "
                     "everywhere probes can look would be a difference no "
                     "probe could ever see."),
                    ("Convention",
                     "Not convention. Drop uniqueness and the table can carry "
                     "phantom distinctions; drop existence and local answers "
                     "cannot be assembled. Both halves of the demand are "
                     "doing work."),
                ),
            ),
        ),
        experiment=(
            Play(
                widget="glue",
                prompt="Set a value on each piece, and change whether the "
                       "pieces meet.",
                notice="Cut cleanly apart, any two answers glue: there is no "
                       "shared ground to disagree on, so the demand is "
                       "automatic. Let the pieces share a middle and the two "
                       "answers must agree there or nothing glues at all. The "
                       "condition has content exactly where pieces meet, which "
                       "is why the next brick can make it vanish.",
                params={},
            ),
            Name(
                plain="cut and glue",
                standard="the sheaf condition",
                notation="X(S &#8852; T) = X(S) &times; X(T)",
                why="The symbol &#8852; is a disjoint union: two probes placed "
                    "side by side with nothing shared. The equation says the "
                    "answers on a side-by-side pair are exactly one answer for "
                    "each piece, which is the simplest instance of gluing.",
            ),
            Math(
                statement="X(S) &rarr; X(S&prime;) "
                          "&#8649; X(S&prime; &times;<sub>S</sub> S&prime;) "
                          "&nbsp; an equaliser",
                reading="S&prime; &rarr; S is a cover, meaning it hits "
                        "everything. The double arrow expresses the two ways "
                        "of restricting to the overlap S&prime; "
                        "&times;<sub>S</sub> S&prime;, which is the collection "
                        "of pairs of points of S&prime; lying over the same "
                        "point of S. <em>Equaliser</em> is the one-word form "
                        "of the demand: the answers on S are exactly the "
                        "answers on S&prime; on which those two restrictions "
                        "agree. Exactly one, no more.",
            ),
        ),
        hold="Local answers that agree where they meet glue to exactly one "
             "global answer. That is the sheaf condition.",
    ),

    Brick(
        slug="a-condensed-set",
        title="The object, finally",
        idea="A condensed set is a table of answers to probes, with backwards "
             "travel, obeying cut and glue. That is the replacement for a "
             "space.",
        need=(
            "The table of answers, restriction, and the gluing demand.",
        ),
        concept=(
            Say("Collect the three requirements. A row of answers for every "
                "probe. Backwards travel along every map of probes. And the "
                "gluing demand, so that local answers assemble uniquely."),
            Say("A table meeting all three is the replacement for a space. It "
                "is not a space with extra structure and not a space with "
                "structure removed. It is a different kind of thing, and "
                "spaces sit inside it."),
        ),
        intuition=(
            Say("Nothing exotic has been introduced. Every ingredient was "
                "something you were already doing to spaces without naming it: "
                "mapping things in, restricting what you found, assembling "
                "local pictures. The only real step was deciding that those "
                "activities <em>are</em> the object."),
            Ask(
                "Does the ruler give such a table?",
                (
                    ("Yes: its answers are the gentle walks",
                     "It does, and checking it is routine. Gentle walks "
                     "restrict along maps of probes, and gentle walks that "
                     "agree on the overlap of a cover patch together into one "
                     "gentle walk. Every space you have ever used produces a "
                     "table satisfying all three demands."),
                    ("Only if the ruler is nice enough",
                     "Every topological space produces such a table. Niceness "
                     "is needed for a different question &mdash; whether the "
                     "table remembers the space exactly &mdash; and that "
                     "question is answered in the next world."),
                    ("No, the ruler has too many points",
                     "Size is not an obstacle here. The table is large, "
                     "certainly, but each row is a perfectly ordinary "
                     "collection of gentle walks."),
                ),
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Check the three demands for the ruler's table, one at a "
                    "time.",
                    "Row for every probe: what is it?",
                    "Backwards travel: given a walk and a map of probes, how "
                    "do you produce the restricted walk?",
                    "Gluing: two gentle walks agreeing where the pieces meet "
                    "&mdash; is the combined rule gentle?",
                ),
                found="Row: the gentle walks from that probe into the ruler. "
                      "Backwards travel: compose &mdash; go in along the map, "
                      "then walk. Gluing: yes, because gentleness is checked "
                      "piece by piece, so a rule that is gentle on each piece "
                      "of a cover and consistent on the overlaps is gentle "
                      "overall. All three hold with no cleverness at all, "
                      "which is the point: the demands were chosen to be "
                      "things spaces already satisfy.",
            ),
            Name(
                plain="a table of answers obeying cut and glue",
                standard="a condensed set",
                notation="X : ProFin<sup>op</sup> &rarr; Set, a sheaf",
                why="Replace Set by abelian groups and you get a condensed "
                    "abelian group: every row is a collection you can add in, "
                    "and the backwards travel respects the adding. That is the "
                    "version world 6 needs.",
            ),
            Math(
                statement="Cond(Set) = Sh(ProFin) &nbsp;&middot;&nbsp; "
                          "X &#8614; ( S &#8614; C(S, X) )",
                reading="Sh means sheaves. The second line is the recipe that "
                        "turns an ordinary space into a condensed set: its row "
                        "at S is all continuous maps from S into it. The "
                        "lectures set this up in Lecture I and are careful "
                        "about the set-theoretic size of ProFin, which is a "
                        "genuine technical point and not a formality.",
                cite="Lecture I, Definition 1.2 and following, page 6 onwards",
                url="https://arxiv.org/pdf/2605.03658v1#page=6",
            ),
        ),
        hold="A condensed set is a table of answers to probes obeying cut and "
             "glue. Spaces produce them; not all of them come from spaces.",
    ),

    Brick(
        slug="probes-that-need-no-glue",
        title="The probes where gluing is free",
        idea="On probes whose covers can always be undone, the gluing demand "
             "is automatic &mdash; and every probe is covered by one of those.",
        need=(
            "The gluing demand, and probes built from finite stages.",
        ),
        concept=(
            Say("The gluing demand is the awkward one to check: it quantifies "
                "over every cover of every probe. There is a family of probes "
                "on which it costs nothing at all."),
            Say("They are the probes where every cover can be undone: given a "
                "cover, there is always a way to choose, gently and "
                "consistently, one point above each point. Nothing has to be "
                "folded together, so there is nothing for two answers to "
                "disagree about."),
        ),
        intuition=(
            Say("You saw the mechanism in the previous experiment. When the "
                "pieces did not meet, gluing was free; the demand only had "
                "teeth where they overlapped. A cover that can be undone is "
                "the same situation writ large: no folding, so no overlap to "
                "argue over."),
            Ask(
                "If every cover of a probe can be undone, what happens to the "
                "gluing demand there?",
                (
                    ("It becomes automatic",
                     "It does. The demand only has teeth where a cover folds "
                     "points together; if the folding can always be undone, "
                     "any answer downstairs is read off from upstairs with "
                     "nothing left to check. On those probes a table is just a "
                     "row for each probe and the backwards travel."),
                    ("It gets harder",
                     "The opposite: it is the folding that creates the "
                     "obligation, so removing the folding removes the "
                     "obligation. These probes are chosen precisely because "
                     "they make the condition vanish."),
                    ("It stays the same",
                     "Not on this family. The equaliser condition compares two "
                     "restrictions to an overlap; when the cover splits, the "
                     "comparison is trivially satisfied and nothing remains to "
                     "impose."),
                ),
                after="This is why the lectures introduce these probes early: "
                      "they turn a condition that must be checked into a "
                      "condition that cannot fail.",
            ),
        ),
        experiment=(
            Try(
                steps=(
                    "Take the cover of a two-point probe by a four-point "
                    "probe, two points sitting over each.",
                    "Choose one point upstairs over each point downstairs, and "
                    "check that your choice is a map of probes.",
                    "Now take an answer upstairs and read it downstairs "
                    "through your choice.",
                    "Ask what could have gone wrong if no such choice existed.",
                ),
                found="Your choice exists &mdash; pick either point over each "
                      "&mdash; and once it does, an answer downstairs is "
                      "simply an answer upstairs read through it, with nothing "
                      "to verify. Had no choice existed, you would have to "
                      "check that the two ways of restricting to the overlap "
                      "agree before you could conclude anything. That check is "
                      "the whole of the gluing demand, and a splitting cover "
                      "removes it.",
            ),
            Name(
                plain="probes where every cover can be undone",
                standard="extremally disconnected profinite sets",
                notation="every surjection onto S splits",
                why="They are exactly the projective objects among probes, and "
                    "they are plentiful: every probe is covered by one. So "
                    "nothing is lost by working with them.",
            ),
            Math(
                statement="S extremally disconnected, T &#8608; S "
                          "&nbsp;&rArr;&nbsp; &exist; s : S &rarr; T with "
                          "T &compfn; s = id",
                reading="The two-headed arrow &#8608; means the map hits "
                        "everything. The line says a section s exists: a "
                        "gentle way of choosing a point upstairs over every "
                        "point downstairs, undoing the cover exactly. On such "
                        "probes, sheaves and mere tables of answers agree, "
                        "which is Proposition 2.7 of the lectures.",
                cite="Proposition 2.7, page 12 of the lectures",
                url="https://arxiv.org/pdf/2605.03658v1#page=12",
            ),
        ),
        hold="On probes whose covers all split, the gluing demand is free, and "
             "every probe is covered by one of those.",
    ),
)


WORLD = World(
    number=5,
    slug="the-answer-sheet",
    title="The table of answers becomes the object",
    promise="By the end you will have replaced the idea of a space with "
            "something that has no points in it at all, and seen why the "
            "replacement is not a loss.",
    bricks=BRICKS,
)

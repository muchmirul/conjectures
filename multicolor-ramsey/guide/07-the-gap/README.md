# 7 · The gap

**The reasoning, concluded.** The walkthrough clears away the tempting shortcuts, in both directions, before the construction begins.

The lower and upper limits can now be placed on the same chart.

![The safe groups known from constructions below and the factorial upper limit above, with the unknown region between them](gap.png)

The lower edge shows group sizes that can actually be kept safe by multiplying known examples. It grows through repeated multiplication by a fixed amount. The upper edge comes from the sorting argument and grows like a factorial, whose multiplying amount rises with every colour. The two kinds of growth move farther apart as more colours are added. Decades of work improved the fixed lower score from 2.24 toward 3.28, but the broad gap remained.

Several attractive shortcuts failed. One of the simplest uses different orderings of the same items.

Take every ordering of a small set of letters. For each pair of orderings, find the first position where they differ and use that position as the connection's colour. Three letters have six orderings, but only the first two positions can be the first difference. If this idea worked, it would keep six people safe with two colours and beat the five-person limit.

![Six letter orderings coloured by their first difference until a one-colour triangle appears](orderings.gif)

It fails. The orderings ABC, BAC and CAB all first differ from one another at the first letter. Their three connections therefore receive the same colour. The same collision can be built with any larger number of items. Recording more detail in each colour can prevent this particular collision, but it also uses so many extra colours that the hoped-for advantage disappears.

Attempts in the opposite direction, proving that the score must settle below a ceiling, also failed. One tempting plan gave each colour's connections a compact summary and multiplied the summaries together. The plan needed every triangle-free pattern to be simple, and in particular to split into a fixed handful of teams, meaning groups of people with no connection inside any one of them; section 9 returns to teams. Triangle-free patterns refuse to be that simple. The next picture shows the classical example this repository rebuilds and checks by exhaustion: eleven people, no triangle anywhere, and no split into three teams can work.

![Eleven people with no triangle at all, whose people still cannot be split into three connection-free teams](groetzsch.png)

Four teams are needed here, and taller versions of the same construction need five, six, or any number you name. Triangle-free does not mean simple, and the summary plan collapsed with that hope.

Addition patterns on number circles face another version of the same difficulty. Every colour, viewed alone, must contain no triangle. Simple methods achieve that by keeping each colour in a restricted part of the construction. To make the people-per-colour score grow, many different rooms must be able to reuse the same colours without letting the reused pieces join into a triangle. The 2026 construction provides a fixed global rule that makes this reuse safe.

---

[← The ceiling](../06-the-ceiling/README.md)  ·  [Palettes →](../08-palettes/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

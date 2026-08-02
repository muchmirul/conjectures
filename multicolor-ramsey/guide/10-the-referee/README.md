# 10 · The referee

Every connection between two rooms needs two choices: a colour allowed by the palettes, and a team on which it may safely land. These choices cannot be improvised for one pair and changed for the next. A single rule must work for every pair of people in every pair of rooms.

The construction begins by fixing a card filled with symbols before any people or rooms are considered. We will call it **the referee's card**. The next animation shows a genuine small example found and checked by this repository.

![A small referee's card being checked so that every four selected columns show both symbols in some row](referee.gif)

This card has thirteen rows and eight columns, and every entry is one of two symbols. Its promise is simple: choose any four columns, and there is at least one row in which both symbols appear among those four entries. There are seventy ways to choose the four columns, and the tests check all seventy.

At this small size, most randomly filled cards already pass. That does not show that the full construction is easy. At the real sizes, direct checking is impossible. Two counting arguments prove that at least one card works for all column choices at once. The rest of the construction needs only that promise, not a case-by-case search.

The card must be fixed first. If a new rule could be invented after seeing each pair of people, it could always be adjusted to make that one pair work. Such an adjustment would say nothing about any other pair. One card chosen in advance has to handle every future pair, which is what gives the promise its force.

Here is how the card guides a connection. For each candidate colour, a person's team number is written as one symbol in a word. The fixed card produces **the two answer lists**, one for each direction between the two people. More precisely, it gives two fixed rules for producing those lists. For any pair of words, at least one position is guaranteed to contain an agreement between one person's team symbol and the answer produced from the other person's word.

![Two team words and their answer lists being scanned until a guaranteed agreement is found](meeting.gif)

The agreeing position selects a candidate colour. It also selects the receiving team in the way section 9 requires: that team is determined from the sender's word. If the same outsider sends two connections of the same colour into a room, both must therefore land on the same team. The dangerous triangle cannot form.

At the small size, each word contains thirteen two-choice symbols, so there are 8192 possible words. The tests verify the meeting promise for every word on one side and every word on the other. This is a complete check of the toy version.

The toy is drawn small enough to read. The smallest card used by the full construction has 57 rows, and each word has 57 symbols. The rule is the same, but the proof that such a card exists depends on the counting arguments rather than exhaustive checking.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/10.html)** to choose card columns and follow the search for an agreeing position.

---

[← The trap](../09-the-trap/README.md)  ·  [The tower →](../11-the-tower/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

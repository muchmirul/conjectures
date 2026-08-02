# 10 · The referee

Here is the enforcement problem, stripped down. A string runs from person u in one room to person v in another. The rule of chapter 9 says the team it lands on must be determined by the sender, not chosen freely. But the string's color must also be held on exactly one side, per chapter 8, and there are many candidate colors, and this must work for every pair of rooms in the construction simultaneously, using no information beyond the two endpoints themselves.

The solution is a single fixed card of symbols, written down once, before any rooms or people exist. This article calls it the **referee's card**. Here is a real one, at toy size, found and fully verified by this repository.

![The referee's card at toy size, with every choice of four columns containing a row that shows both symbols](referee.gif)

The card's one promise: choose any four of its columns, and some row shows every symbol within those four columns. Thirteen rows of coin flips are enough to make that hold for all seventy ways of picking four columns out of eight, and the tests check all seventy. At this toy size the promise is easy and almost any random card passes; at the sizes the real construction needs, nothing could be checked case by case, and the existence of a valid card is guaranteed instead by two counting arguments layered on top of each other. What matters downstream is only this: the card is fixed once and works for every situation at once.

Why insist that the card come first? Because a rule invented after seeing a particular pair of words could always be bent to fit that pair, and an agreement arranged after the fact guarantees nothing about the next pair. The promise has force precisely because one card, written blind, must serve every pair of rooms on every floor, forever.

From the card come two fixed answer lists, one for each direction of the conversation. Each person's teams, across the relevant colors, spell out a word. When two words meet, the promise of the card guarantees a position where one word agrees with the answer list of the other.

![Two words and the two fixed answer lists, scanned until the guaranteed agreement appears](meeting.gif)

That agreeing position picks the string's color, and it does so in exactly the shape chapter 9 demanded: the landing team at the receiving end is read off from the sender's word. Two red strings from the same outsider therefore land on the same team, always, and the trap never springs. The tests verify the meeting promise exhaustively at toy size: all 8192 possible words on one side, every possible word on the other, no pair escapes.

One honest caveat. The toy is real and fully checked, but its size is chosen for the eye. The real construction's smallest card has 57 rows, and the words are 57 symbols long. Nothing conceptual changes with the size; only the counting arguments do.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/10.html)** and turn the idea over yourself.

---

[← The trap](../09-the-trap/README.md)  ·  [The tower →](../11-the-tower/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

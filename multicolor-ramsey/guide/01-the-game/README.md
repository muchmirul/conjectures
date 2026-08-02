# 1 · The game

Start with a group of people and draw a connection between every pair. Give every connection a colour. Any choice of three people forms a triangle because each pair among them is connected. You lose if all three connections in one of those triangles have the same colour.

We will call this a **one-colour triangle**. A completed colouring with no one-colour triangle will be called **safe**. A group together with a safe colouring is a **safe table**.

![Two colourings of four people, with a one-colour triangle on the left and a safe result on the right](rules.png)

The thick triangle on the left uses one colour on all three sides, so that colouring loses. Four people contain four possible groups of three. On the right, each of those four triangles uses at least two colours, so the colouring is safe.

With two colours, a group of five can be kept safe. Apart from renaming the people or swapping the colours, there is only one way to do it. Place the five people around a circle. Use the first colour for neighbouring pairs around the outside, then use the second colour for the five connections that skip across the circle.

![The ten connections among five people being coloured, followed by a check of all ten triangles](pentagon.gif)

The final sweep checks every possible group of three. There are ten of them, and every one uses both colours. Safety is therefore not based on how the picture looks. It comes from checking a short, complete list. The tests in this repository perform the same check.

There is also a quick way to understand the pattern. Look at either colour by itself. Its five connections form a ring, and a ring contains no triangle. Since neither colour can make a triangle on its own, the combined colouring is safe.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/01.html)** to colour the five-person group and check each triangle.

---

[← Start here](../00-start-here/README.md)  ·  [Six is forced →](../02-six-is-forced/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

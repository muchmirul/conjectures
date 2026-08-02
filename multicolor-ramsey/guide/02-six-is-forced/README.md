# 2 · Six is forced

Five people can be kept safe with two colors. Six cannot. This is the one theorem this article proves completely, and the proof fits in a picture.

Sit six people down, pick one of them, and look at her five strings. Five strings, two colors: some color appears on at least three of them. Say it is red, going to three particular people.

![The pigeonhole proof playing out: three same-colored strings force a triangle either way](pigeonhole.gif)

Now watch those three people. If any two of them are joined by a red string, that string plus their two red strings back to the first person close a red triangle. So all three of their mutual strings must avoid red, which means all three are blue, and that is a blue triangle. A one-color triangle appears in either case.

Nothing about the argument used which coloring was chosen, so every coloring of six people fails. Machines agree: this repository's tests walk through all 32768 ways to two-color the fifteen strings of a six-person group, and not one is safe. The sweep finds a little more than the proof promised.

![The census of all 32768 colorings of six people, counted by how many one-color triangles each contains](census.png)

The bar at zero is empty, which is the theorem. The bar at one is also empty: the luckiest colorings of six contain exactly two one-color triangles, never just one. That refinement is a 1959 observation of Goodman, rediscovered here by brute force.

So the story of two colors is complete: five people can be kept safe and six cannot. Call six the **forcing size** for two colors: the group size at which a one-color triangle becomes unavoidable.

**[Play with this](https://muchmirul.github.io/conjectures/multicolor-ramsey/play/02.html)** and turn the idea over yourself.

---

[← The game](../01-the-game/README.md)  ·  [More crayons →](../03-more-crayons/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

# 9 · The wall

Push the radius in and the demand gets harder. The negative half of the weight does not shrink; it is always exactly half. It just has less room to sit in.

![Shrinking the radius until the demand cannot be met](wall.gif)

The 2026 proof shows there is a wall. Once the radius drops below one over pi, times the square root of the dimension, the amount of weight that can possibly sit inside that ball is exponentially small. Half is not exponentially small. So the radius cannot go there, for any certificate at all.

That is the hard half of the theorem, and it is the half that says the method has a ceiling.

The number pi appears because of the shape of the machinery, not by coincidence. Roughly, the argument moves the problem into a coordinate system where taking the Fourier transform becomes a reflection, works inside a strip, and uses a classical principle that bounds a function inside a region by its values on the edges. That principle assigns each frequency a weight. As the argument is pushed to the decisive edge of the strip, those weights settle into one specific bell shaped curve.

![The weighting used by the argument, and the shape it becomes at the edge](ingredients.png)

That curve is where one over pi comes from. This repository does not implement the argument, but it does check the ingredients: the reflection has size exactly one along the relevant line, the limiting curve is a genuine probability density with the stated frequency profile, and its logarithmic average has the closed form the proof uses.

One detail is worth repeating because it is the kind of thing that decides a constant. The weights do not add up to one. It is tempting to normalise them into a probability, and doing it too early changes the answer.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/09.html)** and turn the idea over yourself.

---

[← The balancing trick](../08-balancing/README.md)  ·  [Building the witness →](../10-the-witness/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

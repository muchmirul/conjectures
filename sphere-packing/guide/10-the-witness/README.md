# 10 · Building the witness

Ruling everything out is only half. Someone still has to produce a certificate that actually reaches the wall.

The natural place to start is a Gaussian, the bell curve, because it is its own Fourier transform. The symmetry the argument needs is free. The trouble is that its radius sits at one over the square root of two pi, which is about 0.399, and the wall is at one over pi, about 0.318. The Gaussian is in the wrong place.

So the construction multiplies it by a carefully chosen even deformation, which moves the radius without disturbing the symmetry.

![The radius sliding from the Gaussian's value down onto the wall](moving_radius.gif)

How far it moves is given by a single integral. An **integral** is an area being gathered up piece by piece, and this one can be watched doing it: the region under the curve fills in from the left, and the jar on the right fills with the total gathered so far. The jar settles on an exact closed value, the logarithm of pi over two. It is an old identity of Wallis.

![The area under the curve being gathered up from the left, and a jar filling to exactly the log of pi over two](wallis.gif)

Put the two together and the Gaussian's 0.399 becomes exactly 0.318. The construction lands on the wall, not near it. That is the second half of the theorem.

Two more pieces are needed to make it work, and both are repairs rather than ideas.

```
    a Gaussian                   already its own Fourier transform,
                                 so the symmetry is free
    an even deformation          slides the radius onto the wall
                                 without breaking that symmetry
    a tiny bump far away         restores the damping the deformation
                                 destroys at huge radii
    a pair of polynomial factors fixes the signs near the origin, where
                                 the estimates say nothing
```

The deformation, left alone, destroys the damping that keeps the function well behaved at enormous radii, so a tiny positive bump is added far away to restore it. And the estimates that control the signs are useless near the origin, so a pair of polynomial factors is included to handle that stretch separately.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/10.html)** and turn the idea over yourself.

---

[← The wall](../09-the-wall/README.md)  ·  [The two halves meet →](../11-they-meet/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

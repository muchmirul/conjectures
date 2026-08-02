# 8 · The balancing trick

Nothing new is needed from here on. The rest of this article uses the two sign rules from section 4, the Fourier transform from the same section, and the idea of a radius. What changes is that we stop asking what a particular certificate proves and start asking what any certificate must look like.

Start with a certificate. Stretch it, like adjusting the zoom on a photograph. Stretching a function makes its transform shrink by the same factor and grow taller, so there is exactly one amount of stretch that makes the function and its transform agree at the centre. Apply that stretch, then subtract one from the other.

![Subtracting the stretched certificate from its own transform](balancing.gif)

Call the result the **balanced function**. Two things are now true about it, and both come for free.

It is zero at the centre, because that is what the stretch was for.

And it turns into minus itself under the Fourier transform. Subtracting swapped the two roles, so taking the transform swaps them back and flips the sign. A function that transforms into minus itself is a rare thing, and it is rigid enough to be attacked.

Here is why that matters. A function that transforms into minus itself has total zero, so exactly half of its weight is negative. And rule one, translated through the subtraction, says the balanced function is never negative beyond a certain radius.

![Half the weight is negative, and all of it is trapped inside one radius](trapped.png)

So the entire negative half is trapped inside one ball. The radius of that ball is the number that decides how good the certificate was: the smaller the radius, the better the certificate. The packing question has turned into a question about how far in you can push a radius.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/08.html)** and turn the idea over yourself.

---

[← Is there a ceiling on the method?](../07-the-ceiling/README.md)  ·  [The wall →](../09-the-wall/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

# 8 · The balancing trick

**The proof of the 2026 result begins here.** This section and the next follow its first half, which rules every certificate out beyond a line. Section 10 follows its second half, which builds a certificate that reaches the line, and section 11 puts the halves together. Alongside the proof, these sections also carry the reasoning walkthrough's account of how each step was found.

The final sections do not require a new starting idea. They reuse the two sign rules and the Fourier transform from section 4, together with the familiar idea of a radius. Until now, we asked what one chosen certificate could prove. We will now ask what every possible certificate is forced to look like.

Begin with any certificate and stretch its graph, as though changing the zoom on a picture. When the original graph becomes wider, its Fourier view becomes narrower and changes height. There is one amount of stretching for which the original function and its Fourier view have the same value at the centre. Make that adjustment, and then subtract the stretched function from its Fourier view.

![A stretched certificate being subtracted from its Fourier view to make a balanced function](balancing.gif)

We will call the result the **balanced function**. The way it was made immediately gives it two useful features.

First, its value at the centre is zero because the two values there were made equal before the subtraction.

Second, taking its Fourier transform changes it into its own negative. The transform swaps the two parts of the subtraction, so their order reverses. This strong symmetry leaves the balanced function much less freedom to change shape.

To see why that helps, look at the area above and below the zero line. Count the area above as positive and the area below as negative. For the balanced function, those two amounts cancel and leave a total of zero, so they must be equal. If all the area is then counted without a sign, exactly half of it lies below zero. The original sign rules also ensure that the balanced function cannot be negative beyond a certain radius.

![The negative half of a balanced function contained inside one marked radius](trapped.png)

All of the negative half must therefore fit inside one ball. The size of this ball records the strength of the original certificate: a smaller radius leads to a stronger density limit. The packing problem has now become a simpler-looking question about how small that radius can be.

**[Play with this](https://muchmirul.github.io/conjectures/sphere-packing/play/08.html)** to stretch the two views until their centre values balance.

---

[← Is there a ceiling on the method?](../07-the-ceiling/README.md)  ·  [The wall →](../09-the-wall/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

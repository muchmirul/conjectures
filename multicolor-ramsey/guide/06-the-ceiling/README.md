# 6 · The ceiling

**The reasoning, continued.** The second classical guardrail, and the reason it grows the way it does.

The argument from section 2 can be extended to any number of colours. Choose one person and sort everyone else into groups according to the colour of their connection to that person.

![The fifteen connections from one person in the sixteen-person group sorting into three colour groups](sort.gif)

The picture uses the safe sixteen-person colouring. The chosen person has fifteen connections, so at least one of the three colour groups contains five people. Inside that group, its sorting colour cannot be used. If two people there were joined in that colour, they would complete a one-colour triangle with the chosen person. The group must therefore survive using only the other two colours, and five is exactly the largest size that can do so.

This also explains why a seventeenth person cannot be added. From one person there would be sixteen connections in three colours, so one colour group would contain at least six people. That group must avoid its sorting colour, leaving only two colours. Section 2 showed that six people cannot survive with two colours.

The same sorting step works again with more colours. Each step removes one available colour and leaves a smaller group. Starting with the one-colour case and working upward gives the forcing sizes 3, 6, 17, 66, 327, and then continues in the same way. These are upper limits: once a group reaches the listed size, the sorting argument guarantees a one-colour triangle.

![The forcing-size staircase compared with factorial growth](staircase.png)

At each step, the size is multiplied by roughly the current number of colours. Repeatedly multiplying by each whole number up to the colour count is called a **factorial**, so this upper limit has factorial growth. The simple staircase gives the exact answers for one, two and three colours. At four colours it gives 66, while stronger work proves the answer is no more than 62.

Later refinements reduce the fixed amount in front of the factorial without changing this overall shape. The best published multiplier is called e minus one sixth, where e is a standard fixed number of about 2.72. No known upper-bound argument has replaced factorial growth with a fundamentally smaller kind of growth.

---

[← Multiply](../05-multiply/README.md)  ·  [The gap →](../07-the-gap/README.md)  ·  [the whole article on one page](../../ARTICLE.md)

# Writing style rules

The repository's house style, copied from the owner's Notion page
"Writing style rules" (fetched 2026-08-13). This file is the reference every
article is revised against, so the rules live in the repository rather than
only in a browser tab.

## The rules, verbatim

Write in a direct, clear, and natural style.

Explain ideas in a smooth order. Each sentence should prepare the reader for
the next sentence. Do not jump between points or present ideas as separate
slogans.

Use simple and familiar words when possible. Keep technical terms only when
they are needed, and explain them clearly when they first appear.

Write for a wide audience. The text should be easy to understand for
beginners and younger readers, while still remaining accurate and respectful.

Prefer connected paragraphs over many short sentences. A paragraph should
usually:

1. Introduce the main idea.
2. Explain how it works.
3. Give an example when useful.
4. Explain why it matters.
5. Connect naturally to the next idea.

Be direct. Remove unnecessary introductions, repeated ideas, dramatic
wording, and decorative language.

Use natural transitions such as:

- "This means that..."
- "For example..."
- "Because of this..."
- "The next step is..."
- "This is important because..."
- "In the same way..."
- "By contrast..."
- "As a result..."

Do not use em dashes. Use commas, periods, parentheses, or separate sentences
instead.

Avoid:

- Short, punchy, slogan-like statements
- Choppy sentence patterns
- Dramatic contrasts
- Clever or poetic wording
- Unnecessary metaphors
- Rhetorical questions
- Informal personification
- Excessive technical language
- Repeated patterns such as "X is not Y. It is Z."
- One-sentence paragraphs unless necessary
- Phrases such as "here is the catch," "quietly changes," "does not
  magically," or "the key idea is simple"

Prefer this:

> "A binary symmetric channel may change a transmitted bit. The receiver
> cannot directly tell whether this happened. A binary erasure channel works
> differently because it marks a bit as missing. This makes the error easier
> to detect, although the original bit still needs to be recovered."

Instead of this:

> "A binary symmetric channel quietly gives the wrong bit. A binary erasure
> channel tells you exactly when a bit went missing."

Before returning the final text, check that:

- The explanation begins directly.
- The ideas appear in a logical order.
- Each sentence connects naturally to the next.
- The wording is simple and accurate.
- The tone sounds natural rather than generated.
- No em dashes are used.
- The text does not sound choppy, dramatic, or overly clever.

## How these interact with the repository's other rules

`CLAUDE.md` carries rules that came out of reader feedback on Hacker News.
Where the two overlap they agree: both forbid the two-beat rhetorical
fragment, both forbid slogans, and both ask for plain declarative sentences
that carry information. The Notion rules go further in two ways that matter
when revising:

The Notion rules ask for **connected paragraphs**, not just plain sentences.
A paragraph should introduce its idea, explain how it works, give an example
where one helps, say why it matters, and lead into what comes next. Much of
the older prose in this repository is built from short standalone
observations instead, and that is the main thing a revision has to repair.

The Notion rules forbid **one-sentence paragraphs unless necessary**. Several
articles use them for emphasis. They should be folded into the paragraph
before or after them unless the sentence genuinely stands alone, such as a
quoted theorem statement.

Nothing in the Notion rules relaxes the accuracy rules. A revision must not
change a number, a citation, a page reference, an attribution, or the
strength of any claim. Where `CLAUDE.md` says a claim must not promise more
than the construction gives, that still binds, and a smoother sentence that
overstates is worse than a choppy one that does not.

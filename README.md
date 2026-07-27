# Conjectures

*Famous math problems, explained from zero, with pictures that move.*

Every topic in this repo is one self-contained folder: its own chapters, its own
animations, its own code, and its own tests. Pick one and start reading.

## Topics

| Topic | What it is about | Read it |
|---|---|---|
| [jacobian-conjecture](jacobian-conjecture/) | A question from 1939 about polynomial machines that can be undone. It stayed open for 87 years and then fell in July 2026. | [chapters](jacobian-conjecture/guide/00-start-here/README.md) · [one page](https://muchmirul.github.io/conjectures/jacobian-conjecture/) |

## How a topic is laid out

```
<topic>/
  README.md   the topic's front page and chapter list
  ARTICLE.md  the whole topic as one continuous page
  guide/      the chapters (each folder: README.md + its images and GIFs)
  src/        the code that generates every figure
  tests/      checks for every mathematical claim the topic makes
  notes/      research notes and sources
```

Two things live at the repository root instead, because they have to:

- `docs/` is what GitHub Pages serves. It holds one subfolder per topic, plus the
  landing page at [docs/index.html](docs/index.html). GitHub Pages can only publish
  from the root or from `/docs`, so the web versions cannot move into their topic folder.
- `.venv/` is one shared virtualenv for all topics.

## Run the code

```bash
make venv    # create the shared .venv and install every topic
make test    # run every topic's tests
make topics  # list the topics
```

Or work inside a single topic:

```bash
cd jacobian-conjecture
make test
make figures
```

## Adding a topic

1. Create the folder, following the layout above.
2. Create `docs/<topic>/` for its web version.
3. Add the topic to `TOPICS` in the root [Makefile](Makefile), to the table above,
   and to the landing page in [docs/index.html](docs/index.html).

## The ethos

Distrust, and verify. The writing is friendly, but the claims are not hand-waved.
Every topic re-checks its own mathematics from scratch, in exact arithmetic, on your
machine, not on anyone's authority.

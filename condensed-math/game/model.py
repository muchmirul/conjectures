"""The pieces a level of the game is built from.

The game is a discovery route, not a lecture, and every brick in it runs in
the same three stages:

    concept      what the idea is, said plainly, before any picture
    intuition    what it feels like, in everyday terms, ending in a guess
    experiment   something the reader runs, which settles the guess, and then
                 the name the literature uses and the mathematics behind it

The order is deliberate and never varies.  Concept first, so the reader knows
what is being talked about and is not asked to infer it from a story.
Intuition second, so the idea attaches to something they already have.
Experiment last, because a guess that has not been tested is not knowledge,
and because a reader who has run the thing themselves does not have to take
the name on trust.

The vocabulary:

* a **beat** is one thing that happens on screen, revealed by one press
* a **brick** is the smallest complete idea: three stages, then what it leaves
  the reader holding
* a **world** is a run of bricks that ends somewhere worth stopping

Everything is plain data.  `build_game.py` turns it into pages, and
`tests/test_game.py` checks the shape of every brick, so a brick that skips a
stage, or forgets its guess, its experiment, its name or its mathematics,
fails there rather than in front of a reader.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- beats: one press of the button each ----------------------------------


@dataclass(frozen=True)
class Say:
    """A paragraph of narration.  No demand on the reader beyond reading."""

    text: str
    kind: str = "say"


@dataclass(frozen=True)
class Ask:
    """A guess, made before the answer exists on screen.

    Every option gets a reply of its own, and no option is called wrong: a
    guess that misses is the most useful thing a reader can produce, because
    the reply can then say exactly which intuition was doing the misleading.
    """

    question: str
    options: tuple[tuple[str, str], ...]
    after: str = ""
    kind: str = "ask"


@dataclass(frozen=True)
class Play:
    """A widget the reader moves, with a thing to watch for while moving."""

    widget: str
    prompt: str
    notice: str
    params: dict = field(default_factory=dict)
    kind: str = "play"


@dataclass(frozen=True)
class Try:
    """An experiment the reader runs off the screen, with pen or in the head.

    Used where a widget would add nothing: the steps are concrete, the reader
    carries them out, and only then asks for the result.  `found` is withheld
    until they say they have done it.
    """

    steps: tuple[str, ...]
    found: str
    prompt: str = "Do this before reading on."
    kind: str = "try"


@dataclass(frozen=True)
class Name:
    """The moment a plain word is swapped for the word the literature uses."""

    plain: str
    standard: str
    notation: str
    why: str = ""
    kind: str = "name"


@dataclass(frozen=True)
class Math:
    """The symbols, and how to read them out loud.

    `statement` is a short line of notation as HTML, since the game pages
    carry no library and no network.  `reading` walks the symbols one at a
    time.  `cite` and `url` point at the numbered result in the lectures when
    there is one.
    """

    statement: str
    reading: str
    cite: str = ""
    url: str = ""
    kind: str = "math"


BEATS = (Say, Ask, Play, Try, Name, Math)


# --- bricks and worlds -----------------------------------------------------


STAGES = (
    ("concept", "Concept", "what the idea is"),
    ("intuition", "Intuition", "what it feels like"),
    ("experiment", "Experiment", "run it yourself"),
)


@dataclass(frozen=True)
class Brick:
    """One idea, from nothing to named, in three stages.

    `idea` states the concept in a single sentence, before anything else
    happens, so a reader always knows what the next few minutes are about.

    `need` is the preliminary: what a reader must already hold to follow this
    brick, said in plain words and assuming no schooling.  Nothing may appear
    in a `need` that an earlier brick did not build.

    `hold` is the single line the reader carries out of the brick.
    """

    slug: str
    title: str
    idea: str
    need: tuple[str, ...]
    concept: tuple
    intuition: tuple
    experiment: tuple
    hold: str

    @property
    def stages(self) -> tuple[tuple[str, str, str, tuple], ...]:
        return tuple((key, label, blurb, getattr(self, key))
                     for key, label, blurb in STAGES)

    @property
    def beats(self) -> tuple:
        return self.concept + self.intuition + self.experiment


@dataclass(frozen=True)
class World:
    number: int
    slug: str
    title: str
    promise: str
    bricks: tuple[Brick, ...]

    @property
    def page(self) -> str:
        return f"{self.number:02d}.html"


def brick_of(world: World, slug: str) -> Brick:
    for brick in world.bricks:
        if brick.slug == slug:
            return brick
    raise KeyError(slug)

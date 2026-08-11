"""Split ARTICLE.md into the per-chapter READMEs under guide/.

    cd zeta-critical-line && make guide   (or: ../.venv/bin/python build_guide.py)

ARTICLE.md is the single source for the prose; the chapter files are
generated.  Keeping the same prose in two hand-written places has already
gone wrong once in this repository, so this topic never does it.

Every chapter folder already exists, because the figure scripts write into it.
This only adds the README.md, with image paths rewritten to sit beside the text
and with links to the neighbouring chapters.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARTICLE = ROOT / "ARTICLE.md"
GUIDE = ROOT / "guide"

#: section number in ARTICLE.md -> chapter folder, in reading order
CHAPTERS = {
    0: ("00-start-here", "Start here"),
    1: ("01-the-primes", "The primes"),
    2: ("02-riemanns-map", "Riemann's map"),
    3: ("03-the-music", "The music of the primes"),
    4: ("04-the-question", "The question"),
    5: ("05-four-counts", "Four ways to count"),
    6: ("06-the-microphones", "The microphones"),
    7: ("07-bowls-and-saddles", "Bowls and saddles"),
    8: ("08-the-prime-side", "What the primes reveal"),
    9: ("09-the-whole-number-trick", "The whole-number trick"),
    10: ("10-two-thirds", "Two thirds"),
    11: ("11-the-checks", "The checks"),
    12: ("12-what-it-means", "Where things stand"),
}


def split_sections(md: str) -> dict[int, tuple[str, str]]:
    """ARTICLE.md as {number: (title, body)}, with 0 being everything above §1."""
    lines = md.splitlines()
    head_at = next(i for i, l in enumerate(lines) if re.match(r"^## \d+ · ", l))
    out = {0: ("Start here", "\n".join(lines[1:head_at]).strip())}

    starts = [i for i, l in enumerate(lines) if re.match(r"^## \d+ · ", l)]
    tail = next((i for i, l in enumerate(lines)
                 if l.startswith("## ") and not re.match(r"^## \d+ · ", l)
                 and i > starts[0]), len(lines))
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else tail
        m = re.match(r"^## (\d+) · (.*)$", lines[start])
        out[int(m.group(1))] = (m.group(2),
                                "\n".join(lines[start + 1:end]).strip())
    return out


def localise(body: str, folder: str) -> str:
    """Point every image at the copy sitting next to this README."""
    return re.sub(r"\((?:guide/)([0-9a-z-]+)/([^)]+)\)",
                  lambda m: f"({m.group(2)})" if m.group(1) == folder
                  else f"(../{m.group(1)}/{m.group(2)})", body)


def main() -> None:
    sections = split_sections(ARTICLE.read_text())
    numbers = sorted(CHAPTERS)
    for n in numbers:
        folder, title = CHAPTERS[n]
        _, body = sections[n]
        target = GUIDE / folder
        target.mkdir(parents=True, exist_ok=True)

        heading = title if n == 0 else f"{n} · {title}"
        parts = [f"# {heading}", "", localise(body, folder), ""]

        nav = []
        if n > 0:
            prev_folder, prev_title = CHAPTERS[numbers[numbers.index(n) - 1]]
            nav.append(f"[← {prev_title}](../{prev_folder}/README.md)")
        if n < numbers[-1]:
            next_folder, next_title = CHAPTERS[numbers[numbers.index(n) + 1]]
            nav.append(f"[{next_title} →](../{next_folder}/README.md)")
        nav.append("[the whole article on one page](../../ARTICLE.md)")
        parts += ["---", "", "  ·  ".join(nav), ""]

        (target / "README.md").write_text("\n".join(parts))
    print(f"wrote {len(numbers)} chapter READMEs under {GUIDE}")


if __name__ == "__main__":
    main()

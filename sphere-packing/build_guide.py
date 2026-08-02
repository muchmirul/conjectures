"""Split ARTICLE.md into the per-chapter READMEs under guide/.

    cd sphere-packing && make guide      (or: ../.venv/bin/python build_guide.py)

The two existing topics in this repository keep the same prose in ARTICLE.md
and in each guide/NN-.../README.md, written out by hand twice.  That has already
gone wrong once here: the published Kakeya page and its ARTICLE.md drifted 91
lines apart.  This script removes the possibility by making the chapter files
generated, with ARTICLE.md the single source.

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
    1: ("01-the-question", "The question"),
    2: ("02-room-runs-out", "The room runs out"),
    3: ("03-cannot-check", "Why you cannot just check"),
    4: ("04-the-certificate", "The certificate"),
    5: ("05-count-twice", "Counting twice"),
    6: ("06-best-so-far", "What certificates actually prove"),
    7: ("07-the-ceiling", "Is there a ceiling on the method?"),
    8: ("08-balancing", "The balancing trick"),
    9: ("09-the-wall", "The wall"),
    10: ("10-the-witness", "Building the witness"),
    11: ("11-they-meet", "The two halves meet"),
    12: ("12-what-it-means", "What it means, and what it does not"),
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

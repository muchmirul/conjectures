"""Split each part's ARTICLE.md into the per-chapter READMEs under guide/.

    cd condensed-math && make guide

Each part has one ARTICLE.md, and that file is the single source for its
prose.  The chapter READMEs are generated from it, with image paths rewritten
to sit beside the text and with links to the neighbouring chapters.  Keeping
the same prose in two hand-written places has already gone wrong once in this
repository, so this topic never does it.
"""

from __future__ import annotations

import re

from condensed_guide.parts import PARTS, Part


def split_sections(md: str) -> dict[int, tuple[str, str]]:
    """ARTICLE.md as {number: (title, body)}, with 0 being everything above §1."""
    lines = md.splitlines()
    starts = [i for i, l in enumerate(lines) if re.match(r"^## \d+ · ", l)]
    out = {0: ("Start here", "\n".join(lines[1:starts[0]]).strip())}

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


def build_part(part: Part) -> int:
    sections = split_sections(part.article.read_text())
    numbers = sorted(part.chapters)
    for n in numbers:
        folder, title = part.chapters[n]
        _, body = sections[n]
        target = part.guide / folder
        target.mkdir(parents=True, exist_ok=True)

        heading = title if n == 0 else f"{n} · {title}"
        parts_ = [f"# {heading}", "",
                  f"*Part {part.number} of three: {part.title}. "
                  f"Retells {part.lectures} of Scholze's "
                  f"[Lectures on Condensed Mathematics]"
                  f"(https://arxiv.org/abs/2605.03658).*", "",
                  localise(body, folder), ""]

        nav = []
        if n > 0:
            prev_folder, prev_title = part.chapters[numbers[numbers.index(n) - 1]]
            nav.append(f"[← {prev_title}](../{prev_folder}/README.md)")
        if n < numbers[-1]:
            next_folder, next_title = part.chapters[numbers[numbers.index(n) + 1]]
            nav.append(f"[{next_title} →](../{next_folder}/README.md)")
        nav.append(f"[all of part {part.number} on one page](../../ARTICLE.md)")
        parts_ += ["---", "", "  ·  ".join(nav), ""]

        (target / "README.md").write_text("\n".join(parts_))
    return len(numbers)


def main() -> None:
    total = 0
    for part in PARTS:
        n = build_part(part)
        total += n
        print(f"  {part.slug}: {n} chapter READMEs")
    print(f"wrote {total} chapter READMEs across {len(PARTS)} parts")


if __name__ == "__main__":
    main()

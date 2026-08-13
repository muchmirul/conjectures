"""Prove that a style revision moved prose and nothing else.

    python notes/style_check.py skeleton <article.md>        # print the skeleton
    python notes/style_check.py compare <before> <after>     # diff the skeletons
    python notes/style_check.py rules <article.md>           # check the style rules

The articles carry a lot that a style revision must not touch: image paths,
figure alt text, links to numbered results, fenced diagrams, table rows, the
exact heading text the tests look for.  The "skeleton" is all of that.  If the
skeleton is unchanged, the revision only rewrote prose.

`rules` checks the mechanical parts of `notes/writing-style.md`: no em dashes,
no one-sentence paragraphs beyond the few that are allowed to stand alone, and
none of the phrasings the rules name outright.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# --- the skeleton -----------------------------------------------------------

STRUCTURAL = (
    re.compile(r"^#{1,6} "),          # every heading, with its exact text
    re.compile(r"^!\["),              # every image: path and alt text
    re.compile(r"^\|"),               # every table row
    re.compile(r"^```"),              # every fence marker
    re.compile(r"^\s*$"),             # blank lines, so block shape is kept
)


def skeleton(text: str) -> list[str]:
    """The lines a style revision is not allowed to change."""
    out, in_fence = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)          # fenced diagrams and commands are data
            continue
        if any(p.match(line) for p in STRUCTURAL[:3]):
            out.append(line)
        # every link target must survive, wherever it sits in a paragraph
        for m in re.finditer(r"\]\(([^)]+)\)", line):
            out.append(f"link {m.group(1)}")
    return out


# --- the mechanical style rules --------------------------------------------

BANNED_PHRASES = [
    "here is the catch", "quietly changes", "does not magically",
    "the key idea is simple", "here is the thing", "that is the whole trick",
    "it is the whole", "here is what", "the trick is simple",
]

#: paragraphs that are allowed to be a single sentence
ALLOWED_SINGLE = (
    re.compile(r"^\*\*\[Play with this\]"),      # the activity pointer
    re.compile(r"^> "),                          # a quoted statement
    re.compile(r"^\*[^*]"),                      # the italic subtitle
    re.compile(r"^!\["),                         # an image
    re.compile(r"^[-|#]"),                       # lists, tables, headings
    re.compile(r"^\*\*\[Part "),                 # the pointer to the next part
    re.compile(r"^\["),                          # a chapter's navigation footer
    re.compile(r"^<"),                           # raw html, used for anchors
    re.compile(r"^\0subtitle"),                  # the line under the title
    re.compile(r"^\*\*[^*]+:?\*\*\s*\["),          # a bold pointer to a page
    re.compile(r"^\*\*\["),                       # a bold link on its own
    re.compile(r"^\*\*[^*]*\[[^\]]*\]\([^)]*\)\*\*$"),  # a bold pointer line
)


def paragraphs(text: str) -> list[tuple[int, str]]:
    """Prose paragraphs, as (line number, text), fences excluded.

    The paragraph directly under the document's title is its subtitle, and a
    subtitle is a single sentence by design, so it is reported with a marker
    the callers use to let it through.
    """
    out, buf, start, in_fence = [], [], 0, False
    after_title = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("# "):
            after_title = True
            continue
        if line.startswith("    ") and not buf:
            continue          # an indented block is code, not a paragraph
        if line.strip():
            if not buf:
                start = i
            buf.append(line.strip())
        elif buf:
            out.append((start, ("\0subtitle" if after_title else "")
                        + " ".join(buf)))
            after_title = False
            buf = []
    if buf:
        out.append((start, ("\0subtitle" if after_title else "")
                    + " ".join(buf)))
    return out


def count_sentences(para: str) -> int:
    """Roughly how many sentences a paragraph holds.

    Abbreviations with a full stop would each read as a sentence break, so the
    few this repository uses are masked out before counting.
    """
    masked = para
    for abbr in ("e.g.", "i.e.", "cf.", "Mr.", "Dr.", "vs.", "St.", "No."):
        masked = masked.replace(abbr, abbr.replace(".", ""))
    masked = re.sub(r"\[[^\]]*\]\([^)]*\)", "LINK", masked)   # links hold dots
    masked = re.sub(r"\b\d+\.\d+", "N", masked)               # so do numbers
    masked = re.sub(r"([.!?])([*_`]+)", r"\2\1 ", masked)   # "**done.**"
    return len([s for s in re.split(r"[.!?]+(?:\s|$)", masked) if s.strip()])


def check_rules(path: Path) -> list[str]:
    text = path.read_text()
    problems = []

    for i, line in enumerate(text.splitlines(), 1):
        if "—" in line:
            problems.append(f"{path}:{i}: em dash")
        low = line.lower()
        for phrase in BANNED_PHRASES:
            if phrase in low:
                problems.append(f"{path}:{i}: banned phrasing {phrase!r}")

    for start, para in paragraphs(text):
        if any(p.match(para) for p in ALLOWED_SINGLE):
            continue
        para = para.replace("\0subtitle", "")
        if para.rstrip().endswith(":"):
            continue                  # a lead-in to a list has to be a fragment
        if count_sentences(para) == 1 and len(para.split()) > 4:
            problems.append(f"{path}:{start}: one-sentence paragraph: "
                            f"{para[:70]}...")

    # A rhetorical question is one asked in the prose. A section heading that
    # is phrased as a question is a title, and a quoted statement may ask
    # whatever the source asked, so neither counts.
    for start, para in paragraphs(text):
        if any(p.match(para) for p in ALLOWED_SINGLE):
            continue
        para = para.replace("\0subtitle", "")
        if para.startswith((">", "|", "#", "[", "<")):
            continue          # quotes, tables, headings, links, raw html
        # a question inside quotation marks is quoted speech, not the text
        # asking the reader something
        para = re.sub(r'"[^"]*"', "Q", para)
        para = re.sub(r"\*[^*]*\*", "Q", para)
        if re.match(r"^\d+\. ", para) or para.startswith("- "):
            continue          # a labelled question in a list is a label
        if "?" in para:
            problems.append(f"{path}:{start}: question mark: {para[:70]}...")

    return problems


def main() -> int:
    mode = sys.argv[1]
    if mode == "skeleton":
        print("\n".join(skeleton(Path(sys.argv[2]).read_text())))
        return 0
    if mode == "compare":
        a = skeleton(Path(sys.argv[2]).read_text())
        b = skeleton(Path(sys.argv[3]).read_text())
        if a == b:
            print("skeleton unchanged: the revision moved prose only")
            return 0
        import difflib
        print("SKELETON CHANGED, the revision moved more than prose:")
        for line in difflib.unified_diff(a, b, "before", "after", lineterm=""):
            print(" ", line)
        return 1
    if mode == "rules":
        problems = []
        for arg in sys.argv[2:]:
            problems += check_rules(Path(arg))
        for p in problems:
            print(p)
        print(f"{len(problems)} problem(s)")
        return 1 if problems else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

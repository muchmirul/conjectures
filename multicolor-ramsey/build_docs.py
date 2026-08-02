"""Build the web version of this topic's article from ARTICLE.md.

    cd multicolor-ramsey && make docs        (or: ../.venv/bin/python build_docs.py)

Writes ../docs/multicolor-ramsey/index.html, the polished one-page version:
MathJax for the mathematics, article typography, and every animation playing.
The page lives in the repository's root docs/ folder, one subfolder per topic,
because GitHub Pages can only publish from the root or from /docs.

ARTICLE.md is the single source of truth; nothing here is written by hand
twice.  The Markdown subset understood is exactly the one the article uses:
headings, paragraphs, images, tables, block quotes, ordered lists, fenced code,
```math blocks, and inline $math$.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

TOPIC = "multicolor-ramsey"
ROOT = Path(__file__).resolve().parent
ARTICLE = ROOT / "ARTICLE.md"
OUT = ROOT.parent / "docs" / TOPIC / "index.html"
RAW = f"https://raw.githubusercontent.com/muchmirul/conjectures/main/{TOPIC}/"
REPO = f"https://github.com/muchmirul/conjectures/tree/main/{TOPIC}"


# --- a very small Markdown reader ------------------------------------------

def inline(text: str) -> str:
    """Bold, italics, links and inline math, for one line of prose."""
    parts, out, last = [], [], 0
    for m in re.finditer(r"\$([^$]+)\$", text):
        parts.append((m.start(), m.end(), f"${html.escape(m.group(1))}$"))
    for start, end, rendered in parts:
        out.append(html.escape(text[last:start]))
        out.append(rendered)
        last = end
    out.append(html.escape(text[last:]))
    s = "".join(out)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    # the one tag the article is allowed to carry: a hard line break inside a
    # quoted statement, which plain Markdown has no way to express
    return s.replace("&lt;br&gt;", "<br>")


def parse(md: str) -> list[tuple]:
    """ARTICLE.md as a list of (kind, payload) blocks."""
    blocks, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            lang = line[3:].strip()
            body, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            blocks.append(("math" if lang == "math" else "code",
                           ("\n".join(body), lang)))
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            blocks.append((f"h{level}", line[level:].strip()))
            i += 1
        elif line.startswith("!["):
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            blocks.append(("image", (m.group(1), m.group(2))))
            i += 1
        elif line.startswith("|"):
            rows, i = [], i
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            blocks.append(("table", rows))
        elif line.startswith(">"):
            body = []
            while i < len(lines) and lines[i].startswith(">"):
                body.append(lines[i].lstrip("> ").rstrip())
                i += 1
            blocks.append(("quote", " ".join(body)))
        elif re.match(r"^\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]))
                i += 1
            blocks.append(("ol", items))
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            blocks.append(("ul", items))
        else:
            body = []
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(#|!\[|\||>|```|- |\d+\. )", lines[i]):
                body.append(lines[i].strip())
                i += 1
            blocks.append(("p", " ".join(body)))
    return blocks


# --- the renderer -----------------------------------------------------------

def render_html(blocks) -> str:
    out, n = [], 0
    sections = []
    for kind, payload in blocks:
        if kind == "h1":
            out.append(f'<header class="hero"><h1>{inline(payload)}</h1>')
        elif kind == "h2":
            n += 1
            sections.append((f"s{n}", payload))
            if "·" in payload:                    # "5 · The Perron tree"
                num, _, rest = payload.partition("·")
                out.append(f'<h2 id="s{n}"><span class="n">{num.strip()} ·</span> '
                           f"{inline(rest.strip())}</h2>")
            else:                                 # an unnumbered closing section
                out.append(f'<h2 id="s{n}">{inline(payload)}</h2>')
        elif kind == "h3":
            out.append(f"<h3>{inline(payload)}</h3>")
        elif kind == "p":
            if payload.startswith("*") and payload.endswith("*") and out:
                out.append(f'<p class="subtitle">{inline(payload.strip("*"))}</p></header>')
            else:
                out.append(f"<p>{inline(payload)}</p>")
        elif kind == "image":
            alt, src = payload
            # The published page can only reach the figures through GitHub raw:
            # guide/ lives in the topic folder, outside the site root.  Opened
            # from disk instead, the file next to this script is the one that
            # works, so the loader at the bottom of the page tries that second.
            # No lazy loading: a GIF that has not started when the reader
            # arrives looks like a broken one.
            candidates = ";".join([f"{RAW}{src}", f"../../{TOPIC}/{src}"])
            out.append(f'<figure><img src="{RAW}{src}" alt="{html.escape(alt)}" '
                       f'data-fallbacks="{html.escape(candidates)}">'
                       f"<figcaption>{html.escape(alt)}</figcaption></figure>")
        elif kind == "quote":
            out.append(f"<blockquote><p>{inline(payload)}</p></blockquote>")
        elif kind in ("ol", "ul"):
            items = "".join(f"<li>{inline(t)}</li>" for t in payload)
            out.append(f"<{kind}>{items}</{kind}>")
        elif kind == "table":
            head, *body = [r for r in payload if not set("-: ") >= set("".join(r))]
            cells = "".join(f"<th>{inline(c)}</th>" for c in head)
            rows = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>"
                                            for c in r) + "</tr>" for r in body)
            # a table of sentences reads badly centred, while a table of
            # numbers reads badly ragged, so the cells decide the alignment
            longest = max((len(c) for r in body for c in r), default=0)
            cls = ' class="words"' if longest > 25 else ""
            out.append(f'<div class="scroll"><table{cls}><thead><tr>{cells}</tr>'
                       f"</thead><tbody>{rows}</tbody></table></div>")
        elif kind == "math":
            out.append(f"$$ {payload[0]} $$")
        elif kind == "code":
            out.append(f"<pre><code>{html.escape(payload[0])}</code></pre>")

    body = "\n".join(out)
    # a map of the road, dropped in just before the first section
    links = "".join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in sections)
    nav = f'<nav class="toc">{links}</nav>'
    body = embed_simulations(body)
    first = body.find("<h2 ")
    body = body[:first] + nav + "\n" + body[first:] if first != -1 else body + nav
    return TEMPLATE.replace("BODY", body)


PLAY_URL = re.compile(
    r'<p><strong><a href="[^"]*play/(\d\d)\.html">Play with this</a></strong>'
    r'[^<]*</p>')


def embed_simulations(body: str) -> str:
    """Put each chapter's simulation into the page, not just a link to it.

    The article is where the reader already is, so the thing they are being
    told about should be movable without leaving.  Each play page is served
    from the same folder, so it can be framed directly; `?embed` tells it to
    drop its own heading and navigation, which the article already provides.
    The link underneath stays, because a full page is better on a phone and
    because a frame is not something you can bookmark.
    """
    def one(m):
        n = m.group(1)
        return (f'<figure class="sim">'
                f'<iframe src="play/{n}.html?embed" loading="lazy"'
                f' title="Interactive picture for chapter {int(n)}"></iframe>'
                f'<figcaption>Use the controls to change the picture. '
                f'<a href="play/{n}.html">Open the activity on its own page</a>'
                f'</figcaption></figure>')
    body = PLAY_URL.sub(one, body)
    # any remaining link to a play page becomes relative, so the built page
    # also works from a local folder and not only from the published site
    return body.replace(
        "https://muchmirul.github.io/conjectures/multicolor-ramsey/play/", "play/")


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Triangle Game, from Zero</title>
<meta name="description" content="A beginner-friendly visual guide to a colouring game with people and coloured connections, and the 2026 proof that its long-term score grows without limit.">
<script>
MathJax = {
  tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
         displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] },
  chtml: { scale: 1.0 }
};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
  :root {
    --surface: #fcfcfb; --ink: #0b0b0b; --ink2: #52514e; --muted: #898781;
    --line: #e1e0d9; --blue: #2a78d6; --green: #008300; --red: #d03b3b;
    --violet: #4a3aa7; --card: #ffffff;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--surface); color: var(--ink);
    font: 17px/1.65 -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }
  main { max-width: 760px; margin: 0 auto; padding: 3rem 1.25rem 5rem; }
  header.hero { text-align: center; margin-bottom: 2.5rem; }
  h1 { font-size: 2.1rem; line-height: 1.2; margin: 0 0 0.75rem; }
  .subtitle { color: var(--ink2); font-style: italic; font-size: 1.05rem; max-width: 40rem; margin: 0 auto; }
  h2 { font-size: 1.5rem; margin: 3.2rem 0 1rem; padding-top: 1.6rem; border-top: 1px solid var(--line); }
  h2 .n { color: var(--blue); }
  p { margin: 0.9rem 0; }
  figure { margin: 1.6rem 0; text-align: center; }
  figure img { max-width: 100%; height: auto; border-radius: 6px; }
  figcaption { color: var(--muted); font-size: 0.85rem; margin-top: 0.45rem; line-height: 1.45; }
  blockquote {
    margin: 1.4rem 0; padding: 0.85rem 1.1rem; border-left: 4px solid var(--green);
    background: var(--card); border-radius: 0 6px 6px 0; color: var(--ink);
  }
  blockquote p { margin: 0.35rem 0; }
  code, pre { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.9em; }
  code { background: #f0efec; padding: 0.1em 0.35em; border-radius: 4px; }
  pre {
    background: #f6f5f2; border: 1px solid var(--line); border-radius: 8px;
    padding: 0.9rem 1.1rem; overflow-x: auto; line-height: 1.5;
  }
  pre code { background: none; padding: 0; }
  .scroll { overflow-x: auto; }
  table { border-collapse: collapse; margin: 1.2rem auto; }
  th, td { border: 1px solid var(--line); padding: 0.45rem 0.8rem; text-align: center; }
  table.words th, table.words td { text-align: left; }
  th { background: #f6f5f2; }
  ul, ol { padding-left: 1.4rem; }
  li { margin: 0.35rem 0; }
  a { color: var(--blue); text-decoration: none; }
  a:hover { text-decoration: underline; }
  footer { margin-top: 4rem; padding-top: 1.4rem; border-top: 1px solid var(--line);
           color: var(--muted); font-size: 0.9rem; }
  nav.toc {
    background: var(--card); border: 1px solid var(--line); border-radius: 10px;
    padding: 1rem 1.3rem; margin: 2rem 0; font-size: 0.95rem;
    columns: 2; column-gap: 2rem;
  }
  nav.toc a { display: block; padding: 0.12rem 0; color: var(--ink2); }
  nav.toc a:hover { color: var(--blue); }
  h3 { font-size: 1.15rem; margin: 2rem 0 0.6rem; color: var(--ink); }
  figure img.missing { outline: 2px dashed var(--red); padding: 1rem; }
  p.source { text-align: center; font-size: 0.85rem; margin: 0 0 1.4rem; }
  p.source a { color: var(--muted); }
  p.source a:hover { color: var(--blue); }
  figure.sim iframe { width: 100%; height: 650px; border: 1px solid var(--line);
                      border-radius: 10px; background: #fff; }
  @media (max-width: 600px) { nav.toc { columns: 1; } h1 { font-size: 1.7rem; } }
</style>
</head>
<body>
<main>

<p class="source"><a href="https://github.com/muchmirul/conjectures">source: github.com/muchmirul/conjectures</a></p>

BODY

<footer>
<p>Written August 2026. This is one topic in <a href="../">conjectures</a>. Every figure
is generated from the <a href="REPO">repository</a>: <code>make figures</code> rebuilds
the pictures, and <code>make test</code> checks the calculated numbers and small
examples used in the guide.</p>
<p>This article was written with AI assistance and careful human review. Its claims
are backed by the repository's test suite where computation can reach them, and are
quoted from the cited sources where it cannot.</p>
</footer>
</main>
<script>
// Every figure lists the places it might live: GitHub raw, which is the only
// one the published page can reach, and then the topic folder beside this file,
// which is the one that works when the page is opened straight from disk.  Try
// them in order rather than giving up on the first miss, so an animation never
// silently fails to appear.
document.querySelectorAll('figure img[data-fallbacks]').forEach(function (img) {
  var tries = img.getAttribute('data-fallbacks').split(';');
  var at = 0;
  function next() {
    at += 1;
    if (at < tries.length) { img.src = tries[at]; }
    else { img.classList.add('missing'); img.alt = 'could not load: ' + img.alt; }
  }
  img.addEventListener('error', next);
  if (img.complete && img.naturalWidth === 0) { next(); }
});
</script>
</body>
</html>
"""


def main():
    blocks = parse(ARTICLE.read_text())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_html(blocks).replace("REPO", REPO))
    print(f"wrote {OUT.relative_to(ROOT.parent)} from {TOPIC}/{ARTICLE.name}")


if __name__ == "__main__":
    main()

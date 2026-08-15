"""Build the web version of each part from its ARTICLE.md, plus a landing page.

    cd condensed-math && make docs

Writes, under the repository's root docs/ folder:

    docs/condensed-math/index.html                     the three parts
    docs/condensed-math/condensed-math01/index.html    part one
    docs/condensed-math/condensed-math02/index.html    part two
    docs/condensed-math/condensed-math03/index.html    part three

Each part's ARTICLE.md is the single source of truth; nothing here is written
by hand twice. The Markdown subset understood is exactly the one the articles
use: headings, paragraphs, images, tables, block quotes, lists, fenced code,
and fenced mathematics. MathJax renders each cited definition or theorem,
which remains paired with a plain reading and its interactive example.
"""

from __future__ import annotations

import html
import re

from condensed_guide.parts import DOCS, PARTS, SITE, Part

REPO = "https://github.com/muchmirul/conjectures/tree/main/condensed-math"


# --- a very small Markdown reader ------------------------------------------

def inline(text: str) -> str:
    """Bold, italics, code, links and inline maths, for one line of prose.

    Maths is escaped but otherwise passed through untouched, so that MathJax
    sees it rather than the Markdown rules: a subscript underscore must not
    be read as emphasis, and a backslash must survive.
    """
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
                           "\n".join(body)))
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            blocks.append((f"h{level}", line[level:].strip()))
            i += 1
        elif line.startswith("!["):
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            blocks.append(("image", (m.group(1), m.group(2))))
            i += 1
        elif line.startswith("|"):
            rows = []
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

def is_italic(text: str) -> bool:
    """Italic, meaning one asterisk each side, not two.

    The hero's subtitle is the article's opening italic line.  A paragraph
    that is entirely bold also begins and ends with an asterisk, and the
    closing line of parts one and two is exactly that, so the two have to be
    told apart or the header is closed in the wrong place.
    """
    return (text.startswith("*") and text.endswith("*")
            and not text.startswith("**"))


#: the heading that opens a chapter's paired block.  Everything from it to
#: the end of the chapter is the formal statement, the plain-words reading of
#: it, and the simulation that moves it, and the three are boxed together.
PAIR_HEADING = "The mathematics"


def render_html(blocks, part: Part) -> str:
    out, n, sections = [], 0, []
    hero_open = False
    pair_open = False

    def close_pair():
        nonlocal pair_open
        if pair_open:
            out.append("</section>")
            pair_open = False

    for kind, payload in blocks:
        if kind == "h1":
            hero_open = True
            out.append(f'<header class="hero">'
                       f'<p class="kicker">Condensed mathematics, part '
                       f'{part.number} of 3</p><h1>{inline(payload)}</h1>')
        elif kind == "h2":
            close_pair()
            n += 1
            sections.append((f"s{n}", payload))
            if "·" in payload:
                num, _, rest = payload.partition("·")
                out.append(f'<h2 id="s{n}"><span class="n">{num.strip()} ·</span> '
                           f"{inline(rest.strip())}</h2>")
            else:
                out.append(f'<h2 id="s{n}">{inline(payload)}</h2>')
        elif kind == "h3":
            if payload.strip() == PAIR_HEADING:
                close_pair()
                out.append('<section class="mathpair">')
                pair_open = True
            out.append(f"<h3>{inline(payload)}</h3>")
        elif kind == "p":
            if hero_open and is_italic(payload):
                hero_open = False
                out.append(f'<p class="subtitle">'
                           f'{inline(payload.strip("*"))}</p></header>')
            else:
                out.append(f"<p>{inline(payload)}</p>")
        elif kind == "image":
            alt, src = payload
            # The published page can only reach the figures through GitHub
            # raw: guide/ lives in the topic folder, outside the site root.
            # Opened from disk instead, the topic folder beside this file is
            # the one that works, so the loader at the bottom tries that
            # second.  No lazy loading: a GIF that has not started when the
            # reader arrives looks like a broken one.
            local = f"../../../condensed-math/parts/{part.slug}/{src}"
            candidates = ";".join([f"{part.raw}{src}", local])
            out.append(f'<figure><img src="{part.raw}{src}" '
                       f'alt="{html.escape(alt)}" '
                       f'data-fallbacks="{html.escape(candidates)}">'
                       f"<figcaption>{html.escape(alt)}</figcaption></figure>")
        elif kind == "quote":
            out.append(f"<blockquote><p>{inline(payload)}</p></blockquote>")
        elif kind in ("ol", "ul"):
            items = "".join(f"<li>{inline(t)}</li>" for t in payload)
            out.append(f"<{kind}>{items}</{kind}>")
        elif kind == "table":
            head, *body = [r for r in payload
                           if not set("-: ") >= set("".join(r))]
            cells = "".join(f"<th>{inline(c)}</th>" for c in head)
            rows = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>"
                                            for c in r) + "</tr>" for r in body)
            longest = max((len(c) for r in body for c in r), default=0)
            cls = ' class="words"' if longest > 25 else ""
            out.append(f'<div class="scroll"><table{cls}><thead><tr>{cells}</tr>'
                       f"</thead><tbody>{rows}</tbody></table></div>")
        elif kind == "math":
            # TeX comparisons such as q<p are text to MathJax, not HTML tags.
            out.append(f'<div class="eq">$$ {html.escape(payload)} $$</div>')
        elif kind == "code":
            out.append(f"<pre><code>{html.escape(payload)}</code></pre>")

    close_pair()                  # in case an article ends inside a pair
    body = "\n".join(out)
    links = "".join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in sections)
    nav = f'<nav class="toc">{links}</nav>'
    body = embed_simulations(body, part)
    body = link_sibling_parts(body)
    first = body.find("<h2 ")
    body = body[:first] + parts_strip(part) + nav + "\n" + body[first:] \
        if first != -1 else body + nav
    return (TEMPLATE
            .replace("TITLEHERE", html.escape(part.title))
            .replace("DESCHERE", html.escape(part.blurb))
            .replace("REPOHERE", REPO)
            .replace("BODY", body))


def parts_strip(part: Part) -> str:
    """A row of links to the three parts, so a reader can move between them."""
    cells = []
    for p in PARTS:
        cls = ' class="here"' if p.slug == part.slug else ""
        href = "index.html" if p.slug == part.slug else f"../{p.slug}/index.html"
        cells.append(f'<a href="{href}"{cls}>'
                     f'<span class="pn">Part {p.number}</span>'
                     f'<span class="pt">{html.escape(p.title)}</span></a>')
    return f'<nav class="parts">{"".join(cells)}</nav>'


PLAY_URL = re.compile(
    r'<p><strong><a href="[^"]*play/(\d\d)\.html">Play with this</a></strong>'
    r'[^<]*</p>')


def embed_simulations(body: str, part: Part) -> str:
    """Put each chapter's simulation into the page, not just a link to it.

    The article is where the reader already is, so the thing they are being
    told about should be movable without leaving.  Each play page is served
    from the same folder, so it can be framed directly; `?embed` tells it to
    drop its own heading and navigation, which the article already provides.
    The link underneath stays, because a full page is better on a phone and
    because a frame is not something you can bookmark.
    """
    def one(m):
        k = m.group(1)
        return (f'<figure class="sim">'
                f'<iframe src="play/{k}.html?embed" loading="lazy"'
                f' title="Interactive picture for chapter {int(k)}"></iframe>'
                f'<figcaption>Use the controls to change the picture. '
                f'<a href="play/{k}.html">Open the activity on its own page</a>'
                f'</figcaption></figure>')
    body = PLAY_URL.sub(one, body)
    return body.replace(part.play_url, "play/")


def link_sibling_parts(body: str) -> str:
    """The articles link each other by source path; the site uses folders."""
    for p in PARTS:
        body = body.replace(f'href="../{p.slug}/ARTICLE.md"',
                            f'href="../{p.slug}/index.html"')
    return body


STYLE = """
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
  .kicker { color: var(--violet); font-size: 0.8rem; letter-spacing: 0.09em;
            text-transform: uppercase; font-weight: 600; margin: 0 0 0.5rem; }
  h1 { font-size: 2.1rem; line-height: 1.2; margin: 0 0 0.75rem; }
  .subtitle { color: var(--ink2); font-style: italic; font-size: 1.05rem;
              max-width: 40rem; margin: 0 auto; }
  h2 { font-size: 1.5rem; margin: 3.2rem 0 1rem; padding-top: 1.6rem;
       border-top: 1px solid var(--line); }
  h2 .n { color: var(--blue); }
  h3 { font-size: 1.15rem; margin: 2rem 0 0.6rem; }
  p { margin: 0.9rem 0; }
  figure { margin: 1.6rem 0; text-align: center; }
  figure img { max-width: 100%; height: auto; border-radius: 6px; }
  figcaption { color: var(--muted); font-size: 0.85rem; margin-top: 0.45rem;
               line-height: 1.45; }
  blockquote {
    margin: 1.4rem 0; padding: 0.85rem 1.1rem; border-left: 4px solid var(--green);
    background: var(--card); border-radius: 0 6px 6px 0; color: var(--ink);
  }
  blockquote p { margin: 0.35rem 0; }
  code, pre { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
              font-size: 0.9em; }
  code { background: #f0efec; padding: 0.1em 0.35em; border-radius: 4px; }
  pre { background: #f6f5f2; border: 1px solid var(--line); border-radius: 8px;
        padding: 0.9rem 1.1rem; overflow-x: auto; line-height: 1.5; }
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
    padding: 1rem 1.3rem; margin: 1.2rem 0 2rem; font-size: 0.95rem;
    columns: 2; column-gap: 2rem;
  }
  nav.toc a { display: block; padding: 0.12rem 0; color: var(--ink2); }
  nav.toc a:hover { color: var(--blue); }
  nav.parts { display: flex; gap: 0.6rem; margin: 2rem 0 0; flex-wrap: wrap; }
  nav.parts a { flex: 1 1 12rem; border: 1px solid var(--line); border-radius: 10px;
                padding: 0.7rem 0.9rem; background: var(--card); color: var(--ink2); }
  nav.parts a:hover { border-color: var(--blue); text-decoration: none; }
  nav.parts a.here { border-color: var(--violet); background: #f6f5ff; }
  nav.parts .pn { display: block; font-size: 0.72rem; letter-spacing: 0.08em;
                  text-transform: uppercase; color: var(--violet); font-weight: 600; }
  nav.parts .pt { display: block; font-size: 0.9rem; margin-top: 0.15rem; }
  .eq { overflow-x: auto; margin: 1rem 0; }
  /* the maths, the plain words and the simulation, rendered as one unit so a
     reader can see that each formal statement is paired with both */
  section.mathpair {
    background: var(--card); border: 1px solid var(--line);
    border-left: 4px solid var(--violet); border-radius: 0 10px 10px 0;
    padding: 0.3rem 1.2rem 1.1rem; margin: 1.9rem 0;
  }
  section.mathpair h3 {
    margin: 1rem 0 0.5rem; color: var(--violet); font-size: 1rem;
    letter-spacing: 0.02em; text-transform: uppercase;
  }
  section.mathpair figure.sim { margin-bottom: 0.4rem; }
  figure img.missing { outline: 2px dashed var(--red); padding: 1rem; }
  figure.sim iframe { width: 100%; height: 660px; border: 1px solid var(--line);
                      border-radius: 10px; background: #fff; }
  @media (max-width: 600px) { nav.toc { columns: 1; } h1 { font-size: 1.7rem; } }
"""

LOADER = """
// Every figure lists the places it might live: GitHub raw, which is the only
// one the published page can reach, and then the topic folder beside this
// file, which is the one that works when the page is opened straight from
// disk.  Try them in order rather than giving up on the first miss, so an
// animation never silently fails to appear.
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
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TITLEHERE</title>
<meta name="description" content="DESCHERE">
<script>
MathJax = {
  tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
         displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] },
  chtml: { scale: 1.0 }
};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>STYLEHERE</style>
</head>
<body>
<main>

BODY

<footer>
<p>Written in August 2026 as part of <a href="../../">conjectures</a>. The
<a href="REPOHERE">repository</a> contains the source for every figure.
<code>make figures</code> rebuilds the pictures, and <code>make test</code> reruns
the finite calculations.</p>
<p>The guide is based on Peter Scholze's <em>Lectures on Condensed Mathematics</em>
(<a href="https://arxiv.org/abs/2605.03658">arXiv:2605.03658</a>), which present
joint work with Dustin Clausen. It was written with AI assistance and human review.
Each chapter clearly separates calculations checked by the code from categorical
results quoted from the lectures.</p>
</footer>
</main>
<script>LOADERHERE</script>
</body>
</html>
""".replace("STYLEHERE", STYLE).replace("LOADERHERE", LOADER)


# --- the landing page for the topic ----------------------------------------

LANDING = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Condensed Mathematics</title>
<meta name="description" content="A step-by-step visual introduction to condensed mathematics, with an interactive activity in every chapter.">
<style>STYLEHERE
  .part { display: block; background: var(--card); border: 1px solid var(--line);
          border-radius: 10px; overflow: hidden; margin: 1.6rem 0; color: inherit; }
  .part:hover { border-color: var(--blue); box-shadow: 0 2px 14px rgba(0,0,0,0.06);
                text-decoration: none; }
  .part img { display: block; width: 100%; height: auto;
              border-bottom: 1px solid var(--line); }
  .part .body { padding: 1.1rem 1.3rem 1.3rem; }
  .part h3 { margin: 0 0 0.4rem; font-size: 1.25rem; }
  .part p { margin: 0.4rem 0 0; color: var(--ink2); font-size: 0.97rem; }
  .part .pn { display: inline-block; font-size: 0.72rem; letter-spacing: 0.08em;
              text-transform: uppercase; color: var(--violet); font-weight: 600; }
  .links { margin-top: 0.8rem; font-size: 0.92rem; color: var(--muted); }
  a.game { display: inline-block; border: 1px solid var(--blue); color: var(--blue);
           border-radius: 999px; padding: 0.5rem 1.1rem; font-size: 0.97rem; }
  a.game:hover { background: var(--blue); color: #fff; text-decoration: none; }
</style>
</head>
<body>
<main>

<header class="hero">
  <h1>Condensed Mathematics</h1>
  <p class="subtitle">A step-by-step introduction for readers who are new to the
  subject. Each chapter explains one idea in plain language and includes an
  activity that lets you change the mathematical example.</p>
</header>

<p>Condensed mathematics describes a space by looking at every continuous map
from a profinite probe into it. A probe is built from finite stages, so its basic
behavior can be explored through concrete pictures. This description repairs
some problems in topological algebra and leads to precise ways of handling
infinite sums, rings, and geometry.</p>

<p>The guide follows Peter Scholze's <a href="https://arxiv.org/abs/2605.03658"><em>Lectures
on Condensed Mathematics</em></a>, which present joint work with Dustin Clausen.
Begin with part one and read the three parts in order. Each part assumes only the
ideas explained in the earlier parts.</p>

CARDS

<h2>Learn through the game</h2>

<p>The three parts above explain the subject chapter by chapter. The
<a href="game/">game</a> teaches the same ideas through eight worlds and assumes
no previous mathematics. Each idea begins with a plain explanation. The game
then asks you to make a prediction, run an experiment, and finally learn the
standard name and notation.</p>

<p><a class="game" href="game/">Play the game &rarr;</a></p>

<h2>What the code checks</h2>

<p>A program cannot prove the category-level theorems in the lectures. It can check
the finite examples used to explain them. The tests build probes from finite sets,
verify compatible integer measures, calculate homology with Smith normal form, and
check the sizes and truncation counts shown in the activities. Every chapter says
which facts are calculated here and which theorems are quoted. The full list is in
<code>notes/research-content.md</code>.</p>

<footer>
  <p>The <a href="https://github.com/muchmirul/conjectures">source repository</a>
  contains the text, code, tests, and animations. A copy of the lectures is available
  in <a href="paper/">paper/</a>.</p>
</footer>

</main>
</body>
</html>
""".replace("STYLEHERE", STYLE)


def build_landing() -> None:
    cards = []
    for p in PARTS:
        hero = f"{p.raw}guide/00-start-here/hero.gif"
        cards.append(
            f'<a class="part" href="{p.slug}/">'
            f'<img src="{hero}" alt="Opening animation of part {p.number}">'
            f'<div class="body"><span class="pn">Part {p.number} · '
            f'{html.escape(p.lectures)}</span>'
            f"<h3>{html.escape(p.title)}</h3>"
            f"<p>{html.escape(p.blurb)}</p>"
            f'<p class="links">{len(p.chapters) - 1} chapters &middot; '
            f'{len(p.chapters) - 1} simulations embedded in the article'
            f"</p></div></a>")
    (DOCS / "index.html").write_text(LANDING.replace("CARDS", "\n".join(cards)))


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    for part in PARTS:
        out = DOCS / part.slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_html(parse(part.article.read_text()), part))
        print(f"  wrote {out.relative_to(DOCS.parent.parent)}")
    build_landing()
    print(f"  wrote {(DOCS / 'index.html').relative_to(DOCS.parent.parent)}")


if __name__ == "__main__":
    main()

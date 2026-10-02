"""Builds study-material pages from the simple text files in this folder.

Usage (inside frontend/materials):   python build.py
Every <name>.txt becomes ../<name>-material.html and uses the same look as python-material.html.

Format, one instruction per line:
  @page <emoji> <title>            @intro <text>
  @module <id> | <emoji> | <navigator label> | <heading> | <subtitle>
  @topic <heading>                 any other line -> paragraph
  - item   -> bullet list          1. item -> numbered list
  @table ... @end                  first row = header; cells split by |  (write \\| for a literal pipe)
  @result ... @end                 same format; shown as the output of the code block above it
  @code [language] ... @end        language defaults to c
  @info / @tip / @warn <text>      @practice  (numbered questions follow)
  @interview <text>
Inline markup: `code` and **bold**.
"""
import argparse
import html
import re
from pathlib import Path

HERE = Path(__file__).parent
BOXES = {"info": "info-box", "tip": "tip-box", "warn": "warn-box"}


def inline(text):
    codes = []

    def keep(match):
        codes.append(f"<code>{html.escape(match.group(1), quote=False)}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def table(rows):
    def cells(row):
        return [inline(c.strip().replace("\\|", "|")) for c in re.split(r"(?<!\\)\|", row)]
    head, *body = rows
    out = ["<table>", "<tr>" + "".join(f"<th>{c}</th>" for c in cells(head)) + "</tr>"]
    out += ["<tr>" + "".join(f"<td>{c}</td>" for c in cells(r)) + "</tr>" for r in body]
    return "\n".join(out + ["</table>"])


def build(source):
    lines = source.read_text(encoding="utf-8").splitlines()
    meta = {"title": "", "intro": ""}
    modules, stats = [], {"topics": 0, "code": 0, "practice": 0}
    module = topic = None
    items, kind = [], None                     # pending list items and "ul"/"ol"

    def target():
        return topic if topic is not None else module["body"]

    def flush_list():
        nonlocal items, kind
        if items:
            target().append(f"<{kind}>" + "".join(f"<li>{i}</li>" for i in items) + f"</{kind}>")
        items, kind = [], None

    def close_topic():
        nonlocal topic
        flush_list()
        if topic is not None:
            module["body"].append('<div class="topic">\n' + "\n".join(topic) + "\n</div>")
        topic = None

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        i += 1
        if not line.strip():
            continue
        if line.startswith("@page "):
            meta["title"] = line[6:].strip()
        elif line.startswith("@intro "):
            meta["intro"] = line[7:].strip()
        elif line.startswith("@module "):
            if module:
                close_topic()
            mid, emoji, label, heading, sub = [p.strip() for p in line[8:].split("|")]
            module = {"id": mid, "emoji": emoji, "label": label, "heading": heading, "sub": sub, "body": []}
            modules.append(module)
        elif line.startswith("@topic "):
            close_topic()
            topic = [f"<h3>{inline(line[7:].strip())}</h3>"]
            stats["topics"] += 1
        elif line == "@practice":
            close_topic()
            topic = ["<h3>🏋️ Practice Questions</h3>"]
        elif line.startswith("@interview "):
            close_topic()
            module["body"].append('<div class="interview-box"><strong>🎤 One-Line Interview Answer</strong>'
                                  f"<span>{inline(line[11:].strip())}</span></div>")
        elif line.split(" ")[0][1:] in BOXES and line.startswith("@"):
            flush_list()
            name, text = line[1:].split(" ", 1)
            target().append(f'<div class="{BOXES[name]}">{inline(text)}</div>')
        elif line in ("@table", "@result"):
            flush_list()
            rows = []
            while lines[i].strip() != "@end":
                rows.append(lines[i])
                i += 1
            i += 1
            if line == "@table":
                target().append(table(rows))
            else:                              # output of the query just above it
                html_table = table(rows)
                if len(rows) == 1:
                    cols = len(re.split(r"(?<!\\)\|", rows[0]))
                    html_table = html_table.replace("</table>", f'<tr><td colspan="{cols}" class="muted">(no rows)</td></tr></table>')
                target().append(f'<div class="result"><span class="result-label">Result</span>\n{html_table}</div>')
        elif line.startswith("@code"):
            flush_list()
            lang = line[5:].strip() or "c"
            code = []
            while lines[i].strip() != "@end":
                code.append(lines[i])
                i += 1
            i += 1
            target().append(f'<pre><code class="language-{lang}">{html.escape(chr(10).join(code), quote=False)}</code></pre>')
            stats["code"] += 1
        elif re.match(r"^- ", line) or re.match(r"^\d+\. ", line):
            new_kind = "ul" if line.startswith("- ") else "ol"
            if kind and kind != new_kind:
                flush_list()
            kind = new_kind
            items.append(inline(re.sub(r"^(- |\d+\. )", "", line)))
            if new_kind == "ol" and topic and topic[0].endswith("Practice Questions</h3>"):
                stats["practice"] += 1
        else:
            flush_list()
            target().append(f"<p>{inline(line.strip())}</p>")
    close_topic()

    cards = []
    for n, m in enumerate(modules):
        cards.append(f"""      <div class="module-card" id="{m['id']}">
        <div class="module-header">
          <span class="module-emoji">{m['emoji']}</span>
          <div class="module-title-group">
            <h2>{inline(m['heading'])}</h2>
            <p>{inline(m['sub'])}</p>
          </div>
          <span class="module-toggle">▼</span>
        </div>
        <div class="module-body{' open' if n == 0 else ''}">
{chr(10).join(m['body'])}
        </div>
      </div>""")
    nav = "\n".join(f'      <a href="#{m["id"]}">{inline(m["label"])}</a>' for m in modules)
    numbers = [(len(modules), "Modules"), (stats["topics"], "Topics"), (stats["code"], "Code Examples"),
               (stats["practice"], "Practice Qs")]
    stat_html = "".join(f'<div class="stat"><div class="stat-num">{v}</div><div class="stat-lbl">{k}</div></div>' for v, k in numbers)
    emoji, title = meta["title"].split(" ", 1)

    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · Portfolio</title>
  <meta name="description" content="{html.escape(meta['intro'])}">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>{emoji}</text></svg>">
  <script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/github-dark.min.css">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <!-- Generated by materials/build.py from materials/{source.name}. Edit that file, not this one. -->
  <main id="app" class="pm">
    <section class="pm-hero">
      <div class="wrap">
        <a href="study.html" class="muted">← Study materials</a>
        <h1>{emoji} {html.escape(title)}</h1>
        <p>{inline(meta['intro'])}</p>
        <div class="stats">{stat_html}</div>
      </div>
    </section>

    <nav class="module-nav" aria-label="Modules">
{nav}
    </nav>

    <div class="wrap pm-content">
      <div class="pm-tools">
        <button class="btn btn-ghost btn-sm" type="button" data-expand>Expand all</button>
        <button class="btn btn-ghost btn-sm" type="button" data-collapse>Collapse all</button>
      </div>

{chr(10).join(cards)}
    </div>
  </main>
  <script src="js/config.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"></script>
  <script type="module" src="js/pages/material.js"></script>
</body>
</html>
"""
    out = HERE.parent / f"{source.stem}-material.html"
    out.write_text(page, encoding="utf-8")
    print(f"{out.name}: {len(modules)} modules, {stats['topics']} topics, {stats['code']} code examples, "
          f"{stats['practice']} practice questions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build study-material pages from DSL source files.")
    parser.add_argument("sources", nargs="*", help="source filenames in this folder; defaults to all .txt files")
    args = parser.parse_args()
    sources = [HERE / name for name in args.sources] if args.sources else sorted(HERE.glob("*.txt"))
    for txt in sources:
        if not txt.is_file():
            parser.error(f"source file not found: {txt}")
        build(txt)

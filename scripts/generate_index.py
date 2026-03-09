#!/usr/bin/env python3
"""
Scans the `public/` directory and generates `index.html` with a linked folder tree.
All files link to viewer.html?file=<path> for format-aware rendering.
Run from the repo root: python3 scripts/generate_index.py
"""

import html
from pathlib import Path

PUBLIC_DIR = Path("public")
OUTPUT_FILE = Path("index.html")


def build_tree(directory: Path) -> str:
    entries = sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    if not entries:
        return ""
    lines = ["<ul>"]
    for entry in entries:
        name = html.escape(entry.name)
        if entry.is_dir():
            inner = build_tree(entry)
            lines.append(f'<li><span class="folder">&#x1F4C1; {name}</span>{inner}</li>')
        else:
            rel = entry.relative_to(Path("."))
            lines.append(f'<li><a href="viewer.html?file={rel}">&#x1F4C4; {name}</a></li>')
    lines.append("</ul>")
    return "\n".join(lines)


def generate() -> None:
    if not PUBLIC_DIR.exists():
        print(f"'{PUBLIC_DIR}' folder not found — nothing to index.")
        return

    tree_html = build_tree(PUBLIC_DIR)
    if not tree_html:
        tree_html = '<p class="empty">No files found in <code>public/</code> yet.</p>'

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>File Index</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 48px 16px;
    }}

    .card {{
      background: #fff;
      border-radius: 16px;
      padding: 40px 48px;
      box-shadow: 0 20px 60px rgba(0,0,0,.2);
      max-width: 640px;
      margin: 0 auto;
    }}

    h1 {{
      font-size: 1.75rem;
      color: #1a1a2e;
      margin-bottom: 4px;
    }}

    .subtitle {{
      color: #888;
      font-size: 0.9rem;
      margin-bottom: 28px;
    }}

    ul {{
      list-style: none;
      padding-left: 20px;
    }}

    ul:first-of-type {{
      padding-left: 0;
    }}

    li {{
      margin: 6px 0;
      font-size: 0.95rem;
    }}

    a {{
      color: #667eea;
      text-decoration: none;
      font-weight: 500;
    }}

    a:hover {{
      text-decoration: underline;
    }}

    .folder {{
      font-weight: 600;
      color: #444;
    }}

    .empty {{
      color: #aaa;
      font-style: italic;
    }}

    .badge {{
      display: inline-block;
      margin-top: 28px;
      padding: 6px 16px;
      background: #667eea;
      color: #fff;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>&#x1F4C2; File Index</h1>
    <p class="subtitle">Auto-generated from the <code>public/</code> folder. Add files there to see them here.</p>
    {tree_html}
    <div><span class="badge">&#x2705; GitHub Pages</span></div>
  </div>
</body>
</html>
"""

    OUTPUT_FILE.write_text(page, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    generate()

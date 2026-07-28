#!/usr/bin/env python3
"""
LP Outreach — Outlook formatter. Turns a draft .md into its paste-ready .html twin.

Usage:
  python scripts/format_html.py drafts/insurance/2026-07-20-grawe-group.md  # one or more paths
  python scripts/format_html.py drafts/pension-funds/*.md                   # a batch
  python scripts/format_html.py --all                                       # every draft missing/stale

Drafts live in per-type subfolders (drafts/pension-funds/, drafts/insurance/, and
one folder per new LP type). --all walks all of them.

The .html is Calibri, bold <strong> bullet labels, a real <ul> list, and a grey
To/Subject header, so it pastes into Outlook with formatting intact. /draft runs
this automatically after writing each .md — you should never format by hand.
"""

import re
import sys
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "drafts"

HEAD = ("<!doctype html><meta charset='utf-8'>"
        "<div style=\"font-family:Calibri,Arial,sans-serif;font-size:11pt;"
        "color:#111;line-height:1.4\">")
FOOT = "</div>"

# Explicit spacing so the blank lines in the .md survive the paste into Outlook.
P_STYLE = "margin:0 0 11pt 0"
UL_STYLE = "margin:0 0 11pt 0;padding-left:22pt"


def esc(text):
    """HTML-escape, then turn **bold** into <strong>."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def split_frontmatter(raw):
    """Return (frontmatter_dict, body_text). Frontmatter is the leading --- block."""
    fm = {}
    body = raw
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip().lower()] = v.strip()
        body = m.group(2)
    return fm, body


def convert(md_path: Path) -> Path:
    raw = md_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(raw)

    to_addr = fm.get("to", "")
    subject = ""

    # Blocks separated by one or more blank lines.
    blocks = re.split(r"\n\s*\n", body.strip())
    parts = []
    for block in blocks:
        lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue

        # Subject line → header, not body.
        if len(lines) == 1 and lines[0].lower().startswith("subject:"):
            subject = lines[0].split(":", 1)[1].strip()
            continue

        # Bullet block: every line starts with "- " → real <ul> list, one <li> each.
        if all(ln.lstrip().startswith("- ") for ln in lines):
            items = "".join(f"<li>{esc(ln.lstrip()[2:].strip())}</li>" for ln in lines)
            parts.append(f"<ul style='{UL_STYLE}'>{items}</ul>")
            continue

        # Normal paragraph: internal line breaks (e.g. the sign-off) become <br>.
        # The margin is explicit because Outlook applies its own <p> defaults on
        # paste, which collapses the spacing the draft was written with.
        parts.append(f"<p style='{P_STYLE}'>" + "<br>".join(esc(ln) for ln in lines) + "</p>")

    header = (f"<p style='color:#666'><b>To:</b> {esc(to_addr) or 'FIND'} &nbsp; "
              f"<b>Subject:</b> {esc(subject)}</p><hr>")

    html = HEAD + header + "".join(parts) + FOOT
    out_path = md_path.with_suffix(".html")
    out_path.write_text(html, encoding="utf-8")
    return out_path


def is_stale(md_path: Path) -> bool:
    html_path = md_path.with_suffix(".html")
    if not html_path.exists():
        return True
    return md_path.stat().st_mtime > html_path.stat().st_mtime


def main(argv):
    if not argv:
        print(__doc__)
        sys.exit(1)

    if argv == ["--all"]:
        # Only dated email drafts (YYYY-MM-DD-<slug>.md), in every type subfolder.
        # Never review packets etc.
        targets = [p for p in sorted(DRAFTS.rglob("20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]-*.md"))
                   if is_stale(p)]
        if not targets:
            print("All draft .html twins are up to date.")
            return
    else:
        targets = [Path(a) for a in argv]

    for md_path in targets:
        md_path = md_path.resolve()
        if not md_path.exists():
            print(f"skip (not found): {md_path}")
            continue
        if md_path.suffix != ".md":
            print(f"skip (not .md): {md_path}")
            continue
        out = convert(md_path)
        try:
            shown = out.relative_to(ROOT)
        except ValueError:
            shown = out
        print(f"formatted: {shown}")


if __name__ == "__main__":
    main(sys.argv[1:])

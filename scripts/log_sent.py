#!/usr/bin/env python3
"""
LP Outreach — record a send: write sent/<lang>/ files and flip the tracker row.

Normally called by make_draft.py once you confirm a draft went out, so the loop
closes without a separate command. Also usable on its own:

  python scripts/log_sent.py drafts/en/pension-funds/2026-07-22-fondo-bcc.html

The point of capturing from the compose window rather than copying the draft is
that /calibrate learns from the difference between what was drafted and what was
actually sent. Copy the draft across and that difference is always zero, which is
exactly how the 2026-07-22 batch lost its calibration signal.
"""

import argparse
import csv
import html as htmllib
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_CSV = ROOT / "data" / "output.csv"
SENT = ROOT / "sent"
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")

HEAD = ("<!doctype html><meta charset='utf-8'>"
        "<div style=\"font-family:Calibri,Arial,sans-serif;font-size:11pt;"
        "color:#111;line-height:1.4\">")
FOOT = "</div>"


def slug_of(path: Path) -> str:
    return DATED.sub("", path.stem)


def read_rows():
    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def write_rows(rows):
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(rows)


def html_to_markdown(body_html: str) -> str:
    """Turn the compose body back into the draft's markdown shape."""
    h = body_html
    h = re.sub(r"<li[^>]*>(.*?)</li>", lambda m: "\n- " + m.group(1).strip(), h, flags=re.S)
    h = re.sub(r"</?ul[^>]*>", "\n", h)
    h = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", h, flags=re.S)
    h = re.sub(r"<b[^>]*>(.*?)</b>", r"**\1**", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", "\n", h)
    h = re.sub(r"</p\s*>", "\n\n", h)
    h = re.sub(r"<p[^>]*>", "", h)
    h = re.sub(r"<div[^>]*>", "\n", h)
    h = re.sub(r"</div\s*>", "", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = htmllib.unescape(h)
    h = re.sub(r"[ \t]+\n", "\n", h)
    h = re.sub(r"\n{3,}", "\n\n", h)
    return h.strip()


def classify_edits(draft_text: str, sent_text: str) -> str:
    """none | minor | major, by how much of the wording moved."""
    a, b = draft_text.split(), sent_text.split()
    if a == b:
        return "none"
    import difflib
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    return "minor" if ratio >= 0.90 else "major"


def render_html(to_addr: str, subject: str, body_md: str) -> str:
    sys.path.insert(0, str(ROOT / "scripts"))
    import format_html as fh
    parts = []
    for block in re.split(r"\n\s*\n", body_md.strip()):
        lines = [l.rstrip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        if all(l.lstrip().startswith("- ") for l in lines):
            items = "".join(f"<li>{fh.esc(l.lstrip()[2:].strip())}</li>" for l in lines)
            parts.append(f"<ul>{items}</ul>")
        else:
            parts.append("<p>" + "<br>".join(fh.esc(l) for l in lines) + "</p>")
    header = (f"<p style='color:#666'><b>To:</b> {fh.esc(to_addr)} &nbsp; "
              f"<b>Subject:</b> {fh.esc(subject)}</p><hr>")
    return HEAD + header + "".join(parts) + FOOT


def log_send(draft_path: Path, to_addr: str, subject: str,
             final_body_html: str | None = None, when: str | None = None):
    """Write the sent record and flip the tracker row. Returns a summary dict."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import format_html as fh

    draft_path = Path(draft_path).resolve()
    md_path = draft_path.with_suffix(".md")
    if not md_path.exists():
        raise SystemExit(f"error: no .md source beside {draft_path.name}")

    fm, draft_body = fh.split_frontmatter(md_path.read_text(encoding="utf-8"))
    draft_blocks = [b for b in re.split(r"\n\s*\n", draft_body.strip())
                    if b.strip() and not b.lower().startswith("subject:")]
    draft_md = "\n\n".join(draft_blocks)

    slug = slug_of(md_path)
    rows = read_rows()
    row = next((r for r in rows if r["slug"] == slug), None)
    if row is None:
        raise SystemExit(f"error: {slug} is not in data/output.csv")
    if row["stage"] == "sent":
        return {"already": True, "slug": slug, "company": row["company"]}

    lang = row.get("language") or fm.get("language") or "en"
    day = when or date.today().isoformat()

    # Prefer what was actually in the compose window; fall back to the draft.
    body_md = html_to_markdown(final_body_html) if final_body_html else draft_md
    if final_body_html and "Valori Capital" not in body_md:
        body_md = draft_md          # capture looked wrong, do not trust it
    edits = classify_edits(draft_md, body_md)

    out_dir = SENT / lang
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{day}-{slug}"

    front = {"lp": fm.get("lp", row["company"]), "to": to_addr,
             "contact": fm.get("contact", row.get("contact_name", "")),
             "bridge": fm.get("bridge", row.get("bridge", "")),
             "category_label": fm.get("category_label", row.get("category", "")),
             "edits": edits, "date_sent": day, "language": lang,
             "source": "captured from the Outlook compose window"
                       if final_body_html else "draft text (compose capture unavailable)"}
    fm_text = "\n".join(f"{k}: {v}" for k, v in front.items())
    (out_dir / f"{stem}.md").write_text(
        f"---\n{fm_text}\n---\n\nSubject: {subject}\n\n{body_md}\n", encoding="utf-8")
    (out_dir / f"{stem}.html").write_text(
        render_html(to_addr, subject, body_md), encoding="utf-8")

    row["stage"] = "sent"
    row["date_sent"] = day
    write_rows(rows)

    return {"already": False, "slug": slug, "company": row["company"], "lang": lang,
            "edits": edits, "md": out_dir / f"{stem}.md", "date": day}


def main():
    ap = argparse.ArgumentParser(description="Record a send from a draft .html.")
    ap.add_argument("draft", help="path to the draft .html that was sent")
    ap.add_argument("--date", help="date sent (YYYY-MM-DD), default today")
    args = ap.parse_args()

    sys.path.insert(0, str(ROOT / "scripts"))
    import make_draft as md
    to, subject, _ = md.parse_draft(Path(args.draft).resolve())
    res = log_send(Path(args.draft), to, subject, None, args.date)
    if res.get("already"):
        print(f"already logged as sent: {res['company']}")
    else:
        print(f"logged {res['company']} -> {res['md'].relative_to(ROOT)}  (edits: {res['edits']})")


if __name__ == "__main__":
    main()

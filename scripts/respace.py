#!/usr/bin/env python3
"""
LP Outreach — open up the spacing in draft bodies.

  python scripts/respace.py --preview drafts/en/pension-funds/2026-07-28-prevedi.md
  python scripts/respace.py drafts/en/**/*.md        # apply
  python scripts/respace.py --all                    # every draft

Four breaks, so the email breathes on a phone screen:
  1. after the salutation                (already standard, left alone)
  2. after the opening sentence          the hook stands on its own line
  3. before the closing block            the CTA stands apart, and is never split
  4. after "Kind regards,"               the name sits apart from the sign-off

Idempotent: running it twice changes nothing. It only moves whitespace, never
a word, so word counts and every fund figure stay exactly as they were.
"""

import argparse
import glob
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import program
ROOT = program.ROOT
import format_html as fh   # noqa: E402

SIGNOFFS = ("Kind regards,", "Mit freundlichen Grüßen,", "S pozdravom,")
# A sentence end: ".", not inside a number or an abbreviation, followed by a capital.
SENT_SPLIT = re.compile(r"(?<=[a-z0-9\)\]])\.\s+(?=[A-ZÄÖÜÁÉÍÓÚČŠŽŤĎŇĽŔ])")


def split_first_sentence(block: str) -> str:
    parts = SENT_SPLIT.split(block, maxsplit=1)
    if len(parts) != 2:
        return block
    first, rest = parts[0].rstrip(), parts[1].lstrip()
    if len(first.split()) < 4 or len(rest.split()) < 4:
        return block          # too short to be worth breaking
    return f"{first}.\n\n{rest}"


def split_last_sentence(block: str) -> str:
    """Put the final sentence of the closing block on its own line."""
    pieces = SENT_SPLIT.split(block)
    if len(pieces) < 2:
        return block
    last = pieces[-1].strip()
    head = block[: block.rfind(last)].rstrip()
    if len(last.split()) < 4 or len(head.split()) < 3:
        return block
    return f"{head}\n\n{last}"


def respace(text: str) -> str:
    fm_match = re.match(r"^(---\s*\n.*?\n---\s*\n)(.*)$", text, re.DOTALL)
    front, body = (fm_match.group(1), fm_match.group(2)) if fm_match else ("", text)

    blocks = [b for b in re.split(r"\n\s*\n", body.strip()) if b.strip()]
    subject = [b for b in blocks if b.lower().startswith("subject:")]
    core = [b for b in blocks if not b.lower().startswith("subject:")]
    if len(core) < 3:
        return text

    sign_idx = next((i for i, b in enumerate(core)
                     if any(s in b for s in SIGNOFFS)), None)

    out = []
    for i, b in enumerate(core):
        is_bullets = all(l.lstrip().startswith("- ") for l in b.splitlines() if l.strip())
        if i == 0:                                   # salutation
            out.append(b)
        elif i == 1 and not is_bullets:              # opening paragraph
            out.append(split_first_sentence(b))
        elif sign_idx is not None and i == sign_idx:  # sign-off block
            lines = [l.strip() for l in b.splitlines() if l.strip()]
            out.append(lines[0] + "\n\n" + "\n".join(lines[1:]) if len(lines) > 1 else b)
        elif sign_idx is not None and i == sign_idx - 1 and not is_bullets:
            # v5's closing block is a deliberate two-sentence CTA (deck sentence
            # plus the call ask) and must stay together. Splitting it here is what
            # v4 wanted, not v5.
            out.append(b)
        else:
            out.append(b)

    return front + ("\n\n".join(subject + out)).strip() + "\n"


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def main():
    ap = argparse.ArgumentParser(description="Open up spacing in draft bodies.")
    ap.add_argument("files", nargs="*", help="draft .md paths")
    ap.add_argument("--all", action="store_true", help="every draft under drafts/")
    ap.add_argument("--preview", action="store_true", help="print the result, write nothing")
    program.add_argument(ap)
    args = ap.parse_args()

    paths = ([Path(p) for p in glob.glob(str(program.DRAFTS / "**" / "*.md"), recursive=True)
              if "REVIEW" not in p] if args.all
             else [Path(f).resolve() for f in args.files])
    if not paths:
        if args.all:
            print(f"no drafts under {program.DRAFTS}, nothing to respace")
            return
        ap.error("give some .md files or --all")

    changed, touched = 0, []
    for p in sorted(paths):
        old = p.read_text(encoding="utf-8")
        new = respace(old)
        if args.preview:
            print(f"===== {rel(p)}\n{new}")
            continue
        if new != old:
            p.write_text(new, encoding="utf-8")
            touched.append(p)
            changed += 1
            print(f"respaced: {rel(p)}")

    if not args.preview:
        # Always refresh the twins. The bot reads the .html, so a respaced .md
        # with a stale twin means the old spacing is what lands in Outlook.
        for p in touched:
            fh.convert(p)
        if touched:
            print(f"rebuilt {len(touched)} .html twins")
        print(f"{changed} of {len(paths)} files changed")


if __name__ == "__main__":
    main()

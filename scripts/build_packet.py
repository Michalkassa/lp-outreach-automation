#!/usr/bin/env python3
"""
LP Outreach — compile drafts into printable REVIEW-PACKET files.

Drafts live at drafts/<language>/<type>/, e.g. drafts/en/pension-funds/.

  python scripts/build_packet.py               # everything
  python scripts/build_packet.py en            # one language bucket
  python scripts/build_packet.py insurance     # one type, across languages
  python scripts/build_packet.py sk/insurance  # one bucket and type

Writes a packet per type folder, a packet per language bucket, and a roll-up at
drafts/REVIEW-PACKET.md. Each is a title, a summary table (LP | Variant | Bridge
| Words), then every draft in full with a --- rule between them.

Deterministic on purpose. /review-packet runs this rather than retyping drafts.
"""

import re
import sys
from datetime import date
from pathlib import Path

import program

ROOT = program.ROOT
DRAFTS = program.DRAFTS
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")
LANGUAGES = ["en", "sk", "de"]
# Exactly two lists, matching FOLDER ROUTING in .claude/commands/draft.md.
LISTS = ["pension-funds", "insurance"]


def split_frontmatter(raw):
    fm, body = {}, raw
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip().lower()] = v.strip()
        body = m.group(2)
    return fm, body


def read_draft(path: Path):
    fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    blocks = [b for b in re.split(r"\n\s*\n", body.strip()) if b.strip()]
    subject = next((b.split(":", 1)[1].strip()
                    for b in blocks if b.lower().startswith("subject:")), "")
    core = [b for b in blocks if not b.lower().startswith("subject:")]
    stem = DATED.sub("", path.stem)
    variant = stem[-1] if re.search(r"-[ABC]$", stem) else "-"
    words = len(" ".join(core[1:-1]).split()) if len(core) > 2 else 0
    return {
        "lp": fm.get("lp", stem),
        "bridge": fm.get("bridge", fm.get("category_label", "")),
        "variant": variant,
        "subject": subject,
        "body": "\n\n".join(core),
        "words": int(fm.get("word_count", words) or words),
    }


def compile_folder(folder: Path, title: str):
    paths = sorted(p for p in folder.glob("*.md") if not p.name.startswith("REVIEW"))
    if not paths:
        return None, 0
    return render([read_draft(p) for p in paths], title), len(paths)


def render(drafts, title):
    out = [f"# REVIEW PACKET — {title}", "",
           f"Total drafts: {len(drafts)}  ·  compiled {date.today().isoformat()}", "",
           "| LP | Variant | Bridge | Words |", "|---|---|---|---|"]
    for d in drafts:
        bridge = d["bridge"][:48]
        out.append(f"| {d['lp']} | {d['variant']} | {bridge} | {d['words']} |")
    out.append("")
    for d in drafts:
        out += ["---", "", f"## {d['lp']} — {d['bridge'][:48]} ({d['variant']})", "",
                f"**Subject:** {d['subject']}", "", d["body"], ""]
    return "\n".join(out) + "\n"


def type_folders():
    """Every drafts/<lang>/<list>/ directory that exists, in language order."""
    found = []
    for lang in LANGUAGES:
        base = DRAFTS / lang
        if not base.is_dir():
            continue
        for name in LISTS:
            folder = base / name
            if folder.is_dir():
                found.append((lang, folder))
        stray = [p.name for p in base.iterdir() if p.is_dir() and p.name not in LISTS]
        if stray:
            print(f"warning: {base} has folders outside the two lists: {stray}")
    return found


def main(argv):
    # program.py already read --program straight from sys.argv; drop it here so
    # it is not mistaken for a folder name.
    cleaned = []
    skip = False
    for a in argv:
        if skip:
            skip = False
            continue
        if a == "--program":
            skip = True
            continue
        if a.startswith("--program="):
            continue
        cleaned.append(a)
    argv = cleaned

    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return

    folders = type_folders()
    scoped = bool(argv)
    if scoped:
        want = argv[0].strip().lower().replace(" ", "-").strip("/")
        # Exact matches only. Substring matching made "de" select
        # en/multilateral-DEvelopment-banks, which then rewrote the en packet.
        folders = [(l, f) for l, f in folders
                   if want == l or want == f.name.lower() or want == f"{l}/{f.name}".lower()]
        if not folders:
            # A real name that simply has no drafts yet is not an error, it is an
            # empty programme. Only an unrecognised name is worth failing on.
            known = set(LANGUAGES) | set(LISTS) | {f"{l}/{n}" for l in LANGUAGES for n in LISTS}
            if want in known:
                print(f"no drafts under {DRAFTS}/{want}, nothing to compile")
                return
            sys.exit(f"no draft folder matching '{argv[0]}'\n"
                     f"       try a language (en, sk, de), a list (insurance,"
                     f" pension-funds), or en/insurance")

    total, all_drafts = 0, []
    by_lang = {}
    for lang, folder in folders:
        title = f"{lang.upper()} — {folder.name.replace('-', ' ').title()}"
        text, n = compile_folder(folder, title)
        if not n:
            continue
        (folder / "REVIEW-PACKET.md").write_text(text, encoding="utf-8")
        print(f"{lang}/{folder.name}: {n} drafts")
        total += n
        drafts = [read_draft(p) for p in
                  sorted(p for p in folder.glob("*.md") if not p.name.startswith("REVIEW"))]
        by_lang.setdefault(lang, []).extend(drafts)
        all_drafts += drafts

    # One packet per language bucket, so a sending session is a single file.
    # Only rewrite a bucket packet when every type in that bucket was compiled,
    # otherwise a scoped run would silently truncate it.
    complete = {l for l, _ in type_folders()} if not scoped else {
        l for l in by_lang
        if {f.name for _, f in folders if _ == l} ==
           {f.name for ll, f in type_folders() if ll == l}
    }
    for lang, drafts in by_lang.items():
        if lang not in complete:
            print(f"{lang}/REVIEW-PACKET.md: left alone (partial run)")
            continue
        drafts.sort(key=lambda d: d["lp"].lower())
        (DRAFTS / lang / "REVIEW-PACKET.md").write_text(
            render(drafts, f"{lang.upper()} drafts (all types)"), encoding="utf-8")
        print(f"{lang}/REVIEW-PACKET.md: {len(drafts)} drafts")

    if not scoped and all_drafts:
        all_drafts.sort(key=lambda d: d["lp"].lower())
        (DRAFTS / "REVIEW-PACKET.md").write_text(
            render(all_drafts, "Valori Capital drafts (all languages)"), encoding="utf-8")
        print(f"REVIEW-PACKET.md (roll-up): {len(all_drafts)} drafts")

    print(f"total: {total}")


if __name__ == "__main__":
    main(sys.argv[1:])

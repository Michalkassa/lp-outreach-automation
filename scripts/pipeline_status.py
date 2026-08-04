#!/usr/bin/env python3
"""Funnel counts, send aging, and file/tracker consistency for the LP pipeline.

Source of truth is data/output.csv (semicolon-delimited). Informational only:
we never send follow-ups, so the aging list is a view, not a worklist.
"""
import csv
import glob
import os
import re
from collections import Counter
from datetime import date
from pathlib import Path

import program

ROOT = program.ROOT
OUTPUT_CSV = program.OUTPUT_CSV
STAGES = ["research", "drafted", "sent"]
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def slugs_in(pattern):
    """Slugs of the .md files under a glob, with any YYYY-MM-DD- prefix stripped."""
    found = set()
    for path in glob.glob(str(ROOT / pattern), recursive=True):
        name = os.path.basename(path)[:-3]
        if name.startswith("REVIEW") or name == "_TEMPLATE":
            continue
        found.add(DATED.sub("", name))
    return found


def misfiled(rows, top):
    """Slugs whose file sits in a language bucket the tracker disagrees with."""
    want = {r["slug"]: (r.get("language") or "") for r in rows}
    bad = []
    for path in glob.glob(str(ROOT / top / "**" / "*.md"), recursive=True):
        name = os.path.basename(path)[:-3]
        if name.startswith("REVIEW"):
            continue
        slug = DATED.sub("", name)
        rel = Path(path).relative_to(ROOT / top).parts
        bucket = rel[0] if len(rel) > 1 else ""
        expected = want.get(slug)
        if expected and bucket and bucket != expected:
            bad.append(f"{slug}: in {top}/{bucket}/, tracker says {expected}")
    return sorted(bad)


def main():
    if not OUTPUT_CSV.exists():
        print(f"missing {OUTPUT_CSV}")
        return

    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter=";"))

    lps = slugs_in(f"{program.PROSPECTS.name}/*.md")
    drafts = slugs_in("drafts/**/*.md")
    sent = slugs_in("sent/**/*.md")

    print(f"FUNNEL  ({len(rows)} LPs)")
    stages = Counter(r["stage"] for r in rows)
    for stage in STAGES:
        print(f"  {stage:<12} {stages.pop(stage, 0)}")
    for stage, n in stages.most_common():
        print(f"  {stage or '(blank)':<12} {n}   <- not a valid stage")

    print("\nBY LANGUAGE BUCKET")
    for code in ("en", "sk", "de"):
        subset = [r for r in rows if (r.get("language") or "") == code]
        if not subset:
            continue
        st = Counter(r["stage"] for r in subset)
        print(f"  {code}  {len(subset):>3} total | research {st['research']:>3}"
              f"  drafted {st['drafted']:>3}  sent {st['sent']:>3}")

    print("\nBY TYPE")
    for kind, n in Counter(r["type"] for r in rows).most_common():
        print(f"  {kind:<28} {n}")

    print("\nSCORE BANDS")
    bands = [(75, "75-100  draft now"), (55, "55-74   strong"),
             (35, "35-54   verify gaps"), (20, "20-34   radar"), (0, "<20     skip")]
    scored = Counter()
    for r in rows:
        value = int(r["score"]) if r["score"].strip().isdigit() else 0
        scored[next(label for floor, label in bands if value >= floor)] += 1
    for _, label in bands:
        print(f"  {label:<20} {scored[label]}")

    aging = []
    for r in rows:
        stamp = (r.get("date_sent") or "").strip()
        if r["stage"] == "sent" and stamp:
            try:
                aging.append(((date.today() - date.fromisoformat(stamp)).days, r["company"]))
            except ValueError:
                pass
    if aging:
        print("\nSENT, DAYS SINCE (informational, no follow-ups)")
        for days, name in sorted(aging, reverse=True):
            print(f"  {days:>4}  {name}")

    print("\nCONSISTENCY")
    checks = [
        ("row has no lps/*.md", [r["slug"] for r in rows if r["slug"] not in lps]),
        ("stage=drafted, no draft file",
         [r["slug"] for r in rows if r["stage"] == "drafted" and r["slug"] not in drafts]),
        ("stage=sent, no sent file",
         [r["slug"] for r in rows if r["stage"] == "sent" and r["slug"] not in sent]),
        ("stage=sent, no date_sent",
         [r["slug"] for r in rows if r["stage"] == "sent" and not (r["date_sent"] or "").strip()]),
        ("draft file matches no row", sorted(drafts - {r["slug"] for r in rows})),
        ("sent file matches no row", sorted(sent - {r["slug"] for r in rows})),
        ("draft filed under the wrong language bucket", misfiled(rows, "drafts")),
        ("sent filed under the wrong language bucket", misfiled(rows, "sent")),
    ]
    clean = True
    for label, bad in checks:
        if bad:
            clean = False
            print(f"  {label}: {len(bad)}")
            for slug in bad[:12]:
                print(f"      {slug}")
            if len(bad) > 12:
                print(f"      ... and {len(bad) - 12} more")
    if clean:
        print("  all clear")


if __name__ == "__main__":
    main()

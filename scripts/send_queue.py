#!/usr/bin/env python3
"""
LP Outreach — build the sending queue for the drafts that have not gone out yet.

  python scripts/send_queue.py                     # today's queue (5, the daily cap)
  python scripts/send_queue.py --lang en           # one language bucket
  python scripts/send_queue.py --all               # every unsent draft, no cap
  python scripts/send_queue.py --script run.sh     # write a runnable shell script

Reads stage=drafted rows from data/output.csv, pairs each with its .html twin,
applies the readiness checks from README.md, and prints the make_draft.py calls
in score order. Nothing is sent and nothing is modified.

Drafts that fail a readiness check are listed separately with the reason, so an
unconfirmed address is visible here rather than at the compose window.

Two LPs sharing one recipient are collapsed to the highest-scoring one. The
others are reported as held: one person gets one email, not one per entity.
"""

import argparse
import csv
import glob
import os
import re
import shlex
import sys
from pathlib import Path

import program

ROOT = program.ROOT
OUTPUT_CSV = program.OUTPUT_CSV
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")
DAILY_CAP = 5                      # PIPELINE.md: max 5 sends per day

SIGNOFFS = {"en": "Kind regards,", "de": "Mit freundlichen", "sk": "S pozdravom"}
RETIRED_ENDINGS = ("first vintage", "prvý vintage", "erste fondsgeneration")


def load_rows():
    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def already_contacted(rows):
    """(addresses, domains) that a sent email has already gone to.

    The queue dedupes within itself, but that misses the case that actually
    burns: a row whose recipient was emailed on a previous day. Same address is
    a hard hold. Same domain is a warning, since a second person at the same
    firm is a judgement call rather than a duplicate.
    """
    addrs, domains = {}, {}
    for r in rows:
        if r.get("stage") != "sent":
            continue
        email = (r.get("contact_email") or "").strip().lower()
        if "@" not in email:
            continue
        addr = email.split("/")[0].strip()
        addrs.setdefault(addr, r.get("company", ""))
        domains.setdefault(addr.split("@")[-1], r.get("company", ""))
    return addrs, domains


def draft_map():
    """slug -> path of the .html twin."""
    out = {}
    for p in glob.glob(str(ROOT / "drafts" / "**" / "*.html"), recursive=True):
        name = os.path.basename(p)
        if name.startswith("REVIEW"):
            continue
        out[DATED.sub("", name[:-5])] = Path(p)
    return out


def check(path: Path, lang: str):
    """Return (to, subject, [problems]) for one draft .html."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import make_draft as md

    try:
        to, subject, body = md.parse_draft(path)
    except SystemExit as exc:
        first = str(exc).splitlines()[0]
        return None, None, [first.split(":", 1)[-1].strip() or "unreadable draft"]

    problems = []
    if "@" not in to:
        problems.append(f"recipient is not an address ({to})")
    if body.count("<strong>") != 3:
        problems.append(f"{body.count('<strong>')} bold bullet labels, expected 3")
    if body.count("<li>") != 3:
        problems.append(f"{body.count('<li>')} bullets, expected 3")
    if any(r in subject.lower() for r in RETIRED_ENDINGS):
        problems.append("subject uses a retired ending")
    want = SIGNOFFS.get(lang)
    if want and want not in body:
        problems.append(f"missing the {lang} sign-off")
    return to, subject, problems


def main():
    ap = argparse.ArgumentParser(description="Build the make_draft.py queue for unsent drafts.")
    ap.add_argument("--lang", choices=["en", "sk", "de"], help="only this language bucket")
    ap.add_argument("--list", dest="lp_list", choices=["insurance", "pension-funds"],
                    help="only this list")
    ap.add_argument("--limit", type=int, default=DAILY_CAP,
                    help=f"how many to queue (default {DAILY_CAP}, the daily cap)")
    ap.add_argument("--all", action="store_true", help="ignore the limit, queue everything ready")
    ap.add_argument("--script", metavar="PATH", help="write a runnable shell script instead")
    program.add_argument(ap)
    args = ap.parse_args()

    rows = load_rows()
    drafts = draft_map()
    folder_of = {"Insurance": "insurance", "Pension funds": "pension-funds"}

    ready, blocked, missing = [], [], []
    for r in rows:
        if r.get("stage") != "drafted":
            continue
        if args.lang and r.get("language") != args.lang:
            continue
        if args.lp_list and folder_of.get(r.get("list")) != args.lp_list:
            continue
        path = drafts.get(r["slug"])
        if not path:
            missing.append(r["company"])
            continue
        to, subject, problems = check(path, r.get("language", "en"))
        score = int(r["score"]) if str(r.get("score", "")).strip().isdigit() else 0
        entry = {"score": score, "company": r["company"], "to": to or "",
                 "path": path, "lang": r.get("language", ""), "flag": r.get("flag", "")}
        (blocked if problems else ready).append({**entry, "problems": problems})

    ready.sort(key=lambda e: (-e["score"], e["company"].lower()))

    # One person, one email. Keep the highest score, hold the rest.
    sent_addrs, sent_domains = already_contacted(rows)
    seen, queue, held, warn = {}, [], [], []
    for e in ready:
        key = e["to"].lower()
        if key in sent_addrs:
            held.append((e, f"already sent to this address ({sent_addrs[key]})"))
        elif key in seen:
            held.append((e, f"shares {e['to']} with {seen[key]['company']}"))
        else:
            seen[key] = e
            queue.append(e)
            firm = sent_domains.get(key.split("@")[-1])
            if firm:
                warn.append((e, firm))

    if not args.all:
        queue = queue[:max(args.limit, 0)]

    print(f"unsent drafts matching filters : {len(ready) + len(blocked)}")
    print(f"  ready                        : {len(ready)}")
    print(f"  held (shared recipient)      : {len(held)}")
    print(f"  blocked (failed a check)     : {len(blocked)}")
    if missing:
        print(f"  no draft file on disk        : {len(missing)} {missing}")
    print(f"  queued now                   : {len(queue)}"
          f"{'' if args.all else f' (cap {args.limit}, use --all to override)'}")

    if blocked:
        print("\nBLOCKED — fix these before they can be queued")
        for e in blocked:
            print(f"  [{e['score']}] {e['company']}")
            for p in e["problems"]:
                print(f"        {p}")

    if held:
        print("\nHELD — one email per person")
        for e, why in held:
            print(f"  [{e['score']}] {e['company']}: {why}")

    if warn:
        print("\nWARNING — this firm has already had an email, different person")
        for e, firm in warn:
            print(f"  [{e['score']}] {e['company']} <{e['to']}>  firm already emailed via {firm}")

    if not queue:
        print("\nnothing to queue.")
        return

    # Paths are printed relative to the REPO, not the programme root, because you
    # run these from the repo root whichever programme they belong to.
    cmds = [f".venv/bin/python scripts/make_draft.py "
            f"{shlex.quote(str(e['path'].relative_to(program.REPO)))}"
            for e in queue]

    if args.script:
        out = Path(args.script)
        lines = ["#!/bin/bash",
                 "# Generated by scripts/send_queue.py. Runs one compose window at a time.",
                 "# Nothing is sent: each draft stops in Outlook for you to check, attach",
                 "# the deck and send by hand. Close the browser to move to the next one.",
                 "set -u",
                 f'cd "$(dirname "$0")"' if out.parent == ROOT else f'cd {shlex.quote(str(ROOT))}',
                 ""]
        for i, (e, c) in enumerate(zip(queue, cmds), 1):
            lines += [f'echo "=== {i}/{len(queue)}  [{e["score"]}] {e["company"]} -> {e["to"]}"',
                      c,
                      f'read -r -p "sent {i}/{len(queue)}? Enter for the next, Ctrl+C to stop " _',
                      ""]
        lines.append('echo "queue finished."')
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        out.chmod(0o755)
        print(f"\nwrote {out}  ({len(queue)} drafts)\nrun it with:  ./{out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
        return

    print("\nRun these one at a time, from your own terminal:\n")
    for i, (e, c) in enumerate(zip(queue, cmds), 1):
        print(f"# {i}/{len(queue)}  [{e['score']}] {e['company']}  ->  {e['to']}")
        print(f"{c}\n")


if __name__ == "__main__":
    main()

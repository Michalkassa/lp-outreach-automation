#!/usr/bin/env python3
"""Funnel counts + aging of sent-awaiting-reply (informational; no follow-ups)."""
import csv
from collections import Counter
from datetime import date
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "crm" / "pipeline.csv"

def main():
    today = date.today()
    stages, aging = Counter(), []
    with open(CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            stages[row.get("stage", "?")] += 1
            if row.get("stage") == "sent" and (row.get("last_touch") or "").strip():
                try:
                    days = (today - date.fromisoformat(row["last_touch"].strip())).days
                    aging.append((days, row["lp_name"]))
                except ValueError:
                    pass
    print("FUNNEL")
    for s, n in stages.most_common():
        print(f"  {s:<20} {n}")
    if aging:
        aging.sort(reverse=True)
        print("\nSENT, AWAITING REPLY (days since send)")
        for days, name in aging:
            print(f"  {days:>4}  {name}")

if __name__ == "__main__":
    main()

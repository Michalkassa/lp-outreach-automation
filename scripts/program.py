#!/usr/bin/env python3
"""
Which outreach programme a script is operating on.

Every script in this folder works on either programme. They are identical in
shape, so the only thing that changes is the root folder:

  lp     the repo root          input.xlsx, data/, lps/,       drafts/, sent/
  co-gp  the co-gp/ folder      input.xlsx, data/, prospects/, drafts/, sent/

Select one of three ways, in this order:

  .venv/bin/python scripts/pipeline_status.py --program co-gp
  VALORI_PROGRAM=co-gp .venv/bin/python scripts/pipeline_status.py
  (nothing)                                          -> lp

The flag is read straight from sys.argv rather than through argparse, because
the paths below are module-level constants that other scripts import at import
time, which happens before any parser runs.
"""

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROGRAMS = ("lp", "co-gp")


def _selected() -> str:
    for i, arg in enumerate(sys.argv):
        if arg == "--program" and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
        if arg.startswith("--program="):
            return arg.split("=", 1)[1]
    return os.environ.get("VALORI_PROGRAM", "lp")


NAME = _selected()
if NAME not in PROGRAMS:
    sys.exit(f"error: unknown programme '{NAME}'. Use one of: {', '.join(PROGRAMS)}")

# lp lives at the repo root, every other programme in a folder of its own.
ROOT = REPO if NAME == "lp" else REPO / NAME

INPUT_XLSX = ROOT / "input.xlsx"
OUTPUT_XLSX = ROOT / "output.xlsx"
DATA = ROOT / "data"
LP_IMPORT = DATA / "lp-import.csv"
OUTPUT_CSV = DATA / "output.csv"
VERIFY_CSV = DATA / "verify.csv"
VERIFY_XLSX = ROOT / "verify.xlsx"
DRAFTS = ROOT / "drafts"
SENT = ROOT / "sent"
TEMPLATES = ROOT / "templates"
# The LP programme calls them lps/, everything else prospects/.
PROSPECTS = ROOT / ("lps" if NAME == "lp" else "prospects")


def add_argument(ap):
    """Register --program so argparse accepts it. The value is already resolved."""
    ap.add_argument("--program", choices=PROGRAMS, default=NAME,
                    help="which outreach programme to operate on (default lp)")


def label() -> str:
    return f"[{NAME}] {ROOT}"


if __name__ == "__main__":
    print(f"programme : {NAME}")
    for k in ("ROOT", "INPUT_XLSX", "OUTPUT_CSV", "PROSPECTS", "DRAFTS", "SENT", "TEMPLATES"):
        print(f"  {k:<12} {globals()[k]}")

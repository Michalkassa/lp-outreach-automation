#!/usr/bin/env python3
"""
LP Outreach — Excel/CSV converter for Valori Capital pipeline.

Usage:
  python scripts/convert.py init     # Create blank input.xlsx template
  python scripts/convert.py import   # input.xlsx → data/lp-import.csv
  python scripts/convert.py export   # data/output.csv → output.xlsx  (input order, not score order)
  python scripts/convert.py sync     # Populate input.xlsx from lp-import.csv + output.csv stage data
"""

import csv
import sys
from pathlib import Path

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("Missing dependency. Run:  .venv/bin/pip install openpyxl")
    sys.exit(1)

ROOT         = Path(__file__).resolve().parent.parent
INPUT_XLSX   = ROOT / "input.xlsx"
LP_IMPORT    = ROOT / "data" / "lp-import.csv"
OUTPUT_CSV   = ROOT / "data" / "output.csv"
OUTPUT_XLSX  = ROOT / "output.xlsx"

# ── Column definitions ────────────────────────────────────────────────────────
# input.xlsx / lp-import.csv columns (what the user fills in)
INPUT_COLS = [
    "Company", "Country", "Website",
    "First Name", "Last Name", "Title", "Email address", "LinkedIn",
    "Considered",
]
INPUT_WIDTHS = [32, 16, 28, 13, 13, 24, 30, 34, 11]

# output.csv / output.xlsx columns
OUTPUT_COLS = [
    "company", "country", "slug", "score", "aum",
    "contact_name", "contact_title", "contact_email",
    "stage", "category", "bridge", "flag", "date_sent",
]
OUTPUT_DISPLAY = {
    "company":       "Company",
    "country":       "Country",
    "slug":          "Slug",
    "score":         "Score /100",
    "aum":           "AUM",
    "contact_name":  "Contact",
    "contact_title": "Title",
    "contact_email": "Email",
    "stage":         "Stage",
    "category":      "Category",
    "bridge":        "Bridge / Key Hook",
    "flag":          "Flag",
    "date_sent":     "Date Sent",
}
OUTPUT_WIDTHS = {
    "company": 32, "country": 14, "slug": 24, "score": 10, "aum": 14,
    "contact_name": 22, "contact_title": 22, "contact_email": 30,
    "stage": 11, "category": 28, "bridge": 52, "flag": 30, "date_sent": 12,
}

# ── Colour palette ────────────────────────────────────────────────────────────
HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)
THIN        = Side(style="thin", color="D0D0D0")
BORDER      = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

SCORE_TIERS = [
    (75, "C6EFCE", "375623"),  # green
    (55, "FFEB9C", "9C5700"),  # yellow
    (35, "FFCCB3", "833C00"),  # orange
    (20, "FFDDE0", "9C0006"),  # red
    ( 0, "F2F2F2", "595959"),  # grey
]
STAGE_FILLS = {
    "drafted": PatternFill("solid", fgColor="BDD7EE"),
    "sent":    PatternFill("solid", fgColor="C6EFCE"),
    "skip":    PatternFill("solid", fgColor="F2F2F2"),
}
STAGE_COLORS_INPUT = {
    "imported": ("E2EFDA", "375623"),
    "research": ("DDEBF7", "1F3864"),
    "drafted":  ("BDD7EE", "1F3864"),
    "sent":     ("C6EFCE", "375623"),
    "skip":     ("F2F2F2", "595959"),
}


# ── Helpers ───────────────────────────────────────────────────────────────────
def make_header(ws, columns):
    ws.append(columns)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[1].height = 30


def score_fill(score_str):
    try:
        val = int(str(score_str).replace("/100", "").strip())
    except (ValueError, AttributeError):
        return PatternFill("solid", fgColor="F2F2F2"), Font(color="595959")
    for threshold, bg, fg in SCORE_TIERS:
        if val >= threshold:
            return PatternFill("solid", fgColor=bg), Font(color=fg, bold=True)
    return PatternFill("solid", fgColor="F2F2F2"), Font(color="595959")


def load_import_order():
    """Return list of company names in lp-import.csv order (lowercased)."""
    if not LP_IMPORT.exists():
        return []
    with open(LP_IMPORT, newline="", encoding="utf-8") as f:
        return [r.get("Company", "").strip().lower()
                for r in csv.DictReader(f, delimiter=";") if r.get("Company", "").strip()]


# ── INIT — create blank input.xlsx template ───────────────────────────────────
def cmd_init():
    if INPUT_XLSX.exists():
        print(f"input.xlsx already exists. Delete it first to recreate.")
        return

    wb  = openpyxl.Workbook()
    ws  = wb.active
    ws.title = "Prospects"

    make_header(ws, INPUT_COLS)
    ws.freeze_panes = f"A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(INPUT_COLS))}1"

    for i, w in enumerate(INPUT_WIDTHS, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    sample = ["Example Pensionskasse AG", "Austria", "https://example.at",
              "Max", "Mustermann", "CIO", "max.mustermann@example.at",
              "linkedin.com/in/max-mustermann", ""]
    ws.append(sample)
    for cell in ws[2]:
        cell.font = Font(italic=True, color="AAAAAA")

    _add_instructions(wb)
    wb.save(INPUT_XLSX)
    print(f"Created: {INPUT_XLSX}")


# ── IMPORT — input.xlsx → lps/lp-import.csv ──────────────────────────────────
def cmd_import():
    if not INPUT_XLSX.exists():
        print("input.xlsx not found. Run:  python scripts/convert.py init")
        sys.exit(1)

    wb   = openpyxl.load_workbook(INPUT_XLSX, data_only=True)
    ws   = wb["Prospects"]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print("No data in Prospects sheet.")
        return

    # Map column names from header row
    headers = [str(h).strip() if h else "" for h in rows[0]]
    data_rows = [
        {headers[i]: (str(v).strip() if v is not None else "") for i, v in enumerate(r)}
        for r in rows[1:]
        if r[0] and "Example" not in str(r[0])
    ]

    # Preserve existing Considered=yes
    existing_yes = set()
    if LP_IMPORT.exists():
        with open(LP_IMPORT, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter=";"):
                if r.get("Considered", "").strip().lower() == "yes":
                    existing_yes.add(r.get("Company", "").strip().lower())

    LP_IMPORT.parent.mkdir(exist_ok=True)
    written = skipped = 0

    with open(LP_IMPORT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=INPUT_COLS, delimiter=";",
                                extrasaction="ignore")
        writer.writeheader()
        for r in data_rows:
            company = r.get("Company", "").strip()
            if not company:
                continue
            considered = r.get("Considered", "").strip()
            if company.lower() in existing_yes:
                considered = "yes"
                skipped += 1
            out = {col: r.get(col, "") for col in INPUT_COLS}
            out["Considered"] = considered
            writer.writerow(out)
            written += 1

    print(f"Written {written} rows to {LP_IMPORT}  ({skipped} already considered=yes)")


# ── EXPORT — output.csv → output.xlsx (input order) ──────────────────────────
def cmd_export():
    if not OUTPUT_CSV.exists():
        print(f"output.csv not found at {OUTPUT_CSV}")
        sys.exit(1)

    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        reader    = csv.DictReader(f, delimiter=";")
        rows      = list(reader)
        csv_cols  = reader.fieldnames or []

    if not rows:
        print("output.csv is empty.")
        return

    # Order: follow lp-import.csv row order; unknowns at end
    import_order = load_import_order()
    order_map    = {name: i for i, name in enumerate(import_order)}
    rows.sort(key=lambda r: order_map.get(r.get("company", "").strip().lower(), 99999))

    # Columns: use OUTPUT_COLS, then any extras from CSV not already listed
    all_cols = OUTPUT_COLS + [c for c in csv_cols if c not in OUTPUT_COLS]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "LP Pipeline"

    make_header(ws, [OUTPUT_DISPLAY.get(c, c.replace("_", " ").title()) for c in all_cols])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(all_cols))}1"

    for row in rows:
        ws.append([row.get(c, "") for c in all_cols])
        row_idx = ws.max_row
        stage   = row.get("stage", "").lower()

        for col_idx, col_name in enumerate(all_cols, start=1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.alignment = Alignment(vertical="top", wrap_text=(col_name == "bridge"))
            cell.border = BORDER

            if col_name == "score":
                fill, font = score_fill(row.get("score", ""))
                cell.fill = fill
                cell.font = font
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_name == "stage" and stage in STAGE_FILLS:
                cell.fill = STAGE_FILLS[stage]
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif stage == "skip":
                cell.font = Font(color="AAAAAA")

    for col_idx, col_name in enumerate(all_cols, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = OUTPUT_WIDTHS.get(col_name, 18)

    _add_score_legend(wb)
    wb.save(OUTPUT_XLSX)

    active  = sum(1 for r in rows if r.get("stage") != "skip")
    skipped = len(rows) - active
    print(f"Exported {len(rows)} rows → {OUTPUT_XLSX}  ({active} active, {skipped} skipped)")
    print("Score distribution:")
    for label, lo, hi in [("75-100 (top)", 75, 100), ("55-74 (strong)", 55, 74),
                           ("35-54 (medium)", 35, 54), ("20-34 (low)", 20, 34), ("<20 (skip)", 0, 19)]:
        n = sum(1 for r in rows
                if lo <= _to_int(r.get("score", "0")) <= hi)
        if n:
            print(f"  {label}: {n}")


# ── SYNC — populate input.xlsx from lp-import.csv + stage/score from output.csv
def cmd_sync():
    if not LP_IMPORT.exists():
        print(f"lp-import.csv not found at {LP_IMPORT}. Nothing to sync.")
        sys.exit(1)

    # Load stages + scores + country from output.csv
    out_data = {}
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter=";"):
                key = r.get("company", "").strip().lower()
                out_data[key] = {
                    "stage":   r.get("stage", ""),
                    "score":   r.get("score", ""),
                    "country": r.get("country", ""),
                }

    with open(LP_IMPORT, newline="", encoding="utf-8") as f:
        import_rows = list(csv.DictReader(f, delimiter=";"))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prospects"

    sync_cols   = INPUT_COLS + ["Stage", "Score /100"]
    sync_widths = INPUT_WIDTHS + [11, 12]

    make_header(ws, sync_cols)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(sync_cols))}1"
    for i, w in enumerate(sync_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    for r in import_rows:
        company = r.get("Company", "").strip()
        if not company:
            continue
        info    = out_data.get(company.lower(), {})
        stage   = info.get("stage", "imported")
        score   = info.get("score", "")
        # Use country from output.csv if import row has none
        country = r.get("Country", "") or info.get("country", "")

        row_vals = [
            company,
            country,
            r.get("Website", ""),
            r.get("First Name", ""),
            r.get("Last Name", ""),
            r.get("Title", ""),
            r.get("Email address", ""),
            r.get("LinkedIn", r.get("Linkedin ", "")),
            r.get("Considered", ""),
            stage,
            score,
        ]
        ws.append(row_vals)
        row_idx = ws.max_row
        bg, fg  = STAGE_COLORS_INPUT.get(stage, ("FFFFFF", "000000"))

        for col_idx, _ in enumerate(row_vals, start=1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top")
            if col_idx == len(INPUT_COLS):       # Stage (last INPUT_COL + 1)
                cell.fill = PatternFill("solid", fgColor=bg)
                cell.font = Font(color=fg)
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx == len(INPUT_COLS) + 1:  # Score
                sfill, sfont = score_fill(score)
                cell.fill = sfill
                cell.font = sfont
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif stage == "skip":
                cell.font = Font(color="AAAAAA")

    _add_instructions(wb)
    wb.save(INPUT_XLSX)

    counts = {}
    for r in import_rows:
        s = out_data.get(r.get("Company", "").strip().lower(), {}).get("stage", "imported")
        counts[s] = counts.get(s, 0) + 1
    print(f"Synced {len(import_rows)} rows → {INPUT_XLSX}")
    print("Stages: " + ", ".join(f"{s}={n}" for s, n in counts.items()))


# ── Shared sheet builders ──────────────────────────────────────────────────────
def _to_int(s):
    try:
        return int(str(s).replace("/100", "").strip())
    except (ValueError, AttributeError):
        return 0


def _add_score_legend(wb):
    ws = wb.create_sheet("Score Legend")
    data = [
        ("Score Range", "Meaning", "Action"),
        ("75 – 100", "Top priority",   "Draft immediately"),
        ("55 – 74", "Strong prospect", "Research complete — draft when ready"),
        ("35 – 54", "Medium",          "Worth contacting — verify gaps first"),
        ("20 – 34", "Low",             "Keep on radar"),
        ("< 20",    "Skip",            "Regulatory barrier or AUM too small"),
    ]
    for i, (rng, meaning, action) in enumerate(data, start=1):
        ws.cell(row=i, column=1, value=rng)
        ws.cell(row=i, column=2, value=meaning)
        ws.cell(row=i, column=3, value=action)
        if i == 1:
            for col in range(1, 4):
                c = ws.cell(row=i, column=col)
                c.fill = HEADER_FILL
                c.font = HEADER_FONT
        else:
            score_val = data[i - 1][0].split("–")[0].replace("<", "0").strip()
            fill, font = score_fill(score_val)
            ws.cell(row=i, column=1).fill = fill
            ws.cell(row=i, column=1).font = font
    for col, w in [(1, 14), (2, 22), (3, 35)]:
        ws.column_dimensions[get_column_letter(col)].width = w


def _add_instructions(wb):
    ws = wb.create_sheet("How to use") if "How to use" not in wb.sheetnames else wb["How to use"]
    lines = [
        ("HOW TO ADD NEW PROSPECTS", True),
        ("1. Add rows to the Prospects sheet: Company, Country, Website, contact details.", False),
        ("2. Leave Considered blank for new rows. Stage and Score are auto-filled by sync.", False),
        ("3. Save, then run:  .venv/bin/python scripts/convert.py import", False),
        ("   This writes data/lp-import.csv preserving existing Considered=yes rows.", False),
        ("", False),
        ("HOW TO RUN RESEARCH IN CLAUDE", True),
        ("4. In Claude Code, run /import-lps  — creates stub .md files for new rows.", False),
        ("5. Run /research <Company Name>  — web research, score 1-100, full context file.", False),
        ("", False),
        ("HOW TO GET THE OUTPUT", True),
        ("6. .venv/bin/python scripts/convert.py export   →  output.xlsx (from data/output.csv)", False),
        ("7. .venv/bin/python scripts/convert.py sync     →  update THIS file with Stage + Score", False),
        ("", False),
        ("STAGE MEANINGS", True),
        ("  imported  stub created, research not yet run", False),
        ("  research  research complete, score assigned", False),
        ("  drafted   email draft in /drafts/", False),
        ("  sent      email sent, stored in /sent/", False),
        ("  skip      not viable (regulatory barrier, AUM too small)", False),
        ("", False),
        ("SCORE RANGE", True),
        ("  75-100   Top priority — draft immediately", False),
        ("  55-74    Strong prospect — draft when ready", False),
        ("  35-54    Medium — verify gaps first", False),
        ("  20-34    Low — keep on radar", False),
        ("  <20      Skip", False),
    ]
    for i, (text, bold) in enumerate(lines, start=1):
        cell = ws.cell(row=i, column=1, value=text)
        cell.font = Font(bold=True, size=11) if bold else (
            Font(color="444444") if text.startswith("  ") else Font()
        )
    ws.column_dimensions["A"].width = 72


# ── Entry point ───────────────────────────────────────────────────────────────
COMMANDS = {
    "init":   cmd_init,
    "import": cmd_import,
    "export": cmd_export,
    "sync":   cmd_sync,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        print(f"Available commands: {', '.join(COMMANDS)}")
        sys.exit(1)
    COMMANDS[sys.argv[1]]()

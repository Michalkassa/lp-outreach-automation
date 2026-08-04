#!/usr/bin/env python3
"""
LP Outreach — Excel/CSV converter for Valori Capital pipeline.

Usage:
  python scripts/convert.py init            # Create blank input.xlsx template
  python scripts/convert.py import          # input.xlsx → data/lp-import.csv
  python scripts/convert.py export          # data/output.csv → output.xlsx
  python scripts/convert.py sync            # Populate input.xlsx with Stage + Score from output.csv
  python scripts/convert.py verify-export   # Scan output.csv for VERIFY/FIND items → verify.xlsx
  python scripts/convert.py verify-import   # Read verify.xlsx confirmed values → patch output.csv
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

import program

ROOT         = program.ROOT
INPUT_XLSX   = program.INPUT_XLSX
LP_IMPORT    = program.LP_IMPORT
OUTPUT_CSV   = program.OUTPUT_CSV
OUTPUT_XLSX  = program.OUTPUT_XLSX
VERIFY_CSV   = program.VERIFY_CSV
VERIFY_XLSX  = program.VERIFY_XLSX

# ── Column definitions ────────────────────────────────────────────────────────
# input.xlsx / lp-import.csv columns (what the user fills in)
INPUT_COLS = [
    "Country", "Type", "Company", "Website",
    "First Name", "Last Name", "Title", "Email address", "LinkedIn",
    "Considered",
]
INPUT_WIDTHS = [14, 20, 30, 26, 12, 12, 24, 30, 32, 11]

# output.csv / output.xlsx columns
OUTPUT_COLS = [
    "country", "language", "type", "list", "company", "slug", "score", "aum",
    "contact_name", "contact_title", "contact_email",
    "stage", "category", "bridge", "flag", "date_sent",
]
# Country decides the email language. Keep this in step with the same rule in
# .claude/commands/draft.md and scripts/build_packet.py.
LANG_BY_COUNTRY = {"Slovakia": "sk", "Czech Republic": "sk",
                   "Austria": "de", "Germany": "de"}
LANGUAGES = ["en", "sk", "de"]

# There are exactly two source lists. Entity type is descriptive detail only:
# a bank or development agency belongs to whichever list it came in on, it is
# never a list of its own. Mirrors FOLDER ROUTING in .claude/commands/draft.md.
LISTS = ["Insurance", "Pension funds"]
LIST_FOLDER = {"Insurance": "insurance", "Pension funds": "pension-funds"}


def language_for(country: str) -> str:
    return LANG_BY_COUNTRY.get((country or "").strip(), "en")


def list_for(lp_type: str) -> str:
    return "Pension funds" if "pension" in (lp_type or "").lower() else "Insurance"


OUTPUT_DISPLAY = {
    "country":       "Country",
    "language":      "Lang",
    "type":          "Type",
    "list":          "List",
    "company":       "Company",
    "slug":          "Slug",
    "score":         "Score",
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
    "country": 14, "language": 7, "type": 20, "list": 14,
    "company": 30, "slug": 24, "score": 8, "aum": 14,
    "contact_name": 22, "contact_title": 22, "contact_email": 30,
    "stage": 11, "category": 28, "bridge": 52, "flag": 30, "date_sent": 12,
}

# ── Verify columns ────────────────────────────────────────────────────────────
# Fields in output.csv that may carry VERIFY / FIND: markers, and whether
# confirming the value should trigger a rescore of that LP.
VERIFY_FIELDS = [
    ("aum",           "AUM",           True),
    ("contact_name",  "Contact Name",  True),
    ("contact_title", "Contact Title", False),
    ("contact_email", "Email",         False),
    ("bridge",        "Bridge",        False),
    ("flag",          "Flag",          False),
]
VERIFY_CSV_COLS = [
    "company", "slug", "field", "display_field",
    "current_value", "verified_value", "source", "affects_score", "status",
]
VERIFY_XLSX_HEADERS = [
    "Company", "Slug", "Field", "What to Verify",
    "Current Value", "Your Verified Value", "Source",
    "Affects Score", "Status",
]
VERIFY_WIDTHS = [28, 22, 14, 16, 36, 36, 30, 14, 10]

# ── Colour palette ────────────────────────────────────────────────────────────
HEADER_FILL = PatternFill("solid", fgColor="EF7B88")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)
THIN        = Side(style="thin", color="D0D0D0")
BORDER      = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

SCORE_TIERS = [
    (75, "C6EFCE", "375623"),  # green
    (55, "FFEB9C", "9C5700"),  # yellow
    (35, "FFCCB3", "833C00"),  # orange
    (20, "FFDDE0", "9C0006"),  # red
    ( 0, "FFFFFF", "000000"),  # white (no fill) — skip/unscored
]
STAGE_FILLS = {
    "drafted": PatternFill("solid", fgColor="BDD7EE"),
    "sent":    PatternFill("solid", fgColor="C6EFCE"),
    "skip":    PatternFill("solid", fgColor="FFFFFF"),
}
STAGE_COLORS_INPUT = {
    "imported": ("E2EFDA", "375623"),
    "research": ("DDEBF7", "1F3864"),
    "drafted":  ("BDD7EE", "1F3864"),
    "sent":     ("C6EFCE", "375623"),
    "skip":     ("FFFFFF", "000000"),
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
        return PatternFill("solid", fgColor="FFFFFF"), Font(color="000000")
    for threshold, bg, fg in SCORE_TIERS:
        if val >= threshold:
            return PatternFill("solid", fgColor=bg), Font(color=fg, bold=True)
    return PatternFill("solid", fgColor="FFFFFF"), Font(color="000000")


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

    sample = ["Austria", "Pension Fund", "Example Pensionskasse AG", "https://example.at",
              "Max", "Mustermann", "CIO", "max.mustermann@example.at",
              "linkedin.com/in/max-mustermann", ""]
    ws.append(sample)
    for cell in ws[2]:
        cell.font = Font(italic=True, color="000000")

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
    data_rows = []
    for r in rows[1:]:
        row_dict = {headers[i]: (str(v).strip() if v is not None else "") for i, v in enumerate(r)}
        company = row_dict.get("Company", "").strip()
        # skip blanks, the template example row, and stray pasted header rows
        if company and "Example" not in company and company.lower() != "company":
            data_rows.append(row_dict)

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

    # Backfill language and list for rows written before those columns existed.
    for row in rows:
        if not (row.get("language") or "").strip():
            row["language"] = language_for(row.get("country", ""))
        if not (row.get("list") or "").strip():
            row["list"] = list_for(row.get("type", ""))

    def fill_sheet(ws, sheet_rows):
        make_header(ws, [OUTPUT_DISPLAY.get(c, c.replace("_", " ").title()) for c in all_cols])
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(len(all_cols))}1"

        for row in sheet_rows:
            def _fmt(c, v):
                if c == "score":
                    try:
                        return int(str(v).replace("/100", "").strip())
                    except (ValueError, AttributeError):
                        return v
                return v
            ws.append([_fmt(c, row.get(c, "")) for c in all_cols])
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
                    cell.font = Font(color="000000")

        for col_idx, col_name in enumerate(all_cols, start=1):
            ws.column_dimensions[get_column_letter(col_idx)].width = OUTPUT_WIDTHS.get(col_name, 18)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "All LPs"
    fill_sheet(ws, rows)

    # Tabs mirror the folder layout: one per list, then one per language bucket.
    per_list = {}
    for name in LISTS:
        subset = [r for r in rows if r.get("list") == name]
        if subset:
            fill_sheet(wb.create_sheet(name), subset)
            per_list[name] = len(subset)

    per_lang = {}
    for code in LANGUAGES:
        subset = [r for r in rows if r.get("language") == code]
        if subset:
            fill_sheet(wb.create_sheet(code.upper()), subset)
            per_lang[code] = len(subset)

    _add_score_legend(wb)
    wb.save(OUTPUT_XLSX)

    active  = sum(1 for r in rows if r.get("stage") != "skip")
    skipped = len(rows) - active
    print(f"Exported {len(rows)} rows → {OUTPUT_XLSX}  ({active} active, {skipped} skipped)")
    print("Tabs: All LPs, "
          + ", ".join(f"{k} ({n})" for k, n in per_list.items()) + ", "
          + ", ".join(f"{c.upper()} ({n})" for c, n in per_lang.items()))
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

    # Load stages + scores + country from output.csv.
    # Keyed on (company, country), because company alone is not unique: two rows
    # are both "Eurolife FFH" (Greece and Romania) and matching on the name only
    # let the Romanian row's stage overwrite the Greek one's "sent".
    out_data, out_by_name, ambiguous = {}, {}, set()
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter=";"):
                name = r.get("company", "").strip().lower()
                info = {"stage": r.get("stage", ""), "score": r.get("score", ""),
                        "country": r.get("country", "")}
                info["contact_name"] = r.get("contact_name", "")
                info["contact_email"] = r.get("contact_email", "")
                out_data[(name, info["country"].strip().lower())] = info
                if name in out_by_name:
                    ambiguous.add(name)
                out_by_name[name] = info
    if ambiguous:
        print(f"note: {len(ambiguous)} company name(s) appear more than once, "
              f"matched on company+country: {', '.join(sorted(ambiguous))}")

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
        row_country = (r.get("Country", "") or "").strip().lower()
        info = out_data.get((company.lower(), row_country))
        if info is None:
            # No country on the import row, or it disagrees. Fall back to the
            # name, which is exact for every company that appears only once.
            info = out_by_name.get(company.lower(), {})
        stage   = info.get("stage", "imported")
        score   = info.get("score", "")
        # Use country from output.csv if import row has none
        country = r.get("Country", "") or info.get("country", "")

        # Carry verified contact data back from the tracker. output.csv is the
        # source of truth once research and verification have run, and the import
        # file is a first draft: it had PZU SA and PZU OFE sharing one contact,
        # and none of this session's corrections would otherwise reach input.xlsx.
        first, last = r.get("First Name", ""), r.get("Last Name", "")
        email = r.get("Email address", "")
        tracked_name = (info.get("contact_name") or "").strip()
        tracked_mail = (info.get("contact_email") or "").strip()
        placeholder = lambda v: (not v) or "FIND" in v.upper() or v.startswith("[")
        if tracked_name and not placeholder(tracked_name):
            parts = tracked_name.split()
            if len(parts) >= 2:
                first, last = " ".join(parts[:-1]), parts[-1]
            else:
                first, last = tracked_name, ""
        if tracked_mail and not placeholder(tracked_mail):
            email = tracked_mail.split("/")[0].strip()

        score_int = _to_int(score)
        row_vals = [
            country,
            r.get("Type", ""),
            company,
            r.get("Website", ""),
            first,
            last,
            r.get("Title", ""),
            email,
            r.get("LinkedIn", r.get("Linkedin ", "")),
            r.get("Considered", ""),
            stage,
            score_int if score_int else score,
        ]
        ws.append(row_vals)
        row_idx   = ws.max_row
        bg, fg    = STAGE_COLORS_INPUT.get(stage, ("FFFFFF", "000000"))
        stage_col = len(INPUT_COLS) + 1   # Stage column (1-indexed)
        score_col = len(INPUT_COLS) + 2   # Score column (1-indexed)

        for col_idx, _ in enumerate(row_vals, start=1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top")
            if col_idx == stage_col:
                cell.fill = PatternFill("solid", fgColor=bg)
                cell.font = Font(color=fg)
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif col_idx == score_col:
                sfill, sfont = score_fill(score)
                cell.fill = sfill
                cell.font = sfont
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif stage == "skip":
                cell.font = Font(color="000000")

    _add_instructions(wb)
    wb.save(INPUT_XLSX)

    counts = {}
    for r in import_rows:
        name = r.get("Company", "").strip().lower()
        country = (r.get("Country", "") or "").strip().lower()
        info = out_data.get((name, country)) or out_by_name.get(name, {})
        s = info.get("stage", "imported")
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
            Font(color="000000") if text.startswith("  ") else Font()
        )
    ws.column_dimensions["A"].width = 72


# ── VERIFY-EXPORT — scan output.csv for VERIFY/FIND items → verify.xlsx ───────
def _needs_verify(value):
    """Return True if a field value contains a VERIFY or FIND: marker."""
    if not value:
        return False
    v = str(value).upper()
    return "VERIFY" in v or "FIND:" in v


def cmd_verify_export():
    if not OUTPUT_CSV.exists():
        print(f"output.csv not found at {OUTPUT_CSV}")
        sys.exit(1)

    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        out_rows = list(csv.DictReader(f, delimiter=";"))

    # Preserve any previously confirmed values from existing verify.csv
    existing = {}
    if VERIFY_CSV.exists():
        with open(VERIFY_CSV, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter=";"):
                key = (r.get("slug", ""), r.get("field", ""))
                existing[key] = r

    verify_rows = []
    for row in out_rows:
        slug    = row.get("slug", "")
        company = row.get("company", "")
        for field_key, display_field, affects_score in VERIFY_FIELDS:
            value = row.get(field_key, "")
            if _needs_verify(value):
                key  = (slug, field_key)
                prev = existing.get(key, {})
                verify_rows.append({
                    "company":       company,
                    "slug":          slug,
                    "field":         field_key,
                    "display_field": display_field,
                    "current_value": value,
                    "verified_value": prev.get("verified_value", ""),
                    "source":        prev.get("source", ""),
                    "affects_score": "yes" if affects_score else "no",
                    "status":        prev.get("status", ""),
                })

    # Write backing CSV
    VERIFY_CSV.parent.mkdir(exist_ok=True)
    with open(VERIFY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=VERIFY_CSV_COLS, delimiter=";",
                                extrasaction="ignore")
        writer.writeheader()
        for r in verify_rows:
            writer.writerow(r)

    # Write user-editable XLSX
    EDITABLE_FILL = PatternFill("solid", fgColor="FFFACD")   # light yellow
    SCORE_FLAG    = PatternFill("solid", fgColor="FFEB9C")   # amber

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Verify"
    make_header(ws, VERIFY_XLSX_HEADERS)
    ws.freeze_panes = "A2"
    for i, w in enumerate(VERIFY_WIDTHS, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    for vr in verify_rows:
        ws.append([
            vr["company"], vr["slug"], vr["field"], vr["display_field"],
            vr["current_value"], vr["verified_value"], vr["source"],
            vr["affects_score"], vr["status"],
        ])
        row_idx = ws.max_row
        for col_idx in range(1, 10):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=(col_idx in (5, 6)))
            if col_idx in (6, 7, 9):          # user fills these
                cell.fill = EDITABLE_FILL
            if col_idx == 8 and vr["affects_score"] == "yes":
                cell.fill = SCORE_FLAG
                cell.font = Font(color="9C5700", bold=True)

    # Instructions sheet
    inst = wb.create_sheet("Instructions")
    lines = [
        ("HOW TO USE THIS FILE", True),
        ("1. Fill in 'Your Verified Value' (column F) with the confirmed fact.", False),
        ("2. Add the source URL or document name in 'Source' (column G).", False),
        ("3. Set 'Status' (column I) to 'done' when the value is confirmed.", False),
        ("4. Save this file.", False),
        ("", False),
        ("THEN IN CLAUDE CODE:", True),
        ("5. Run:  .venv/bin/python scripts/convert.py verify-import", False),
        ("   This patches data/output.csv with your confirmed values.", False),
        ("6. Claude will tell you which LPs need /rescore after the update.", False),
        ("", False),
        ("AFFECTS SCORE column:", True),
        ("  yes = this field feeds into the scoring rubric — run /rescore after confirming", False),
        ("  no  = informational only — no rescore needed", False),
    ]
    for i, (text, bold) in enumerate(lines, start=1):
        cell = inst.cell(row=i, column=1, value=text)
        cell.font = Font(bold=True, size=11) if bold else Font()
    inst.column_dimensions["A"].width = 76

    wb.save(VERIFY_XLSX)

    score_count = sum(1 for r in verify_rows if r["affects_score"] == "yes")
    print(f"Found {len(verify_rows)} items to verify → {VERIFY_XLSX}")
    print(f"Backing CSV: {VERIFY_CSV}")
    if score_count:
        print(f"  {score_count} items affect scoring — run /rescore for each after confirming")
    print("Fill in 'Your Verified Value' + 'Source', set Status=done, then run verify-import.")


# ── VERIFY-IMPORT — read verify.xlsx confirmed rows → patch output.csv ─────────
def cmd_verify_import():
    if not VERIFY_XLSX.exists() and not VERIFY_CSV.exists():
        print("No verify file found. Run:  .venv/bin/python scripts/convert.py verify-export")
        sys.exit(1)

    # Prefer xlsx (user edits there); fall back to csv
    verify_rows = []
    if VERIFY_XLSX.exists():
        wb = openpyxl.load_workbook(VERIFY_XLSX, data_only=True)
        ws = wb["Verify"]
        raw = list(ws.iter_rows(values_only=True))
        if len(raw) < 2:
            print("No data rows in verify.xlsx.")
            return
        headers = [str(h).strip() if h else "" for h in raw[0]]
        xlsx_to_csv = {
            "Company": "company", "Slug": "slug", "Field": "field",
            "What to Verify": "display_field", "Current Value": "current_value",
            "Your Verified Value": "verified_value", "Source": "source",
            "Affects Score": "affects_score", "Status": "status",
        }
        for r in raw[1:]:
            d = {headers[i]: (str(v).strip() if v is not None else "") for i, v in enumerate(r)}
            verify_rows.append({xlsx_to_csv.get(k, k): v for k, v in d.items()})
    else:
        with open(VERIFY_CSV, newline="", encoding="utf-8") as f:
            verify_rows = list(csv.DictReader(f, delimiter=";"))

    # Only rows marked done with a confirmed value
    actionable = [r for r in verify_rows
                  if r.get("status", "").strip().lower() == "done"
                  and r.get("verified_value", "").strip()]

    if not actionable:
        print("No rows marked 'done' with a verified value. Nothing to import.")
        return

    if not OUTPUT_CSV.exists():
        print(f"output.csv not found at {OUTPUT_CSV}")
        sys.exit(1)

    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        reader    = csv.DictReader(f, delimiter=";")
        out_rows  = list(reader)
        fieldnames = reader.fieldnames or OUTPUT_COLS

    # Build patch map: slug → {field: verified_value}
    patches: dict[str, dict] = {}
    rescore_slugs: list[str] = []
    for r in actionable:
        slug  = r.get("slug",  "").strip()
        field = r.get("field", "").strip()
        val   = r.get("verified_value", "").strip()
        if slug and field and val:
            patches.setdefault(slug, {})[field] = val
            if r.get("affects_score", "").strip().lower() == "yes":
                if slug not in rescore_slugs:
                    rescore_slugs.append(slug)

    patched_companies = []
    for row in out_rows:
        slug = row.get("slug", "").strip()
        if slug in patches:
            for field, val in patches[slug].items():
                row[field] = val
            patched_companies.append(row.get("company", slug))

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";",
                                extrasaction="ignore")
        writer.writeheader()
        for row in out_rows:
            writer.writerow(row)

    # Update verify.csv status to "done" for patched rows
    for r in verify_rows:
        slug  = r.get("slug",  "")
        field = r.get("field", "")
        if slug in patches and field in patches.get(slug, {}):
            r["status"] = "done"

    with open(VERIFY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=VERIFY_CSV_COLS, delimiter=";",
                                extrasaction="ignore")
        writer.writeheader()
        for r in verify_rows:
            writer.writerow(r)

    print(f"Patched {len(patched_companies)} LP(s) in output.csv:")
    for c in patched_companies:
        print(f"  - {c}")

    if rescore_slugs:
        # Find company names for display
        slug_to_company = {r.get("slug", ""): r.get("company", "") for r in out_rows}
        print("\nThese LPs have score-affecting changes — run /rescore for each:")
        for slug in rescore_slugs:
            print(f"  /rescore {slug_to_company.get(slug, slug)}")
    else:
        print("\nNo score-affecting changes — no rescore needed.")

    print(f"\nRun:  .venv/bin/python scripts/convert.py export   to regenerate output.xlsx")


# ── Entry point ───────────────────────────────────────────────────────────────
COMMANDS = {
    "init":          cmd_init,
    "import":        cmd_import,
    "export":        cmd_export,
    "sync":          cmd_sync,
    "verify-export": cmd_verify_export,
    "verify-import": cmd_verify_import,
}

def _strip_program(argv):
    """Drop --program (already consumed by program.py) so the command still parses."""
    out, skip = [], False
    for a in argv:
        if skip:
            skip = False
            continue
        if a == "--program":
            skip = True
            continue
        if a.startswith("--program="):
            continue
        out.append(a)
    return out


if __name__ == "__main__":
    print(f"programme: {program.label()}")
    sys.argv = [sys.argv[0]] + _strip_program(sys.argv[1:])
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        print(f"Available commands: {', '.join(COMMANDS)}")
        sys.exit(1)
    COMMANDS[sys.argv[1]]()

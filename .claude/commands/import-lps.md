The user only ever touches input.xlsx and output.xlsx. All CSVs are internal
mid-steps — never ask the user to edit or look at them.

STEP 0 — ALWAYS run the converter first so input.xlsx is picked up:
  .venv/bin/python scripts/convert.py import
This converts input.xlsx → data/lp-import.csv, preserving Considered=yes on
rows already processed. If it fails (missing venv/openpyxl), report the error
and stop.

STEP 1 — Read data/lp-import.csv and process ALL rows where considered = no
(or blank). Import every row — duplicates and shared contacts included. Never
skip a row. If a row looks like a duplicate of an existing LP or shares a
contact with another row, still import it and put a short warning in the
output.csv flag column (e.g. "likely duplicate of X — do not contact
separately", "shares contact with Y — one email max").

For each unprocessed row:
1. Create /lps/<lp-slug>.md using the supplied data (no web search needed):
   - slug = company name lowercased, diacritics stripped, periods/commas
     removed, spaces replaced with hyphens
   - Fill Data section from the row fields
   - Contacts section from first_name, last_name, title, email, linkedin
   - Leave Investment Strategy, Recent Activity, Bridge Candidates blank with [TO BE WRITTEN — run /research]
   - Summary: [TO BE WRITTEN — run /research or fill manually]
   - Score: [UNSCORED]
2. Add row to data/output.csv (stage=imported, score blank).
3. Mark the row as considered=yes in data/lp-import.csv.

STEP 2 — ALWAYS regenerate the Excel files the user works with:
  .venv/bin/python scripts/convert.py export   # data/output.csv → output.xlsx
  .venv/bin/python scripts/convert.py sync     # stage/score → input.xlsx
Run both even if zero rows were imported, so the Excel files always reflect
the current pipeline. If input.xlsx or output.xlsx is open in Excel, the save
may still succeed but the user must close and reopen the file to see changes —
mention this in the summary.

After processing, print a summary table: company | slug | contact | status
(include any duplicate/shared-contact flags in status).
Do not run web searches. Do not draft emails. Import only.

INTERNAL DATA FILE: data/output.csv — semicolons (;) as delimiter. No semicolons inside field values.
Columns: country;language;type;list;company;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent
Score is a plain integer 1-100 (not "90/100").

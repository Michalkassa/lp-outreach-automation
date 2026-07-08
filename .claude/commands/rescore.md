Recalculate the LP score for the company in $ARGUMENTS using the full 6-layer rubric.

1. Read `data/output.csv` — find the row for this LP (match on company name or slug).
2. Read `/lps/<lp-slug>.md` — extract all known facts about the LP.
3. Read `RESEARCH_REQUIREMENTS.md` — apply the 6-layer heuristic in full:
   - Layer 1: AUM / Ability to Write the Cheque (★★★★★ CRITICAL)
   - Layer 2: Alternatives / Private Credit Exposure (★★★★★ CRITICAL)
   - Layer 3: Investment Priority Alignment (★★★★ VERY IMPORTANT)
   - Layer 4: Operational Fit — local decisions + named contact (★★★★ VERY IMPORTANT)
   - Layer 5: Mandate / Regulatory Fit (★★★ IMPORTANT)
   - Layer 6: Values / ESG / Long-term Hook (★★ SLIGHT CONSIDERATION)
4. Start at 50. Apply each adjustment from the heuristic table. Run the sanity checks:
   - Score >75 requires confirmed alternatives AND local contact. If either is missing, cap at 74.
   - Score <25 requires a hard blocker. If none, floor at 25.
   - If both AUM and alternatives are unconfirmed, cap at 55.
5. Show your working: one bullet per layer with the signal found and adjustment applied.
   State the final score and why.
6. Update `data/output.csv`: write the new integer score (1–100, no "/100") in the score column
   for this LP's row. Do not change any other field unless the LP file contradicts a flag or
   category and you are certain the correction is warranted.
7. Print: "Score updated: <company> → <old_score> → <new_score>".
   Remind the user to run `export` if they want output.xlsx refreshed:
   `.venv/bin/python scripts/convert.py export`

DATA FILE: data/output.csv — semicolons (;) as delimiter. No semicolons inside field values.
Columns: country;type;company;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent
Score is a plain integer 1-100 (not "90/100").

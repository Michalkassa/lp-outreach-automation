Draft the one-time first-touch email for the LP in $ARGUMENTS.

1. Read /lps/<lp-slug>.md (if missing, offer /research and stop),
   templates/voice.md, templates/learnings.md. Apply learnings.
2. Write 3 draft variations (A, B, C) each using a different bridge
   angle from the LP file's Bridge Candidates section. Each draft must:
   - Follow the structure in voice.md (intro / bullets / close)
   - 200 to 230 words (body only, not subject/salutation/sign-off)
   - Plain, direct language — no corporate filler, no contractions
   - No political or religious statements
   - Address the primary contact from the LP file
3. Run the QA list in voice.md silently; fix fails before showing.
   Show pass/fail table after drafts.
4. Save each to /drafts/YYYY-MM-DD-<lp-slug>-A.md, -B.md, -C.md
   with frontmatter: lp, contact, bridge, category_label, word_count.
5. output.csv: stage=drafted. Note 3 drafts saved, nothing sent.

DATA FILE: data/output.csv — semicolons (;) as delimiter. No semicolons inside field values.
Columns: company;country;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent

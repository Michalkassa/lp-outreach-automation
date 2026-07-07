Log a manual send for the LP in $ARGUMENTS.

1. Ask me to paste the FINAL version I sent (or confirm the draft went
   unchanged) and the date.
2. Save it to /sent/YYYY-MM-DD-<lp-slug>.md with frontmatter: lp,
   contact, bridge, category_label, edits: none|minor|major.
3. output.csv: stage=sent, date_sent filled.
4. If I edited the draft, suggest running /calibrate.

OUTPUT.CSV FORMAT: output.csv uses semicolons (;) as delimiter.
Columns: company;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent

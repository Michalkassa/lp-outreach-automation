Log a manual send for the LP in $ARGUMENTS.

1. Ask me to paste the FINAL version I sent (or confirm the draft went
   unchanged) and the date.
2. Save it to /sent/<language>/YYYY-MM-DD-<lp-slug>.md with frontmatter:
   lp, to, contact, bridge, category_label, edits: none|minor|major,
   date_sent, language.
   <language> is the LP's `language` column in output.csv (en, sk or de), so
   the sent archive mirrors the drafts/<language>/ buckets. The slug must match
   output.csv exactly — /calibrate and the consistency check pair drafts to
   sent files on slug, and a shortened slug makes the record invisible to both.
   - `to` = the recipient email address the message was sent to. Carry it
     over from the draft's `to:` field. If the draft has none, use the
     `contact_email` column from output.csv for this LP. Never drop it —
     the sent record must always show where it was sent.
3. Also generate /sent/<language>/YYYY-MM-DD-<lp-slug>.html — the paste-ready
   twin of the sent email (mirror the draft's `.html`): a grey "To: /
   Subject:" reference header, then the body with the three metric labels
   (Track Record / Current Dynamics / Target Returns, or the SK/DE
   equivalents) bold and rendered as a real <ul> bullet list, Calibri 11.
   Render it faithfully from the sent text — do not alter wording.
4. output.csv: stage=sent, date_sent filled. Then refresh both workbooks:
     .venv/bin/python scripts/convert.py export
     .venv/bin/python scripts/convert.py sync
   Do NOT delete the draft files. Move them to
   .archive/sent-drafts-for-calibration/ instead, keeping the folder structure,
   so /drafts/ shows only pending work while /calibrate can still diff them.
5. If I edited the draft, suggest running /calibrate.

DATA FILE: data/output.csv — semicolons (;) as delimiter. No semicolons inside field values.
Columns: country;language;type;list;company;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent
Score is a plain integer 1-100 (not "90/100").

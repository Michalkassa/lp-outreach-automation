Read /data/lp-import.csv and process all rows where considered = no (or blank).

For each unprocessed row:
1. Create /lps/<lp-slug>.md using the supplied data (no web search needed):
   - slug = company_name lowercased, spaces replaced with hyphens
   - Fill Data section from the row fields
   - Contacts section from first_name, last_name, title, email, linkedin
   - Leave Investment Strategy, Recent Activity, Bridge Candidates blank with [TO BE WRITTEN — run /research]
   - Summary: [TO BE WRITTEN — run /research or fill manually]
   - Score: [UNSCORED]
2. Add row to output.csv (stage=imported, score blank).
3. Mark the row as considered=yes in data/lp-import.csv.

After processing, print a summary table: company | slug | contact | status.
Do not run web searches. Do not draft emails. Import only.

DATA FILE: data/output.csv — semicolons (;) as delimiter. No semicolons inside field values.
Columns: country;company;type;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent
Score is a plain integer 1-100 (not "90/100").

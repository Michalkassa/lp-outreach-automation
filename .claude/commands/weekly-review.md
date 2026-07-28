Run a pipeline review.

1. Run: .venv/bin/python scripts/pipeline_status.py
   It reads data/output.csv — the single source of truth for the pipeline.
   (crm/pipeline.csv is a retired v1 stub. Do not read it.)
2. Report tightly:
   a. Funnel: count per stage (research / drafted / sent); week-over-week
      change vs the latest crm/snapshots/ file if present.
   b. Which bridges are converting — read category_label and bridge from
      /sent/ frontmatter and group the sent emails by them. We do not track
      replies in the tracker, so report send mix, not a reply rate, unless
      I have told you a reply came in.
   c. Days since send — informational aging list only. We never follow up.
   d. Consistency: relay the CONSISTENCY block from the script verbatim if
      it is not "all clear". Those are real state bugs and block clean work.
   e. Stale research: /lps/ files >60 days old still in research/drafted.
3. Snapshot: copy data/output.csv to crm/snapshots/YYYY-MM-DD.csv.
4. Max 3 data-backed suggestions (e.g. which bridge style to use more).

Run a pipeline review.

1. Read /crm/pipeline.csv in full. Also run: python3 scripts/pipeline_status.py
2. Report tightly:
   a. Funnel: count per stage; week-over-week change vs latest
      crm/snapshots/ file if present.
   b. Reply rate on sent emails — overall, by segment, and by bridge_hook
      and category_label (pull from /sent/ frontmatter). Which bridges
      are converting?
   c. Awaiting reply: sent >21 days ago with no reply — informational
      aging list only (we do not send follow-ups).
   d. Replied but no next_action set — needs my response.
   e. Stale research: /lps/ files >60 days old still in research/drafted.
3. Snapshot: copy pipeline.csv to crm/snapshots/YYYY-MM-DD.csv.
4. Max 3 data-backed suggestions (e.g. which bridge style to use more).

# TUTORIAL — how to run the LP outreach loop

The rhythm in one line:
research 5-10 LPs → draft them → /review-packet → supervisor session
(he edits and sends) → /log-sent everything → /calibrate → next batch.

tracker.csv is the at-a-glance overview of every LP and its stage
(research / drafted / sent). Open it in Excel whenever the supervisor
asks where things stand.

---

## Phase 0 — One-time setup (10 minutes, done once)

1. Install Claude Code: `npm install -g @anthropic-ai/claude-code`
   (requires Node.js).
2. Put this folder somewhere permanent (e.g. Documents). The folder IS
   the system. Every file in it is the memory.
3. Open a terminal in the folder and run `claude`. It reads CLAUDE.md
   automatically and knows the whole workflow.
4. Skim CLAUDE.md once and confirm the fund facts and sender details
   are correct. These are copied verbatim into every email, so a wrong
   number here is a wrong number everywhere.
5. Recommended: run `git init` in the folder so every draft and every
   change is versioned.

## Phase 1 — Research (you, ~10 min per LP, batch of 5-10)

6. Take the next names from the outreach list. For each:
   `/research <Company Name>`
7. Claude searches the web and writes a context file to /lps/ with:
   - the company: type, AUM, mandate in their own words, recent
     activity, fit score 1-5
   - 2-3 named contact people, ranked, with titles and sources
   - 3 ranked bridge candidates (the fact that becomes sentence two)
   - the category label to use
8. Your job: read the file for 2 minutes.
   - Verify the primary contact is real (quick LinkedIn check).
   - Confirm the email address if Claude marked it FIND.
   - Sanity-check the #1 bridge: is it true and specific?
   - Add anything you know that is not public.
   - Fit score 1-2 → skip the LP and move on.

## Phase 2 — Drafting (Claude ~1 min per LP; you review 2 min each)

9. For each researched LP: `/draft <Company Name>`
10. Claude reads the context file + templates/voice.md +
    templates/learnings.md, writes the email on the fixed skeleton,
    runs the 9-point QA check on itself, and saves the draft to
    /drafts/ with the date and LP name.
11. Your job: read the draft once, aloud if possible. Only three things
    vary per email — the bridge sentence, the category label, and the
    salutation — so that is where you look. If the bridge feels
    generic, say "the bridge is weak, use candidate #2 instead" and
    Claude regenerates. Fix small things directly in the file if that
    is faster.
12. Repeat 9-11 until the agreed batch size is ready (say 10-15 drafts).

## Phase 3 — Supervisor review session

13. Run `/review-packet`. Claude compiles every pending draft into ONE
    document: a summary table up top for a fast skim, then each email
    numbered and ordered by fit score, with the contact, the bridge and
    its source (so the supervisor can verify the personalization is
    factual in seconds), and a blank "Supervisor notes:" line under each.
14. Sit down with the supervisor and go through the packet. He edits
    what he wants and HE sends, from his mailbox, deck attached. The
    system never touches sending and neither do you.

Tip: bring the packet, not a laptop full of files. The one-document
format is designed so the supervisor can clear 15 drafts in 20 minutes.

## Phase 4 — Logging (you, ~1 min per email, same day as the session)

15. Run `/log-sent` for each email (or the batch). For each one, paste
    the FINAL version as actually sent — or say "unchanged" — plus the
    date. Claude stores it in /sent/, marks edits none/minor/major and
    whether they came from you or the supervisor, and sets the tracker
    row to `sent`.
16. If the supervisor rejected a draft, say so. It goes back to
    `research` stage with a note on why, instead of silently
    disappearing.
17. Do not skip or postpone this step. The final sent versions are the
    fuel for the self-correction. Without them the system never improves.

## Phase 5 — Calibration (Claude, run after each logged batch)

18. Run `/calibrate`. Claude diffs every sent version against its own
    original draft and looks for patterns: words the supervisor always
    cuts, how bridges get rewritten, length trims, tone shifts.
    - Seen 2+ times → becomes a rule in templates/learnings.md
    - Seen once → hypothesis, applied softly
    - Seen 3+ times → Claude proposes a permanent one-line change to
      templates/voice.md and waits for an explicit yes
19. Every future /draft reads learnings.md first. Batch 2 is drafted
    the way batch 1 was edited; batch 3 the way batch 2 was edited.
    The number of supervisor changes should shrink each round, and
    /calibrate reports the trend (e.g. "sent unchanged: 4 of 12 → 9 of 14").

---

## Command reference

/research <LP>    LP context file: company info + 2-3 named contacts
/draft <LP>       one email draft file in /drafts/ for review
/review-packet    all pending drafts compiled into one supervisor document
/log-sent <LP>    store the final sent version(s), update tracker.csv
/calibrate        learn from the edits, update learnings.md

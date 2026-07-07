# Tutorial — LP Outreach Pipeline, Valori Capital

This is the full walkthrough. For a quick reference, see README.md.

---

## Phase 0 — One-time setup

1. Install Node.js from https://nodejs.org (LTS version).
2. Install Claude Code:
   ```
   npm install -g @anthropic-ai/claude-code
   ```
3. Install Python dependencies (inside this folder):
   ```
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```
4. Open a terminal in this folder, type `claude`. On first run it will ask
   you to log in in the browser.
5. Open `CLAUDE.md` and verify the FUND FACTS section is correct.
   Every number here goes verbatim into every email. Wrong number here =
   wrong number everywhere.
6. Optional but recommended: `git init` — every file change becomes
   recoverable.

---

## Phase 1 — Add prospects to input.xlsx

`input.xlsx` is your input sheet. Add one row per LP contact.

**Columns:**
| Column | What to fill |
|---|---|
| Company | Full legal name |
| Website | Company website |
| First Name / Last Name | Contact person |
| Title | Their exact job title |
| Email address | Confirmed email, or leave blank |
| LinkedIn | Profile URL |
| Considered | Leave blank for new rows. Set `yes` to skip on import. |
| Stage / Score | Auto-filled by `sync` — do not edit manually |

**Rules:**
- One row = one LP (not one company — if a company has two relevant
  contacts, add two rows).
- Leave Considered blank for any row you want Claude to process.
  Rows marked `yes` are skipped on the next import run.
- Save the file before running the import.

---

## Phase 2 — Import into the pipeline

After filling `input.xlsx`, run:

```
.venv/bin/python scripts/convert.py import
```

This reads `input.xlsx` and writes `lps/lp-import.csv` with semicolons as
delimiters. Rows already marked `Considered=yes` are preserved.

Then inside Claude:
```
/import-lps
```

Claude reads `lp-import.csv` and creates a stub `.md` file in `lps/` for
every new row. It does not run web searches at this stage — stubs contain
only the contact data you supplied.

---

## Phase 3 — Research

For each LP you want to research, inside Claude:
```
/research <Company Name>
```

Claude runs 3-5 web searches, fills the LP file with:
- Company data: type, AUM, regulator, ownership, alternatives allocation
- Investment strategy in their own words
- Recent activity (last 18 months)
- 2 named contacts with titles, emails, and why them
- 3 bridge candidates ranked (the hook for sentence 2 of the email)
- Score 1-100 with brief explanation in the Summary

Claude then updates `output.csv` (stage=research, score filled).

**Your job after each research (2 minutes):**
- Verify the primary contact is real — quick LinkedIn check.
- Confirm email if marked FIND.
- Check the #1 bridge is true and specific.
- Score < 35? Add to output.csv as skip and move on.

**Batch tip:** you can ask Claude to research multiple LPs at once:
"research the next 5 companies from lp-import.csv" — it will run them
sequentially.

---

## Phase 4 — Draft

For each researched LP (score ≥ 35):
```
/draft <Company Name>
```

Claude writes 3 variations (A, B, C) each using a different bridge angle.
Each draft:
- 200-230 words
- Follows the voice.md skeleton: intro / 3-4 bullets / values close
- No contractions, no religious statements, addressed to the primary contact
- Runs a QA checklist internally before showing you

Drafts are saved to `/drafts/YYYY-MM-DD-<slug>-A.md`, `-B.md`, `-C.md`.
`output.csv` is updated to stage=drafted.

**Your job (2 minutes per LP):**
- Read each draft once, aloud if possible.
- The only things that vary between emails: bridge sentence, category label,
  greeting. That is where to look.
- If the bridge feels generic: "use bridge candidate #2 instead."
- Edit the file directly if it is faster.
- Pick one draft (or merge two) as your send candidate.

---

## Phase 5 — Supervisor review and send

Run this before a review session:
```
/review-packet
```

Claude compiles all pending drafts into one document in `drafts/`, ordered
by score, with contact, bridge, and source for each.

**In the review session:**
- Supervisor reads, edits what he wants, and sends from his own mailbox
  with the deck attached.
- You do not send. Claude does not send. Max 5 emails per day.
- Best sending window: Tuesday-Thursday, 08:30-10:30 recipient local time.

---

## Phase 6 — Log what was sent

Same day, for each email sent:
```
/log-sent <Company Name>
```

Claude asks for the final version exactly as sent (or "unchanged") and the
date. It stores it in `/sent/`, marks edits as none/minor/major, and updates
`output.csv` to stage=sent.

**Do not skip or batch this for later.** The sent versions are the fuel for
calibration. Without them the system never improves.

---

## Phase 7 — Calibrate

After each logged batch (typically every 10-15 sends):
```
/calibrate
```

Claude diffs every sent version against its original draft, finds patterns:
- Seen 2+ times → becomes a rule in `templates/learnings.md`
- Seen 3+ times → Claude proposes a change to `voice.md` and waits for
  your explicit approval before touching it

Every future `/draft` reads `learnings.md` first. Batch 2 is drafted the
way batch 1 was edited. The share of drafts sent unchanged should rise each
round, and `/calibrate` reports the trend.

---

## Phase 8 — Export the pipeline view

At any time to get a fresh `output.xlsx`:
```
.venv/bin/python scripts/convert.py export
```

To update `input.xlsx` with current stages and scores from `output.csv`:
```
.venv/bin/python scripts/convert.py sync
```

---

## Full command reference

### Python (run from terminal)
| Command | Effect |
|---|---|
| `scripts/convert.py init` | Create blank `input.xlsx` template |
| `scripts/convert.py import` | `input.xlsx` → `lps/lp-import.csv` |
| `scripts/convert.py export` | `output.csv` → `output.xlsx` |
| `scripts/convert.py sync` | Pull stage + score into `input.xlsx` |

Prefix all with `.venv/bin/python` unless your venv is activated.

### Claude (type inside claude session)
| Command | Effect |
|---|---|
| `/import-lps` | Create stub `.md` files from `lp-import.csv` |
| `/research <LP>` | Full research + score, update `output.csv` |
| `/draft <LP>` | 3 email drafts (A/B/C) to `drafts/`, update `output.csv` |
| `/log-sent <LP>` | Store sent version, update `output.csv` to sent |
| `/calibrate` | Learn from edits, update `learnings.md` |

---

## Score scale

| Score | Meaning | Action |
|---|---|---|
| 75-100 | Top priority | Draft immediately |
| 55-74 | Strong prospect | Draft when ready |
| 35-54 | Medium | Verify key gaps first |
| 20-34 | Low | Keep on radar |
| < 20 | Skip | Regulatory barrier or AUM too small |

Scores use partial credit. A subsidiary of a group with confirmed
alternatives exposure scores 40-60, not zero. "Plausible based on entity
type" counts and is marked `[likely]` in the LP file.

---

## File locations

| File | Purpose |
|---|---|
| `input.xlsx` | Your prospect input sheet |
| `lps/lp-import.csv` | Auto-generated from input.xlsx, read by /import-lps |
| `lps/<slug>.md` | One research file per LP |
| `lps/_TEMPLATE.md` | Template structure for LP files |
| `output.csv` | Pipeline state, semicolon-delimited, updated by Claude |
| `output.xlsx` | Pipeline view, color-coded, generated by convert.py |
| `drafts/` | Draft emails (not sent) |
| `sent/` | Final sent emails, exact version |
| `templates/voice.md` | Email structure canon — do not edit without approval |
| `templates/learnings.md` | Learned edit patterns — updated by /calibrate only |
| `CLAUDE.md` | Fund facts, sender, rules — update fund numbers here |
| `RESEARCH_REQUIREMENTS.md` | Scoring rubric and segment guidance |

---

## What NOT to do

- Do not edit `voice.md` directly — propose the change and wait for approval.
- Do not edit `CLAUDE.md` directly — propose and wait.
- Do not send emails yourself — the supervisor sends from his mailbox.
- Do not skip `/log-sent` — it breaks calibration.
- Do not batch research a company that already has a researched `.md` file
  (score already assigned) — it will overwrite existing work. Check
  `output.csv` stage first.

# Tutorial — LP Outreach Pipeline, Valori Capital

This is the full step-by-step guide. For a quick reference, see README.md.

---

## Phase 0 — One-time setup

**Do this once before anything else.**

**1. Install Node.js**
Download from https://nodejs.org (LTS version). Install normally.

**2. Install Claude Code**
```
npm install -g @anthropic-ai/claude-code
```

**3. Install Python dependencies**
Open a terminal inside this folder and run:
```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

**4. Start Claude**
```
claude
```
On first run it will open a browser to log in. After that you are inside
a chat that can read and write all files in this folder.

**5. Verify fund facts**
Open `CLAUDE.md` and read the FUND FACTS section carefully.
Every number here goes verbatim into every email. Fix anything wrong
before running research — a wrong number here is a wrong number everywhere.

**6. Optional but recommended — version history**
```
git init
```
Every file change becomes recoverable.

---

## Phase 1 — Add prospects to input.xlsx

`input.xlsx` is your starting point. Add one row per LP contact.

**Columns to fill:**

| Column | What to fill |
|---|---|
| Company | Full legal name |
| Country | Country of the entity (drives email language — see below) |
| Website | Company website |
| First Name / Last Name | Contact person |
| Title | Their exact job title |
| Email address | Confirmed email, or leave blank |
| LinkedIn | Profile URL |
| Considered | Leave blank for new rows. Set `yes` to skip on next import. |
| Stage / Score | Auto-filled by `sync` — do not edit manually |

**Language is set automatically by country:**
- Slovakia, Czechia → Slovak
- Austria, Germany → German
- All other countries → English

To override for a specific LP permanently, add this to the LP's `.md` file under Data:
```
Language override: en
```
To override for a single draft run without saving anything:
```
/draft <Company Name> en
```
Valid codes: `en`, `sk`, `de`.

**Rules:**
- One row = one LP. If a company has two relevant contacts, add two rows.
- Leave Considered blank for any row you want Claude to process.
- Save the file before running the import.

---

## Phase 2 — Import into the pipeline

After filling `input.xlsx`, run this in the terminal:

```
.venv/bin/python scripts/convert.py import
```

This reads `input.xlsx` and writes `lps/lp-import.csv`. Rows already
marked `Considered=yes` are preserved and skipped.

Then inside Claude:
```
/import-lps
```

Claude reads `lp-import.csv` and creates a stub `.md` file in `lps/`
for every new row. No web searches yet — stubs contain only the contact
data you supplied. It also adds each LP to `output.csv` with stage=imported.

---

## Phase 3 — Research

For each LP you want to research, inside Claude:
```
/research <Company Name>
```

Claude runs web searches and fills the LP file with:
- Company type, AUM, regulator, ownership structure
- Investment strategy in their own words
- Recent activity (last 18 months)
- 2-3 named contacts with titles, emails, and why each one
- 3 bridge candidates ranked (the hook for sentence 2 of the email)
- Score 1-100 with brief working

Claude then updates `output.csv` with stage=research and the score.

**Your job after each research (2-3 minutes):**
- Verify the primary contact exists — quick LinkedIn check.
- Confirm email if marked `FIND:` (pattern given, address not confirmed).
- Check the top bridge is true, specific, and sourced.
- Score below 35? Note it in `output.csv` and move on — do not draft.

**Batch tip:** you can ask Claude to research multiple at once:
"research the next 5 companies from lp-import.csv"

**If a score looks wrong after research:**
```
/rescore <Company Name>
```
Claude re-applies the full 6-layer rubric and shows the working per layer.
This is useful after you verify new data (confirmed AUM, confirmed alternatives
allocation, etc.).

---

## Phase 4 — Verify contact data (optional but recommended before drafting)

After a research batch, some emails will be `FIND:` or `[VERIFY]`.
To manage these in bulk:

```
.venv/bin/python scripts/convert.py verify-export
```

This writes `verify.xlsx` — one row per field needing verification, with the
current value and a blank column for your corrected value. Fill it in,
then run:

```
.venv/bin/python scripts/convert.py verify-import
```

This applies your corrections back to `output.csv`. Fields that affect the
score are flagged in the sheet. Do this before drafting so the correct
contact name goes into the email.

---

## Phase 5 — Draft

For each researched LP with score 35 or above:
```
/draft <Company Name>
```

Claude writes up to 3 variations (A, B, C), each using a different
bridge angle from the LP file. Default is 3 — to get fewer, add a
number to the command:
```
/draft <Company Name> 2
/draft <Company Name> en 1     ← combinable with a language code
```
Or set it permanently for an LP in its `.md` file under Data:
```
Draft count: 2
```
Fewer drafts always use the highest-ranked bridge angles first.
Each draft:
- 200-230 words (body only, not subject line, salutation, or sign-off)
- Follows the voice.md structure: intro / 3-4 bullets / values close
- Written in the correct language based on the LP's country
- No contractions, no em-dashes, no Oxford commas
- Addressed to the primary contact from the LP file
- Runs the QA checklist internally before showing you

Drafts are saved to `/drafts/YYYY-MM-DD-<slug>-A.md`, `-B.md`, `-C.md`.
`output.csv` is updated to stage=drafted.

**Your job after drafting (2 minutes per LP):**
- Read each variation once.
- The bridge sentence (sentence 2 of the intro) is the only thing that
  makes this email different from a generic one. That is where to focus.
- If the bridge feels generic or too data-heavy, tell Claude to use a
  different angle, or edit the file directly.
- Pick one variation as your send candidate, or merge two.

---

## Phase 6 — Review

Before a review session with the supervisor, compile all pending drafts:
```
/review-packet
```

This creates `drafts/REVIEW-PACKET.md` — all current drafts in one document
with a summary table at the top (LP, bridge, word count per draft).
Easy to read on screen or print.

**In the review session:**
- Supervisor reads, edits what he wants, sends from his own mailbox
  with the deck attached.
- You do not send. Claude does not send.
- Max 5 emails per day to keep deliverability clean.
- Best window: Tuesday to Thursday, 08:30 to 10:30 recipient local time.
- Triple-check the surname spelling in the salutation before sending.

---

## Phase 7 — Log what was sent

Same day, immediately after each email is sent:
```
/log-sent <Company Name>
```

Claude will ask you to paste the final email exactly as sent, or say
"unchanged" if you sent the draft without edits. It also asks for the
send date.

Claude then:
- Saves the exact sent version to `/sent/YYYY-MM-DD-<slug>.md`
- Marks the frontmatter: `edits: none | minor | major`
- Updates `output.csv` to stage=sent with the date

**Do not skip or batch this for later.** The sent versions are what
calibration learns from. Without them the system never improves.

---

## Phase 8 — Calibrate (after every 5-10 sends)

```
/calibrate
```

Claude diffs every sent version against its matching draft and finds
patterns — words you remove, phrases you replace, bridges you rewrite,
length trims you make consistently. It applies this rule:

| Frequency | What happens |
|---|---|
| Seen once | Stored as a hypothesis in `learnings.md` — watched but not acted on |
| Seen 2+ times | Becomes a confirmed rule in `learnings.md` — applied to all future drafts |
| Seen 3+ times | Claude proposes the exact change to `voice.md` and waits for your yes |

After calibration, every `/draft` reads `learnings.md` first. The goal
is that the share of drafts sent unchanged rises batch by batch.

---

## Phase 9 — Weekly review (every Monday)

```
/weekly-review
```

Claude gives you:
- Funnel counts per stage and week-over-week change
- Reply rate overall, by segment, and by bridge style
- Emails sent more than 21 days ago with no reply (aging list — for awareness only, we do not follow up)
- Stale research: LP files older than 60 days still at research/drafted stage

Use the bridge reply rates to guide the next shortlist — prioritise LPs
where the best-performing bridge angle is available.

---

## Phase 10 — Export the pipeline view

At any time:
```
.venv/bin/python scripts/convert.py export
```

This reads `output.csv` and writes `output.xlsx` — color-coded by stage
and sorted by score. Your live view of the whole pipeline.

To pull current stage and score back into `input.xlsx`:
```
.venv/bin/python scripts/convert.py sync
```

---

## Full command reference

### Python (run from terminal, prefix with `.venv/bin/python`)

| Command | What it does |
|---|---|
| `scripts/convert.py init` | Create blank `input.xlsx` template |
| `scripts/convert.py import` | `input.xlsx` → `lps/lp-import.csv` |
| `scripts/convert.py export` | `output.csv` → `output.xlsx` |
| `scripts/convert.py sync` | Pull stage + score into `input.xlsx` |
| `scripts/convert.py verify-export` | Write `verify.xlsx` with fields needing verification |
| `scripts/convert.py verify-import` | Apply verified values from `verify.xlsx` to `output.csv` |

### Claude (type inside Claude session)

| Command | What it does |
|---|---|
| `/import-lps` | Create stub `.md` files from `lp-import.csv` |
| `/research <LP>` | Full research + score, update `output.csv` |
| `/rescore <LP>` | Recalculate score with 6-layer rubric, show working per layer |
| `/draft <LP>` | 1-3 email drafts (default 3) to `drafts/`, update `output.csv` |
| `/review-packet` | Compile all drafts into `drafts/REVIEW-PACKET.md` |
| `/log-sent <LP>` | Store sent version in `sent/`, update `output.csv` to sent |
| `/calibrate` | Learn from edits, update `learnings.md` |
| `/weekly-review` | Pipeline summary: funnel, reply rates, aging, stale research |

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
type" counts and is marked `[likely]` in the LP file. Full rubric in
`RESEARCH_REQUIREMENTS.md`.

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
| `verify.xlsx` | Verification checklist, generated by verify-export |
| `drafts/` | Draft emails (not sent) |
| `drafts/REVIEW-PACKET.md` | All current drafts compiled into one printable file |
| `sent/` | Final sent emails, exact version as sent |
| `templates/voice.md` | English email structure canon |
| `templates/voice-sk.md` | Slovak email structure canon |
| `templates/voice-de.md` | German email structure canon |
| `templates/learnings.md` | Learned edit patterns, updated by /calibrate only |
| `CLAUDE.md` | Fund facts, sender identity, rules — update fund numbers here |
| `RESEARCH_REQUIREMENTS.md` | Scoring rubric and segment guidance |

---

## What NOT to do

- Do not edit `voice.md`, `voice-sk.md`, `voice-de.md`, or `CLAUDE.md` directly.
  Tell Claude what you want changed — it will propose the edit and wait for your approval.
- Do not send emails yourself — the supervisor sends from his mailbox with the deck attached.
- Do not skip `/log-sent` — it breaks calibration. Log each send the same day.
- Do not research an LP that already has a researched `.md` file (check `output.csv` stage first)
  — it will overwrite existing work.
- Do not edit `output.csv` manually unless Claude instructs you to — it is the source of truth
  for the entire pipeline and formatting errors break the export.

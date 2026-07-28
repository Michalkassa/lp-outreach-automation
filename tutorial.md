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

This reads `input.xlsx` and writes `data/lp-import.csv`. Rows already
marked `Considered=yes` are preserved and skipped.

Then inside Claude:
```
/import-lps
```

Claude reads `lp-import.csv` and creates a stub `.md` file in `lps/`
for every new row. No web searches yet — stubs contain only the contact
data you supplied. It also adds each LP to `data/output.csv` with stage=imported.

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
- 3 bridge candidates ranked (the LP-specific hook for the email's opening)
- Score 1-100 with brief working

Claude then updates `data/output.csv` with stage=research and the score.

**Your job after each research (2-3 minutes):**
- Verify the primary contact exists — quick LinkedIn check.
- Confirm email if marked `FIND:` (pattern given, address not confirmed).
- Check the top bridge is true, specific, and sourced.
- Score below 35? Note it in `data/output.csv` and move on — do not draft.

**Batch tip:** you can ask Claude to research multiple at once:
"research the next 5 companies from lp-import.csv"

**If a score looks wrong after research:**
```
/rescore <Company Name>
```
Claude re-applies the full 8-layer rubric and shows the working per layer.
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

This applies your corrections back to `data/output.csv`. Fields that affect the
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
Each draft follows the current voice canon (structure v4 — see
`templates/voice.md`):
- A short reason-for-writing hook that names the fit (drawn from the LP's
  research, framed generally), never opening with the LP's company name
- A mid-motion line about the first vintage, with one genuine personal touch
- Three bold-labelled bullets: **Track Record**, **Current Dynamics**,
  **Target Returns**, then the deck line once and a short, confident close
- Body about 120–190 words, no em-dashes; correct language by country
  (English contractions light; German and Slovak stay formal)
- Runs the QA checklist internally before showing you

**Each drafted LP produces two files in its type folder under `drafts/`**
(`drafts/<lang>/<list>/`, e.g. `drafts/en/pension-funds/`, `drafts/de/insurance/`)**:**

| File | What it is |
|---|---|
| `YYYY-MM-DD-<slug>.md` | The editable source. Its frontmatter has `to:` (the recipient email) and the `Subject:` line sits just below. Edit wording here. |
| `YYYY-MM-DD-<slug>.html` | The Outlook paste-ready version. Bold labels and bullets are baked in so you never re-format by hand. Copy from here. |

(If you run `/draft` with variants A/B/C, each variant gets its own pair of
files. Pick one to load into Outlook.)

`data/output.csv` is updated to stage=drafted. Loading these into an actual
Outlook email draft is **Phase 7** below.

**Your job after drafting (2 minutes per LP):**
- Read the draft once.
- The **opening hook** (the LP-specific fact in the first one or two
  sentences) is the only thing that makes this email different from a generic
  one. That is where to focus. It should be true, specific, and not sendable
  to any other LP unchanged.
- The strategy paragraph, fund-status paragraph, and the three bold bullets
  are fixed blocks — they do not change per LP, so you do not need to re-read
  them each time.
- If the hook feels generic or presumptuous about their book, tell Claude to
  use a different angle, or edit the `.md` directly.
- If you ran variants (A/B/C), pick one to load into Outlook, or merge two.

---

## Phase 6 — Review

Before a review session with the supervisor, compile all pending drafts:
```
/review-packet
```

This creates one `REVIEW-PACKET.md` per type folder (for example
`drafts/en/REVIEW-PACKET.md`) — that type's current drafts in one document
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

## Phase 7 — Build the sending queue

Before touching Outlook, ask the system what is actually ready. This reads only.
It sends nothing and changes nothing.

```
.venv/bin/python scripts/send_queue.py --lang en
```

You get three groups:

```
unsent drafts matching filters : 15
  ready                        : 15
  held (shared recipient)      : 1
  blocked (failed a check)     : 0
  queued now                   : 14

HELD — same recipient as an earlier draft, send one email only
  [72] AZ Mandatory B Category  shares kristijan.buk@azfond.hr with AZ Mandatory Pension Fund

# 1/14  [86] AZ Mandatory Pension Fund  ->  kristijan.buk@azfond.hr
.venv/bin/python scripts/make_draft.py drafts/en/pension-funds/2026-07-22-az-mandatory-pension-fund.html
```

- **queued** — ready now, in score order, as commands you can paste
- **held** — two LPs share one contact (a CEO over both the carrier and the
  pension arm). One person gets one email. The highest-scoring entity is kept
  and the collision is named. Mark the other row skipped.
- **blocked** — failed a check, with the reason. These never reach the queue.

A draft is blocked when any of these is true:

| Problem | Meaning |
|---|---|
| `recipient is 'FIND'` | The address was never confirmed. Confirm it, fix `to:` in the `.md`, re-run `format_html.py` on that file. |
| `N bold bullet labels, expected 3` | The `**` markers are missing, so the labels paste flat. Fix the `.md`. |
| `subject uses a retired ending` | `first vintage` is retired. Regenerate the subject per `templates/caption.md`. |
| `missing the <lang> sign-off` | The sign-off does not match the draft's language. |

Useful flags:

| Flag | Effect |
|---|---|
| `--lang en\|sk\|de` | One language bucket |
| `--list insurance\|pension-funds` | One list |
| `--limit N` | How many to queue (default 5, the daily cap) |
| `--all` | Ignore the cap |
| `--script today.sh` | Write a runnable script instead of printing |

With `--script`, the file runs one compose window at a time and pauses between
each. That is required, not a convenience: Chromium allows a single process per
profile, so these cannot run in parallel.

```
.venv/bin/python scripts/send_queue.py --lang en --script today.sh
./today.sh
```

---

## Phase 8 — Send each draft

Run one command per LP, **from your own Terminal** — not from inside Claude Code.
In your terminal the script can pause and wait if your Outlook session has
expired; run from elsewhere and it cannot.

```
.venv/bin/python scripts/make_draft.py drafts/en/pension-funds/2026-07-22-az-mandatory-pension-fund.html
```

What happens:

1. A Chrome window opens on Outlook. **First run only:** log in. The session is
   saved to `.browser-profile/`, so every later run goes straight to a compose
   window.
2. It fills **To**, **Subject** and the **body**, with the three bold labels and
   the bullet list intact. Then it **stops**.
3. **Your turn:** read it, check the surname spelling, **attach the deck PDF**,
   and send by hand. The script never sends and never attaches anything.
4. Close the browser window.

It refuses to open a compose window at all if the recipient is `FIND`. That is
the guard working, not a bug.

**One browser at a time.** If a window from a previous run is still open you get:

```
error: another Chromium (pid 62452) is already using the profile
```

Close that window and run again, or use `--profile .browser-profile-2` for a
second independent session with its own login.

### If the body does not fill

Run the same command with `--inspect`. It opens the compose window, prints every
field it can see with its real tag and label, fills nothing, and stops. Send that
output to Claude.

```
.venv/bin/python scripts/make_draft.py <draft.html> --inspect
```

### Doing it by hand instead

The `.html` file is still a normal formatted email. Double-click it, select from
the salutation down to "Partner, Valori Capital", copy, paste into a new Outlook
message with **Keep Source Formatting**, then fill To and Subject from the `.md`
frontmatter. Use this if the browser automation is unavailable.

### Volume and timing

- Maximum **5 emails per day** to protect deliverability.
- Best window: **Tuesday–Thursday, 08:30–10:30** recipient local time.

---

## Phase 8b — Logging (automatic, one keystroke)

When you close the compose window, the script reads the body back out of it and
asks:

```
Did you send it to AZ Mandatory Pension Fund? [y/N]
```

Answer `y` and it:

- writes `sent/<lang>/YYYY-MM-DD-<slug>.md` and `.html`
- sets `stage=sent` and `date_sent` in the tracker
- records `edits: none | minor | major` by comparing what you sent against what
  was drafted

Anything other than `y` leaves the row as `drafted`, writes nothing, and the LP
stays in tomorrow's queue.

**Why it asks rather than assuming.** Closing a window is not proof an email went
out. You might close it after deciding not to send. A false `sent` removes that
LP from the pipeline permanently and silently — much more expensive than one
keystroke. Use `--no-log` to switch the prompt off.

**Why it reads the window rather than copying the draft.** Calibration learns
from the gap between what was drafted and what was actually sent. Copy the draft
into the sent record and that gap is always zero. Capturing the compose body
means edits you make inside Outlook are preserved, and `edits:` is real.

If something goes wrong, log it afterwards:

```
.venv/bin/python scripts/log_sent.py drafts/en/pension-funds/2026-07-22-az-mandatory-pension-fund.html
```

Logging twice is safe. A row already marked `sent` is left alone.

Sending from somewhere other than this script? Use `/log-sent <LP>` in Claude and
paste the final text.

---

## Phase 9 — Calibrate (after every 5-10 sends)

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

## Phase 10 — Weekly review (every Monday)

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

## Phase 11 — Export the pipeline view

At any time:
```
.venv/bin/python scripts/convert.py export
```

This reads `data/output.csv` and writes `output.xlsx` — color-coded by stage
and sorted by score. Your live view of the whole pipeline.

To pull current stage and score back into `input.xlsx`:
```
.venv/bin/python scripts/convert.py sync
```

---

## Full command reference

### Python (run from terminal, prefix with `.venv/bin/python`)

**Data in and out**

| Command | What it does |
|---|---|
| `scripts/convert.py init` | Create blank `input.xlsx` template |
| `scripts/convert.py import` | `input.xlsx` → `data/lp-import.csv` |
| `scripts/convert.py export` | `data/output.csv` → `output.xlsx` (tabs: All LPs, Insurance, Pension funds, EN, SK, DE) |
| `scripts/convert.py sync` | Pull stage + score into `input.xlsx` |
| `scripts/convert.py verify-export` | Write `verify.xlsx` with fields needing verification |
| `scripts/convert.py verify-import` | Apply verified values from `verify.xlsx` to `data/output.csv` |

Close `input.xlsx` and `output.xlsx` in Excel before running these — Excel locks
the file and the write fails.

**Checking and sending**

| Command | What it does |
|---|---|
| `scripts/pipeline_status.py` | Funnel, language split, send aging, and the consistency check |
| `scripts/send_queue.py` | Build the sending queue from unsent drafts |
| `scripts/send_queue.py --lang en --all` | Queue one language, no daily cap |
| `scripts/send_queue.py --script today.sh` | Write a runnable session script |
| `scripts/make_draft.py <draft.html>` | Open a filled Outlook compose window, then stop |
| `scripts/make_draft.py <draft.html> --inspect` | Dump the compose fields for debugging |
| `scripts/log_sent.py <draft.html>` | Record a send by hand if the prompt was missed |

**Rebuilding files**

| Command | What it does |
|---|---|
| `scripts/format_html.py --all` | Refresh every `.html` twin that is stale |
| `scripts/respace.py --all` | Apply the four paragraph breaks, rebuild the twins |
| `scripts/make_all_drafts.py --lang en --all` | Build an Outlook draft for every unsent English draft |
| `scripts/format_html.py <file.md>` | Refresh one twin after editing its `.md` |
| `scripts/build_packet.py` | Rebuild every review packet |
| `scripts/build_packet.py en` | Rebuild one language bucket's packets |

### Claude (type inside Claude session)

| Command | What it does |
|---|---|
| `/import-lps` | Create stub `.md` files from `lp-import.csv` |
| `/research <LP>` | Full research + score, update `data/output.csv` |
| `/rescore <LP>` | Recalculate score with 8-layer rubric, show working per layer |
| `/draft <LP>` | 1-3 email drafts (default 3) to `drafts/<lang>/<list>/`, update `data/output.csv` |
| `/review-packet [en\|sk\|de\|type]` | Packets per type, per language, and a roll-up |
| `/log-sent <LP>` | Store sent version in `sent/<lang>/`, update `data/output.csv` to sent |
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
| `data/lp-import.csv` | Auto-generated from input.xlsx, read by /import-lps |
| `lps/<slug>.md` | One research file per LP |
| `lps/_TEMPLATE.md` | Template structure for LP files |
| `data/output.csv` | Pipeline state, semicolon-delimited, updated by Claude |
| `output.xlsx` | Pipeline view, color-coded, generated by convert.py |
| `verify.xlsx` | Verification checklist, generated by verify-export |
| `drafts/` | Draft emails (not sent), split into one folder per LP type: `pension-funds/`, `insurance/`, and a new folder per new type |
| `drafts/<lang>/<list>/<slug>.md` | The editable source of each draft (`to:` + subject in the frontmatter) |
| `drafts/<lang>/<list>/<slug>.html` | The formatted, copy-into-Outlook version of each draft (bold labels + bullets baked in) |
| `drafts/<lang>/REVIEW-PACKET.md` | Every pending draft in that language — the file to print for a sending session |
| `sent/<lang>/` | Final sent emails, exact version as sent, bucketed by language |
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
- Do not research an LP that already has a researched `.md` file (check `data/output.csv` stage first)
  — it will overwrite existing work.
- Do not edit `data/output.csv` manually unless Claude instructs you to — it is the source of truth
  for the entire pipeline and formatting errors break the export.

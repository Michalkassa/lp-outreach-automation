# LP Outreach System — Valori Capital

A research and email-drafting system for LP cold outreach, running inside
**Claude Code**. Claude researches investors, scores them, writes draft emails,
and learns from your edits. A human sends every email manually — Claude never
touches a mailbox.

---

## What's in this folder

| File / folder | What it is |
|---|---|
| `CLAUDE.md` | Sender identity, fund facts, and system rules. Claude reads this automatically every session. |
| `input.xlsx` | **Your input.** Fill this with LP prospects. One row per contact. |
| `output.xlsx` | **Your output.** Color-coded pipeline view with scores, contacts, stage, and bridge hooks. |
| `data/output.csv` | Machine-readable version of output.xlsx, and the single source of truth for the pipeline. Updated automatically by Claude commands. |
| `data/lp-import.csv` | Semicolon-delimited import file read by `/import-lps`. Generated from input.xlsx. |
| `lps/` | One research file per LP. Created by `/import-lps`, enriched by `/research`. |
| `lps/_TEMPLATE.md` | Blank template structure for LP files. |
| `drafts/` | Email drafts waiting for review. Nothing here has been sent. Split by language, then by list. |
| `drafts/en/`, `drafts/sk/`, `drafts/de/` | One bucket per email language. Country decides the bucket. |
| `drafts/<lang>/pension-funds/` | Drafts from the **Pension funds** list, in that language. |
| `drafts/<lang>/insurance/` | Drafts from the **Insurance** list, in that language. These are the only two folders per bucket. |
| `drafts/<lang>/<list>/<slug>.md` | The editable source of a draft. Its frontmatter carries `to:` (recipient email) and the `Subject:` line. |
| `drafts/<lang>/<list>/<slug>.html` | The Outlook paste-ready version — bold labels and bullets baked in. This is the file you copy into Outlook. |
| `drafts/<lang>/REVIEW-PACKET.md` | **The file to print for a sending session** — every pending draft in that language. |
| `drafts/<lang>/<list>/REVIEW-PACKET.md` | That bucket-and-list's pending drafts. |
| `drafts/REVIEW-PACKET.md` | Roll-up across all languages. |
| `sent/<lang>/` | Final sent versions, exactly as sent, bucketed by language to mirror `drafts/`. |
| `templates/voice.md` | Email structure and style canon. Every English draft follows this. |
| `templates/voice-sk.md` | Slovak voice template — used for Slovakia and Czechia. |
| `templates/voice-de.md` | German voice template — used for Austria and Germany. |
| `templates/learnings.md` | Patterns Claude has learned from your edits. Updated by `/calibrate`. |
| `scripts/convert.py` | Python script — converts between xlsx and csv in both directions. |
| `scripts/send_queue.py` | Builds the sending queue: checks every unsent draft and prints the commands to run. |
| `scripts/log_sent.py` | Records a send: writes `sent/<lang>/` and flips the tracker row. Called automatically by `make_draft.py`. |
| `scripts/respace.py` | Opens up body spacing (four breaks) and rebuilds the `.html` twins. |
| `scripts/make_all_drafts.py` | Builds an Outlook draft for every unsent draft in one browser run. Never sends. |
| `RESEARCH_REQUIREMENTS.md` | What Valori looks for in an LP, scoring rubric, and segment notes. |
| `PIPELINE.md` | Manual outreach operating procedure. |
| `tutorial.md` | Full step-by-step walkthrough of the working rhythm. |
| `.claude/commands/` | Definitions of the slash commands. You never need to open these. |

---

## One-time setup (~15 minutes)

**1. Install Node.js**
Download from https://nodejs.org (LTS version). Install normally.

**2. Install Claude Code**
Open a terminal and run:
```
npm install -g @anthropic-ai/claude-code
```

**3. Install Python dependencies**
In the terminal, from inside this folder:
```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

**4. Open this folder in the terminal**
Type `cd `, then drag this folder into the terminal window. Press Enter.

**5. Start Claude**
```
claude
```
The first time it will ask you to log in in the browser. After that you are
inside a chat that can read and write all files in this folder.

**6. Verify fund facts**
Open `CLAUDE.md` and read the FUND FACTS section. These numbers go verbatim
into every email. Fix anything wrong before running research.

**7. (Optional but recommended) Turn on version history**
```
git init
```
Every change to every file becomes recoverable.

---

## The commands, in the order you run them

A full cycle, start to finish. Everything below runs from the project folder.

```bash
# 1. Get prospects in  (you fill input.xlsx first)
.venv/bin/python scripts/convert.py import
```
```
/import-lps                 # in Claude — creates the LP stub files
/research <LP>              # in Claude — one per LP, or a batch
/draft <LP>                 # in Claude — writes the .md and .html twin
/review-packet              # in Claude — compiles the packets to read
```
```bash
# 2. Check what is actually ready to send
.venv/bin/python scripts/pipeline_status.py          # consistency must say "all clear"
.venv/bin/python scripts/send_queue.py --lang en     # the queue, in score order

# 3. Send, one at a time, from your OWN terminal
.venv/bin/python scripts/make_draft.py drafts/en/pension-funds/<file>.html
#    -> check it, attach the deck, send by hand, close the window
#    -> answer "y" when it asks whether it went out; it logs the send for you

# 4. After a batch
.venv/bin/python scripts/convert.py export           # refresh output.xlsx
```
```
/calibrate                  # in Claude — learn from your edits
/weekly-review              # in Claude — Monday pipeline review
```

Two rules worth knowing before you start:

- **Run `make_draft.py` from your own Terminal**, not from inside Claude Code. In
  a real terminal it can pause and wait if your Outlook login has expired.
- **One browser at a time.** Chromium allows a single process per profile. If a
  window from an earlier run is still open, the script says so and names the PID.

---

## The pipeline — how it works

```
input.xlsx              ← you fill this in
    │
    ▼  python scripts/convert.py import
data/lp-import.csv
    │
    ▼  /import-lps  (Claude)
lps/*.md  (stubs)
    │
    ▼  /research <LP>  (Claude — one per LP, or batches)
lps/*.md  (full research: score, contacts, bridges)
    │
    ▼  /draft <LP>  (Claude)
drafts/<lang>/<list>/*.md  +  .html   (Outlook twin, incl. recipient email)
                        (lang = en|sk|de,   list = pension-funds | insurance)
    │
    ▼  /review-packet  (Claude — packets per type, per language, and a roll-up)
drafts/<lang>/REVIEW-PACKET.md
    │
    ▼  copy each *.html into a new Outlook message  →  Outlook "Drafts" folder
    │     (see "Getting a draft into Outlook" below, and Phase 7 in tutorial.md)
    │
    ▼  supervisor does the final check + sends manually (deck attached)
    │
    ▼  /log-sent <LP>  (Claude)
sent/<lang>/*.md  +  data/output.csv updated
    │
    ▼  /calibrate  (Claude — after each batch)
templates/learnings.md updated
    │
    ▼  python scripts/convert.py export
output.xlsx             ← your live view of the pipeline
```

---

## Getting a draft into Outlook

Every drafted LP produces **two files** in its type folder under `drafts/`
(`drafts/en/pension-funds/`, `drafts/de/insurance/`): a `.md` (the source) and
a `.html` (the formatted, paste-ready version). The `.html` keeps the three
bold labels and the bullet list intact so you do not re-format anything by hand.

**Steps (about 30 seconds per email):**

1. **Double-click the `.html` file** in the type folder — it opens formatted in your
   browser. The grey top line shows the **To** and **Subject** for reference.
2. **Select the body** from the salutation down to "Partner, Valori Capital",
   and copy (Ctrl+C / Cmd+C).
3. In Outlook, click **New Email**, click into the body, and **paste**. If asked,
   choose **Keep Source Formatting** so bold and bullets survive.
4. Fill **To** from the `to:` line at the top of the `.md` file, and **Subject**
   from the `Subject:` line.
5. **Attach the current deck PDF** (the email says "our deck is attached").
6. **Save as a draft — do not send.** It lands in your Outlook **Drafts** folder.

**If bullets or bold get lost:** you pasted as plain text. Undo, paste again,
and pick **Keep Source Formatting**.

**If `to:` says `FIND`:** the address was never confirmed. Confirm it before
sending, or ask Claude.

**To change wording:** small tweaks — edit directly in the Outlook draft.
Bigger changes — edit the `.md`, then ask Claude to rebuild the `.html` twin
and re-copy. Full detail is in `tutorial.md`, Phase 7.

---

## Language support

Email language is determined automatically from the LP's country field.
No manual step is needed.

| Country | Language | Voice template | Bucket |
|---|---|---|---|
| Slovakia, Czechia | Slovak | `templates/voice-sk.md` | `drafts/sk/`, `sent/sk/` |
| Austria, Germany | German | `templates/voice-de.md` | `drafts/de/`, `sent/de/` |
| All others | English | `templates/voice.md` | `drafts/en/`, `sent/en/` |

The same buckets appear as tabs in `output.xlsx` and as a `Language` column in
`data/output.csv`. Drafts, sent records, workbook tabs, and review packets all
use the one rule above, so an LP is in exactly one bucket everywhere.

## The two lists

Inside every language bucket there are exactly **two** folders, named for the
two source lists you work from:

| List | Folder | What goes in it |
|---|---|---|
| **Pension funds** | `pension-funds/` | Any LP whose type mentions a pension |
| **Insurance** | `insurance/` | Everything else, including banks and development agencies |

Entity type is descriptive detail only — it never creates a folder. A national
promotional bank sits in `insurance/` because that is the list it came in on.
`output.xlsx` carries this as a **List** column plus **Insurance** and
**Pension funds** tabs.

New entity types added later still resolve to one of these two lists.

**Overriding the language:**

One-off (this draft only — does not save):
```
/draft <Company Name> en
/draft <Company Name> sk
/draft <Company Name> de
```

Permanent (add to the LP's `.md` file under Data):
```
Language override: en
```
Leave blank to use auto-detection.

**Choosing the number of drafts:**

Default is 3 variations (A/B/C), one per bridge angle from the LP file.

One-off (this run only):
```
/draft <Company Name> 2
/draft <Company Name> en 2     ← combinable with a language code
```

Permanent for an LP (add to its `.md` file under Data):
```
Draft count: 2
```
Leave blank to get 3. Fewer drafts always use the highest-ranked
bridge angles first.

**Rules that apply in every language:**
- Full translation: the hook, the pitch and fund-status lines, the three bullet
  labels and bodies, the subject line, and the close are all translated.
- `Partner, Valori Capital` in the sign-off stays in English (it is the official title).
- Euro amounts and fund numbers stay as numbers (€400M, 19% IRR, etc.); just the surrounding text is translated.
- `Valori Capital` is never translated.
- Structure v4 applies in every language: recipient email in `to:`, a research-grounded
  fit hook (never opening with the LP's company name), a mid-motion line with one
  personal touch, three bold-labelled bullets, the deck line once, and a short
  confident close. Body about 120–190 words. No em-dashes. Contractions are light in
  English and not used in formal German or Slovak. It is a flowing style, not a rigid
  form. Full per-language rules are in `voice.md`, `voice-de.md`, and `voice-sk.md`.

---

## Python script commands

Run from inside this folder, prefixed with `.venv/bin/python`.

**Data in and out**

| Command | What it does |
|---|---|
| `scripts/convert.py init` | Create a blank `input.xlsx` template |
| `scripts/convert.py import` | `input.xlsx` → `data/lp-import.csv` |
| `scripts/convert.py export` | `data/output.csv` → `output.xlsx` |
| `scripts/convert.py sync` | Pull stage + score from `data/output.csv` into `input.xlsx` |
| `scripts/convert.py verify-export` | Export a `verify.xlsx` checklist of fields needing verification |
| `scripts/convert.py verify-import` | Apply verified values back to `data/output.csv` |

Close `input.xlsx` and `output.xlsx` in Excel before running `import`, `export`
or `sync` — Excel locks the file and the write will fail.

**Checking and sending**

| Command | What it does |
|---|---|
| `scripts/pipeline_status.py` | Funnel, language split, send aging, consistency check |
| `scripts/send_queue.py` | Build the sending queue from unsent drafts |
| `scripts/make_draft.py <draft.html>` | Open a filled Outlook compose window, then stop |
| `scripts/log_sent.py <draft.html>` | Record a send by hand |

**Rebuilding generated files**

| Command | What it does |
|---|---|
| `scripts/format_html.py --all` | Refresh every stale `.html` twin |
| `scripts/respace.py --all` | Apply the four paragraph breaks and rebuild the twins |
| `scripts/format_html.py <file.md>` | Refresh one twin after editing its `.md` |
| `scripts/build_packet.py` | Rebuild every review packet |
| `scripts/build_packet.py en` | Rebuild one language bucket |

---

## Claude slash commands

Type these inside the Claude session. Replace `<LP>` with the company name.

| Command | What it does |
|---|---|
| `/import-lps` | Read `lp-import.csv`, create stub `.md` files for any new rows |
| `/research <LP>` | Web-research the LP, score 1-100, write full context file to `lps/` |
| `/draft <LP>` | Write 1-3 email draft variations (default 3) to `drafts/<lang>/<list>/`, update `data/output.csv` |
| `/rescore <LP>` | Recalculate the score for one LP using the 8-layer rubric, show working |
| `/review-packet [en\|sk\|de\|type]` | Compile pending drafts into packets per type, per language, and a roll-up |
| `/log-sent <LP>` | Store the final sent version in `sent/`, update `data/output.csv` to `sent` |
| `/calibrate` | Compare sent emails vs drafts, learn edit patterns, update `learnings.md` |
| `/weekly-review` | Pipeline summary: funnel counts, send aging, tracker-vs-files consistency, stale research |

---

## Before a sending session — the readiness check

Run this before you start. It refuses nothing and changes nothing, it just tells
you which drafts are actually safe to load.

```
.venv/bin/python scripts/pipeline_status.py
```

Read the **CONSISTENCY** block at the bottom. Anything other than `all clear`
means a draft, a sent record and the tracker disagree — fix that before sending.

A draft is ready only when all of these hold. `make_draft.py` enforces the first
one itself and refuses to open a compose window without it:

| Check | Why it matters |
|---|---|
| `to:` is a real address, not `FIND` | `FIND` means the address was never confirmed. The script stops. |
| Three bullet labels wrapped in `**` | Without them the `.html` twin has no bold and the trust block pastes flat. |
| Subject ending is a current one | `first vintage` is retired. Identical subjects across a batch read as mass-sent. |
| Sign-off matches the language | `Kind regards,` / `Mit freundlichen Grüßen,` / `S pozdravom,` |
| The draft sits in `drafts/<lang>/<list>/` | The folder must match the LP's country rule and its `language:` frontmatter. |

**Watch for two LPs sharing one recipient.** Some contacts cover more than one
entity (a CEO over both the carrier and the pension arm). The tracker flags these
in its `flag` column. Send **one** email to that person, not one per entity.

### Closing the loop automatically

When you close the compose window, `make_draft.py` reads the body back out of it,
asks one question, and logs the send for you:

```
Did you send it to Fondo BCC? [y/N]
logged: Fondo BCC -> sent/en/2026-07-28-fondo-bcc.md  (edits: minor, stage=sent)
```

Answer `y` and it writes `sent/<lang>/` (both `.md` and `.html`), sets
`stage=sent` and `date_sent` in the tracker, and records `edits: none|minor|major`
by comparing what you sent against what was drafted. Anything else leaves the row
as `drafted` and writes nothing, so the LP stays in tomorrow's queue.

**Why it asks instead of assuming.** Closing a window is not proof an email went
out. You might close it after deciding not to send. A false `sent` removes that LP
from the queue permanently and silently, which is far more expensive than one
keystroke.

**Why it reads the window instead of copying the draft.** `/calibrate` learns from
the gap between what was drafted and what was actually sent. Copy the draft into
the sent record and that gap is always zero — which is exactly how the 2026-07-22
batch ended up with no calibration signal at all. Capturing the compose body means
edits you make in Outlook are preserved in the record.

Use `--no-log` to turn the prompt off. To log a send after the fact:

```
.venv/bin/python scripts/log_sent.py drafts/en/pension-funds/2026-07-22-fondo-bcc.html
```

Logging twice is safe — a row already marked `sent` is left alone.

---

### Draft formatting

Every body carries four breaks so it reads well on a phone: after the salutation,
after the opening sentence, before the closing sentence, and after the sign-off
line. `scripts/respace.py --all` applies them and rebuilds the `.html` twins.

**The bot reads the `.html`, never the `.md`.** Edit a `.md` and the twin is
stale until you rebuild it, which means the old text goes into Outlook. Both
`respace.py` and `/draft` rebuild twins automatically. If you hand-edit a `.md`,
run `scripts/format_html.py <file.md>` yourself.

---

### Building the sending queue

`scripts/send_queue.py` applies every check in the table above to all unsent
drafts and hands you the exact commands to run, in score order. It reads only,
sends nothing, and changes nothing.

```
.venv/bin/python scripts/send_queue.py                  # today's 5, the daily cap
.venv/bin/python scripts/send_queue.py --lang en        # one language bucket
.venv/bin/python scripts/send_queue.py --all            # every ready draft
.venv/bin/python scripts/send_queue.py --lang en --script today.sh
```

| Flag | What it does |
|---|---|
| `--lang en\|sk\|de` | Only that language bucket |
| `--list insurance\|pension-funds` | Only that list |
| `--limit N` | Queue N drafts (default 5, the PIPELINE.md daily cap) |
| `--all` | Ignore the cap, queue everything ready |
| `--script PATH` | Write a runnable shell script instead of printing |

It sorts the output into three groups:

- **queued** — ready now, printed as `make_draft.py` commands in score order
- **held** — a draft whose recipient already appears earlier in the queue. One
  person gets one email, so the highest-scoring entity is kept and the rest are
  held with the name of the draft they collide with.
- **blocked** — failed a readiness check, listed with the specific reason
  (unconfirmed address, missing bold labels, retired subject ending, wrong
  sign-off for the language). These never reach the queue.

With `--script`, the generated file runs one compose window at a time and pauses
between each, because Chromium allows a single process per profile. Close the
browser, press Enter, and it opens the next.

---

## Loading a draft into Outlook automatically

Instead of the copy-paste routine below, `scripts/make_draft.py` opens Outlook on
the web, starts a new message, and fills in the recipient, subject and body for
you — bold labels and bullets intact. Then it **stops**.

```
.venv/bin/python scripts/make_draft.py drafts/en/insurance/2026-07-22-adriatic-osiguranje.html
```

It never clicks Send and it never attaches the deck. You still do the final
check, attach the deck, and send by hand. Outlook autosaves the message to
your Drafts folder while you work.

**First run** opens Outlook and waits for you to log in. The session is saved
to `.browser-profile/` (git-ignored), so every run after that goes straight to
the compose window.

| Flag | What it does |
|---|---|
| `--dry-run` | Print the parsed To / Subject / body and exit. No browser. |
| `--url URL` | Point at a different mailbox (default `https://outlook.office.com/mail/`) |
| `--profile DIR` | Use a different saved login profile |

If a draft's recipient is still `FIND`, the script refuses to open a compose
window. Fill the `to:` field in the `.md`, re-run `scripts/format_html.py` on
it, then try again.

---

## Score scale

Scores are 1-100. Partial credit is given — subsidiaries of groups with confirmed
alternatives exposure still score 40-60+.

| Score | Meaning | Action |
|---|---|---|
| 75-100 | Top priority | Draft immediately |
| 55-74 | Strong prospect | Draft when ready |
| 35-54 | Medium | Verify key gaps first |
| 20-34 | Low | Keep on radar |
| < 20 | Skip | Regulatory barrier or AUM too small |

The score is built from 8 layers: (1) AUM / cheque & ticket fit, (2) alternatives /
private credit exposure, (3) strategy-language alignment, (4) first-time-manager
appetite, (5) geography & entity type, (6) operational fit (local decisions + named
contact), (7) mandate / regulatory fit, and (8) values / ESG / long-term hook. Full
rubric in `RESEARCH_REQUIREMENTS.md`.

---

## Contact verification

After running `/research` on a batch, some email addresses will be marked `FIND:` (pattern known,
address not confirmed) or `[VERIFY]` (data point needs checking). To manage this:

```
.venv/bin/python scripts/convert.py verify-export
```

This writes `verify.xlsx` — one row per field needing verification, with the current value and
a blank column for the verified value. Fill it in, then:

```
.venv/bin/python scripts/convert.py verify-import
```

This applies your corrections back to `data/output.csv`. Fields that affect the score are flagged
in the checklist.

---

## Common questions

**Can Claude send an email by accident?**
No. It has no mailbox connection. Sending is always a human copying the draft
into a real email client.

**What if I close the terminal?**
Nothing is lost. All memory is in the files. Reopen terminal, `cd` to the
folder, type `claude`, continue where you left off.

**Where do I update fund numbers?**
`CLAUDE.md`, FUND FACTS section. One edit, affects every future draft.

**A draft sounds off. What do I do?**
Tell Claude in plain English. After the same issue appears on a few drafts,
run `/calibrate` — it becomes a standing rule automatically.

**How do I change voice.md or CLAUDE.md?**
Do not edit them directly. Tell Claude what you want changed — it will propose
the edit and wait for your approval before touching either file.

**Can two people use this?**
Yes — it's a folder. Share via synced drive, or put in a private GitHub repo.

**Something looks broken.**
Ask Claude: "something seems wrong with output.csv, can you check it?"
It can read every file and repair its own state.

**How do I add a new language?**
Ask Claude to create `templates/voice-<lang>.md` with the translated fixed phrases.
Then tell it which countries should map to that language — it will add the rule to the
draft command and the README.

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
| `output.csv` | Machine-readable version of output.xlsx. Updated automatically by Claude commands. |
| `lps/lp-import.csv` | Semicolon-delimited import file read by `/import-lps`. Generated from input.xlsx. |
| `lps/` | One research file per LP. Created by `/import-lps`, enriched by `/research`. |
| `drafts/` | Email drafts waiting for review. Nothing here has been sent. |
| `sent/` | Final sent versions, exactly as sent. |
| `templates/voice.md` | Email structure and style canon. Every draft follows this. |
| `templates/learnings.md` | Patterns Claude has learned from your edits. Updated by `/calibrate`. |
| `scripts/convert.py` | Python script — converts between xlsx and csv in both directions. |
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

## The pipeline — how it works

```
input.xlsx              ← you fill this in
    │
    ▼  python scripts/convert.py import
lps/lp-import.csv
    │
    ▼  /import-lps  (Claude)
lps/*.md  (stubs)
    │
    ▼  /research <LP>  (Claude — one per LP, or batches)
lps/*.md  (full research: score, contacts, bridges)
    │
    ▼  /draft <LP>  (Claude)
drafts/*.md
    │
    ▼  you review + supervisor sends manually
    │
    ▼  /log-sent <LP>  (Claude)
sent/*.md  +  output.csv updated
    │
    ▼  /calibrate  (Claude — after each batch)
templates/learnings.md updated
    │
    ▼  python scripts/convert.py export
output.xlsx             ← your live view of the pipeline
```

---

## Python script commands

Run these from inside this folder, after activating the venv.

| Command | What it does |
|---|---|
| `.venv/bin/python scripts/convert.py init` | Create a blank `input.xlsx` template (run once if file is missing) |
| `.venv/bin/python scripts/convert.py import` | Read `input.xlsx` → write `lps/lp-import.csv` |
| `.venv/bin/python scripts/convert.py export` | Read `output.csv` → write `output.xlsx` (color-coded, sorted) |
| `.venv/bin/python scripts/convert.py sync` | Pull current Stage + Score from `output.csv` into `input.xlsx` |

---

## Claude slash commands

Type these inside the Claude session. Replace `<LP>` with the company name.

| Command | What it does |
|---|---|
| `/import-lps` | Read `lp-import.csv`, create stub `.md` files for any new rows |
| `/research <LP>` | Web-research the LP, score 1-100, write full context file to `lps/` |
| `/draft <LP>` | Write 3 email draft variations (A/B/C) to `drafts/`, update `output.csv` |
| `/log-sent <LP>` | Store the final sent version in `sent/`, update `output.csv` to `sent` |
| `/calibrate` | Compare sent emails vs drafts, learn edit patterns, update `learnings.md` |

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

**Can two people use this?**
Yes — it's a folder. Share via synced drive, or put in a private GitHub repo.

**Something looks broken.**
Ask Claude: "something seems wrong with output.csv, can you check it?"
It can read every file and repair its own state.

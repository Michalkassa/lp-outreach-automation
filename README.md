# LP Outreach System — Valori Capital

A self-correcting system for LP (Limited Partner) cold outreach that runs
inside **Claude Code**, an AI assistant that works from your terminal and
reads/writes the files in this folder.

**The most important rule: this system never sends emails.** It researches
investors, writes draft emails as files for you to review, and learns from
the edits you and your supervisor make. A human sends every email manually.

No technical background is needed. If you can use a folder and copy-paste,
you can run this.

---

## 1. What is actually in this folder?

Think of this folder as a filing cabinet that Claude can read and write.
Every piece of the system is just a normal text file you can open yourself.

| File / folder            | What it is |
|--------------------------|------------|
| `CLAUDE.md`              | The instruction sheet Claude reads automatically every time it starts. Contains the sender identity (Valori Capital, Jozef Martinak), the fund facts used in every email, and the rules. |
| `templates/voice.md`     | The "voice canon": the structure and style of the email that already won a client. Every draft is built on this skeleton. |
| `templates/learnings.md` | Claude's memory of the edits you and your supervisor keep making. Starts empty, fills up over time, and makes each batch of drafts better than the last. |
| `lps/`                   | One research file per investor: who the company is, what they invest in, and 2–3 named contact people. |
| `drafts/`                | Email drafts waiting for review. Nothing in here has been sent. |
| `sent/`                  | The final versions that were actually sent, exactly as sent. |
| `tracker.csv`            | Your overview spreadsheet: every investor, their contact, and their stage (research / drafted / sent). Opens in Excel. |
| `tutorial.md`            | The full step-by-step walkthrough of the working rhythm. |
| `.claude/commands/`      | The definitions of the slash commands below. You never need to open these. |

---

## 2. One-time setup (10–15 minutes)

You only do this once.

**Step 1 — Install Node.js** (a free program Claude Code needs)
Go to https://nodejs.org and download the "LTS" version for your computer
(Windows or Mac). Install it like any normal program, clicking Next through
the installer.

**Step 2 — Open a terminal**
- **Windows:** press the Windows key, type `powershell`, press Enter.
- **Mac:** press Cmd+Space, type `terminal`, press Enter.
A black/white window with a blinking cursor appears. This is just a way to
type commands instead of clicking buttons. You will only ever need three:
`cd`, `claude`, and `git init`.

**Step 3 — Install Claude Code**
Type this into the terminal and press Enter:

```
npm install -g @anthropic-ai/claude-code
```

Wait until it finishes (a minute or two).

**Step 4 — Go to this folder in the terminal**
Type `cd ` (with a space after it), then drag this folder from your file
explorer into the terminal window — the path appears automatically. Press
Enter. Example of what it looks like:

```
cd C:\Users\You\Documents\lp-outreach
```

**Step 5 — Start Claude**
Type:

```
claude
```

The first time, it will ask you to log in with your Claude account in the
browser. After that, you are inside a chat with Claude — but this Claude
can see and edit the files in this folder, and it has already read
`CLAUDE.md`, so it knows the entire workflow. You can type to it in plain
English at any time, plus the special commands below.

**Step 6 — Check the facts**
Open `CLAUDE.md` (double-click it, it opens in any text editor) and read
the "FUND FACTS" section once. These exact numbers go into every email.
If anything is wrong or changes later (fund size, close date, committed
amounts), fix it there — one edit updates all future emails.

**Step 7 (optional but recommended) — turn on version history**
In the terminal (not inside Claude), type `git init` and press Enter, once.
From then on every change to every file can be recovered. You never have
to think about it again.

**Every day after setup:** open the terminal, `cd` into the folder (step 4),
type `claude`. That's it.

---

## 3. The five commands

You type these inside the Claude session. `<LP>` means the investor's name,
written normally — for example `/research Bergman Family Office`.

### `/research <LP>` — build the investor's context file
Claude searches the web and writes a file into `lps/` containing:
- **The company:** what type of investor they are, size, what they invest
  in (in their own words), recent activity, and a fit score from 1 to 5.
- **The people:** 2–3 named contact candidates, ranked, with their exact
  titles and where the information came from. Claude never guesses email
  addresses — if one isn't public, it writes `FIND` and the likely format
  so you can verify it yourself.
- **Bridge candidates:** three specific, sourced facts about the investor,
  ranked. The best one becomes the single personalized sentence of the
  email.

**Your job (about 2 minutes):** open the file, check the main contact is
real (a quick LinkedIn look), confirm the email address if marked FIND, and
ask yourself whether the #1 bridge fact is true and specific. Add anything
you know that isn't public. If the fit score is 1 or 2, skip this investor.

### `/draft <LP>` — write the email draft
Claude reads the investor's context file, the voice canon, and the
learnings file, then writes one email on the fixed winning structure and
saves it as a file in `drafts/`. It checks its own work against a 9-point
quality list (correct length, no invented facts, no AI-sounding patterns,
exact fund numbers) before showing it to you.

**Your job (about 2 minutes):** read it once, out loud if you can. Only
three things ever change between emails — the personalized bridge sentence,
the category label, and the greeting — so that is where to look. If the
bridge feels generic, just tell Claude in plain English: *"the bridge is
weak, use candidate #2 instead"* and it rewrites. You can also edit the
file directly yourself.

Repeat research + draft until you have a batch (usually 10–15 drafts).

### `/review-packet` — prepare the supervisor session
Claude gathers **all** pending drafts into one single document in `drafts/`,
ordered best-fit first, with a summary table at the top. Under each email
it shows the contact, the bridge fact **and its source** — so your
supervisor can verify in seconds that the personalization is factual — and
a blank "Supervisor notes:" line.

**Your job:** bring this one document to the review session. Your
supervisor reads, edits what he wants, and **he sends the emails from his
own mailbox, deck attached.** Nothing is sent by you or by Claude.

### `/log-sent <LP>` — record what was actually sent
Run this after the session, the same day, for each email. Claude asks you
to paste the final version exactly as it was sent (or say "unchanged"), and
the date. It stores it in `sent/`, notes whether the edits were none, minor
or major, and updates `tracker.csv` to "sent". If the supervisor rejected a
draft, say so — it goes back to research stage with a note on why.

**Do not skip this step.** The sent versions are the fuel for the next one.

### `/calibrate` — the self-correction
Claude compares every final sent version against its own original draft and
looks for patterns: words the supervisor always deletes, how bridges get
rewritten, length trims, tone changes.
- A pattern seen **twice or more** becomes a rule in
  `templates/learnings.md` and applies to all future drafts.
- Seen **once**, it's noted as a hypothesis and applied softly.
- Seen **three or more times**, Claude proposes a permanent change to the
  voice canon — and waits for your explicit yes before touching it.

The result: batch 2 is drafted the way batch 1 was *edited*. The share of
drafts your supervisor sends unchanged should rise every round, and
`/calibrate` reports that trend (e.g. "sent unchanged: 4 of 12 → 9 of 14").

---

## 4. The working rhythm

```
 ┌────────────────────────────────────────────────────────────┐
 │  /research × 5-10   →   /draft each   →   /review-packet   │
 │        ↑                                        │          │
 │        │                          supervisor session:      │
 │        │                          he edits and HE sends    │
 │        │                                        │          │
 │  /calibrate   ←   /log-sent everything   ←─────┘           │
 └────────────────────────────────────────────────────────────┘
```

One starting email per investor. No follow-up sequences. No reply tracking.
`tracker.csv` always shows the current state of every investor — open it in
Excel whenever your supervisor asks where things stand.

For the fully detailed version of each phase with timings, read
`tutorial.md`.

---

## 5. Common questions

**Do I have to use the slash commands, or can I just talk to Claude?**
You can always type plain English ("research the next three names on my
list", "make the bridge in the Bergman draft more specific"). The commands
just guarantee Claude follows the full checklist every time.

**Can Claude send an email by accident?**
No. It has no connection to any mailbox. It can only create and edit files
in this folder. Sending is always a human copying the draft into a real
email client.

**What if I close the terminal or my computer restarts?**
Nothing is lost. All memory lives in the files. Reopen the terminal,
`cd` into the folder, type `claude`, and continue where you left off.

**Where do I change fund numbers when they update?**
`CLAUDE.md`, "FUND FACTS" section. One place, affects every future email.

**A draft sounds off / too AI-like. What do I do?**
Tell Claude exactly what bothers you, in plain words. Then, after it
happens on a few drafts, run `/calibrate` — if the same fix keeps
appearing, it becomes a standing rule automatically.

**Can two people use this?**
Yes — it's just a folder. Share it via a synced drive, or (better) put it
in a private GitHub repository so changes from both people are tracked.

**Something looks broken.**
Ask Claude itself: "something seems wrong with the tracker, can you check
it?" It can read every file in the folder and repair its own system.

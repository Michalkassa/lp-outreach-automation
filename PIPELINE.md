# MANUAL REACH-OUT PIPELINE
One-time first-touch emails only. Follow this exactly, in batches.

## STEP 0 — Prepare the spreadsheet you were given (once, 20 min)
Do not reorder or delete anything in the original. Add these columns to
the right of the existing data:

  STATUS          (blank | shortlisted | skipped | drafted | sent | replied | call | passed)
  PRIORITY        (A / B / C, see scoring below)
  SEGMENT         (family_office / pension / insurance / endowment / fof / wealth_platform)
  DOMICILE_OK     (yes / no / check — per compliance/rules.md)
  BRIDGE_HOOK     (the one-line fact about them you used in sentence two)
  CATEGORY_LABEL  (which label you used, see email-master.md slot guide)
  DATE_SENT
  REPLY           (blank / positive / negative / neutral)
  NOTES

Save a copy of the original file untouched before you start (e.g.
"outreach-list-ORIGINAL.xlsx"). You will thank yourself later.

## STEP 1 — Shortlist (weekly, ~30 min, pick 15 to 25 names)
Go down the list and score each contact A/B/C:

  A = clear private credit or real assets allocation, Europe-friendly,
      right person (private markets / investments role), domicile OK
  B = plausible fit but something unverified (mandate unclear, contact
      is generic info@, domicile needs checking)
  C = poor fit (pure equities/VC mandate, ticket size mismatch, direct
      competitor conflict, domicile not approved) → STATUS = skipped,
      one word in NOTES why

Rules of thumb:
  - A named person beats a generic inbox. If only info@ exists, spend
    2 minutes on LinkedIn to find the private markets contact first.
  - If their minimum check is clearly above or below our €10M to €50M
    world and fund size, skip. A polite skip now beats a wasted send.
  - DOMICILE_OK = no → never send, whatever the fit. Performance figures
    in the email make jurisdiction the hard gate.

## STEP 2 — Research the day's batch (5 per day, ~10 min each)
For each A-priority name, in Claude Code: /research <LP name>
Read the output. You are looking for ONE thing above all: the fact that
becomes the bridge clause. It must be true, sourced, and specific to
them (their stated mandate, a recent allocation, how they describe
their own bucket). Write it into BRIDGE_HOOK on the sheet.
If no defensible bridge exists after 10 minutes, downgrade to B and
move on. A generic bridge is worse than no email.

## STEP 3 — Draft (same day)
/draft <LP name> in Claude Code (add a number for fewer variants,
e.g. /draft <LP name> 1). Either way, run the Draft QA check in
templates/voice.md yourself, top to bottom (structure v4). Read the email
aloud once, and ask: does it flow? If any sentence sounds like
it was written for "an LP" rather than THIS LP, fix the bridge.

## STEP 3b — Readiness check (once per sending session, 1 min)
Before loading anything into Outlook:

  .venv/bin/python scripts/pipeline_status.py

Read the CONSISTENCY block at the bottom. Anything other than "all clear" means
a draft, a sent record and the tracker disagree. Fix that first.

A draft is ready only when all of these hold:
  - `to:` is a real address, not FIND. make_draft.py refuses FIND by design.
  - The three bullet labels are wrapped in ** so the .html twin renders bold.
  - The .html twin is newer than its .md. The bot reads the .html, so a stale
    twin sends the old text. scripts/respace.py --all rebuilds them.
  - The subject ending is a current one from templates/caption.md.
    "first vintage" is retired, and a batch of identical subjects reads as mass-sent.
  - The sign-off matches the language of the draft.
  - The file sits in drafts/<lang>/<list>/ matching the LP's country rule.

TWO LPs, ONE PERSON: some contacts cover several entities (a CEO over both the
carrier and the pension arm). The tracker flags these in its `flag` column.
Send ONE email to that person, not one per entity, and mark the other row
skipped with a note. This is the easiest way to look careless in front of an LP.

## STEP 4 — Send (manually, from the approved mailbox)
Build the queue first. It applies every STEP 3b check to all unsent drafts and
prints the commands in score order, holding shared recipients and excluding
anything that fails a check:

  .venv/bin/python scripts/send_queue.py                 # today's 5
  .venv/bin/python scripts/send_queue.py --lang en       # one language
  .venv/bin/python scripts/send_queue.py --script today.sh   # runnable script

Then load each draft into a compose window (see "Loading a draft into Outlook
automatically" in README.md):

  .venv/bin/python scripts/make_draft.py drafts/<lang>/<list>/<file>.html

It fills To, Subject and the body, then stops. It never sends and never attaches
the deck. Run it from your own terminal, not from inside Claude Code, so it can
wait for a login if the session has expired. One browser at a time: Chromium
allows a single process per profile and the script will tell you if one is
already running.

  - Deck attached. Correct deck version. Check the attachment is there.
  - Salutation spelling of the surname, triple-checked.
  - Send Tue to Thu, 08:30 to 10:30 their local time when possible.
  - Max 5 sends per day. Quality of the bridge beats volume, and low
    daily volume from a normal mailbox also keeps deliverability clean.

## STEP 5 — Log (now automatic, confirm with one keystroke)
When you close the compose window, make_draft.py reads the body back out of it
and asks:

  Did you send it to <LP>? [y/N]

Answer y and it writes sent/<lang>/ (.md and .html), sets stage=sent and
DATE_SENT in the tracker, and records edits: none|minor|major by comparing the
sent text against the draft. Anything else leaves the row as drafted, so the LP
stays in tomorrow's queue.

It asks rather than assuming because closing a window is not proof of a send. A
false "sent" drops that LP out of the pipeline silently.

Because the record comes from the compose window and not from the draft file,
edits you make in Outlook are captured, and /calibrate has something real to
learn from. Copying the draft across is what made the 2026-07-22 batch produce
zero calibration signal.

If something goes wrong, log it by hand:
  .venv/bin/python scripts/log_sent.py drafts/<lang>/<list>/<file>.html
Never batch this for "later". Later does not happen.

## STEP 6 — Replies
  - Positive or neutral reply → STATUS = replied, REPLY filled, respond
    within 24h, aim for the call. Paste the reply into /log-sent so the
    system records which bridge worked.
  - Negative → STATUS = passed, one-line NOTES why. No rebuttal email.
  - No reply → nothing. This is a one-time email by design.

## WEEKLY (Monday, 15 min)
  - /weekly-review in Claude Code.
  - On the sheet: count sent vs replied by SEGMENT and by BRIDGE_HOOK
    style. Whatever bridge style is pulling replies, shortlist more
    names where that bridge is available.
  - Refill the shortlist back up to 15 to 25 A-names.

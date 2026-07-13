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
e.g. /draft <LP name> 1), or fill templates/email-master.md by
hand. Either way, run the Draft QA check in voice-examples.md yourself,
top to bottom. Read the email aloud once. If any sentence sounds like
it was written for "an LP" rather than THIS LP, fix the bridge.

## STEP 4 — Send (manually, from the approved mailbox)
  - Deck attached. Correct deck version. Check the attachment is there.
  - Salutation spelling of the surname, triple-checked.
  - Send Tue to Thu, 08:30 to 10:30 their local time when possible.
  - Max 5 sends per day. Quality of the bridge beats volume, and low
    daily volume from a normal mailbox also keeps deliverability clean.

## STEP 5 — Log (immediately after each send, 1 min)
  - Spreadsheet: STATUS = sent, DATE_SENT, confirm BRIDGE_HOOK and
    CATEGORY_LABEL are filled.
  - Claude Code: /log-sent <LP name> and paste the final version.
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

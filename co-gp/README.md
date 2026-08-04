# Co-GP outreach — Valori Capital

A second, separate outreach programme. **Nothing here is live yet.**

This folder is self-contained: its own prospect list, tracker, drafts, sent
archive and voice. It shares nothing with the LP programme except the scripts in
`../scripts/` and the fund facts in `../CLAUDE.md`.

---

## Why it is separate

The LP programme asks institutions to allocate capital to a fund. This one
proposes working alongside another firm on deals. Different reader, different
proof, different ask. Mixing them would mean one tracker with two incompatible
scoring rubrics and one voice file trying to serve two audiences.

Keeping them apart also means the LP campaign, which is mid-flight, is not
disturbed by anything that happens here.

---

## What is in this folder

| File / folder | What it is |
|---|---|
| `input.xlsx` | **Your input.** One row per Co-GP prospect. Same shape as the LP input, with `Firm` in place of `Company`. Delete the grey example row. |
| `data/output.csv` | The tracker. Headers only right now. |
| `prospects/` | One research file per firm. `_TEMPLATE.md` is the blank structure. |
| `drafts/` | Email drafts awaiting review. Empty. |
| `sent/` | Final sent versions. Empty. |
| `templates/voice.md` | Voice canon for this programme. Adapted from the LP voice, with open questions marked TODO. |
| `templates/caption.md` | Subject-line rules. TODO. |
| `templates/learnings.md` | Deliberately empty. Fills up from calibration once real sends exist. |
| `RESEARCH_REQUIREMENTS.md` | What to research, and the scoring rubric. Rubric is TODO. |

---

## The offer

`OFFER.md` holds the commercial terms and is to this programme what FUND FACTS
in `../CLAUDE.md` is to the LP one. Numbers go into emails verbatim.

In short: **€100M from a partner unlocks a further €50M** alongside the €50M
already committed, against a €400M target. **Half management fees and carry**,
plus **20% of the total carry pool**. **First look and first priority pro rata**
on co-investments alongside the first anchor. Governance and rights open to
negotiation.

Three items in `OFFER.md` are marked **[CONFIRM]** and must not appear in an
email until settled: who provides the matched €50M, whether "half fees and carry"
means half the rate or half of Valori's share, and the basis of the 17.4%
expected IRR.

## Scoring

`RESEARCH_REQUIREMENTS.md` scores six layers against what a Co-GP actually has to
be: fundraising capability and distribution are the two critical layers, then
ability to co-manage, partnership fit, strategy overlap and structural readiness.

Two hard rules fall out of it: a **direct competitor caps at 25**, and a firm
that invests only its own balance sheet is an **LP prospect, not a Co-GP** — say
so in the summary and move them.

`templates/learnings.md` is still empty on purpose: it is an evidence file, and
copying LP learnings into it would present assumptions as findings.

---

## Before this goes live

- [ ] Resolve the three [CONFIRM] items in `OFFER.md`
- [ ] Fill `input.xlsx` with prospects
- [x] Define the scoring rubric in `RESEARCH_REQUIREMENTS.md`
- [x] Define what makes the email persuasive, then finish `templates/voice.md`
- [x] Define subject rules in `templates/caption.md`
- [ ] Wire the slash commands (/research, /draft) to accept a programme

---

## Scripts

Every script in `../scripts/` works on this programme. Add `--program co-gp`:

```bash
.venv/bin/python scripts/pipeline_status.py --program co-gp
.venv/bin/python scripts/send_queue.py      --program co-gp
.venv/bin/python scripts/make_all_drafts.py --program co-gp --all
.venv/bin/python scripts/convert.py import  --program co-gp
.venv/bin/python scripts/convert.py export  --program co-gp
.venv/bin/python scripts/build_packet.py    --program co-gp
.venv/bin/python scripts/format_html.py --all --program co-gp
.venv/bin/python scripts/respace.py     --all --program co-gp
```

Or set it once for a whole session:

```bash
export VALORI_PROGRAM=co-gp
```

No flag means `lp`, so the LP workflow is unchanged. `--program=co-gp` works too,
and the flag can go anywhere in the command.

`scripts/program.py` resolves it. Run it on its own to see which paths a
programme maps to:

```bash
.venv/bin/python scripts/program.py --program co-gp
```

Paths this programme uses:

| | |
|---|---|
| input | `co-gp/input.xlsx` |
| tracker | `co-gp/data/output.csv` |
| research | `co-gp/prospects/` |
| drafts | `co-gp/drafts/<lang>/<list>/` |
| sent | `co-gp/sent/<lang>/` |
| voice | `co-gp/templates/` |

The schema is **identical** to the LP programme, deliberately. Same tracker
columns, same input columns, same folder convention. That is what lets one set of
scripts serve both without a special case anywhere.

One thing is shared rather than duplicated: the Outlook browser profile at
`.browser-profile/`. There is one mailbox, so both programmes send from it, and
only one browser can run at a time across both.

---

## Getting started

```bash
# 1. Fill co-gp/input.xlsx with prospects (delete the example row)
.venv/bin/python scripts/convert.py import --program co-gp

# 2. In Claude: research and draft, writing into co-gp/prospects/ and co-gp/drafts/
# 3. Check what is ready
.venv/bin/python scripts/send_queue.py --program co-gp

# 4. Build the Outlook drafts
.venv/bin/python scripts/make_all_drafts.py --program co-gp --all
```

Step 2 has no slash-command support yet: `/research` and `/draft` are written
against the LP paths. Until that is wired, ask Claude directly and point it at
this folder.

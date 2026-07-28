Build or refresh the context file for the LP in $ARGUMENTS at
/lps/<lp-slug>.md using /lps/_TEMPLATE.md.

Read RESEARCH_REQUIREMENTS.md before starting.

---

## Purpose — research does two things only
1. Find the right contact — the CIO / Head of Investments / Head of Alternatives
   first; CFO, then CEO / board chair only as a fallback. Find who actually decides
   allocations, and record the desk, not just the title.
2. Surface the one or two things the firm most values, so /draft can lean that way
   subtly. The email never states these back to the LP (see templates/voice.md).

Do not over-research. Stop once you have a CIO, a size band, and one value thread.

## Research process — ~3 targeted searches
1. `"{company}" CIO OR "head of investments" OR "chief investment officer" 2024 2025`
   — the contact, first priority
2. `"{company}" investment strategy AUM annual report 2025` — size band + how they invest
3. `"{company}" private credit alternatives real estate` — one value / priority thread

Run a 4th only if the score is genuinely on a knife-edge (a specific mandate limit,
first-time-manager evidence). Otherwise stop. No research papers.

---

## File content — keep it tight

**Target length:** 150–250 words of substantive content (excluding headings).
Enough to draft from and to score. Specific facts over volume.

**Data section:** Every field filled or marked VERIFY. AUM needs a source (size band
is fine).

**Investment Strategy:** 2–4 sentences. How they invest, their size, and the one or
two things they most value (the angle /draft will lean on). No generic sector filler.

**People & Org:** 1–2 sentences. Who decides allocations. Local or HQ.

**Contacts:** ONE contact — the CIO / investment lead (fallback CFO, then CEO). 2–3
sentence background, one line on why they own the decision. Never guess emails —
FIND with pattern.

**Bridge / value threads:** 1–2 lines. The general framing of their world the hook
can use (e.g. "conservative insurance balance sheet," "book active in real assets").
Never something to quote back at them.

**Summary:** 1 sentence. Who they are, the fit angle, the main caveat, the score.

Drop Recent Activity, multi-candidate contacts, and Peer Context unless they change
the score or the bridge.

---

## Accuracy rules
- Never invent AUM. If not found: [VERIFY — not found publicly].
- Never guess emails. Use import data first; mark FIND with pattern.
- Mark unverified claims [VERIFY] with what source would confirm.
- No generic sector padding. Every sentence must be about THIS company.

---

## Scoring
Score 1-100 using RESEARCH_REQUIREMENTS.md rubric. Partial credit generous.
Add score to top of file: `score: XX/100`

---

## Output file update
Update data/output.csv (stage=research, score filled).
data/output.csv uses semicolons (;) as delimiter. No semicolons inside field values.
Columns: country;language;type;list;company;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent
Score is a plain integer 1-100 (not "90/100").

---

## End summary (print after writing the file)
Score: XX/100
Best contact (CIO first): [name, title, email]
Fit angle: [the general framing the hook will use]
Data gaps: [list any key fields still marked VERIFY]

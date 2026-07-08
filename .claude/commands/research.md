Build or refresh the context file for the LP in $ARGUMENTS at
/lps/<lp-slug>.md using /lps/_TEMPLATE.md.

Read RESEARCH_REQUIREMENTS.md before starting.

---

## Research process — 4-6 searches per company

### Tier 1 — always run
1. "{company name} investment strategy AUM annual report 2024 2025"
2. "{company name} private credit alternatives real estate debt"
3. Visit their website — find AUM, asset allocation, strategy statements

### Tier 2 — always run
4. "{contact name} {company} LinkedIn" — career history, role, posts
5. "{company name} CIO investment committee alternatives 2024 2025"

### Tier 3 — run for likely score >50
6. "{company name} annual report portfolio allocation breakdown"
7. "{company name} ESG sustainability responsible investment"

---

## File content — keep it tight

**Target length:** 400-600 words of substantive content (excluding headings).
Write for someone scanning before a call, not writing a research paper.
Specific facts and quotes over volume.

**Data section:** Every field filled or marked VERIFY. AUM needs a source.

**Investment Strategy:** 5-8 sentences. Their allocation philosophy,
how they name their alternatives bucket (quoted), confirmed or estimated
private credit exposure, regulatory context, any recent shift.
Quote directly with source. No generic sector filler.

**People & Org:** 2-3 sentences. Who decides on alternatives. Local or HQ.

**Contacts:** 2 people max. For each: 2-3 sentence background, one sentence
on why they own this decision. Never guess emails — FIND with pattern.

**Recent Activity:** 3-4 dated bullets. Allocation changes, mandate
developments, leadership moves. Each sourced.

**Bridge Candidates:** 3 options, each a different angle. Specific and
verifiable — quote the source. No generic observations.

**Summary:** 3-4 sentences. Who they are, why they fit, best bridge,
key contact, main caveat, score explanation.

Peer Context section is optional — include only if a direct comparison
adds real insight (e.g. named peer has committed to private credit and
this LP has not yet matched it).

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
Columns: country;company;type;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent
Score is a plain integer 1-100 (not "90/100").

---

## End summary (print after writing the file)
Score: XX/100
Best contact: [name, title, email]
Best bridge: [one sentence, sourced]
Data gaps: [list any key fields still marked VERIFY]

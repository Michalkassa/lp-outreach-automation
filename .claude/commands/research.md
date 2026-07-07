Build or refresh the context file for the LP in $ARGUMENTS at
/lps/<lp-slug>.md using /lps/_TEMPLATE.md.

Read RESEARCH_REQUIREMENTS.md before starting.

---

## Research process — minimum 6-8 searches per company

Run ALL of the following searches. Do not skip any unless the company is
clearly a skip (mandatory fund, <€200M AUM, absorbed entity).

### Tier 1 — always run (company overview)
1. "{company name} investment strategy AUM annual report 2024 2025"
2. "{company name} private credit alternatives real estate debt investment"
3. "{company name} website" — then visit their actual website:
   - Look for: Investor Relations, Annual Report, About Us, Investment Philosophy
   - Find: AUM, asset allocation breakdown, alternatives %, any strategy statements
   - Quote their own language directly into the Investment Strategy section

### Tier 2 — always run (people and org)
4. "{first name} {last name} {company} LinkedIn" — visit their LinkedIn profile:
   - Career history: previous firms, how long in current role
   - Any posts or articles about alternatives, private markets, credit investing
5. "{company name} CIO investment committee alternatives 2024 2025"
6. "{company name} {CEO/CIO name} interview conference statement private credit"

### Tier 3 — run for all companies scoring likely >40
7. "{company name} annual report 2023 2024 investment portfolio allocation"
8. "{company name} private equity infrastructure debt real assets commitment"

### Tier 4 — run for high-priority companies (likely >65)
9. "{company name} ESG sustainability responsible investment mandate"
10. "{company name} LP investor alternatives fund commitment 2024 2025"

---

## What to extract from each source

**Company website / annual report:**
- Exact AUM or invested assets figure with year
- Asset allocation breakdown (% equities, bonds, alternatives, real estate)
- Any quote about investment philosophy or alternatives mandate
- Names of investment team or investment committee members
- Regulator and legal entity type

**LinkedIn (contact person):**
- Full career history: where they worked before, for how long
- Current title and how long in role
- Any posts, articles, or comments about private markets, credit, real assets
- Education (relevant for gauging sophistication)

**News / press / conference sources:**
- Any public statement about alternatives or private credit strategy
- Fund commitments or new manager relationships announced
- Strategy changes, new investment guidelines, regulatory updates

---

## File content — depth requirements

**Target length:** Each LP file should be 600-900 words of substantive content
(excluding headings and placeholder lines). Do not pad with generics — depth
comes from specificity, not length for its own sake.

**Data section:** Every field filled or explicitly marked VERIFY with a reason.
AUM must have a source year and named document. Ownership must name the parent
group and ownership % if subsidiary.

**Investment Strategy:** 8-12 sentences minimum. This is the core section.
Must include ALL of:
- Their asset allocation philosophy in their own words (quoted where possible)
- How they name their alternatives or private credit bucket (exact terminology)
- Confirmed or estimated private credit / real asset debt exposure with source
- Target return or yield requirements if stated
- Geographic preference if stated
- Manager preference: size, track record, LP alignment, co-investment appetite
- Regulatory context (Solvency II, IORP, local pension law) and how it shapes mandate
- Any recent strategic shift: new CIO, new guidelines, new asset class added
Every direct quote must be in "quotation marks" with source in parentheses.

**People & Org Structure:** 4-5 sentences. Name the investment committee explicitly.
State: who chairs it, quorum for alternatives sign-off, number of investment professionals,
and whether decisions are local or require parent HQ approval.

**Contacts:** For each person, write a full background paragraph (3-4 sentences):
- Full career history: previous firms, roles, and tenure at each
- How long in current role
- Any public statements, conference appearances, or articles about private markets
- Education background
- Why they specifically own this allocation decision (their actual remit, not just title)

**Recent Activity:** Minimum 5 bullets, each with a date or named source. Cover:
one return/performance figure, one allocation development, one people/governance event,
one public statement or conference appearance.

**Peer Context:** 3-4 sentences. Name 1-2 specific peers and compare directly.
State explicitly whether this LP is ahead of or behind peers on private credit.
Note any peer LP commitments this fund has not yet matched.

**Bridge Candidates:** Each bridge must be specific and verifiable — quote the source.
No generic sector observations. Three bridges minimum, each a different angle.

**Summary:** 6-8 sentences written as a partner briefing note. Cover: entity and
market position, specific mandate fit (not generic), best bridge and why it lands,
key contact and actual remit, confirmed vs. inferred facts, main caveat, and a
plain-English score explanation.

---

## Accuracy rules

- Never invent AUM figures. If not found, write [VERIFY — not found publicly].
- Never guess email addresses. Use import data first; mark FIND with pattern.
- Mark every unverified claim with [VERIFY] and note what source would confirm it.
- If a website or LinkedIn contradicts earlier research, use the newer/direct source.
- Do not pad the file with generic sector commentary — every sentence must be
  specific to THIS company.

---

## Scoring

Score 1-100 using RESEARCH_REQUIREMENTS.md rubric. Apply partial credit generously.
Add score to top of file: `score: XX/100`

---

## Output file update

Update data/output.csv (stage=research, score filled).
data/output.csv uses semicolons (;) as delimiter. No semicolons inside field values — use
em dashes (—) or commas instead.
Columns: company;country;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent

---

## End summary (print after writing the file)
Score: XX/100
Best contact: [name, title, email]
Best bridge: [one sentence, sourced]
Data gaps: [list any key fields still marked VERIFY]

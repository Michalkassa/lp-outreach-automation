Build or refresh the context file for the LP in $ARGUMENTS at
/lps/<lp-slug>.md using /lps/_TEMPLATE.md.

Read RESEARCH_REQUIREMENTS.md before starting — it defines the 100-point scoring
rubric, partial credit rules, red flags, segment notes, and bridge examples.

## Research process

Run a minimum of 3 web searches per company:
1. "{company} AUM investment strategy alternatives private credit 2024 2025"
2. "{company} annual report investment portfolio real estate debt"
3. "{company} CIO CEO investment team"

For companies likely to score >60, add:
4. "{company} private markets infrastructure alternatives commitment 2025"
5. "{company} ESG sustainability long-term investment mandate"

## File content

Fill all sections of the LP file using _TEMPLATE.md:

- **Data**: type, domicile, regulator, AUM, ownership, alternatives exposure.
  Mark unverified items [VERIFY]. Do not guess.

- **Investment Strategy**: 3-5 sentences on how they invest. Use their own language.
  Cover asset allocation framework, alternatives approach, any illiquid credit angle.

- **Recent Activity**: 2-3 bullet points from the last 18 months. Sourced facts only.
  Examples: new allocation, strategy shift, fund launch, public statement, hire.

- **Contacts**: 2 people. Use import data first. For each: name, title, email,
  and one sentence on why they are the right door (role, decision scope).

- **Bridge Candidates**: 3 options ranked best to third. Each one sentence,
  specific, sourced. Pick the one that is most verifiable and directly relevant
  to Valori's mandate (distressed credit, European real estate backed, bilateral).

- **Summary**: 3-4 sentences — who they are, why they fit Valori, best bridge hook,
  and briefly why the score is what it is (key strength and any key caveat).
  Do NOT list scores per criterion — just explain the overall number in plain English.

## Scoring

Score 1-100 using RESEARCH_REQUIREMENTS.md rubric. Be generous with partial credit:
- Plausible based on entity type counts, mark it [likely]
- Subsidiaries of alternatives-active groups still score 40-60+ range
- Unconfirmed AUM but entity type implies sufficient scale: give partial points

Add score to top of file: `score: XX/100`

## Output file update

Update output.csv (stage=research, score filled).
output.csv uses semicolons (;) as delimiter.
Columns: company;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent

## End summary
Score: XX/100
Best contact: [name, title, email]
Best bridge: [one sentence]

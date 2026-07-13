# LP Outreach — Valori Capital

## SENDER (who every email is from)
- Fund: Valori Capital, first vintage
- Person: Jozef Martinak, Partner
- Sign-off: "Kind regards,"

## FUND FACTS (verbatim in every email, never improvise numbers)
- Strategy: distressed credit and special situations backed by European
  real estate. Bilateral, highly protected deals.
- Tickets: €10M to €50M, a segment too fragmented for mega-funds.
- Raise: €400M target close by April 2027. €50M anchor + €1M GP committed.
- Pipeline: €100M+ proprietary, mostly bilateral.
- Track record: 50+ years combined experience, €1.35B previously
  underwritten at a 19% IRR.
- Target: 15%+ net IRR to LPs.
- Foundation: partners hold strong Christian values, absolute integrity,
  significant share of profits given back to society.

## THE LOOP (you never send anything, no exceptions)
1. /research <LP>  → context file in /lps/: the RECEIVER. Company (type,
   AUM, mandate, recent activity) and person (2-3 named contact
   candidates with titles and sources).
2. /draft <LP> [n] → 1-3 draft variants (default 3, one per bridge
   angle) in /drafts/, built from that context file +
   templates/voice.md + templates/learnings.md.
3. I review the draft file, edit, send manually.
4. /log-sent <LP>  → I paste my final sent version, you store it in /sent/
   and update tracker.csv.
5. /calibrate      → compare my sent versions against your drafts, learn
   my edit patterns, update templates/learnings.md so future drafts need
   fewer of my corrections.

One email per LP. No follow-ups. No reply tracking.

## RULES
- Never draft without reading: the LP's /lps/ file, templates/voice.md,
  templates/learnings.md. If no LP file exists, run /research first.
- Never invent facts about the LP (their file only) or Valori (Fund facts
  only, exact numbers).
- Drafts are files: /drafts/YYYY-MM-DD-<lp-slug>-A.md (-B, -C)
- Only /calibrate edits learnings.md. Never edit voice.md or this file
  yourself: propose the change, wait for my yes.
- tracker.csv stages: research → drafted → sent. Nothing else.

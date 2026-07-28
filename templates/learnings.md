# LEARNINGS — read before every draft. Only /calibrate edits this.
# Basis: v4 framework + CALIBRATION 2026-07-22 (15 sent edits). Canon = voice.md / voice-sk.md.
# GOLD-STANDARD BANK: templates/sent-examples.md — 15 of the user's final edited emails.
# Read it before drafting and DRAW phrasing/structure/register from it (never copy verbatim).
#
# CALIBRATION 2026-07-28 — 27 sent (20 en, 7 sk), ZERO new style signal.
# Every sent file is byte-identical to its draft, because the 2026-07-22 pass
# rewrote the drafts to match the user's final versions (sent frontmatter reads
# "revision: user final (calibration) 2026-07-22"). The draft-vs-sent delta was
# already consumed on that date and cannot be re-derived from these files. So
# nothing below changed on style grounds. Treat the Confirmed list as still
# current, not as re-validated.

## CONFIRMED (2+ occurrences in the 15 edits) — apply every time
1. **"deals"/"tickets" → "transactions ranging from €10M to €50M".** Say "secured,
   bilateral transactions ranging from €10M to €50M" (or "tickets ranging from"). Never "deals".
2. **Hedged fit opener that names the LP's real situation (from research).** Pattern:
   "I am reaching out as/because there may be a fit with [your X]" or "our strategy could
   be a good fit for [X]". [X] is a concrete research profile, e.g. "your existing
   alternatives allocation", "a large fund with unutilized private credit allocation",
   "large, bond-led portfolios diversifying beyond government bonds", "your balance sheet
   allocation", "a portfolio already active in real assets", "your fund's existing
   real-economy allocation". Sometimes name the LP directly (OTP). Hedge words:
   "there may be a fit", "could be a good/natural fit". Softer than the blunt "our approach fits X".
3. **Present-tense, experienced verbs; NEVER "We are building".** Use "We provide /
   We operate / We manage / We originate / We run". "We are building our first fund now"
   is banned (the user confirmed it was an error). The team is experienced (€1.35B, 19% IRR).
4. **Fund-status default (simple): "We are targeting €400M by April 2027. €50M is
   committed and €1M is our own."** Vary it: "We are currently fundraising for our latest
   private credit strategy…", "We are now raising our first vintage…", "We are currently
   €50M into raising our €400M target fund, with a planned close by April 2027…", "The
   fundraise is underway for our €400M target fund…". Keep "by April 2027" (usually retained).
5. **Protection as a fuller professional clause** (not only terse "protection ahead of
   yield"): "with the underlying property providing strong downside protection", "secured
   against the underlying real estate", "focused on capital preservation and durable yield
   generation", "capital protection alongside yield". (Short "protection ahead of yield" still OK.)
6. **Selectivity woven into the fund-status paragraph:** "the initial investor base is
   being built selectively with a small group of aligned partners ahead of the broader
   fundraising process" / "the initial close reserved for a carefully selected group of
   founding investors" / "engaging with a select group of investors ahead of the broader raise".
7. **Close — two accepted forms.** Standard: "Our deck is attached. If a specialised
   European real asset debt manager fits your current mandate or co-investment interests,
   I would welcome a brief introductory call." OR softer: "Our deck is attached for your
   review. If this interests you, I would welcome the opportunity to introduce the strategy
   in more detail and discuss whether it could complement [LP]'s investment objectives."
   "aligns with" is an accepted alt to "fits".
8. **Register more formal/professional throughout:** "risk-adjusted returns", "capital
   preservation", "for your review", "the opportunity for a brief introductory call".

## HYPOTHESES (single occurrence — watch, do not force)
- Bullets occasionally reworded ("previously underwritten", "supported by over 50 years",
  "predominantly bilateral", "with 15%+ unlevered returns at the asset level"). Labels never
  change. Many kept the original — treat as an optional variant, not a rule.
- Personal touch sometimes on its own line, sometimes folded into the fund-status sentence.

## RETIRE (stopped doing)
- "We are building a private credit strategy" / "We are building our first fund now" — banned.
- The single terse "…in tickets of €10M to €50M, protection ahead of yield." as the ONLY
  form — now expanded and varied per Confirmed #1 and #5.
- SK "Budujeme…" opener — replaced by "Naša stratégia … prirodzene dopĺňa …" (voice-sk.md).

## STILL TRUE (v4)
- Never open with the LP's company name as the first word (naming them mid-sentence is fine,
  e.g. "a fit between OTP's activities and our strategy").
- Three bold trust bullets; deck line; a close that explicitly asks for a call.
- No em-dashes, no semicolons. Every number matches Fund facts.
- SK: keep "private credit" in English; "Pričom ochrana kapitálu je našou hlavnou prioritou.";
  "Naša prezentácia je v prílohe." close; no "Budujeme".

## DRIFT CAUGHT BY CALIBRATION (not a style edit — a rule that stopped being applied)
- **Retired subject ending survived in old drafts (15 occurrences, 2026-07-28).**
  caption.md retires "first vintage" as the Subject ending, but every draft from the
  2026-07-22 batch still carried "Valori Capital, [category], first vintage". Left alone
  they would have gone out with near-identical subjects, which is the mass-send signal
  caption.md exists to prevent. All 15 rotated onto the approved endings, zero adjacent
  duplicates. BEFORE DRAFTING: generate the Subject from caption.md fresh. Never inherit
  a subject from an older draft of the same LP, and never reuse a retired ending.
- Check-before-send: no draft's subject ending should repeat the one immediately
  before it in its review packet.
- **Bold markers lost on the trust bullets (15 occurrences, 2026-07-28).** The whole
  2026-07-22 batch wrote the bullets as "- Track Record: ..." with no `**`. voice.md
  requires the label before the colon in bold, and format_html.py produces `<strong>`
  only from `**`, so those emails paste into Outlook with plain labels and the trust
  block loses its scan value. 14 of the 15 had already been sent that way. WRITE THE
  BULLETS EXACTLY AS: "- **Track Record:** ..." and confirm the .html twin shows three
  `<strong>` before treating a draft as ready.

## DATA-FIXES seen (not style — verify contacts)
- PZU → "Sołdek" (draft had Trela). Modra → "Matzele" (shortened from Golob Matzele).
- Generali Versicherung → "gregor.pilgram@" (import had the typo "greogor.pilgram@";
  corrected 2026-07-28 from the import's own First Name field and the LinkedIn slug).
- KOOPERATIVA → "Vladimír Bakeš" (import has "Valdimir Bakes"); short email format unverified.

## PROCESS GAP (blocks future calibration — worth fixing)
- No file in /sent/ carries the `edits: none|minor|major` field that log-sent.md mandates.
  Without it, once drafts are regenerated the draft-vs-sent diff goes to zero and there is
  no record of whether a send was edited at all. Set `edits:` on every future /log-sent.

# VOICE — canon. Structure v5 (2026-08-03), set by Michal.
# v5 replaces the v4 structure. The v4 openers and the mid-motion personal touch
# are retired. The deck is referenced again, but only inside the two-sentence CTA
# in part 5. Do not reintroduce v4 shapes from older drafts or from
# templates/sent-examples.md, which is a v4 archive.

## The feel we are going for
A short, plain email from one partner to one investor. It states what we are
raising, why it might fit, what stands behind it, and asks for a short call.
No build-up, no salesmanship. If a sentence is not doing one of those four jobs,
cut it.

## Output format (every draft)
- Frontmatter carries `to:` = recipient email. Always present.
- Ship BOTH a `.md` and a `.html` (Outlook paste-ready) per draft. Regenerate the
  `.html` whenever the `.md` changes: the sending bot reads the `.html`, so a
  stale twin puts the old wording or spacing into Outlook.
- The three bullets are a real list with the label before the colon in bold.
- Four breaks in every body: after the salutation, after the opening sentence,
  before the closing block, and after the sign-off line so the name sits apart.
  `scripts/respace.py` applies these. The closing block is two sentences and is
  never split.

## The structure (v5 — five parts, in this order)

**1. What we are raising.** Opens the body. Product first, no preamble.

    "We are currently fundraising for our European opportunistic private credit
    fund backed by real estate collateral, in tickets of €10M to €50M."

  - The product name is **"European opportunistic private credit fund backed by
    real estate collateral"**. Use it in full.
  - The €10M to €50M tickets belong in this sentence.
  - **The word "bilateral" is retired.** It does not appear anywhere in the body.

**2. Why it might fit.** One sentence, hedged, generic.

    "We think our strategy might fit into your portfolio and may nicely
    complement [a general framing of their situation]."

  - Keep "we think" and "might" / "may". The fit is offered, not asserted.
  - The framing after "complement" is the one part that changes per LP, drawn
    from their research file and stated GENERALLY: "a book taking its first steps
    into alternatives", "a large, bond-led portfolio", "a fund with room to put
    private capital to work".
  - Do not name the institution, quote their figures, or describe their own
    position back to them.

**3. Where the raise stands.** Its own short paragraph.

    "We are targeting €400M by April 2027. €50M is committed and €1M is our own."

  - Vary the wording lightly, never the numbers.
  - Present tense. Never "we are building".

**4. The proof — three bullets.** The trust block below, as a real list.

**5. The ask.** The closing block, on its own. TWO sentences, ONE block.

    "Please find attached our presentation. If you are interested, I would be happy to have a 20 minute short introductory call."

  - Keep it verbatim. The deck sentence and the call ask stay together on one
    block, not split across two.
  - "If you are interested" is the hinge: it makes the call conditional rather
    than presumed.
  - It asks for a specific, small commitment. Keep the 20 minutes.
  - The deck IS referenced again, so it must actually be attached at send time.

## The three bullets (the trust block — exact numbers, these three)
- **Track Record:** €1.35B underwritten previously at a 19% IRR, over 50 years of combined experience.
- **Current Dynamics:** €50M committed and a €100M+ proprietary pipeline.
- **Target Returns:** 15%+ net IRR to LPs (15%+ unlevered at the asset level).

## Fixed points (do not drift on these)
- Fund-facts numbers verbatim; never improvise a figure.
- The three bold bullets above, exactly as written.
- Never open the body with the LP's company name.
- Research shows through the framing in part 2, never quoted back at them, never
  framed as something they asked for or showed interest in.
- No em-dashes. No semicolons. No "bilateral".
- Salutation "Dear Mr./Ms. Surname" (surname only). Sign-off "Kind regards," /
  Jozef Martinak / Partner, Valori Capital (English always).
- Body roughly 100–150 words. Secular values only.

## Vary, always (this is a style, not a template)
- Parts 1, 4 and 5 are close to fixed. The variety lives in part 2's framing and
  lightly in part 3's wording.
- No two consecutive LPs should share the framing after "complement". If a line
  could be pasted into any email, cut it.

## Retired in v5 (do not reintroduce)
- The "I'm reaching out because our approach fits…" opener.
- The second opener, "We run a private credit strategy… which would be a natural
  fit to…".
- The mid-motion paragraph and its personal touch (handling it himself, a region
  note, an offer of time).
- The old close, "Our deck is attached." followed by "If a specialised European
  real asset debt manager fits your current mandate or co-investment
  interests…". Replaced by the single two-sentence CTA in part 5.
- The word "bilateral", and "in transactions ranging from €10M to €50M".

## Banned lines
- Sales clichés: "exactly where we fit," "built for," "the problem we solve."
- Needy lines: "I'd love to," "hope this finds you well," "at your earliest
  convenience," "please don't hesitate."
- Market-narrative filler, or any line describing the LP back to themselves.

## A light QA — read it aloud, does it flow?
- `to:` present; `.html` newer than the `.md`. Three bullet labels bold, a real list.
- Five parts, in order. No "bilateral" anywhere.
- Part 2 is hedged and generic — no company name, no quoted LP facts.
- No em-dashes, no semicolons. Body 100–150 words. Numbers all match Fund facts.
- The close is the CTA verbatim, one block, deck sentence included.

## Example
Dear Mr. Gentile,

We are currently fundraising for our European opportunistic private credit fund
backed by real estate collateral, in tickets of €10M to €50M.

We think our strategy might fit into your portfolio and may nicely complement a
book taking its first steps into alternatives.

We are targeting €400M by April 2027. €50M is committed and €1M is our own.

- **Track Record:** €1.35B underwritten previously at a 19% IRR, over 50 years of combined experience.
- **Current Dynamics:** €50M committed and a €100M+ proprietary pipeline.
- **Target Returns:** 15%+ net IRR to LPs (15%+ unlevered at the asset level).

Please find attached our presentation. If you are interested, I would be happy to have a 20 minute short introductory call.

Kind regards,

Jozef Martinak
Partner, Valori Capital

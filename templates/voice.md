# VOICE — canon. Structure v4 (2026-07-21), from live drafting calibration.

## The feel we are going for
A short, human email from one partner to one investor. It should read like someone
who did their homework wrote it in one sitting: a clear reason for the note, a
confident but unforced pitch, and an easy close. It flows. It is not a form filled in.
If a draft reads like it was assembled from slots, loosen it until it sounds like a
person talking.

## Output format (every draft)
- Frontmatter carries `to:` = recipient email. Always present.
- Ship BOTH a `.md` and a `.html` (Outlook paste-ready) per draft. Regenerate the
  `.html` whenever the `.md` changes: the sending bot reads the `.html`, so a
  stale twin puts the old wording or spacing into Outlook.
- The three bullets are a real list with the label before the colon in bold.
- Four breaks in every body, so it breathes on a phone screen: after the
  salutation, after the opening sentence, before the closing sentence, and after
  the sign-off line so the name sits apart. `scripts/respace.py` applies these.

## How it usually flows (a guide, not a fixed order)
- **The opener — the "I'm reaching out" method (this tested best, use it).**
  Open with the READER'S situation and the payoff they would want, so the first
  thing they read is why they should care — not what we do. Lead with the fit,
  then the product. Pattern:
    "I'm reaching out because our approach fits [a general framing of their situation
    that carries the benefit]. We provide private credit backed by European real
    estate, secured and bilateral, in tickets of €10M to €50M."
  Worked example (this is the model):
    "Dear Mr. Greco,
     I'm reaching out because our approach fits a large book that wants more yield
     without taking on more risk. We provide private credit backed by European real
     estate, secured and bilateral, in tickets of €10M to €50M, protection ahead of yield."
  Rules for the opener:
  - The fit clause comes from the LP's research, framed GENERALLY, and IMPLIES we can
    help without ever saying "we can help you" — e.g. "a large book that wants more
    yield without more risk," "a book already active in real assets," "a fund with
    room to put private capital to work." It changes per LP; that is the main variety.
  - Vary only lightly within the family: "I'm reaching out because…" / "I wanted to
    reach you because…" / "there may be a fit for…". Do NOT reach for clever
    fit-first openers ("A large book can…", "Yield is hard to find…") — they read cheesy.
  - The product line is "private credit backed by European real estate" (the correct
    term — NOT "secured European real estate credit" alone, and never "private debt"
    as the label). Never open with what we do or with the LP's company name, and never
    quote their figures or deals.
- **Second opener (rotate with the first — keep BOTH for variety).** Sometimes lead
  with what we run and tie it to their portfolio, based on their research:
    "We run a private credit strategy backed by European real estate, which would be a
    natural fit to [a research-based framing of their portfolio]."
  Use the present tense ("We run", "We provide") — never "we are building". The fund is
  a first vintage, but the TEAM is experienced (€1.35B underwritten at 19% IRR). Frame
  fundraising as "our first vintage under the Valori brand", not "our first fund" — the
  brand is new, the team is not. The "[…]" changes per LP from their research (e.g.
  "a large, bond-led book," "a book already active in real assets," "a fund with room
  to put private capital to work"). Alternate with the "I'm reaching out" opener so no
  two in a row are alike.
- **Into motion.** Bring the fund in mid-motion — the first vintage is underway
  (raising, placing, building, assembling), with the status woven in and one genuine
  personal touch (handling it himself, the partners' own €1M in the fund, a region or
  segment note, a personal offer of time).
- **The proof — three bullets.** The trust block below, carried as a real list.
- **The close — deck + explicit ask for a call (fixed).** One short closing that
  attaches the deck and explicitly asks for a call:
    "Our deck is attached. If a specialised European real asset debt manager fits your
    current mandate or co-investment interests, I would welcome a brief introductory call."
  Keep it verbatim. It must explicitly request the call (not a soft "happy to chat").
  Drop "or co-investment interests" only for a pension/insurer with clearly no
  co-invest programme.

Let the order breathe. If the pitch reads better before the fit line, or the personal
touch belongs in the close, or the ticket size sits best in the hook — move it. The
point is flow, not sequence. Just do not skip the fixed points below.

## The three bullets (the trust block — exact numbers, these three)
- **Track Record:** €1.35B underwritten previously at a 19% IRR, over 50 years of combined experience.
- **Current Dynamics:** €50M committed and a €100M+ proprietary pipeline, mostly bilateral.
- **Target Returns:** 15%+ net IRR to LPs (15%+ unlevered at the asset level).

## Fixed points (do not drift on these)
- Fund-facts numbers verbatim; never improvise a figure.
- The three bold bullets above, and the deck line exactly once.
- Never open the body with the LP's company name.
- Research shows through the angle, never quoted back at them, never framed as
  something they asked for or showed interest in.
- No em-dashes. No semicolons.
- Salutation "Dear Mr./Ms. Surname" (surname only). Sign-off "Kind regards," /
  Jozef Martinak / Partner, Valori Capital (English always).
- Body roughly 120–190 words. Secular values only. Contractions optional and light.

## Vary, always (this is a style, not a template)
- No two consecutive LPs should share an opener framing, a mid-motion verb, a personal
  touch, or a close. If a line could be pasted into any email, cut it.
- Pick the angle — protection, real-asset credit, reliable yield, yield-without-risk —
  that fits THIS LP's file.

## Banned lines
- Sales clichés: "exactly where we fit," "built for," "clear line between what you do
  and what we offer," "the problem we solve," "I'd rather test that than assume it."
- Needy lines: "I'd love to," "hope this finds you well," "worth both our time,"
  "at your earliest convenience," "please don't hesitate."
- Market-narrative filler, or any line describing the LP back to themselves.

## A light QA — read it aloud, does it flow?
- `to:` present; `.html` generated. Three bullet labels bold, a real list.
- The hook names the fit through a general research-framing — no company name first,
  no quoted LP facts.
- One genuine personal touch, not reused from the last LP.
- No em-dashes, no semicolons. Body 120–190 words. Deck line once. Numbers all match
  Fund facts. No banned lines. Close is confident and different from recent drafts.

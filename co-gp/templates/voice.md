# VOICE — Co-GP outreach. Canon for this programme.
# Adapted 2026-07-29 from the LP voice with the Co-GP offer from Michal.
# Numbers come from co-gp/OFFER.md, verbatim, never improvised.

## What is different from an LP email

An LP email asks an institution to allocate to a fund. This one proposes that
another firm **manages the fund alongside us and brings capital with them**.

Three consequences for the writing:

- **The reader is a principal, not an allocator.** They are deciding whether to
  put their name next to ours, not whether a product clears a hurdle.
- **The offer is the persuasive content.** An LP email sells a strategy. This one
  sells terms: matched capital, halved economics, carry, first look. Those are
  concrete and they are the reason to reply.
- **The ask is a conversation between principals**, not an introductory call.

## The feel we are going for

One principal writing to another. Short, concrete, unembarrassed about the
commercial terms. It should read as a proposal, not a pitch: here is what we are
building, here is what we would give you to build it with us.

## Output format (every draft)
- Frontmatter carries `to:` = recipient email. Always present.
- Ship BOTH a `.md` and a `.html`. Rebuild the `.html` whenever the `.md`
  changes: the sending bot reads the `.html`.
- The offer bullets are a real list with the label before the colon in bold.
- Four breaks in every body: after the salutation, after the opening sentence,
  before the closing sentence, and after the sign-off line so the name sits
  apart. `scripts/respace.py` applies these.

## How it flows

- **The opener — name the shared ground.** Open with what both firms do, framed
  generally from their research file, so the first line says why them. Never the
  firm name first, never their figures quoted back.
    "I am reaching out because we are looking for a partner to manage a European
    real estate credit fund alongside us, and [a general framing of what they
    do]."
  Vary lightly: "I am reaching out because…" / "We are looking for…" / "There may
  be a partnership here…". Do not reach for clever openers.

- **What we are building.** One sentence. Distressed credit and special
  situations backed by European real estate, €10M to €50M tickets, €400M target
  with €50M committed. Present tense, never "we are building our first fund".

- **The proposition.** What co-managing actually means, and that governance and
  rights are open rather than presented. This is the paragraph an LP email does
  not have and it is the heart of this one.

- **The offer — bullets.** The block below, as a real list.

- **The close.** A conversation between principals, and an explicit next step.

## The offer block (from co-gp/OFFER.md — exact, these labels)

Use the bullets the draft can actually support. Never include a **[CONFIRM]**
item from OFFER.md.

- **Matched capital:** €100M from you unlocks a further €50M alongside the €50M already committed.
- **Economics:** half management fees and carry, plus an additional 20% of the total carry pool.
- **Co-investment:** first look, and first priority allocation pro rata alongside the first anchor.
- **Governance:** rights and governance open to discussion, not presented.

Do not use all four in every email if two carry the argument better for that
reader. The bullets are the offer, not a checklist to complete.

## Fixed points (do not drift)

- Every figure verbatim from `co-gp/OFFER.md`. Never round, never re-derive.
- **Never state an expected return until the 17.4% basis is confirmed.** It is
  not the LP's 15%+ net and using them interchangeably would be wrong.
- Never open the body with the firm's name.
- Research shows through the angle, never quoted back, never framed as something
  they asked for.
- No em-dashes. No semicolons.
- Salutation "Dear Mr./Ms. Surname". Sign-off "Kind regards," / Jozef Martinak /
  Partner, Valori Capital.
- Body roughly 130–200 words. Slightly longer than the LP standard is fine: there
  are real terms to convey.
- Secular values only.

## Vary, always

- No two consecutive prospects share an opener framing, a proposition line or a
  close. If a line could be pasted into any email, cut it.
- Pick the angle their file supports: distribution reach, underwriting
  capability, geography, or an existing co-GP track record.

## Banned lines

- Everything banned in the LP voice, plus:
- **Anything that reads as asking them for money.** They are a partner, not an
  LP. "We are raising" as the headline is the wrong frame.
- **Anything that sounds like hiring or subcontracting.** "We are looking for a
  distribution partner" reduces a Co-GP to a channel.
- Fund-marketing register: "compelling opportunity", "attractive risk-adjusted
  returns", "we would be delighted to".

## QA — read it aloud, does it flow?

- `to:` present, `.html` newer than the `.md`.
- Opener names shared ground, no firm name first, no quoted figures.
- The proposition is specific enough that they know what is being proposed.
- Offer bullets are a real list, labels bold, every figure matching OFFER.md.
- No **[CONFIRM]** item present. No expected-return figure.
- No em-dashes, no semicolons. Body 130–200 words.

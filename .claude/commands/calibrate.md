Self-correction pass. Drafts nothing, sends nothing.

1. For every file in /sent/, diff my final version against the matching
   file in /drafts/. Drafts sit at drafts/<language>/<list>/ (e.g.
   drafts/en/pension-funds/, drafts/de/insurance/), so search every language
   bucket and every type folder inside it for the slug.
   ALSO search .archive/ . Once an LP is sent its draft is moved out of the
   working folder into .archive/sent-drafts-for-calibration/ so that /drafts/
   only ever shows pending work. Those archived drafts are the other half of
   every diff: skip them and calibration silently finds nothing to compare.
   Compare like with like: a Slovak sent email against its Slovak draft. When
   you report a pattern, say which language bucket it came from, since register
   and phrasing edits rarely transfer across languages.
2. Find edit patterns appearing 2+ times: words I remove, phrasing I
   change, how I rewrite bridges, length trims.
3. Where an edit pattern is clearly tied to one LP type, say so in the
   finding. Do not split learnings.md by type unless I ask.
4. Update templates/learnings.md directly:
   - "Confirmed" needs 2+ occurrences, "Hypotheses" for single ones,
     retire anything I've stopped doing.
5. If a pattern is strong (3+ occurrences), propose the exact one-line
   change to voice.md and wait for my yes. Never edit voice.md or
   CLAUDE.md yourself.
6. Finish with 3 lines: my most common edit, what you'll do differently
   in the next draft, current draft acceptance trend (sent unchanged vs
   edited).

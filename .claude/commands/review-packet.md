Compile current drafts into printable review files.

Drafts live at drafts/<language>/<list>/ — see FOLDER ROUTING in draft.md.

SCOPE — pass $ARGUMENTS straight through to the builder:
  a language bucket   en | sk | de
  a list              insurance | pension-funds
  a bucket and type   sk/insurance
  nothing             everything
Matching is exact, so "de" means the German bucket and never
"multilateral-development-banks".

RUN THE BUILDER — do not retype drafts by hand. This is deterministic, the
same way /draft never hand-writes the .html twin:

  .venv/bin/python scripts/build_packet.py               # everything
  .venv/bin/python scripts/build_packet.py en            # one language bucket
  .venv/bin/python scripts/build_packet.py sk/insurance  # one bucket and type

It writes three levels, using the layout below for each draft:
  drafts/<lang>/<list>/REVIEW-PACKET.md   one per list folder in scope
  drafts/<lang>/REVIEW-PACKET.md          one per language bucket
  drafts/REVIEW-PACKET.md                 roll-up across all languages
   - A header line: "## [LP name] — [bridge short label] ([variant letter])"
     pulled from the frontmatter (lp, bridge, filename suffix).
   - Subject line.
   - Full email body (salutation through sign-off).
   - A horizontal rule (---) between drafts.
At the top of each file: a title naming the bucket and type, then a table
   | LP | Variant | Bridge | Words |
Folders holding no drafts are skipped silently. A scoped run leaves the
bucket and roll-up packets alone rather than truncating them to the subset.

The per-language packet is the one to print for a sending session: one file,
one language, every pending draft in it.

Relay the script's output: one line per folder with its draft count, then the
total. If a draft is missing from a packet, its .md is not in a language and
type folder — check FOLDER ROUTING in draft.md.

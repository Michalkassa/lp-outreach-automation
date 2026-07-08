Compile all current drafts into one printable review file.

1. Read every .md file in /drafts/ (sorted alphabetically by filename).
2. Create /drafts/REVIEW-PACKET.md with this layout for each draft:
   - A header line: "## [LP name] — [bridge short label] ([variant letter])"
     pulled from the frontmatter (lp, bridge, filename suffix).
   - Subject line.
   - Full email body (salutation through sign-off).
   - A horizontal rule (---) between drafts.
3. At the top of the file add a summary table:
   | LP | Variant | Bridge | Words |
   One row per draft, values from frontmatter.
4. Print the total number of drafts compiled.

Draft the one-time first-touch email for the LP in $ARGUMENTS.

LANGUAGE DETECTION (apply in this order — first match wins):
1. If $ARGUMENTS contains a language code after the LP name (e.g. "/draft Grawe en"),
   use that language for this run only. Do not save it to the LP file.
2. If the LP file has "Language override:" set to en, sk, or de, use that.
3. Otherwise, derive from the LP's country field:
   - Slovakia or Czechia → sk → templates/voice-sk.md
   - Austria or Germany → de → templates/voice-de.md
   - All other countries → en → templates/voice.md

The country rule decides the language. An Austrian LP gets a German email even
when the surrounding batch is English. English mode was tried on 2026-07-28 and
reverted the same day: write these LPs in their own language.

DRAFT COUNT (apply in this order — first match wins):
1. If $ARGUMENTS contains a number 1-3 after the LP name (e.g. "/draft Grawe 2"
   or "/draft Grawe en 2"), write that many variants for this run only.
   Do not save it to the LP file.
2. If the LP file has "Draft count:" set to 1, 2, or 3, use that.
3. Otherwise write 3.
Variants follow bridge-candidate rank: 1 draft = top bridge only,
2 drafts = bridges 1 and 2, 3 drafts = all three angles.

1. Read /lps/<lp-slug>.md (if missing, offer /research and stop).
   Read the correct voice template (see above), templates/learnings.md,
   templates/sent-examples.md (the user's 15 gold-standard edited emails — draw
   phrasing, structure and register from them, never copy verbatim), and
   templates/caption.md (the Subject-line rules). Apply learnings.
   Generate the Subject strictly per templates/caption.md
   ("Valori Capital, [category], [rotating ending]"), rotating the ending across LPs.
2. Write the chosen number of draft variations (lettered A, B, C in
   rank order), each led by a different fit angle (the general framing of
   the LP's world from their file — see templates/voice.md). Each draft must:
   - Follow templates/voice.md — treat it as a flow, not a rigid form
   - 120 to 190 words (body only, not subject/salutation/sign-off)
   - Fully translated into the target language. "Valori Capital" and
     "Partner, Valori Capital" in the sign-off stay in English always.
   - Plain, direct language, no corporate filler. Contractions optional and
     light (formal SK/DE use none).
   - No political or religious statements
   - Address the primary contact (CIO first) from the LP file
3. Run the QA list in the voice template silently; fix fails before showing.
   Show pass/fail table after drafts.
4. Save each to /drafts/<language>/<list-folder>/YYYY-MM-DD-<lp-slug>-A.md
   (and -B.md, -C.md if more than one) with frontmatter: lp, to (recipient
   email from the LP file / tracker; FIND if unconfirmed), contact, bridge,
   category_label, word_count, language.
   <language> is the language resolved above (en, sk or de) and must match the
   `language` column in output.csv. <list-folder> is insurance/ or
   pension-funds/, from the LP's `list` column. See FOLDER ROUTING below.
5. OUTLOOK FORMATTING (automatic — always run, never skip). Immediately
   after writing the .md files, generate the Outlook paste-ready .html twin
   for each by running the formatter on exactly the files you just wrote:
     .venv/bin/python scripts/format_html.py <each .md path you wrote>
   This is deterministic — do NOT hand-write the HTML. The script bolds the
   three bullet labels, renders a real <ul> list, and adds the To/Subject
   header. Confirm it printed "formatted: ..." for every draft; if any .md
   is edited later, re-run the same command (or scripts/format_html.py --all)
   to refresh its twin. This is not optional: make_draft.py reads the .html, so
   a .md edited without rebuilding its twin sends the OLD text.
   Then run the spacing pass, which rebuilds the twins itself:
     .venv/bin/python scripts/respace.py <each .md path you wrote>
6. output.csv: stage=drafted. Note how many drafts were saved (each with its
   .html twin), nothing sent.
7. Refresh the workbooks so the new stage is visible to Michal:
     .venv/bin/python scripts/convert.py export
     .venv/bin/python scripts/convert.py sync
   A draft that exists but still reads `research` in input.xlsx and output.xlsx
   is a draft he cannot see.

FOLDER ROUTING — every draft lives at drafts/<language>/<list>/.
Language bucket first, then the list it belongs to:

  drafts/en/   all countries except those listed below
  drafts/sk/   Slovakia, Czech Republic
  drafts/de/   Austria, Germany

Inside each bucket there are exactly TWO folders, named for the two source
lists. Use the `list` column in output.csv:

  list = Pension funds  → pension-funds/
  list = Insurance      → insurance/

Never create a third folder. The `list` column is derived from `type`:
anything whose type contains "Pension" is Pension funds, everything else is
Insurance. A bank, a development agency or any other entity type is not a
separate folder, it just belongs to whichever list it came in on.

So an Austrian insurer goes to drafts/de/insurance/, an Italian pension fund
to drafts/en/pension-funds/, and a development bank to insurance/.

New entity types will be added later. They still resolve to one of these two
folders. If a genuinely new LIST is ever introduced, ask before adding a
third folder rather than inventing one.

Never write a draft to the /drafts/ root or straight into a language bucket.
Only REVIEW-PACKET files live at those two levels.

DATA FILE: data/output.csv — semicolons (;) as delimiter. No semicolons inside field values.
Columns: country;language;type;list;company;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent
Score is a plain integer 1-100 (not "90/100").

STAGE CHANGES MUST REACH BOTH WORKBOOKS — never skip this.
data/output.csv is the source of truth, but Michal reads input.xlsx and
output.xlsx. A stage written only to the CSV is invisible to him, and the two
files then disagree until something happens to resync them. Immediately after
any stage change, run BOTH:

  .venv/bin/python scripts/convert.py export   # data/output.csv -> output.xlsx
  .venv/bin/python scripts/convert.py sync     # stage + score  -> input.xlsx

Then confirm the three sources agree. `scripts/pipeline_status.py` reports the
funnel; the two workbooks must show the same counts. If Excel has either file
open the write fails silently for him, so say so in your reply when that is
possible.

Draft the one-time first-touch email for the LP in $ARGUMENTS.

LANGUAGE DETECTION (apply in this order — first match wins):
1. If $ARGUMENTS contains a language code after the LP name (e.g. "/draft Grawe en"),
   use that language for this run only. Do not save it to the LP file.
2. If the LP file has "Language override:" set to en, sk, or de, use that.
3. Otherwise, derive from the LP's country field:
   - Slovakia or Czechia → sk → templates/voice-sk.md
   - Austria or Germany → de → templates/voice-de.md
   - All other countries → en → templates/voice.md

DRAFT COUNT (apply in this order — first match wins):
1. If $ARGUMENTS contains a number 1-3 after the LP name (e.g. "/draft Grawe 2"
   or "/draft Grawe en 2"), write that many variants for this run only.
   Do not save it to the LP file.
2. If the LP file has "Draft count:" set to 1, 2, or 3, use that.
3. Otherwise write 3.
Variants follow bridge-candidate rank: 1 draft = top bridge only,
2 drafts = bridges 1 and 2, 3 drafts = all three angles.

1. Read /lps/<lp-slug>.md (if missing, offer /research and stop).
   Read the correct voice template (see above) and templates/learnings.md.
   Apply learnings.
2. Write the chosen number of draft variations (lettered A, B, C in
   bridge rank order), each using a different bridge angle from the LP
   file's Bridge Candidates section. Each draft must:
   - Follow the structure in the voice template (intro / bullets / close)
   - 200 to 230 words (body only, not subject/salutation/sign-off)
   - Fully translated into the target language. "Valori Capital" and
     "Partner, Valori Capital" in the sign-off stay in English always.
   - Plain, direct language — no corporate filler, no contractions
   - No political or religious statements
   - Address the primary contact from the LP file
3. Run the QA list in the voice template silently; fix fails before showing.
   Show pass/fail table after drafts.
4. Save each to /drafts/YYYY-MM-DD-<lp-slug>-A.md (and -B.md, -C.md if
   more than one) with frontmatter: lp, contact, bridge, category_label,
   word_count, language.
5. output.csv: stage=drafted. Note how many drafts were saved, nothing sent.

DATA FILE: data/output.csv — semicolons (;) as delimiter. No semicolons inside field values.
Columns: country;company;type;slug;score;aum;contact_name;contact_title;contact_email;stage;category;bridge;flag;date_sent
Score is a plain integer 1-100 (not "90/100").

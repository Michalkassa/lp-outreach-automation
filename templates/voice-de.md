# VOICE-DE — Kanon für deutschsprachige LPs (Österreich, Deutschland).
# Struktur v5 (2026-08-03). Deutsche Fassung von templates/voice.md, gleiche
# Prinzipien und gleiche feste Punkte.
#
# v5 ersetzt v4: der alte Einstieg und der Absatz "in Bewegung" mit persönlichem
# Touch sind gestrichen. Die Präsentation wird wieder erwähnt, aber nur in der
# zweisätzigen CTA in Teil 5.

## Das Gefühl, das wir wollen
Eine kurze, sachliche E-Mail von einem Partner an einen Investor. Sie sagt, was
wir platzieren, warum es passen könnte, was dahintersteht, und bittet um ein
kurzes Gespräch. Kein Anlauf, keine Verkaufsfloskeln. Wenn ein Satz keine dieser
vier Aufgaben erfüllt, streichen Sie ihn.

## Ausgabeformat (jeder Draft)
- Frontmatter enthält `to:` = Empfänger-E-Mail. Immer vorhanden.
- Immer BEIDES: `.md` und `.html` (Outlook-fertig). Das `.html` neu erzeugen,
  sobald sich das `.md` ändert: das Versandskript liest das `.html`.
- Die drei Aufzählungspunkte sind eine echte Liste, Label vor dem Doppelpunkt fett.
- Vier Absatzumbrüche in jedem Text: nach der Anrede, nach dem ersten Satz, vor
  dem Schlussblock und nach der Grußformel. `scripts/respace.py` setzt sie. Der
  Schlussblock besteht aus zwei Sätzen und wird nie getrennt.

## Die Struktur (v5 — fünf Teile, in dieser Reihenfolge)

**1. Was wir platzieren.** Eröffnet den Text. Zuerst das Produkt, kein Vorlauf.

    "Wir sammeln derzeit Kapital für unseren europäischen opportunistischen
    Private-Credit-Fonds, besichert durch Immobilien, in Tickets von €10 Mio.
    bis €50 Mio."

  - Produktname: **"europäischer opportunistischer Private-Credit-Fonds,
    besichert durch Immobilien"**. Vollständig verwenden.
  - Die Tickets von €10 Mio. bis €50 Mio. gehören in diesen Satz.
  - **Das Wort "bilateral" ist gestrichen.** Es kommt im Text nicht mehr vor.

**2. Warum es passen könnte.** Ein Satz, zurückhaltend, allgemein.

    "Wir denken, dass unsere Strategie in Ihr Portfolio passen könnte und
    [eine allgemeine Rahmung ihrer Situation] gut ergänzen würde."

  - "Wir denken" und "könnte" bleiben. Wir bieten an, wir behaupten nicht.
  - Nur die Rahmung nach "ergänzen würde" wechselt, aus dem Research und immer
    ALLGEMEIN: "eine konservative, anleihenlastige Bilanz" · "ein Haus, das
    bereits in Real Assets investiert ist" · "ein Portfolio mit Spielraum für
    private Anlagen" · "eine Bilanz, die erste Schritte in Alternatives macht".
  - Nennen Sie das Haus nicht, zitieren Sie keine ihrer Zahlen, beschreiben Sie
    ihnen nicht ihre eigene Position.

**3. Wo die Platzierung steht.** Eigener kurzer Absatz.

    "Wir streben €400 Mio. bis April 2027 an. €50 Mio. sind zugesagt und
    €1 Mio. ist unser eigenes Kapital."

  - Formulierung leicht variieren, die Zahlen nie.
  - Präsens. Nie "wir bauen auf".

**4. Der Beleg — drei Punkte.** Der Trust-Block unten als echte Liste.

**5. Die Bitte.** Der Schlussblock, allein stehend. ZWEI Sätze, EIN Block.

    "Anbei finden Sie unsere Präsentation. Bei Interesse würde ich mich über ein kurzes 20-minütiges Einführungsgespräch freuen."

  - Wörtlich beibehalten. Der Satz zur Präsentation und die Bitte um das
    Gespräch bleiben zusammen in einem Block, nicht getrennt.
  - "Bei Interesse" ist das Gelenk: es macht das Gespräch bedingt statt gesetzt.
  - Bittet um eine konkrete, kleine Zusage. Die 20 Minuten bleiben.
  - Die Präsentation wird erwähnt, also muss sie beim Versand angehängt sein.

## Die drei Aufzählungspunkte (Trust-Block, exakte Zahlen, genau diese drei)
- **Track Record:** 50+ Jahre kombinierte Erfahrung, zuvor €1,35 Mrd. bei 19% IRR gezeichnet.
- **Aktuelle Dynamik:** €50 Mio. bereits zugesagt und eine proprietäre Pipeline von über €100 Mio.
- **Zielrendite:** 15%+ Netto-IRR für die LPs (15%+ unlevered auf Asset-Ebene).

## Feste Punkte (hier nie abweichen)
- Fund-Facts-Zahlen wörtlich; nie eine Zahl erfinden.
- Die drei fetten Punkte oben, genau so wie geschrieben.
- Nie mit dem Firmennamen des LP beginnen.
- Research zeigt sich in der Rahmung in Teil 2, nie zurückgespiegelt.
- Keine Gedankenstriche. Keine Semikolons. Kein "bilateral".
- Anrede "Sehr geehrter Herr [Nachname]," / "Sehr geehrte Frau [Nachname],".
  Grußformel "Mit freundlichen Grüßen," / Jozef Martinak / Partner, Valori Capital
  (Firmenname und Titel immer englisch).
- Haupttext etwa 100–150 Wörter. Durchgehend "Sie". Keine Kontraktionen.
  Nur säkulare Werte.
- Etablierte Fachbegriffe bleiben englisch: Private Credit, Distressed Credit,
  Special Situations, Track Record, IRR, LP, GP, Pipeline, unlevered.

## Immer variieren
- Teil 1, 4 und 5 sind nahezu fest. Die Variation liegt in der Rahmung in Teil 2
  und leicht in der Formulierung von Teil 3.
- Zwei aufeinanderfolgende LPs teilen nie dieselbe Rahmung nach "ergänzen würde".

## In v5 gestrichen (nicht wieder einführen)
- Der Einstieg "Ich wende mich an Sie, weil unsere Strategie gut zu … passt".
- Der Absatz "in Bewegung" mit persönlichem Touch.
- Der alte Abschluss. Ersetzt durch die einzelne zweisätzige CTA in Teil 5.
- Das Wort "bilateral".

## Kurze QA — laut lesen, fließt es?
- `to:` vorhanden, `.html` neuer als das `.md`. Drei Labels fett, echte Liste.
- Fünf Teile in der Reihenfolge. Nirgends "bilateral".
- Teil 2 ist zurückhaltend und allgemein, ohne Firmennamen und ohne ihre Zahlen.
- Keine Gedankenstriche, keine Semikolons. 100–150 Wörter. Alle Zahlen stimmen
  mit den Fund Facts.
- Der Schluss ist die CTA wörtlich, ein Block, inklusive Präsentationssatz.

## Beispiel
Sehr geehrter Herr Muster,

Wir sammeln derzeit Kapital für unseren europäischen opportunistischen
Private-Credit-Fonds, besichert durch Immobilien, in Tickets von €10 Mio. bis
€50 Mio.

Wir denken, dass unsere Strategie in Ihr Portfolio passen könnte und eine
konservative, anleihenlastige Bilanz gut ergänzen würde.

Wir streben €400 Mio. bis April 2027 an. €50 Mio. sind zugesagt und €1 Mio. ist
unser eigenes Kapital.

- **Track Record:** 50+ Jahre kombinierte Erfahrung, zuvor €1,35 Mrd. bei 19% IRR gezeichnet.
- **Aktuelle Dynamik:** €50 Mio. bereits zugesagt und eine proprietäre Pipeline von über €100 Mio.
- **Zielrendite:** 15%+ Netto-IRR für die LPs (15%+ unlevered auf Asset-Ebene).

Anbei finden Sie unsere Präsentation. Bei Interesse würde ich mich über ein kurzes 20-minütiges Einführungsgespräch freuen.

Mit freundlichen Grüßen,

Jozef Martinak
Partner, Valori Capital

"""Build the pipeline showcase presentation — Valori style."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import math

# ── Palette ──────────────────────────────────────────────────────────
CORAL     = RGBColor(0xEF, 0x7B, 0x88)
CORAL_LT  = RGBColor(0xF4, 0xA5, 0xAE)
CORAL_XLT = RGBColor(0xFB, 0xE0, 0xE3)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
OFF_WHITE = RGBColor(0xF7, 0xF7, 0xF7)
LIGHT_GR  = RGBColor(0xF0, 0xF0, 0xF0)
MID_GRAY  = RGBColor(0x99, 0x99, 0x99)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
CHARCOAL  = RGBColor(0x2A, 0x2A, 0x2A)
BLACK     = RGBColor(0x00, 0x00, 0x00)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

SERIF = "Georgia"
SANS  = "Calibri"
MONO  = "Consolas"

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
BLANK = prs.slide_layouts[6]


# ── Helpers ──────────────────────────────────────────────────────────
def set_bg(slide, color=WHITE):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def rect(slide, l, t, w, h, fill=CORAL, border=None, bw=Pt(1)):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if border:
        sh.line.color.rgb = border
        sh.line.width = bw
    else:
        sh.line.fill.background()
    return sh


def txt(slide, l, t, w, h, text, sz=18, color=DARK_GRAY, bold=False,
        align=PP_ALIGN.LEFT, font=SANS, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = text
    tf.paragraphs[0].font.size = Pt(sz)
    tf.paragraphs[0].font.color.rgb = color
    tf.paragraphs[0].font.bold = bold
    tf.paragraphs[0].font.name = font
    tf.paragraphs[0].alignment = align
    return tb


def multi(slide, l, t, w, h, lines, sz=14, color=DARK_GRAY, bold=False,
          align=PP_ALIGN.LEFT, font=SANS, spacing=1.5):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(sz)
        p.font.color.rgb = color
        p.font.bold = bold
        p.font.name = font
        p.alignment = align
        p.space_after = Pt(sz * (spacing - 1))
    return tb


def page_num(slide, num):
    txt(slide, Inches(0.5), Inches(7.05), Inches(0.5), Inches(0.3),
        str(num), sz=9, color=CORAL, font=SANS)


def accent_line(slide, l, t, w):
    """Thin horizontal coral accent line."""
    rect(slide, l, t, w, Pt(2), fill=CORAL)


def sidebar(slide, label, width=Inches(2.5)):
    """Left coral sidebar with white uppercase label."""
    rect(slide, 0, 0, width, SLIDE_H, fill=CORAL)
    tb = slide.shapes.add_textbox(
        Inches(0.3), Inches(1.5), width - Inches(0.6), Inches(4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = label.upper()
    p.font.size = Pt(22)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.font.name = SERIF
    p.alignment = PP_ALIGN.LEFT
    p.line_spacing = Pt(30)
    return width


def section_heading(slide, text_str):
    """Coral uppercase section heading inside content area."""
    txt(slide, Inches(3.0), Inches(0.8), Inches(9), Inches(0.4),
        text_str.upper(), sz=12, color=CORAL, bold=True, font=SANS)


def screenshot_box(slide, l, t, w, h, label):
    """Sharp-edged dashed placeholder for screenshot."""
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = OFF_WHITE
    sh.line.color.rgb = MID_GRAY
    sh.line.width = Pt(1)
    sh.line.dash_style = 2  # dash
    tf = sh.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].text = label
    tf.paragraphs[0].font.size = Pt(11)
    tf.paragraphs[0].font.color.rgb = MID_GRAY
    tf.paragraphs[0].font.name = SANS
    tf.paragraphs[0].font.italic = True
    return sh


def add_diagonal_stripes(slide, base_color=LIGHT_GR):
    """Subtle diagonal stripe decoration on section divider slides."""
    stripes = [
        (Inches(6), Inches(-1), Inches(1.8), Inches(10)),
        (Inches(8), Inches(-1), Inches(1.2), Inches(10)),
        (Inches(9.5), Inches(-1), Inches(2.5), Inches(10)),
        (Inches(11.5), Inches(-1), Inches(1.5), Inches(10)),
    ]
    for l, t, w, h in stripes:
        sh = slide.shapes.add_shape(
            MSO_SHAPE.PARALLELOGRAM, l, t, w, h)
        sh.fill.solid()
        sh.fill.fore_color.rgb = base_color
        sh.line.fill.background()
        # Set transparency via XML on the spPr element
        try:
            spPr = sh._element.find(qn('p:spPr'))
            if spPr is None:
                spPr = sh._element.find(qn('p:sp')).find(qn('p:spPr'))
            sf = spPr.find(qn('a:solidFill'))
            if sf is not None:
                clr_el = sf[0]
                alpha = clr_el.makeelement(qn('a:alpha'), {'val': '25000'})
                clr_el.append(alpha)
        except Exception:
            pass


def step_box(slide, l, t, w, h, num, label, sublabel=None):
    """Numbered step with coral number badge and dark text."""
    # Number
    badge = rect(slide, l, t, Inches(0.4), Inches(0.4), fill=CORAL)
    tf = badge.text_frame
    tf.paragraphs[0].text = str(num)
    tf.paragraphs[0].font.size = Pt(14)
    tf.paragraphs[0].font.color.rgb = WHITE
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.name = SANS
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Label
    txt(slide, l + Inches(0.55), t, w - Inches(0.6), Inches(0.35),
        label, sz=13, color=DARK_GRAY, bold=True)
    if sublabel:
        txt(slide, l + Inches(0.55), t + Inches(0.3), w - Inches(0.6),
            Inches(0.25), sublabel, sz=10, color=MID_GRAY)


# ════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title (full coral background like inspiration)
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, CORAL)
add_diagonal_stripes(s, CORAL_LT)

txt(s, Inches(2), Inches(3.0), Inches(9), Inches(1),
    "Semi-Automatic\nFundraising Pipeline",
    sz=38, color=WHITE, bold=True, font=SERIF)

txt(s, Inches(2), Inches(5.0), Inches(9), Inches(0.4),
    "Valori Capital", sz=20, color=WHITE, bold=True, font=SERIF)

txt(s, Inches(2), Inches(5.5), Inches(9), Inches(0.4),
    "AI-assisted research, scoring, drafting", sz=14, color=WHITE, font=SANS)

txt(s, Inches(2), Inches(5.9), Inches(9), Inches(0.3),
    "Human-controlled sending", sz=14, color=WHITE, font=SANS)


# ════════════════════════════════════════════════════════════════════
# SLIDE 2 — Section Divider: Pipeline Overview
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, OFF_WHITE)
add_diagonal_stripes(s)

txt(s, Inches(1.2), Inches(3.0), Inches(8), Inches(1.2),
    "Pipeline Overview",
    sz=40, color=CORAL, bold=True, font=SERIF)

page_num(s, 2)


# ════════════════════════════════════════════════════════════════════
# SLIDE 3 — Pipeline Flow Diagram
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)

# Top accent line
accent_line(s, 0, 0, SLIDE_W)

# Title
txt(s, Inches(0.8), Inches(0.5), Inches(10), Inches(0.6),
    "THE COMPLETE PIPELINE", sz=12, color=CORAL, bold=True, font=SANS)

# Flow steps — two rows of 4
steps = [
    ("1", "Build LP Universe", "input.xlsx", CORAL),
    ("2", "Import", "/import-lps", CORAL_LT),
    ("3", "AI Research", "/research", CORAL),
    ("4", "Score & Prioritise", "1-100 rubric", CORAL_LT),
    ("5", "Draft Emails", "/draft", CORAL),
    ("6", "Human Review", "/review-packet", CORAL_LT),
    ("7", "Send & Log", "/log-sent", CORAL),
    ("8", "Calibrate", "/calibrate", CORAL_LT),
]

box_w = Inches(2.5)
box_h = Inches(1.6)
gap_x = Inches(0.35)
row1_y = Inches(1.8)
row2_y = Inches(4.5)

for i, (num, label, cmd, clr) in enumerate(steps):
    row = 0 if i < 4 else 1
    col = i if i < 4 else (7 - i)  # reverse direction on row 2
    x = Inches(0.6) + col * (box_w + gap_x)
    y = row1_y if row == 0 else row2_y

    # Box
    box = rect(s, x, y, box_w, box_h, fill=WHITE, border=LIGHT_GR, bw=Pt(1))

    # Number badge top-left
    badge = rect(s, x, y, Inches(0.45), Inches(0.45), fill=clr)
    tf = badge.text_frame
    tf.paragraphs[0].text = num
    tf.paragraphs[0].font.size = Pt(16)
    tf.paragraphs[0].font.color.rgb = WHITE
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.name = SANS
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Label
    txt(s, x + Inches(0.15), y + Inches(0.6), box_w - Inches(0.3),
        Inches(0.4), label, sz=15, color=DARK_GRAY, bold=True,
        align=PP_ALIGN.CENTER)

    # Command
    txt(s, x + Inches(0.15), y + Inches(1.05), box_w - Inches(0.3),
        Inches(0.3), cmd, sz=10, color=MID_GRAY, font=MONO,
        align=PP_ALIGN.CENTER)

    # Arrows row 1: right
    if row == 0 and i < 3:
        ax = x + box_w
        txt(s, ax, y + box_h / 2 - Inches(0.15), Inches(0.35),
            Inches(0.3), "\u203A", sz=20, color=CORAL,
            align=PP_ALIGN.CENTER)

    # Arrows row 2: left (reversed)
    if row == 1 and i < 7:
        ax = x + box_w
        txt(s, ax, y + box_h / 2 - Inches(0.15), Inches(0.35),
            Inches(0.3), "\u2039", sz=20, color=CORAL,
            align=PP_ALIGN.CENTER)

# Down arrow between rows (right side)
txt(s, Inches(0.6) + 3 * (box_w + gap_x) + box_w / 2 - Inches(0.2),
    row1_y + box_h, Inches(0.4), Inches(0.5),
    "\u2304", sz=28, color=CORAL, align=PP_ALIGN.CENTER)

# Cycle arrow text at bottom
txt(s, Inches(3), Inches(6.7), Inches(7), Inches(0.4),
    "\u21bb  Cycle repeats — each round, drafts improve from learned edits",
    sz=11, color=MID_GRAY, align=PP_ALIGN.CENTER)

page_num(s, 3)


# ════════════════════════════════════════════════════════════════════
# SLIDE 4 — Build LP Universe
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)
sw = sidebar(s, "Build LP\nUniverse")

accent_line(s, sw, 0, SLIDE_W - sw)
section_heading(s, "Fill input.xlsx with prospects")

screenshot_box(
    s, Inches(3.0), Inches(1.5), Inches(6.5), Inches(4.5),
    "\u2702 SCREENSHOT: input.xlsx in Excel\n"
    "Columns: Company, Country, First Name, Last Name,\n"
    "Title, Email, LinkedIn, Considered")

# Language box — right side
rect(s, Inches(10.0), Inches(1.5), Inches(2.8), Inches(4.5),
     fill=OFF_WHITE, border=CORAL_XLT, bw=Pt(1))

txt(s, Inches(10.2), Inches(1.7), Inches(2.4), Inches(0.3),
    "LANGUAGE", sz=10, color=CORAL, bold=True)

accent_line(s, Inches(10.2), Inches(2.1), Inches(2.4))

lang_lines = [
    "SK / CZ  \u2192  Slovak",
    "AT / DE  \u2192  German",
    "Other     \u2192  English",
    "",
    "Override per draft:",
    "/draft <LP> en",
]
multi(s, Inches(10.2), Inches(2.3), Inches(2.4), Inches(2.5),
      lang_lines, sz=10, color=DARK_GRAY, font=MONO, spacing=1.8)

multi(s, Inches(10.2), Inches(4.5), Inches(2.4), Inches(1.2), [
    "\u2022  One row = one LP",
    "\u2022  Country drives language",
    "\u2022  Stage + Score auto-filled",
], sz=10, color=DARK_GRAY, spacing=1.8)

page_num(s, 4)


# ════════════════════════════════════════════════════════════════════
# SLIDE 5 — Import
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)
sw = sidebar(s, "Import\ninto\nPipeline")

accent_line(s, sw, 0, SLIDE_W - sw)
section_heading(s, "Two-step import process")

# Step boxes
step_box(s, Inches(3.0), Inches(1.8), Inches(5), Inches(0.6),
         1, "convert.py import", "Reads input.xlsx, writes lp-import.csv")
step_box(s, Inches(3.0), Inches(2.8), Inches(5), Inches(0.6),
         2, "/import-lps", "Creates stub .md files + adds rows to output.csv")

# Arrow between
txt(s, Inches(3.2), Inches(2.35), Inches(0.4), Inches(0.4),
    "\u2193", sz=16, color=CORAL, align=PP_ALIGN.CENTER)

screenshot_box(
    s, Inches(3.0), Inches(3.8), Inches(9.5), Inches(3.2),
    "\u2702 SCREENSHOT: Claude terminal running /import-lps\n"
    "Show the summary table: company | slug | contact | status")

page_num(s, 5)


# ════════════════════════════════════════════════════════════════════
# SLIDE 6 — AI Research
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)
sw = sidebar(s, "AI-Powered\nResearch")

accent_line(s, sw, 0, SLIDE_W - sw)
section_heading(s, "/research <LP> — web search, score, contacts, bridges")

screenshot_box(
    s, Inches(3.0), Inches(1.5), Inches(5.5), Inches(5.2),
    "\u2702 SCREENSHOT: Claude running /research\n"
    "Show web searches executing and\n"
    "research output being written to LP file")

# Research output items — right column with coral bullets
items = [
    ("Company Profile", "AUM, type, regulator, ownership"),
    ("Investment Strategy", "Alternatives allocation in their words"),
    ("Named Contacts", "2-3 people with titles and emails"),
    ("Bridge Candidates", "3 ranked hooks for the email"),
    ("Score 1-100", "6-layer rubric with working shown"),
]

x_right = Inches(9.0)
for i, (title, desc) in enumerate(items):
    iy = Inches(1.7) + i * Inches(1.0)
    # Coral square bullet
    rect(s, x_right, iy + Inches(0.05), Inches(0.12), Inches(0.12),
         fill=CORAL)
    txt(s, x_right + Inches(0.25), iy, Inches(3.5), Inches(0.25),
        title, sz=13, color=DARK_GRAY, bold=True)
    txt(s, x_right + Inches(0.25), iy + Inches(0.3), Inches(3.5),
        Inches(0.25), desc, sz=10, color=MID_GRAY)

page_num(s, 6)


# ════════════════════════════════════════════════════════════════════
# SLIDE 7 — Scoring & Prioritisation
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)
sw = sidebar(s, "Scoring &\nPriori-\ntisation")

accent_line(s, sw, 0, SLIDE_W - sw)
section_heading(s, "6-layer scoring rubric, 1-100 scale")

# Score tiers — table style like inspiration
tiers = [
    ("75 \u2013 100", "Top Priority", "Draft immediately"),
    ("55 \u2013 74", "Strong Prospect", "Draft when ready"),
    ("35 \u2013 54", "Medium", "Verify gaps first"),
    ("20 \u2013 34", "Low", "Keep on radar"),
    ("< 20", "Skip", "Regulatory barrier"),
]

table_x = Inches(3.0)
table_y = Inches(1.5)
row_h = Inches(0.65)

for i, (score, label, action) in enumerate(tiers):
    ry = table_y + i * row_h
    # Alternating background
    bg = CORAL if i % 2 == 0 else CORAL_XLT
    fg = WHITE if i % 2 == 0 else DARK_GRAY

    row_bg = rect(s, table_x, ry, Inches(4.5), row_h, fill=bg)

    txt(s, table_x + Inches(0.15), ry + Inches(0.15),
        Inches(1.2), Inches(0.35),
        score, sz=13, color=fg, bold=True, font=SANS)
    txt(s, table_x + Inches(1.4), ry + Inches(0.15),
        Inches(1.5), Inches(0.35),
        label, sz=13, color=fg, bold=False)
    txt(s, table_x + Inches(3.0), ry + Inches(0.15),
        Inches(1.5), Inches(0.35),
        action, sz=11, color=fg)

# Screenshot on right
screenshot_box(
    s, Inches(8.0), Inches(1.5), Inches(4.8), Inches(5.2),
    "\u2702 SCREENSHOT: output.xlsx in Excel\n"
    "Color-coded rows by stage\n"
    "Columns: company, score, contact,\n"
    "stage, bridge")

page_num(s, 7)


# ════════════════════════════════════════════════════════════════════
# SLIDE 8 — LP Research Files
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)
sw = sidebar(s, "LP Research\nFiles")

accent_line(s, sw, 0, SLIDE_W - sw)
section_heading(s, "One structured file per LP — single source of truth")

screenshot_box(
    s, Inches(3.0), Inches(1.5), Inches(5.5), Inches(5.2),
    "\u2702 SCREENSHOT: LP .md file in editor\n"
    "e.g. lps/bonus-pensionskasse-ag.md\n\n"
    "Show sections: Data, Investment Strategy,\n"
    "Contacts, Recent Activity,\n"
    "Bridge Candidates, Summary")

# Section list — right side
sections = [
    "Data",
    "Investment Strategy",
    "People & Org",
    "Contacts",
    "Recent Activity",
    "Bridge Candidates",
    "Summary",
]
for i, sec in enumerate(sections):
    sy = Inches(1.7) + i * Inches(0.7)
    # Small coral square
    rect(s, Inches(9.0), sy + Inches(0.05), Inches(0.12), Inches(0.12),
         fill=CORAL)
    txt(s, Inches(9.25), sy, Inches(3.5), Inches(0.3),
        sec, sz=13, color=DARK_GRAY)

page_num(s, 8)


# ════════════════════════════════════════════════════════════════════
# SLIDE 9 — Personalised Outreach
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)
sw = sidebar(s, "Personalised\nOutreach")

accent_line(s, sw, 0, SLIDE_W - sw)
section_heading(s, "/draft <LP> — generates 3 variations (A / B / C)")

screenshot_box(
    s, Inches(3.0), Inches(1.5), Inches(6.5), Inches(5.2),
    "\u2702 SCREENSHOT: draft .md file or REVIEW-PACKET.md\n"
    "Show one complete email: subject, salutation,\n"
    "intro with bridge, bullets, values close, sign-off\n\n"
    "Ideally two variants side by side (A and B)")

# Features — right column
features = [
    "3 bridge angles per LP",
    "200-230 words, QA-checked",
    "Auto language: SK / DE / EN",
    "Override: /draft <LP> en",
    "Fund facts locked",
]
for i, feat in enumerate(features):
    fy = Inches(1.7) + i * Inches(0.8)
    rect(s, Inches(10.0), fy + Inches(0.05), Inches(0.12), Inches(0.12),
         fill=CORAL)
    txt(s, Inches(10.25), fy, Inches(2.5), Inches(0.3),
        feat, sz=12, color=DARK_GRAY)

page_num(s, 9)


# ════════════════════════════════════════════════════════════════════
# SLIDE 10 — Human Review
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)
sw = sidebar(s, "Human\nReview\n& Send")

accent_line(s, sw, 0, SLIDE_W - sw)
section_heading(s, "AI never sends — supervisor reviews, edits, sends")

# Three columns
cols = [
    ("/review-packet", "Compile", "All emails in one\nprintable document"),
    ("Supervisor", "Review & Edit", "Read, edit bridge,\npick best variant"),
    ("Manual Send", "Send", "Deck attached\nMax 5/day, Tue-Thu"),
]

for i, (cmd, title, desc) in enumerate(cols):
    cx = Inches(3.2) + i * Inches(3.3)
    cy = Inches(1.8)

    # Box
    box = rect(s, cx, cy, Inches(2.8), Inches(2.8),
               fill=WHITE, border=LIGHT_GR, bw=Pt(1))
    # Top coral stripe
    rect(s, cx, cy, Inches(2.8), Inches(0.06), fill=CORAL)

    txt(s, cx + Inches(0.2), cy + Inches(0.3), Inches(2.4), Inches(0.3),
        cmd, sz=9, color=MID_GRAY, font=MONO)
    txt(s, cx + Inches(0.2), cy + Inches(0.7), Inches(2.4), Inches(0.4),
        title, sz=18, color=DARK_GRAY, bold=True, font=SERIF)
    txt(s, cx + Inches(0.2), cy + Inches(1.3), Inches(2.4), Inches(1.2),
        desc, sz=12, color=MID_GRAY)

    # Arrow
    if i < 2:
        txt(s, cx + Inches(2.8), cy + Inches(1.2), Inches(0.5),
            Inches(0.4), "\u203A", sz=24, color=CORAL,
            align=PP_ALIGN.CENTER)

screenshot_box(
    s, Inches(3.2), Inches(5.2), Inches(9.3), Inches(1.8),
    "\u2702 SCREENSHOT: REVIEW-PACKET.md — summary table at top, "
    "two emails visible with bridge and word count")

page_num(s, 10)


# ════════════════════════════════════════════════════════════════════
# SLIDE 11 — Log & Learn
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)
sw = sidebar(s, "Log &\nLearn")

accent_line(s, sw, 0, SLIDE_W - sw)

# Two panels side by side
# Left panel: /log-sent
rect(s, Inches(3.0), Inches(1.0), Inches(4.5), Inches(5.5),
     fill=OFF_WHITE, border=LIGHT_GR, bw=Pt(1))
rect(s, Inches(3.0), Inches(1.0), Inches(4.5), Inches(0.06), fill=CORAL)

txt(s, Inches(3.3), Inches(1.3), Inches(4), Inches(0.4),
    "/log-sent <LP>", sz=16, color=CORAL, bold=True, font=MONO)

log_lines = [
    "1.  Paste the email exactly as sent",
    "     (or say \"unchanged\")",
    "",
    "2.  Saved to /sent/ with date",
    "",
    "3.  Marked: edits none / minor / major",
    "",
    "4.  output.csv \u2192 stage = sent",
]
multi(s, Inches(3.3), Inches(2.0), Inches(3.8), Inches(4),
      log_lines, sz=11, color=DARK_GRAY, font=SANS, spacing=1.4)

# Right panel: /calibrate
rect(s, Inches(8.0), Inches(1.0), Inches(4.8), Inches(5.5),
     fill=OFF_WHITE, border=LIGHT_GR, bw=Pt(1))
rect(s, Inches(8.0), Inches(1.0), Inches(4.8), Inches(0.06), fill=CORAL)

txt(s, Inches(8.3), Inches(1.3), Inches(4), Inches(0.4),
    "/calibrate", sz=16, color=CORAL, bold=True, font=MONO)

txt(s, Inches(8.3), Inches(2.0), Inches(4.2), Inches(0.3),
    "DIFFS EVERY SENT VS. DRAFT", sz=10, color=CORAL, bold=True)

# Frequency table
freq = [
    ("Seen 1x", "Hypothesis (watched)"),
    ("Seen 2x", "Confirmed rule in learnings.md"),
    ("Seen 3x", "Proposes change to voice.md"),
]
for i, (trigger, result) in enumerate(freq):
    fy = Inches(2.6) + i * Inches(0.85)
    # Alternating rows
    bg = CORAL if i % 2 == 0 else CORAL_XLT
    fg = WHITE if i % 2 == 0 else DARK_GRAY
    rect(s, Inches(8.3), fy, Inches(4.2), Inches(0.6), fill=bg)
    txt(s, Inches(8.5), fy + Inches(0.12), Inches(1.3), Inches(0.35),
        trigger, sz=12, color=fg, bold=True)
    txt(s, Inches(9.9), fy + Inches(0.12), Inches(2.5), Inches(0.35),
        result, sz=11, color=fg)

txt(s, Inches(8.3), Inches(5.3), Inches(4.2), Inches(0.8),
    "Next /draft applies all learned rules.\n"
    "Run after every 5-10 sends.",
    sz=11, color=MID_GRAY)

# Arrow between panels
txt(s, Inches(7.5), Inches(3.5), Inches(0.5), Inches(0.5),
    "\u203A", sz=28, color=CORAL, align=PP_ALIGN.CENTER)

page_num(s, 11)


# ════════════════════════════════════════════════════════════════════
# SLIDE 12 — The Cycle
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)

accent_line(s, 0, 0, SLIDE_W)

txt(s, Inches(0.8), Inches(0.5), Inches(10), Inches(0.5),
    "THE CYCLE", sz=12, color=CORAL, bold=True)

# Circular layout of 6 steps
cycle = [
    ("Research", "/research"),
    ("Score", "/rescore"),
    ("Draft", "/draft"),
    ("Review & Send", "Supervisor"),
    ("Log", "/log-sent"),
    ("Calibrate", "/calibrate"),
]

cx = Inches(6.666)
cy = Inches(3.8)
radius = Inches(2.3)
item_w = Inches(2.0)
item_h = Inches(0.9)

for i, (label, cmd) in enumerate(cycle):
    angle = -90 + i * 60
    rad = math.radians(angle)
    ix = int(cx + radius * math.cos(rad) - item_w // 2)
    iy = int(cy + radius * math.sin(rad) - item_h // 2)

    bg = CORAL if i % 2 == 0 else CORAL_XLT
    fg = WHITE if i % 2 == 0 else DARK_GRAY

    box = rect(s, ix, iy, item_w, item_h, fill=bg)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(14)
    p.font.color.rgb = fg
    p.font.bold = True
    p.font.name = SANS
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = cmd
    p2.font.size = Pt(9)
    p2.font.color.rgb = fg
    p2.font.name = MONO
    p2.alignment = PP_ALIGN.CENTER

# Center label
txt(s, cx - Inches(1.2), cy - Inches(0.5), Inches(2.4), Inches(1.0),
    "Continuous\nImprovement", sz=18, color=CORAL, bold=True,
    font=SERIF, align=PP_ALIGN.CENTER)

txt(s, Inches(2.5), Inches(6.8), Inches(8), Inches(0.3),
    "Each round, drafts get closer to your voice. "
    "After 5-10 sends, run /calibrate.",
    sz=11, color=MID_GRAY, align=PP_ALIGN.CENTER)

page_num(s, 12)


# ════════════════════════════════════════════════════════════════════
# SLIDE 13 — Quick Reference
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
set_bg(s, WHITE)
sw = sidebar(s, "Quick\nReference")

accent_line(s, sw, 0, SLIDE_W - sw)

# Claude commands — left table
txt(s, Inches(3.0), Inches(0.8), Inches(5), Inches(0.3),
    "CLAUDE COMMANDS", sz=10, color=CORAL, bold=True)

claude_cmds = [
    ("/import-lps", "Create stub files from import"),
    ("/research <LP>", "Full web research + score"),
    ("/rescore <LP>", "Recalculate score"),
    ("/draft <LP>", "3 email variations (A/B/C)"),
    ("/review-packet", "Compile all drafts"),
    ("/log-sent <LP>", "Archive sent version"),
    ("/calibrate", "Learn from edits"),
    ("/weekly-review", "Pipeline summary"),
]

for i, (cmd, desc) in enumerate(claude_cmds):
    ry = Inches(1.2) + i * Inches(0.55)
    bg = OFF_WHITE if i % 2 == 0 else WHITE
    rect(s, Inches(3.0), ry, Inches(5.0), Inches(0.5), fill=bg)
    txt(s, Inches(3.1), ry + Inches(0.1), Inches(2.2), Inches(0.3),
        cmd, sz=10, color=DARK_GRAY, font=MONO)
    txt(s, Inches(5.3), ry + Inches(0.1), Inches(2.5), Inches(0.3),
        desc, sz=10, color=MID_GRAY)

# Terminal commands — right table
txt(s, Inches(8.5), Inches(0.8), Inches(4.5), Inches(0.3),
    "TERMINAL COMMANDS", sz=10, color=CORAL, bold=True)

py_cmds = [
    ("convert.py init", "Blank input.xlsx"),
    ("convert.py import", "xlsx \u2192 csv"),
    ("convert.py export", "csv \u2192 xlsx"),
    ("convert.py sync", "Pull stage/score"),
    ("convert.py verify-export", "Verification checklist"),
    ("convert.py verify-import", "Apply corrections"),
]

for i, (cmd, desc) in enumerate(py_cmds):
    ry = Inches(1.2) + i * Inches(0.55)
    bg = OFF_WHITE if i % 2 == 0 else WHITE
    rect(s, Inches(8.5), ry, Inches(4.3), Inches(0.5), fill=bg)
    txt(s, Inches(8.6), ry + Inches(0.1), Inches(2.5), Inches(0.3),
        cmd, sz=10, color=DARK_GRAY, font=MONO)
    txt(s, Inches(11.2), ry + Inches(0.1), Inches(1.5), Inches(0.3),
        desc, sz=10, color=MID_GRAY)

page_num(s, 13)


# ════════════════════════════════════════════════════════════════════
out = "Valori-fundraising-semi-automatic-pipeline.pptx"
prs.save(out)
print(f"Saved {len(prs.slides)} slides to {out}")

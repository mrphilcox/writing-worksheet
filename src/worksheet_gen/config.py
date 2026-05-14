from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors


"""
Configuration for worksheet-gen.

Design goals:
- All layout is expressed in points (pt) internally.
- All "knobs" that affect layout live here so layout iteration is fast.
- Derived values are computed from base constants so changes remain consistent.

Units:
- 1 inch = 72 points
- mm() and inch() helpers convert to points.
"""

# -----------------------------------------------------------------------------
# Units and conversion helpers
# -----------------------------------------------------------------------------

# Points per inch. This is fixed by the PDF specification.
# Valid range: must be 72.0 for PDF coordinates.
INCH_TO_PT = 72.0

# Points per millimeter.
# Derived from INCH_TO_PT / 25.4, do not change unless you are deliberately
# breaking standard conversions.
MM_TO_PT = INCH_TO_PT / 25.4


def inch(value: float) -> float:
    """
    Convert inches to points.
    Valid range: any float, but typically positive.
    """
    return value * INCH_TO_PT


def mm(value: float) -> float:
    """
    Convert millimeters to points.
    Valid range: any float, but typically positive.
    """
    return value * MM_TO_PT


# -----------------------------------------------------------------------------
# Repo and asset paths
# -----------------------------------------------------------------------------

# Repo root is computed relative to this file: src/worksheet_gen/config.py
# parents[2] assumes the layout:
#   repo_root/
#     src/
#       worksheet_gen/
#         config.py
#
# If you move config.py, you must update this.
REPO_ROOT = Path(__file__).resolve().parents[2]

# Assets directory under the repo root.
ASSETS_DIR = REPO_ROOT / "assets"

# Fonts live in assets/fonts by convention.
FONTS_DIR = ASSETS_DIR / "fonts"

# Andika font files.
# Valid range: must point to existing .ttf files at runtime if you want Andika.
ANDIKA_REGULAR_TTF = FONTS_DIR / "Andika-Regular.ttf"
ANDIKA_BOLD_TTF = FONTS_DIR / "Andika-Bold.ttf"

# ReportLab "internal" font names used after TTFont registration.
# Valid range: any non-empty string. Should match what render.py registers.
FONT_REGULAR_NAME = "Andika"
FONT_BOLD_NAME = "Andika-Bold"

# Fallback fonts if the TTF files cannot be loaded.
# Valid range: must be a font name ReportLab knows (built-ins are safe).
FALLBACK_FONT_REGULAR = "Helvetica"
FALLBACK_FONT_BOLD = "Helvetica-Bold"


# -----------------------------------------------------------------------------
# Page geometry (Letter)
# -----------------------------------------------------------------------------

# PDF page size in points.
# Letter size is 8.5 x 11 inches.
PAGE_WIDTH_PT = inch(8.5)
PAGE_HEIGHT_PT = inch(11.0)

# Page margins (content inset).
# Valid range:
# - Must be >= 0
# - Left + Right < PAGE_WIDTH_PT
# - Top + Bottom < PAGE_HEIGHT_PT
#
# Practical range for worksheets: 10mm to 20mm.
# The renderer clamps margins to MIN_MARGIN_PT as a lower bound.
MIN_MARGIN_MM = 10.0
MIN_MARGIN_PT = mm(MIN_MARGIN_MM)

# Default margins before the minimum-margin clamp is applied. The current left
# and right defaults are intentionally smaller than MIN_MARGIN_PT, so the
# effective rendered margins are 10mm unless these values are raised.
MARGIN_DEFAULT_LEFT_PT = inch(0.25)
MARGIN_DEFAULT_RIGHT_PT = inch(0.25)
MARGIN_DEFAULT_TOP_PT = inch(0.5)
MARGIN_DEFAULT_BOTTOM_PT = inch(0.5)

# Current margin knobs (override to tune, renderer clamps to MIN_MARGIN_PT).
MARGIN_LEFT_PT = MARGIN_DEFAULT_LEFT_PT
MARGIN_RIGHT_PT = MARGIN_DEFAULT_RIGHT_PT
MARGIN_TOP_PT = MARGIN_DEFAULT_TOP_PT
MARGIN_BOTTOM_PT = MARGIN_DEFAULT_BOTTOM_PT

# Derived content area size.
# Do not edit directly. Edit margins or page size instead.
# These are the default content sizes before MIN_MARGIN_PT clamping.
CONTENT_WIDTH_PT = PAGE_WIDTH_PT - MARGIN_LEFT_PT - MARGIN_RIGHT_PT
CONTENT_HEIGHT_PT = PAGE_HEIGHT_PT - MARGIN_TOP_PT - MARGIN_BOTTOM_PT


# -----------------------------------------------------------------------------
# Handwriting guide system (the lined practice rows)
# -----------------------------------------------------------------------------

# Width of the handwriting guides area before clamping to the effective content
# width.
# This can be less than CONTENT_WIDTH_PT to leave space for side blocks or just
# to avoid "edge-to-edge" lines.
#
# Valid range:
# - > 0
# - Typically <= CONTENT_WIDTH_PT (renderer clamps to effective content width)
GUIDE_WIDTH_PT = inch(8.0)

# "Main" height of the guide: baseline -> topline (also sometimes called
# the cap-height zone in handwriting paper).
#
# Valid range:
# - > 0
# - Common handwriting main heights: 12mm to 20mm depending on age.
GUIDE_MAIN_HEIGHT_PT = mm(10.0)

# Ratio that allocates part of the row below the baseline for descenders (g, y, p).
# GUIDE_DESC_HEIGHT_PT = GUIDE_MAIN_HEIGHT_PT * GUIDE_DESC_RATIO
#
# Valid range:
# - 0.0 to 1.0
# Practical range:
# - 0.25 to 0.60
GUIDE_DESC_RATIO = 0.45

# Derived descender height (baseline -> bottom of descender zone).
GUIDE_DESC_HEIGHT_PT = GUIDE_MAIN_HEIGHT_PT * GUIDE_DESC_RATIO

# Extra vertical padding above the topline inside each row.
# This is "air" so tall glyphs or slight overshoot do not look cramped.
#
# Valid range:
# - >= 0
# Practical range:
# - 0mm to 4mm
GUIDE_PAD_TOP_PT = mm(2.0)

# Total row height in points.
# This is the full vertical space consumed per writing row, not counting
# extra gaps between rows.
# Derived, do not edit directly.
GUIDE_ROW_HEIGHT_PT = GUIDE_DESC_HEIGHT_PT + GUIDE_MAIN_HEIGHT_PT + GUIDE_PAD_TOP_PT

# Stroke widths (line thickness) for the guide lines.
# Valid range:
# - > 0
# Practical range for printing:
# - 0.5 to 1.5 pt
GUIDE_BASELINE_STROKE_PT = 1.0
GUIDE_TOPLINE_STROKE_PT = 1.0
GUIDE_MIDLINE_STROKE_PT = 0.8

# Midline dash pattern (on/off lengths) in points.
# Midline is typically dashed to visually distinguish from baseline/topline.
#
# Valid range:
# - > 0 for both values
# Practical range:
# - 2 to 6 pt
GUIDE_MIDLINE_DASH_ON_PT = 3.0
GUIDE_MIDLINE_DASH_OFF_PT = 3.0

# Horizontal inset for the model sentence text inside the guide row.
# This prevents the text from touching the left guide boundary.
#
# Valid range:
# - >= 0
# Practical range:
# - 2 to 10 pt
GUIDE_TEXT_X_OFFSET_PT =2.0

# Whether to draw a topline at all.
# Some worksheets use baseline + midline only.
GUIDE_DRAW_TOPLINE = True

# Where the midline sits between baseline and topline.
# 0.5 means midline is halfway up the main zone.
#
# Valid range:
# - 0.0 to 1.0
# Practical range:
# - 0.45 to 0.60 (handwriting midline often slightly above half)
MIDLINE_RATIO = 0.5


# -----------------------------------------------------------------------------
# Typography sizes (points)
# -----------------------------------------------------------------------------

# Title at the very top.
# Valid range:
# - ~12 to 24 depending on header design
TITLE_SIZE_PT = 16.0

# Default body text (labels and small block text).
# Valid range:
# - ~9 to 13
BODY_SIZE_PT = 11.0

# Sentence "display" size near the top of practice area.
# This is the visible model sentence label line, not the ghost text inside rows.
# Valid range:
# - ~11 to 18
SENTENCE_DISPLAY_SIZE_PT = 14.0

# Model (ghost) text sizing safety factor.
# This is a final multiplier applied to the computed font size used for model text
# inside trace rows. Increasing makes text bigger, decreasing makes it smaller.
#
# Valid range:
# - 0.85 to 1.05 (beyond this you may clip or look too small)
# Practical tuning:
# - 0.96 for "bigger but safe"
# - 0.98 for "tight / near-max"
# - 1.00 for "fill the guides as much as possible"
MODEL_TEXT_SAFETY = 0.96

# Font metrics are typically expressed in "units per em".
# Some ReportLab APIs use a 1000-unit convention; fonttools reads actual unitsPerEm.
# Keep as 1000.0 only if your sizing code uses ReportLab ascent/descent in 1000-em units.
FONT_EM_UNITS = 1000.0

# When cap-height / x-height is not available in OS/2 table, approximate.
# These ratios are applied to a fallback ascent metric (like usWinAscent).
#
# Valid range:
# - 0.0 to 1.0
# Practical range:
# - cap: 0.65 to 0.80
# - x:   0.45 to 0.60
CAP_HEIGHT_FALLBACK_RATIO = 0.72
X_HEIGHT_FALLBACK_RATIO = 0.52


# -----------------------------------------------------------------------------
# Header layout spacing (points)
# -----------------------------------------------------------------------------

# Vertical gaps controlling header block layout.
# Valid range: >= 0
HEADER_TITLE_GAP_PT = 10.0      # Space under the title line
HEADER_LINE_GAP_PT = 10.0       # Space between "Name" and "Date" lines
HEADER_BLOCK_GAP_PT = 15.0      # Space after header before next block


# -----------------------------------------------------------------------------
# Emotion prompt layout (points)
# -----------------------------------------------------------------------------

# Gap after emotion prompt block.
# Valid range: >= 0
EMOTION_PROMPT_GAP_PT = 12.0

# Circle checkbox geometry.
# Radius controls size of the circle.
# Valid range:
# - > 0
# Practical range:
# - 4 to 8 pt
EMOTION_CIRCLE_RADIUS_PT = 6.0

# Slight vertical tweak for the circle center relative to text baseline.
# Valid range:
# - can be negative or positive
# Practical range:
# - -2 to +6
EMOTION_CIRCLE_CENTER_OFFSET_PT = 3.0

# Spacing between the circle and the label text.
# Valid range: >= 0
EMOTION_LABEL_GAP_PT = 6.0

# Spacing between choices (Happy / Okay / Hard).
# Valid range: >= 0
EMOTION_CHOICE_GAP_PT = 12.0

# Stroke width for circle outlines.
# Valid range: > 0
EMOTION_CIRCLE_STROKE_PT = 1.0

# Derived diameter for convenience.
EMOTION_CIRCLE_DIAMETER_PT = EMOTION_CIRCLE_RADIUS_PT * 2.0


# -----------------------------------------------------------------------------
# Reminder box layout (points)
# -----------------------------------------------------------------------------

# Padding inside the reminder box.
# Valid range: >= 0
REMINDER_BOX_PADDING_PT = 6.0

# Gaps within reminder box.
# Valid range: >= 0
REMINDER_TITLE_GAP_PT = 4.0
REMINDER_LINE_GAP_PT = 3.0

# Border stroke width.
# Valid range: > 0
REMINDER_BORDER_STROKE_PT = 1.0


# -----------------------------------------------------------------------------
# Section / sentence spacing (points)
# -----------------------------------------------------------------------------

# Gap between "Sentence:" label and the sentence display line.
# Valid range: >= 0
SENTENCE_LABEL_GAP_PT = 4.0

# Gap between a section title and its first row.
# Valid range: >= 0
SECTION_TITLE_GAP_PT = 15.0


# -----------------------------------------------------------------------------
# Practice row spacing (points)
# -----------------------------------------------------------------------------

# Vertical gap between trace rows.
# Valid range: >= 0
TRACE_ROW_GAP_PT = 10.0

# Gap between the trace section and the write section.
# Valid range: >= 0
TRACE_TO_WRITE_GAP_PT = 8.0

# Vertical gaps between write rows.
# You may want slightly different spacing depending on whether the row includes
# a midline (midline rows can look "busier").
#
# Valid range: >= 0
WRITE_ROW_GAP_MIDLINE_PT = 10.0
WRITE_ROW_GAP_NO_MIDLINE_PT = 18.0

# Gap between major sections (if multiple sections exist).
# Valid range: >= 0
SECTION_GAP_PT = 10.0


# -----------------------------------------------------------------------------
# Trace model text wrapping
# -----------------------------------------------------------------------------

# Enable render-time wrapping for trace section model text. The wrapping helper
# is always available for tests and callers, but the renderer only consumes it
# when this flag is true.
TRACE_WRAP_ENABLED = False

# Maximum number of guide rows a wrapped trace sentence can occupy.
# Valid range: >= 1
# Practical range: 1 to 3
TRACE_WRAP_MAX_LINES = 2

# Width tolerance to account for floating-point rounding in text metrics.
# Valid range: >= 0
# Practical range: 0.0 to 1.0 pt
TRACE_WRAP_EPSILON_PT = 0.5

# Allow breaking long single words that exceed the guide width.
TRACE_WRAP_HARD_BREAK_LONG_WORDS = True

# Minimum word length to allow hard-break splitting.
# Valid range: >= 1
# Practical range: 8 to 20 characters
TRACE_WRAP_MIN_CHARS_FOR_HARD_BREAK = 10


# -----------------------------------------------------------------------------
# Cartoon placement (header) and placeholder
# -----------------------------------------------------------------------------

# Maximum cartoon size in inches (as author-friendly knobs).
# Valid range: > 0
CARTOON_MAX_W_IN = 1.5
CARTOON_MAX_H_IN = 1.5

# Converted maximum cartoon size in points (used by renderer).
CARTOON_MAX_W_PT = inch(CARTOON_MAX_W_IN)
CARTOON_MAX_H_PT = inch(CARTOON_MAX_H_IN)

# Padding around the cartoon within the header area.
# Valid range: >= 0
CARTOON_PAD_PT = mm(6.0)

# Stroke for the placeholder rectangle if a cartoon is enabled but the PNG image
# is missing, omitted, or unsupported.
# Valid range: > 0
CARTOON_PLACEHOLDER_STROKE_PT = 1.0


# -----------------------------------------------------------------------------
# Colors
# -----------------------------------------------------------------------------

# Ghost model text color (light gray).
# colors.Color(r,g,b) takes 0.0 to 1.0 float values.
MODEL_TEXT_COLOR = colors.Color(0.85, 0.85, 0.85)

# Midline color (dashed).
MIDLINE_COLOR = colors.grey

# Main guide line color (baseline/topline).
PRIMARY_LINE_COLOR = colors.black

# General text color.
TEXT_COLOR = colors.black


# -----------------------------------------------------------------------------
# PDF metadata (keep deterministic)
# -----------------------------------------------------------------------------

# PDF author metadata string.
# Valid range: any string. Keep stable for deterministic output.
PDF_AUTHOR = "worksheet-gen"

# PDF subject metadata string.
# Valid range: any string. Keep stable for deterministic output.
PDF_SUBJECT = "handwriting practice"


# -----------------------------------------------------------------------------
# Default content strings (used only if YAML omits fields)
# -----------------------------------------------------------------------------

DEFAULT_TITLE_EN = "Abby’s Handwriting Practice – English"
DEFAULT_TITLE_FR = "Pratique d’écriture – Français"
DEFAULT_DATE_EN = "Date: ____________________"
DEFAULT_DATE_FR = "Date : ____________________"

DEFAULT_EMOTION_TEXT_EN = "How does this feel today?"
DEFAULT_EMOTION_CHOICES_EN = ["Easy", "Okay", "Hard"]

DEFAULT_REMINDER_TITLE_EN = "Remember:"
DEFAULT_REMINDER_B_LINE_EN = "b = stick first, then circle (ball)"
DEFAULT_REMINDER_D_LINE_EN = "d = circle first, then stick (dog)"

DEFAULT_SENTENCE_DISPLAY_EN = "Abby bakes bread."
DEFAULT_SENTENCE_MODEL_EN = "Abby bakes bread."

# Used if child_name is absent.
DEFAULT_CHILD_NAME_PLACEHOLDER = "____________________"

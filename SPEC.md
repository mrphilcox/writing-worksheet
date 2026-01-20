# SPEC.md

## Overview

This spec defines the **v2 handwriting worksheet layout** as iterated in this thread. The generator MUST produce deterministic, print-stable PDFs via ReportLab.

The v2 worksheet is **one page** and contains, in order:

1. Title
2. Date line
3. Emotions check-in (3 choices)
4. b/d reminder with “ball” and “dog”
5. Sentence (display)
6. Trace section: 2 guide rows (row 1 with midline, row 2 without)
7. Write section: 5 guide rows (first 3 with midline, last 2 without)

No additional sections or layout changes are permitted unless explicitly configured and accepted later.

---

## Page

- **Paper**: US Letter (8.5 × 11 in)
- **Orientation**: Portrait
- **Units**: all geometry is defined in points (pt) and/or millimeters (mm). Rendering MUST convert consistently.

### Margins (content frame)
- Left margin: **0.6 in** (preferred)
- Right margin: **0.6 in** (preferred)
- Top margin: **0.5 in** (preferred)
- Bottom margin: **0.5 in** (preferred)
- Minimum margin: **10 mm** (reserved border; effective margins clamp to this)

All layout coordinates are relative to this content frame.

---

## Typography

### Fonts

#### Primary font for handwriting content
- **Family name**: Andika (Regular)
- **Font file**: `Andika-Regular.ttf` (or equivalent regular upright face)
- **Used for**:
  - the sentence display line (read-only)
  - the model/tracing text inside guide rows

#### UI / headings font
- **Family**: Helvetica
- **Used for**:
  - Title (header)
  - Body labels/headings (“Sentence:”, “Trace…”, “Write…”)
  - Emotions line and reminder block

### Font sizes

- Title: **16 pt** (Helvetica)
- Date line: **11 pt** (Helvetica)
- Body text: **11 pt** (Helvetica)
- Sentence display line: **14 pt** (Andika Regular)
- Model/tracing text inside guide rows: **computed dynamically** (Andika Regular), calibrated so that the glyph height of `max('A','b')` touches the topline.

#### Model/tracing text size calibration rule (critical)

The model text MUST be sized so that:
- The **baseline** aligns exactly to the worksheet **baseline**.
- The **reference glyph** top reaches the worksheet **topline**.

Reference glyph choice:
- Compute `yMax` for glyphs “A” and “b” from the TrueType font (fontTools).
- Let `yMax_ref = max(yMax('A'), yMax('b'))`.
- Let `units_per_em` come from the font `head.unitsPerEm`.
- Let `ratio = yMax_ref / units_per_em`.

Then for a given guide main height (baseline → topline):
- `font_size_pt = main_height_pt / ratio`

This ensures:
- “A” and “b” extend from baseline to topline as expected.
- Descenders (e.g., “y”) naturally fall below baseline into the descender area.

### Color / grayscale

All colors are grayscale for print stability.

- Primary lines (baseline + topline): **black** (RGB 0,0,0)
- Midline: **gray** (ReportLab `grey`, nominal RGB ~0.5,0.5,0.5)
- Model/tracing text: **light gray** (RGB **0.75, 0.75, 0.75**)
- Other UI text: **black**

No transparency is required; use solid RGB values (print-stable across viewers/printers).

---

## Handwriting guide system (precise)

Each “guide row” is a handwriting practice band with **two solid lines** and an optional dashed midline.

### Lines per row

- **Topline**: solid line
- **Baseline**: solid line
- **Midline (optional)**: dashed line halfway between baseline and topline
- **No extra bottom line**: there is additional blank descender space below the baseline but no additional line.

### Vertical geometry per row

Define:

- `main_height` = distance from **baseline** to **topline**
- `descender_height` = extra blank space **below baseline**

In v2:
- `main_height = 15 mm` (baseline → topline)
- `descender_height = 0.45 * main_height` (below baseline)
- `row_internal_pad_top = 2 mm` (blank space above topline inside the row box)

So row height is:
- `row_height = descender_height + main_height + row_internal_pad_top`

Midline position:
- `midline_y = baseline_y + main_height / 2`

### Stroke weights and dash patterns

- Baseline:
  - stroke width: **1.0 pt**
  - solid
- Topline:
  - stroke width: **1.0 pt**
  - solid
- Midline (when enabled):
  - stroke width: **0.8 pt**
  - dash pattern: **3 pt on, 3 pt off**

### Model/tracing text placement

- Text is drawn with `drawString()`.
- X offset from guide left edge: **4 pt**
- Y position: exactly at **baseline_y**
- Fill color: light gray (RGB 0.75)

---

## Worksheet sections (order, headings, allocation)

### 1) Title
- Text: `Abby’s Handwriting Practice – English`
- Font: Helvetica 16 pt
- Positioned at top of content frame.

### 2) Date line
- Text: `Date: ____________________`
- Font: Helvetica 11 pt
- Immediately below title.

### 3) Emotions line
- Text: `How does this feel today?  ◯ Happy   ◯ Okay   ◯ Hard`
- Font: Helvetica 11 pt

### 4) b/d reminder block
Rendered as a short 2-line reminder. Exact v2 wording:

- Heading: `Remember:`
- Lines:
  - `b = stick first, then circle (ball)`
  - `d = circle first, then stick (dog)`

Font: Helvetica 11 pt. The “Remember:” label is bold.

### 5) Sentence display
- Heading: `Sentence:`
- Sentence text (v2 micro-sentence):
  - `Abby bakes bread.`
- Heading uses Helvetica 11 pt.
- Sentence uses Andika 14 pt.

### 6) Trace section
- Heading: `Trace (2 times):` (Helvetica 11 pt, bold label)
- 2 guide rows:
  1. With midline + model text (light gray)
  2. Without midline + model text (light gray)
- Trace model sentences may wrap to a second guide row when they exceed the guide width; more than two lines is an error.

### 7) Write section
- Heading: `Write (5 times):` (Helvetica 11 pt, bold label)
- 5 guide rows:
  - Rows 1–3: with midline (no model text)
  - Rows 4–5: without midline (no model text)

### Footer / header extras
- None in v2 beyond the title/date/emotions/reminder/sentence.

---

## Spacing rules (exact, v2)

Spacing uses fixed point values between blocks:

- After “Trace row 1” and “Trace row 2”: **6 pt**
- After “Trace section” before “Write section”: **8 pt**
- Between write rows 1–3: **6 pt**
- Between write rows 4–5: **8 pt**
- A small spacer is used between major blocks (title/date/emotions/reminder/sentence/trace/write) consistent with the current generator.

---

## Cartoon line art feature (defined but OFF by default)

Status in v2:
- Not required to render (default: none), but schema supports it.

If provided, the renderer MUST:
- Place a single line-art image in the **top-right area of the header block** (inside the content frame).
- It must not overlap the title/date/emotions/reminder/sentence.

Constraints:
- Maximum bounding box: **1.5 in × 1.5 in**
- Padding from top/right edges of content frame: **6 mm**
- Style: line art intended to be colorable
- Opacity: solid grayscale line art (no transparency requirement); recommended stroke gray ~0.6 if needed
- Format: SVG preferred; renderer may rasterize deterministically to a fixed DPI if necessary.

---

## Determinism requirements

- No randomness.
- All coordinates derived from constants + content.
- Font metrics read from the specified font file.
- Output must be stable across runs given identical inputs.


# SPEC.md

## Overview

This document describes the current v2 handwriting worksheet layout implemented
by `worksheet_gen.render`.

The generator produces deterministic, print-stable PDFs via ReportLab. A
worksheet is one US Letter portrait page containing:

1. Title
2. Name line
3. Date line
4. Emotions check-in
5. b/d reminder box
6. Sentence display
7. Trace section
8. Write section

Optional cartoon art may be placed in the top-right header area.

## Page

- Paper: US Letter, 8.5 x 11 in
- Orientation: portrait
- Internal units: points
- PDF size: 612 x 792 pt
- Deterministic output: ReportLab canvas uses `invariant=1`

### Margins

Configured defaults:

- Left: 0.25 in
- Right: 0.25 in
- Top: 0.5 in
- Bottom: 0.5 in

The renderer clamps each margin to `MIN_MARGIN_MM`, currently 10 mm. Effective
left/right margins are therefore 10 mm unless the configured values are raised.

## Typography

### Fonts

- Andika Regular: sentence display and trace model text.
- Andika Bold: headings when available.
- Helvetica / Helvetica-Bold: fallback fonts when bundled TTF files are missing.

### Font sizes

- Title: 16 pt
- Body text and labels: 11 pt
- Sentence display: 14 pt
- Trace model text: computed from font metrics and guide geometry

Trace model text is sized from the available cap-height area and descender
space, then multiplied by `MODEL_TEXT_SAFETY` (`0.96`). If TrueType metrics are
unavailable, the renderer falls back to ReportLab ascent/descent metrics.

## Colors

All rendered PDF colors are grayscale or black:

- Primary guide lines: black
- Midline: ReportLab `grey`
- Trace model text: RGB `0.85, 0.85, 0.85`
- General text and reminder border: black

## Handwriting Guide Rows

Each guide row contains:

- Baseline: solid black line, 1.0 pt
- Topline: solid black line, 1.0 pt, controlled by `GUIDE_DRAW_TOPLINE`
- Optional midline: dashed grey line, 0.8 pt, dash pattern 3 pt on / 3 pt off
- Descender space below the baseline with no extra bottom line

Geometry:

- Main height, baseline to topline: 10 mm
- Descender height: `0.45 * main height`
- Internal padding above topline: 2 mm
- Total row height: 16.5 mm
- Midline position: halfway between baseline and topline (`MIDLINE_RATIO = 0.5`)
- Model text left inset: 2 pt

Guide width is configured as 8.0 in and clamped to the effective content width.

## Worksheet Sections

### Title

Rendered at the top-left of the content frame using the configured title.
Default English title:

`Abby’s Handwriting Practice – English`

### Name Line

Rendered below the title:

`Name: ____________________`

If `child_name` is provided, it replaces the underline placeholder.

### Date Line

Rendered below the name line. Default English text:

`Date: ____________________`

### Emotions Check-in

Default English prompt and choices:

`How does this feel today?` with `Easy`, `Okay`, `Hard`

Choices are drawn as circle controls followed by labels.

### b/d Reminder

Rendered in a bordered box. Default English copy:

- `Remember:`
- `b = stick first, then circle (ball)`
- `d = circle first, then stick (dog)`

### Sentence Display

The label `Sentence:` is rendered in bold, followed by `sentence.display` in the
regular handwriting font at 14 pt.

### Trace Section

Default heading:

`Trace (2 times):`

Default rows:

- Row 1: midline enabled, model text enabled
- Row 2: midline disabled, model text enabled

Trace wrapping helpers exist in `render.py`. Rendering only applies wrapped
trace rows when `TRACE_WRAP_ENABLED` is set to true in `config.py`.

### Write Section

Default heading:

`Write (5 times):`

Default rows:

- Rows 1-3: midline enabled, no model text
- Rows 4-5: midline disabled, no model text

Write rows with `model_text: true` are rejected by schema validation.

## Spacing

Current spacing constants:

- Title to name line: 10 pt
- Name to date line: 10 pt
- Date/emotion/reminder block gaps: 15 pt major header gap
- Reminder title gap: 4 pt
- Reminder line gap: 3 pt
- Sentence label to sentence text: 4 pt
- Section title to first row: 15 pt
- Trace row gap: 10 pt
- Trace-to-write gap: 8 pt
- Write row gap when adjacent rows both have midlines: 10 pt
- Write row gap otherwise: 18 pt

## Cartoon Art

Cartoon art is optional and disabled by default. When enabled:

- Placement: top-right header area
- Supported rendered image format: PNG
- Default max size: 1.5 x 1.5 in
- Padding from content top/right: 6 mm

If the configured asset is missing, omitted, or not a PNG, the renderer emits a
warning and draws a placeholder rectangle.

## Determinism Requirements

- No randomness.
- All coordinates derive from configuration constants and worksheet content.
- Font metrics are read from the configured TTF when available.
- PDF canvas uses invariant mode.
- Given identical inputs, config, fonts, and assets, output should be stable
  across runs.

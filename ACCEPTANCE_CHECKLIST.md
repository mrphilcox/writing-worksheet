# ACCEPTANCE_CHECKLIST.md

## PDF and print stability
- [ ] PDF renders identically across runs given the same YAML input.
- [ ] PDF is US Letter (8.5×11 in), portrait.
- [ ] Printing at 100% scale (no “fit to page”) produces the expected physical sizes.

## Margins and content frame
- [ ] Left/right margins are 0.6 in; top/bottom margins are 0.5 in.
- [ ] No content crosses the margins.

## Typography
- [ ] Title is Helvetica 16 pt: “Abby’s Handwriting Practice – English”.
- [ ] Date line is Helvetica 11 pt: “Date: ____________________”.
- [ ] Sentence display uses Andika Regular 14 pt.
- [ ] Model/tracing text uses Andika Regular and is light gray (RGB 0.75).

## Handwriting guides (geometry)
- [ ] Each guide row has exactly:
  - [ ] one solid baseline
  - [ ] one solid topline
  - [ ] optional dashed midline (only when enabled)
- [ ] Baseline→topline distance is 15 mm.
- [ ] Midline (when present) is exactly halfway between baseline and topline.
- [ ] There is blank descender space below baseline (0.45× main height) and no extra line.
- [ ] Baseline/topline stroke is 1.0 pt black.
- [ ] Midline stroke is 0.8 pt grey with dash pattern 3pt on / 3pt off.

## Model text alignment
- [ ] In the traced lines, “Abby” shows:
  - [ ] Capital “A” touches topline and sits on baseline.
  - [ ] Lowercase “b” touches topline and sits on baseline.
  - [ ] Descenders (e.g., “y”) extend below baseline into the descender space.
- [ ] Model text starts 4 pt from the left edge of the guide row.

## Section content and row counts
- [ ] Emotions line appears: “How does this feel today?  ◯ Happy   ◯ Okay   ◯ Hard”.
- [ ] Reminder block appears with exact text:
  - [ ] “Remember:”
  - [ ] “b = stick first, then circle (ball)”
  - [ ] “d = circle first, then stick (dog)”
- [ ] Sentence is terminated with a period: “Abby bakes bread.”
- [ ] Trace section:
  - [ ] heading “Trace (2 times):”
  - [ ] 2 rows total
  - [ ] row 1 has midline + model text
  - [ ] row 2 has no midline + model text
- [ ] Write section:
  - [ ] heading “Write (5 times):”
  - [ ] 5 rows total
  - [ ] first 3 rows with midline (no model text)
  - [ ] last 2 rows without midline (no model text)

## Spacing
- [ ] Gap between trace rows is 6 pt.
- [ ] Gap before write section is 8 pt.
- [ ] Gaps between write rows 1–3 are 6 pt.
- [ ] Gaps between write rows 4–5 are 8 pt.

## Cartoon line art (optional)
- [ ] When disabled, no cartoon appears.
- [ ] When enabled, cartoon is placed top-right in header area within:
  - [ ] max 1.5 in × 1.5 in
  - [ ] 6 mm padding from top/right of content frame
  - [ ] does not overlap any text blocks.


# ACCEPTANCE_CHECKLIST.md

Use this checklist when manually reviewing a generated worksheet PDF.

## PDF and print stability

- [ ] PDF renders identically across runs given the same YAML input, config,
      fonts, and assets.
- [ ] PDF is US Letter, 8.5 x 11 in, portrait.
- [ ] Printing at 100% scale produces expected physical sizes.

## Margins and content frame

- [ ] Effective left/right margins are at least 10 mm.
- [ ] Effective top/bottom margins are at least 10 mm.
- [ ] No content crosses the effective margins.
- [ ] Guide rows fit within the effective content width.

## Header content

- [ ] Title is rendered at the top-left.
- [ ] Name line appears below the title.
- [ ] Date line appears below the name line.
- [ ] Optional `child_name` replaces the name underline placeholder.

## Typography

- [ ] Title is 16 pt.
- [ ] Body labels and text are 11 pt.
- [ ] Sentence display uses the regular handwriting font at 14 pt.
- [ ] Model/tracing text uses the regular handwriting font and light gray fill.
- [ ] Helvetica fallbacks are acceptable only when Andika font files are missing.

## Handwriting guides

- [ ] Each guide row has one solid baseline.
- [ ] Each guide row has one solid topline when `GUIDE_DRAW_TOPLINE` is true.
- [ ] Rows with `midline: true` have one dashed midline.
- [ ] Rows with `midline: false` have no midline.
- [ ] Baseline-to-topline distance is 10 mm.
- [ ] Midline is halfway between baseline and topline.
- [ ] Descender space appears below baseline with no extra bottom line.
- [ ] Baseline/topline stroke is 1.0 pt black.
- [ ] Midline stroke is 0.8 pt grey with dash pattern 3 pt on / 3 pt off.

## Model text alignment

- [ ] Trace model text sits on the guide baseline.
- [ ] Tall letters fit within the guide area without clipping.
- [ ] Descenders extend into the descender space.
- [ ] Model text starts 2 pt from the left edge of the guide row.

## Section content and row counts

- [ ] Emotions prompt appears with exactly three choices.
- [ ] Reminder block appears with title, b-line, and d-line.
- [ ] Sentence display appears below the `Sentence:` label.
- [ ] Default trace section has 2 rows.
- [ ] Trace row 1 has midline and model text.
- [ ] Trace row 2 has no midline and has model text.
- [ ] Default write section has 5 rows.
- [ ] Write rows 1-3 have midlines and no model text.
- [ ] Write rows 4-5 have no midlines and no model text.

## Spacing

- [ ] Header blocks have enough vertical space to avoid overlap.
- [ ] Gap between trace rows is 10 pt.
- [ ] Gap before write section is 8 pt.
- [ ] Gaps between adjacent midline write rows are 10 pt.
- [ ] Gaps before no-midline write rows are 18 pt.

## Cartoon art

- [ ] When disabled, no cartoon appears.
- [ ] When enabled with a valid PNG, the image appears in the top-right header
      area.
- [ ] Cartoon respects max 1.5 in x 1.5 in by default.
- [ ] Cartoon has 6 mm top/right padding from the content frame.
- [ ] Cartoon or placeholder does not overlap text blocks.
- [ ] Missing, omitted, or non-PNG cartoon assets produce a placeholder and
      warning rather than a crash.

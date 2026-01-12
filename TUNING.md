# TUNING.md
Layout and Visual Tuning Guide

This document explains how to adjust the appearance of the worksheet PDFs by
editing values in `src/worksheet_gen/config.py`.

The guiding rule is simple:

> If you want the worksheet to *look* different, you should only need to edit
> config.py.

No changes to rendering code should be required for normal layout iteration.

---

## Mental model

Each handwriting row is built from three vertical zones:

1. **Main zone**  
   Baseline → Topline  
   Used for capitals and tall lowercase letters (b, d, h, k).

2. **Descender zone**  
   Baseline → Bottom of row  
   Used for g, y, p, j.

3. **Pad-top zone**  
   Extra air above the topline  
   Prevents tall letters from feeling cramped.

If something looks off, ask yourself:
- Is it too tall or too short?
- Is it cramped vertically or too airy?
- Is spacing between elements too dense?

Then adjust the matching knob below.

---

## Most commonly adjusted knobs

### “The letters are too small / too big”
**Primary knob:**
```python
MODEL_TEXT_SAFETY
```

- Increases or decreases ghost (model) text uniformly.
- Safe tuning range: `0.95` to `1.02`
- Typical values:
  - 0.96 – conservative, lots of white space
  - 0.98 – tight but safe
  - 1.00 – fills the guides confidently

Change this first before touching guide geometry.

---

### “The rows feel too short / too tall”
**Primary knob:**
```python
GUIDE_MAIN_HEIGHT_PT
```

- Controls the baseline → topline distance.
- Larger value = taller writing rows.
- Typical handwriting ranges:
  - Younger kids: 16–20 mm
  - Older kids: 12–15 mm

Example:
```python
GUIDE_MAIN_HEIGHT_PT = mm(17.0)
```

---

### “Descenders are cramped or too deep”
**Primary knob:**
```python
GUIDE_DESC_RATIO
```

- Fraction of main height allocated below the baseline.
- Typical range: `0.30` to `0.55`

Examples:
- Fewer descenders (cleaner look): `0.35`
- Generous descenders: `0.50`

---

### “Letters feel cramped near the topline”
**Primary knob:**
```python
GUIDE_PAD_TOP_PT
```

- Adds breathing room above the topline.
- Does not move any guide lines.
- Typical range: `0mm` to `4mm`

This is a good knob when things are *almost* right.

---

### “Midline feels too high or too low”
**Primary knob:**
```python
MIDLINE_RATIO
```

- Fraction of main height where the midline is drawn.
- `0.5` = centered
- Typical handwriting values: `0.45`–`0.60`

Lower values give more space above the midline.

---

## Spacing and density

### “Rows are too close together”
**Knobs:**
```python
TRACE_ROW_GAP_PT
WRITE_ROW_GAP_MIDLINE_PT
WRITE_ROW_GAP_NO_MIDLINE_PT
```

- Increase these for a lighter, less dense page.
- Decrease for more rows per page.

---

### “Sections feel cramped”
**Knobs:**
```python
SECTION_TITLE_GAP_PT
SECTION_GAP_PT
TRACE_TO_WRITE_GAP_PT
```

These control breathing room between logical blocks.

---

## Header and top-of-page tuning

### “Header feels crowded”
**Knobs:**
```python
HEADER_TITLE_GAP_PT
HEADER_LINE_GAP_PT
HEADER_BLOCK_GAP_PT
```

- Increase to make the page feel calmer.
- Decrease to fit more content on one page.

---

## Emotion prompt tuning

### “Circles look too big / too small”
**Knob:**
```python
EMOTION_CIRCLE_RADIUS_PT
```

Typical range: `4` to `8`.

---

### “Circle alignment feels off relative to text”
**Knob:**
```python
EMOTION_CIRCLE_CENTER_OFFSET_PT
```

Positive moves the circle up, negative moves it down.

---

## Reminder box tuning

### “Reminder box feels tight”
**Knob:**
```python
REMINDER_BOX_PADDING_PT
```

Increase for a softer, friendlier look.

---

### “Lines in reminder box are too close”
**Knob:**
```python
REMINDER_LINE_GAP_PT
```

---

## Cartoon placement

### “Cartoon is too dominant”
**Knobs:**
```python
CARTOON_MAX_W_IN
CARTOON_MAX_H_IN
```

Lower these to keep the worksheet focused on writing.

---

## What NOT to tune casually

Avoid changing these unless you know why:

- `FONT_EM_UNITS`
- `CAP_HEIGHT_FALLBACK_RATIO`
- `X_HEIGHT_FALLBACK_RATIO`
- Any font metric logic in `render.py`

These exist to make typography math stable across fonts.

---

## Recommended tuning workflow

1. Render `out/test.pdf`
2. Identify *one* visual problem
3. Change *one* knob in `config.py`
4. Re-render
5. Repeat

If you find yourself changing more than 2–3 knobs at once, step back and reassess.

---

## When to change code instead of config

You probably need code changes if:
- A new block or section type is required
- Layout logic is fundamentally wrong (overlap, clipping)
- You want different behavior per section type, not global tuning

For everything else, config.py is the right place.

---

## Philosophy

This project intentionally trades pixel perfection for:
- fast iteration
- clarity
- maintainability

If a worksheet looks “90% right” and is easy to tune, that is success.

# TUNING.md

Layout and visual tuning is centralized in `src/worksheet_gen/config.py`.

The guiding rule:

> If the worksheet should look different, first try changing `config.py`.

Rendering code should only change when the layout model itself needs new
behavior.

## Workflow

1. Render a baseline PDF into `out/`.
2. Identify one visual issue.
3. Change one config knob.
4. Re-render and compare at 100% zoom or on paper.
5. Repeat.

Changing several knobs at once makes it harder to understand which adjustment
helped.

## Page and margins

`MARGIN_LEFT_PT`, `MARGIN_RIGHT_PT`, `MARGIN_TOP_PT`, and `MARGIN_BOTTOM_PT`
control the configured content inset. The renderer clamps each side to
`MIN_MARGIN_PT`, currently 10 mm, so setting a smaller margin will not reduce
the effective margin unless the clamp is also changed.

`GUIDE_WIDTH_PT` controls the requested guide width. The renderer clamps it to
the effective content width.

## Handwriting row model

Each row is built from three vertical zones:

- Main zone: baseline to topline, used by capitals and tall lowercase letters.
- Descender zone: baseline downward, used by letters like `g`, `y`, `p`, and
  `j`.
- Top padding: extra air above the topline.

### Letters are too small or too big

Primary knob:

```python
MODEL_TEXT_SAFETY
```

This multiplier is applied after model text size is computed from font metrics.
The current value is `0.96`.

Practical range: `0.95` to `1.02`.

### Rows are too short or too tall

Primary knob:

```python
GUIDE_MAIN_HEIGHT_PT
```

This controls baseline-to-topline distance. The current value is 10 mm.

Typical handwriting range: 10-20 mm.

### Descenders are cramped or too deep

Primary knob:

```python
GUIDE_DESC_RATIO
```

The current value is `0.45`, meaning descender space is 45% of the main guide
height.

Practical range: `0.30` to `0.60`.

### Letters feel cramped near the topline

Primary knob:

```python
GUIDE_PAD_TOP_PT
```

This adds air above the topline without moving the baseline-to-topline distance.
The current value is 2 mm.

Practical range: 0-4 mm.

### Midline feels too high or too low

Primary knob:

```python
MIDLINE_RATIO
```

`0.5` places the midline halfway between baseline and topline. Values below
`0.5` move it toward the baseline; values above `0.5` move it toward the
topline.

## Spacing and density

### Rows are too close together

Knobs:

```python
TRACE_ROW_GAP_PT
WRITE_ROW_GAP_MIDLINE_PT
WRITE_ROW_GAP_NO_MIDLINE_PT
```

The current defaults are 10 pt, 10 pt, and 18 pt.

### Sections feel cramped

Knobs:

```python
SECTION_TITLE_GAP_PT
SECTION_GAP_PT
TRACE_TO_WRITE_GAP_PT
```

These control breathing room around section headings and between section groups.

### Header feels crowded

Knobs:

```python
HEADER_TITLE_GAP_PT
HEADER_LINE_GAP_PT
HEADER_BLOCK_GAP_PT
```

The current header includes title, name, date, emotions prompt, reminder box,
and sentence display.

## Emotion prompt

Circle size:

```python
EMOTION_CIRCLE_RADIUS_PT
```

Circle alignment:

```python
EMOTION_CIRCLE_CENTER_OFFSET_PT
```

Choice spacing:

```python
EMOTION_PROMPT_GAP_PT
EMOTION_LABEL_GAP_PT
EMOTION_CHOICE_GAP_PT
```

## Reminder box

Padding:

```python
REMINDER_BOX_PADDING_PT
```

Internal line spacing:

```python
REMINDER_TITLE_GAP_PT
REMINDER_LINE_GAP_PT
```

## Cartoon placement

Maximum size:

```python
CARTOON_MAX_W_IN
CARTOON_MAX_H_IN
```

Padding from the content top/right:

```python
CARTOON_PAD_PT
```

The current renderer draws PNG assets. Missing or unsupported assets produce a
placeholder rectangle.

## Trace wrapping

Trace wrapping helpers exist in `render.py`, but render-time wrapping is gated
by:

```python
TRACE_WRAP_ENABLED
```

When enabled, wrapping uses:

```python
TRACE_WRAP_MAX_LINES
TRACE_WRAP_EPSILON_PT
TRACE_WRAP_HARD_BREAK_LONG_WORDS
TRACE_WRAP_MIN_CHARS_FOR_HARD_BREAK
```

Keep `TRACE_WRAP_MAX_LINES` low enough that the worksheet still fits on one
page.

## Knobs to change cautiously

Avoid changing these unless you are intentionally changing font metric behavior:

- `FONT_EM_UNITS`
- `CAP_HEIGHT_FALLBACK_RATIO`
- `X_HEIGHT_FALLBACK_RATIO`
- font metric logic in `render.py`

## When to change code instead of config

Code changes are appropriate when:

- A new block or section type is required.
- Layout behavior needs to vary per section or per row beyond existing schema
  fields.
- Content overlaps or clips despite reasonable config values.
- A new asset format needs renderer support.

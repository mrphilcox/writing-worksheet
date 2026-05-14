# RENDERING_PARAMS.md

The renderer stores its layout knobs in `src/worksheet_gen/config.py`. Values
below reflect the current implementation.

| Name | Unit | Value | Description |
|---|---:|---:|---|
| `PAGE_WIDTH_IN` | in | 8.5 | US Letter width |
| `PAGE_HEIGHT_IN` | in | 11.0 | US Letter height |
| `PAGE_WIDTH_PT` | pt | 612.0 | 8.5 x 72 |
| `PAGE_HEIGHT_PT` | pt | 792.0 | 11 x 72 |
| `MARGIN_DEFAULT_LEFT_PT` | pt | 18.0 | Configured left margin before clamp |
| `MARGIN_DEFAULT_RIGHT_PT` | pt | 18.0 | Configured right margin before clamp |
| `MARGIN_DEFAULT_TOP_PT` | pt | 36.0 | Configured top margin before clamp |
| `MARGIN_DEFAULT_BOTTOM_PT` | pt | 36.0 | Configured bottom margin before clamp |
| `MIN_MARGIN_MM` | mm | 10.0 | Minimum margin clamp |
| `MIN_MARGIN_PT` | pt | 28.3465 | 10 x (72 / 25.4) |
| `EFFECTIVE_LEFT_MARGIN_PT` | pt | 28.3465 | `max(MARGIN_LEFT_PT, MIN_MARGIN_PT)` |
| `EFFECTIVE_RIGHT_MARGIN_PT` | pt | 28.3465 | `max(MARGIN_RIGHT_PT, MIN_MARGIN_PT)` |
| `EFFECTIVE_TOP_MARGIN_PT` | pt | 36.0 | `max(MARGIN_TOP_PT, MIN_MARGIN_PT)` |
| `EFFECTIVE_BOTTOM_MARGIN_PT` | pt | 36.0 | `max(MARGIN_BOTTOM_PT, MIN_MARGIN_PT)` |
| `EFFECTIVE_CONTENT_WIDTH_PT` | pt | 555.3071 | Page width minus effective left/right margins |
| `GUIDE_WIDTH_IN` | in | 8.0 | Configured guide width |
| `GUIDE_WIDTH_PT` | pt | 576.0 | 8.0 x 72, clamped to effective content width |
| `EFFECTIVE_GUIDE_WIDTH_PT` | pt | 555.3071 | Current guide width after content clamp |
| `GUIDE_MAIN_HEIGHT_MM` | mm | 10.0 | Baseline to topline |
| `GUIDE_MAIN_HEIGHT_PT` | pt | 28.3465 | 10 x (72 / 25.4) |
| `GUIDE_DESC_RATIO` | ratio | 0.45 | Descender space fraction of main height |
| `GUIDE_DESC_HEIGHT_MM` | mm | 4.5 | 10 x 0.45 |
| `GUIDE_DESC_HEIGHT_PT` | pt | 12.7559 | 4.5 x (72 / 25.4) |
| `GUIDE_PAD_TOP_MM` | mm | 2.0 | Internal padding above topline |
| `GUIDE_PAD_TOP_PT` | pt | 5.6693 | 2 x (72 / 25.4) |
| `GUIDE_ROW_HEIGHT_MM` | mm | 16.5 | 4.5 + 10 + 2 |
| `GUIDE_ROW_HEIGHT_PT` | pt | 46.7717 | 16.5 x (72 / 25.4) |
| `GUIDE_BASELINE_STROKE_PT` | pt | 1.0 | Baseline stroke width |
| `GUIDE_TOPLINE_STROKE_PT` | pt | 1.0 | Topline stroke width |
| `GUIDE_MIDLINE_STROKE_PT` | pt | 0.8 | Midline stroke width |
| `GUIDE_MIDLINE_DASH_ON_PT` | pt | 3.0 | Dash on length |
| `GUIDE_MIDLINE_DASH_OFF_PT` | pt | 3.0 | Dash off length |
| `GUIDE_TEXT_X_OFFSET_PT` | pt | 2.0 | Model text left padding inside guide |
| `GUIDE_DRAW_TOPLINE` | bool | true | Draw the solid topline |
| `MIDLINE_RATIO` | ratio | 0.5 | Midline location between baseline and topline |
| `TITLE_FONT` | name | Andika Bold / Helvetica-Bold fallback | Title and bold labels |
| `TITLE_SIZE_PT` | pt | 16.0 | Title size |
| `BODY_SIZE_PT` | pt | 11.0 | Body size |
| `SENTENCE_DISPLAY_FONT` | name | Andika Regular / Helvetica fallback | Sentence display font |
| `SENTENCE_DISPLAY_SIZE_PT` | pt | 14.0 | Sentence display size |
| `MODEL_TEXT_SAFETY` | ratio | 0.96 | Multiplier applied to computed trace model size |
| `MODEL_TEXT_COLOR` | rgb | 0.85, 0.85, 0.85 | Light gray model text |
| `MIDLINE_COLOR` | named | `reportlab.lib.colors.grey` | Midline stroke color |
| `PRIMARY_LINE_COLOR` | named | black | Baseline/topline color |
| `HEADER_TITLE_GAP_PT` | pt | 10.0 | Space below title |
| `HEADER_LINE_GAP_PT` | pt | 10.0 | Space between name and date lines |
| `HEADER_BLOCK_GAP_PT` | pt | 15.0 | Space after major header blocks |
| `EMOTION_PROMPT_GAP_PT` | pt | 12.0 | Gap between prompt and first choice |
| `EMOTION_CIRCLE_RADIUS_PT` | pt | 6.0 | Emotion choice circle radius |
| `EMOTION_CIRCLE_CENTER_OFFSET_PT` | pt | 3.0 | Circle center offset from text baseline |
| `EMOTION_LABEL_GAP_PT` | pt | 6.0 | Circle-to-label gap |
| `EMOTION_CHOICE_GAP_PT` | pt | 12.0 | Gap between choices |
| `REMINDER_BOX_PADDING_PT` | pt | 6.0 | Inner padding in reminder box |
| `REMINDER_TITLE_GAP_PT` | pt | 4.0 | Gap below reminder title |
| `REMINDER_LINE_GAP_PT` | pt | 3.0 | Gap between reminder lines |
| `SENTENCE_LABEL_GAP_PT` | pt | 4.0 | Gap below `Sentence:` label |
| `SECTION_TITLE_GAP_PT` | pt | 15.0 | Gap below section headings |
| `TRACE_ROW_GAP_PT` | pt | 10.0 | Gap between trace rows |
| `TRACE_TO_WRITE_GAP_PT` | pt | 8.0 | Gap after trace rows before write heading |
| `WRITE_ROW_GAP_MIDLINE_PT` | pt | 10.0 | Gap between adjacent midline write rows |
| `WRITE_ROW_GAP_NO_MIDLINE_PT` | pt | 18.0 | Gap when the next write row omits a midline |
| `TRACE_WRAP_ENABLED` | bool | false | Whether render-time trace wrapping is active |
| `TRACE_WRAP_MAX_LINES` | count | 2 | Maximum physical rows for a wrapped trace sentence |
| `TRACE_WRAP_EPSILON_PT` | pt | 0.5 | Width tolerance for text metrics |
| `CARTOON_MAX_W_IN` | in | 1.5 | Optional cartoon bounding box width |
| `CARTOON_MAX_H_IN` | in | 1.5 | Optional cartoon bounding box height |
| `CARTOON_PAD_MM` | mm | 6.0 | Padding from top/right content edges |

# RENDERING_PARAMS.md

| Name | Unit | Value | Description |
|---|---:|---:|---|
| PAGE_WIDTH_IN | in | 8.5 | US Letter width |
| PAGE_HEIGHT_IN | in | 11.0 | US Letter height |
| PAGE_WIDTH_PT | pt | 612.0 | 8.5 × 72 |
| PAGE_HEIGHT_PT | pt | 792.0 | 11 × 72 |
| MARGIN_LEFT_IN | in | 0.6 | Left margin |
| MARGIN_RIGHT_IN | in | 0.6 | Right margin |
| MARGIN_TOP_IN | in | 0.5 | Top margin |
| MARGIN_BOTTOM_IN | in | 0.5 | Bottom margin |
| MARGIN_LEFT_PT | pt | 43.2 | 0.6 × 72 |
| MARGIN_RIGHT_PT | pt | 43.2 | 0.6 × 72 |
| MARGIN_TOP_PT | pt | 36.0 | 0.5 × 72 |
| MARGIN_BOTTOM_PT | pt | 36.0 | 0.5 × 72 |
| CONTENT_WIDTH_IN | in | 7.3 | 8.5 - 0.6 - 0.6 |
| CONTENT_WIDTH_PT | pt | 525.6 | 7.3 × 72 |
| GUIDE_WIDTH_IN | in | 6.8 | Guide row width used in v2 |
| GUIDE_WIDTH_PT | pt | 489.6 | 6.8 × 72 |
| GUIDE_MAIN_HEIGHT_MM | mm | 15.0 | Baseline → topline |
| GUIDE_MAIN_HEIGHT_PT | pt | 42.5197 | 15 × (72/25.4) |
| GUIDE_DESC_RATIO | ratio | 0.45 | Descender space fraction of main height |
| GUIDE_DESC_HEIGHT_MM | mm | 6.75 | 15 × 0.45 |
| GUIDE_DESC_HEIGHT_PT | pt | 19.1339 | 6.75 × (72/25.4) |
| GUIDE_PAD_TOP_MM | mm | 2.0 | Internal padding above topline within row box |
| GUIDE_PAD_TOP_PT | pt | 5.6693 | 2 × (72/25.4) |
| GUIDE_ROW_HEIGHT_MM | mm | 23.75 | 6.75 + 15 + 2 |
| GUIDE_ROW_HEIGHT_PT | pt | 67.3229 | 23.75 × (72/25.4) |
| GUIDE_BASELINE_STROKE_PT | pt | 1.0 | Baseline stroke width |
| GUIDE_TOPLINE_STROKE_PT | pt | 1.0 | Topline stroke width |
| GUIDE_MIDLINE_STROKE_PT | pt | 0.8 | Midline stroke width |
| GUIDE_MIDLINE_DASH_ON_PT | pt | 3.0 | Dash on length |
| GUIDE_MIDLINE_DASH_OFF_PT | pt | 3.0 | Dash off length |
| GUIDE_TEXT_X_OFFSET_PT | pt | 4.0 | Model text left padding inside guide |
| TRACE_TEXT_GRAY_RGB | rgb | 0.75,0.75,0.75 | Light gray for model text |
| MIDLINE_GRAY | named | reportlab.lib.colors.grey | Midline stroke color |
| TITLE_FONT | name | Helvetica | Title font |
| TITLE_SIZE_PT | pt | 16 | Title size |
| BODY_FONT | name | Helvetica | Body font |
| BODY_SIZE_PT | pt | 11 | Body size |
| SENTENCE_DISPLAY_FONT | name | Andika Regular | Sentence display font |
| SENTENCE_DISPLAY_SIZE_PT | pt | 14 | Sentence display size |
| MODEL_TEXT_SIZE_RULE | formula | main_height_pt / (yMax_ref/unitsPerEm) | Calibrate model font size so A/b reach topline |
| TRACE_ROW_GAP_PT | pt | 6 | Gap between the two trace rows |
| TRACE_TO_WRITE_GAP_PT | pt | 8 | Gap after trace rows before write heading |
| WRITE_ROW_GAP_MIDLINE_PT | pt | 6 | Gap between write rows 1–3 |
| WRITE_ROW_GAP_NO_MIDLINE_PT | pt | 8 | Gap between write rows 4–5 |
| CARTOON_MAX_W_IN | in | 1.5 | Optional cartoon bounding box width |
| CARTOON_MAX_H_IN | in | 1.5 | Optional cartoon bounding box height |
| CARTOON_PAD_MM | mm | 6.0 | Padding from top/right content edges |


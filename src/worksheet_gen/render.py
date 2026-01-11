from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from . import config
from .schema import Worksheet


@dataclass(frozen=True)
class FontSet:
    regular: str
    bold: str
    regular_face: Any | None


def _warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def _register_fonts() -> FontSet:
    regular_name = config.FONT_REGULAR_NAME
    bold_name = config.FONT_BOLD_NAME
    regular_face = None

    if config.ANDIKA_REGULAR_TTF.is_file():
        regular_font = TTFont(regular_name, str(config.ANDIKA_REGULAR_TTF))
        pdfmetrics.registerFont(regular_font)
        regular_face = regular_font.face
    else:
        _warn(f"missing font: {config.ANDIKA_REGULAR_TTF}")
        regular_name = config.FALLBACK_FONT_REGULAR

    if config.ANDIKA_BOLD_TTF.is_file():
        bold_font = TTFont(bold_name, str(config.ANDIKA_BOLD_TTF))
        pdfmetrics.registerFont(bold_font)
    else:
        _warn(f"missing font: {config.ANDIKA_BOLD_TTF}")
        bold_name = config.FALLBACK_FONT_BOLD

    return FontSet(regular=regular_name, bold=bold_name, regular_face=regular_face)


def fit_font_size_to_guides(
    font_name: str,
    main_height_pts: float,
    desc_height_pts: float,
    safety: float,
) -> float:
    ascent = pdfmetrics.getAscent(font_name)   # 1000-em units
    descent = pdfmetrics.getDescent(font_name) # negative 1000-em units

    # Fallback if metrics are weird
    if ascent <= 0:
        return main_height_pts * safety

    ascent_ratio = ascent / config.FONT_EM_UNITS
    descent_ratio = (-descent) / config.FONT_EM_UNITS if descent < 0 else 0.0

    # Size constrained by ascenders in the main zone
    size_from_main = main_height_pts / ascent_ratio

    # Size constrained by descenders in the descender zone (if any)
    if descent_ratio > 0:
        size_from_desc = desc_height_pts / descent_ratio
        size = min(size_from_main, size_from_desc)
    else:
        size = size_from_main

    return size * safety


def _draw_text_line(
    c: canvas.Canvas,
    text: str,
    x: float,
    y_top: float,
    font_name: str,
    font_size: float,
    gap_after: float,
) -> float:
    baseline_y = y_top - font_size
    c.setFont(font_name, font_size)
    c.setFillColor(config.TEXT_COLOR)
    c.drawString(x, baseline_y, text)
    return baseline_y - gap_after


def _draw_emotion_line(
    c: canvas.Canvas,
    prompt: str,
    choices: list[str],
    x: float,
    y_top: float,
    font_name: str,
) -> float:
    baseline_y = y_top - config.BODY_SIZE_PT
    c.setFont(font_name, config.BODY_SIZE_PT)
    c.setFillColor(config.TEXT_COLOR)
    c.setStrokeColor(config.TEXT_COLOR)
    c.setLineWidth(config.EMOTION_CIRCLE_STROKE_PT)
    c.drawString(x, baseline_y, prompt)

    prompt_width = pdfmetrics.stringWidth(prompt, font_name, config.BODY_SIZE_PT)
    cursor_x = x + prompt_width + config.EMOTION_PROMPT_GAP_PT
    circle_center_y = baseline_y + config.EMOTION_CIRCLE_CENTER_OFFSET_PT

    for choice in choices:
        circle_center_x = cursor_x + config.EMOTION_CIRCLE_RADIUS_PT
        c.circle(circle_center_x, circle_center_y, config.EMOTION_CIRCLE_RADIUS_PT)
        label_x = cursor_x + config.EMOTION_CIRCLE_DIAMETER_PT + config.EMOTION_LABEL_GAP_PT
        c.drawString(label_x, baseline_y, choice)
        choice_width = pdfmetrics.stringWidth(choice, font_name, config.BODY_SIZE_PT)
        cursor_x = label_x + choice_width + config.EMOTION_CHOICE_GAP_PT

    return baseline_y - config.HEADER_BLOCK_GAP_PT


def _draw_reminder_box(
    c: canvas.Canvas,
    title: str,
    b_line: str,
    d_line: str,
    x: float,
    y_top: float,
    width: float,
    regular_font: str,
    bold_font: str,
) -> float:
    title_y = y_top - config.REMINDER_BOX_PADDING_PT - config.BODY_SIZE_PT
    line_one_y = title_y - config.REMINDER_TITLE_GAP_PT - config.BODY_SIZE_PT
    line_two_y = line_one_y - config.REMINDER_LINE_GAP_PT - config.BODY_SIZE_PT
    box_bottom = line_two_y - config.REMINDER_BOX_PADDING_PT
    box_height = y_top - box_bottom

    c.setStrokeColor(config.TEXT_COLOR)
    c.setLineWidth(config.REMINDER_BORDER_STROKE_PT)
    c.rect(x, box_bottom, width, box_height, stroke=1, fill=0)

    c.setFillColor(config.TEXT_COLOR)
    c.setFont(bold_font, config.BODY_SIZE_PT)
    c.drawString(x + config.REMINDER_BOX_PADDING_PT, title_y, title)

    c.setFont(regular_font, config.BODY_SIZE_PT)
    c.drawString(x + config.REMINDER_BOX_PADDING_PT, line_one_y, b_line)
    c.drawString(x + config.REMINDER_BOX_PADDING_PT, line_two_y, d_line)

    return box_bottom - config.HEADER_BLOCK_GAP_PT


def _draw_guide_row(
    c: canvas.Canvas,
    row_top: float,
    left: float,
    width: float,
    row: Any,
    model_text: str,
    font_name: str,
    model_font_size: float,
) -> float:
    topline_y = row_top - config.GUIDE_PAD_TOP_PT
    baseline_y = topline_y - config.GUIDE_MAIN_HEIGHT_PT
    row_bottom = row_top - config.GUIDE_ROW_HEIGHT_PT

    c.setStrokeColor(config.PRIMARY_LINE_COLOR)
    c.setLineWidth(config.GUIDE_BASELINE_STROKE_PT)
    c.line(left, baseline_y, left + width, baseline_y)

    if config.GUIDE_DRAW_TOPLINE:
        c.setLineWidth(config.GUIDE_TOPLINE_STROKE_PT)
        c.line(left, topline_y, left + width, topline_y)

    if row.midline:
        midline_y = baseline_y + config.GUIDE_MAIN_HEIGHT_PT * config.MIDLINE_RATIO
        c.setStrokeColor(config.MIDLINE_COLOR)
        c.setLineWidth(config.GUIDE_MIDLINE_STROKE_PT)
        c.setDash(config.GUIDE_MIDLINE_DASH_ON_PT, config.GUIDE_MIDLINE_DASH_OFF_PT)
        c.line(left, midline_y, left + width, midline_y)
        c.setDash()

    if row.model_text:
        c.setFillColor(config.MODEL_TEXT_COLOR)
        c.setFont(font_name, model_font_size)
        c.drawString(left + config.GUIDE_TEXT_X_OFFSET_PT, baseline_y, model_text)
        c.setFillColor(config.TEXT_COLOR)

    return row_bottom


def _resolve_asset_path(asset: str | None, base_dir: Path) -> Path | None:
    if not asset:
        return None
    path = Path(asset)
    if not path.is_absolute():
        candidate = base_dir / path
        if candidate.exists():
            return candidate
        path = config.REPO_ROOT / path
    return path


def _draw_cartoon(
    c: canvas.Canvas,
    worksheet: Worksheet,
    base_dir: Path,
    content_right: float,
    content_top: float,
) -> float:
    if worksheet.cartoon is None or not worksheet.cartoon.enabled:
        return content_right

    max_width_in = worksheet.cartoon.max_width_in or config.CARTOON_MAX_W_IN
    max_height_in = worksheet.cartoon.max_height_in or config.CARTOON_MAX_H_IN
    max_width_pt = config.inch(max_width_in)
    max_height_pt = config.inch(max_height_in)

    asset_path = _resolve_asset_path(worksheet.cartoon.asset, base_dir)
    has_png = asset_path is not None and asset_path.suffix.lower() == ".png"

    x_right = content_right - config.CARTOON_PAD_PT
    y_top = content_top - config.CARTOON_PAD_PT
    box_left = x_right - max_width_pt
    box_bottom = y_top - max_height_pt

    if asset_path is None:
        _warn("cartoon enabled but no asset specified; drawing placeholder")
    elif not has_png:
        _warn(f"cartoon asset is not PNG: {asset_path}")
    elif not asset_path.exists():
        _warn(f"cartoon asset missing: {asset_path}")

    if has_png and asset_path is not None and asset_path.exists():
        image = ImageReader(str(asset_path))
        img_width, img_height = image.getSize()
        if img_width > 0 and img_height > 0:
            scale = min(max_width_pt / img_width, max_height_pt / img_height)
            draw_w = img_width * scale
            draw_h = img_height * scale
            draw_x = x_right - draw_w
            draw_y = y_top - draw_h
            c.drawImage(image, draw_x, draw_y, width=draw_w, height=draw_h, mask=None)
            return box_left

    c.setStrokeColor(config.TEXT_COLOR)
    c.setLineWidth(config.CARTOON_PLACEHOLDER_STROKE_PT)
    c.rect(box_left, box_bottom, max_width_pt, max_height_pt, stroke=1, fill=0)
    return box_left


def render_pdf(worksheet: Worksheet, output_path: str | Path, base_dir: str | Path | None = None) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    base_dir = Path(base_dir) if base_dir is not None else Path.cwd()

    fonts = _register_fonts()
    model_font_size = fit_font_size_to_guides(
        fonts.regular,
        config.GUIDE_MAIN_HEIGHT_PT,
        config.GUIDE_DESC_HEIGHT_PT,
        config.MODEL_TEXT_SAFETY,
    )

    c = canvas.Canvas(
        str(output_path),
        pagesize=(config.PAGE_WIDTH_PT, config.PAGE_HEIGHT_PT),
        invariant=1,
    )
    c.setAuthor(config.PDF_AUTHOR)
    c.setSubject(config.PDF_SUBJECT)
    c.setTitle(worksheet.title)

    content_left = config.MARGIN_LEFT_PT
    content_right = config.PAGE_WIDTH_PT - config.MARGIN_RIGHT_PT
    content_top = config.PAGE_HEIGHT_PT - config.MARGIN_TOP_PT

    header_right_limit = _draw_cartoon(c, worksheet, base_dir, content_right, content_top)

    cursor_y = content_top

    cursor_y = _draw_text_line(
        c,
        worksheet.title,
        content_left,
        cursor_y,
        fonts.bold,
        config.TITLE_SIZE_PT,
        config.HEADER_TITLE_GAP_PT,
    )

    child_value = worksheet.child_name or config.DEFAULT_CHILD_NAME_PLACEHOLDER
    child_line = f"Name: {child_value}"
    cursor_y = _draw_text_line(
        c,
        child_line,
        content_left,
        cursor_y,
        fonts.regular,
        config.BODY_SIZE_PT,
        config.HEADER_LINE_GAP_PT,
    )

    cursor_y = _draw_text_line(
        c,
        worksheet.date_text,
        content_left,
        cursor_y,
        fonts.regular,
        config.BODY_SIZE_PT,
        config.HEADER_BLOCK_GAP_PT,
    )

    cursor_y = _draw_emotion_line(
        c,
        worksheet.emotion_prompt.text,
        worksheet.emotion_prompt.choices,
        content_left,
        cursor_y,
        fonts.regular,
    )

    cursor_y = _draw_reminder_box(
        c,
        worksheet.reminder_bd.title,
        worksheet.reminder_bd.b_line,
        worksheet.reminder_bd.d_line,
        content_left,
        cursor_y,
        min(config.CONTENT_WIDTH_PT, header_right_limit - content_left),
        fonts.regular,
        fonts.bold,
    )

    cursor_y = _draw_text_line(
        c,
        "Sentence:",
        content_left,
        cursor_y,
        fonts.bold,
        config.BODY_SIZE_PT,
        config.SENTENCE_LABEL_GAP_PT,
    )

    cursor_y = _draw_text_line(
        c,
        worksheet.sentence.display,
        content_left,
        cursor_y,
        fonts.regular,
        config.SENTENCE_DISPLAY_SIZE_PT,
        config.SECTION_TITLE_GAP_PT,
    )

    for index, section in enumerate(worksheet.sections):
        cursor_y = _draw_text_line(
            c,
            section.title,
            content_left,
            cursor_y,
            fonts.bold,
            config.BODY_SIZE_PT,
            config.SECTION_TITLE_GAP_PT,
        )

        rows = list(section.rows)
        for row_index, row in enumerate(rows):
            row_top = cursor_y
            cursor_y = _draw_guide_row(
                c,
                row_top,
                content_left,
                config.GUIDE_WIDTH_PT,
                row,
                worksheet.sentence.model,
                fonts.regular,
                model_font_size,
            )

            if row_index < len(rows) - 1:
                if section.type == "trace":
                    gap = config.TRACE_ROW_GAP_PT
                else:
                    next_row = rows[row_index + 1]
                    if row.midline and next_row.midline:
                        gap = config.WRITE_ROW_GAP_MIDLINE_PT
                    else:
                        gap = config.WRITE_ROW_GAP_NO_MIDLINE_PT
                cursor_y -= gap

        if index < len(worksheet.sections) - 1:
            if section.type == "trace" and worksheet.sections[index + 1].type == "write":
                cursor_y -= config.TRACE_TO_WRITE_GAP_PT
            else:
                cursor_y -= config.SECTION_GAP_PT

    c.showPage()
    c.save()

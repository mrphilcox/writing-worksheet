from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from io import BytesIO
from pathlib import Path
import sys
from typing import Any

from fontTools.ttLib import TTFont as FontToolsTTFont
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
    regular_ttf: Path | None


@dataclass(frozen=True)
class FontMetrics:
    units_per_em: float
    descent: float
    cap_height: float
    x_height: float


@dataclass(frozen=True)
class LayoutMetrics:
    margin_left: float
    margin_right: float
    margin_top: float
    margin_bottom: float
    content_left: float
    content_right: float
    content_top: float
    content_width: float
    content_height: float
    guide_width: float


def _compute_layout_metrics() -> LayoutMetrics:
    margin_left = max(config.MARGIN_LEFT_PT, config.MIN_MARGIN_PT)
    margin_right = max(config.MARGIN_RIGHT_PT, config.MIN_MARGIN_PT)
    margin_top = max(config.MARGIN_TOP_PT, config.MIN_MARGIN_PT)
    margin_bottom = max(config.MARGIN_BOTTOM_PT, config.MIN_MARGIN_PT)

    content_left = margin_left
    content_right = config.PAGE_WIDTH_PT - margin_right
    content_top = config.PAGE_HEIGHT_PT - margin_top
    content_width = config.PAGE_WIDTH_PT - margin_left - margin_right
    content_height = config.PAGE_HEIGHT_PT - margin_top - margin_bottom
    guide_width = min(config.GUIDE_WIDTH_PT, content_width)

    return LayoutMetrics(
        margin_left=margin_left,
        margin_right=margin_right,
        margin_top=margin_top,
        margin_bottom=margin_bottom,
        content_left=content_left,
        content_right=content_right,
        content_top=content_top,
        content_width=content_width,
        content_height=content_height,
        guide_width=guide_width,
    )


def _warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def _register_fonts() -> FontSet:
    regular_name = config.FONT_REGULAR_NAME
    bold_name = config.FONT_BOLD_NAME
    regular_ttf = None

    if config.ANDIKA_REGULAR_TTF.is_file():
        regular_font = TTFont(regular_name, str(config.ANDIKA_REGULAR_TTF))
        pdfmetrics.registerFont(regular_font)
        regular_ttf = config.ANDIKA_REGULAR_TTF
    else:
        _warn(f"missing font: {config.ANDIKA_REGULAR_TTF}")
        regular_name = config.FALLBACK_FONT_REGULAR

    if config.ANDIKA_BOLD_TTF.is_file():
        bold_font = TTFont(bold_name, str(config.ANDIKA_BOLD_TTF))
        pdfmetrics.registerFont(bold_font)
    else:
        _warn(f"missing font: {config.ANDIKA_BOLD_TTF}")
        bold_name = config.FALLBACK_FONT_BOLD

    return FontSet(regular=regular_name, bold=bold_name, regular_ttf=regular_ttf)


def fit_font_size_to_height(font_name: str, available_height_pts: float, safety: float) -> float:
    ascent = pdfmetrics.getAscent(font_name)
    descent = pdfmetrics.getDescent(font_name)
    em_height = (ascent - descent) / config.FONT_EM_UNITS
    if em_height <= 0:
        return available_height_pts * safety
    return (available_height_pts / em_height) * safety


@lru_cache(maxsize=None)
def _load_font_metrics(font_path: str) -> FontMetrics:
    font = FontToolsTTFont(font_path)
    try:
        head = font["head"]
        hhea = font["hhea"]
        os2 = font["OS/2"] if "OS/2" in font else None

        units_per_em = float(head.unitsPerEm)
        descent = getattr(hhea, "descent", None)
        if descent is None and os2 is not None:
            descent = getattr(os2, "sTypoDescender", None)
        if descent is None:
            descent = 0.0

        cap_height = None
        if os2 is not None:
            cap_height = getattr(os2, "sCapHeight", None)
        if cap_height:
            cap_height_value = float(cap_height)
        elif os2 is not None and getattr(os2, "usWinAscent", None):
            cap_height_value = float(os2.usWinAscent) * config.CAP_HEIGHT_FALLBACK_RATIO
        else:
            cap_height_value = float(hhea.ascent) * config.CAP_HEIGHT_FALLBACK_RATIO

        x_height = None
        if os2 is not None:
            x_height = getattr(os2, "sxHeight", None)
        if x_height:
            x_height_value = float(x_height)
        elif os2 is not None and getattr(os2, "usWinAscent", None):
            x_height_value = float(os2.usWinAscent) * config.X_HEIGHT_FALLBACK_RATIO
        else:
            x_height_value = float(hhea.ascent) * config.X_HEIGHT_FALLBACK_RATIO

        return FontMetrics(
            units_per_em=units_per_em,
            descent=float(descent),
            cap_height=cap_height_value,
            x_height=x_height_value,
        )
    finally:
        font.close()


def _compute_model_font_size(font_name: str, font_path: Path | None) -> float:
    available_cap_height_pts = config.GUIDE_MAIN_HEIGHT_PT + config.GUIDE_PAD_TOP_PT

    if font_path is None or not font_path.exists():
        _warn("cap-height metrics unavailable; using ascent-based sizing")
        return fit_font_size_to_height(
            font_name,
            available_cap_height_pts,
            config.MODEL_TEXT_SAFETY,
        )

    metrics = _load_font_metrics(str(font_path))
    if metrics.units_per_em <= 0:
        _warn("invalid font units per em; using ascent-based sizing")
        return fit_font_size_to_height(
            font_name,
            available_cap_height_pts,
            config.MODEL_TEXT_SAFETY,
        )

    cap_ratio = metrics.cap_height / metrics.units_per_em
    desc_ratio = abs(metrics.descent) / metrics.units_per_em

    size_from_caps = (
        available_cap_height_pts / cap_ratio if cap_ratio > 0 else available_cap_height_pts
    )
    size_from_desc = (
        config.GUIDE_DESC_HEIGHT_PT / desc_ratio
        if desc_ratio > 0
        else available_cap_height_pts
    )

    return min(size_from_caps, size_from_desc) * config.MODEL_TEXT_SAFETY


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


def _wrap_error_message(text: str, max_width: float) -> str:
    normalized_text = " ".join(text.split())
    return (
        f"Trace model sentence does not fit within {config.TRACE_WRAP_MAX_LINES} lines "
        f"(max width in points: {max_width:.2f}, sentence text length: {len(normalized_text)})."
    )


def wrap_text_to_width(
    text: str,
    font_name: str,
    font_size: float,
    max_width: float,
) -> list[str]:
    normalized_text = " ".join(text.split())
    if not normalized_text:
        return [""]

    def text_fits(candidate: str) -> bool:
        width = pdfmetrics.stringWidth(candidate, font_name, font_size)
        return width <= max_width + config.TRACE_WRAP_EPSILON_PT

    def break_long_word(word: str) -> list[str]:
        if (
            not config.TRACE_WRAP_HARD_BREAK_LONG_WORDS
            or len(word) < config.TRACE_WRAP_MIN_CHARS_FOR_HARD_BREAK
        ):
            raise ValueError(
                f"{_wrap_error_message(normalized_text, max_width)} "
                f"Word '{word}' is too long to fit on one line."
            )

        chunks: list[str] = []
        current_chunk = ""
        for char in word:
            candidate = current_chunk + char
            if text_fits(candidate):
                current_chunk = candidate
                continue
            if not current_chunk:
                raise ValueError(
                    f"{_wrap_error_message(normalized_text, max_width)} "
                    f"Word '{word}' is too long to fit on one line."
                )
            chunks.append(current_chunk)
            current_chunk = char
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    words = normalized_text.split(" ")
    lines: list[str] = []
    current_line = ""

    for word in words:
        candidate = f"{current_line} {word}" if current_line else word
        if text_fits(candidate):
            current_line = candidate
            continue

        if not current_line:
            chunks = break_long_word(word)
            lines.extend(chunks[:-1])
            current_line = chunks[-1] if chunks else ""
            continue

        lines.append(current_line)
        if text_fits(word):
            current_line = word
        else:
            chunks = break_long_word(word)
            lines.extend(chunks[:-1])
            current_line = chunks[-1] if chunks else ""

    if current_line:
        lines.append(current_line)

    return lines


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


def _render_to_canvas(worksheet: Worksheet, c: canvas.Canvas, base_dir: Path) -> None:
    fonts = _register_fonts()
    model_font_size = _compute_model_font_size(fonts.regular, fonts.regular_ttf)
    layout = _compute_layout_metrics()

    c.setAuthor(config.PDF_AUTHOR)
    c.setSubject(config.PDF_SUBJECT)
    c.setTitle(worksheet.title)

    content_left = layout.content_left
    content_right = layout.content_right
    content_top = layout.content_top

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
        min(layout.content_width, header_right_limit - content_left),
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
            if section.type == "trace" and row.model_text and config.TRACE_WRAP_ENABLED:
                normalized_model = " ".join(worksheet.sentence.model.split())
                available_width = layout.guide_width - config.GUIDE_TEXT_X_OFFSET_PT
                text_width = pdfmetrics.stringWidth(
                    normalized_model,
                    fonts.regular,
                    model_font_size,
                )
                if text_width <= available_width + config.TRACE_WRAP_EPSILON_PT:
                    lines = [normalized_model]
                else:
                    lines = wrap_text_to_width(
                        normalized_model,
                        fonts.regular,
                        model_font_size,
                        available_width,
                    )

                if len(lines) > config.TRACE_WRAP_MAX_LINES:
                    raise ValueError(_wrap_error_message(normalized_model, available_width))

                if len(lines) > 1:
                    required_bottom = (
                        cursor_y
                        - (config.GUIDE_ROW_HEIGHT_PT * len(lines))
                        - (config.TRACE_ROW_GAP_PT * (len(lines) - 1))
                    )
                    if required_bottom < layout.margin_bottom:
                        raise ValueError(
                            "Sentence wrap requires additional rows and does not fit on one page with current layout."
                        )

                for line_index, line in enumerate(lines):
                    row_top = cursor_y
                    cursor_y = _draw_guide_row(
                        c,
                        row_top,
                        content_left,
                        layout.guide_width,
                        row,
                        line,
                        fonts.regular,
                        model_font_size,
                    )
                    is_last_physical_row = (
                        row_index == len(rows) - 1 and line_index == len(lines) - 1
                    )
                    if not is_last_physical_row:
                        cursor_y -= config.TRACE_ROW_GAP_PT
                continue

            row_top = cursor_y
            cursor_y = _draw_guide_row(
                c,
                row_top,
                content_left,
                layout.guide_width,
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


def render_pdf(worksheet: Worksheet, output_path: str | Path, base_dir: str | Path | None = None) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    base_dir = Path(base_dir) if base_dir is not None else Path.cwd()

    c = canvas.Canvas(
        str(output_path),
        pagesize=(config.PAGE_WIDTH_PT, config.PAGE_HEIGHT_PT),
        invariant=1,
    )
    _render_to_canvas(worksheet, c, base_dir)


def render_pdf_bytes(worksheet: Worksheet, base_dir: str | Path | None = None) -> bytes:
    base_dir = Path(base_dir) if base_dir is not None else Path.cwd()
    buffer = BytesIO()
    c = canvas.Canvas(
        buffer,
        pagesize=(config.PAGE_WIDTH_PT, config.PAGE_HEIGHT_PT),
        invariant=1,
    )
    _render_to_canvas(worksheet, c, base_dir)
    data = buffer.getvalue()
    buffer.close()
    return data

from __future__ import annotations

from reportlab.pdfbase import pdfmetrics
import pytest

from worksheet_gen import config
from worksheet_gen.load import load_data
from worksheet_gen.render import (
    _compute_layout_metrics,
    _compute_model_font_size,
    _register_fonts,
    render_pdf,
    wrap_text_to_width,
)


def _wrap_metrics() -> tuple[str, float, float]:
    fonts = _register_fonts()
    model_font_size = _compute_model_font_size(fonts.regular, fonts.regular_ttf)
    layout = _compute_layout_metrics()
    max_width = layout.guide_width - config.GUIDE_TEXT_X_OFFSET_PT
    return fonts.regular, model_font_size, max_width


def _base_spec(model_text: str) -> dict[str, object]:
    return {
        "schema_version": "2.0",
        "language": "en",
        "sentence": {
            "display": "Wrap test sentence.",
            "model": model_text,
        },
    }


def _build_two_line_sentence(font_name: str, font_size: float, max_width: float) -> str:
    sentence = "practice"
    for _ in range(200):
        lines = wrap_text_to_width(sentence, font_name, font_size, max_width)
        if len(lines) == 2:
            return sentence
        if len(lines) > 2:
            break
        sentence = f"{sentence} practice"
    raise RuntimeError("Unable to build a two-line sentence for wrap test.")


def _build_long_word(font_name: str, font_size: float, max_width: float) -> str:
    word = "m" * config.TRACE_WRAP_MIN_CHARS_FOR_HARD_BREAK
    while pdfmetrics.stringWidth(word, font_name, font_size) <= max_width:
        word += "m"
    max_total_width = max_width * config.TRACE_WRAP_MAX_LINES
    while pdfmetrics.stringWidth(word, font_name, font_size) > max_total_width:
        word = word[:-1]
        if len(word) < config.TRACE_WRAP_MIN_CHARS_FOR_HARD_BREAK:
            raise RuntimeError("Unable to build a long word within wrap limits.")
    if pdfmetrics.stringWidth(word, font_name, font_size) <= max_width:
        raise RuntimeError("Long word did not exceed wrap width.")
    return word


def test_trace_wrap_two_lines(tmp_path) -> None:
    font_name, font_size, max_width = _wrap_metrics()
    sentence = _build_two_line_sentence(font_name, font_size, max_width)
    lines = wrap_text_to_width(sentence, font_name, font_size, max_width)
    assert len(lines) == 2

    worksheet = load_data(_base_spec(sentence))
    output_path = tmp_path / "wrap-two-lines.pdf"
    render_pdf(worksheet, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 5 * 1024


def test_trace_wrap_overflow_raises(tmp_path) -> None:
    font_name, font_size, max_width = _wrap_metrics()
    long_sentence = ("practice " * 200).strip()
    assert len(wrap_text_to_width(long_sentence, font_name, font_size, max_width)) > (
        config.TRACE_WRAP_MAX_LINES
    )

    worksheet = load_data(_base_spec(long_sentence))
    with pytest.raises(ValueError) as excinfo:
        render_pdf(worksheet, tmp_path / "wrap-too-long.pdf")

    message = str(excinfo.value)
    assert "does not fit within" in message
    assert "max width in points" in message
    assert "sentence text length" in message


def test_trace_wrap_hard_break_long_word(tmp_path) -> None:
    font_name, font_size, max_width = _wrap_metrics()
    word = _build_long_word(font_name, font_size, max_width)
    assert pdfmetrics.stringWidth(word, font_name, font_size) > max_width

    lines = wrap_text_to_width(word, font_name, font_size, max_width)
    assert 1 < len(lines) <= config.TRACE_WRAP_MAX_LINES

    worksheet = load_data(_base_spec(word))
    output_path = tmp_path / "wrap-hard-break.pdf"
    render_pdf(worksheet, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 5 * 1024

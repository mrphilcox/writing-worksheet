from __future__ import annotations

import math
from pathlib import Path

from worksheet_gen import config
from worksheet_gen.load import load_yaml
from worksheet_gen.render import _compute_layout_metrics, render_pdf


def test_min_margin_clamps_content_width(monkeypatch, tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    input_path = repo_root / "examples" / "example-full.yaml"
    worksheet = load_yaml(input_path)

    default_content_width = config.PAGE_WIDTH_PT - config.MARGIN_LEFT_PT - config.MARGIN_RIGHT_PT

    small_margin = config.mm(6.0)
    monkeypatch.setattr(config, "MARGIN_LEFT_PT", small_margin)
    monkeypatch.setattr(config, "MARGIN_RIGHT_PT", small_margin)
    monkeypatch.setattr(config, "MIN_MARGIN_PT", config.mm(5.0))

    expanded_layout = _compute_layout_metrics()
    assert expanded_layout.content_width > default_content_width

    clamped_margin = config.mm(10.0)
    monkeypatch.setattr(config, "MIN_MARGIN_PT", clamped_margin)
    clamped_layout = _compute_layout_metrics()

    assert math.isclose(clamped_layout.margin_left, clamped_margin, rel_tol=0.0, abs_tol=1e-6)
    assert clamped_layout.content_width < expanded_layout.content_width

    output_path = tmp_path / "min-margin.pdf"
    render_pdf(worksheet, output_path, base_dir=input_path.parent)
    assert output_path.exists()
    assert output_path.stat().st_size > 5 * 1024

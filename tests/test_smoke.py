from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from worksheet_gen.load import load_yaml
from worksheet_gen.render import render_pdf


def test_smoke() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    input_path = repo_root / "examples" / "example-full.yaml"

    worksheet = load_yaml(input_path)
    with TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "smoke.pdf"
        render_pdf(worksheet, output_path, base_dir=input_path.parent)
        assert output_path.exists()
        assert output_path.stat().st_size > 5 * 1024

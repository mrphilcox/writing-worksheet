# Repository Guidelines

## Project Structure & Module Organization
- `src/worksheet_gen/` contains the PDF generator package (CLI, schema, loader, renderer).
- `tests/` holds pytest-based smoke tests.
- `examples/` includes sample YAML inputs for rendering.
- `assets/` stores fonts and art assets referenced by YAML.
- `out/` is used for generated PDFs or local artifacts (keep generated files out of git).
- Design references live in `SPEC.md`, `RENDERING_PARAMS.md`, and `YAML_SCHEMA.md`.

## Build, Test, and Development Commands
- `python -m worksheet_gen render examples/example-full.yaml out/example.pdf` renders a PDF using the module entry point.
- `worksheet-gen render examples/example-full.yaml out/example.pdf` runs the installed CLI script.
- `pytest` runs the smoke test suite in `tests/`.
- `pip install -e .` installs the package in editable mode for local development.

## Coding Style & Naming Conventions
- Python 3.12+, 4-space indentation, explicit type hints, and `pathlib.Path` for file paths.
- Module and function names use `snake_case`; constants use `UPPER_SNAKE_CASE`.
- Prefer small, single-purpose functions (loading, validation, rendering are separate modules).
- Keep YAML schema changes synchronized with examples and documentation.

## Testing Guidelines
- Framework: pytest (see `tests/test_smoke.py`).
- Tests should be fast and use temporary directories for generated PDFs.
- Naming: `test_*.py` files and `test_*` functions. Keep coverage focused on CLI, YAML loading, and rendering behavior.
- When adding renderer logic, add a focused regression test that asserts output size or key metadata.

## Commit & Pull Request Guidelines
- Commit messages are short, sentence-case, imperative (e.g., "Update font size calculation").
- PRs should include a concise summary, linked issue (if any), and sample output PDFs or screenshots when rendering changes.
- Call out asset additions or font changes explicitly in the PR description.

## Configuration & Assets
- YAML inputs follow `YAML_SCHEMA.md`; update examples when schema changes.
- Font and art assets live under `assets/`; reference them with paths relative to the YAML file.
- If adding new assets, keep filenames descriptive (e.g., `assets/cartoons/robot-wave.png`).

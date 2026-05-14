# Worksheet Gen

Worksheet Gen renders deterministic US Letter handwriting worksheets from YAML
input, with both a command-line interface and a small local web preview form.

The renderer uses ReportLab, validates input with Pydantic, and reads the Andika
font assets from this repository when they are available. Generated PDFs should
be written to `out/` or another local artifact directory.

## Install

```bash
pip install -e .
```

Python 3.12 or newer is required.

## Render From YAML

```bash
python -m worksheet_gen render examples/example-full.yaml out/example.pdf
```

After editable installation, the console script is equivalent:

```bash
worksheet-gen render examples/example-full.yaml out/example.pdf
```

Asset paths in YAML are resolved relative to the YAML file first, then relative
to the repository root. For example, `examples/example-full.yaml` enables the
placeholder cartoon at `assets/cartoons/placeholder-unicorn.png`.

## Web Preview

```bash
worksheet-gen serve --host 127.0.0.1 --port 8000
```

Or:

```bash
python -m worksheet_gen serve --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` in a browser. The form accepts a sentence, optional
child name, optional title, and optional date line.

- Click `Preview` to render the PDF inline below the form.
- Click `Download PDF` to save the worksheet.

## Input Files

YAML inputs follow [YAML_SCHEMA.md](YAML_SCHEMA.md). Minimal input only needs a
schema version, language, and the fields that should override defaults; the
loader fills in the standard v2 worksheet structure when sections, reminder
text, emotion prompt, or cartoon settings are omitted.

See:

- [examples/example-minimal.yaml](examples/example-minimal.yaml)
- [examples/example-full.yaml](examples/example-full.yaml)
- [examples/example-wrap.yaml](examples/example-wrap.yaml)

## Design References

- [SPEC.md](SPEC.md): current worksheet layout and renderer behavior.
- [RENDERING_PARAMS.md](RENDERING_PARAMS.md): config constants and derived values.
- [TUNING.md](TUNING.md): which `config.py` knobs to adjust for visual changes.
- [ASSETS.md](ASSETS.md): expected font and cartoon assets.
- [ACCEPTANCE_CHECKLIST.md](ACCEPTANCE_CHECKLIST.md): manual PDF review checklist.

## Tests

```bash
pytest
```

The smoke tests render PDFs into temporary directories and exercise the CLI
loader, renderer, wrapping helpers, layout clamp logic, and web preview routes.

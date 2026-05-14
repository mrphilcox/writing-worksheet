# ASSETS.md

## Asset locations

Runtime assets live under `assets/`:

- `assets/fonts/Andika-Regular.ttf`
- `assets/fonts/Andika-Bold.ttf`
- `assets/cartoons/placeholder-unicorn.png`

The renderer resolves relative cartoon paths against the YAML file's directory
first, then against the repository root. Font paths are configured in
`src/worksheet_gen/config.py`.

## Fonts

Andika Regular is the primary handwriting font. It is used for the sentence
display and model text inside trace rows.

Andika Bold is registered for headings when available. If either font file is
missing, the renderer prints a warning and falls back to ReportLab's built-in
Helvetica or Helvetica-Bold fonts.

Keep replacement font filenames descriptive and update `config.py`,
[RENDERING_PARAMS.md](RENDERING_PARAMS.md), and any examples that depend on the
new files.

## Cartoons

The current renderer supports PNG cartoon assets. A cartoon can be enabled in
YAML with:

```yaml
cartoon:
  enabled: true
  asset: "assets/cartoons/placeholder-unicorn.png"
  placement: "header_top_right"
  max_width_in: 1.5
  max_height_in: 1.5
```

When a cartoon is enabled but cannot be rendered, the PDF includes a placeholder
rectangle in the same header position.

## Generated artifacts

Generated PDFs and other local outputs belong in `out/` or a temporary
directory and should stay out of git.

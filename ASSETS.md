# ASSETS.md

## Required assets

### Fonts
1. **Andika Regular**
   - File: `Andika-Regular.ttf` (or equivalent upright regular)
   - Path: `assets/fonts/andika/Andika-Regular.ttf`

> Note: If you keep the upstream font package, ensure the generator always selects the *regular upright* face and not italic/bold.

### Cartoons / line art (optional; OFF by default in v2)
- Placeholder SVGs (line art, colorable)
  - `assets/cartoons/placeholder-unicorn.svg`
  - `assets/cartoons/placeholder-rainbow.svg`
  - `assets/cartoons/placeholder-princess.svg`

### No other icons are required in v2
- The open-circle bullets are plain text `◯`.

---

## Recommended repo layout

- `spec/SPEC.md`
- `spec/YAML_SCHEMA.md`
- `spec/RENDERING_PARAMS.md`
- `spec/ASSETS.md`
- `spec/ACCEPTANCE_CHECKLIST.md`
- `assets/fonts/andika/Andika-Regular.ttf`
- `assets/cartoons/*.svg`
- `examples/example-minimal.yaml`
- `examples/example-full.yaml`


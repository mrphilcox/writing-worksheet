# YAML_SCHEMA.md

## YAML schema (worksheet instance)

Top-level keys:

- `schema_version` (string, required): e.g. `"2.0"`
- `language` (string, required): `"en"` or `"fr"`
- `title` (string, optional): defaults to:
  - English: `"Abby’s Handwriting Practice – English"`
  - French: `"Pratique d’écriture – Français"`
- `child_name` (string, optional): used only for templating text if desired later (v2 does not require dynamic substitution)
- `date_text` (string, optional): default `"Date: ____________________"` (English) / `"Date : ____________________"` (French)
- `emotion_prompt` (object, optional):
  - `text` (string): prompt line
  - `choices` (list of strings): 3 choices displayed inline with open circles
- `reminder_bd` (object, required in v2):
  - `title` (string): e.g. `"Remember:"` / `"Rappel :"`
  - `b_line` (string)
  - `d_line` (string)
- `sentence` (object, required):
  - `display` (string): shown under “Sentence:”
  - `model` (string): used for trace rows (normally same as display)
- `sections` (list, required):
  - Each section:
    - `type` (string): `"trace"` or `"write"`
    - `title` (string): section heading text
    - `rows` (list of row specs):
      - `midline` (bool)
      - `model_text` (bool)  # whether to draw model text in this row
- `cartoon` (object, optional):
  - `enabled` (bool)
  - `asset` (string): path to SVG (repo-relative)
  - `placement` (string): `"header_top_right"` (only supported placement in v2)
  - `max_width_in` (float): default 1.5
  - `max_height_in` (float): default 1.5

### Required v2 behavior
- If a key is omitted, renderer must fall back to the v2 defaults defined in SPEC.md.
- Section row counts must match v2 unless you later extend the spec.

---


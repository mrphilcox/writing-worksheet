# YAML_SCHEMA.md

## YAML schema

Worksheet YAML describes one handwriting worksheet instance. The public schema
version is currently `"2.0"`.

The loader accepts sparse YAML and applies defaults before Pydantic validation.
That means fields documented as defaultable may be omitted from input files even
though the validated `Worksheet` model always contains them.

## Top-level keys

- `schema_version` (string, required): must be `"2.0"`.
- `language` (string, required): `"en"` or `"fr"`.
- `title` (string, optional): worksheet title. Defaults by language.
- `child_name` (string, optional): printed on the `Name:` line. If omitted, the
  renderer prints a blank underline placeholder.
- `date_text` (string, optional): date line text. Defaults by language.
- `emotion_prompt` (object, optional): prompt plus exactly three choices.
- `reminder_bd` (object, optional): b/d reminder copy.
- `sentence` (object, optional): display and trace sentence text.
- `sections` (list, optional): trace/write section definitions.
- `cartoon` (object, optional): optional header image settings.

Unknown keys are rejected at every schema level.

## Defaults

When fields are omitted, English defaults are:

- `title`: `Abby’s Handwriting Practice – English`
- `date_text`: `Date: ____________________`
- `emotion_prompt.text`: `How does this feel today?`
- `emotion_prompt.choices`: `Easy`, `Okay`, `Hard`
- `reminder_bd.title`: `Remember:`
- `reminder_bd.b_line`: `b = stick first, then circle (ball)`
- `reminder_bd.d_line`: `d = circle first, then stick (dog)`
- `sentence.display`: `Abby bakes bread.`
- `sentence.model`: the `sentence.display` value
- `cartoon.enabled`: `false`
- `cartoon.placement`: `header_top_right`
- `cartoon.max_width_in`: `1.5`
- `cartoon.max_height_in`: `1.5`

French defaults currently cover the title and date line. Other default content
uses the English values unless the YAML overrides it.

## Nested objects

### `emotion_prompt`

- `text` (string, optional when object is provided): prompt shown before choices.
- `choices` (list of strings, optional when object is provided): exactly three
  choices, rendered as circle controls with labels.

### `reminder_bd`

- `title` (string, optional when object is provided)
- `b_line` (string, optional when object is provided)
- `d_line` (string, optional when object is provided)

### `sentence`

- `display` (string, optional when object is provided): shown under `Sentence:`.
- `model` (string, optional): drawn as model text in trace rows. Defaults to
  `display`.

### `sections`

Each section is either `trace` or `write`.

Trace section:

- `type`: `"trace"`
- `title`: section heading text
- `rows`: list of row specs

Write section:

- `type`: `"write"`
- `title`: section heading text
- `rows`: list of row specs

Row spec:

- `midline` (bool): whether to draw the dashed midline.
- `model_text` (bool): whether to draw the sentence model text.

Write rows must set `model_text: false`; validation rejects write rows with
model text enabled.

The default v2 sections are:

- Trace, 2 rows:
  - row 1: `midline: true`, `model_text: true`
  - row 2: `midline: false`, `model_text: true`
- Write, 5 rows:
  - rows 1-3: `midline: true`, `model_text: false`
  - rows 4-5: `midline: false`, `model_text: false`

### `cartoon`

- `enabled` (bool, optional): whether to draw the image or placeholder.
- `asset` (string or null, optional): image path. PNG is the supported rendered
  format.
- `placement` (string, optional): only `"header_top_right"` is supported.
- `max_width_in` (float, optional): defaults to `1.5`.
- `max_height_in` (float, optional): defaults to `1.5`.

If `enabled` is true and the asset is missing, omitted, or not a PNG, the
renderer emits a warning and draws a placeholder rectangle.

## Minimal example

```yaml
schema_version: "2.0"
language: "en"
sentence:
  display: "Abby bakes bread."
```

## Full example

See [examples/example-full.yaml](examples/example-full.yaml).

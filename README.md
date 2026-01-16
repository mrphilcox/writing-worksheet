# Worksheet Gen

## Install

`pip install -e .`

## CLI

`python -m worksheet_gen render examples/example-full.yaml out/example.pdf`

## Web

`worksheet-gen serve --host 127.0.0.1 --port 8000`

Or:

`python -m worksheet_gen serve --host 127.0.0.1 --port 8000`

Open `http://127.0.0.1:8000` in a browser, fill out the form, then:

- Click "Preview" to render the PDF inline below the form.
- Click "Download PDF" to save the worksheet.

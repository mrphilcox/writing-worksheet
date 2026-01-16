from __future__ import annotations

import html

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, Response

from . import config
from .load import load_data
from .render import render_pdf_bytes

app = FastAPI()

MAX_SENTENCE_LEN = 200

def _html_page() -> str:
    title_placeholder = html.escape(config.DEFAULT_TITLE_EN)
    date_placeholder = html.escape(config.DEFAULT_DATE_EN)
    sentence_placeholder = html.escape(config.DEFAULT_SENTENCE_DISPLAY_EN)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Worksheet Generator</title>
    <style>
      body {{
        font-family: "Helvetica Neue", Arial, sans-serif;
        margin: 2rem;
        color: #1b1b1b;
        background: #f7f6f2;
      }}
      main {{
        max-width: 720px;
        margin: 0 auto;
      }}
      form {{
        display: grid;
        gap: 0.6rem;
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
      }}
      label {{
        font-weight: 600;
      }}
      input,
      textarea {{
        padding: 0.5rem 0.7rem;
        font-size: 1rem;
        border-radius: 6px;
        border: 1px solid #c9c6bf;
      }}
      textarea {{
        min-height: 90px;
        resize: vertical;
      }}
      .actions {{
        display: flex;
        gap: 0.75rem;
        margin-top: 0.5rem;
      }}
      button {{
        padding: 0.6rem 1.2rem;
        border-radius: 6px;
        border: 1px solid #1b1b1b;
        background: #1b1b1b;
        color: #ffffff;
        cursor: pointer;
      }}
      button[formaction="/download"] {{
        background: #ffffff;
        color: #1b1b1b;
      }}
      section {{
        margin-top: 1.5rem;
      }}
      iframe {{
        width: 100%;
        height: 720px;
        border: 1px solid #c9c6bf;
        border-radius: 10px;
        background: #ffffff;
      }}
    </style>
  </head>
  <body>
    <main>
      <h1>Worksheet Generator</h1>
      <form action="/preview" method="post" target="preview_frame">
        <label for="child_name">Child name (optional)</label>
        <input id="child_name" name="child_name" type="text" autocomplete="off">

        <label for="sentence_text">Sentence text</label>
        <textarea id="sentence_text" name="sentence_text" maxlength="{MAX_SENTENCE_LEN}" required
          placeholder="{sentence_placeholder}"></textarea>

        <label for="title">Title (optional)</label>
        <input id="title" name="title" type="text" placeholder="{title_placeholder}">

        <label for="date_text">Date (optional)</label>
        <input id="date_text" name="date_text" type="text" placeholder="{date_placeholder}">

        <div class="actions">
          <button type="submit">Preview</button>
          <button type="submit" formaction="/download" formtarget="_self">Download PDF</button>
        </div>
      </form>

      <section>
        <h2>Preview</h2>
        <iframe name="preview_frame" title="Worksheet preview"></iframe>
      </section>
    </main>
  </body>
</html>
"""


def _collapse_whitespace(value: str) -> str:
    return " ".join(value.split())


def _normalize_optional(value: str | None) -> str | None:
    if value is None:
        return None
    value = _collapse_whitespace(value)
    if not value:
        return None
    return value


def _validate_sentence_text(value: str) -> str:
    normalized = _collapse_whitespace(value)
    if not normalized:
        raise ValueError("Sentence text is required.")
    if len(normalized) > MAX_SENTENCE_LEN:
        raise ValueError(f"Sentence text must be {MAX_SENTENCE_LEN} characters or fewer.")
    return normalized


def _build_worksheet(
    child_name: str | None,
    sentence_text: str,
    title: str | None,
    date_text: str | None,
) -> bytes:
    sentence_text = _validate_sentence_text(sentence_text)
    data = {
        "schema_version": "2.0",
        "language": "en",
        "title": _normalize_optional(title),
        "child_name": _normalize_optional(child_name),
        "date_text": _normalize_optional(date_text),
        "sentence": {"display": sentence_text, "model": sentence_text},
    }
    worksheet = load_data(data)
    return render_pdf_bytes(worksheet, base_dir=config.REPO_ROOT)


def _error_response(message: str) -> HTMLResponse:
    safe_message = html.escape(message)
    content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Worksheet Generator - Error</title>
  </head>
  <body>
    <main>
      <h1>Worksheet Generator</h1>
      <p>{safe_message}</p>
      <p><a href="/">Back to the form</a></p>
    </main>
  </body>
</html>
"""
    return HTMLResponse(content=content, status_code=400)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return _html_page()


@app.post("/preview")
def preview(
    sentence_text: str = Form(...),
    child_name: str | None = Form(default=None),
    title: str | None = Form(default=None),
    date_text: str | None = Form(default=None),
) -> Response:
    try:
        pdf_bytes = _build_worksheet(child_name, sentence_text, title, date_text)
    except ValueError as exc:
        return _error_response(str(exc))
    return Response(content=pdf_bytes, media_type="application/pdf")


@app.post("/download")
def download(
    sentence_text: str = Form(...),
    child_name: str | None = Form(default=None),
    title: str | None = Form(default=None),
    date_text: str | None = Form(default=None),
) -> Response:
    try:
        pdf_bytes = _build_worksheet(child_name, sentence_text, title, date_text)
    except ValueError as exc:
        return _error_response(str(exc))
    headers = {"Content-Disposition": 'attachment; filename="worksheet.pdf"'}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)

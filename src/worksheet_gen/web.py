from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, Response
import yaml

from . import config
from .load import load_data
from .render import render_pdf_bytes

app = FastAPI()

EXAMPLE_YAML_PATH = config.REPO_ROOT / "examples" / "example-full.yaml"
DEFAULT_CHILD_NAME = "____________"
MAX_CHILD_NAME_LEN = 32
FILENAME_SAFE_RE = re.compile(r"[^A-Za-z0-9-]+")

HTML_PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Worksheet Generator</title>
  </head>
  <body>
    <main>
      <h1>Worksheet Generator</h1>
      <form action="/generate" method="post">
        <label for="child_name">Child name</label>
        <input id="child_name" name="child_name" type="text" maxlength="32" autocomplete="off">
        <button type="submit">Download PDF</button>
      </form>
    </main>
  </body>
</html>
"""


def _sanitize_child_name(value: str | None) -> str:
    value = "" if value is None else value
    value = value.strip()[:MAX_CHILD_NAME_LEN]
    if not value:
        return DEFAULT_CHILD_NAME
    return value


def _safe_filename(child_name: str) -> str:
    slug = FILENAME_SAFE_RE.sub("-", child_name).strip("-")
    if not slug:
        slug = "worksheet"
    return f"worksheet-{slug}.pdf"


def _load_base_spec(child_name: str) -> dict[str, Any]:
    raw = yaml.safe_load(EXAMPLE_YAML_PATH.read_text(encoding="utf-8"))
    if raw is None:
        raise ValueError("example YAML is empty")
    if not isinstance(raw, dict):
        raise ValueError("example YAML must be a mapping")

    data = dict(raw)
    data["child_name"] = child_name
    return data


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return HTML_PAGE


@app.post("/generate")
def generate(child_name: str = Form(default="")) -> Response:
    sanitized = _sanitize_child_name(child_name)
    data = _load_base_spec(sanitized)
    worksheet = load_data(data)
    pdf_bytes = render_pdf_bytes(worksheet, base_dir=EXAMPLE_YAML_PATH.parent)
    filename = _safe_filename(sanitized)
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)

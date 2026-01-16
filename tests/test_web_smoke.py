from __future__ import annotations

from fastapi.testclient import TestClient

from worksheet_gen.web import app


def test_web_form() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "name=\"sentence_text\"" in response.text
    assert "action=\"/preview\"" in response.text
    assert "formaction=\"/download\"" in response.text


def test_web_preview() -> None:
    client = TestClient(app)
    response = client.post("/preview", data={"sentence_text": "Ava writes letters."})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert len(response.content) > 1024


def test_web_download() -> None:
    client = TestClient(app)
    response = client.post("/download", data={"sentence_text": "Ava writes letters."})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert "attachment" in response.headers.get("content-disposition", "").lower()

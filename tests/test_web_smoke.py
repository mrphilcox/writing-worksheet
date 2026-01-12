from __future__ import annotations

from fastapi.testclient import TestClient

from worksheet_gen.web import app


def test_web_form() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "name=\"child_name\"" in response.text
    assert "action=\"/generate\"" in response.text


def test_web_generate() -> None:
    client = TestClient(app)
    response = client.post("/generate", data={"child_name": "Ava"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert len(response.content) > 1024

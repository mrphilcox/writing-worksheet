from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from . import config
from .schema import Worksheet


class LoadError(RuntimeError):
    pass


def _default_sections() -> list[dict[str, Any]]:
    return [
        {
            "type": "trace",
            "title": "Trace (2 times):",
            "rows": [
                {"midline": True, "model_text": True},
                {"midline": False, "model_text": True},
            ],
        },
        {
            "type": "write",
            "title": "Write (5 times):",
            "rows": [
                {"midline": True, "model_text": False},
                {"midline": True, "model_text": False},
                {"midline": True, "model_text": False},
                {"midline": False, "model_text": False},
                {"midline": False, "model_text": False},
            ],
        },
    ]


def _apply_defaults(data: dict[str, Any]) -> dict[str, Any]:
    result = dict(data)
    language = result.get("language")
    if language not in {"en", "fr"}:
        raise LoadError("language must be 'en' or 'fr'")

    if result.get("title") is None:
        result["title"] = (
            config.DEFAULT_TITLE_EN if language == "en" else config.DEFAULT_TITLE_FR
        )

    if result.get("date_text") is None:
        result["date_text"] = (
            config.DEFAULT_DATE_EN if language == "en" else config.DEFAULT_DATE_FR
        )

    emotion_prompt = result.get("emotion_prompt")
    if emotion_prompt is None:
        result["emotion_prompt"] = {
            "text": config.DEFAULT_EMOTION_TEXT_EN,
            "choices": list(config.DEFAULT_EMOTION_CHOICES_EN),
        }
    else:
        emotion_prompt = dict(emotion_prompt)
        if emotion_prompt.get("text") is None:
            emotion_prompt["text"] = config.DEFAULT_EMOTION_TEXT_EN
        if emotion_prompt.get("choices") is None:
            emotion_prompt["choices"] = list(config.DEFAULT_EMOTION_CHOICES_EN)
        result["emotion_prompt"] = emotion_prompt

    reminder_bd = result.get("reminder_bd")
    if reminder_bd is None:
        reminder_bd = {}
    reminder_bd = dict(reminder_bd)
    reminder_bd.setdefault("title", config.DEFAULT_REMINDER_TITLE_EN)
    reminder_bd.setdefault("b_line", config.DEFAULT_REMINDER_B_LINE_EN)
    reminder_bd.setdefault("d_line", config.DEFAULT_REMINDER_D_LINE_EN)
    result["reminder_bd"] = reminder_bd

    sentence = result.get("sentence")
    if sentence is None:
        sentence = {}
    sentence = dict(sentence)
    sentence.setdefault("display", config.DEFAULT_SENTENCE_DISPLAY_EN)
    if sentence.get("model") is None:
        sentence["model"] = sentence["display"]
    result["sentence"] = sentence

    if result.get("sections") is None:
        result["sections"] = _default_sections()

    cartoon = result.get("cartoon")
    if cartoon is None:
        result["cartoon"] = {
            "enabled": False,
            "asset": None,
            "placement": "header_top_right",
            "max_width_in": config.CARTOON_MAX_W_IN,
            "max_height_in": config.CARTOON_MAX_H_IN,
        }
    else:
        cartoon = dict(cartoon)
        cartoon.setdefault("enabled", False)
        cartoon.setdefault("placement", "header_top_right")
        cartoon.setdefault("max_width_in", config.CARTOON_MAX_W_IN)
        cartoon.setdefault("max_height_in", config.CARTOON_MAX_H_IN)
        result["cartoon"] = cartoon

    return result


def load_yaml(path: str | Path) -> Worksheet:
    path = Path(path)
    if not path.exists():
        raise LoadError(f"input file not found: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        raise LoadError("input YAML is empty")
    if not isinstance(raw, dict):
        raise LoadError("input YAML must be a mapping")

    return load_data(raw)


def load_data(data: dict[str, Any]) -> Worksheet:
    data = _apply_defaults(data)
    return Worksheet.model_validate(data)

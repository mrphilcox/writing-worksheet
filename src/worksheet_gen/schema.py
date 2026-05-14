from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictStr, field_validator


class StrictModel(BaseModel):
    """Base model for YAML data: strict types and no unknown keys."""

    model_config = ConfigDict(extra="forbid", strict=True)


class EmotionPrompt(StrictModel):
    """Prompt text plus exactly three rendered choice labels."""

    text: StrictStr
    choices: list[StrictStr]

    @field_validator("choices")
    @classmethod
    def _choices_len(cls, value: list[StrictStr]) -> list[StrictStr]:
        if len(value) != 3:
            raise ValueError("emotion_prompt.choices must have exactly 3 items")
        return value


class ReminderBD(StrictModel):
    """Copy for the b/d reminder box."""

    title: StrictStr
    b_line: StrictStr
    d_line: StrictStr


class Sentence(StrictModel):
    """Sentence shown in the header and optionally drawn in trace rows."""

    display: StrictStr
    model: StrictStr


class Cartoon(StrictModel):
    """Optional header cartoon configuration."""

    enabled: StrictBool
    asset: StrictStr | None = None
    placement: Literal["header_top_right"]
    max_width_in: StrictFloat | None = None
    max_height_in: StrictFloat | None = None


class RowSpec(StrictModel):
    """One handwriting guide row."""

    midline: StrictBool
    model_text: StrictBool


class TraceSection(StrictModel):
    """Section whose rows may draw model text."""

    type: Literal["trace"]
    title: StrictStr
    rows: list[RowSpec]


class WriteSection(StrictModel):
    """Section for independent writing rows; model text is not allowed."""

    type: Literal["write"]
    title: StrictStr
    rows: list[RowSpec]

    @field_validator("rows")
    @classmethod
    def _no_model_text(cls, rows: list[RowSpec]) -> list[RowSpec]:
        for row in rows:
            if row.model_text:
                raise ValueError("write section rows must have model_text == false")
        return rows


Section = Annotated[TraceSection | WriteSection, Field(discriminator="type")]


class Worksheet(StrictModel):
    """Validated worksheet instance after loader defaults are applied."""

    schema_version: Literal["2.0"]
    language: Literal["en", "fr"]
    title: StrictStr
    child_name: StrictStr | None = None
    date_text: StrictStr
    emotion_prompt: EmotionPrompt
    reminder_bd: ReminderBD
    sentence: Sentence
    sections: list[Section]
    cartoon: Cartoon | None = None

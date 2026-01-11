from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictStr, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class EmotionPrompt(StrictModel):
    text: StrictStr
    choices: list[StrictStr]

    @field_validator("choices")
    @classmethod
    def _choices_len(cls, value: list[StrictStr]) -> list[StrictStr]:
        if len(value) != 3:
            raise ValueError("emotion_prompt.choices must have exactly 3 items")
        return value


class ReminderBD(StrictModel):
    title: StrictStr
    b_line: StrictStr
    d_line: StrictStr


class Sentence(StrictModel):
    display: StrictStr
    model: StrictStr


class Cartoon(StrictModel):
    enabled: StrictBool
    asset: StrictStr | None = None
    placement: Literal["header_top_right"]
    max_width_in: StrictFloat | None = None
    max_height_in: StrictFloat | None = None


class RowSpec(StrictModel):
    midline: StrictBool
    model_text: StrictBool


class TraceSection(StrictModel):
    type: Literal["trace"]
    title: StrictStr
    rows: list[RowSpec]


class WriteSection(StrictModel):
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

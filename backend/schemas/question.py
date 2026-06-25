"""Pydantic-схемы вопроса."""

import uuid

from pydantic import BaseModel, ConfigDict

from backend.models.question import QuestionType


class QuestionCreate(BaseModel):
    """Данные для создания вопроса."""

    text: str
    question_type: QuestionType = QuestionType.OPEN_TEXT
    reference_answer: str = ""
    difficulty: float = 0.0


class QuestionRead(BaseModel):
    """Представление вопроса."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lesson_id: uuid.UUID
    text: str
    question_type: QuestionType
    reference_answer: str
    difficulty: float

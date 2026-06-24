"""Pydantic-схемы сессии и ответа."""

import uuid

from pydantic import BaseModel, ConfigDict

from backend.models.session import SessionStatus


class SessionCreate(BaseModel):
    """Данные для запуска учебной сессии."""

    lesson_id: uuid.UUID


class SessionRead(BaseModel):
    """Представление учебной сессии."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    student_id: uuid.UUID
    lesson_id: uuid.UUID
    status: SessionStatus


class AnswerSubmit(BaseModel):
    """Отправка ответа на вопрос."""

    question_id: uuid.UUID
    text: str


class AnswerRead(BaseModel):
    """Результат проверки ответа."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question_id: uuid.UUID
    is_correct: bool | None
    score: float

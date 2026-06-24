"""Pydantic-схемы курса и урока."""

import uuid

from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):
    """Данные для создания курса."""

    title: str
    description: str = ""


class CourseRead(BaseModel):
    """Представление курса."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str
    teacher_id: uuid.UUID


class LessonCreate(BaseModel):
    """Данные для создания урока."""

    title: str
    content: str = ""
    order_index: int = 0
    knowledge_node_id: str | None = None


class LessonRead(BaseModel):
    """Представление урока."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    course_id: uuid.UUID
    title: str
    content: str
    order_index: int
    knowledge_node_id: str | None

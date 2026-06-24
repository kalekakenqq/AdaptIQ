"""Модель вопроса к уроку."""

import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class QuestionType(str, enum.Enum):
    """Тип вопроса."""

    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_TEXT = "open_text"


class Question(Base):
    """Вопрос, используемый для проверки знаний студента."""

    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lessons.id"), index=True, nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(Enum(QuestionType), nullable=False)
    reference_answer: Mapped[str] = mapped_column(Text, default="")
    difficulty: Mapped[float] = mapped_column(Float, default=0.0)

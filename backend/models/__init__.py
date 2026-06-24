"""Импорт всех ORM-моделей для регистрации в Base.metadata."""

from backend.models.analytics import StudentAnalytics
from backend.models.answer import Answer
from backend.models.course import Course
from backend.models.lesson import Lesson
from backend.models.question import Question
from backend.models.session import Session
from backend.models.user import User

__all__ = [
    "Answer",
    "Course",
    "Lesson",
    "Question",
    "Session",
    "StudentAnalytics",
    "User",
]

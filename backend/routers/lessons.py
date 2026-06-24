"""Роутер управления уроками."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.lesson import Lesson
from backend.schemas.course import LessonCreate, LessonRead

router = APIRouter(prefix="/api/lessons", tags=["lessons"])


@router.get("", response_model=list[LessonRead])
async def list_lessons(course_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> list[Lesson]:
    """Возвращает уроки курса, упорядоченные по индексу."""
    result = await db.execute(
        select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order_index)
    )
    return list(result.scalars().all())


@router.post("", response_model=LessonRead, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    course_id: uuid.UUID, data: LessonCreate, db: AsyncSession = Depends(get_db)
) -> Lesson:
    """Создаёт новый урок в курсе."""
    lesson = Lesson(course_id=course_id, **data.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.get("/{lesson_id}", response_model=LessonRead)
async def get_lesson(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Lesson:
    """Возвращает урок по идентификатору."""
    lesson = await db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "урок не найден")
    return lesson

"""Роутер управления курсами."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.course import Course
from backend.schemas.course import CourseCreate, CourseRead

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("", response_model=list[CourseRead])
async def list_courses(db: AsyncSession = Depends(get_db)) -> list[Course]:
    """Возвращает список всех курсов."""
    result = await db.execute(select(Course))
    return list(result.scalars().all())


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_course(
    data: CourseCreate, teacher_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Course:
    """Создаёт новый курс."""
    course = Course(title=data.title, description=data.description, teacher_id=teacher_id)
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


@router.get("/{course_id}", response_model=CourseRead)
async def get_course(course_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Course:
    """Возвращает курс по идентификатору."""
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "курс не найден")
    return course

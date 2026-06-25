"""Роутер управления вопросами к урокам."""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.question import Question
from backend.schemas.question import QuestionCreate, QuestionRead

router = APIRouter(prefix="/api/questions", tags=["questions"])


@router.get("", response_model=list[QuestionRead])
async def list_questions(
    lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[Question]:
    """Возвращает список вопросов урока."""
    result = await db.execute(select(Question).where(Question.lesson_id == lesson_id))
    return list(result.scalars().all())


@router.post("", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
async def create_question(
    lesson_id: uuid.UUID, data: QuestionCreate, db: AsyncSession = Depends(get_db)
) -> Question:
    """Создаёт новый вопрос для урока."""
    question = Question(lesson_id=lesson_id, **data.model_dump())
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question

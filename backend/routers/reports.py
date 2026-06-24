"""Роутер формирования отчётов для преподавателя."""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.answer import Answer
from backend.models.session import Session

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/lesson/{lesson_id}/summary")
async def get_lesson_summary(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> dict:
    """Возвращает сводный отчёт по уроку: число сессий и средний балл."""
    sessions_count = await db.scalar(
        select(func.count()).select_from(Session).where(Session.lesson_id == lesson_id)
    )
    average_score = await db.scalar(
        select(func.avg(Answer.score))
        .join(Session, Session.id == Answer.session_id)
        .where(Session.lesson_id == lesson_id)
    )
    return {
        "lesson_id": str(lesson_id),
        "sessions_count": sessions_count or 0,
        "average_score": float(average_score) if average_score is not None else 0.0,
    }

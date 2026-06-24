"""Роутер аналитики по студентам."""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.analytics import StudentAnalytics
from backend.schemas.analytics import StudentAnalyticsRead

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/risk/{student_id}", response_model=StudentAnalyticsRead | None)
async def get_risk_score(
    student_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> StudentAnalytics | None:
    """Возвращает последний снимок риск-оценки студента."""
    result = await db.execute(
        select(StudentAnalytics)
        .where(StudentAnalytics.student_id == student_id)
        .order_by(StudentAnalytics.recorded_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


@router.get("/history/{student_id}", response_model=list[StudentAnalyticsRead])
async def get_analytics_history(
    student_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[StudentAnalytics]:
    """Возвращает историю аналитических снимков студента."""
    result = await db.execute(
        select(StudentAnalytics)
        .where(StudentAnalytics.student_id == student_id)
        .order_by(StudentAnalytics.recorded_at)
    )
    return list(result.scalars().all())

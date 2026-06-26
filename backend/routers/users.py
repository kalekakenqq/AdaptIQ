"""Роутер профиля текущего пользователя."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.answer import Answer
from backend.models.session import Session
from backend.models.user import User
from backend.services.auth_service import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
async def read_current_user(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
) -> dict:
    """Возвращает профиль текущего пользователя и его статистику."""
    sessions_count = await db.scalar(
        select(func.count()).select_from(Session).where(Session.student_id == user.id)
    )
    avg_score = await db.scalar(
        select(func.avg(Answer.score))
        .join(Session, Session.id == Answer.session_id)
        .where(Session.student_id == user.id)
    )
    return {
        "id": str(user.id),
        "name": user.full_name,
        "email": user.email,
        "role": user.role.value,
        "created_at": user.created_at.isoformat(),
        "stats": {
            "sessions_count": sessions_count or 0,
            "avg_score": round(float(avg_score), 2) if avg_score is not None else 0.0,
        },
    }

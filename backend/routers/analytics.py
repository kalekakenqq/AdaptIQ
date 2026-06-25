"""Роутер аналитики по студентам."""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.analytics import StudentAnalytics
from backend.schemas.analytics import StudentAnalyticsRead

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

# темы курса математического анализа для графа знаний
KNOWLEDGE_TOPICS = [
    {"id": "limits", "label": "Пределы", "knowledge": 0.88, "importance": 5},
    {"id": "derivatives", "label": "Производные", "knowledge": 0.81, "importance": 5},
    {"id": "indefinite_integral", "label": "Неопределённый интеграл",
     "knowledge": 0.62, "importance": 4},
    {"id": "definite_integral", "label": "Определённый интеграл",
     "knowledge": 0.55, "importance": 4},
    {"id": "integrals", "label": "Интегралы", "knowledge": 0.49, "importance": 5},
    {"id": "taylor_series", "label": "Ряды Тейлора", "knowledge": 0.34, "importance": 4},
    {"id": "numeric_series", "label": "Числовые ряды", "knowledge": 0.41, "importance": 3},
    {"id": "diff_equations", "label": "Дифференциальные уравнения",
     "knowledge": 0.22, "importance": 5},
    {"id": "multivar_functions", "label": "Функции нескольких переменных",
     "knowledge": 0.28, "importance": 4},
    {"id": "extrema", "label": "Экстремумы", "knowledge": 0.67, "importance": 3},
    {"id": "lagrange_theorem", "label": "Теорема Лагранжа", "knowledge": 0.45, "importance": 2},
    {"id": "newton_leibniz", "label": "Формула Ньютона-Лейбница",
     "knowledge": 0.58, "importance": 3},
]

KNOWLEDGE_EDGES = [
    {"source": "limits", "target": "derivatives"},
    {"source": "derivatives", "target": "extrema"},
    {"source": "derivatives", "target": "lagrange_theorem"},
    {"source": "derivatives", "target": "indefinite_integral"},
    {"source": "indefinite_integral", "target": "definite_integral"},
    {"source": "definite_integral", "target": "integrals"},
    {"source": "definite_integral", "target": "newton_leibniz"},
    {"source": "integrals", "target": "diff_equations"},
    {"source": "derivatives", "target": "taylor_series"},
    {"source": "taylor_series", "target": "numeric_series"},
    {"source": "derivatives", "target": "multivar_functions"},
    {"source": "multivar_functions", "target": "extrema"},
]


@router.get("/knowledge-graph")
async def get_knowledge_graph() -> dict:
    """Возвращает узлы и связи графа знаний предметной области для визуализации D3.js."""
    return {"nodes": KNOWLEDGE_TOPICS, "edges": KNOWLEDGE_EDGES}


@router.get("/exam-prediction")
async def get_exam_prediction() -> dict:
    """Возвращает прогноз вероятности сдачи экзамена по неделям (симуляция LSTM)."""
    weeks = list(range(1, 11))
    probability = [0.45, 0.48, 0.52, 0.51, 0.57, 0.63, 0.66, 0.71, 0.76, 0.82]
    return {"weeks": weeks, "probability": probability, "current_week": 5}


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

"""Роутер управления учебными сессиями и ответами."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.answer import Answer
from backend.models.course import Course
from backend.models.lesson import Lesson
from backend.models.question import Question
from backend.models.session import Session
from backend.models.user import User
from backend.schemas.session import AnswerRead, AnswerSubmit, SessionCreate, SessionRead
from backend.services.adaptive_engine import select_next_lesson
from backend.services.auth_service import get_current_user

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.get("/history")
async def get_session_history(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
) -> list[dict]:
    """Возвращает историю учебных сессий текущего пользователя с деталями."""
    result = await db.execute(
        select(Session, Lesson.title, Course.title)
        .join(Lesson, Lesson.id == Session.lesson_id, isouter=True)
        .join(Course, Course.id == Lesson.course_id, isouter=True)
        .where(Session.student_id == user.id)
        .order_by(Session.started_at.desc())
    )

    history = []
    for session, lesson_title, course_title in result.all():
        avg_score = await db.scalar(
            select(func.avg(Answer.score)).where(Answer.session_id == session.id)
        )
        mistakes = await db.scalar(
            select(func.count())
            .select_from(Answer)
            .where(Answer.session_id == session.id, Answer.is_correct.is_(False))
        )
        finished = session.finished_at or datetime.now(timezone.utc)
        started = session.started_at
        duration = int((finished - started).total_seconds()) if started else 0

        history.append({
            "id": str(session.id),
            "date": session.started_at.isoformat() if session.started_at else None,
            "course": course_title or lesson_title or "Курс",
            "score": round(float(avg_score), 2) if avg_score is not None else 0.0,
            "violations": int(mistakes or 0),
            "duration_seconds": max(0, duration),
            "status": session.status.value,
        })
    return history


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
async def start_session(
    student_id: uuid.UUID, data: SessionCreate, db: AsyncSession = Depends(get_db)
) -> Session:
    """Запускает новую учебную сессию для студента."""
    session = Session(student_id=student_id, lesson_id=data.lesson_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


@router.post("/{session_id}/answer", response_model=AnswerRead)
async def submit_answer(
    session_id: uuid.UUID, data: AnswerSubmit, db: AsyncSession = Depends(get_db)
) -> Answer:
    """Принимает и оценивает ответ студента на вопрос."""
    question = await db.get(Question, data.question_id)
    if question is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "вопрос не найден")

    is_correct = data.text.strip().lower() == question.reference_answer.strip().lower()
    answer = Answer(
        session_id=session_id,
        question_id=data.question_id,
        text=data.text,
        is_correct=is_correct,
        score=1.0 if is_correct else 0.0,
    )
    db.add(answer)
    await db.commit()
    await db.refresh(answer)
    return answer


@router.get("/{session_id}/next-lesson")
async def get_next_lesson(session_id: uuid.UUID) -> dict[str, str]:
    """Возвращает рекомендацию RL-агента по следующему материалу."""
    difficulty = select_next_lesson(session_id)
    return {"recommended_difficulty": difficulty}

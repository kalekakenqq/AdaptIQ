"""Модель агрегированной аналитики по студенту."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class StudentAnalytics(Base):
    """Снимок аналитических показателей студента на момент времени."""

    __tablename__ = "student_analytics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )
    cognitive_load_index: Mapped[float] = mapped_column(Float, default=0.0)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    cluster_label: Mapped[int] = mapped_column(default=-1)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

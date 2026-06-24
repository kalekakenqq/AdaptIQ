"""Pydantic-схемы аналитики."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudentAnalyticsRead(BaseModel):
    """Представление снимка аналитики студента."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    student_id: uuid.UUID
    cognitive_load_index: float
    risk_score: float
    cluster_label: int
    recorded_at: datetime

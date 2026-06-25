"""WebSocket-роутер для стрима CV-аналитики в реальном времени."""

import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.services.cognitive_load import CognitiveSignals, compute_cognitive_load_index

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/session/{session_id}")
async def session_stream(websocket: WebSocket, session_id: str) -> None:
    """Принимает кадры CV-метрик от клиента и возвращает индекс когнитивной нагрузки."""
    await websocket.accept()
    try:
        while True:
            payload = await websocket.receive_json()
            signals = CognitiveSignals(
                emotion_stress_score=payload.get("emotion_stress_score", 0.0),
                concentration_score=payload.get("concentration_score", 0.0),
                answer_latency_seconds=payload.get("answer_latency_seconds", 0.0),
                error_rate=payload.get("error_rate", 0.0),
            )
            index = compute_cognitive_load_index(signals)
            await websocket.send_json({"session_id": session_id, "cognitive_load_index": index})
    except WebSocketDisconnect:
        logger.info("клиент отключился от сессии %s", session_id)


# вес каждого типа нарушения прокторинга в риск-скоре
VIOLATION_RISK_WEIGHTS = {
    "face_absent": 3.0,
    "face_away": 1.0,
    "multiple_faces": 5.0,
}


@router.websocket("/ws/{session_id}")
async def proctoring_stream(websocket: WebSocket, session_id: str) -> None:
    """Принимает события прокторинга от камеры и возвращает накопленный риск-скор."""
    await websocket.accept()
    risk_score = 0.0
    try:
        while True:
            payload = await websocket.receive_json()
            event_type = payload.get("type", "")
            risk_score += VIOLATION_RISK_WEIGHTS.get(event_type, 0.0)
            risk_score = max(0.0, min(10.0, risk_score))
            logger.info("прокторинг сессии %s: событие %s", session_id, event_type)
            await websocket.send_json({"session_id": session_id, "risk_score": risk_score})
    except WebSocketDisconnect:
        logger.info("клиент прокторинга отключился от сессии %s", session_id)

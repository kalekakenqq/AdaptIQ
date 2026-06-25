"""Точка входа FastAPI-приложения AdaptIQ."""

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import get_settings
from backend.database import init_db
from backend.graph_db import close_driver
from backend.routers import analytics, auth, courses, lessons, reports, sessions, ws

FRONTEND_DIST_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def _warmup_ml_components() -> None:
    """Прогревает тяжёлые ML-компоненты в фоне, не блокируя приём запросов."""
    try:
        from backend.services.adaptive_engine import _get_agent

        _get_agent()
        logger.info("rl-агент прогрет в фоне")
    except Exception:
        logger.warning("не удалось прогреть rl-агента в фоне, будет загружен по требованию")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управляет жизненным циклом приложения: быстрый старт, тяжёлая инициализация в фоне."""
    await init_db()
    asyncio.get_event_loop().run_in_executor(None, _warmup_ml_components)

    yield

    try:
        await close_driver()
    except Exception:
        logger.warning("не удалось корректно закрыть подключение к neo4j", exc_info=True)


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(sessions.router)
app.include_router(analytics.router)
app.include_router(reports.router)
app.include_router(ws.router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}


if FRONTEND_DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST_DIR, html=True), name="frontend")

"""Точка входа FastAPI-приложения AdaptIQ."""

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text

from backend.config import get_settings
from backend.database import engine, init_db
from backend.graph_db import close_driver
from backend.rate_limit import limiter
from backend.routers import (
    analytics,
    auth,
    courses,
    lessons,
    questions,
    reports,
    sessions,
    users,
    ws,
)

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

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(questions.router)
app.include_router(sessions.router)
app.include_router(analytics.router)
app.include_router(reports.router)
app.include_router(ws.router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}


@app.get("/api/health")
async def api_health_check() -> dict[str, str]:
    """Проверка работоспособности сервиса и доступности базы данных."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as exc:
        logger.warning("health check: база данных недоступна", exc_info=True)
        db_status = str(exc)
    return {"status": "ok", "db": db_status}


if FRONTEND_DIST_DIR.exists():
    app.mount(
        "/assets", StaticFiles(directory=FRONTEND_DIST_DIR / "assets"), name="frontend-assets"
    )

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str) -> FileResponse:
        """SPA fallback: отдаёт index.html для всех клиентских роутов Vue Router."""
        index_file = FRONTEND_DIST_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "frontend not found")

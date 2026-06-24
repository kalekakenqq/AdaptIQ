"""Точка входа FastAPI-приложения AdaptIQ."""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import get_settings
from backend.graph_db import close_driver
from backend.routers import analytics, auth, courses, lessons, reports, sessions, ws

FRONTEND_DIST_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

logging.basicConfig(level=logging.INFO)

settings = get_settings()

app = FastAPI(title=settings.app_name)

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


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Закрывает внешние подключения при остановке приложения."""
    await close_driver()


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}


if FRONTEND_DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST_DIR, html=True), name="frontend")

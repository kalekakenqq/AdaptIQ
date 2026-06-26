"""Роутер регистрации и входа пользователей."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.database import get_db
from backend.models.user import User
from backend.rate_limit import limiter
from backend.schemas.user import Token, UserCreate, UserLogin, UserRegisterResponse
from backend.services.auth_service import authenticate_user, create_access_token, hash_password

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.rate_limit_auth)
async def register(
    request: Request, data: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserRegisterResponse:
    """Регистрирует нового пользователя и возвращает токен доступа."""
    try:
        existing = await db.execute(select(User).where(User.email == data.email))
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "пользователь с таким email уже существует"
            )

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        logger.exception("ошибка базы данных при регистрации пользователя %s", data.email)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"ошибка базы данных: {exc}"
        ) from exc
    except Exception as exc:
        logger.exception("непредвиденная ошибка при регистрации пользователя %s", data.email)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"непредвиденная ошибка: {exc}"
        ) from exc

    token = create_access_token(subject=str(user.id), name=user.full_name, role=user.role.value)
    return UserRegisterResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        access_token=token,
    )


@router.post("/login", response_model=Token)
@limiter.limit(settings.rate_limit_auth)
async def login(request: Request, data: UserLogin, db: AsyncSession = Depends(get_db)) -> Token:
    """Выполняет вход пользователя и возвращает JWT-токен."""
    try:
        user = await authenticate_user(db, data.email, data.password)
    except SQLAlchemyError as exc:
        logger.exception("ошибка базы данных при входе пользователя %s", data.email)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"ошибка базы данных: {exc}"
        ) from exc

    if user is None:
        logger.warning("неудачная попытка входа: %s", data.email)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "неверный email или пароль")

    token = create_access_token(subject=str(user.id), name=user.full_name, role=user.role.value)
    return Token(access_token=token)

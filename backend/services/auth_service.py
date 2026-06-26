"""Сервис аутентификации и работы с JWT-токенами."""

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.database import get_db
from backend.models.user import User

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=True)


def hash_password(password: str) -> str:
    """Хэширует пароль пользователя."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля его хэшу."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, name: str = "", role: str = "") -> str:
    """Создаёт JWT-токен доступа с именем и ролью пользователя в полезной нагрузке."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "name": name, "role": role, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """Проверяет учётные данные пользователя и возвращает его при успехе."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Возвращает текущего пользователя по JWT-токену из заголовка Authorization."""
    invalid = HTTPException(status.HTTP_401_UNAUTHORIZED, "недействительный токен")
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=["HS256"])
        subject = payload.get("sub")
        if subject is None:
            raise invalid
        user_id = uuid.UUID(subject)
    except (JWTError, ValueError) as exc:
        raise invalid from exc

    user = await db.get(User, user_id)
    if user is None:
        raise invalid
    return user

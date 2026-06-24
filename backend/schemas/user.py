"""Pydantic-схемы пользователя."""

import uuid

from pydantic import BaseModel, ConfigDict, EmailStr

from backend.models.user import UserRole


class UserCreate(BaseModel):
    """Данные для регистрации пользователя."""

    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.STUDENT


class UserLogin(BaseModel):
    """Данные для входа пользователя."""

    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Публичное представление пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool


class Token(BaseModel):
    """JWT-токен доступа."""

    access_token: str
    token_type: str = "bearer"

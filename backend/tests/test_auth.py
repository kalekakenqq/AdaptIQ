"""Тесты сервиса и роутера аутентификации."""

from httpx import AsyncClient

from backend.services.auth_service import create_access_token, hash_password, verify_password


def test_hash_password_creates_verifiable_hash() -> None:
    """Хэш пароля должен успешно проверяться исходным паролем."""
    hashed = hash_password("secret123")
    assert hashed != "secret123"
    assert verify_password("secret123", hashed)


def test_verify_password_rejects_wrong_password() -> None:
    """Проверка неверного пароля должна возвращать False."""
    hashed = hash_password("secret123")
    assert not verify_password("wrong-password", hashed)


def test_create_access_token_contains_subject() -> None:
    """Токен должен корректно декодироваться и содержать subject."""
    from jose import jwt

    from backend.config import get_settings

    token = create_access_token(subject="user-123")
    payload = jwt.decode(token, get_settings().secret_key, algorithms=["HS256"])
    assert payload["sub"] == "user-123"


async def test_register_and_login(client: AsyncClient) -> None:
    """Пользователь должен успешно регистрироваться и входить в систему."""
    register_response = await client.post(
        "/api/auth/register",
        json={"email": "test@adaptiq.dev", "password": "secret123", "full_name": "Тест Тестов"},
    )
    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/auth/login", json={"email": "test@adaptiq.dev", "password": "secret123"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


async def test_login_with_wrong_password_fails(client: AsyncClient) -> None:
    """Вход с неверным паролем должен возвращать 401."""
    await client.post(
        "/api/auth/register",
        json={"email": "user2@adaptiq.dev", "password": "secret123", "full_name": "Студент"},
    )
    response = await client.post(
        "/api/auth/login", json={"email": "user2@adaptiq.dev", "password": "wrong"}
    )
    assert response.status_code == 401

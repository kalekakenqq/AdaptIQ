"""Тесты роутеров курсов и уроков."""

import uuid

from httpx import AsyncClient


async def test_create_and_get_course(client: AsyncClient) -> None:
    """Курс должен создаваться и быть доступным по идентификатору."""
    teacher_id = uuid.uuid4()
    create_response = await client.post(
        f"/api/courses?teacher_id={teacher_id}",
        json={"title": "Линейная алгебра", "description": "Базовый курс"},
    )
    assert create_response.status_code == 201
    course_id = create_response.json()["id"]

    get_response = await client.get(f"/api/courses/{course_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Линейная алгебра"


async def test_get_unknown_course_returns_404(client: AsyncClient) -> None:
    """Запрос несуществующего курса должен возвращать 404."""
    response = await client.get(f"/api/courses/{uuid.uuid4()}")
    assert response.status_code == 404


async def test_create_and_list_lessons(client: AsyncClient) -> None:
    """Уроки должны создаваться внутри курса и возвращаться по порядку."""
    teacher_id = uuid.uuid4()
    course_response = await client.post(
        f"/api/courses?teacher_id={teacher_id}", json={"title": "Курс"}
    )
    course_id = course_response.json()["id"]

    await client.post(
        f"/api/lessons?course_id={course_id}", json={"title": "Урок 1", "order_index": 0}
    )
    await client.post(
        f"/api/lessons?course_id={course_id}", json={"title": "Урок 2", "order_index": 1}
    )

    list_response = await client.get(f"/api/lessons?course_id={course_id}")
    assert list_response.status_code == 200
    lessons = list_response.json()
    assert len(lessons) == 2
    assert lessons[0]["title"] == "Урок 1"

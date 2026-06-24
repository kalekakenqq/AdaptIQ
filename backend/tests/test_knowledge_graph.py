"""Тесты сервиса работы с графом знаний Neo4j."""

from unittest.mock import AsyncMock

from backend.services.knowledge_graph import create_concept_node, get_prerequisites, link_concepts


async def test_create_concept_node_runs_merge_query() -> None:
    """Создание узла концепции должно вызывать MERGE-запрос с нужными параметрами."""
    session = AsyncMock()
    await create_concept_node(session, concept_id="c1", name="Производные")
    session.run.assert_awaited_once()
    args, kwargs = session.run.call_args
    assert "MERGE" in args[0]
    assert kwargs["concept_id"] == "c1"
    assert kwargs["name"] == "Производные"


async def test_link_concepts_runs_relationship_query() -> None:
    """Связывание концепций должно вызывать запрос создания PRECEDES-связи."""
    session = AsyncMock()
    await link_concepts(session, from_id="c1", to_id="c2")
    args, kwargs = session.run.call_args
    assert "PRECEDES" in args[0]
    assert kwargs["from_id"] == "c1"
    assert kwargs["to_id"] == "c2"


async def test_get_prerequisites_returns_list_of_ids() -> None:
    """Получение предпосылок должно возвращать список идентификаторов."""

    async def _record_generator():
        for record in [{"id": "c1"}, {"id": "c2"}]:
            yield record

    session = AsyncMock()
    session.run.return_value = _record_generator()

    result = await get_prerequisites(session, concept_id="c3")
    assert result == ["c1", "c2"]

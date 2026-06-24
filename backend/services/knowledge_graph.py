"""Работа с графом знаний предметной области в Neo4j."""

import logging

from neo4j import AsyncSession as Neo4jSession

logger = logging.getLogger(__name__)


async def create_concept_node(session: Neo4jSession, concept_id: str, name: str) -> None:
    """Создаёт узел концепции в графе знаний."""
    await session.run(
        "MERGE (c:Concept {id: $concept_id}) SET c.name = $name",
        concept_id=concept_id,
        name=name,
    )


async def link_concepts(session: Neo4jSession, from_id: str, to_id: str) -> None:
    """Создаёт связь предшествования между двумя концепциями."""
    await session.run(
        """
        MATCH (a:Concept {id: $from_id}), (b:Concept {id: $to_id})
        MERGE (a)-[:PRECEDES]->(b)
        """,
        from_id=from_id,
        to_id=to_id,
    )


async def get_prerequisites(session: Neo4jSession, concept_id: str) -> list[str]:
    """Возвращает список идентификаторов концепций-предпосылок."""
    result = await session.run(
        "MATCH (a:Concept)-[:PRECEDES]->(b:Concept {id: $concept_id}) RETURN a.id AS id",
        concept_id=concept_id,
    )
    return [record["id"] async for record in result]
